# 03 — Engineering Standards

Non-negotiable conventions so results are reproducible and the code stays readable.

---

## Environment

- **Python 3.10 or 3.11.**
- One virtualenv per machine: `python -m venv .venv && source .venv/bin/activate`.
- `code/requirements.txt` with **pinned versions** (`torch==x.y.z`, not `torch`).
- Record the exact versions in each run's `meta.json`.

Base deps: `torch`, `numpy`, `scipy`, `gymnasium`, `matplotlib`, `pandas`, `pyyaml`,
`tensorboard`, `pytest`.

---

## Configuration

- Every experiment is driven by a YAML file in `code/configs/`.
- **No hyperparameter, path, or magic number hardcoded** in `.py` files.
- The config includes the **seed**. Different seed = different config file (or a
  `--seed` override that is recorded).
- A config is never edited in place after runs use it — copy and rename.

Example skeleton (`code/configs/stage1_mappo.yaml`):

```yaml
run_name: b1_standard_mappo_stage1
seed: 0
env:
  n_drones: 3
  world_size: 100.0
  dt: 0.1
  v_max: 5.0
  d_col: 2.0
  d_safe: 3.0
  arrival_radius: 3.0
  t_max: 600
  n_obstacles: 0
  moving_targets: false
algo:
  name: mappo
  hidden_dim: 128
  n_hidden_layers: 2
  lr: 3.0e-4
  gamma: 0.99
  gae_lambda: 0.95
  ppo_clip: 0.2
  ppo_epochs: 10
  entropy_coef: 0.01
  rollout_steps: 2048
  n_envs: 32
train:
  total_env_steps: 3_000_000
  checkpoint_every_steps: 100_000
  eval_every_steps: 100_000
```

(Values above are placeholders — real defaults come from `docs/research/03_baseline_specs.md`.)

---

## Determinism

- At startup set seeds for `random`, `numpy`, and `torch` (CPU and CUDA).
- `torch.use_deterministic_algorithms(True)` where feasible; document any op that
  forces it off.
- The env must be seedable and reproducible: same seed → identical episode (unit test).
- Vectorized envs get **derived seeds** (`base_seed + env_index`), recorded.

---

## Testing

`code/tests/` with `pytest`. Minimum set:

**Environment**
- position update + speed clamp + boundary clamp
- drone–drone collision detection (hand-built near/far cases)
- drone–obstacle collision detection
- target-reached detection at the arrival radius
- reward term signs: progress toward target → positive; collision → large negative;
  step → small negative
- determinism: same seed → byte-identical trajectory
- obs vector shape is fixed for K-padding regardless of live neighbor count

**Algorithms**
- `hungarian.py`: matches hand-solved 3×3 and 4×4 assignments; handles ties
- `conflict_graph.py`: TTC / DCPA against analytic cases (head-on, parallel, diverging,
  crossing); adjacency is symmetric with zero diagonal
- `pah.py`: forward on `[B, 3]` returns `[B, 1]` in `[0, 1]`; gradients are non-zero

**Smoke**
- MAPPO can overfit a trivial 1-step task (loss goes down)

Run the test suite before every training run. A failing test blocks training.

---

## Logging

- **TensorBoard** by default (offline, no account needed). W&B optional if a free
  account is set up — same metrics either way.
- Log: returns, episode length, all losses, entropy, approx-KL, learning rate, and for
  the full model the **α histogram** and **α vs τ_collision** scatter.
- Each run writes `meta.json`: git commit hash, full config, seed, package versions,
  host, start/end time.
- Never overwrite a run directory. `run_id` includes the date.

---

## Checkpointing

- Save model + optimizer state every `checkpoint_every_steps` and at the end.
- Keep the best-by-eval checkpoint separately.
- Training must be **resumable** from a checkpoint (Kaggle sessions expire ~ every few
  hours) — verified by a test: resume produces a matching continuation curve.

---

## Code style

- Format with `black`; lint with `ruff`.
- Docstrings on every public function/class: what it does, shapes of tensors in/out.
- Type hints where they are cheap and clarifying.
- Comments explain **why**, not what. Match the surrounding style.
- Prefer clarity over cleverness — Ayesha (and the committee) must be able to read
  every line. No dense one-liners in the core algorithm files.
- Keep `mappo.py` small and legible (~300–400 lines). If it grows, split it.

---

## Data hygiene / git

- `code/results/` is git-ignored **except** `tables/` and small manifest files.
- Trained model weights are **not** committed (too large). Store on Kaggle output /
  Google Drive; keep an index file `code/results/models_index.md` (run_id → location).
- Raw eval CSVs are small — those can be committed.
- **No `git commit` or `git push` unless Manish asks.** When he does: branch first if
  on `main`, follow the attribution rules in the repo.
- `bin/` and `000aaaaaa. after approval/` are never modified.

---

## Kaggle workflow

1. Push code to a private GitHub repo (only when Manish asks) **or** upload as a
   Kaggle Dataset.
2. In the notebook: `!git clone <repo>` or attach the dataset.
3. `!pip install -r code/requirements.txt`.
4. Enable GPU (Settings → Accelerator → GPU T4). Note: for this problem size the GPU
   helps the update step only; env stepping is CPU-bound — keep `n_envs` high.
5. Train, checkpointing to `/kaggle/working/` every ~30 min.
6. Download checkpoints + logs from the Output panel; record location in `models_index.md`.

---

## Per-experiment reproducibility checklist

- [ ] Config file committed (or its exact content in `meta.json`)
- [ ] Seed recorded
- [ ] Git commit hash recorded
- [ ] Package versions recorded
- [ ] Test suite was green before the run
- [ ] Checkpoints + logs saved and indexed
- [ ] Result added to the session log
