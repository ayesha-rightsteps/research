"""
v3_env.py -- ONE frozen copy of the v3 environment + networks, used ONLY to
evaluate the already-trained v3 models (read-only). Not the v4 environment.

Provenance (extracted programmatically, not retyped, on 2026-10-12):
  * ConflictGraph, MultiUAVEnv, Actor  <- v3/results-table/paper_style_results.ipynb
    cells 2, 3, 4 (this copy reproduced the v3 results table, e.g. M Stage 3 = 72.0%).
    Stage 2 and Stage 3 share this code; only n_drones / n_obstacles differ.
  * PAHNormalizer, PriorityArbitrationHead <- v3/stage3/var-alpha/
    kaggle_stage3_pah_seed42test.ipynb cell 4 (Stage 2 v3-pah-change uses the
    same class and the same settings: horizon 3.0, d_max 500*sqrt(2), alpha 0.1-0.9,
    delta_scale 0.2).
  * Critic, RolloutBuffer (added 2026-10-12 for the advantage-correlation check) <- the same
    stage3/var-alpha cell 4, verbatim. All six v3 training notebooks share this RolloutBuffer logic and
    the same update() (checked: identical update() source; the Stage 2 Fixed-weight notebook's buffer
    differs only in comment punctuation).

Do not edit the copied classes. If v4 changes the environment, that goes in a
new file, so v3 models keep being evaluated on exactly the code they trained on.
"""

import numpy as np
import torch
import torch.nn as nn
from torch.distributions import Normal
from scipy.optimize import linear_sum_assignment

DEVICE = torch.device('cpu')

# ---- ConflictGraph (verbatim) ----
def _time_to_cpa(pos_i, pos_j, vel_i, vel_j):
    p = pos_i - pos_j
    v = vel_i - vel_j
    vv = np.dot(v, v)
    if vv < 1e-8:
        return np.inf
    return -np.dot(p, v) / vv

def _dist_at_cpa(pos_i, pos_j, vel_i, vel_j, horizon):
    p = pos_i - pos_j
    v = vel_i - vel_j
    vv = np.dot(v, v)
    if vv < 1e-8:
        return float(np.linalg.norm(p)), 0.0
    t_star = -np.dot(p, v) / vv
    t_clamped = float(np.clip(t_star, 0.0, horizon))
    return float(np.linalg.norm(p + v * t_clamped)), t_star

class ConflictGraph:
    K_NBR = 4

    def __init__(self, n_drones, horizon=3.0, d_danger=9.0):
        self.n      = n_drones
        self.H      = horizon
        self.d_dan  = d_danger
        self.adj    = np.zeros((n_drones, n_drones), dtype=bool)
        self.t_mat  = np.full((n_drones, n_drones), np.inf)

    def update(self, pos, vel):
        self.adj[:] = False
        self.t_mat[:] = np.inf
        for i in range(self.n):
            for j in range(i + 1, self.n):
                dcpa, t_star = _dist_at_cpa(pos[i], pos[j], vel[i], vel[j], self.H)
                self.t_mat[i, j] = self.t_mat[j, i] = t_star
                if dcpa < self.d_dan and 0.0 <= t_star <= self.H:
                    self.adj[i, j] = self.adj[j, i] = True

    def n_conflict(self, i):
        return int(self.adj[i].sum())

    def tau_collision(self, i):
        nbrs = np.where(self.adj[i])[0]
        if len(nbrs) == 0:
            return self.H
        return float(np.min(self.t_mat[i, nbrs]))

    def neighbor_obs(self, i, pos, vel):
        obs = np.zeros(self.K_NBR * 5, dtype=np.float32)
        nbrs = np.where(self.adj[i])[0]
        if len(nbrs) == 0:
            return obs
        order = np.argsort(self.t_mat[i, nbrs])
        nbrs  = nbrs[order]
        for slot, j in enumerate(nbrs[:self.K_NBR]):
            b = slot * 5
            obs[b:b+2]   = pos[j] - pos[i]
            obs[b+2:b+4] = vel[j] - vel[i]
            obs[b+4]     = 1.0
        return obs

# ---- MultiUAVEnv (verbatim) ----
K_NBR    = 4
BASE_DIM = 10
OBS_DIM  = BASE_DIM + K_NBR * 5  # 30

class MultiUAVEnv:
    def __init__(self, n_drones=5, n_obstacles=5, world_size=500.0,
                 max_speed=5.0, max_steps=500, collision_radius=3.0,
                 target_radius=25.0, success_bonus=20.0,
                 target_speed=1.0, use_hungarian=True, seed=None):
        self.n         = n_drones
        self.n_obs     = n_obstacles
        self.W         = world_size
        self.max_sp    = max_speed
        self.max_steps = max_steps
        self.col_r     = collision_radius
        self.tgt_r     = target_radius
        self.bonus     = success_bonus
        self.tgt_speed = target_speed
        # Ablation switch (see Cell 0): True = per-step optimal Hungarian
        # assignment (normal). False = fixed pairing decided once at
        # reset(), never re-solved.
        self.use_hungarian = use_hungarian
        self.rng       = np.random.default_rng(seed)
        self.cg        = ConflictGraph(n_drones, horizon=3.0,
                                       d_danger=collision_radius * 3.0)
        self.obs_dim   = OBS_DIM
        self.act_dim   = 2

    def reset(self):
        self.t                  = 0
        self.collision_occurred = False
        all_pos = self._sample_non_overlapping(self.n * 2, self.col_r * 2)
        self.drone_pos  = all_pos[:self.n].copy()
        self.target_pos = all_pos[self.n:].copy()
        self.obstacle_pos = self._place_obstacles(
            np.concatenate([self.drone_pos, self.target_pos]), self.n_obs
        )
        self.drone_vel = np.zeros((self.n, 2), dtype=np.float32)
        angles = self.rng.uniform(0, 2 * np.pi, self.n)
        self.target_vel = (self.tgt_speed * np.stack(
            [np.cos(angles), np.sin(angles)], axis=1
        )).astype(np.float32)
        # Ablation: fixed pairing (arbitrary) when Hungarian is off -- never
        # re-solved, even though targets keep moving. See Cell 0.
        self.assignment = self._hungarian() if self.use_hungarian else np.arange(self.n)
        self.cg.update(self.drone_pos, self.drone_vel)
        return self._obs()

    def step(self, actions):
        self.t += 1
        actions = np.clip(actions, -self.max_sp, self.max_sp)
        self.drone_vel = actions.astype(np.float32)
        self.drone_pos = np.clip(self.drone_pos + self.drone_vel, 0.0, self.W)

        self.target_pos = self.target_pos + self.target_vel
        for k in range(self.n):
            for dim in range(2):
                if self.target_pos[k, dim] < 10.0:
                    self.target_pos[k, dim] = 10.0
                    self.target_vel[k, dim] *= -1.0
                elif self.target_pos[k, dim] > self.W - 10.0:
                    self.target_pos[k, dim] = self.W - 10.0
                    self.target_vel[k, dim] *= -1.0

        # Ablation: keep the reset()-time assignment fixed when Hungarian is
        # off -- re-solved every step only in the normal (True) case.
        if self.use_hungarian:
            self.assignment = self._hungarian()
        self.cg.update(self.drone_pos, self.drone_vel)

        rewards, r_mission, r_safety = self._rewards()
        all_reached   = self._all_reached()
        any_collision = self._any_collision()
        timeout       = self.t >= self.max_steps

        if any_collision:
            self.collision_occurred = True

        terminated = all_reached or any_collision
        truncated  = timeout

        if all_reached and self.bonus:
            rewards   = rewards + self.bonus
            r_mission = r_mission + self.bonus   # bonus is a mission outcome, not safety

        # PAH inputs — per drone, from the conflict graph + current assignment.
        pah_inputs = {
            'tau': np.array([self.cg.tau_collision(i) for i in range(self.n)], dtype=np.float32),
            'd_target': np.array([
                np.linalg.norm(self.drone_pos[i] - self.target_pos[self.assignment[i]])
                for i in range(self.n)
            ], dtype=np.float32),
            'n_conflict': np.array([self.cg.n_conflict(i) for i in range(self.n)], dtype=np.float32),
        }

        info = {
            'all_targets_reached': all_reached,
            'any_collision':       any_collision,
            'episode_collision':   self.collision_occurred,
            'r_mission':           r_mission,
            'r_safety':            r_safety,
            'pah_inputs':          pah_inputs,
        }
        return self._obs(), rewards, terminated, truncated, info

    def _obs(self):
        obs = np.zeros((self.n, self.obs_dim), dtype=np.float32)
        for i in range(self.n):
            rel = self.target_pos[self.assignment[i]] - self.drone_pos[i]
            cl  = self._clearances(i)
            base = np.concatenate([
                self.drone_pos[i] / self.W,
                self.drone_vel[i] / self.max_sp,
                rel               / self.W,
                cl,
            ])
            nbr = self.cg.neighbor_obs(i, self.drone_pos, self.drone_vel)
            for s in range(K_NBR):
                nbr[s*5 : s*5+2]   /= self.W
                nbr[s*5+2 : s*5+4] /= self.max_sp
            obs[i] = np.concatenate([base, nbr])
        return obs

    def _rewards(self):
        r_mission = np.zeros(self.n, dtype=np.float32)
        r_safety  = np.zeros(self.n, dtype=np.float32)
        d_danger  = self.col_r * 3.0
        zone_w    = d_danger - self.col_r
        for i in range(self.n):
            rel  = self.target_pos[self.assignment[i]] - self.drone_pos[i]
            dist = np.linalg.norm(rel)
            direction  = rel / (dist + 1e-6)
            r_progress = float(np.dot(self.drone_vel[i], direction) / self.max_sp)
            r_mission[i] = 0.4 * r_progress + 0.3 * (-dist / self.W)
            min_d = float('inf')
            for j in range(self.n):
                if j != i:
                    min_d = min(min_d, np.linalg.norm(self.drone_pos[i] - self.drone_pos[j]))
            for op in self.obstacle_pos:
                min_d = min(min_d, np.linalg.norm(self.drone_pos[i] - op))
            if min_d < self.col_r:
                r_safety[i] = -1.0
            elif min_d < d_danger:
                r_safety[i] = -((d_danger - min_d) / zone_w)
        rewards = r_mission + 0.3 * r_safety
        return rewards, r_mission, r_safety

    def _hungarian(self):
        cost = np.array([
            [np.linalg.norm(self.drone_pos[i] - self.target_pos[j])
             for j in range(self.n)]
            for i in range(self.n)
        ])
        _, col = linear_sum_assignment(cost)
        return col

    def _all_reached(self):
        return all(
            np.linalg.norm(self.drone_pos[i] - self.target_pos[self.assignment[i]]) <= self.tgt_r
            for i in range(self.n)
        )

    def _any_collision(self):
        for i in range(self.n):
            for j in range(self.n):
                if j != i and np.linalg.norm(self.drone_pos[i] - self.drone_pos[j]) < self.col_r:
                    return True
            for op in self.obstacle_pos:
                if np.linalg.norm(self.drone_pos[i] - op) < self.col_r:
                    return True
        return False

    def _clearances(self, i):
        pos = self.drone_pos[i]
        cl  = np.array([self.W - pos[1], pos[1], self.W - pos[0], pos[0]], dtype=np.float32)
        for op in self.obstacle_pos:
            diff = op - pos
            if diff[1] > 0: cl[0] = min(cl[0],  diff[1])
            else:           cl[1] = min(cl[1], -diff[1])
            if diff[0] > 0: cl[2] = min(cl[2],  diff[0])
            else:           cl[3] = min(cl[3], -diff[0])
        return cl / self.W

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

    def _place_obstacles(self, existing, n_obs, max_tries=1000):
        if n_obs <= 0:
            return np.zeros((0, 2), dtype=np.float32)
        r_min = 2.0 * self.col_r
        placed = []
        for _ in range(n_obs):
            for _ in range(max_tries):
                c = self.rng.uniform(10.0, self.W - 10.0, 2)
                if any(np.linalg.norm(c - o) < r_min for o in placed): continue
                if any(np.linalg.norm(c - p) < self.col_r for p in existing): continue
                placed.append(c)
                break
            else:
                break
        return np.array(placed, dtype=np.float32) if placed else np.zeros((0, 2), dtype=np.float32)



# ---- Actor (verbatim) ----
class Actor(nn.Module):
    def __init__(self, obs_dim, act_dim, hidden=64):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(obs_dim, hidden), nn.Tanh(),
            nn.Linear(hidden, hidden),  nn.Tanh(),
        )
        self.mu_head = nn.Linear(hidden, act_dim)
        self.log_std = nn.Parameter(torch.zeros(act_dim))

    def forward(self, x):
        mu      = self.mu_head(self.net(x))
        log_std = self.log_std.clamp(-4.0, 1.5)
        return Normal(mu, log_std.exp().expand_as(mu))


# ---- PAH (verbatim) ----
class PAHNormalizer:
    """Scales the 3 raw PAH inputs to roughly [0,1]. Ported from code/algorithms/pah.py."""
    def __init__(self, horizon=3.0, d_max=707.1, n_drones=5):
        self.horizon  = horizon
        self.d_max    = d_max
        self.n_drones = n_drones

    def normalize(self, tau, d_target, n_conflict):
        tau_norm = tau.clamp(0.0, self.horizon) / self.horizon
        d_norm   = d_target.clamp(0.0, self.d_max) / self.d_max
        denom    = max(self.n_drones - 1, 1)
        n_norm   = n_conflict.clamp(0.0, denom) / denom
        return torch.stack([tau_norm, d_norm, n_norm], dim=-1)


class PriorityArbitrationHead(nn.Module):
    """alpha(s) = clip(alpha_safe(tau) + delta(s), alpha_min, alpha_max).
    alpha_safe is a hardcoded tau-formula (never learned, never lost).
    delta is a small learned correction, tanh-bounded to
    [-delta_scale, +delta_scale], regularized toward zero. See Cell 4
    header for the full rationale."""
    def __init__(self, hidden_dim=32, alpha_min=0.1, alpha_max=0.9,
                 delta_scale=0.2, prior_coef=0.15):
        super().__init__()
        self.alpha_min   = alpha_min
        self.alpha_max   = alpha_max
        self.delta_scale = delta_scale
        self.prior_coef  = prior_coef
        self.net = nn.Sequential(
            nn.Linear(3, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1),
        )
        nn.init.zeros_(self.net[-1].bias)
        nn.init.xavier_uniform_(self.net[-1].weight, gain=0.1)

    def alpha_safe(self, tau_norm):
        return self.alpha_min + (self.alpha_max - self.alpha_min) * tau_norm

    def forward(self, x):
        """x: (..., 3) = [tau_norm, d_norm, n_norm]. Returns (alpha, delta)."""
        tau_norm  = x[..., 0]
        raw_delta = torch.tanh(self.net(x).squeeze(-1))
        delta     = self.delta_scale * raw_delta
        alpha     = (self.alpha_safe(tau_norm) + delta).clamp(self.alpha_min, self.alpha_max)
        return alpha, delta

    def compute_prior_loss(self, delta):
        """Regularizes the residual toward zero -- NOT toward the formula
        (alpha_safe already IS the formula, hardcoded). This only earns a
        role in training if a non-zero delta demonstrably lowers the total
        loss beyond what alpha_safe already gets for free."""
        if self.prior_coef == 0.0:
            return torch.tensor(0.0, device=delta.device)
        return self.prior_coef * delta.pow(2).mean()


# ---- Critic (verbatim) ----
class Critic(nn.Module):
    """Centralized critic -- one value per timestep from the flattened joint state."""
    def __init__(self, global_dim, hidden=64):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(global_dim, hidden), nn.Tanh(),
            nn.Linear(hidden, hidden),     nn.Tanh(),
            nn.Linear(hidden, 1),
        )

    def forward(self, global_state):
        return self.net(global_state).squeeze(-1)


# ---- RolloutBuffer (verbatim) ----
class RolloutBuffer:
    """Per-drone rewards/log-probs/PAH-inputs kept separate throughout -- nothing
    here is averaged across drones (see sessions/2026-09-15.md Part 12 for why
    that was a bug in an earlier version of the Stage 2 notebook)."""
    def __init__(self, n_drones):
        self.n_drones = n_drones
        self.clear()

    def clear(self):
        self.obs, self.acts, self.rews = [], [], []
        self.vals, self.lps, self.dones = [], [], []
        self.r_mission, self.r_safety = [], []
        self.tau, self.d_target, self.n_conflict = [], [], []

    def add(self, obs, act, rew, val, lp, done, r_mission, r_safety, pah_inputs):
        self.obs.append(obs.copy())
        self.acts.append(act.copy())
        self.rews.append(rew.copy())
        self.vals.append(float(val))
        self.lps.append(lp.copy())
        self.dones.append(bool(done))
        self.r_mission.append(r_mission.copy())
        self.r_safety.append(r_safety.copy())
        self.tau.append(pah_inputs['tau'].copy())
        self.d_target.append(pah_inputs['d_target'].copy())
        self.n_conflict.append(pah_inputs['n_conflict'].copy())

    def __len__(self):
        return len(self.rews)

    def compute_gae(self, last_val, gamma, lam):
        """Combined-reward GAE -- used for the critic's return target."""
        T = len(self.rews)
        n = self.n_drones
        rewards = np.array(self.rews,  dtype=np.float32)
        values  = np.array(self.vals,  dtype=np.float32)
        dones   = np.array(self.dones, dtype=np.float32)
        adv      = np.zeros((T, n), dtype=np.float32)
        last_gae = np.zeros(n, dtype=np.float32)
        for t in reversed(range(T)):
            next_val = last_val if t == T - 1 else values[t + 1]
            mask     = 1.0 - dones[t]
            delta    = rewards[t] + gamma * next_val * mask - values[t]
            last_gae = delta + gamma * lam * mask * last_gae
            adv[t]   = last_gae
        returns = adv + values[:, np.newaxis]
        return adv, returns

    def compute_gae_components(self, last_val, gamma, lam):
        """Separate GAE for r_mission and r_safety, sharing the combined-reward
        critic as baseline ("Option B lite" -- see docs/research/01_pah_design.md
        Section 9). Used for the alpha-weighted actor loss."""
        T = len(self.rews)
        n = self.n_drones
        rm      = np.array(self.r_mission, dtype=np.float32)
        rs      = np.array(self.r_safety,  dtype=np.float32)
        values  = np.array(self.vals,      dtype=np.float32)
        dones   = np.array(self.dones,     dtype=np.float32)
        adv_m = np.zeros((T, n), dtype=np.float32)
        adv_s = np.zeros((T, n), dtype=np.float32)
        gae_m = np.zeros(n, dtype=np.float32)
        gae_s = np.zeros(n, dtype=np.float32)
        for t in reversed(range(T)):
            next_val = last_val if t == T - 1 else values[t + 1]
            mask     = 1.0 - dones[t]
            delta_m  = rm[t] + gamma * next_val * mask - values[t]
            delta_s  = rs[t] + gamma * next_val * mask - values[t]
            gae_m    = delta_m + gamma * lam * mask * gae_m
            gae_s    = delta_s + gamma * lam * mask * gae_s
            adv_m[t] = gae_m
            adv_s[t] = gae_s
        return adv_m, adv_s


# ---------------------------------------------------------------------------
# Loaders + action helpers (new code, not copied)
# ---------------------------------------------------------------------------
PAH_HORIZON = 3.0
PAH_D_MAX   = 500.0 * 1.4142136


def load_checkpoint(path):
    """Returns (actor, pah_or_None). B4 checkpoints have no 'pah' key."""
    ck = torch.load(path, map_location=DEVICE, weights_only=True)
    actor = Actor(OBS_DIM, 2).to(DEVICE)
    actor.load_state_dict(ck['actor'])
    actor.eval()
    pah = None
    if 'pah' in ck:
        pah = PriorityArbitrationHead().to(DEVICE)
        pah.load_state_dict(ck['pah'])
        pah.eval()
    return actor, pah


@torch.no_grad()
def deterministic_action(actor, obs_np):
    """Distribution mean (evaluation protocol)."""
    return actor(torch.tensor(obs_np, dtype=torch.float32)).mean.numpy()


@torch.no_grad()
def stochastic_action(actor, obs_np, gen):
    """Sampled action, exactly like the training rollout (dist.sample()).
    gen: a torch.Generator, so runs are reproducible."""
    dist = actor(torch.tensor(obs_np, dtype=torch.float32))
    eps = torch.randn(dist.mean.shape, generator=gen)
    return (dist.mean + dist.stddev * eps).numpy()


@torch.no_grad()
def pah_alpha(pah, pah_inputs, n_drones):
    """alpha per drone, computed the same way as compute_alpha() in training."""
    norm = PAHNormalizer(PAH_HORIZON, PAH_D_MAX, n_drones)
    x = norm.normalize(torch.tensor(pah_inputs['tau'], dtype=torch.float32),
                       torch.tensor(pah_inputs['d_target'], dtype=torch.float32),
                       torch.tensor(pah_inputs['n_conflict'], dtype=torch.float32))
    alpha, _ = pah(x)
    return alpha.numpy()


def load_critic(path, n_drones):
    """The checkpoint's centralized critic. Input = all drones' observations flattened
    (n_drones * OBS_DIM), exactly as in training (obs.flatten())."""
    ck = torch.load(path, map_location=DEVICE, weights_only=True)
    critic = Critic(n_drones * OBS_DIM).to(DEVICE)
    critic.load_state_dict(ck['critic'], strict=True)   # raises on any missing / unexpected key
    critic.eval()
    return critic
