# v4 mechanism check — advantage correlation (report)

Run 2026-10-17, `advantage_check.py` (80 final models: 4 two-head methods × 2 stages × 10 seeds; 10 training-style
batches of 512 steps each; no training; 1.5 min). Table: `output/advantage_summary.md`; per batch:
`output/advantage_per_batch.csv`. Planned in `02-redesign/PLAN.md` Section 5 ("is the actor signal still ~plain
MAPPO? it should not be"), same check as Phase 0 on the v3 models. Gate: Fixed-weight MAPPO's signal equals the
α = 0.5 signal (cosine 1.00, both stages) — passed. A second full run gave identical numbers.

| Stage | Method | corr(A_mission, A_safety) | corr(actor signal, Plain MAPPO signal) | Opposite sign to Plain MAPPO: all / safety-reward steps / other steps (%) | Success (main results) |
|---|---|---|---|---|---|
| 2 | Fixed-weight MAPPO | 0.28 | 0.92 | 7.6 / 16.9 / 7.1 | 79.9 |
| 2 | Hand-coded τ-rule MAPPO | 0.19 | 0.98 | 4.4 / 11.4 / 3.9 | 84.8 |
| 2 | MAPPO + PAH | 0.18 | 0.98 | 2.5 / 5.8 / 2.3 | 86.8 |
| 2 | MAPPO + PAH (Hungarian off) | 0.16 | 0.98 | 3.0 / 5.8 / 2.7 | 83.5 |
| 3 | Fixed-weight MAPPO | 0.19 | 0.92 | 8.7 / 14.1 / 8.2 | 74.2 |
| 3 | Hand-coded τ-rule MAPPO | 0.15 | 0.94 | 8.5 / 12.7 / 7.7 | 71.5 |
| 3 | MAPPO + PAH | 0.14 | 0.98 | 3.7 / 5.2 / 3.5 | 82.7 |
| 3 | MAPPO + PAH (Hungarian off) | 0.13 | 0.99 | 2.6 / 3.6 / 2.5 | 68.4 |

(Plain MAPPO success for reference: S2 68.9, S3 44.2. CIs in `output/advantage_summary.md`; all ≤ 0.06.)

## What it shows

1. **The two value heads carry different information.** Mission and safety advantages are only weakly correlated
   (0.13–0.28). Two heads are not a copy of one head.
2. **The actor signal of every two-head method stays close to Plain MAPPO's signal** (correlation 0.92–0.99; Phase 0
   on v3: 0.95–1.00). The planned expectation "it should not be ~plain MAPPO" is **not met**: the signals differ only
   on a small share of samples (2.5–8.7% get the opposite sign), more often on steps with a safety reward.
3. **Closeness to Plain MAPPO's signal does not track success.** MAPPO + PAH's signal is *closer* to Plain MAPPO's
   (0.98) than Fixed-weight MAPPO's is (0.92), yet MAPPO + PAH beats Fixed-weight MAPPO (+8.6, Stage 3) and Plain
   MAPPO (+38.5). So this check does not explain where the gains come from.

## How to use it in the thesis

- Report it as a mechanism check whose answer is "not explained by a large change in the actor's learning signal".
- Do not claim that PAH works by reshaping the actor's advantage. The data do not support that.
- The two-heads step (Plain MAPPO → Fixed-weight MAPPO, +30.0) also changes how the critic learns (two value
  targets instead of one). That route is not measured here; it is a possible explanation, not a result.
- Limits: final models only; 10 batches per model; signal similarity is measured on the model's own rollouts.
