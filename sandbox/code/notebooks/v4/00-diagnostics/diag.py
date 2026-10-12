"""
diag.py -- instrumented rollouts for v4 Phase 0 (diagnostics on the v3 models).

One function, run_episode(), plays one episode and records, per step:
  * which drones have the safety reward switched on (r_safety != 0), and why
    (another drone within the danger radius, or an obstacle within it)
  * which drones the conflict graph flags (n_conflict > 0, i.e. tau < horizon)
  * the alpha each drone gets (B4: fixed 0.5, H: the tau formula, M: the PAH head)
  * loss-of-separation (LoS): drone pairs closer than the danger radius
  * active conflict-graph edges
and, if the episode ends in a collision, what was hit (drone or obstacle) and
whether it happened near the colliding drone's goal.

Nothing here changes the environment: everything is read from env state after
env.step(). The environment and networks come from ../common/v3_env.py.

Definitions (written once, used everywhere in Phase 0):
  danger radius d_danger = 3 x collision radius = 9 units. This is the same
  radius the v3 reward uses for r_safety and the conflict graph uses for an edge.
"""

import numpy as np

import torch

from v3_env import (MultiUAVEnv, RolloutBuffer, load_checkpoint, load_critic, deterministic_action,
                    stochastic_action, pah_alpha, PAH_HORIZON)

D_DANGER_FACTOR = 3.0


def make_env(entry, seed, success_bonus=0.0):
    """success_bonus: 0 for the evaluation-style checks (does not change dynamics or outcomes);
    20 for the advantage-correlation check, because there rewards must be exactly as in training."""
    return MultiUAVEnv(n_drones=entry['n_drones'], n_obstacles=entry['n_obstacles'],
                       success_bonus=success_bonus, use_hungarian=entry['use_hungarian'], seed=seed)


def alpha_values(method, pah, pah_inputs, n_drones):
    """The alpha each drone would get in training, for this state."""
    if method == 'B4':
        return np.full(n_drones, 0.5, dtype=np.float32)
    if method == 'H':   # HandCodedRule: alpha_min + (alpha_max - alpha_min) * tau_norm
        tau_norm = np.clip(pah_inputs['tau'], 0.0, PAH_HORIZON) / PAH_HORIZON
        return np.clip(0.1 + 0.8 * tau_norm, 0.1, 0.9).astype(np.float32)
    return pah_alpha(pah, pah_inputs, n_drones)   # M and M-noHungarian: the trained head


def _pair_distances(pos):
    d = np.linalg.norm(pos[:, None, :] - pos[None, :, :], axis=-1)
    np.fill_diagonal(d, np.inf)
    return d


def _obstacle_distances(pos, obstacles):
    if len(obstacles) == 0:
        return np.full(len(pos), np.inf)
    return np.linalg.norm(pos[:, None, :] - obstacles[None, :, :], axis=-1).min(axis=1)


def collision_kind(env):
    """Called after the step on which the episode ended in a collision.
    Returns (kind, near_goal): kind in {'drone-drone', 'drone-obstacle', 'both'};
    near_goal = a drone involved was within target_radius of its assigned target."""
    pos = env.drone_pos
    dd = _pair_distances(pos)
    do = _obstacle_distances(pos, env.obstacle_pos)
    hit_drone = np.where((dd < env.col_r).any(axis=1))[0]
    hit_obs = np.where(do < env.col_r)[0]
    if len(hit_drone) and len(hit_obs):
        kind = 'both'
    elif len(hit_drone):
        kind = 'drone-drone'
    elif len(hit_obs):
        kind = 'drone-obstacle'
    else:
        kind = 'unknown'   # should not happen; kept visible rather than hidden
    involved = np.union1d(hit_drone, hit_obs).astype(int)
    goal_d = np.linalg.norm(pos[involved] - env.target_pos[env.assignment[involved]], axis=1)
    return kind, bool((goal_d <= env.tgt_r).any())


def run_episode(env, actor, pah, method, mode, gen=None):
    """mode: 'det' (distribution mean, the evaluation protocol) or 'stoch'
    (sampled, like the training rollout; needs gen = torch.Generator).
    Returns (summary dict, per-drone-step alpha array)."""
    n = env.n
    d_dan = env.col_r * D_DANGER_FACTOR
    iu = np.triu_indices(n, 1)
    obs = env.reset()
    steps = 0
    safety_any = safety_drone = safety_obs = conflict = 0
    los_pair_steps = edges_sum = 0
    alphas = []
    done = False
    while not done:
        act = deterministic_action(actor, obs) if mode == 'det' else stochastic_action(actor, obs, gen)
        obs, _, terminated, truncated, info = env.step(act)
        steps += 1

        dd = _pair_distances(env.drone_pos)
        do = _obstacle_distances(env.drone_pos, env.obstacle_pos)
        near_drone = dd.min(axis=1) < d_dan
        near_obs = do < d_dan
        active = info['r_safety'] != 0
        # r_safety is non-zero exactly when the nearest drone OR obstacle is inside d_danger
        assert np.array_equal(active, near_drone | near_obs), 'r_safety bookkeeping mismatch'
        safety_any += int(active.sum())
        safety_drone += int(near_drone.sum())
        safety_obs += int(near_obs.sum())
        conflict += int((info['pah_inputs']['n_conflict'] > 0).sum())
        los_pair_steps += int((dd[iu] < d_dan).sum())
        edges_sum += int(env.cg.adj[iu].sum())
        alphas.append(alpha_values(method, pah, info['pah_inputs'], n))
        done = terminated or truncated

    if info['episode_collision']:
        outcome = 'collision'
        kind, near_goal = collision_kind(env)
    else:
        outcome = 'success' if info['all_targets_reached'] else 'timeout'
        kind, near_goal = '', False

    drone_steps = steps * n
    summary = dict(
        outcome=outcome, steps=steps,
        collision_kind=kind, collision_near_goal=near_goal,
        safety_frac=safety_any / drone_steps,            # share of drone-steps with r_safety != 0
        safety_drone_frac=safety_drone / drone_steps,    # ... because another drone is within d_danger
        safety_obs_frac=safety_obs / drone_steps,        # ... because an obstacle is within d_danger
        conflict_frac=conflict / drone_steps,            # share of drone-steps the conflict graph flags
        los_pair_steps=los_pair_steps,                   # IGAT-style loss-of-separation, summed over the episode
        los_rate=los_pair_steps / steps,                 # ... per step
        edges_mean=edges_sum / steps,                    # mean active conflict-graph edges per step
    )
    return summary, np.concatenate(alphas)


# ---------------------------------------------------------------------------
# Advantage-correlation check (PLAN-after-review.md, Step 2, revised after Manish's review)
# ---------------------------------------------------------------------------
GAMMA, LAM, ROLLOUT_STEPS, TRAIN_BONUS = 0.99, 0.95, 512, 20.0   # v3 training CFG


def _z(x):
    """z-normalization exactly as in v3 update(): torch .std() is the unbiased (ddof=1) std."""
    return (x - x.mean()) / (x.std(ddof=1) + 1e-8)


def _cos(a, b):
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-12))


@torch.no_grad()
def advantage_batch(entry, ckpt_path, env_seed, gen_seed):
    """Collects ONE training-style batch (512 env steps, stochastic actions, success bonus 20, episodes
    reset inside the batch) with the checkpoint's actor, critic and alpha source, then computes the
    advantages with the verbatim v3 RolloutBuffer code. Returns a dict of measurements."""
    n, method = entry['n_drones'], entry['method']
    actor, pah = load_checkpoint(ckpt_path)
    critic = load_critic(ckpt_path, n)
    env = make_env(entry, env_seed, success_bonus=TRAIN_BONUS)
    gen = torch.Generator().manual_seed(gen_seed)
    buf = RolloutBuffer(n)
    alphas = []
    obs = env.reset()
    for _ in range(ROLLOUT_STEPS):
        acts = stochastic_action(actor, obs, gen)
        val = critic(torch.tensor(obs, dtype=torch.float32).flatten().unsqueeze(0)).item()
        next_obs, _, terminated, truncated, info = env.step(acts)
        done = terminated or truncated
        alpha = alpha_values(method, pah, info['pah_inputs'], n)        # same pairing as training
        rews = alpha * info['r_mission'] + (1.0 - alpha) * info['r_safety']
        buf.add(obs, acts, rews, val, np.zeros(n, dtype=np.float32), done,
                info['r_mission'], info['r_safety'], info['pah_inputs'])
        alphas.append(alpha)
        obs = env.reset() if done else next_obs
    last_val = critic(torch.tensor(obs, dtype=torch.float32).flatten().unsqueeze(0)).item()
    A, _ = buf.compute_gae(last_val, GAMMA, LAM)
    A_m, A_s = buf.compute_gae_components(last_val, GAMMA, LAM)
    a = np.array(alphas, dtype=np.float64).ravel()
    A, A_m, A_s = (np.asarray(x, dtype=np.float64).ravel() for x in (A, A_m, A_s))

    z_m, z_s = _z(A_m), _z(A_s)
    w = lambda al: al * z_m + (1.0 - al) * z_s                       # what update() feeds the actor
    w_own, w_05, w_09 = w(a), w(0.5), w(0.9)
    mix_raw = a * A_m + (1.0 - a) * A_s                               # identity check: equals A if alpha constant
    return dict(
        alpha_mean=float(a.mean()), alpha_std=float(a.std()),
        corr_m_s=float(np.corrcoef(A_m, A_s)[0, 1]),                  # sign matters (Manish, 16.2)
        std_m_raw=float(A_m.std(ddof=1)), std_s_raw=float(A_s.std(ddof=1)), std_comb_raw=float(A.std(ddof=1)),
        cos_own_05=_cos(w_own, w_05), norm_own_over_05=float(np.linalg.norm(w_own) / np.linalg.norm(w_05)),
        cos_own_09=_cos(w_own, w_09), norm_own_over_09=float(np.linalg.norm(w_own) / np.linalg.norm(w_09)),
        corr_own_comb=float(np.corrcoef(w_own, A)[0, 1]),            # is the mixed signal just plain MAPPO's?
        identity_rel_err=float(np.linalg.norm(mix_raw - A) / (np.linalg.norm(A) + 1e-12)),
        safety_on_frac=float((np.asarray(buf.r_safety).ravel() != 0).mean()),
        episodes_done=int(sum(buf.dones)), drone_steps=int(A.size),
    )
