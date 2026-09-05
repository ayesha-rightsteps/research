# code/

All implementation code. The structure follows the implementation guide (Section 13).

```
code/
├── environment/
│   ├── multi_uav_env.py     # 2D Gymnasium env (drones, targets, obstacles, step/reset/reward)
│   └── rendering.py          # matplotlib visualization (optional, for debugging)
│
├── algorithms/
│   ├── hungarian.py          # target assignment (scipy.optimize.linear_sum_assignment wrapper)
│   ├── conflict_graph.py     # which drone pairs are on a collision course
│   ├── mappo.py              # MAPPO actor-critic (base: marlbenchmark/on-policy)
│   └── pah.py                # Priority Arbitration Head — THE NOVEL PART
│
├── training/
│   ├── train.py              # main training loop
│   └── curriculum.py         # 4-stage curriculum (3 -> 5 -> 8 -> unseen)
│
├── evaluation/
│   └── evaluate.py           # test trained models against the 4 baselines
│
├── configs/
│   └── config.yaml           # hyperparameters — keep them here, not hardcoded
│
├── results/
│   ├── models/               # saved weights (name with config + timestamp)
│   └── plots/                # graphs
│
└── notebooks/
    └── experiments.ipynb     # Kaggle notebook (real training here, free T4 GPU)
```

## Setup
```bash
python -m venv .venv && source .venv/bin/activate
pip install torch numpy scipy gymnasium matplotlib pandas pyyaml
```

## Rules (full rules in CLAUDE.md)
- Python 3.10 / 3.11
- No PyBullet — custom 2D Gymnasium env
- Fix the seed for every experiment
- Readable, commented code (Ayesha is new to the field)
- Never fake results
