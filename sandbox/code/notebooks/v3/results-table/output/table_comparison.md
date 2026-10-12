| Method | Environment (N drones, obstacles) | R_success (%) | R_collision (%) | R_timeout (%) | Source |
|---|---|---|---|---|---|
| IPPO | N=3, 30 / 40 / 50 | 78 / 57 / 53 | 22 / 43 / 47 | 0 / 0 / 0 | DA-MAPPO Table V (ENV-1 / 2 / 3) |
| RMAPPO | N=3, 30 / 40 / 50 | 85 / 69 / 67 | 15 / 31 / 33 | 0 / 0 / 0 | DA-MAPPO Table V (ENV-1 / 2 / 3) |
| MAPPO | N=3, 30 / 40 / 50 | 83 / 70 / 64 | 17 / 30 / 36 | 0 / 0 / 0 | DA-MAPPO Table V (ENV-1 / 2 / 3) |
| NavRL | N=3, 30 / 40 / 50 | 63 / 53 / 32 | 34 / 43 / 65 | 3 / 4 / 3 | DA-MAPPO Table V (ENV-1 / 2 / 3) |
| EGO-Planner v2 | N=3, 30 / 40 / 50 | 53 / 51 / 43 | 45 / 48 / 57 | 2 / 1 / 0 | DA-MAPPO Table V (ENV-1 / 2 / 3) |
| **DA-MAPPO** | N=3, 30 / 40 / 50 | **99 / 95 / 90** | 1 / 5 / 10 | 0 / 0 / 0 | DA-MAPPO Table V (ENV-1 / 2 / 3) |
| B4 (fixed α) | N=5, 5 / N=8, 10 | 89.2 / 73.5 | 10.8 / 26.5 | 0 / 0 | this work (Stage 2, 5 seeds / Stage 3, seed 42) |
| H (τ-formula) | N=5, 5 | 87.5 | 12.5 | 0 | this work (Stage 2, 5 seeds) |
| **M (PAH, ours)** | N=5, 5 / N=8, 10 | **89.5 / 72.0** | 10.5 / 28.0 | 0 / 0 | this work (Stage 2, 5 seeds / Stage 3, seed 42) |
| M, no Hungarian | N=8, 10 | 51.5 | 48.5 | 0 | this work (Stage 3, seed 42) |
