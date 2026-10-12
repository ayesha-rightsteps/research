"""
env_v4.py -- the v4 environment (Phase 1b, plan: v4/02-redesign/PLAN.md).

Starts from the v3 MultiUAVEnv (v4/common/v3_env.py, frozen) and changes only four things:
  1. Obstacles are discs of radius OBS_RADIUS (v3: points). A drone collides with a disc when its centre
     is closer than OBS_RADIUS + collision_radius to the disc centre.
  2. Obstacle sensing is a 24-ray LiDAR (v3: four axis-projected clearances). Each ray returns the distance
     to the nearest disc surface or wall, divided by the ray range. Rays are in the world frame (the
     drones are holonomic point masses with no heading).
  3. PAH's time-to-collision tau covers every hazard: tau = min(tau_drone, tau_obstacle), capped at the
     horizon. tau_drone is the v3 conflict-graph value; tau_obstacle is the number of steps until the
     drone, at its current velocity, reaches a disc's collision boundary.
  4. Targets bounce off discs as they bounce off walls, at disc radius + collision radius + 5, so a drone
     sitting on its target can never touch a disc.
Everything else is the v3 code: world size, speeds, collision radius, target radius, Hungarian
assignment every step, the drone-drone conflict graph (neighbour features and n_conflict), the reward
terms (the safety distance now uses the nearest drone OR disc surface), success definition.

Extra per-step info for logging (v4 logs diagnostics during training): collision kind, safety-reward
cause, which hazard set tau, loss-of-separation pairs, active conflict edges.
"""

import numpy as np
from scipy.optimize import linear_sum_assignment

from v3_env import ConflictGraph          # unchanged v3 drone-drone conflict graph (single copy)

K_NBR = 4
N_RAYS = 24
RAY_RANGE = 100.0
OBS_RADIUS = 12.0
TAU_HORIZON = 3.0
BASE_DIM = 6                               # own pos (2) + own vel (2) + target offset (2)
OBS_DIM = BASE_DIM + N_RAYS + K_NBR * 5    # 6 + 24 + 20 = 50
RAY_DIRS = np.stack([np.cos(np.arange(N_RAYS) * 2 * np.pi / N_RAYS),
                     np.sin(np.arange(N_RAYS) * 2 * np.pi / N_RAYS)], axis=1)   # (24, 2), 15 deg apart


def ray_distances(pos, centres, radius, world, dirs=RAY_DIRS, max_range=RAY_RANGE):
    """Distance along each ray from pos to the first disc surface or wall, capped at max_range.
    pos (2,), centres (M,2), dirs (R,2) unit vectors. Returns (R,)."""
    d = np.full(len(dirs), max_range, dtype=np.float64)
    # walls of the square [0, world]^2
    with np.errstate(divide='ignore', invalid='ignore'):
        tx = np.where(dirs[:, 0] > 0, (world - pos[0]) / dirs[:, 0],
                      np.where(dirs[:, 0] < 0, (0.0 - pos[0]) / dirs[:, 0], np.inf))
        ty = np.where(dirs[:, 1] > 0, (world - pos[1]) / dirs[:, 1],
                      np.where(dirs[:, 1] < 0, (0.0 - pos[1]) / dirs[:, 1], np.inf))
    d = np.minimum(d, np.minimum(tx, ty))
    if len(centres):
        oc = pos[None, :] - centres                       # (M,2)
        b = dirs @ oc.T                                   # (R,M)  d . (p - c)
        cc = (oc ** 2).sum(axis=1) - radius ** 2          # (M,)
        disc = b ** 2 - cc[None, :]
        hit = disc >= 0
        t = -b - np.sqrt(np.where(hit, disc, 0.0))        # nearest intersection
        inside = cc[None, :] < 0                          # pos inside a disc (only possible after a collision)
        t = np.where(inside, 0.0, t)
        valid = hit & (t >= 0)
        t = np.where(valid, t, np.inf)
        d = np.minimum(d, t.min(axis=1))
    return np.clip(d, 0.0, max_range)


def time_to_disc(pos, vel, centres, boundary, horizon=TAU_HORIZON):
    """Steps until pos moving at vel (per step) reaches the nearest disc boundary (radius `boundary`),
    capped at horizon. 0 if already inside; horizon if not moving or no disc ahead within horizon."""
    if len(centres) == 0:
        return horizon
    oc = pos[None, :] - centres
    cc = (oc ** 2).sum(axis=1) - boundary ** 2
    if (cc <= 0).any():
        return 0.0
    vv = float(vel @ vel)
    if vv < 1e-8:
        return horizon
    b = oc @ vel                                          # (M,)
    disc = b ** 2 - vv * cc
    hit = (disc >= 0) & (b < 0)                           # moving towards the disc
    if not hit.any():
        return horizon
    t = (-b[hit] - np.sqrt(disc[hit])) / vv
    return float(min(t.min(), horizon))


class MultiUAVEnvV4:
    def __init__(self, n_drones=5, n_obstacles=20, world_size=500.0,
                 max_speed=5.0, max_steps=500, collision_radius=3.0,
                 target_radius=25.0, success_bonus=20.0, target_speed=1.0,
                 obstacle_radius=OBS_RADIUS, use_hungarian=True, seed=None,
                 safety_danger_radius=None, collision_penalty=1.0):
        self.n = n_drones
        self.n_obs = n_obstacles
        self.W = world_size
        self.max_sp = max_speed
        self.max_steps = max_steps
        self.col_r = collision_radius
        self.tgt_r = target_radius
        self.bonus = success_bonus
        self.tgt_speed = target_speed
        self.obs_r = obstacle_radius
        self.use_hungarian = use_hungarian
        # safety-reward shape (Phase 1b Step 3 tuning knobs). Defaults = v3: shaping starts 3 x collision
        # radius from the nearest drone / disc surface, and a collision gives r_safety = -1.
        self.safety_danger_r = collision_radius * 3.0 if safety_danger_radius is None else safety_danger_radius
        self.collision_penalty = collision_penalty
        self.rng = np.random.default_rng(seed)
        self.cg = ConflictGraph(n_drones, horizon=TAU_HORIZON, d_danger=collision_radius * 3.0)
        self.obs_dim = OBS_DIM
        self.act_dim = 2

    # ---------------------------------------------------------------- reset / step
    def reset(self):
        self.t = 0
        self.collision_occurred = False
        self.collision_kind = ''
        all_pos = self._sample_non_overlapping(self.n * 2, self.col_r * 2)
        self.drone_pos = all_pos[:self.n].copy()
        self.target_pos = all_pos[self.n:].copy()
        self.obstacle_pos = self._place_discs(np.concatenate([self.drone_pos, self.target_pos]), self.n_obs)
        self.drone_vel = np.zeros((self.n, 2), dtype=np.float32)
        angles = self.rng.uniform(0, 2 * np.pi, self.n)
        self.target_vel = (self.tgt_speed * np.stack([np.cos(angles), np.sin(angles)], axis=1)).astype(np.float32)
        self.assignment = self._hungarian() if self.use_hungarian else np.arange(self.n)
        self.cg.update(self.drone_pos, self.drone_vel)
        return self._obs()

    def step(self, actions):
        self.t += 1
        actions = np.clip(actions, -self.max_sp, self.max_sp)
        self.drone_vel = actions.astype(np.float32)
        self.drone_pos = np.clip(self.drone_pos + self.drone_vel, 0.0, self.W)
        self._move_targets()
        if self.use_hungarian:
            self.assignment = self._hungarian()
        self.cg.update(self.drone_pos, self.drone_vel)

        rewards, r_mission, r_safety, near_drone, near_obs = self._rewards()
        all_reached = self._all_reached()
        kind = self._collision_kind()
        any_collision = kind != ''
        timeout = self.t >= self.max_steps
        if any_collision and not self.collision_occurred:
            self.collision_occurred = True
            self.collision_kind = kind
        terminated = all_reached or any_collision
        truncated = timeout
        if all_reached and self.bonus:
            rewards = rewards + self.bonus
            r_mission = r_mission + self.bonus

        tau_d = np.array([self.cg.tau_collision(i) for i in range(self.n)], dtype=np.float32)
        tau_o = np.array([time_to_disc(self.drone_pos[i], self.drone_vel[i], self.obstacle_pos,
                                       self.obs_r + self.col_r) for i in range(self.n)], dtype=np.float32)
        tau = np.minimum(tau_d, tau_o)
        pah_inputs = {
            'tau': tau,
            'd_target': np.array([np.linalg.norm(self.drone_pos[i] - self.target_pos[self.assignment[i]])
                                  for i in range(self.n)], dtype=np.float32),
            'n_conflict': np.array([self.cg.n_conflict(i) for i in range(self.n)], dtype=np.float32),
        }
        iu = np.triu_indices(self.n, 1)
        pd = self._pair_dist()
        info = {
            'all_targets_reached': all_reached,
            'any_collision': any_collision,
            'episode_collision': self.collision_occurred,
            'collision_kind': self.collision_kind,          # '', 'drone-drone', 'drone-obstacle', 'both'
            'r_mission': r_mission,
            'r_safety': r_safety,
            'pah_inputs': pah_inputs,
            'tau_drone': tau_d, 'tau_obstacle': tau_o,
            'safety_cause_drone': near_drone, 'safety_cause_obstacle': near_obs,
            'los_pairs': int((pd[iu] < self.col_r * 3.0).sum()),
            'active_edges': int(self.cg.adj[iu].sum()),
        }
        return self._obs(), rewards, terminated, truncated, info

    # ---------------------------------------------------------------- pieces
    def _pair_dist(self):
        d = np.linalg.norm(self.drone_pos[:, None, :] - self.drone_pos[None, :, :], axis=-1)
        np.fill_diagonal(d, np.inf)
        return d

    def _disc_clearance(self):
        """Distance from each drone centre to the nearest disc SURFACE (inf if no discs)."""
        if len(self.obstacle_pos) == 0:
            return np.full(self.n, np.inf)
        c = np.linalg.norm(self.drone_pos[:, None, :] - self.obstacle_pos[None, :, :], axis=-1)
        return c.min(axis=1) - self.obs_r

    def _obs(self):
        obs = np.zeros((self.n, self.obs_dim), dtype=np.float32)
        for i in range(self.n):
            rel = self.target_pos[self.assignment[i]] - self.drone_pos[i]
            rays = ray_distances(self.drone_pos[i].astype(np.float64), self.obstacle_pos.astype(np.float64),
                                 self.obs_r, self.W) / RAY_RANGE
            base = np.concatenate([self.drone_pos[i] / self.W, self.drone_vel[i] / self.max_sp, rel / self.W, rays])
            nbr = self.cg.neighbor_obs(i, self.drone_pos, self.drone_vel)
            for s in range(K_NBR):
                nbr[s * 5: s * 5 + 2] /= self.W
                nbr[s * 5 + 2: s * 5 + 4] /= self.max_sp
            obs[i] = np.concatenate([base, nbr])
        return obs

    def _rewards(self):
        """v3 reward terms; the safety distance is the nearest drone centre OR disc surface."""
        r_mission = np.zeros(self.n, dtype=np.float32)
        r_safety = np.zeros(self.n, dtype=np.float32)
        d_danger = self.safety_danger_r
        zone_w = d_danger - self.col_r
        pd = self._pair_dist().min(axis=1)
        dc = self._disc_clearance()
        for i in range(self.n):
            rel = self.target_pos[self.assignment[i]] - self.drone_pos[i]
            dist = np.linalg.norm(rel)
            direction = rel / (dist + 1e-6)
            r_progress = float(np.dot(self.drone_vel[i], direction) / self.max_sp)
            r_mission[i] = 0.4 * r_progress + 0.3 * (-dist / self.W)
            min_d = min(pd[i], dc[i])
            if min_d < self.col_r:
                r_safety[i] = -self.collision_penalty
            elif min_d < d_danger:
                r_safety[i] = -((d_danger - min_d) / zone_w)
        rewards = r_mission + 0.3 * r_safety
        return rewards, r_mission, r_safety, pd < d_danger, dc < d_danger

    def _collision_kind(self):
        dd = (self._pair_dist() < self.col_r).any()
        do = (self._disc_clearance() < self.col_r).any()
        return 'both' if (dd and do) else 'drone-drone' if dd else 'drone-obstacle' if do else ''

    def _move_targets(self):
        self.target_pos = self.target_pos + self.target_vel
        for k in range(self.n):
            for dim in range(2):                              # walls (as v3)
                if self.target_pos[k, dim] < 10.0:
                    self.target_pos[k, dim] = 10.0
                    self.target_vel[k, dim] *= -1.0
                elif self.target_pos[k, dim] > self.W - 10.0:
                    self.target_pos[k, dim] = self.W - 10.0
                    self.target_vel[k, dim] *= -1.0
            # discs (new): reflect at a clearance big enough that a drone sitting ON its target can never touch
            # the disc (disc radius + collision radius + 5). Fix 2026-10-12: the first version reflected at
            # the disc radius only, so targets dragged hovering drones into discs.
            clear_r = self.obs_r + self.col_r + 5.0
            for c in self.obstacle_pos:
                off = self.target_pos[k] - c
                dist = float(np.linalg.norm(off))
                if dist < clear_r:
                    nrm = off / dist if dist > 1e-6 else np.array([1.0, 0.0], dtype=np.float32)
                    vn = float(self.target_vel[k] @ nrm)
                    if vn < 0:
                        self.target_vel[k] = self.target_vel[k] - 2 * vn * nrm
                    self.target_pos[k] = c + nrm * clear_r

    def _hungarian(self):
        cost = np.linalg.norm(self.drone_pos[:, None, :] - self.target_pos[None, :, :], axis=-1)
        _, col = linear_sum_assignment(cost)
        return col

    def _all_reached(self):
        return all(np.linalg.norm(self.drone_pos[i] - self.target_pos[self.assignment[i]]) <= self.tgt_r
                   for i in range(self.n))

    def _sample_non_overlapping(self, n, min_dist):
        pts, attempts = [], 0
        while len(pts) < n:
            attempts += 1
            if attempts > 10000:
                raise RuntimeError('World too crowded.')
            c = self.rng.uniform(10.0, self.W - 10.0, 2)
            if not any(np.linalg.norm(c - p) < min_dist for p in pts):
                pts.append(c)
        return np.array(pts, dtype=np.float32)

    def _place_discs(self, existing, n_obs, max_tries=2000):
        """Discs do not overlap each other and keep a clear margin around every drone start and target
        (a drone never starts inside or touching a disc)."""
        if n_obs <= 0:
            return np.zeros((0, 2), dtype=np.float32)
        margin = self.obs_r + self.col_r + 5.0
        placed = []
        for _ in range(n_obs):
            for _ in range(max_tries):
                c = self.rng.uniform(self.obs_r, self.W - self.obs_r, 2)
                if any(np.linalg.norm(c - o) < 2 * self.obs_r + 2.0 for o in placed):
                    continue
                if any(np.linalg.norm(c - p) < margin for p in existing):
                    continue
                placed.append(c)
                break
            else:
                raise RuntimeError('could not place disc {} of {}'.format(len(placed) + 1, n_obs))
        return np.array(placed, dtype=np.float32)
