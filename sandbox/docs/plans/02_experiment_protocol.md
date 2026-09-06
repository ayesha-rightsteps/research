# 02 — Experiment Protocol

Fix this **before** running experiments and do not change it mid-project. If it must
change, note the change and the date here, and re-run affected configs.

---

## Metrics

### Primary

**Mission Success Rate (MSR)** — fraction of evaluation episodes in which *every* drone
reaches its assigned target, with *zero* collisions (drone–drone and drone–obstacle)
and no boundary violation, within the time limit `T_max`.

```
MSR = (# episodes with all_targets_reached AND zero_collisions AND no_boundary AND t <= T_max) / N_eval
```

### Secondary (per episode, reported as mean ± std over eval episodes)

| Metric | Definition |
|--------|-----------|
| Inter-drone collisions | count of steps where any pair is closer than `d_col` |
| Obstacle collisions | count of drone–obstacle contacts |
| Boundary violations | count of drones leaving the workspace |
| Target reassignments | number of times a drone's Hungarian-assigned target changes |
| Avg trajectory length | mean path length per drone |
| Avg completion time | mean steps until all targets reached (successful episodes only) |
| Dangerous-proximity time | steps spent within `d_danger` of another drone (IGAT "t_loss" analogue) |

### Training diagnostics (logged every update)

Episode return, episode length, actor/critic loss, entropy, approx-KL, and — for the
full model — the **distribution of α** (mean, std, histogram) and **α vs
time-to-collision** correlation.

---

## Evaluation procedure

- **N_eval = 200 episodes** per (config, swarm size, obstacle density) cell.
- **Eval seeds are fixed and disjoint from training seeds.** Same 200 episode layouts
  for every config so comparisons are paired.
- Policy at eval: **deterministic** (mean action, no exploration noise).
- No gradient updates, no curriculum — evaluate at the final trained stage.
- Record raw per-episode results to `code/results/<run_id>/eval.csv`; all tables and
  plots are derived from these CSVs by script.

---

## Seeds and reporting

- **≥ 5 training seeds** per reported configuration. More (10) for the headline
  PAH-vs-fixed-α comparison if compute allows.
- Report **mean ± standard deviation** across seeds, and a **95% confidence interval**
  for the primary metric.
- For the headline comparison, also report a **Welch's t-test** p-value (or a
  bootstrap CI on the difference). Do not over-claim on overlapping CIs.
- Every plot with a mean curve shows a shaded band (±1 std or 95% CI across seeds).

---

## Configuration grid

### Swarm size × obstacle density (evaluation)

|              | Low obstacles | Med obstacles | High obstacles |
|--------------|---------------|---------------|----------------|
| **3 drones** | ✓ | ✓ | ✓ |
| **5 drones** | ✓ | ✓ | ✓ |
| **8 drones** | ✓ | ✓ | ✓ |

(Exact obstacle counts set in P0 — DA-MAPPO used 30/40/50 in a larger arena; ours will
be scaled to the 2D world size, see `docs/research/00`.)

### Methods

| ID | Method | Assignment aug | Conflict graph | α |
|----|--------|:-:|:-:|---|
| B1 | Standard MAPPO | ✗ | ✗ | n/a (single reward) |
| B2 | DA-MAPPO-2D | ✓ (per-step Hungarian) | ✗ | fixed |
| B3 | IGAT-style (MAPPO-adapted) | ✗ (static/one-shot) | ✓ | fixed |
| B4 | Fixed-weight MAPPO | ✓ | ✓ | **fixed**, swept ∈ {0.3, 0.5, 0.7} |
| **M** | **Ours (PAH)** | ✓ | ✓ | **learned per step** |

B4 is the decisive comparison. B1–B3 establish that each component contributes.

### Ablations (on M, Stage 3 unless noted)

- M without conflict graph
- M without assignment augmentation
- M with α frozen at its mean learned value (is it the *adaptivity* that matters, or
  just the average level?)
- M without the α regularizer/prior (if one is used)
- PAH input ablation: drop `n_conflict`, drop `τ_collision`, drop `d_target` one at a time

### Generalization (Stage 4)

Train M and B4 on {3, 5, 8}; evaluate on swarm sizes **not seen in training**
(e.g. 4, 6, 7, and one larger like 10) with fixed obstacle density.

---

## Decision rule — "does PAH win?"

PAH is judged **better than fixed-α** if, on Stage 3 (8 drones) and at least one other
stage:

- MSR(M) ≥ MSR(best B4) **and** the 95% CIs do not overlap (or t-test p < 0.05), **and**
- inter-drone + obstacle collision rate of M is ≤ that of the best B4 (not trading
  safety for success).

Also report the **adaptivity evidence**: learned α is *not* constant, and it varies
with `τ_collision` / `n_conflict` in the expected direction (α down when danger is
close). If α turns out ≈ constant, PAH reduces to fixed-α and we say so.

A negative or null result is reported honestly with an analysis of why.

---

## Compute budget (rough)

- Env is small; the real speed lever is **vectorized envs on CPU**, not GPU.
- One training run (Stage 1–3 curriculum): estimate 1–4 hours on a Kaggle T4, more for
  8 drones. Confirm after the first real run.
- Full grid: ~5 methods × 9 cells × 5 seeds ≈ 225 runs, but many share early curriculum
  stages. Prioritize: Stage 3 grid first, then fill in. Use Kaggle's 30 GPU-h/week;
  parallelize across accounts/sessions if needed.
- Checkpoint every ~30 min of training (Kaggle sessions expire).

---

## Results artifacts

```
code/results/
├── <run_id>/
│   ├── config.yaml          # exact config used
│   ├── meta.json            # git commit, seed, start/end time, host
│   ├── train_log/           # TensorBoard event files
│   ├── checkpoints/
│   └── eval.csv             # per-episode eval results
├── tables/                  # generated by make_results_table.py
└── plots/                   # generated by make_plots.py
```

`run_id` = `<method>_<stage>_<swarmsize>_<density>_seed<k>_<date>`.
