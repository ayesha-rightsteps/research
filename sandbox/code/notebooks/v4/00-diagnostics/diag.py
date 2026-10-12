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

from v3_env import (MultiUAVEnv, load_checkpoint, deterministic_action,
                    stochastic_action, pah_alpha, PAH_HORIZON)

D_DANGER_FACTOR = 3.0


def make_env(entry, seed):
    return MultiUAVEnv(n_drones=entry['n_drones'], n_obstacles=entry['n_obstacles'],
                       success_bonus=0.0, use_hungarian=entry['use_hungarian'], seed=seed)


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
