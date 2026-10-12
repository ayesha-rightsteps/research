"""
train_runner.py -- v4 Phase 1a: train one (run, seed) on the laptop with the UNCHANGED v3 Stage 2
training code plus a few guarded overrides. Nothing is written into v3/.

Base notebook (cells 1-6): v3/stage2/stage2-pah-v3-pah-change/var-alpha/kaggle_stage2_pah_allseeds.ipynb
(the notebook that trained Stage 2 Hand-coded tau-rule MAPPO and MAPPO + PAH). With use_pah=False it is
Fixed-weight MAPPO; Gate 1 (README) checked it against the notebook that trained the original Kaggle
Fixed-weight MAPPO: identical environment, networks, buffer, update(); only seeding style, the seed loop and
inactive PAH code differ.

Runs:
  fixed-weight-mappo-laptop : use_pah=False, fixed_alpha=0.5, unchanged update()        (run B)
  plain-mappo               : as B, but the actor uses the plain combined-reward advantage (run A)
  plain-mappo-alpha09       : as A, with fixed_alpha=0.9 in the combined reward            (run C)

Usage: python train_runner.py RUN SEED [--print-code] [--episodes N]   (--episodes only for smoke tests)
Outputs go to runs/RUN/output-seed<SEED>/ (final_model.pt, checkpoints, history.json, training_curves.png).
"""
import os, sys, json, time

HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.normpath(os.path.join(HERE, '..', '..', 'v3'))
NB = os.path.join(V3, 'stage2', 'stage2-pah-v3-pah-change', 'var-alpha', 'kaggle_stage2_pah_allseeds.ipynb')
WARM = os.path.join(V3, 'stage2', 'stage2-b', 'output', 'final_model.pt')

RUNS = {
    'fixed-weight-mappo-laptop': dict(alpha=0.5, plain=False),
    'plain-mappo':               dict(alpha=0.5, plain=True),
    'plain-mappo-alpha09':       dict(alpha=0.9, plain=True),
}

MIX_LINE = 'w_adv = alpha * adv_m_flat[idx] + (1.0 - alpha) * adv_s_flat[idx]'
PLAIN_LINE = 'w_adv = adv_t.reshape(-1)[idx]   # v4 Phase 1a: plain combined-reward advantage (normalized), no mission/safety mixing'


def replace_once(src, old, new, what):
    n = src.count(old)
    assert n == 1, 'override "{}": expected the original text exactly once, found {}'.format(what, n)
    return src.replace(old, new)


def build_cells(run, seed):
    spec = RUNS[run]
    cells = [''.join(c['source']) for c in json.load(open(NB))['cells']]
    c4, c5 = cells[4], cells[5]
    # cell 5: seed, method switch, alpha, warm-start path
    c5 = replace_once(c5, 'SEEDS = [42, 43, 44, 45, 46]', 'SEEDS = [{}]'.format(seed), 'seed')
    c5 = replace_once(c5, "'use_pah':          True,", "'use_pah':          False,", 'use_pah')
    c5 = replace_once(c5, "'fixed_alpha':      0.5,", "'fixed_alpha':      {},".format(spec['alpha']), 'fixed_alpha')
    c5 = replace_once(c5, "'../../stage2-b/output/final_model.pt'", repr(WARM), 'warm-start path')
    # cell 4: the one algorithmic change for the plain-MAPPO runs
    if spec['plain']:
        c4 = replace_once(c4, MIX_LINE, PLAIN_LINE, 'plain advantage')
    cells[4], cells[5] = c4, c5
    return cells


def main():
    run, seed = sys.argv[1], int(sys.argv[2])
    assert run in RUNS, 'unknown run ' + run
    assert os.path.exists(WARM), WARM
    cells = build_cells(run, seed)
    if '--print-code' in sys.argv:
        print(cells[4]); print(cells[5]); return

    import matplotlib
    matplotlib.use('Agg')
    import torch
    torch.set_num_threads(1)

    workdir = os.path.join(HERE, 'runs', run)
    os.makedirs(workdir, exist_ok=True)
    os.chdir(workdir)                      # the notebook writes output-seed<N>/ under the cwd
    ns = {'__name__': '__main__'}
    t0 = time.time()
    episodes = int(sys.argv[sys.argv.index('--episodes') + 1]) if '--episodes' in sys.argv else None
    for i, src in enumerate(cells[1:7], start=1):   # cells 1-6: imports, conflict graph, env, agent, config, train
        exec(src, ns)
        if i == 5 and episodes is not None:         # smoke test only: shorten training
            ns['CFG']['total_episodes'] = episodes
    minutes = (time.time() - t0) / 60
    with open(os.path.join(workdir, 'output-seed{}'.format(seed), 'wall_time.json'), 'w') as f:
        json.dump({'run': run, 'seed': seed, 'wall_minutes': round(minutes, 2), 'threads': 1}, f)
    print('RUN_DONE run={} seed={} wall_min={:.1f}'.format(run, seed, minutes))


if __name__ == '__main__':
    main()
