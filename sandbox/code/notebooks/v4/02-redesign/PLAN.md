# Plan — v4 Phase 1b: environment and PAH redesign

**Status: PLAN ONLY — nothing implemented.** Written 2026-10-12. Built step by step, each step with a gate;
nothing in `v3/` is touched. The supervisor will be shown the finished work (Ayesha's decision).

## 0. Why (one paragraph)

Phase 0 and Phase 1a showed: (1) 94–100% of failures are obstacle collisions; (2) PAH cannot see obstacles
— its time-to-collision τ comes only from drone–drone conflicts; (3) the v3 way of mixing the mission and
safety advantages gives α no measurable leverage — Plain MAPPO does as well as Fixed-weight MAPPO
(89.9 ± 1.4 vs 88.2 ± 2.2%); (4) obstacles are points that a drone senses through four axis-aligned
distances, far from the base paper's 35-beam LiDAR and dense physical obstacles. So, as built, PAH had no
chance to matter. Phase 1b fixes the four causes, nothing else.

## 1. The four changes

| # | Change | Design (proposed default) | Why |
|---|---|---|---|
| 1 | **Sized, denser obstacles** | Discs of radius 12 units in the same 500×500 world (drone speed, world size and target radius unchanged, so the reward scales stay valid). Collision if centre distance < 12 + 3. Stage 2: 20 discs, Stage 3: 40 discs (~3.6% and ~7% of the area; base-paper-like density, decided by area — the paper gives no obstacle size). Targets also bounce off discs, so a goal never sits inside an obstacle. | Obstacles are what drones fail on; points are too easy and unrealistic |
| 2 | **LiDAR-like sensing** | 24 rays over 360°, range 100 units (~20 steps of travel), normalized distance to the nearest disc surface or wall. Replaces the four axis-projected clearances. Observation: own position/velocity (4) + target (2) + 24 rays + 4 conflict neighbours × 5 = 50. | The current obstacle feature is misleading; the base paper uses 35 rays |
| 3 | **PAH's τ covers every hazard** | τ = min(time-to-collision with the most urgent drone, time until the drone's current velocity hits a disc), capped at 3 steps. PAH keeps its **three inputs** (τ, d_target, n_conflict) — the synopsis defines τ as "time-to-collision", not drone-only, so the PAH design is unchanged; only τ's computation now includes obstacles. | PAH must see the danger that actually ends episodes |
| 4 | **Separate mission and safety value heads** | Critic outputs V_mission and V_safety (shared body, two heads), each trained on its own return. Mission advantage from V_mission, safety advantage from V_safety; each z-normalized; actor gets α·A_mission + (1−α)·A_safety. | With one shared critic the mixing collapses to plain MAPPO (Phase 0, 1a); with separate heads the safety advantage is a real safety signal and α has leverage (Manish's open question 2) |

Kept the same: Hungarian assignment every step, conflict graph (drone–drone), MAPPO/PPO hyperparameters,
reward terms (the safety reward now measures distance to the nearest drone **or disc surface**), success
definition (all drones at targets, no collision), deterministic 200-episode evaluation.

## 2. Methods trained in the new environment

| Method | α | Critic |
|---|---|---|
| Plain MAPPO | — (one combined reward, 0.5 / 0.5) | one head |
| Fixed-weight MAPPO | 0.5 | two heads |
| Hand-coded τ-rule MAPPO | 0.1 + 0.8·τ/3 (hazard τ) | two heads |
| MAPPO + PAH (the thesis method) | τ-rule + learned residual (hazard τ) | two heads |
| MAPPO + PAH, Hungarian off (ablation) | as above | two heads |

The base papers' methods (IPPO, DA-MAPPO-style, IGAT-style) and their experiments (obstacle-density and
swarm-size sweeps) come after this, in Phase 2/3, in the same environment.

## 3. Steps and gates

**Step 1 — `v4/common/env_v4.py` (new file; `v3_env.py` stays frozen).** Discs, LiDAR, hazard τ, targets
bouncing off discs, per-step logging (collision type, safety-reward cause, τ source, loss-of-separation,
active edges). *Gate:* unit tests on hand-built scenes — a ray pointing at a disc returns the exact surface
distance; a ray missing it returns the range; collision exactly at 12 + 3; τ_obstacle matches a hand
calculation; same seed → identical episode; with discs removed and 4 rays the observation logic still
behaves (sanity); a random policy runs 1000 episodes without errors.

**Step 2 — `v4/common/mappo_v4.py`.** Actor, two-head critic, PAH (same classes as v3, PAH unchanged),
buffer computing GAE per head, Plain-MAPPO mode (one head). Copied from the v3 code where unchanged, with
the change marked. *Gate:* (a) GAE per head equals a hand-computed toy example; (b) in Plain mode the update
is identical to the v3 update on the same batch (compare losses/gradients on a fixed batch); (c) with two
heads and α constant, the actor signal is no longer ~identical to the plain combined advantage (re-run the
Phase 0 advantage-correlation check on a short run — this is the point of change 4).

**Step 3 — sanity training (decision point).** Plain MAPPO, Stage 2 config, 2 seeds, 8000 episodes, from
scratch (the observation size changes, so no v3 warm start), on the laptop (~15 min). *Gate:* it learns
(training success clearly rises) and collisions are not ~all obstacle hits any more. If it does not learn:
add the base paper's obstacle curriculum (start with few discs, add more during training) and retry —
recorded, not hidden. Only after this works do we train the other methods.

**Step 4 — main training.** The five methods × 5 seeds, Stage 2 and Stage 3 (25 + 25 runs; ~2–3 h on the
laptop, 8 in parallel). Training logs the diagnostics directly (Manish: log them during training in v4).

**Step 5 — evaluation and checks.** Deterministic, 200 episodes, disjoint seed. Re-run the Phase 0 checks on
the new models (collision type, α spread, advantage correlation, IGAT-MARL metrics) to confirm α now has
leverage. Report success / collision / timeout / T_ave / L_ave per method with seed spread — whatever the
outcome, including another tie.

## 4. Decisions I am making (can be changed before Step 1)

Obstacle radius 12 and counts 20 / 40; 24 rays with range 100; targets bounce off discs; z-normalize each
advantage stream separately; τ cap 3 steps (as v3); train from scratch. Reason for each is in Section 1.

## 5. What Ayesha needs to do

- Nothing to run by hand. During Steps 3–4 the laptop must stay on the charger with the lid open
  (~15 min and ~2–3 h).
- Look at this plan; anything to change (especially Section 4) is easiest before Step 1.
