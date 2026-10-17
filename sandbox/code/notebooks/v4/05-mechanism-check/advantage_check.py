"""
advantage_check.py -- v4 mechanism check (02-redesign/PLAN.md Section 5, "advantage correlation: is the actor signal
still ~plain MAPPO? it should not be"). The same check as Phase 0 (00-diagnostics, v3 models), now on the final v4
models of the four two-head methods.

What it measures. In training, each two-head method (Fixed-weight MAPPO, Hand-coded τ-rule MAPPO, MAPPO + PAH,
MAPPO + PAH (Hungarian off)) gives the actor the signal
    w = α · z(A_mission) + (1 − α) · z(A_safety)          (mappo_v4.Agent.update, actor_adv='mixed')
where A_mission / A_safety are the GAE advantages of the two reward streams on their own value heads and z() is the
batch normalization. Plain MAPPO instead uses z(A_combined) for the combined reward 0.5·r_mission + 0.5·r_safety.
With one value 0.5·(V_m + V_s), GAE is linear, so A_combined = 0.5·(A_m + A_s) and Plain MAPPO's signal is
z(A_m + A_s). For every batch:
  corr_m_s       corr(A_mission, A_safety)
  cos_vs_fixed   cosine(w, 0.5·z_m + 0.5·z_s)      = 1 for Fixed-weight MAPPO by construction (gate)
  corr_vs_plain  corr(w, z(A_m + A_s))              how close the actor signal is to Plain MAPPO's
  sign_flip      share of samples where w and z(A_m + A_s) have opposite signs (the actor is pushed the other way)
  safety_on      share of samples with a non-zero safety reward
  flip_safety_on / flip_safety_off   sign_flip among samples with / without a safety reward
Phase 0 (v3 models) found corr_vs_plain 0.95–1.00 for every v3 method.

Batches: training-style -- the training environment of the run (its stage, obstacles, assignment, success bonus 20),
stochastic actions, 512 steps per batch, 10 batches per model, environment seed 7001 + model seed, torch seed =
model seed. Final models (final_model.pt), 10 seeds × 2 stages × 4 methods = 80 models. No training.

Writes output/advantage_per_batch.csv, output/advantage_summary.md.

Usage:  python advantage_check.py [--procs 6] [--batches 10]
"""
import os, sys, json
import numpy as np
import torch
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
V4 = os.path.join(HERE, '..')
sys.path.insert(0, os.path.join(V4, 'common'))
import env_v4 as E
import mappo_v4 as M

RUNS = os.path.join(V4, '02-redesign', 'runs')
METHODS = ['fixed-weight-mappo', 'tau-rule-mappo', 'mappo-pah', 'mappo-pah-no-hungarian']
NAMES = {'fixed-weight-mappo': 'Fixed-weight MAPPO', 'tau-rule-mappo': 'Hand-coded τ-rule MAPPO',
         'mappo-pah': 'MAPPO + PAH', 'mappo-pah-no-hungarian': 'MAPPO + PAH (Hungarian off)'}
SEEDS = range(42, 52)
STEPS = 512
ENV_SEED = 7001


def zn(x):
    return (x - x.mean()) / (x.std(ddof=1) + 1e-8)          # as mappo_v4 (torch std is unbiased)


def corr(a, b):
    return float(np.corrcoef(a, b)[0, 1])


def check_run(run_dir, batches):
    torch.set_num_threads(1)
    c = json.load(open(os.path.join(run_dir, 'config.json')))
    torch.manual_seed(c['seed']); np.random.seed(c['seed'])
    agent = M.Agent(n_drones=c['n_drones'], obs_dim=E.OBS_DIM, **c['agent'], pah_hidden=c['pah_hidden'],
                    alpha_min=c['alpha_min'], alpha_max=c['alpha_max'], pah_delta_scale=c['pah_delta_scale'],
                    pah_prior_coef=c['pah_prior_coef'], pah_horizon=c['pah_horizon'], pah_d_max=c['pah_d_max'],
                    gamma=c['gamma'], lam=c['lam'], hidden=c['hidden'])
    agent.load(os.path.join(run_dir, 'final_model.pt'))
    env = E.MultiUAVEnvV4(n_drones=c['n_drones'], n_obstacles=c['n_obstacles'], world_size=c['world_size'],
                          max_speed=c['max_speed'], max_steps=c['max_steps'], collision_radius=c['collision_radius'],
                          target_radius=c['target_radius'], success_bonus=c['success_bonus'],
                          target_speed=c['target_speed'], use_hungarian=c['use_hungarian'], seed=ENV_SEED + c['seed'],
                          safety_danger_radius=c['safety_danger_radius'], collision_penalty=c['collision_penalty'])
    rows, obs = [], env.reset()
    for b in range(batches):
        buf = M.Buffer()
        for _ in range(STEPS):                                    # the training rollout loop (train.py)
            act, lp, vals = agent.get_actions(obs)
            nobs, _, te, tr, info = env.step(act)
            done = te or tr
            p = info['pah_inputs']
            alpha = agent.compute_alpha(p['tau'], p['d_target'], p['n_conflict'])
            rew = alpha * info['r_mission'] + (1.0 - alpha) * info['r_safety']
            buf.add(obs, act, lp, done, info['r_mission'], info['r_safety'], rew, vals, p)
            obs = env.reset() if done else nobs
        # advantages exactly as Agent.update (two-head branch)
        with torch.no_grad():
            last = tuple(v.item() for v in agent._values(torch.tensor(obs, dtype=torch.float32).flatten().unsqueeze(0)))
        dones = np.array(buf.dones, dtype=np.float32)
        r_m, r_s = np.array(buf.r_m, dtype=np.float32), np.array(buf.r_s, dtype=np.float32)
        v_m, v_s = np.array(buf.v_m, dtype=np.float32), np.array(buf.v_s, dtype=np.float32)
        A_m = M.gae(r_m, v_m, last[0], dones, agent.gamma, agent.lam).reshape(-1).astype(np.float64)
        A_s = M.gae(r_s, v_s, last[1], dones, agent.gamma, agent.lam).reshape(-1).astype(np.float64)
        alpha = agent.compute_alpha(np.array(buf.tau).reshape(-1), np.array(buf.d_target).reshape(-1),
                                    np.array(buf.n_conflict).reshape(-1)).astype(np.float64)
        z_m, z_s, z_c = zn(A_m), zn(A_s), zn(A_m + A_s)
        w = alpha * z_m + (1 - alpha) * z_s
        w_fixed = 0.5 * z_m + 0.5 * z_s
        rows.append(dict(method=c['method'],
                         stage=c['stage'], seed=c['seed'], batch=b,
                         corr_m_s=corr(A_m, A_s),
                         cos_vs_fixed=float(w @ w_fixed / (np.linalg.norm(w) * np.linalg.norm(w_fixed))),
                         corr_vs_plain=corr(w, z_c), sign_flip=float(np.mean(np.sign(w) != np.sign(z_c))),
                         safety_on=float(np.mean(r_s.reshape(-1) != 0)),
                         flip_safety_on=float(np.mean((np.sign(w) != np.sign(z_c))[r_s.reshape(-1) != 0])),
                         flip_safety_off=float(np.mean((np.sign(w) != np.sign(z_c))[r_s.reshape(-1) == 0])), alpha_mean=float(alpha.mean()),
                         alpha_std=float(alpha.std())))
    return rows


def main():
    procs = int(sys.argv[sys.argv.index('--procs') + 1]) if '--procs' in sys.argv else 6
    batches = int(sys.argv[sys.argv.index('--batches') + 1]) if '--batches' in sys.argv else 10
    runs = [os.path.join(RUNS, 'stage{}'.format(st), m, 'seed-{}'.format(s)) for st in (2, 3) for m in METHODS for s in SEEDS]
    with Pool(procs) as pool:
        rows = [r for res in pool.starmap(check_run, [(d, batches) for d in runs]) for r in res]
    os.makedirs(os.path.join(HERE, 'output'), exist_ok=True)
    keys = list(rows[0])
    with open(os.path.join(HERE, 'output', 'advantage_per_batch.csv'), 'w') as f:
        f.write(','.join(keys) + '\n')
        for r in rows:
            f.write(','.join(str(r[k]) if isinstance(r[k], (int, str)) else '{:.6f}'.format(r[k]) for k in keys) + '\n')

    from scipy import stats
    def ms(v):
        h = stats.t.ppf(0.975, len(v) - 1) * np.std(v, ddof=1) / np.sqrt(len(v))
        return '{:+.2f} ± {:.2f}'.format(np.mean(v), h) if np.mean(v) < 0 else '{:.2f} ± {:.2f}'.format(np.mean(v), h)
    L = ['# Advantage check — v4 two-head methods (final models)', '',
         'Generated by `05-mechanism-check/advantage_check.py`. {} training-style batches of {} steps per model; value = '
         'mean over the 10 seeds (each seed = mean of its batches) ± 95% t half-width. See the docstring for the '
         'definitions. Phase 0 (v3 models): corr_vs_plain 0.95–1.00 for every method.'.format(batches, STEPS), '',
         '| Stage | Method | corr(A_mission, A_safety) | cosine(own signal, α = 0.5 signal) | corr(own signal, Plain MAPPO signal) | Opposite sign to Plain MAPPO (%) | … on safety-reward steps (%) | … on other steps (%) | Safety reward on (%) | α mean (sd) |',
         '|---|---|---|---|---|---|---|---|---|---|']
    for st in (2, 3):
        for m in METHODS:
            R = [r for r in rows if r['stage'] == st and r['method'] == m]
            per_seed = lambda k: np.array([np.mean([r[k] for r in R if r['seed'] == s]) for s in SEEDS])
            L.append('| {} | {} | {} | {} | {} | {:.1f} | {:.1f} | {:.1f} | {:.1f} | {:.2f} ({:.2f}) |'.format(
                st, NAMES[m], ms(per_seed('corr_m_s')), ms(per_seed('cos_vs_fixed')), ms(per_seed('corr_vs_plain')),
                100 * per_seed('sign_flip').mean(), 100 * per_seed('flip_safety_on').mean(),
                100 * per_seed('flip_safety_off').mean(), 100 * per_seed('safety_on').mean(), per_seed('alpha_mean').mean(),
                per_seed('alpha_std').mean()))
    open(os.path.join(HERE, 'output', 'advantage_summary.md'), 'w').write('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    main()
