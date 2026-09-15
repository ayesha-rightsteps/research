import numpy as np
import gymnasium as gym
from gymnasium import spaces
from scipy.optimize import linear_sum_assignment

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from algorithms.conflict_graph import ConflictGraph

K_NBR = 4   # fixed number of conflict-neighbor slots in observation


class MultiUAVEnv(gym.Env):
    """
    2D multi-UAV environment.
    N drones must reach N targets without colliding with each other or obstacles.

    Observation per drone (when use_conflict_graph=True):
        pos(2) + vel(2) + rel_target(2) + clearances(4)
        + K_NBR * [rel_pos(2) + rel_vel(2) + mask(1)]  = 10 + 20 = 30 dims

    Observation per drone (when use_conflict_graph=False):
        pos(2) + vel(2) + rel_target(2) + clearances(4) = 10 dims
    """

    def __init__(self, n_drones=3, n_obstacles=3, world_size=100.0,
                 max_speed=5.0, max_steps=300, collision_radius=3.0,
                 target_radius=5.0, use_conflict_graph=True,
                 horizon=3.0, success_bonus=0.0, use_hungarian=True,
                 seed=None):

        super().__init__()

        self.n_drones            = n_drones
        self.n_obstacles         = n_obstacles
        self.world_size          = world_size
        self.max_speed           = max_speed
        self.max_steps           = max_steps
        self.collision_radius    = collision_radius
        self.target_radius       = target_radius
        self.use_conflict_graph  = use_conflict_graph
        self.success_bonus       = success_bonus
        # Ablation switch (see docs/research/03_baseline_specs.md, baseline B1):
        # True  = per-step optimal Hungarian assignment (default, matches DA-MAPPO)
        # False = fixed identity pairing decided once at reset(), never re-solved —
        #         used to test whether the assignment mechanism actually matters.
        # Ported from code/notebooks/v3/ablation/kaggle_stage1_ablation.ipynb (2026-09-15)
        # so this capability lives in tested code, not only in a throwaway notebook.
        self.use_hungarian       = use_hungarian

        # Observation size depends on whether conflict graph is used
        # Base: pos(2) + vel(2) + rel_target(2) + clearances(4) = 10
        # + conflict neighbors: K_NBR * 5 = 20
        self._base_obs_dim = 10
        obs_dim = self._base_obs_dim + (K_NBR * 5 if use_conflict_graph else 0)

        self.observation_space = spaces.Box(
            low=-np.inf, high=np.inf,
            shape=(n_drones, obs_dim), dtype=np.float32
        )

        if use_conflict_graph:
            self.cg = ConflictGraph(
                n_drones=n_drones,
                horizon=horizon,
                d_danger=collision_radius * 3.0,
                k_nbr=K_NBR,
            )
        else:
            self.cg = None

        # Action: (vx, vy) velocity command per drone, clipped to max_speed
        self.action_space = spaces.Box(
            low=-max_speed, high=max_speed,
            shape=(n_drones, 2), dtype=np.float32
        )

        self.rng = np.random.default_rng(seed)
        self.drone_pos   = None
        self.drone_vel   = None
        self.target_pos  = None
        self.obstacle_pos = None
        self.assignment  = None   # assignment[i] = index of target assigned to drone i
        self.step_count  = 0

    # ------------------------------------------------------------------
    # RESET
    # ------------------------------------------------------------------
    def reset(self, seed=None, options=None):
        if seed is not None:
            self.rng = np.random.default_rng(seed)

        self.step_count = 0

        # Place drones and targets randomly, keeping them apart
        all_positions = self._sample_non_overlapping(
            self.n_drones + self.n_drones,
            min_dist=self.collision_radius * 2
        )

        self.drone_pos    = all_positions[:self.n_drones].copy()
        self.target_pos   = all_positions[self.n_drones:2*self.n_drones].copy()
        self.obstacle_pos = self._place_obstacles_poisson(
            np.concatenate([self.drone_pos, self.target_pos]), self.n_obstacles
        )
        self.drone_vel    = np.zeros((self.n_drones, 2), dtype=np.float32)

        # Ablation: fixed identity pairing (drone i -> target i) when Hungarian is
        # off. Positions are sampled in arbitrary order, so this is a genuine
        # (usually non-optimal) pairing, not a disguised optimal one.
        self.assignment = (
            self._hungarian_assignment() if self.use_hungarian
            else np.arange(self.n_drones)
        )

        if self.cg is not None:
            self.cg.update(self.drone_pos, self.drone_vel)

        return self._get_obs(), {}

    # ------------------------------------------------------------------
    # STEP
    # ------------------------------------------------------------------
    def step(self, actions):
        self.step_count += 1

        # Apply velocity commands (clip to max_speed)
        actions = np.clip(actions, -self.max_speed, self.max_speed)
        self.drone_vel = actions.astype(np.float32)
        self.drone_pos = self.drone_pos + self.drone_vel

        # Keep drones inside the world
        self.drone_pos = np.clip(self.drone_pos, 0.0, self.world_size)

        # Reassign targets every step (DA-MAPPO style) — unless the ablation
        # flag is off, in which case the assignment fixed at reset() is kept.
        if self.use_hungarian:
            self.assignment = self._hungarian_assignment()

        # Update conflict graph with new positions and velocities
        if self.cg is not None:
            self.cg.update(self.drone_pos, self.drone_vel)

        # ---- rewards -------------------------------------------------
        rewards, r_mission, r_safety = self._compute_rewards()

        # ---- termination --------------------------------------------
        all_reached    = self._all_targets_reached()
        any_collision  = self._any_collision()
        timeout        = self.step_count >= self.max_steps
        terminated     = all_reached or any_collision
        truncated      = timeout

        # Success bonus: a one-time reward when every drone reaches its target.
        # Validated empirically (2026-09-15, v2->v4 Kaggle runs): without it,
        # Stage-1 training got 0% success for 3000+ episodes — a purely
        # distance-shaped reward gives the policy no reason to actually arrive
        # and hold, vs. hovering nearby. Added to r_mission (a mission outcome,
        # not a safety one) so it flows into the PAH-weighted reward correctly.
        if all_reached and self.success_bonus:
            r_mission = r_mission + self.success_bonus
            rewards   = rewards + self.success_bonus

        info = {
            "all_targets_reached": all_reached,
            "any_collision":       any_collision,
            "timeout":             timeout,
            "step":                self.step_count,
            # Separate reward components — PAH uses these during PPO update
            "r_mission":           r_mission,
            "r_safety":            r_safety,
        }

        # PAH inputs — only when conflict graph is active (Stage 2+)
        if self.cg is not None:
            info["pah_inputs"] = {
                "tau":       np.array([self.cg.tau_collision(i) for i in range(self.n_drones)], dtype=np.float32),
                "d_target":  np.array([
                    np.linalg.norm(self.drone_pos[i] - self.target_pos[self.assignment[i]])
                    for i in range(self.n_drones)
                ], dtype=np.float32),
                "n_conflict": np.array([self.cg.n_conflict(i) for i in range(self.n_drones)], dtype=np.float32),
            }

        return self._get_obs(), rewards, terminated, truncated, info

    # ------------------------------------------------------------------
    # OBSERVATION
    # ------------------------------------------------------------------
    def _get_obs(self):
        obs_dim = self.observation_space.shape[1]
        obs = np.zeros((self.n_drones, obs_dim), dtype=np.float32)
        for i in range(self.n_drones):
            target_idx = self.assignment[i]
            rel_target = self.target_pos[target_idx] - self.drone_pos[i]
            clearances = self._obstacle_clearances(i)

            base = np.concatenate([
                self.drone_pos[i] / self.world_size,    # 2  — own position      [0, 1]
                self.drone_vel[i] / self.max_speed,     # 2  — own velocity      [-1, 1]
                rel_target        / self.world_size,    # 2  — relative target   [-1, 1]
                clearances,                             # 4  — clearances (already [0,1])
            ])                                          # = 10 total

            if self.cg is not None:
                nbr_obs = self.cg.neighbor_obs(i, self.drone_pos, self.drone_vel)
                obs[i] = np.concatenate([base, nbr_obs])   # 10 + 20 = 30
            else:
                obs[i] = base                              # 10

        return obs

    # ------------------------------------------------------------------
    # REWARDS
    # ------------------------------------------------------------------
    def _compute_rewards(self):
        """
        Returns (rewards, r_mission, r_safety) — all shape (n_drones,).

        r_mission : 0.4 * r_progress + 0.3 * (negative normalised distance)
                      r_progress = velocity component toward the assigned
                      target, normalised to [-1, 1]. Added 2026-09-15 after
                      Stage-1 training got 0% success for 3000+ episodes on a
                      pure distance penalty: a policy gets no reward for
                      *moving the right way*, only for *already being close*,
                      which gives almost no gradient early in training. See
                      sessions/2026-09-15.md Part 2 for the diagnosis.
        r_safety  : graded collision / proximity penalty, in [-1, 0]
                      -1.0  on actual collision (hard boundary)
                      linear ramp toward -1 inside the danger zone
                       0    when clear of all threats

        The danger zone spans [collision_radius, 3 × collision_radius].
        A graded r_safety gives PAH a useful gradient signal before a
        collision happens — a binary -1-on-contact gives no signal during
        the approach phase, which starves PAH of training signal.

        `rewards` is the validated fixed-weight combination used when PAH is
        OFF (Stage 1): `r_mission + 0.3 * r_safety`, matching the formula
        empirically validated in code/notebooks/v3/v3-output (100% success,
        0% collision over 5000 episodes). When PAH is ON, the caller ignores
        `rewards` and instead combines `r_mission` / `r_safety` with a
        learned α — see algorithms/pah.py.
        """
        r_mission  = np.zeros(self.n_drones, dtype=np.float32)
        r_safety   = np.zeros(self.n_drones, dtype=np.float32)
        d_danger   = self.collision_radius * 3.0
        zone_width = d_danger - self.collision_radius

        for i in range(self.n_drones):
            # ---- mission: progress toward target + negative distance ----
            target_idx = self.assignment[i]
            rel_target = self.target_pos[target_idx] - self.drone_pos[i]
            dist       = np.linalg.norm(rel_target)
            r_dist     = -dist / self.world_size

            direction  = rel_target / (dist + 1e-6)   # unit vector to target
            r_progress = float(np.dot(self.drone_vel[i], direction) / self.max_speed)

            r_mission[i] = 0.4 * r_progress + 0.3 * r_dist

            # ---- safety: closest threatening object (drone or obstacle) ----
            min_dist = float('inf')

            for j in range(self.n_drones):
                if j == i:
                    continue
                min_dist = min(min_dist,
                               np.linalg.norm(self.drone_pos[i] - self.drone_pos[j]))

            for obs_pos in self.obstacle_pos:   # empty loop when n_obstacles == 0
                min_dist = min(min_dist,
                               np.linalg.norm(self.drone_pos[i] - obs_pos))

            if min_dist < self.collision_radius:
                r_safety[i] = -1.0                                   # hard collision
            elif min_dist < d_danger:
                r_safety[i] = -((d_danger - min_dist) / zone_width) # graded proximity

        # Validated fixed-weight combination for the no-PAH (Stage 1) path.
        rewards = r_mission + 0.3 * r_safety
        return rewards, r_mission, r_safety

    # ------------------------------------------------------------------
    # HUNGARIAN ASSIGNMENT
    # ------------------------------------------------------------------
    def _hungarian_assignment(self):
        cost = np.zeros((self.n_drones, self.n_drones))
        for i in range(self.n_drones):
            for j in range(self.n_drones):
                cost[i, j] = np.linalg.norm(self.drone_pos[i] - self.target_pos[j])
        _, col_ind = linear_sum_assignment(cost)
        return col_ind   # assignment[i] = target index for drone i

    # ------------------------------------------------------------------
    # COLLISION CHECKS
    # ------------------------------------------------------------------
    def _drone_collision(self, drone_idx):
        for j in range(self.n_drones):
            if j == drone_idx:
                continue
            dist = np.linalg.norm(self.drone_pos[drone_idx] - self.drone_pos[j])
            if dist < self.collision_radius:
                return True
        return False

    def _obstacle_collision(self, drone_idx):
        for obs_pos in self.obstacle_pos:
            dist = np.linalg.norm(self.drone_pos[drone_idx] - obs_pos)
            if dist < self.collision_radius:
                return True
        return False

    def _any_collision(self):
        for i in range(self.n_drones):
            if self._drone_collision(i) or self._obstacle_collision(i):
                return True
        return False

    # ------------------------------------------------------------------
    # TARGET REACHED
    # ------------------------------------------------------------------
    def _all_targets_reached(self):
        for i in range(self.n_drones):
            target_idx = self.assignment[i]
            dist = np.linalg.norm(self.drone_pos[i] - self.target_pos[target_idx])
            if dist > self.target_radius:
                return False
        return True

    # ------------------------------------------------------------------
    # OBSTACLE CLEARANCE (4 directions)
    # ------------------------------------------------------------------
    def _obstacle_clearances(self, drone_idx):
        pos = self.drone_pos[drone_idx]
        clearances = np.array([
            self.world_size,   # North
            self.world_size,   # South
            self.world_size,   # East
            self.world_size,   # West
        ], dtype=np.float32)

        # World boundary clearances
        clearances[0] = min(clearances[0], self.world_size - pos[1])  # North
        clearances[1] = min(clearances[1], pos[1])                    # South
        clearances[2] = min(clearances[2], self.world_size - pos[0])  # East
        clearances[3] = min(clearances[3], pos[0])                    # West

        # Obstacle clearances
        for obs in self.obstacle_pos:
            diff = obs - pos
            dist = np.linalg.norm(diff)
            if dist < 1e-6:
                continue
            if diff[1] > 0:
                clearances[0] = min(clearances[0], diff[1])   # North
            else:
                clearances[1] = min(clearances[1], -diff[1])  # South
            if diff[0] > 0:
                clearances[2] = min(clearances[2], diff[0])   # East
            else:
                clearances[3] = min(clearances[3], -diff[0])  # West

        return clearances / self.world_size   # normalize to [0, 1]

    # ------------------------------------------------------------------
    # HELPER: sample positions that are not too close to each other
    # (used for drones + targets)
    # ------------------------------------------------------------------
    def _sample_non_overlapping(self, n, min_dist):
        positions = []
        attempts  = 0
        while len(positions) < n:
            attempts += 1
            if attempts > 10000:
                raise RuntimeError("Could not place all objects — world too crowded.")
            candidate = self.rng.uniform(10.0, self.world_size - 10.0, size=2)
            too_close = any(
                np.linalg.norm(candidate - p) < min_dist for p in positions
            )
            if not too_close:
                positions.append(candidate)
        return np.array(positions, dtype=np.float32)

    # ------------------------------------------------------------------
    # HELPER: Poisson-disk obstacle placement
    # (docs/research/00_problem_formalization.md Section 2.2)
    # ------------------------------------------------------------------
    def _place_obstacles_poisson(self, existing_points, n_obstacles,
                                  margin=10.0, max_tries=1000):
        """
        Place `n_obstacles` circles such that every obstacle is at least
        `2 * collision_radius` from every other obstacle, and at least
        `collision_radius` from every drone/target position already placed.

        Uses `collision_radius` as the stand-in for the design doc's `d_safe`
        (the codebase does not currently distinguish d_safe from d_col — see
        docs/research/00_problem_formalization.md Section 8 parameter table).

        Rejection-samples each obstacle up to `max_tries` times. If a valid
        spot can't be found (world too crowded), that obstacle is skipped
        rather than raising — matches the documented "reduce K silently"
        behaviour. Returns an (n, 2) array with n <= n_obstacles.
        """
        if n_obstacles <= 0:
            return np.zeros((0, 2), dtype=np.float32)

        r_obs_min = 2.0 * self.collision_radius
        obstacles = []

        for _ in range(n_obstacles):
            for _attempt in range(max_tries):
                candidate = self.rng.uniform(margin, self.world_size - margin, size=2)
                if any(np.linalg.norm(candidate - o) < r_obs_min for o in obstacles):
                    continue
                if any(np.linalg.norm(candidate - p) < self.collision_radius
                       for p in existing_points):
                    continue
                obstacles.append(candidate)
                break
            else:
                break   # couldn't place this one within max_tries — stop, don't raise

        if not obstacles:
            return np.zeros((0, 2), dtype=np.float32)
        return np.array(obstacles, dtype=np.float32)
