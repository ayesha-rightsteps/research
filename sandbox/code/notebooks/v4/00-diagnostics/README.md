# v4 / 00-diagnostics — what the v3 models actually do

**Status (2026-10-12):** done, including the follow-up steps from `PLAN-after-review.md` (verified by
Manish's Claude, session Section 16). Read-only: nothing trained, no v3 file written.
Run `diagnostics.ipynb` from this folder (CPU, ~8 min from scratch; results cached in `output/`).

## Names used here

| Full name | What it is | v3 code key |
|---|---|---|
| Fixed-weight MAPPO | α fixed at 0.5 | `B4` |
| Hand-coded τ-rule MAPPO | α = 0.1 + 0.8·(τ/3), nothing learned | `H` |
| MAPPO + PAH | α = τ-rule + learned residual (the thesis method) | `M` |
| MAPPO + PAH, Hungarian off | same, target pairing fixed at reset (ablation) | `M-noHungarian` |

Stage 2 = 5 drones, 5 obstacles (seeds 42–46). Stage 3 = 8 drones, 10 obstacles (seed 42 only).

## Checks

| Check | Question | Pass |
|---|---|---|
| Collision-type check | Are collisions drone–drone or drone–obstacle? | evaluation |
| Safety-reward frequency check | How often is the safety *reward* on? | training-like replay |
| α spread check | How much does α move, and what drives it? | training-like replay |
| IGAT-MARL metrics check | Loss-of-separation, active conflict edges | evaluation |
| Advantage-correlation check | Does α's mixing change the actor's learning signal? | advantage pass |

- **Evaluation pass:** all 18 final models, deterministic policy, 200 episodes, env seed 7001 (same protocol
  and episode layouts as `v3/results-table`).
- **Training-like replay:** every saved checkpoint of every run (Stage 2: 5 seeds per method; Stage 3:
  seed 42), stochastic policy, 50 episodes, env seed 9101. *An approximation of training conditions* —
  saved checkpoints replayed on a new seed, not the actual training rollouts.
- **Advantage pass:** training-style batches (512 env steps, stochastic, success bonus 20 as in training,
  episodes reset inside the batch), advantages computed with the verbatim v3 `RolloutBuffer` and each
  checkpoint's own critic; 10 batches per checkpoint.
- **Danger radius** = 3 × collision radius = 9 units (used by the v3 safety reward and the conflict graph).

### Gates (all passed)
1. The frozen copy `../common/v3_env.py` reproduces v3 episode-by-episode: 200/200 for Stage 3 MAPPO + PAH
   and Stage 2 Fixed-weight MAPPO (seed 43); 5 models checked during development, all 200/200.
2. Every collision episode is cross-checked with the environment's own collision test.
3. Advantage pass: for Fixed-weight MAPPO (α constant = 0.5), `0.5·A_mission + 0.5·A_safety` equals the
   plain combined-reward advantage to float precision (relative error 5·10⁻⁷ at Stage 2, 4·10⁻⁷ at Stage 3).

## Results

### Collision-type check — `output/collision_type_check.png`

| Stage | Method | Collision episodes | Drone–obstacle | Drone–drone | % obstacle | % near goal |
|---|---|---|---|---|---|---|
| 2 (1000 ep) | Fixed-weight MAPPO | 108 | 107 | 1 | 99.1 | 20.4 |
| 2 (1000 ep) | Hand-coded τ-rule MAPPO | 125 | 124 | 1 | 99.2 | 20.8 |
| 2 (1000 ep) | MAPPO + PAH | 105 | 104 | 1 | 99.0 | 21.9 |
| 3 (200 ep) | Fixed-weight MAPPO | 53 | 50 | 3 | 94.3 | 30.2 |
| 3 (200 ep) | MAPPO + PAH | 56 | 56 | 0 | 100.0 | 39.3 |
| 3 (200 ep) | MAPPO + PAH, Hungarian off | 97 | 78 | 19 | 80.4 | 19.6 |

**Almost every failure is a drone hitting an obstacle.** Drone–drone collisions become common only when
Hungarian assignment is off.

### Safety-reward frequency check — `output/safety_reward_frequency_check.png`

| Stage | Method | Safety reward on, % drone-steps (range over training) | Final: drone within 9 | Final: obstacle within 9 | Conflict flagged, % (final) |
|---|---|---|---|---|---|
| 2 | Fixed-weight MAPPO | 0.18–0.55 | 0.01 ± 0.02 | 0.36 ± 0.08 | 0.04 ± 0.02 |
| 2 | Hand-coded τ-rule MAPPO | 0.19–0.57 | 0.01 ± 0.02 | 0.37 ± 0.09 | 0.03 ± 0.02 |
| 2 | MAPPO + PAH | 0.17–0.62 | 0.00 ± 0.01 | 0.32 ± 0.04 | 0.02 ± 0.01 |
| 3 | Fixed-weight MAPPO | 0.81–1.31 | 0.41 | 0.86 | 0.20 |
| 3 | MAPPO + PAH | 0.85–1.26 | 0.10 | 0.97 | 0.10 |
| 3 | MAPPO + PAH, Hungarian off | 1.20–1.71 | 0.61 | 0.74 | 1.06 |

Stage 2 final values: mean ± std over 5 seeds. The safety reward is on in about 1 drone-step in 60 to 1 in
600, mostly because of obstacles; the conflict graph (PAH's only source of τ) flags a conflict far less.

> **Correction (2026-10-12, verified by Manish's Claude):** an earlier version concluded from these numbers
> that α "can only matter this often". That does not follow: the safety *advantage* uses the shared
> critic's TD term and is non-zero on most steps. Whether α changes the learning signal is answered by the
> advantage-correlation check below.

### α spread check — `output/alpha_spread_check.png`

| Stage | Method | α median (final) | α 10th pct (final) | % steps α < 0.5 (final) |
|---|---|---|---|---|
| 2 | Fixed-weight MAPPO | 0.50 | 0.50 | 0 |
| 2 | Hand-coded τ-rule MAPPO | 0.90 ± 0.00 | 0.90 ± 0.00 | 0.00 ± 0.01 |
| 2 | MAPPO + PAH | 0.88 ± 0.05 | 0.71 ± 0.02 | 0.01 ± 0.01 |
| 3 | MAPPO + PAH | 0.87 | 0.70 | 0.03 |
| 3 | MAPPO + PAH, Hungarian off | 0.90 | 0.70 | 0.70 |

**What drives MAPPO + PAH's α** (`output/alpha_vs_target_distance.csv`, final models, 50 stochastic
episodes): with no conflict (≥ 98.9% of drone-steps) α still ranges 0.70–0.90 and tracks **distance to the
target**, not danger: corr(α, distance) = −0.73, −0.88, −0.89, −0.33, −0.79 for Stage 2 seeds 42–46,
−0.92 at Stage 3, −0.83 with Hungarian off. Median α ≈ 0.88–0.90 near the target, 0.70 beyond 300 units.

So in practice α behaves like three nearly fixed weightings: 0.5 (Fixed-weight MAPPO), ≈ 0.9 (Hand-coded
τ-rule MAPPO, because τ is almost always at its maximum), ≈ 0.7–0.9 by target distance (MAPPO + PAH).

### IGAT-MARL metrics check — `output/igat_marl_metrics_check.png`

| Stage | Method | Loss-of-separation pair-steps per episode | Active conflict edges per step |
|---|---|---|---|
| 2 | Fixed-weight MAPPO | 0.098 ± 0.038 | 0.0016 ± 0.0007 |
| 2 | Hand-coded τ-rule MAPPO | 0.064 ± 0.030 | 0.0010 ± 0.0003 |
| 2 | MAPPO + PAH | 0.100 ± 0.049 | 0.0014 ± 0.0007 |
| 3 | Fixed-weight MAPPO | 0.215 ± 0.166 | 0.0039 ± 0.0028 |
| 3 | MAPPO + PAH | 0.185 ± 0.163 | 0.0030 ± 0.0026 |
| 3 | MAPPO + PAH, Hungarian off | 0.870 ± 0.243 | 0.0514 ± 0.0182 |

Stage 2: mean ± std over 5 seeds; Stage 3: mean ± 95% CI over 200 episodes. Drone–drone near-misses are
rare; MAPPO + PAH and Fixed-weight MAPPO do not differ; removing Hungarian raises near-misses ~4.7× and
active edges ~15×.

### Advantage-correlation check — `output/advantage_correlation_check.png`

The actor in v3 learns from `w = α·z(A_mission) + (1−α)·z(A_safety)` (z = separate z-normalization over
the batch). Algebraic fact (verified, gate 3): for constant α, `α·A_mission + (1−α)·A_safety` *before*
normalization is exactly the plain combined-reward advantage; α's mixing can only make a difference through
the separate normalization (or through α inside the combined reward).

Final checkpoints, 10 batches each (Stage 2: mean ± std over the 5 seed means):

| Stage | Method | α mean | corr(mission adv., safety adv.) | raw std mission / safety | cosine(own-α signal, α = 0.5 signal) | magnitude own / α = 0.5 | **corr(own-α signal, plain combined advantage)** |
|---|---|---|---|---|---|---|---|
| 2 | Fixed-weight MAPPO | 0.50 | −0.52 ± 0.03 | 3.22 / 2.32 | 1.00 | 1.00 | **0.96 ± 0.01** |
| 2 | Hand-coded τ-rule MAPPO | 0.90 | 0.00 ± 0.06 | 2.59 / 4.09 | 0.78 ± 0.02 | 1.29 ± 0.03 | **0.99 ± 0.00** |
| 2 | MAPPO + PAH | 0.85 | −0.03 ± 0.12 | 2.66 / 3.97 | 0.79 ± 0.04 | 1.28 ± 0.07 | **0.98 ± 0.01** |
| 3 | Fixed-weight MAPPO | 0.50 | −0.27 | 3.75 / 2.27 | 1.00 | 1.00 | **0.95** |
| 3 | MAPPO + PAH | 0.84 | +0.22 | 3.57 / 4.28 | 0.85 | 1.15 | **0.99** |
| 3 | MAPPO + PAH, Hungarian off | 0.87 | +0.51 | 4.22 / 4.43 | 0.91 | 1.09 | **1.00** |

Stage 3 checkpoints across training (early / middle / late / final) show the same pattern
(`output/tables.md`).

**What it shows (measured):**
1. **For every method, the actor's learning signal is 95–100% correlated with the plain combined-reward
   advantage** — each method trains almost exactly like ordinary MAPPO on its own combined reward
   `α·r_mission + (1−α)·r_safety`. The separate mission/safety mixing changes the signal by only a few
   percent.
2. **The sign of corr(mission advantage, safety advantage) depends on α:** negative for Fixed-weight MAPPO
   (−0.52 / −0.27 — Manish's "opposite" case appears here), about zero for the α ≈ 0.9 methods at Stage 2,
   positive at Stage 3. No single sign holds; the critic's fit differs between methods.
3. Re-mixing the *same* batch with α = 0.5 instead of the run's own α would change its direction moderately
   (cosine 0.78–0.91). This is a counterfactual about the mixing step only; it does not correspond to any
   trained method.

**Interpretation (hypothesis, not proven):** since every method is effectively plain MAPPO on a combined
reward, and z-normalization removes the overall scale, the methods' rewards differ only where the safety
reward is non-zero (0.2–1.7% of drone-steps) and, for MAPPO + PAH, through the distance-dependent scaling of
the mission reward. That leaves little room for α to change behaviour — consistent with the tie on success.
A direct test would be to train plain MAPPO on the same combined rewards and compare; that is training, so
it belongs to a later phase.

## What this means (for discussion — nothing decided)

1. **The failures are obstacles, and PAH cannot see obstacles** (code fact: τ comes only from the
   drone–drone conflict graph; collision-type check).
2. **α behaves like three nearly fixed weightings**, and **the advantage mixing gives α very little
   leverage**: the actor's signal is essentially the ordinary combined-reward advantage for every method.
3. **Obstacle sensing is the likely bottleneck for success itself** (four axis-projected clearances vs the
   base paper's 35-beam LiDAR).
4. **Hungarian assignment keeps drones apart** (near-misses ~4.7×, edges ~15× without it; −20.5 points
   success in `v3/results-table`).

Directions these numbers point to (Ayesha, Manish and the supervisor decide):
- two value heads (mission value, safety value) so the safety advantage is a real safety signal —
  Manish's open question 2, which these results support;
- give PAH the danger that matters (obstacle proximity / time-to-collision as an input);
- better obstacle sensing (LiDAR-like rays, as in the base paper);
- a setting with real mission-vs-safety conflict, so arbitration has something to do.

## Caveats

- Stage 3: one seed (42). Training-like replay is an approximation of training conditions.
- 50 replay episodes per checkpoint: the safety-reward frequency curves are noisy point to point; the level
  (≈ 1% or less) is the finding.
- Collision kind is read on the step the episode ended; `both` never occurred.
- "Near goal" = a drone involved was within the target radius (25 units) of its assigned target.

## Files

| File | What |
|---|---|
| `diagnostics.ipynb` | the notebook (10 cells; gates in Cells 2 and 6) |
| `diag.py` | instrumented rollout (`run_episode`), α per method, `advantage_batch` |
| `PLAN-after-review.md` | the verified plan these steps follow |
| `output/eval_episodes.csv` | one row per evaluation episode (3600) |
| `output/training_like_replay.csv` | one row per checkpoint (all runs) |
| `output/alpha_vs_target_distance.csv` | α vs target distance, final MAPPO + PAH models |
| `output/advantage_correlation.csv` | one row per advantage batch (270) |
| `output/tables.md`, `output/summary.json` | all tables, machine-generated |
| `output/*_check.png/.svg` | figures, one per check |
