| Method | Environment (N, obstacles) | R_success (%) | R_collision (%) | Source |
|---|---|---|---|---|
| IPPO | N=3, 30 | 78 | 22 | DA-MAPPO Table V (ENV-1) |
| MAPPO | N=3, 30 | 83 | 17 | DA-MAPPO Table V (ENV-1) |
| RMAPPO | N=3, 30 | 85 | 15 | DA-MAPPO Table V (ENV-1) |
| NavRL | N=3, 30 | 63 | 34 | DA-MAPPO Table V (ENV-1) |
| EGO-Planner v2 | N=3, 30 | 53 | 45 | DA-MAPPO Table V (ENV-1) |
| **DA-MAPPO** | N=3, 30-50 | **90-99** | 1-10 | DA-MAPPO Table V (ENV-1-3) |
| **Ours — M (Stage 2)** | N=5, 5 | **89.5** | 10.5 | this work, 5 seeds, 200 ep det. |
| **Ours — M (Stage 3)** | N=8, 10 | **72.0** | 28.0 | this work, seed 42, 200 ep det. |
