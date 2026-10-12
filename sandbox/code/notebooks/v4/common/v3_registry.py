"""
v3_registry.py -- where every trained v3 model lives, in one place.

v3 folders were named inconsistently (output / output-seed42 / seed-43/output),
so the paths are listed here once, and everything in v4 that reads a v3 model
goes through this file. Same paths as v3/results-table Cell 5 (verified there).

Each entry: stage, method, seed, use_hungarian, n_drones, n_obstacles, run_dir
(the folder holding final_model.pt, history.json and checkpoint_ep*.pt).
"""

import os
import re

# this file lives in code/notebooks/v4/common/ -> v3 is ../../v3
V3 = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'v3'))

S2 = dict(n_drones=5, n_obstacles=5)
S3 = dict(n_drones=8, n_obstacles=10)


def _s2_b4_dir(seed):
    sub = 'output' if seed == 42 else 'seed-%d/output' % seed
    return os.path.join(V3, 'stage2', 'stage2-pah-v0', 'fixed-alpha', sub)


REGISTRY = []
for _seed in (42, 43, 44, 45, 46):
    REGISTRY += [
        dict(stage=2, method='B4', seed=_seed, use_hungarian=True, run_dir=_s2_b4_dir(_seed), **S2),
        dict(stage=2, method='H', seed=_seed, use_hungarian=True,
             run_dir=os.path.join(V3, 'stage2', 'stage2-pah-v3-pah-change', 'h-baseline', 'output-seed%d' % _seed), **S2),
        dict(stage=2, method='M', seed=_seed, use_hungarian=True,
             run_dir=os.path.join(V3, 'stage2', 'stage2-pah-v3-pah-change', 'var-alpha', 'output-seed%d' % _seed), **S2),
    ]
REGISTRY += [
    dict(stage=3, method='B4', seed=42, use_hungarian=True,
         run_dir=os.path.join(V3, 'stage3', 'fixed-alpha', 'output'), **S3),
    dict(stage=3, method='M', seed=42, use_hungarian=True,
         run_dir=os.path.join(V3, 'stage3', 'var-alpha', 'output'), **S3),
    dict(stage=3, method='M-noHungarian', seed=42, use_hungarian=False,
         run_dir=os.path.join(V3, 'stage3', 'ablation-hungarian', 'output'), **S3),
]


def final_model(entry):
    return os.path.join(entry['run_dir'], 'final_model.pt')


def checkpoints(entry):
    """[(episode, path), ...] sorted by episode, plus the final model at the end
    (episode = None). Empty list if the run saved no intermediate checkpoints."""
    if not os.path.isdir(entry['run_dir']):
        return []
    out = []
    for f in os.listdir(entry['run_dir']):
        m = re.fullmatch(r'checkpoint_ep(\d+)\.pt', f)
        if m:
            out.append((int(m.group(1)), os.path.join(entry['run_dir'], f)))
    out.sort()
    return out


def find(stage, method, seed=42):
    hits = [e for e in REGISTRY if e['stage'] == stage and e['method'] == method and e['seed'] == seed]
    if len(hits) != 1:
        raise KeyError('no unique registry entry for stage=%s method=%s seed=%s' % (stage, method, seed))
    return hits[0]


def check_all():
    """Raises if any final_model.pt is missing. Returns a short summary."""
    missing = [final_model(e) for e in REGISTRY if not os.path.exists(final_model(e))]
    if missing:
        raise FileNotFoundError('missing:\n  ' + '\n  '.join(missing))
    return '{} models, all final_model.pt found'.format(len(REGISTRY))
