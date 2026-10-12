# Plan — fixes and next checks after the Phase 0 self-review

**Status:** verified by Manish's Claude (session Section 16); Step 2 revised per his review; implementation
started 2026-10-12 after Ayesha's go-ahead. Progress is logged in the session file.
Written 2026-10-12. Ayesha's instruction: write everything down first; Manish's Claude verifies it;
only after that do we implement and run anything.

Context: `sessions/2026-10-12.md`, Sections 12 (Phase 0 diagnostics) and 13 (self-review, which found
one wrong interpretation).

---

## 0. Names used in this plan (no short codes)

| Full name used here | What it is | Key in v3 code / files (unchanged) |
|---|---|---|
| **Fixed-weight MAPPO** | MAPPO, mission/safety weight α fixed at 0.5 | `B4`, `fixed-alpha/` |
| **Hand-coded τ-rule MAPPO** | MAPPO, α = 0.1 + 0.8·(τ/3), nothing learned | `H`, `h-baseline/` |
| **MAPPO + PAH** | MAPPO, α = τ-rule + learned residual (the thesis method) | `M`, `var-alpha/` |
| **MAPPO + PAH, Hungarian off** | same, but target pairing fixed at reset (ablation) | `M-noHungarian`, `ablation-hungarian/` |
| **Stage 2** | 5 drones, 5 obstacles (5 training seeds: 42–46) | |
| **Stage 3** | 8 drones, 10 obstacles (training seed 42 only) | |
| **Mission advantage / safety advantage** | the two advantage streams α mixes in the actor loss | `adv_m`, `adv_s` |

Phase 0 check names: **collision-type check**, **safety-reward frequency check**, **α spread check**,
**IGAT-MARL metrics check** (loss-of-separation, active conflict edges). New in this plan:
**advantage-correlation check**.

---

## 1. Verification checklist for Manish's Claude (what is already done)

Please check these independently before anything below is implemented.

| # | Claim | Where | How to verify |
|---|---|---|---|
| 1.1 | `v4/common/v3_env.py` is an exact copy of the v3 environment, conflict graph, actor and PAH | `v4/common/v3_env.py` (header lists sources) | Diff its classes against `v3/results-table/paper_style_results.ipynb` cells 2–4 and `v3/stage3/var-alpha/kaggle_stage3_pah_seed42test.ipynb` cell 4. Run `diagnostics.ipynb` Cell 2 (gate): 200/200 episodes must match v3 for Stage 3 MAPPO + PAH and Stage 2 Fixed-weight MAPPO (seed 43). |
| 1.2 | Collisions are almost all drone–obstacle (Stage 2 ~99%; Stage 3: Fixed-weight MAPPO 50/53, MAPPO + PAH 56/56) | `00-diagnostics/output/eval_episodes.csv`, `README.md` | Recount from the CSV; read `diag.collision_kind()`. |
| 1.3 | PAH's τ input comes only from drone–drone conflicts, never from obstacles | `v3_env.py`: `ConflictGraph.update`, `tau_collision` | Read the code: `update()` takes drone positions/velocities only. |
| 1.4 | With no conflict (99.9% of drone-steps), MAPPO + PAH's α tracks distance to target: corr = −0.73 (Stage 2), −0.92 (Stage 3) | session 2026-10-12, Section 12.3 (computed in a one-off check, **not yet in the notebook**) | Re-run: final MAPPO + PAH models, 50 stochastic episodes, env seed 9101, correlate α with `d_target` where `n_conflict == 0`. |
| 1.5 | **Shared-critic advantage computation** (the reason the safety-reward frequency interpretation is wrong) | `v3/stage3/var-alpha/…ipynb` cell 4: `RolloutBuffer.compute_gae_components`, `update()` | Confirm: `delta_s = r_safety + γ·V(s') − V(s)` with V the single critic trained on the combined reward `α·r_mission + (1−α)·r_safety`; mission and safety advantages are z-normalized separately, then `w_adv = α·A_mission + (1−α)·A_safety`. |
| 1.6 | The shared baseline was a deliberate, documented simplification, not a bug | `docs/research/01_pah_design.md` Section 9 ("Option B lite", decided 2026-09-14 after Manish's review) | Read it. |

---

## 1b. Laptop training speed test (approved by Ayesha 2026-10-12, run before the review)

**Question:** can training run on the laptop (Apple M3, 8 cores) instead of only Kaggle, and can several
runs go in parallel? Speed only — no result from this test is used anywhere.

**Method:** run the *unchanged* v3 Stage 3 MAPPO + PAH training notebook code (cells 1–6 of
`v3/stage3/var-alpha/kaggle_stage3_pah_seed42test.ipynb`, executed from a scratch folder so nothing is
written into `v3/`), same config and seed 42, but stop after ~600 episodes. Only two overrides: the
episode count, and the warm-start path pointed at the existing local file
`v3/stage2/stage2-b/output/final_model.pt` (read-only). Compare the cumulative time at the same episode
with Kaggle's own log for that run (Kaggle: 64.4 min for 7939 episodes). Then run 4 and 8 copies at once
(different seeds) to see how the laptop scales.

**Output:** numbers in the session log only; scratch outputs deleted.

## 2. Planned work (in order)

### Step 1 — Correct the safety-reward frequency interpretation (text only, no new numbers)

**What is wrong now:** `00-diagnostics/README.md` ("What this means", point 2, and the D2/D3 paragraphs),
`handbook/code/notebooks/v4/00-diagnostics/diagnostics.md`, and session Section 12.4 say that because the
safety reward is on in only ~0.2–1.7% of drone-steps, "PAH has little to arbitrate" / "α can matter only
that often". That is wrong: the safety advantage uses the shared critic's TD term, so it is non-zero on
almost every step even when the safety reward is zero (checklist 1.5).

**Change:**
- Keep the measured numbers (how often the safety reward is on) — they are correct.
- Replace the conclusion with: "the safety *reward* is rare, but the safety *advantage* is not, because it
  shares the combined critic's baseline; whether α's mixing changes the learning signal is tested by the
  advantage-correlation check (Step 2)".
- Also correct session Section 13.2 point 3: the shared baseline was a deliberate simplification
  (checklist 1.6), not an unknown design question; the open question is whether to keep it in v4.
- Replace short codes with full names in these files (Section 0).

**Files:** `00-diagnostics/README.md`, `handbook/code/notebooks/v4/00-diagnostics/diagnostics.md`,
`sessions/2026-10-12.md` (a correction note, not rewriting history).
**Risk:** none to data. **Time:** ~20 min.

### Step 2 — Advantage-correlation check (new measurement)

**Question:** When α changes, does the actor's learning signal actually change? If the mission advantage
and safety advantage are nearly the same signal, then Fixed-weight MAPPO (α = 0.5), Hand-coded τ-rule MAPPO
(α ≈ 0.9) and MAPPO + PAH (α ≈ 0.7–0.9) all push the policy in nearly the same direction — which would
explain why they tie.

**Method (replicates the training update's advantage computation, nothing is trained):**
1. For each run: load a checkpoint (actor, critic, PAH if present) via `v4/common/v3_env.py`. A small
   loader extension is needed because the current `load_checkpoint` ignores the critic: add a `Critic`
   class copied verbatim from the v3 notebook cell 4 (same extraction method as `v3_env.py`).
2. Collect a rollout exactly the way training builds one batch: `rollout_steps = 512` environment steps
   (episodes reset inside the segment), **stochastic** actions, env with `success_bonus = 20` (as in
   training — Phase 0 used 0, which did not matter there but matters for rewards here).
   Per step store: `r_mission`, `r_safety`, α (Fixed-weight: 0.5; τ-rule: formula; PAH: head), combined
   reward `α·r_mission + (1−α)·r_safety`, critic value `V(flatten(obs of all drones))`, done.
3. Compute, exactly as `compute_gae_components` does (γ = 0.99, λ = 0.95, shared value V): mission
   advantage and safety advantage per drone-step; z-normalize each over the batch.
4. Measure — **revised 2026-10-12 after Manish's review (session Section 16.2); thresholds dropped,
   report first, decide after:**
   - **sign and size of corr(mission advantage, safety advantage)**, on the raw advantages (before
     z-normalization). Manish's point: with a well-fitted critic the two are expected to be *opposite*
     (safety ≈ −α/(1−α) × mission); with a poor critic they can move together. Which one holds decides how
     to read everything else.
   - **raw std of each advantage before z-normalization** (normalization hides the scale difference).
   - **cosine and magnitude, separately,** between `w(own α)` and `w(0.5)` (and `w(0.9)`), where
     `w(α) = α·z(A_mission) + (1−α)·z(A_safety)` exactly as in training. Correlation alone is misleading
     because it ignores scale.
   - **(addition from the algebra check)** corr(`w(own α)`, plain combined-reward advantage). Exact identity,
     checked to machine precision on synthetic data: for constant α,
     `α·A_mission + (1−α)·A_safety = A_combined` (the ordinary MAPPO advantage of the combined reward).
     So the α-mixing adds nothing by itself; any effect must come from the separate z-normalization or from α
     inside the combined reward. If corr(`w(own α)`, `A_combined`) ≈ 1, the mixing step is redundant in
     practice.
   - Note: comparing `w(own α)` with `w(0.5)` changes α only in the mixing, not in the reward the critic
     learned — it is a counterfactual about the mixing step only, and is reported as such.
5. Repeat for 10 batches per checkpoint (different env seeds), report mean ± std.

**Runs:** Stage 2 (all three methods, seeds 42–46, final models) and Stage 3 (Fixed-weight MAPPO,
MAPPO + PAH, MAPPO + PAH Hungarian off; seed 42; final model plus 3 checkpoints across training).

**Gate before trusting it:** (a) the GAE code is the v3 `RolloutBuffer.compute_gae` /
`compute_gae_components`, extracted verbatim (not retyped); (b) on real Fixed-weight MAPPO batches (α constant
= 0.5) the identity `0.5·A_mission + 0.5·A_safety = A_combined` must hold to float precision — if it does not,
the extraction or the batch construction is wrong; (c) the critic weights load without missing/unexpected keys.

**Decision rule:** none fixed in advance (Manish, 16.2: report first, set thresholds after seeing the
sign and scale). The original "≥ 0.9 / ≤ 0.5 correlation" rule is withdrawn.

**Output:** `00-diagnostics/output/advantage_correlation.csv`, one figure, README section.
**Where:** new cells in `diagnostics.ipynb` (or a separate `advantage_check.ipynb` if Manish prefers),
helper code in `diag.py`. **Time:** ~1–2 h to write, minutes to run (CPU).

### Step 3 — Safety-reward frequency and α spread checks on all five Stage 2 seeds

**Why:** Phase 0 ran these on seed 42 only, while the collision-type and IGAT-MARL checks used all five
Stage 2 seeds — inconsistent, and the extra seeds are cheap.
**Change:** extend `TRAIN_RUNS` in `diagnostics.ipynb` Cell 4 to seeds 42–46 for Stage 2; report mean ±
std across seeds; also move the α–target-distance correlation (checklist 1.4) into the notebook so it is
reproducible. Also rename the pass from "training conditions" to "training-like replay (approximation)"
in the notebook and README, since it replays saved checkpoints on a new seed rather than reproducing the
actual training rollouts.
**Time:** ~30 min write, ~2 min run.

### Step 4 — Full names in all human-facing labels

Figures, tables and READMEs from Phase 0 (and this morning's `v3/results-table` fig11) label methods as
"B4 (fixed α)", "M (PAH)", "H (τ-formula)". Change only the display labels to the Section 0 names and
regenerate the figures. Numbers do not change. Registry keys in code stay as they are (v3 data uses them).
**Time:** ~30 min.

### Step 5 — Handbook entries still pending from this morning

Mirror the morning changes in `handbook/` (Hinglish): fig11 / Cell 15 in `handbook/code/results_table.md`,
and the rewritten comparison section of the 09 report in `handbook/research/`.
**Time:** ~20 min.

---

## 3. What this plan will NOT do

- No training, no Kaggle, no environment change, nothing written in `v3/`.
- No Phase 1 decision. Phase 1 (environment changes, base-paper baselines) is decided after Steps 1–3,
  by Ayesha, Manish and the supervisor.

## 4. Open questions for Manish

1. Is the advantage-correlation check's decision rule (Step 2) acceptable, or should the thresholds differ?
2. For v4: keep the shared critic baseline ("Option B lite"), or move to two value heads
   (mission value, safety value) so the safety advantage is a real safety signal? (Depends partly on Step 2.)
3. Is replaying saved checkpoints on a new seed an acceptable stand-in for "training conditions", or should
   v4 training log these quantities directly during training from now on? (Recommended: log them directly
   in v4.)
