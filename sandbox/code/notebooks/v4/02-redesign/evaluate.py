"""
evaluate.py -- v4 Phase 1b, Step 5: final evaluation of every trained model. Plan: PLAN.md Sections 5-6.

Protocol (fixed in the plan before any result was seen):
  * every final_model.pt in runs/stage{2,3}/<method>/seed-<n>/  (5 methods x 10 seeds x 2 stages = 100 models);
  * 200 episodes, deterministic actions (the actor's mean), evaluation seed 7001 -- disjoint from the training
    seeds (42-51), the sanity seeds (101/102) and the training-time evaluation seed (999);
  * the environment of every model is rebuilt from that run's own config.json (drones, discs, safety reward),
    so evaluation uses exactly the setting the model was trained in;
  * the same evaluation seed gives every model of a stage the same 200 starting layouts.

Per episode it records the outcome (success / collision / timeout), the collision kind, the steps taken and the
path length of every drone; per drone-step the PAH-side quantities (alpha, tau, which hazard set tau).

Usage:
  python evaluate.py                 # all 100 models, 4 processes  -> output/eval_per_seed.csv, output/eval_raw/
  python evaluate.py --episodes 20   # quick check
"""
import os, sys, json, glob, time
import numpy as np
import torch
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'common'))
import env_v4 as E
import mappo_v4 as M

EVAL_SEED = 7001
EPISODES = 200
METHODS = ['plain-mappo', 'fixed-weight-mappo', 'tau-rule-mappo', 'mappo-pah', 'mappo-pah-no-hungarian']
OUT = os.path.join(HERE, 'output')


def build(run_dir):
    """Agent + environment exactly as in training, from the run's config.json."""
    c = json.load(open(os.path.join(run_dir, 'config.json')))
    agent = M.Agent(n_drones=c['n_drones'], obs_dim=E.OBS_DIM, **c['agent'], pah_hidden=c['pah_hidden'],
                    alpha_min=c['alpha_min'], alpha_max=c['alpha_max'], pah_delta_scale=c['pah_delta_scale'],
                    pah_prior_coef=c['pah_prior_coef'], pah_horizon=c['pah_horizon'], pah_d_max=c['pah_d_max'],
                    hidden=c['hidden'])
    agent.load(os.path.join(run_dir, 'final_model.pt'))
    env = E.MultiUAVEnvV4(n_drones=c['n_drones'], n_obstacles=c['n_obstacles'], world_size=c['world_size'],
                          max_speed=c['max_speed'], max_steps=c['max_steps'], collision_radius=c['collision_radius'],
                          target_radius=c['target_radius'], success_bonus=0.0, target_speed=c['target_speed'],
                          use_hungarian=c['use_hungarian'], seed=EVAL_SEED,
                          safety_danger_radius=c['safety_danger_radius'], collision_penalty=c['collision_penalty'])
    return c, agent, env


def evaluate_run(run_dir, episodes=EPISODES):
    torch.set_num_threads(1)
    c, agent, env = build(run_dir)
    horizon = c['pah_horizon']
    eps = []                                   # one dict per episode
    alpha_by_tau = {k: [] for k in range(4)}   # tau bins [0,1), [1,2), [2,3), 3 (= nothing within the horizon)
    tau_obst = tau_drone = flagged_steps = drone_steps = 0
    for _ in range(episodes):
        obs, done, steps = env.reset(), False, 0
        path = np.zeros(c['n_drones'])
        while not done:
            act, _, _ = agent.get_actions(obs, deterministic=True)
            before = env.drone_pos.copy()
            obs, _, te, tr, info = env.step(act)
            path += np.linalg.norm(env.drone_pos - before, axis=1)
            steps += 1
            done = te or tr
            p = info['pah_inputs']
            tau, td, to = p['tau'], info['tau_drone'], info['tau_obstacle']
            alpha = agent.compute_alpha(tau, p['d_target'], p['n_conflict'])
            bins = np.where(tau >= horizon - 1e-6, 3, np.floor(tau).astype(int).clip(0, 2))
            for b, a in zip(bins, alpha):
                alpha_by_tau[int(b)].append(float(a))
            flagged = tau < horizon - 1e-6
            tau_obst += int((flagged & (to <= td)).sum()); tau_drone += int((flagged & (td < to)).sum())
            flagged_steps += int(flagged.sum()); drone_steps += len(tau)
        if info['episode_collision']:
            outcome = 'collision'
        elif info['all_targets_reached']:
            outcome = 'success'
        else:
            outcome = 'timeout'
        eps.append(dict(outcome=outcome, kind=info['collision_kind'], steps=steps, path=float(path.mean())))

    succ = [e for e in eps if e['outcome'] == 'success']
    kinds = [e['kind'] for e in eps if e['outcome'] == 'collision']
    mean = lambda v: float(np.mean(v)) if len(v) else float('nan')
    return dict(
        method=c['method'], stage=c['stage'], seed=c['seed'], episodes=episodes,
        success=sum(e['outcome'] == 'success' for e in eps) / episodes,
        collision=sum(e['outcome'] == 'collision' for e in eps) / episodes,
        timeout=sum(e['outcome'] == 'timeout' for e in eps) / episodes,
        coll_drone_drone=kinds.count('drone-drone'), coll_drone_obstacle=kinds.count('drone-obstacle'),
        coll_both=kinds.count('both'),
        T_ave=mean([e['steps'] for e in succ]),          # steps to finish, successful episodes only
        L_ave=mean([e['path'] for e in succ]),           # mean per-drone path length, successful episodes only
        alpha_tau_bins=[mean(alpha_by_tau[k]) for k in range(4)],
        alpha_danger=mean(alpha_by_tau[0]), alpha_safe=mean(alpha_by_tau[3]),
        tau_flagged_frac=flagged_steps / max(drone_steps, 1),
        tau_set_by_obstacle=tau_obst / max(flagged_steps, 1), tau_set_by_drone=tau_drone / max(flagged_steps, 1),
        outcomes=[e['outcome'][0] for e in eps])        # 's' / 'c' / 't' per episode, same layouts for every model


def main():
    episodes = int(sys.argv[sys.argv.index('--episodes') + 1]) if '--episodes' in sys.argv else EPISODES
    runs = sorted(d for st in (2, 3) for m in METHODS
                  for d in glob.glob(os.path.join(HERE, 'runs', 'stage{}'.format(st), m, 'seed-*'))
                  if os.path.exists(os.path.join(d, 'final_model.pt')))
    print('{} models, {} episodes each, evaluation seed {}'.format(len(runs), episodes, EVAL_SEED), flush=True)
    t0 = time.time()
    with Pool(4) as pool:
        res = pool.starmap(evaluate_run, [(d, episodes) for d in runs])
    raw = os.path.join(OUT, 'eval_raw' if episodes == EPISODES else 'eval_raw_check')
    os.makedirs(raw, exist_ok=True)
    for r in res:
        json.dump(r, open(os.path.join(raw, 'stage{}_{}_seed{}.json'.format(r['stage'], r['method'], r['seed'])), 'w'))
    print('done in {:.1f} min -> {}'.format((time.time() - t0) / 60, raw))


if __name__ == '__main__':
    main()
