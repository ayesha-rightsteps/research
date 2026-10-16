# 11 — Thesis reporting notes (how to state the v4 results)

Written 2026-10-16 from Manish's review (`sessions/2026-10-16.md` §3–5) and the fact-check of it (same file, §9–10).
Purpose: one place that says how each result must be worded in the thesis, so the text never claims more than the
data shows. Numbers come from `v4/03-base-paper-baselines/output/eval_summary.md` (made by `summarize.py`) unless
stated otherwise. All final numbers: 200 test episodes per model, deterministic actions, evaluation seed 7001.

## 1. The primary result

- Pre-registered before training (`v4/02-redesign/PLAN.md` §5): **Stage 3, MAPPO + PAH vs Fixed-weight MAPPO,
  mission success**, read with a 95% Welch CI over 10 vs 10 seeds.
- Result: **+8.6 [+1.7, +15.4]** points (exact difference 8.55). MAPPO + PAH is higher on 9 of 10 seed indices.
- Write: *"MAPPO + PAH is better than Fixed-weight MAPPO at 8 drones; the gain is plausibly between about 2 and 15
  points."* Always give the CI with the number.
- Do not write: "PAH improves success by 8.6 points" without the CI, "PAH is much better", or any wording that
  treats the lower end (+1.7) as large.
- Earlier documents say +8.5; that came from float noise in rounding (§9 below). Use +8.6.

## 2. Primary vs secondary comparisons

- Only §1 was pre-registered as primary. PLAN §5 lists the secondary ones (collisions, Stage 2, τ-rule, Plain MAPPO,
  Hungarian on/off). The Phase 2 comparisons with base-paper methods are also secondary.
- No multiple-comparison correction was applied. Label everything except §1 as **secondary** and say that no
  correction was applied.
- Stage 2, MAPPO + PAH vs Hand-coded τ-rule MAPPO: **+2.0 [−2.6, +6.6], not settled.** Write: *"the learned α is
  clearly better than the hand-coded rule only at 8 drones (Stage 3: +11.3 [+4.6, +17.9])."*

## 3. The PAH fix and seed 42 (answer before it is asked)

Facts (`sessions/2026-10-12.md` §22.2–22.4, `v4/02-redesign/PAH_FIX_PLAN.md`):
- The first (residual, RL-gradient) PAH was trained on all seeds; its Stage 3 seed-42 run was the first finished.
  Its training-time success (last 10 evaluations, seed 999) was 56.0% vs Hand-coded τ-rule MAPPO 86.5%.
- The cause was found by mechanism, not by performance: the gradient of α·A_m + (1−α)·A_s with respect to α is
  A_m − A_s, so in danger PAH pushes α towards the mission (measured δ = +0.200, the maximum, when τ < 1). The bias
  was already described in v3 (`01_pah_design.md` §9.2).
- The design was changed **once** (risk-learning PAH). Its gates were a synthetic-data test and a 300-episode smoke
  run, not seed-42 performance. Then all 40 runs were trained with no further change. The design is frozen.

Robustness check to report (seed 42 left out, seeds 43–51, 9 vs 9):

| Comparison | Seeds 42–51 | Without seed 42 |
|---|---|---|
| Stage 3, PAH − Fixed-weight MAPPO | +8.6 [+1.7, +15.4] | +7.9 [+0.7, +15.1] |
| Stage 3, PAH − Hand-coded τ-rule MAPPO | +11.3 [+4.6, +17.9] | +12.8 [+5.9, +19.6] |
| Stage 2, PAH − Fixed-weight MAPPO | +7.0 [+2.8, +11.1] | +7.7 [+3.1, +12.2] |

On seed 42 itself the new PAH (79.5%) is below Hand-coded τ-rule MAPPO (82.0%) at Stage 3, so the design was not
shaped to win that seed. Optional extra: a separate replication on fresh seeds with its rule written first, not
pooled with seeds 42–51.

## 4. The first PAH (v1) is a finding

Write it as a result: *"A learned α trained through the policy objective is biased against safety."* Give the
mechanism (gradient sign) and the measured δ. Its performance number is **one seed, training-time** and must be
labelled so. Then: the risk-learning PAH, with the same inputs and network, works (§1).

PAH now: same 3 inputs and 3→32→1 network; α = 0.9 − 0.8·p, where p is the predicted risk, learned by regression on
the observed safety cost-to-go; no gradient from the actor loss. It still "learns from experience" (targets are
observed costs, not a formula). If asked "is this a learned τ-rule?": Stage 3 +11.3 [+4.6, +17.9] over the
hand-coded rule; Stage 2 not settled.

## 5. Ablation names

- "MAPPO + PAH (Hungarian off)" uses `fixed-arbitrary` (drone i → target i, fixed). Describe it as **no assignment
  mechanism at all**, not as "no real-time re-assignment".
- The effect of real-time re-assignment alone is measured in Phase 2 with the plain agent: DA-MAPPO (2D) − MAPPO
  (`every-step` vs `fixed-at-reset`): Stage 2 +4.2 [−0.4, +8.7] (not settled), Stage 3 +7.0 [+2.3, +11.6].

## 6. Base-paper methods

- Write *"same environment, same training budget, same hyperparameters"*. Do not write that the base papers'
  numbers were reproduced.
- Hyperparameters were tuned once on Plain MAPPO (sanity seeds 101/102) and then frozen for every method. Say so.
- Absolute numbers are lower than in the papers (ours Stage 3: DA-MAPPO (2D) 28.9, MAPPO 21.9, IPPO 17.1; DA-MAPPO
  paper ENV-3: 90 / 64 / 53). The ranking pattern matches (dynamic assignment above rigid assignment, IPPO weakest).
- The base-paper methods keep one value head (faithful to the published methods); the effect of two heads is
  measured separately (Fixed-weight MAPPO − Plain MAPPO).
- IGAT-style MAPPO uses width 64 and no dropout (shared settings), not IGAT-MARL's own 128 / 0.6.

## 7. The gap to DA-MAPPO (2D)

Headline is **PAH's own +8.6**, not the +53.9 gap. The gap can be explained step by step with controlled
comparisons (each step changes one thing), and is only roughly additive:

| Step | Stage 3 |
|---|---|
| Conflict-graph observation (DA-MAPPO (2D) → Plain MAPPO) | +15.4 [+10.3, +20.4] |
| Two value heads (Plain MAPPO → Fixed-weight MAPPO) | +30.0 [+22.8, +37.1] |
| PAH learned α (Fixed-weight MAPPO → MAPPO + PAH) | +8.6 [+1.7, +15.4] |

## 8. RMAPPO

Not a performance number. Under the shared settings its exploration collapsed (log std at the −4.0 clamp by about
episode 2,000; 0% on all 6 seeds; recurrent replay checked, no bug). Keep it **out of the main tables**; put it in
an appendix with the reason (6 seeds, Stage 3 only, Stage 2 not run, original batch setting not tried). Never show
"RMAPPO 0.0 ± 0.0" as if it were a result, and never drop it silently. Whether to re-run it with its original
batch setting is still open (Manish recommends a sanity check first).

## 9. Tables and numbers

- T_ave and L_ave are computed on successful episodes only. Add under every such table: *"conditioned on success;
  methods have different success rates, so these are not computed on the same episodes."* Success and collision are
  the ranking metrics.
- Never mix training-time numbers (20 episodes, seed 999) with final numbers (200 episodes, seed 7001) in one table.
- Rounding: one decimal, half up. Each seed's success is k/200, so 10-seed means are often exactly x.x5. CIs are
  computed from unrounded values.
- Reproducibility: all 186 final evaluations were re-run on 2026-10-16 with `02-redesign/evaluate.py` (and
  `--phase2`) and were byte-identical; tables are regenerated by `summarize.py` in both folders.
