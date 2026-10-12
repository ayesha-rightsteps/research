## Success, Stage 2 (deterministic, 200 episodes, mean ± std over 5 seeds)

| Run                                  | Success %   | Collision %   |   Timeout % |   T_ave | % collisions with obstacles   | Loss-of-separation / episode   |
|:-------------------------------------|:------------|:--------------|------------:|--------:|:------------------------------|:-------------------------------|
| Fixed-weight MAPPO (laptop)          | 88.2 ± 2.2  | 11.8 ± 2.2    |           0 |    48.8 | 99                            | 0.140                          |
| Plain MAPPO                          | 89.9 ± 1.4  | 10.1 ± 1.4    |           0 |    49.2 | 96                            | 0.157                          |
| Plain MAPPO, α = 0.9 reward          | 89.4 ± 1.9  | 10.6 ± 1.9    |           0 |    48.7 | 94                            | 0.141                          |
| Fixed-weight MAPPO (Kaggle, v3)      | 89.2 ± 2.0  | 10.8 ± 2.0    |           0 |    49.1 | —                             | —                              |
| Hand-coded τ-rule MAPPO (Kaggle, v3) | 87.5 ± 1.5  | 12.5 ± 1.5    |           0 |    49.1 | —                             | —                              |
| MAPPO + PAH (Kaggle, v3)             | 89.5 ± 1.0  | 10.5 ± 1.0    |           0 |    49.4 | —                             | —                              |

## Comparison (reading rule from PLAN.md)

| Comparison                                                |   Difference (points) | 95% CI        |   Welch p | Reading      |
|:----------------------------------------------------------|----------------------:|:--------------|----------:|:-------------|
| Plain MAPPO − Fixed-weight MAPPO (laptop)                 |                   1.7 | [-1.07, 4.47] |     0.188 | INCONCLUSIVE |
| Plain MAPPO, α = 0.9 reward − Fixed-weight MAPPO (laptop) |                   1.2 | [-1.82, 4.22] |     0.385 | INCONCLUSIVE |

Wall time per full run (8 in parallel on the laptop): 11.0–12.3 min, median 12.1.
