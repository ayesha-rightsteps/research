# v4 Phase 1b — environment and PAH redesign: results

Plan: `PLAN.md` (settings frozen in §10), PAH fix: `PAH_FIX_PLAN.md`. Session logs: `sessions/2026-10-12.md`
(§17–22), `sessions/2026-10-14.md`.

## Setup (identical for every method)

| | Stage 2 | Stage 3 |
|---|---|---|
| Drones / obstacle discs (radius 12) | 5 / 10 | 8 / 20 |
| World, speed, target radius, moving targets | 500×500, 5, 25, speed 1 | same |
| Safety reward | shaping within 20 units of a drone or disc surface; collision −10 | same |
| Training | 8000 episodes, from scratch, PPO settings of v3 (lr 3e-4, entropy 0.003, hidden 64) | same |
| Seeds | 42–51 (10 per method) | same |

Methods: **Plain MAPPO** (one value head, combined reward 0.5/0.5), **Fixed-weight MAPPO** (α = 0.5, mission and
safety value heads), **Hand-coded τ-rule MAPPO** (α = 0.1 + 0.8·τ/3), **MAPPO + PAH** (risk-learning PAH:
α = 0.9 − 0.8·p, p = predicted risk, regressed onto the observed safety cost-to-go; no gradient from the actor loss),
**MAPPO + PAH (Hungarian off)** (no assignment mechanism: drone i → target i for the whole episode, `fixed-arbitrary`; not the Phase 2 "fixed at reset" mode). τ = steps until the nearest drone **or** obstacle
collision, capped at 3.

## Final evaluation (Step 5)

`evaluate.py` → `summarize.py` → `figures.py`. Deterministic actions, 200 episodes per model, evaluation seed 7001
(same 200 layouts for every model of a stage), each model in its own training configuration (read from its
`config.json`). `evaluate.py` was cross-checked against the training-time evaluator on 4 models (identical results).
Rounding: one decimal, half up (10-seed means are often exactly x.x5; the primary difference is exactly 8.55); updated 2026-10-16. Full tables: `output/eval_summary.md`; per seed: `output/eval_per_seed.csv`; raw: `output/eval_raw/`.

| Method | Stage 2 success % | Stage 3 success % | Stage 3 collision % | Stage 3 T_ave | Stage 3 L_ave |
|---|---|---|---|---|---|
| Plain MAPPO | 68.9 | 44.2 | 55.8 | 63.1 | 171 |
| Fixed-weight MAPPO | 79.9 | 74.2 | 25.8 | 75.5 | 199 |
| Hand-coded τ-rule MAPPO | 84.8 | 71.5 | 28.6 | 72.9 | 182 |
| **MAPPO + PAH** | **86.8** | **82.7** | **17.3** | **61.3** | 173 |
| MAPPO + PAH (Hungarian off) | 83.5 | 68.4 | 31.2 | 108.9 | 342 |

Timeouts ≈ 0 everywhere: an episode that fails, fails by a collision, almost always with an obstacle.

### Comparisons (PLAN §5 reading rule: 95% Welch CI of the difference in mean success, 10 vs 10 seeds)

| Comparison | Stage 2 | Stage 3 |
|---|---|---|
| **MAPPO + PAH − Fixed-weight MAPPO** (primary question, asked at Stage 3) | +7.0 [+2.8, +11.1] better | **+8.6 [+1.7, +15.4] better** |
| MAPPO + PAH − Hand-coded τ-rule MAPPO (learned α vs the formula) | +2.0 [−2.6, +6.6] inconclusive | +11.3 [+4.6, +17.9] better |
| MAPPO + PAH − Plain MAPPO | +17.9 [+13.0, +22.8] better | +38.5 [+32.8, +44.2] better |
| MAPPO + PAH − MAPPO + PAH (Hungarian off) | +3.4 [−1.8, +8.5] inconclusive | +14.3 [+6.3, +22.3] better |
| Fixed-weight MAPPO − Plain MAPPO (separate value heads) | +11.0 [+7.0, +14.9] better | +30.0 [+22.8, +37.1] better |

### What it means

1. **Primary question: MAPPO + PAH beats Fixed-weight MAPPO at Stage 3** (+8.6 points, CI above 0), and at Stage 2.
   It is also the fastest to finish (T_ave 61 vs 76 steps at Stage 3): the extra safety does not cost time.
2. **Learning α beats the hand-coded formula at Stage 3** (+11.3). At Stage 2 the two are not distinguishable.
   The formula on its own is not better than a fixed α = 0.5 at Stage 3 (71.5 vs 74.2), so what helps is the
   learned shape, not just "lower α in danger".
3. **What PAH learned** (`fig3_alpha_by_tau`): α ≈ 0.13–0.19 in danger (τ < 1) and ≈ 0.81–0.85 when nothing is
   ahead — and, unlike the formula, it stays low already at 1 ≤ τ < 2 (0.25–0.32 vs 0.51): it switches to
   safety earlier. 80–89% of the danger signals come from obstacles, the hazard that ends episodes.
4. **Separate mission and safety value heads** are the largest single gain (+30 points over Plain MAPPO at
   Stage 3); every arbitration method builds on them.
5. **Hungarian assignment matters**: without it paths are ~1.6–2× longer, drone–drone collisions rise
   (127 vs 16 at Stage 3) and Stage 3 success drops by 14 points.

### Limits — say these in the thesis

- **The PAH fix came after a look at a main seed.** The first (residual) PAH was stopped after its Stage 3 seed 42
  run showed the bias (α pushed towards the mission in danger; `runs_pah_v1_flawed/`). The fix removes a measured
  bias (the gradient of the policy objective w.r.t. α); it was not tuned on results: no PAH setting was searched,
  the risk scale is the collision penalty (10), and α's range 0.1–0.9 is the original one. The flawed v1 result is
  reported as a finding.
- Stage 3 seed-to-seed spread is large (success 72.5–91 for MAPPO + PAH), so the Stage 3 CIs are wide; the primary
  CI's lower end is +1.7 points.
- Secondary comparisons are not corrected for multiple testing; only the primary question was fixed in advance.
- Training-time numbers (20-episode evaluations, `sessions/2026-10-12.md` §22.9) are higher than these final ones
  (e.g. MAPPO + PAH Stage 3 88.2 vs 82.7); the ranking is the same. The numbers above are the official ones.
- Obstacle density is moderate (10 / 20 discs); the denser 20 / 40 setting is for Phase 3.

## Folders

`runs/` (100 trained runs + launchers and logs), `runs_pah_v1_flawed/` (evidence for the v1 bias), `sanity/`,
`sanity_fixed/`, `tuning/` (Step 3, Plain MAPPO only), `output/` (Step 5 results and figures).
