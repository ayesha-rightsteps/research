# v4 / 01-plain-mappo-check — does Plain MAPPO match Fixed-weight MAPPO?

**Status (2026-10-12): done.** Plan: `PLAN.md`. Implemented on Ayesha's instruction ("do what is right")
without a separate review of `PLAN.md` by Manish's Claude — the plan, gates and reading rule were written
before running and are unchanged; Manish can review the results.

## Question

Phase 0 (`../00-diagnostics/README.md`) found that for every v3 method the actor's learning signal is
95–100% correlated with the plain combined-reward advantage. Hypothesis: the three v3 methods tie because
each is, in effect, plain MAPPO on a combined reward. Test: train **Plain MAPPO** (one combined reward, one
ordinary advantage, no mission/safety mixing) and compare it with **Fixed-weight MAPPO** (α = 0.5).

## What was run (laptop, Stage 2 = 5 drones, 5 obstacles, seeds 42–46, 8000 episodes each)

| Run | What |
|---|---|
| Fixed-weight MAPPO (laptop) | unchanged v3 code (`use_pah = False`, α = 0.5) — same-hardware reference |
| Plain MAPPO | identical except one line: the actor uses the normalized combined-reward advantage |
| Plain MAPPO, α = 0.9 reward | as Plain MAPPO, combined reward 0.9·r_mission + 0.1·r_safety |

Base code: `v3/stage2/stage2-pah-v3-pah-change/var-alpha/kaggle_stage2_pah_allseeds.ipynb`, executed by
`train_runner.py` with guarded string overrides (seed, `use_pah`, `fixed_alpha`, warm-start path, and for
Plain MAPPO the one advantage line). Nothing written in `v3/`.

## Gates (all passed)

1. **Base code equivalence:** the base notebook with `use_pah = False` has the same imports, conflict graph,
   environment, Actor, Critic, PAHNormalizer and RolloutBuffer as the notebook that trained the original
   Kaggle Fixed-weight MAPPO (`stage2-pah-v0/fixed-alpha/kaggle_stage2_pah.ipynb`). Differences: PAH code
   (inactive with `use_pah = False`), seeding style (`np.random.seed` added), and the 5-seed loop.
2. **Code diff between runs:** Fixed-weight → Plain MAPPO differs by exactly the advantage line; Plain MAPPO →
   α = 0.9 differs by exactly `fixed_alpha`.
3. **Laptop reproduces the Kaggle level:** laptop Fixed-weight MAPPO 88.2 ± 2.2% vs Kaggle 89.2 ± 2.0%
   (difference 1.0 point, within one seed-to-seed std).

Smoke test (60 episodes per run) before the full runs: no errors.

## Results (deterministic policy, 200 episodes, env seed 7001; mean ± std over 5 seeds)

| Run | Success % | Collision % | Timeout % | T_ave | % collisions with obstacles | Loss-of-separation / episode |
|---|---|---|---|---|---|---|
| Fixed-weight MAPPO (laptop) | 88.2 ± 2.2 | 11.8 ± 2.2 | 0 | 48.8 | 99 | 0.140 |
| **Plain MAPPO** | **89.9 ± 1.4** | 10.1 ± 1.4 | 0 | 49.2 | 96 | 0.157 |
| Plain MAPPO, α = 0.9 reward | 89.4 ± 1.9 | 10.6 ± 1.9 | 0 | 48.7 | 94 | 0.141 |
| *Context (Kaggle, v3):* Fixed-weight MAPPO | 89.2 ± 2.0 | 10.8 ± 2.0 | 0 | 49.1 | — | — |
| *Context (Kaggle, v3):* Hand-coded τ-rule MAPPO | 87.5 ± 1.5 | 12.5 ± 1.5 | 0 | 49.1 | — | — |
| *Context (Kaggle, v3):* MAPPO + PAH | 89.5 ± 1.0 | 10.5 ± 1.0 | 0 | 49.4 | — | — |

Figure: `output/plain_mappo_check.png` (final success per seed; training curves).

### Comparison, using the reading rule fixed in `PLAN.md` before the runs

| Comparison | Difference | 95% CI | Welch p | Reading |
|---|---|---|---|---|
| Plain MAPPO − Fixed-weight MAPPO (laptop) | +1.7 | [−1.1, +4.5] | 0.19 | **Inconclusive** |
| Plain MAPPO (α = 0.9 reward) − Fixed-weight MAPPO (laptop) | +1.2 | [−1.8, +4.2] | 0.39 | **Inconclusive** |

By the pre-set rule ("match" = CI inside ±3 points and containing 0) the result is **inconclusive**: with 5
seeds the interval reaches +4.5. The rule is not changed after the fact.

## What can and cannot be said

- **Can:** removing the mission/safety mixing did **not** make MAPPO worse — the CI's lower end is −1.1
  points, so "the mixing adds something" (CI entirely below 0) is not supported. Changing the reward weight
  from 0.5 to 0.9 also made no measurable difference. All six Stage 2 results (three laptop runs here, three
  Kaggle v3 methods) lie between 87.5% and 89.9%.
- **Can:** laptop training reproduces Kaggle results (gate 3), and a full 8000-episode Stage 2 run takes
  11–12 minutes with 8 runs in parallel (Kaggle: ~44 min for one).
- **Cannot:** claim a statistically confirmed "match" — the interval is too wide with 5 seeds. Narrowing it
  would need more seeds (each extra batch of 8 runs ≈ 12 min). Whether that is worth doing is a decision
  for Ayesha and Manish; it does not change the practical conclusion below.

**Practical conclusion for v4:** the v3 mission/safety mixing gives no measurable benefit over plain MAPPO.
For PAH's arbitration to be able to matter, the design has to change (Phase 1b: separate mission and safety
value heads, obstacle danger in PAH's time-to-collision input, LiDAR-like sensing, sized and denser
obstacles).

## Files

| File | What |
|---|---|
| `PLAN.md` | the plan (written before running) |
| `train_runner.py` | runs one (run, seed) with guarded overrides; `--episodes N` only for smoke tests |
| `evaluate.ipynb` | gate 3, evaluation, comparison, figure |
| `runs/<run>/output-seed<N>/` | final model, checkpoints, `history.json`, `wall_time.json` (22 MB total) |
| `logs/` | training logs, batch start/end time |
| `output/` | `eval_episodes.csv`, `per_seed.csv`, `results.md`, `plain_mappo_check.png/.svg` |
