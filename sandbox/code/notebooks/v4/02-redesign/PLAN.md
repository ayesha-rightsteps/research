# Plan — v4 Phase 1b: environment and PAH redesign

**Status: PLAN ONLY — nothing implemented or run** (Ayesha, 2026-10-12: "1b ko plan karna, abhi run
nahin karna"). Built later step by step, each step with a gate; nothing in `v3/` is touched. The supervisor
is shown the finished work (Ayesha's decision).

## 0. Why

Phase 0 and Phase 1a showed four causes for PAH having no effect:
1. 94–100% of failures are obstacle collisions — in every method, including Plain MAPPO (Phase 1a).
2. PAH cannot see obstacles: its time-to-collision τ comes only from drone–drone conflicts.
3. The v3 mixing of mission and safety advantages gives α no leverage: Plain MAPPO (no mixing) does as well
   as Fixed-weight MAPPO (89.9 ± 1.4 vs 88.2 ± 2.2%, Phase 1a).
4. Obstacles are points, sensed through four axis-aligned distances — far from the base paper's dense
   physical obstacles and 35-beam LiDAR.

All Stage 2 methods sit at ~88–90%, held back by the same obstacle failures. Phase 1b removes the four
causes and nothing else.

## 1. The four changes

| # | Change | Design (proposed default) | Why |
|---|---|---|---|
| 1 | **Sized, denser obstacles** | Discs of radius 12 in the same 500×500 world (drone speed 5, collision radius 3, target radius 25 unchanged, so reward scales stay valid). Collision if centre distance < 12 + 3. Stage 2: 20 discs, Stage 3: 40 discs (≈3.6% and ≈7.2% of the area). Targets bounce off discs as off walls, so a goal never sits inside an obstacle. | Obstacles are what drones fail on; points are unrealistically easy to miss and hard to sense |
| 2 | **LiDAR-like sensing** | 24 rays at 15° spacing, range 100 (≈20 steps of travel), each = distance to the nearest disc surface or wall ÷ 100. Replaces the four axis-projected clearances. Observation: own position (2) + velocity (2) + target offset (2) + 24 rays + 4 conflict neighbours × 5 = **50** (was 30). | The v3 obstacle feature is misleading (a disc 200 units to the side but 1 unit ahead reads as "1 unit away") |
| 3 | **PAH's τ covers every hazard** | τ = min(τ_drone, τ_obstacle), capped at 3 steps. τ_drone as in v3 (conflict graph). τ_obstacle = steps until the drone, at its current velocity, reaches a disc surface (ray–circle intersection); 3 if none within the cap. PAH keeps its **three inputs** (τ, d_target, n_conflict) and its architecture; only τ's computation changes. The synopsis defines τ as "time-to-collision", not drone-only. | PAH must see the danger that actually ends episodes |
| 4 | **Separate mission and safety value heads** | Critic: shared body, two heads V_mission and V_safety, loss = ½(V_m − R_m)² + ½(V_s − R_s)². Mission advantage = GAE(r_mission, V_mission), safety advantage = GAE(r_safety, V_safety); each z-normalized over the batch; actor gets α·A_mission + (1−α)·A_safety. | With one shared critic the mixing collapses to plain MAPPO (exact identity, Phase 0; confirmed in training, Phase 1a). With separate heads the safety advantage is a real safety signal, so α has leverage (Manish's open question 2) |

**Kept the same:** Hungarian assignment every step; drone–drone conflict graph (horizon 3, danger radius
9) for neighbour features and n_conflict; reward terms (the safety reward now uses the distance to the
nearest drone **or disc surface**); success = all drones at their targets with no collision; PPO
hyperparameters (lr 3e-4, γ 0.99, λ 0.95, clip 0.2, entropy 0.003, 10 epochs, batch 64, 512-step
rollouts); PAH residual design (α_min 0.1, α_max 0.9, δ scale 0.2).

## 2. Methods trained in the new environment

| Method | α | Critic |
|---|---|---|
| Plain MAPPO | — (combined reward 0.5·r_mission + 0.5·r_safety, one advantage) | one head |
| Fixed-weight MAPPO | 0.5 | two heads |
| Hand-coded τ-rule MAPPO | 0.1 + 0.8·τ/3 (hazard τ) | two heads |
| **MAPPO + PAH** (thesis method) | τ-rule + learned residual (hazard τ) | two heads |
| MAPPO + PAH, Hungarian off (ablation) | as above, target pairing fixed at reset | two heads |

## 3. Fairness rules (decided now, before any run)

1. **Any tuning happens on Plain MAPPO only** (Step 3), and the resulting settings are applied unchanged to
   every method. No method gets its own tuning.
2. Every method: same environment code, same seeds, same episode budget, same hardware (laptop), same
   evaluation protocol.
3. Warm start: none (the observation size changes from 30 to 50). Every run trains from scratch.

## 4. Sample size (power check — the lesson from Phase 1a)

Observed seed-to-seed std of Stage 2 success: ~1.7 points (pooled over six groups). With two-sided
α = 0.05 and 80% power:

| Seeds per method | 95% CI half-width of a difference | Smallest difference reliably detected |
|---|---|---|
| 5 | ±2.5 points | ~4 points |
| **10** | **±1.6 points** | **~3 points** |
| 15 | ±1.3 points | ~2.5 points |

Phase 1a's "match = CI inside ±3" rule could only pass with ~0 difference at 5 seeds — a planning error.
**Phase 1b uses 10 seeds per method per stage.** Stage 3's spread is unknown (v3 had one seed); it is
measured in Step 4 and reported; seeds are not added after seeing results.

## 5. Primary question and reading rule (decided now)

- **Primary:** Stage 3, MAPPO + PAH vs Fixed-weight MAPPO (both two heads), mission success rate.
- **Secondary:** collision rate; share of obstacle collisions; loss-of-separation per episode; the same
  comparisons at Stage 2; MAPPO + PAH vs Hand-coded τ-rule MAPPO (does learning the residual add anything);
  MAPPO + PAH vs Plain MAPPO (does arbitration add anything at all); Hungarian on vs off.
- **Reading rule:** difference in means with a 95% Welch CI over the 10 seeds.
  - CI entirely above 0 → MAPPO + PAH better.
  - CI entirely below 0 → MAPPO + PAH worse.
  - CI inside ±3 points and containing 0 → equivalent within 3 points.
  - Otherwise → inconclusive.
  Reported as it comes out, including another tie.
- **Mechanism checks (always reported):** α spread and what drives it; advantage correlation (is the actor
  signal still ~plain MAPPO? it should not be); how often τ_obstacle vs τ_drone sets PAH's τ.

## 6. Steps and gates

**Step 1 — `v4/common/env_v4.py`** (new file; `v3_env.py` stays frozen). Discs, LiDAR, hazard τ, targets
bouncing off discs, per-step info for logging (collision type, safety-reward cause, which hazard set τ,
loss-of-separation pairs, active edges).
*Gate (unit tests, `v4/common/test_env_v4.py`):* a ray aimed at a disc returns the exact surface distance;
a ray that misses returns the range; a ray stops at the wall; collision exactly at 12 + 3 and not at
12 + 3 + ε; τ_obstacle equals a hand calculation for a straight approach and is 3 (cap) when moving away;
targets never end a step inside a disc; same seed → identical episode; a random policy runs 1000 episodes
with no error and no NaN.

**Step 2 — `v4/common/mappo_v4.py`.** Actor (input 50), critic with one or two heads, PAH (v3 class,
unchanged), buffer with per-head GAE, Plain mode. Code copied from v3 where unchanged, every change marked.
*Gate:* (a) per-head GAE equals a hand-computed 5-step example; (b) Plain mode reproduces the v3 update
exactly on a fixed batch (same losses and gradients, with the observation size set to 30 for this test);
(c) two-head update on a fixed batch runs and both value losses decrease over a few updates.

**Step 3 — sanity training (decision point).** Plain MAPPO, Stage 2 config, 2 seeds, 8000 episodes,
laptop (~15 min). *Gate:* training success clearly rises and ends well above the level of a random policy;
evaluation shows obstacle collisions no longer ~100% of failures. If it fails: (i) the base paper's obstacle
curriculum (start with 5 discs, add discs during training up to the stage's count); (ii) if still failing,
more episodes. Every attempt is recorded. Tuning stops at the first setting that passes and is then frozen
for all methods (Section 3).

**Step 4 — main training.** 5 methods × 10 seeds × Stage 2 and Stage 3 = 100 runs, 8 in parallel on the
laptop, `caffeinate` on. Estimate: Stage 2 ~7 batches × 12 min ≈ 1.5 h; Stage 3 ~7 batches × 25 min ≈
3 h (Stage 3 time to be confirmed in Step 3's speed log). Training logs the diagnostics directly
(Manish: log them during training).

**Step 5 — evaluation.** Deterministic, 200 episodes, evaluation seed 7001 (disjoint from training seeds
42–51). Tables in the base paper's format (success / collision / timeout / T_ave / L_ave), the Section 5
comparisons, the mechanism checks, and figures in the thesis house style.

## 7. Decisions I am making (can be changed before Step 1)

Disc radius 12; 20 / 40 discs; 24 rays, range 100; targets bounce off discs; each advantage stream
z-normalized separately; τ cap 3 steps; training from scratch; 10 seeds; the reading rule in Section 5.

## 8. Planned files (created when implementation starts)

```
v4/common/env_v4.py, mappo_v4.py, test_env_v4.py, test_mappo_v4.py
v4/02-redesign/
├── PLAN.md          ← this file
├── README.md        ← results
├── train.py         ← one (method, stage, seed) per process
├── sanity/          ← Step 3 runs
├── runs/<stage>/<method>/seed-<n>/
├── evaluate.ipynb   ← Step 5
└── output/
```

## 9. What Ayesha needs to do

Nothing to run by hand. During Steps 3–4 the laptop stays on the charger with the lid open (~15 min, then
~4–5 h — can run overnight).
