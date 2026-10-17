# v4 Phase 3 — the base papers' experiments on our trained models (plan)

Status: written 2026-10-17; code and gates done (186/186 byte-identical); **run started 2026-10-17 21:12** on Ayesha's
decision (`run_phase3.sh`).

## 1. Purpose

Phase 1b and Phase 2 answered "is MAPPO + PAH better, in one setting per stage?" Phase 3 repeats the **kinds of
experiments the base papers report**, so the thesis can say how the methods behave when the setting changes:
denser obstacles (DA-MAPPO ENV-1–3), static vs moving targets (DA-MAPPO), assignment every step vs every 50 steps
(DA-MAPPO ablation), swarm size 3–10 (IGAT-MARL), IGAT-MARL's metrics, sensor noise and computation time.

**No training.** Every experiment re-evaluates the 186 models that already exist under a changed test setting.
Nothing about PAH, the reward, the training environment or the hyperparameters changes (Manish's review §5:
"Phase 3 sirf base-paper ke experiments").

## 2. Fixed for every experiment

- Models: `02-redesign/runs/stage{2,3}/<method>/seed-42…51/final_model.pt` (5 methods) and
  `03-base-paper-baselines/runs/...` (4 base-paper methods). RMAPPO is excluded (it did not learn; REPORT.md note).
- 200 episodes per model per setting, deterministic actions, evaluation seed 7001 (same layouts as the main
  results wherever the setting allows).
- Each model keeps its own training configuration (read from its `config.json`); only the one test setting named
  by the experiment changes.
- Statistics as before: mean over 10 seeds, 95% CI; differences with a 95% Welch CI; one decimal, half up.

## 3. Reading rule (decided now, before any result)

Phase 3 has **no new primary claim**. Every comparison is secondary/exploratory and reported as it comes out,
including ones where MAPPO + PAH is not ahead. Main question to read: *does MAPPO + PAH's lead over Fixed-weight
MAPPO (and over the base-paper methods) hold when the test setting changes?* Read with the PLAN 02 §5 rule (CI
entirely above 0 = better, entirely below = worse, otherwise not settled); no multiple-testing correction, said so.
Test settings outside the training setting are generalisation tests: a drop for every method is expected and is
not a failure of the method.

## 4. Experiments

| # | Experiment (base paper) | Test setting changed | Methods | Evaluations |
|---|---|---|---|---|
| E1 | **Obstacle density** (DA-MAPPO ENV-1/2/3 = 30/40/50) | discs 10, 20, 30, 40, 50 at both stages (S2@10 and S3@20 already exist) | all 9 | 9 × 10 × 2 × 4 = 720 |
| E2 | **Static vs moving targets** (DA-MAPPO static and dynamic tables) | target speed 0 (trained at 1) | all 9 | 9 × 10 × 2 = 180 |
| E3 | **Assignment every step vs every 50 steps** (DA-MAPPO ablation) | re-assignment every 50 steps instead of every step | methods trained with every-step assignment: MAPPO + PAH, Fixed-weight, τ-rule, Plain MAPPO, DA-MAPPO (2D) | 5 × 10 × 2 = 100 |
| E4 | **Swarm size 3–10** (IGAT-MARL, N = 3…10) | drones 3, 4, …, 10 (Stage 3 models trained on 8; Stage 2 models trained on 5), each model with its own obstacle count | methods whose observation does not depend on the number of drones: MAPPO + PAH, Fixed-weight, τ-rule, Plain MAPPO, IGAT-style MAPPO | 5 × 10 × 2 × 8 = 800 |
| E5 | **IGAT-MARL metrics** | none: loss-of-separation per episode and active conflict-graph edges per step, recorded during E1–E4 and the main setting | all | (inside the others) |
| E6 | **Sensor noise** (robustness) | Gaussian noise on the LiDAR distances, σ = 0.02, 0.05, 0.10 of the ray range, Stage 3 | all 9 | 9 × 10 × 3 = 270 |
| E7 | **Computation time** | wall-clock time per decision step (all drones) for 3–10 drones, 1 process, 20 episodes | MAPPO + PAH, Fixed-weight, IGAT-style MAPPO (Stage 3 models) | 3 × 10 × 8 (20 episodes each) |
| — | **Learning curves** | already done (`03-base-paper-baselines/output/figures/fig5_learning_curves`) | — | 0 |

Known limits, to state in the thesis:
- **E4 excludes MAPPO, DA-MAPPO (2D) and IPPO**: they see all teammates, so their input size is fixed to the trained
  swarm size and they cannot run on another size without retraining. IGAT-MARL's own swarm test also uses a
  neighbour-based observation.
- **E3 is a test-time change**: the models were trained with every-step assignment. DA-MAPPO's ablation may have
  trained with the reduced frequency; if Manish or the supervisor want that, it needs training (one night) and is
  a separate decision.
- The density sweep tests trained-on-20 models up to 50 discs; DA-MAPPO trained with an obstacle curriculum.

## 5. Code changes needed (small; defaults must reproduce today's results exactly)

1. `common/env_v4.py`: assignment mode `'every-k'` with `assign_every=K` (Hungarian every K steps); LiDAR noise
   `lidar_noise=σ` (default 0). Defaults unchanged.
2. `common/mappo_v4.py`, `common/baselines_v4.py`: `get_actions(..., values=False)` skips the critic. Needed for E4:
   the critic's input is the whole team's observation, so it only fits the trained swarm size; the actor works on
   any number of drones. Default `values=True`, so training is untouched.
3. `02-redesign/evaluate.py`: test-setting options `--obstacles N`, `--target-speed v`, `--drones N`,
   `--assign-every K`, `--lidar-noise σ`, `--raw-dir NAME` (exists); extra recorded fields: loss-of-separation per
   episode, active edges per step, decision time.
4. `04-base-paper-experiments/run_phase3.sh` (all evaluations, 6 processes) and `summarize.py` + `figures.py`
   (tables and base-paper-style figures: success vs density, success vs swarm size, static vs moving, every step vs
   every 50, noise).

## 6. Gates (before the real run)

1. Unit tests: `every-k` with K = 1 gives the same episode as `every-step`; with K = 50 the assignment changes only
   at steps 0, 50, 100, …; noise σ = 0 gives identical observations; `values=False` gives the same actions as before.
2. All existing tests still pass (env 15, baselines 7, agent 7).
3. **Identity check:** re-evaluating all 186 models with the new code and default settings gives byte-identical
   JSON to `output/eval_raw/` (as on 2026-10-16).
4. Smoke run: each experiment on one model with 5 episodes, no errors; 50 discs and 10 drones place without
   "World too crowded".

## 7. Cost

Code + tests ~3–4 h. Laptop: about 2,100 model evaluations; at the measured rate (86 models in 6.5 min with 6
processes) about **3–4 hours**, longer for 10 drones and dense maps — one evening or night. Light-to-moderate CPU
(evaluation only). Then tables, figures and write-up ~half a day.

## 8. Not doing

- No training, no new seeds, no change to PAH, reward, environment defaults or hyperparameters.
- No RMAPPO (separate decision, see 2026-10-16 session §4 Q1).
- No retuning of any method for a new setting.
- Not mixing Phase 3 numbers with the main (Phase 1b/2) results in one table without labelling the setting.
