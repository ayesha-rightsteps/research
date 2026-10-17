"""
summarize.py -- v4 Phase 3: the tables of the base-paper experiments (PLAN.md Section 4), from the evaluation JSON.

Reads
  ../02-redesign/output/phase3/<experiment>/            our 5 methods
  ../03-base-paper-baselines/output/phase3/<experiment>/ the 4 base-paper methods (RMAPPO excluded)
written by run_phase3.sh. phase3/main/ is the training setting itself (same success numbers as the main results,
plus the Phase 3 metrics), so it is the reference level of every experiment: S2 = 10 discs, 5 drones; S3 = 20 discs,
8 drones; target speed 1; assignment every step; no LiDAR noise.

Writes output/phase3_summary.md and output/phase3_per_seed.csv.

Statistics (PLAN 02 Section 5, as in Phase 1b/2): mean over the 10 seeds, "±" = 95% t half-width; between methods a
95% Welch CI on the success difference. Within one method, the change from the training setting is a paired 95% t CI
over the 10 seeds (same models, same evaluation seed). Reading: CI entirely above 0 = better (▲), entirely below =
worse (▼), otherwise not settled (·). Every Phase 3 comparison is secondary (PLAN.md Section 3), no multiple-testing
correction. One decimal, half up (summarize helpers of Phase 2).

Usage:  python summarize.py
"""
import os, json, glob
import importlib.util
import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
V4 = os.path.join(HERE, '..')
# Phase 2 helpers (welch, verdict, f1, ci, NAMES), loaded by path because every phase calls its file summarize.py
_spec = importlib.util.spec_from_file_location('summarize_phase2', os.path.join(V4, '03-base-paper-baselines', 'summarize.py'))
P2 = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(P2)
welch, f1, NAMES = P2.welch, P2.f1, P2.NAMES

ALL = ['mappo-pah', 'fixed-weight-mappo', 'tau-rule-mappo', 'mappo-pah-no-hungarian', 'plain-mappo',
       'igat-style', 'da-mappo-2d', 'mappo', 'ippo']
E3_METHODS = ['mappo-pah', 'fixed-weight-mappo', 'tau-rule-mappo', 'plain-mappo', 'da-mappo-2d']
E4_METHODS = ['mappo-pah', 'fixed-weight-mappo', 'tau-rule-mappo', 'plain-mappo', 'igat-style']
TIMING_METHODS = ['mappo-pah', 'fixed-weight-mappo', 'igat-style']

# levels of each experiment -> results folder (None = the training setting, phase3/main)
TRAINED_OBST, TRAINED_N = {2: 10, 3: 20}, {2: 5, 3: 8}
DENSITY = {st: [(n, None if n == TRAINED_OBST[st] else 'density_s{}_n{}'.format(st, n)) for n in (10, 20, 30, 40, 50)]
           for st in (2, 3)}
SWARM = {st: [(n, None if n == TRAINED_N[st] else 'swarm_s{}_n{}'.format(st, n)) for n in range(3, 11)] for st in (2, 3)}
NOISE = [(0.0, None)] + [(s, 'noise_s3_{}'.format(s)) for s in (0.02, 0.05, 0.1)]
TIMING = [(n, 'timing_n{}'.format(n)) for n in range(3, 11)]


def load():
    R = {}
    for f in glob.glob(os.path.join(V4, '0[23]-*', 'output', 'phase3', '*', '*.json')):
        r = json.load(open(f))
        R[(os.path.basename(os.path.dirname(f)), r['stage'], r['method'], r['seed'])] = r
    return R


R = load()


def get(exp, st, m, k='success'):
    """One value per seed (sorted by seed); success-type fields in %."""
    exp = exp or 'main'
    v = np.array([R[(exp, st, m, s)][k] for s in sorted(s for (e, a, b, s) in R if (e, a, b) == (exp, st, m))], dtype=float)
    return v * 100 if k in ('success', 'collision', 'timeout') else v


def half(x):
    return stats.t.ppf(0.975, len(x) - 1) * x.std(ddof=1) / np.sqrt(len(x))


def paired(a, b):
    """a - b over the same seeds, paired 95% t CI."""
    d = a - b
    return d.mean(), d.mean() - half(d), d.mean() + half(d)


def mark(lo, hi):
    return '▲' if lo > 0 else '▼' if hi < 0 else '·'


def cell_ci(d, lo, hi):
    return '{} [{}, {}] {}'.format(f1(d, True), f1(lo, True), f1(hi, True), mark(lo, hi))


def ms(x):
    return '{} ± {}'.format(f1(x.mean()), f1(half(x)))


def success_table(L, levels, methods, st, label, fmt=str):
    """Success (mean ± CI) per method per level, then MAPPO + PAH minus each method per level (Welch)."""
    L += ['| Method | ' + ' | '.join(label.format(fmt(v)) for v, _ in levels) + ' |', '|---' * (len(levels) + 1) + '|']
    for m in methods:
        L.append('| {} | {} |'.format(NAMES[m], ' | '.join(ms(get(e, st, m)) for _, e in levels)))
    L += ['', 'MAPPO + PAH minus each method (success points, 95% Welch CI):', '',
          '| Compared with | ' + ' | '.join(label.format(fmt(v)) for v, _ in levels) + ' |', '|---' * (len(levels) + 1) + '|']
    for m in methods[1:]:
        L.append('| {} | {} |'.format(NAMES[m], ' | '.join(
            cell_ci(*welch(get(e, st, 'mappo-pah'), get(e, st, m))) for _, e in levels)))
    L.append('')


def two_setting_table(L, exp, methods, name):
    """Training setting vs one changed setting, both stages: success, paired change, PAH minus each method."""
    L += ['| Method | S2 trained | S2 {0} | S2 change | S3 trained | S3 {0} | S3 change |'.format(name), '|---' * 7 + '|']
    for m in methods:
        cells = []
        for st in (2, 3):
            a, b = get(None, st, m), get(exp, st, m)
            cells += [ms(a), ms(b), cell_ci(*paired(b, a))]
        L.append('| {} | {} |'.format(NAMES[m], ' | '.join(cells)))
    L += ['', 'MAPPO + PAH minus each method under "{}" (95% Welch CI):'.format(name), '',
          '| Compared with | Stage 2 | Stage 3 |', '|---|---|---|']
    for m in methods[1:]:
        L.append('| {} | {} |'.format(NAMES[m], ' | '.join(
            cell_ci(*welch(get(exp, st, 'mappo-pah'), get(exp, st, m))) for st in (2, 3))))
    L.append('')


def main():
    L = ['# Phase 3 — base-paper experiments on the trained models (summary)', '',
         'Generated by `04-base-paper-experiments/summarize.py` from `output/phase3/` of 02-redesign and '
         '03-base-paper-baselines. No training: the same 180 models (9 methods × 2 stages × 10 seeds; RMAPPO excluded), '
         '200 deterministic episodes each, evaluation seed 7001, one test setting changed at a time. '
         '"Trained" = the training setting (S2: 10 discs, 5 drones; S3: 20 discs, 8 drones; moving targets; '
         'assignment every step; no noise). ▲ CI above 0, ▼ CI below 0, · not settled. All comparisons secondary '
         '(PLAN.md Section 3).', '']

    # E5 at the training setting
    L += ['## E5 — IGAT-MARL metrics at the training setting', '',
          'LoS = drone pairs closer than 3 collision radii (loss of separation), summed over the steps of an episode, '
          'mean per episode. Edges = active conflict-graph edges per step. Both are counted for every method from the '
          'environment state, whatever the method observes.', '',
          '| Method | S2 Success | S2 LoS / episode | S2 Edges / step | S3 Success | S3 LoS / episode | S3 Edges / step |',
          '|---|---|---|---|---|---|---|']
    for m in ALL:
        cells = []
        for st in (2, 3):
            cells += [ms(get(None, st, m)), '{:.2f}'.format(get(None, st, m, 'los_per_episode').mean()),
                      '{:.4f}'.format(get(None, st, m, 'active_edges_per_step').mean())]
        L.append('| {} | {} |'.format(NAMES[m], ' | '.join(cells)))
    L.append('')

    L += ['## E1 — obstacle density (success %, trained: S2 10 discs, S3 20 discs)', '']
    for st in (2, 3):
        L += ['### Stage {}'.format(st), '']
        success_table(L, DENSITY[st], ALL, st, '{} discs')

    L += ['## E2 — static targets (target speed 0; trained with moving targets, speed 1)', '',
          'Change = static minus trained, paired over the 10 seeds.', '']
    two_setting_table(L, 'static', ALL, 'static')

    L += ['## E3 — assignment every 50 steps (trained: every step)', '',
          'Only methods that re-assign every step in training. Change = every-50 minus every-step, paired.', '']
    two_setting_table(L, 'assign50', E3_METHODS, 'every 50')

    L += ['## E4 — swarm size (success %, trained: S2 5 drones, S3 8 drones)', '',
          'Only methods whose observation does not depend on the number of drones (PLAN.md Section 4). '
          'Each model keeps its own obstacle count.', '']
    for st in (2, 3):
        L += ['### Stage {}'.format(st), '']
        success_table(L, SWARM[st], E4_METHODS, st, 'N = {}')
        for k, name, fmt in (('los_per_episode', 'LoS per episode', '{:.2f}'), ('active_edges_per_step', 'Active edges per step', '{:.4f}')):
            L += ['{} (IGAT-MARL metric), Stage {}:'.format(name, st), '',
                  '| Method | ' + ' | '.join('N = {}'.format(n) for n, _ in SWARM[st]) + ' |', '|---' * 9 + '|']
            for m in E4_METHODS:
                L.append('| {} | {} |'.format(NAMES[m], ' | '.join(fmt.format(get(e, st, m, k).mean()) for _, e in SWARM[st])))
            L.append('')

    L += ['## E6 — LiDAR noise, Stage 3 (success %; σ as a fraction of the ray range, trained without noise)', '']
    success_table(L, NOISE, ALL, 3, 'σ = {}', fmt=lambda s: '{:g}'.format(s))

    L += ['## E7 — decision time (ms per step, all drones together; Stage 3 models)', '',
          'Time of one `get_actions` call (actor only, deterministic) for the whole swarm, 1 process, 1 thread, '
          '20 episodes per model, mean ± 95% CI over the 10 seeds. Laptop CPU; the conflict graph and the environment '
          'step are not included. Absolute values depend on the machine; the trend with N is the result.', '',
          '| Method | ' + ' | '.join('N = {}'.format(n) for n, _ in TIMING) + ' |', '|---' * 9 + '|']
    for m in TIMING_METHODS:
        L.append('| {} | {} |'.format(NAMES[m], ' | '.join(
            '{:.3f} ± {:.3f}'.format(get(e, 3, m, 'decision_ms').mean(), half(get(e, 3, m, 'decision_ms'))) for _, e in TIMING)))
    L.append('')

    os.makedirs(os.path.join(HERE, 'output'), exist_ok=True)
    open(os.path.join(HERE, 'output', 'phase3_summary.md'), 'w').write('\n'.join(L))
    with open(os.path.join(HERE, 'output', 'phase3_per_seed.csv'), 'w') as f:
        f.write('experiment,stage,method,seed,setting,n_drones_test,success,collision,timeout,los_per_episode,'
                'active_edges_per_step,decision_ms\n')
        for (e, st, m, s), r in sorted(R.items()):
            f.write('{},{},{},{},"{}",{},{:.3f},{:.3f},{:.3f},{:.4f},{:.6f},{:.5f}\n'.format(
                e, st, m, s, json.dumps(r['setting']).replace('"', "'"), r['n_drones_test'], r['success'],
                r['collision'], r['timeout'], r['los_per_episode'], r['active_edges_per_step'], r['decision_ms']))
    print('\n'.join(L))


if __name__ == '__main__':
    main()
