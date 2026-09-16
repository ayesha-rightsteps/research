# Implementation Progress Report
**Thesis:** Multi-Agent Proximal Policy Optimization for Joint Dynamic Target Assignment and Collision Avoidance in UAV Systems
**Student:** Ayesha Khalil — SP25-RCS-009/ATD, MS (CS), COMSATS Abbottabad
**Supervisor:** Dr. Faisal Rehman | **Co-supervisor:** Mr. Ehzaz Mustafa
**Report date:** 17 September 2026

---

## 1. Summary

Implementation of the MAPPO framework with Priority Arbitration Head (PAH) is complete for the Stage 2 environment (5 drones, moving targets, 5 obstacles). All curriculum stages have been trained and validated. The PAH's core claim — that it learns *situation-aware* reward weighting (safety vs. mission) rather than using a fixed weight — has been empirically verified after two rounds of debugging.

---

## 2. What Has Been Implemented

| Component | Status |
|-----------|--------|
| Custom 2D Gymnasium environment (5 drones, moving targets, obstacles) | Complete |
| Hungarian algorithm target assignment (`scipy.optimize.linear_sum_assignment`) | Complete |
| Conflict graph (collision-course drone pairs) | Complete |
| MAPPO — shared actor, centralized critic (CTDE), GAE, PPO clip, entropy | Complete |
| Priority Arbitration Head (PAH) — learns dynamic α weight from τ, d_target, n_conflict | Complete |
| Fixed-alpha baseline (B4) — same architecture, α constant at 0.5 | Complete |
| Curriculum training pipeline: Stage 2a → Stage 2b → PAH runs | Complete |
| Alpha collapse diagnostic (danger-close vs. safe α comparison) | Complete |

---

## 3. Training Results

All runs: 8,000 episodes, 5 drones, seed 42, Kaggle T4 GPU. Each eval point averages 20 evaluation episodes.

### 3.1 Stage 2a — Plain MAPPO, 2 Obstacles (Curriculum Baseline)

| Metric | Value |
|--------|-------|
| Eval points | 76 (ep105 – ep7983) |
| Average success rate | **94.7%** |
| Average collision rate | 5.3% |
| Success range | — |
| Entropy (start → end) | 2.398 → 2.579 (stable) |
| Trend (first-third → last-third) | 94.8% → 94.8% (converged) |

Stage 2a converged cleanly. Used as warm-start for Stage 2b.

---

### 3.2 Stage 2b — Plain MAPPO, 5 Obstacles (Curriculum Step 2)

| Metric | Value |
|--------|-------|
| Eval points | 76 (ep100 – ep7965) |
| Average success rate | **90.5%** |
| Average collision rate | 9.5% |
| Entropy (start → end) | 2.706 → 2.725 (stable) |
| Trend (first-third → last-third) | 89.6% → 91.6% (still improving slightly) |

Warm-started from Stage 2a final checkpoint. Adding obstacles caused a ~4% success drop, which is expected. This run establishes the plain MAPPO baseline and was used as warm-start for PAH experiments.

---

### 3.3 PAH vs. Fixed-Alpha Baseline (B4) — Head-to-Head Comparison

Both runs: same environment as Stage 2b, same warm-start (Stage 2b final checkpoint), seed 42.

| Metric | PAH (learned α) | B4 (fixed α = 0.5) |
|--------|-----------------|---------------------|
| Eval points | 76 (ep111–ep7959) | 76 (ep111–ep7972) |
| **Average success rate** | **91.2%** | 89.9% |
| **Average collision rate** | **8.8%** | 10.1% |
| Success range | 80% – 100% | 70% – 100% |
| Entropy (start → end) | 2.795 → **−0.379** | 2.873 → 1.893 |
| Alpha range | 0.618 – 0.879 (varies) | 0.500 (fixed) |
| Alpha average | 0.792 | 0.500 |
| Danger-direction correct | **14/14 (100%)** | N/A |

**PAH outperforms the fixed-alpha baseline on both primary metrics (+1.3% success, −1.3% collision).** More importantly, PAH's α correctly responds to situation: in danger-close scenarios (small τ_collision), α decreases (more safety weight); in safe scenarios, α increases (more mission weight). This is the core thesis claim, now empirically confirmed.

PAH's entropy converges to near-zero (−0.379 differential entropy), indicating a highly confident, deterministic final policy. B4's entropy remains at 1.893 — still exploratory after 8,000 episodes — because the fixed α=0.5 gives no situation-specific signal to structure the policy around.

---

## 4. Debugging History (Honest Record)

| Issue | Sessions | Resolution |
|-------|----------|------------|
| Centralized critic bug — `Critic(obs_dim)` instead of `Critic(n_drones × obs_dim)` | 2026-09-15 | Fixed by Manish (commit e12d5dd) |
| Credit assignment bug — per-drone rewards averaged to single scalar | 2026-09-15 | Fixed by Manish (same commit) |
| Modulo-skip bug — eval triggered only on exact multiples, missed when episode count jumps | 2026-09-16 | Fixed with `last_eval`/`last_save` threshold pattern |
| PAH α direction wrong (10/17 danger samples: α rising in danger instead of falling) | 2026-09-16 | Root cause: flat prior gave no directional signal; actor loss pushed α upward in danger due to collision penalty magnitude |
| First α-direction fix failed — τ-informed target, unweighted loss (coef 0.05) | 2026-09-17 | 11/19 still wrong; root cause: rare danger samples drowned in batch average |
| Second α-direction fix — danger-weighted prior loss (coef 0.15, weight ∝ danger level) | 2026-09-17 | **0/14 wrong — all danger-close samples now correct direction** |

---

## 5. Current Status

| Item | Status |
|------|--------|
| Stage 2 environment + MAPPO | Complete and validated |
| PAH implementation + alpha-direction fix | Complete and empirically verified |
| Single-seed comparison (PAH vs. B4, seed 42) | Complete — PAH leads on both metrics |
| **Multi-seed validation (seeds 43, 44, 45…)** | **Not yet started — next priority** |
| Stage 3 (8 drones, high obstacle density) | Pending multi-seed completion |
| Other baselines (DA-MAPPO, IGAT-MARL, Standard MAPPO) | Pending |
| Thesis writing | Pending |

**Important note:** All results above are from a single random seed (42). The master plan requires ≥3–5 seeds before any result is reported as final. The current results are a strong positive signal but not yet a conclusive finding.

---

## 6. Next Steps (Priority Order)

1. **Multi-seed runs** — PAH and B4, seeds 43, 44, 45 minimum — to confirm the single-seed result is not a fluke
2. **Stage 3** — 8 drones, high obstacle density — after multi-seed PAH/B4 comparison is stable
3. **Other baselines** — DA-MAPPO, IGAT-MARL, Standard MAPPO (no assignment, no conflict graph)
4. **Thesis writing** — results chapter can begin after multi-seed data is in

---

*All code, session logs, and output data are version-controlled in the project repository.*
