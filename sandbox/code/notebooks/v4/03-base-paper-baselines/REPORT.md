# PAH Phase 2 Scorecard — MAPPO + PAH against the base-paper baselines

MS thesis · Ayesha Khalil · Phase 2 results · 15 Oct 2026 (RMAPPO added 16 Oct 2026)
Online version: https://claude.ai/artifact/4bu8Wa31ccoxmtztcwWfAz

All methods were trained in the same 2D multi-UAV environment with moving targets. Each method has 10 training
seeds (42–51), and every seed was tested on the same 200 starting layouts (deterministic actions, evaluation
seed 7001). Success means every drone reaches its own target with no collision inside the time limit.

**Status:** Phase 2 closed · 86 runs (80 + RMAPPO Stage 3 seeds 42–47) · 10 methods with results. RMAPPO was reported as
trained with the shared settings: Stage 3 only, 6 seeds, Stage 2 not run (see "RMAPPO note" below).

Stage 2 = 5 drones, 10 obstacles. Stage 3 = 8 drones, 20 obstacles.

---

## Table 1 — Success, collision, timeout (% of episodes)

Success = mean over 10 seeds ± 95% confidence half-width.

| Method | S2 Success | S2 Coll. | S2 Timeout | S3 Success | S3 Coll. | S3 Timeout |
|---|---|---|---|---|---|---|
| *Our methods (Phase 1b)* | | | | | | |
| **MAPPO + PAH** | **86.8 ± 3.8** | 13.2 | 0.0 | **82.7 ± 4.0** | 17.3 | 0.0 |
| Fixed-weight MAPPO | 79.8 ± 2.2 | 20.2 | 0.0 | 74.2 ± 6.1 | 25.8 | 0.0 |
| Hand-coded τ-rule MAPPO | 84.8 ± 3.1 | 15.2 | 0.0 | 71.4 ± 5.9 | 28.6 | 0.0 |
| MAPPO + PAH (Hungarian off) | 83.4 ± 3.9 | 16.6 | 0.0 | 68.4 ± 7.4 | 31.2 | 0.4 |
| Plain MAPPO | 68.9 ± 3.6 | 31.1 | 0.0 | 44.2 ± 4.7 | 55.8 | 0.0 |
| *Base-paper methods in our environment (Phase 2)* | | | | | | |
| IGAT-style MAPPO | 73.0 ± 5.4 | 26.2 | 0.9 | 46.8 ± 9.5 | 52.3 | 1.0 |
| DA-MAPPO (2D) | 59.9 ± 2.4 | 40.0 | 0.2 | 28.8 ± 2.7 | 70.5 | 0.6 |
| MAPPO | 55.8 ± 4.2 | 43.4 | 0.8 | 21.9 ± 4.1 | 76.4 | 1.7 |
| IPPO | 57.4 ± 7.4 | 39.6 | 2.9 | 17.1 ± 5.1 | 77.0 | 6.0 |
| RMAPPO † | not run | | | 0.0 ± 0.0 | 86.3 | 13.7 |

† RMAPPO: Stage 3 only, 6 seeds (42–47), shared settings. See "RMAPPO note".

## Table 2 — Speed and path (successful episodes only)

T_ave = steps until all drones arrived. L_ave = mean path length per drone (world units). Hits = collisions summed
over all 2,000 test episodes of a method, drone–drone / drone–obstacle.

| Method | S2 T_ave | S2 L_ave | S2 Hits D–D / D–O | S3 T_ave | S3 L_ave | S3 Hits D–D / D–O |
|---|---|---|---|---|---|---|
| **MAPPO + PAH** | 54 | 188 | 6 / 258 | 61 | 173 | 16 / 330 |
| Fixed-weight MAPPO | 59 | 200 | 12 / 391 | 76 | 199 | 24 / 492 |
| Hand-coded τ-rule MAPPO | 58 | 190 | 8 / 296 | 73 | 182 | 10 / 561 |
| MAPPO + PAH (Hungarian off) | 78 | 301 | 76 / 255 | 109 | 342 | 127 / 495 |
| Plain MAPPO | 60 | 194 | 10 / 612 | 63 | 171 | 9 / 1106 |
| IGAT-style MAPPO | 76 | 225 | 50 / 473 | 118 | 312 | 215 / 831 |
| DA-MAPPO (2D) | 68 | 197 | 15 / 784 | 103 | 203 | 51 / 1359 |
| MAPPO | 76 | 209 | 46 / 822 | 113 | 214 | 116 / 1412 |
| IPPO | 101 | 226 | 62 / 731 | 177 | 293 | 242 / 1297 |
| RMAPPO † | not run | | | — (no successes) | — | 115 / 920 ‡ |

‡ RMAPPO hits are over 1,200 test episodes (6 seeds), not 2,000.

## Table 3 — MAPPO + PAH minus each method (success points, Welch 95% CI)

Whole interval above zero → PAH better. Interval contains zero → not settled.

| Compared with | Stage 2 [95% CI] | Verdict | Stage 3 [95% CI] | Verdict |
|---|---|---|---|---|
| Fixed-weight MAPPO | +7.0 [+2.8, +11.1] | PAH better | +8.5 [+1.7, +15.4] | PAH better |
| Hand-coded τ-rule MAPPO | +2.0 [−2.6, +6.6] | not settled | +11.2 [+4.6, +17.9] | PAH better |
| MAPPO + PAH (Hungarian off) | +3.3 [−1.8, +8.5] | not settled | +14.3 [+6.3, +22.3] | PAH better |
| Plain MAPPO | +17.9 [+13.0, +22.8] | PAH better | +38.5 [+32.8, +44.2] | PAH better |
| IGAT-style MAPPO | +13.8 [+7.7, +20.0] | PAH better | +36.0 [+26.0, +45.9] | PAH better |
| **DA-MAPPO (2D) — primary comparison** | **+26.9 [+22.6, +31.2]** | **PAH better** | **+53.8 [+49.3, +58.4]** | **PAH better** |
| MAPPO | +31.0 [+25.8, +36.3] | PAH better | +60.8 [+55.5, +66.1] | PAH better |
| IPPO | +29.3 [+21.4, +37.3] | PAH better | +65.6 [+59.6, +71.6] | PAH better |
| RMAPPO † (6 seeds) | not run | | +82.7 [+78.7, +86.7] | PAH better |

## Table 4 — Base paper: DA-MAPPO, Table V (dynamic multi-target)

Copied from the DA-MAPPO paper (IEEE Internet of Things Journal). Their setup: 3D Gazebo simulator with LiDAR,
256-unit networks, ~3 million training steps with an obstacle curriculum; their T_ave / L_ave use different units.
**Absolute numbers cannot be compared with ours; the ranking of methods can.**

| Method | ENV-1 (30 obst.) Success | ENV-1 Coll. | ENV-2 (40) Success | ENV-2 Coll. | ENV-3 (50) Success | ENV-3 Coll. |
|---|---|---|---|---|---|---|
| **DA-MAPPO** | **99** | 1 | **95** | 5 | **90** | 10 |
| RMAPPO | 85 | 15 | 69 | 31 | 67 | 33 |
| MAPPO | 83 | 17 | 70 | 30 | 64 | 36 |
| IPPO | 78 | 22 | 57 | 43 | 53 | 47 |
| NavRL | 63 | 34 | 53 | 43 | 32 | 65 |
| EGO-Planner v2 | 53 | 45 | 51 | 48 | 43 | 57 |

## Side by side — hardest setting, success %, best first

| Rank | Base paper (ENV-3) | | Ours (Stage 3) | |
|---|---|---|---|---|
| 1 | **DA-MAPPO** | **90** | **MAPPO + PAH** | **82.7** |
| 2 | RMAPPO | 67 | IGAT-style MAPPO | 46.8 |
| 3 | MAPPO | 64 | DA-MAPPO (2D) | 28.8 |
| 4 | IPPO | 53 | MAPPO | 21.9 |
| 5 | EGO-Planner v2 | 43 | IPPO | 17.1 |
| 6 | NavRL | 32 | RMAPPO † | 0.0 |

- **Same shape.** In both, dynamic target re-assignment beats MAPPO with a fixed assignment (paper: DA-MAPPO 90 vs
  MAPPO 64; ours: DA-MAPPO (2D) − MAPPO = +7.0 [2.3, 11.6] at Stage 3), and IPPO is the weakest MARL method.
- **Our addition sits on top.** MAPPO + PAH is above every base-paper method at both stages, the way DA-MAPPO is above
  its baselines in the paper.
- **Our baselines score lower than the paper's.** All methods share our small 64-unit network and 8,000-episode
  budget, with no curriculum, so Stage 3 is harder for them.

## Where the Stage 3 gap to DA-MAPPO (2D) comes from

DA-MAPPO (2D) and Plain MAPPO use the same agent, reward and settings; the only difference is that Plain MAPPO sees
conflict-graph features instead of raw teammate positions. So the gap splits into three measured steps:

| Step | From → to | Stage 2 | Stage 3 |
|---|---|---|---|
| Conflict-graph observation | DA-MAPPO (2D) → Plain MAPPO | +9.0 [5.0, 13.0] | +15.4 [10.3, 20.4] |
| Two value heads (mission + safety) | Plain MAPPO → Fixed-weight MAPPO | +10.9 [7.0, 14.9] | +30.0 [22.8, 37.1] |
| **PAH learned α** | Fixed-weight MAPPO → MAPPO + PAH | **+7.0 [2.8, 11.1]** | **+8.5 [1.7, 15.4]** |

All three steps help at both stages. PAH's own share is the smallest, but its interval stays above zero at both
stages.

## RMAPPO note — why it shows 0%

- **Result.** Stage 3, seeds 42–47, all 8,000 episodes: success 0.0% on every seed (200 test episodes each); collision
  86.3%, timeout 13.7%. Training-time checks (every 100 episodes) were also 0% on every seed. MAPPO, the same method
  without the GRU, reaches 21.9% here.
- **Cause found: exploration collapse.** The policy's action spread (log std) fell to the lower clamp −4.0 by about
  episode 2,000 (seed 45: −2.1 at ep 500, −3.2 at ep 1,000, −4.0 at ep 2,000) and the other seeds end at −2.9 to −3.5.
  All other methods end at −0.04 to −0.9. With almost no exploration the policy stopped improving before it had learnt
  to navigate.
- **Not an implementation bug in the recurrent replay.** Log-probabilities recomputed over stored chunks match the
  ones from data collection (max difference 1e-6).
- **Likely reason (not tested).** The shared minibatch of 64 drone-steps means only 4 sequences of 16 steps per
  gradient step (640 noisy steps per update). The original RMAPPO (Yu et al., MAPPO paper) updates on large batches.
- **Decision (Ayesha, 16 Oct 2026).** Report as trained, without retuning; Stage 2 and seeds 48–51 were not run.
- **How to read it.** This row shows that RMAPPO fails under our shared settings; it does not show how well a tuned
  RMAPPO would do. In the base paper RMAPPO scored 67% at ENV-3.

## Limits — what a reviewer may ask

- **One 2D environment.** No claim is made against the paper's 3D Gazebo numbers.
- **Shared hyperparameters.** Every method used the same settings, as the base paper did; base-paper methods were not
  tuned separately.
- **PAH vs hand-coded τ-rule at Stage 2 is unresolved:** +2.0 [−2.6, 6.6]. PAH is clearly ahead at Stage 3.
- **PAH design.** One PAH fix came after looking at the first Stage 3 seed-42 result. It corrected a bias and was not
  tuned on the test seeds; recorded in the Phase 1b README.
- **RMAPPO did not learn under the shared settings** (0.0% at Stage 3, 6 seeds; Stage 2 not run). A reviewer can call this
  an under-tuned baseline; the PAH − RMAPPO gap should not be used as evidence for PAH. See "RMAPPO note".
- **Multiple comparisons.** Secondary comparisons in Table 3 are not corrected for multiple testing.

---

Sources: `v4/02-redesign/output/eval_raw/` (Phase 1b, 100 JSON) and `v4/03-base-paper-baselines/output/eval_raw/`
(Phase 2, 86 JSON). Phase 2 evaluation used `02-redesign/evaluate.py:evaluate_run` (same protocol as Phase 1b).
