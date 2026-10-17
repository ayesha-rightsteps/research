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
  python evaluate.py                 # all 100 models, 4 processes  -> output/eval_raw/
  python evaluate.py --episodes 20   # quick check
  python evaluate.py --phase2        # Phase 2 base-paper methods: ../03-base-paper-baselines/runs -> that folder's output/
  Options (any combination):
    --methods a,b      only these methods          --stages 3     only these stages (e.g. 2,3)
    --raw-dir NAME     write to output/NAME/ instead of output/eval_raw/ (e.g. a re-run to compare with the original)
    --procs N          parallel processes (default 4)
  Example, RMAPPO Stage 3 only: python evaluate.py --phase2 --methods rmappo --stages 3
  Phase 3 test settings (v4/04-base-paper-experiments/PLAN.md); any of them switches on the Phase 3 output, which adds
  'setting' and the extra metrics (loss-of-separation per episode, active edges per step, decision time):
    --obstacles N   --target-speed V   --drones N   --assign-every K   --lidar-noise S   --phase3 (default setting)
  The models are not changed; only the test environment is. --drones needs a method whose observation does not
  depend on the swarm size (not 'all' teammates).
Phase 2 models (config.json has 'assignment') are rebuilt with 03-base-paper-baselines/train_baselines.py; the
episode loop is the same, with the two hooks those agents need (graph for IGAT-style, hidden-state reset for RMAPPO).
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
PHASE2 = os.path.join(HERE, '..', '03-base-paper-baselines')
PHASE2_METHODS = ['ippo', 'mappo', 'rmappo', 'da-mappo-2d', 'igat-style']


def build(run_dir, setting=None):
    """Agent exactly as trained (from the run's config.json) and its test environment. With a Phase 3 setting the
    environment is rebuilt with that one change (obstacles, target speed, drones, assignment frequency, LiDAR noise);
    without one it is the training environment, as before."""
    c = json.load(open(os.path.join(run_dir, 'config.json')))
    if 'assignment' in c:                       # Phase 2 base-paper method
        sys.path.insert(0, PHASE2)
        import train_baselines as TB
        agent = TB.make_agent(c)
        agent.load(os.path.join(run_dir, 'final_model.pt'))
        if setting is None:
            return c, agent, TB.make_env(c, EVAL_SEED, bonus=0.0)
        mode, teammates = c['assignment'], c['teammates']
    else:
        agent = M.Agent(n_drones=c['n_drones'], obs_dim=E.OBS_DIM, **c['agent'], pah_hidden=c['pah_hidden'],
                        alpha_min=c['alpha_min'], alpha_max=c['alpha_max'], pah_delta_scale=c['pah_delta_scale'],
                        pah_prior_coef=c['pah_prior_coef'], pah_horizon=c['pah_horizon'], pah_d_max=c['pah_d_max'],
                        hidden=c['hidden'])
        agent.load(os.path.join(run_dir, 'final_model.pt'))
        if setting is None:
            env = E.MultiUAVEnvV4(n_drones=c['n_drones'], n_obstacles=c['n_obstacles'], world_size=c['world_size'],
                                  max_speed=c['max_speed'], max_steps=c['max_steps'], collision_radius=c['collision_radius'],
                                  target_radius=c['target_radius'], success_bonus=0.0, target_speed=c['target_speed'],
                                  use_hungarian=c['use_hungarian'], seed=EVAL_SEED,
                                  safety_danger_radius=c['safety_danger_radius'], collision_penalty=c['collision_penalty'])
            return c, agent, env
        mode, teammates = ('every-step' if c['use_hungarian'] else 'fixed-arbitrary'), 'conflict'
    n = setting.get('drones', c['n_drones'])
    if n != c['n_drones'] and teammates == 'all':
        raise ValueError('{}: observation includes all teammates, so it cannot run with {} drones'.format(run_dir, n))
    if 'assign_every' in setting:
        if mode != 'every-step':
            raise ValueError('{}: --assign-every only applies to methods trained with every-step assignment'.format(run_dir))
        mode = 'every-k'
    env = E.MultiUAVEnvV4(n_drones=n, n_obstacles=setting.get('obstacles', c['n_obstacles']), world_size=c['world_size'],
                          max_speed=c['max_speed'], max_steps=c['max_steps'], collision_radius=c['collision_radius'],
                          target_radius=c['target_radius'], success_bonus=0.0,
                          target_speed=setting.get('target_speed', c['target_speed']), seed=EVAL_SEED,
                          safety_danger_radius=c['safety_danger_radius'], collision_penalty=c['collision_penalty'],
                          assignment=mode, teammates=teammates, assign_every=setting.get('assign_every', 1),
                          lidar_noise=setting.get('lidar_noise', 0.0))
    return c, agent, env


def evaluate_run(run_dir, episodes=EPISODES, setting=None):
    torch.set_num_threads(1)
    c, agent, env = build(run_dir, setting)
    los_eps, edges, dt = [], [], []            # Phase 3 extras (IGAT-MARL metrics, decision time)
    horizon = c.get('pah_horizon', E.TAU_HORIZON)
    eps = []                                   # one dict per episode
    alpha_by_tau = {k: [] for k in range(4)}   # tau bins [0,1), [1,2), [2,3), 3 (= nothing within the horizon)
    tau_obst = tau_drone = flagged_steps = drone_steps = 0
    for _ in range(episodes):
        obs, done, steps = env.reset(), False, 0
        if hasattr(agent, 'reset_episode'):
            agent.reset_episode()
        path = np.zeros(env.n)
        los = 0
        while not done:
            kw = {'adj': env.cg.adj.copy()} if getattr(agent, 'uses_graph', False) else {}
            t0 = time.perf_counter()
            act, _, _ = agent.get_actions(obs, deterministic=True, values=False, **kw)
            dt.append(time.perf_counter() - t0)
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
            los += info['los_pairs']; edges.append(info['active_edges'])
        los_eps.append(los)
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
    out = dict(
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
    if setting is not None:                              # Phase 3 output only; the main results keep their exact format
        out.update(setting=setting, n_drones_test=env.n, los_per_episode=mean(los_eps), active_edges_per_step=mean(edges),
                   decision_ms=1000 * mean(dt))
    return out


def arg(name, default=None):
    """Value after a command-line flag, or the default when the flag is absent."""
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


def main():
    episodes = int(arg('--episodes', EPISODES))
    root, methods, out = (PHASE2, PHASE2_METHODS, os.path.join(PHASE2, 'output')) if '--phase2' in sys.argv \
        else (HERE, METHODS, OUT)
    if '--methods' in sys.argv:
        methods = arg('--methods').split(',')
    stages = [int(s) for s in arg('--stages', '2,3').split(',')]
    setting = {k: cast(arg(flag)) for flag, k, cast in (('--obstacles', 'obstacles', int), ('--target-speed', 'target_speed', float),
               ('--drones', 'drones', int), ('--assign-every', 'assign_every', int), ('--lidar-noise', 'lidar_noise', float))
               if flag in sys.argv}
    setting = setting if (setting or '--phase3' in sys.argv) else None
    runs = sorted(d for st in stages for m in methods
                  for d in glob.glob(os.path.join(root, 'runs', 'stage{}'.format(st), m, 'seed-*'))
                  if os.path.exists(os.path.join(d, 'final_model.pt')))
    print('{} models, {} episodes each, evaluation seed {}'.format(len(runs), episodes, EVAL_SEED), flush=True)
    t0 = time.time()
    with Pool(int(arg('--procs', 4))) as pool:
        res = pool.starmap(evaluate_run, [(d, episodes, setting) for d in runs])
    raw = os.path.join(out, arg('--raw-dir', 'eval_raw' if episodes == EPISODES else 'eval_raw_check'))
    os.makedirs(raw, exist_ok=True)
    for r in res:
        json.dump(r, open(os.path.join(raw, 'stage{}_{}_seed{}.json'.format(r['stage'], r['method'], r['seed'])), 'w'))
    print('done in {:.1f} min -> {}'.format((time.time() - t0) / 60, raw))


if __name__ == '__main__':
    main()
