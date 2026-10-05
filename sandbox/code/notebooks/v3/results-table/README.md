# results-table — paper-style results (DA-MAPPO Table V format)

Built 2026-10-05 after the teacher asked for the comparison "in the style of
the base paper". DA-MAPPO (`bin/91`) reports results as tables (IV, V, VI)
and clean white-background bar charts. This folder produces both, from our
already-trained models. **Inference only: no training, no Kaggle, runs on a
laptop CPU in about 80 seconds.**

## Run it

Open `paper_style_results.ipynb` and run all cells from this folder (paths
are relative to it). Per-model results are cached in `output/raw/`, so a
re-run is instant; delete `output/raw/` to re-evaluate from scratch.

## Protocol

200 episodes per (method, training seed), deterministic policy (actor
mean), disjoint evaluation seed `7001`, identical episode layouts for every
method. Stage 2 is mean ± std over 5 training seeds; Stage 3 is one seed
with 95% Wilson intervals. Follows `docs/plans/02_experiment_protocol.md`.

## What is in `output/`

| File | Content |
|---|---|
| `table_stage2.md`, `table_stage3.md` | DA-MAPPO-style tables: R_success, R_collision, R_timeout, T_ave, L_ave |
| `per_seed_stage2.csv` | the same metrics for every Stage 2 training seed |
| `fig1_stage2_success_collision` | grouped bars, Stage 2, error bars = std over 5 seeds |
| `fig2_stage3_success_collision` | grouped bars, Stage 3, error bars = 95% CI |
| `fig3_stage2_time_path`, `fig4_stage3_time_path` | T_ave and L_ave |
| `fig5_effect_sizes` | α effect (Stage 2 and Stage 3) vs removing optimal assignment |
| `fig6_training_curves` | IGAT-MARL Fig. 3 style panels: success, collision and entropy over training, Stage 2 and Stage 3 (training-time eval, see caveat below) |
| `fig7_comparison_vs_literature` | our results next to DA-MAPPO's Table V (success + collision bars, per-bar config labels) |
| `fig8_comparison_curves` | fig6-style: our success-rate training curves with the papers' reported levels as horizontal reference bands |
| `fig9_pah_alpha_behavior` | PAH's mechanism: α in danger vs when safe, Stage 2 and Stage 3 (0/586 wrong direction) |
| `fig9b_pah_response_curve` | the learned α as a continuous function of time-to-collision (sweep through the head) |
| `fig10_generalization` | M vs B4, in-distribution vs harder out-of-distribution (held-out seeds) |
| `table_comparison.md` | the same comparison as a table, with an Environment column |
| `raw/` | every episode of every model (outcome, steps, path length) |

Figures are saved as `.png` (for documents) and `.svg` (vector).

## Results

Stage 2 (5 drones, 5 obstacles), mean ± std over 5 seeds:

| Method | R_success (%) | R_collision (%) |
|---|---|---|
| B4 (fixed α) | 89.2 ± 2.0 | 10.8 ± 2.0 |
| H (τ-formula) | 87.5 ± 1.5 | 12.5 ± 1.5 |
| M (PAH residual) | 89.5 ± 1.0 | 10.5 ± 1.0 |

Stage 3 (8 drones, 10 obstacles), seed 42:

| Method | R_success (%) | R_collision (%) |
|---|---|---|
| B4 (fixed α) | 73.5 [67.0, 79.1] | 26.5 |
| M (PAH residual) | 72.0 [65.4, 77.8] | 28.0 |
| M, no Hungarian | 51.5 [44.6, 58.3] | 48.5 |

## Read these before citing the numbers

- **M vs B4 is a tie** at both stages (Stage 2: +0.3 pts, Welch p = 0.78; Stage 3: intervals overlap).
- **M vs H at Stage 2 is +2.0 pts, p = 0.039.** That is uncorrected for three pairwise comparisons and
  would not survive a Bonferroni correction (0.05/3 = 0.017). Treat it as a hint, not a finding.
- **Removing optimal assignment costs 20.5 pts at Stage 3** and nearly doubles the path length of the
  episodes that still succeed (L_ave 151 → 276). Single seed; the intervals do not overlap.
- **These numbers differ from the training logs.** Training-time evaluation sampled stochastic actions on
  20-episode batches. Here the policy is deterministic on 200 episodes. Do not mix the two in one table.
- **`fig6_training_curves` uses the training-time evaluation** (stochastic actions, 20 episodes per
  checkpoint, 5-checkpoint moving average), not the deterministic 200-episode protocol, so its levels
  differ from the tables. Use it for curve shape only. Stage 2 curves overlap; at Stage 3 the
  no-Hungarian run is lower from the start. Entropy is not quality: the ablation has the lowest
  entropy at Stage 3 and the worst outcomes.
- `L_ave` is the per-drone mean path length over successful episodes; DA-MAPPO's write-up says "total by
  all UAVs", and our world units and drone counts differ from theirs. Compare our methods with each other,
  not with the paper's `T_ave`/`L_ave`.
- The ablation here (target stays in the observation, optimal assignment replaced by a fixed pairing) is
  **not** the same manipulation as DA-MAPPO's Table VI (target removed from the observation).
- **`fig7_comparison_vs_literature` is a context comparison, not head-to-head.** DA-MAPPO runs N=3 drones /
  30–50 obstacles; ours is N=5–8 / 5–10. More drones vs fewer obstacles pull difficulty in opposite
  directions, so the raw success bars cannot be ranked directly — the per-bar config labels and the title
  say so. It shows our Stage 2 sits inside DA-MAPPO's reported band (a pipeline sanity check), nothing more.
- **`fig8_comparison_curves` cannot show DA-MAPPO's learning curve** — the paper gives only final numbers,
  so their result is drawn as a horizontal reference band, not a curve. Our curves there are the
  training-time stochastic eval (same as fig6), so their levels are approximate; the bands are the papers'
  final numbers at a different scale. Orientation only.
- **`fig9_pah_alpha_behavior`** is PAH's real contribution: the mechanism adapts α correctly (safety-first
  in danger, mission-first when safe), 0/586 wrong direction. This is separate from the outcome, where M
  ties B4 — do not let the figure imply M beats B4 on success. Its danger-state values come from
  training-time logging (eval_alpha_low_tau); at eval the converged policy rarely enters danger.
- **`fig9b_pah_response_curve`** is a synthetic sweep of the trained head (not real eval states, which
  cluster at τ=max because the policy avoids danger). It shows the learned function: α rises smoothly with
  τ, the learned head is slightly more safety-conservative than the α_safe prior, and conflict count barely
  moves it (τ dominates). Label it as a response curve, not a measurement of visited states.
- **`fig10_generalization`** is a single training run (100-episode deterministic eval on held-out seeds).
  M's edge (−12 vs −14 pts under shift) is a trend, not a win; the gap is small and unreplicated.
- Still open: Stage 3 has one seed, and the Stage 2 Hungarian ablation has not been run.

## Models evaluated

Stage 2, seeds 42–46: B4 from `stage2/stage2-pah-v0/fixed-alpha/` (seed 42 is the base notebook's
`output/`, seeds 43–46 their own `seed-N/output/`), H from `stage2/stage2-pah-v3-pah-change/h-baseline/`,
M from `stage2/stage2-pah-v3-pah-change/var-alpha/`. Stage 3, seed 42: `stage3/fixed-alpha/`,
`stage3/var-alpha/`, `stage3/ablation-hungarian/`. Duplicate output folders were checked and are
byte-identical (md5), so the choice between them does not matter.
