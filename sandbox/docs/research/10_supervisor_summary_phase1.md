# Progress summary and decisions needed — October 2026

**Thesis:** Multi-Agent PPO for Joint Dynamic Target Assignment and Collision Avoidance in UAV Systems
**Student:** Ayesha Khalil · **Prepared:** 12 October 2026

## 1. Where the results stand

| Setting | Fixed-weight MAPPO (α = 0.5) | Hand-coded τ-rule MAPPO | MAPPO + PAH (proposed) |
|---|---|---|---|
| 5 drones, 5 obstacles (5 seeds) | 89.2% ± 2.0 | 87.5% ± 1.5 | 89.5% ± 1.0 |
| 8 drones, 10 obstacles (1 seed) | 73.5% | — | 72.0% |

Mission success, 200 evaluation episodes per model. Removing Hungarian target assignment drops success to
51.5% (8 drones) — the largest effect we measured. The PAH mechanism works as designed (α lower in danger,
higher when safe, correct direction in 586/586 checked states), but PAH does not improve success.

## 2. What the diagnostics found (no new training; analysis of the trained models)

1. **Failures are obstacle collisions.** 94–100% of collision episodes are a drone hitting an obstacle, not
   another drone.
2. **PAH cannot see obstacles.** Its danger input (time-to-collision) comes only from drone–drone conflicts.
3. **α barely changes the learning signal.** In the current design, every method's training signal is
   95–100% correlated with that of plain MAPPO. This is the most likely reason the three methods tie.
4. **Obstacle sensing is weak.** Drones see obstacles only through four axis-aligned distances; the base
   paper (DA-MAPPO) uses a 35-beam LiDAR.

## 3. Why our numbers are not directly comparable to DA-MAPPO

DA-MAPPO reports 90–99% with 3 drones and 30–50 obstacles; we use 5–8 drones and 5–10 point obstacles —
a different problem (and target assignment is only one part of ours). A fair comparison requires running the
base papers' methods and experiments in our environment, which has not been done yet.

## 4. Proposed changes — approval requested

| # | Change | Why | Effect on the thesis |
|---|---|---|---|
| 1 | Separate mission and safety value heads in the critic | So that α actually changes what the policy learns | Training-method change, PAH idea unchanged |
| 2 | Add obstacle danger to PAH's inputs | Obstacles are where failures happen | **Changes PAH's input set** (synopsis: τ, d_target, n_conflict) |
| 3 | LiDAR-like obstacle sensing | Matches the base paper; addresses the failure mode | Environment change |
| 4 | Physical (sized), denser obstacles | Matches the base paper's setting; creates real mission-vs-safety conflict | Environment change |

Then, in the new environment: our methods plus the base papers' methods (plain MAPPO, IPPO, a DA-MAPPO-style
method, an IGAT-style method), and their experiments (obstacle-density and swarm-size sweeps, their metrics).

## 5. Feasibility

Training now runs on a laptop CPU ~5× faster than on Kaggle (an 8-drone run takes ~11 minutes instead of
~64), so all retraining fits in about a day. Estimated total: **2–3 weeks**. Already in progress: a small
check that plain MAPPO matches the current results (confirms finding 3).

## 6. Questions for the supervisor

1. Are changes 1–4 acceptable — in particular change 2, which extends PAH's inputs beyond the synopsis?
2. Which base-paper baselines are required (plain MAPPO, IPPO, DA-MAPPO-style, IGAT-style)? For IGAT-MARL,
   is a MAPPO-based "IGAT-style" baseline acceptable, or is a faithful DQN reproduction expected?
3. Is it acceptable to report the current results as the first stage of the study (what we found and why we
   changed the design)?
