# Plan — v4 Phase 1a: plain MAPPO check

**Status:** implemented and run 2026-10-12 on Ayesha's instruction ("do what is right"), without a separate
review by Manish's Claude. Optional run C was included. Results: `README.md`. Plan text below unchanged.

## Names

Fixed-weight MAPPO (α = 0.5; v3 key `B4`) · Hand-coded τ-rule MAPPO (`H`) · MAPPO + PAH (`M`) ·
**Plain MAPPO** (new here: one combined reward, one ordinary advantage — no mission/safety split).
Stage 2 = 5 drones, 5 obstacles.

## 1. Question

Phase 0 (`../00-diagnostics/README.md`, advantage-correlation check) found that for every v3 method the
actor's learning signal is 95–100% correlated with the plain combined-reward advantage. Hypothesis: the three
v3 methods tie because each of them is, in effect, plain MAPPO on a combined reward.

**Test:** train Plain MAPPO and see whether it reaches the same success as Fixed-weight MAPPO. If it does, the
explanation of the tie becomes a measured result instead of a hypothesis.

## 2. Runs (all on the laptop, Stage 2, seeds 42–46)

| Run | What | Why |
|---|---|---|
| **A. Plain MAPPO** | Combined reward 0.5·r_mission + 0.5·r_safety; the actor uses the ordinary normalized combined-reward advantage | the test |
| **B. Fixed-weight MAPPO (laptop rerun)** | Unchanged v3 Fixed-weight MAPPO code | Same-hardware reference for A (CPU and GPU results are not bit-identical, so A must not be compared with the old Kaggle runs), and a check that laptop training reaches the Kaggle level |
| C. Plain MAPPO, combined reward with α = 0.9 *(optional — Manish decides)* | As A, but 0.9·r_mission + 0.1·r_safety | Tests whether the reward weighting itself matters once the mixing is gone |

10 runs (15 with C). Each Stage 2 run took ~44 min on Kaggle; the speed test suggests ~8 min on the laptop,
8 at a time → **~30 min for all of A and B**. This also gives the pending full-run speed confirmation.

## 3. Exactly what changes in the code

- **Base code:** the v3 notebook that trained Stage 2 Hand-coded τ-rule MAPPO and MAPPO + PAH,
  `v3/stage2/stage2-pah-v3-pah-change/var-alpha/kaggle_stage2_pah_allseeds.ipynb` (5-seed loop), with
  `use_pah = False`, `fixed_alpha = 0.5` → this is Fixed-weight MAPPO (run B).
- **Run A = run B + one line** in `update()`: the actor's advantage `w_adv = alpha*adv_m_flat + (1-alpha)*adv_s_flat`
  is replaced by the already-computed, currently unused `adv_t` (normalized combined-reward advantage,
  flattened). Nothing else changes: same critic, same reward, same hyperparameters, same warm start.
- **How it is run (nothing written in `v3/`):** a runner script in this folder reads the notebook's cells,
  applies only these string replacements — each guarded by an `assert` that the original text is present
  exactly once — and executes them from `runs/<run>/seed-<n>/`:
  1. the warm-start path → the existing local `v3/stage2/stage2-b/output/final_model.pt` (read-only);
  2. `use_pah` / `fixed_alpha` (and for run A, the one advantage line);
  3. torch threads = 1, matplotlib Agg (no figure windows).
  The runner prints the diff between the code actually executed for A and for B; it must be exactly the
  one advantage line.

## 4. Gates (stop if any fails)

1. **Base code equivalence:** the pah-v3 notebook with `use_pah = False` must match the notebook that trained
   the original Stage 2 Fixed-weight MAPPO (`stage2-pah-v0/fixed-alpha/kaggle_stage2_pah.ipynb`) in the
   environment, networks, buffer and `update()` (already known: `update()` identical, buffer identical
   except comment punctuation). Any other difference (config, warm start) is listed in the README before
   running.
2. **A vs B code diff = one line** (printed by the runner).
3. **Laptop reproduces the Kaggle level:** run B evaluated with the Phase 0 protocol must land in the range of
   the original Kaggle Fixed-weight MAPPO (89.2 ± 2.0% success over 5 seeds). If it is clearly outside
   (e.g. mean more than 2 std away), stop and investigate before reading run A.

## 5. Evaluation (same protocol as Phase 0 and `v3/results-table`)

Deterministic policy, 200 episodes, env seed 7001, every final model, through `../common/v3_env.py`.
Logged per episode: outcome, T_ave, L_ave, collision type, loss-of-separation, active edges (reusing
`../00-diagnostics/diag.py`). Training also logs wall time per run.

## 6. How the result will be read — proposal, Manish to approve before running

Compare A with B over the 5 seeds: difference in mean success with a 95% confidence interval (Welch).
- CI inside ±3 points and containing 0 → **Plain MAPPO matches Fixed-weight MAPPO** → supports the
  explanation of the tie.
- CI entirely below 0 → the mission/safety mixing does add something; the explanation is incomplete.
- CI entirely above 0 → the mixing hurts.
- Anything else → inconclusive, reported as such.

## 7. What this does NOT do

No environment change, no PAH change, no Stage 3 (v3 Stage 3 has one seed, too few for this comparison),
nothing written in `v3/`. The environment / PAH redesign (Phase 1b) waits for the supervisor.

## 8. Planned files (created only when implementation starts)

```
01-plain-mappo-check/
├── PLAN.md           ← this file
├── README.md         ← results
├── train_runner.py   ← applies the guarded overrides, runs one (run, seed)
├── evaluate.ipynb    ← gates 2–3 + evaluation + comparison
└── runs/
    ├── plain-mappo/seed-42 … seed-46/
    └── fixed-weight-mappo-laptop/seed-42 … seed-46/
```

## 9. What Ayesha needs to do

- Share this plan with Manish's Claude for verification (and the optional run C decision).
- During training (~30 min): laptop plugged in; it will be kept awake with `caffeinate` while the runs go.
