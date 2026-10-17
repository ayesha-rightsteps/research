# v4 Phase 3 — base-paper experiments on the trained models (report)

Run 2026-10-17 21:12–22:53 (`run_phase3.sh`, 70 batches, 0 errors, 2,390 result files). Plan: `PLAN.md`.
All tables: `output/phase3_summary.md` (from `summarize.py`); per seed: `output/phase3_per_seed.csv`;
figures: `output/figures/p3_fig1…8` (from `figures.py`).

**What was done.** No training. The 180 trained models (9 methods × 2 stages × 10 seeds; RMAPPO excluded) were
re-evaluated with one test setting changed at a time, 200 deterministic episodes each, evaluation seed 7001.
"Trained setting" = Stage 2: 5 drones, 10 discs; Stage 3: 8 drones, 20 discs; moving targets; assignment every step;
no sensor noise. Its numbers are the main results (identical, checked).

**How to read it.** Phase 3 has no new primary claim (PLAN.md Section 3, fixed before the run). Every comparison is
secondary, no multiple-testing correction. Between methods: 95% Welch CI on the success difference; within one
method (change from the trained setting): paired 95% t CI over the 10 seeds. CI above 0 = better, below 0 = worse,
otherwise not settled. Settings other than the trained one are generalisation tests: every method is expected to
drop, and a drop is not a failure.

## 1. Main question: does MAPPO + PAH stay ahead of Fixed-weight MAPPO?

**Yes, in all 31 settings tested** (Stage 2: 14, Stage 3: 17); the 95% CI is above 0 in every one
(figure `p3_fig2_pah_lead`). Range of the lead:

| Setting family | Stage 2 | Stage 3 |
|---|---|---|
| Trained setting | +7.0 [+2.8, +11.1] | +8.6 [+1.7, +15.4] |
| Obstacle density 10–50 discs | +9.8 to +11.3 | +5.5 to +14.7 |
| Static targets | +9.6 [+3.1, +16.1] | +16.6 [+7.8, +25.4] |
| Assignment every 50 steps | +6.6 [+2.0, +11.1] | +7.7 [+1.1, +14.3] |
| Swarm size 3–10 | +3.5 to +8.5 | +4.8 to +12.3 |
| LiDAR noise σ 0.02–0.1 | — | +8.5 to +8.7 |

The weakest cases are the smallest swarm (N = 3: S2 +3.5 [+0.6, +6.3], S3 +4.8 [+0.1, +9.5]) — with three drones
there are few conflicts, so a learned safety/mission balance has the least to do. The lead tends to grow when the
setting gets harder (denser obstacles in Stage 3, larger swarms in Stage 3).

Against **Hand-coded τ-rule MAPPO** the picture is the same as in the main results: in Stage 3 the lead is settled in
16 of 17 settings (not settled only at N = 3); in Stage 2 it is not settled in most settings (+1.6 to +6.6) and
settled only for 8–10 drones. Against the other methods (Plain MAPPO, IGAT-style MAPPO, DA-MAPPO (2D), MAPPO, IPPO,
MAPPO + PAH (Hungarian off)) the lead is settled in every setting, except MAPPO + PAH (Hungarian off) in Stage 2 at
10 and 30 discs (not settled).

## 2. Obstacle density (E1; DA-MAPPO ENV-1/2/3) — `p3_fig1_density`

Success falls for every method as discs are added (Stage 3, MAPPO + PAH: 93.5 → 82.7 → 70.3 → 51.3 → 40.4 at
10/20/30/40/50 discs). The order of the methods stays the same at every density; MAPPO + PAH is first everywhere.
At 50 discs in Stage 3: MAPPO + PAH 40.4, Hand-coded τ-rule MAPPO 28.6, Fixed-weight MAPPO 25.7, IGAT-style
MAPPO 8.0, DA-MAPPO (2D) 2.7, MAPPO 2.6, IPPO 1.9. Like the DA-MAPPO paper's ENV-1 → ENV-3 trend, the methods
without a conflict graph fall towards zero. These models were trained at one density only (DA-MAPPO used a
curriculum), so this is a generalisation test.

## 3. Static vs moving targets (E2; DA-MAPPO) — `p3_fig3_static`

All methods were trained with moving targets. With static targets **every method does worse** (settled for 17 of
18 method–stage pairs; MAPPO Stage 2 not settled). This is the opposite of the intuition "static is easier", and we
do not have a tested explanation; the likely one is that static targets are a different situation from the one the
models were trained in (the trained policies may rely on target motion, e.g. targets moving away from obstacles).
This should be reported as an observation, not explained beyond that without a test. MAPPO + PAH loses less than
Fixed-weight MAPPO (Stage 3: −7.0 vs −15.0), so its lead grows to +16.6.

## 4. Assignment every step vs every 50 steps (E3; DA-MAPPO ablation) — `p3_fig4_assign50`

Re-assigning only every 50 steps costs every method a little: −0.7 to −1.3 points in Stage 2, −1.3 to −3.8 in
Stage 3 (settled for 9 of 10). So real-time re-assignment helps, but the effect is small in our setting. The lead of
MAPPO + PAH over Fixed-weight MAPPO is unchanged (+6.6 / +7.7). Limit: test-time change only; the models were
trained with every-step assignment.

## 5. Swarm size 3–10 (E4; IGAT-MARL) — `p3_fig5_swarm`

Only methods whose observation does not depend on the number of drones (MAPPO, DA-MAPPO (2D) and IPPO see all
teammates, so they cannot run at another size without retraining). From 3 to 10 drones, Stage 3 models:

| Method | N = 3 | N = 8 (trained) | N = 10 | 3 → 10 |
|---|---|---|---|---|
| MAPPO + PAH | 90.5 | 82.7 | 80.5 | −10.0 |
| Fixed-weight MAPPO | 85.7 | 74.2 | 68.3 | −17.4 |
| Hand-coded τ-rule MAPPO | 86.5 | 71.5 | 70.6 | −15.9 |
| Plain MAPPO | 65.2 | 44.2 | 37.4 | −27.8 |
| IGAT-style MAPPO | 77.3 | 46.8 | 32.5 | −44.8 |

MAPPO + PAH degrades least; IGAT-style MAPPO degrades most. Stage 2 models (trained on 5) show the same order
(MAPPO + PAH 90.7 → 81.9; IGAT-style MAPPO 84.4 → 57.2). The models generalise both to smaller and to larger swarms
than they were trained on.

## 6. IGAT-MARL metrics (E5) — `p3_fig6_swarm_los`

Loss of separation (LoS: drone pairs closer than 3 collision radii, summed over an episode) and active conflict-graph
edges per step, counted from the environment for every method.
- LoS grows with swarm size for every method, as in IGAT-MARL. IGAT-style MAPPO has by far the most LoS
  (Stage 3: 2.64 per episode at N = 8, 4.26 at N = 10); the methods with a conflict-graph observation and
  re-assignment stay around 0.3–1.2.
- **MAPPO + PAH does not have clearly less LoS than Fixed-weight MAPPO or Hand-coded τ-rule MAPPO** (Stage 3 trained:
  0.63 vs 0.55 vs 0.73). Its advantage is in mission success, not in fewer close passes. (LoS is a close-approach
  count, not a collision; collisions are in the success numbers.) No CI was computed for LoS; it is descriptive.
- In the main setting, MAPPO + PAH (Hungarian off) has much more LoS and edges than MAPPO + PAH (Stage 3: 1.85 vs
  0.63; edges 0.0275 vs 0.0044): without assignment, drones crowd the same targets.

## 7. Sensor noise (E6) — `p3_fig7_noise`

Gaussian noise on the LiDAR distances up to σ = 0.1 of the ray range changes success by at most about 3 points for
any method (Stage 3, MAPPO + PAH 82.7 → 80.8). The lead over Fixed-weight MAPPO stays +8.5 to +8.7. All methods
are robust to this noise level. (IGAT-style MAPPO rises slightly, 46.8 → 49.5, inside its wide CI.)

## 8. Decision time (E7) — `p3_fig8_timing`

Actor forward pass for the whole swarm, 1 CPU thread, laptop: MAPPO + PAH and Fixed-weight MAPPO 0.04–0.05 ms per
step for 3–10 drones (the same: PAH is used for the training reward, not for choosing actions). IGAT-style MAPPO
0.23–0.29 ms (graph attention), about 6× slower but still far below a real-time limit. Absolute values depend on
the machine; the conflict graph and the environment step are not included.

## 9. What this adds to the thesis (and what not)

- Adds: the PAH result is not specific to one test setting — the lead over Fixed-weight MAPPO holds across density,
  target motion, assignment frequency, swarm size and sensor noise; the base-paper-style experiments reproduce the
  base papers' trends (density hurts methods without a conflict graph most; larger swarms hurt IGAT-style most;
  real-time assignment helps).
- Does not add: a new primary claim; evidence that PAH reduces close approaches (LoS); a training-time version of the
  DA-MAPPO assignment ablation or of a density curriculum (would need training).
- Unexplained, to be stated as such: all methods do worse on static targets.
