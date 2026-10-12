# v4 / 00-diagnostics — what the v3 models actually do

**Status: done (2026-10-12).** Read-only: nothing trained, no v3 file written.
Run `diagnostics.ipynb` from this folder (CPU, ~4 min the first time; results are cached in `output/`).

## Why

The 2026-10-12 discussion (`sessions/2026-10-12.md`, Sections 9–11) raised four questions that decide
what v4 should change. They are answered here from the models v3 already trained.

| # | Question |
|---|---|
| D1 | Are the collisions drone–drone or drone–obstacle? |
| D2 | During training, how often was the safety reward switched on? |
| D3 | How much does α actually move? |
| D4 | Loss-of-separation and active conflict edges (IGAT-MARL's metrics) |

## How

- **Code:** `../common/v3_env.py` (one frozen copy of the v3 env + networks, extracted programmatically from
  the v3 notebooks), `../common/v3_registry.py` (all 18 v3 models), `diag.py` (instrumented rollout).
- **Gate (Cell 2):** before anything else, the frozen copy must reproduce v3's evaluation episode-by-episode.
  It does: 200/200 identical episodes for Stage 3 M and Stage 2 B4 (seed 43); 5 models checked during
  development, all 200/200.
- **Evaluation pass (D1, D4):** all 18 final models, deterministic policy, 200 episodes, env seed 7001 —
  same protocol and episode layouts as `v3/results-table`.
- **Training-conditions pass (D2, D3):** every saved checkpoint (~every 500 episodes) of the six seed-42
  runs, **stochastic** policy (sampled actions, as in the training rollout), 50 episodes per checkpoint,
  env seed 9101.
- **Definitions:** danger radius = 3 × collision radius = **9 units** (the radius the v3 reward uses for
  `r_safety` and the conflict graph uses for an edge). Loss-of-separation (LoS) = a drone pair closer than
  9 units at a step. Active edges = conflict-graph edges per step.

## Results

### D1 — What did the drones hit? (`output/d1_collision_kinds.png`)

| Stage | Method | Collision episodes | Drone–obstacle | Drone–drone | % obstacle | % near goal |
|---|---|---|---|---|---|---|
| 2 (1000 ep) | B4 | 108 | 107 | 1 | 99.1 | 20.4 |
| 2 (1000 ep) | H | 125 | 124 | 1 | 99.2 | 20.8 |
| 2 (1000 ep) | M | 105 | 104 | 1 | 99.0 | 21.9 |
| 3 (200 ep) | B4 | 53 | 50 | 3 | 94.3 | 30.2 |
| 3 (200 ep) | M | 56 | 56 | 0 | 100.0 | 39.3 |
| 3 (200 ep) | M, no Hungarian | 97 | 78 | 19 | 80.4 | 19.6 |

**Almost every failure is a drone hitting an obstacle.** Drone–drone collisions are rare whenever
Hungarian assignment is on; they only become common (19 of 97) when it is removed. Most collisions happen
on the way, not at the goal.

### D2 — How often is there anything to arbitrate? (`output/d2_safety_active.png`)

Share of drone-steps, across training checkpoints (stochastic policy):

| Run | Safety reward ON | of which: another drone within 9 | of which: obstacle within 9 | Conflict graph flags a conflict |
|---|---|---|---|---|
| Stage 2, B4 / H / M | 0.19 – 0.62 % | 0.00 – 0.03 % (final) | 0.30 – 0.49 % (final) | ~0.02 – 0.10 % |
| Stage 3, B4 | 0.81 – 1.31 % | 0.41 % (final) | 0.86 % (final) | ~0.07 – 0.26 % |
| Stage 3, M | 0.85 – 1.26 % | 0.10 % (final) | 0.97 % (final) | ~0.05 – 0.40 % |
| Stage 3, M, no Hungarian | 1.20 – 1.71 % | 0.61 % (final) | 0.74 % (final) | ~0.90 – 1.16 % |

**The safety reward is on in roughly 1 drone-step in 60 to 1 in 500 (0.19–1.71%), and mostly because of
obstacles.** The
conflict graph — the only source of PAH's τ input — flags a conflict in roughly 1 drone-step in 250 to
1 in 5000. (α weights advantages, and GAE spreads the safety advantage a few steps back, so these are
lower bounds on how often α can matter — but they are small.)

### D3 — How much does α actually move? (`output/d3_alpha_spread.png`)

Final checkpoint, all drone-steps (stochastic policy):

| Method | α 10th pct | α median | α 90th pct | % steps α < 0.5 | % steps α < 0.8 |
|---|---|---|---|---|---|
| B4 | 0.50 | 0.50 | 0.50 | — | — (always 0.5) |
| H, Stage 2 | 0.90 | 0.90 | 0.90 | 0.00 | 0.02 |
| M, Stage 2 | 0.74 | 0.89 | 0.90 | 0.00 | 13.1 |
| M, Stage 3 | 0.70 | 0.87 | 0.90 | 0.03 | 26.2 |
| M, no Hungarian, Stage 3 | 0.70 | 0.90 | 0.90 | 0.70 | 17.8 |

Checked separately (final M models, 50 stochastic episodes): with no conflict (99.9% of drone-steps), α
still ranges 0.70–0.90, and it tracks **distance to the target**, not danger — correlation(α, d_target)
= −0.73 at Stage 2 and −0.92 at Stage 3 (median α ≈ 0.89 within 50 units of the target, ≈ 0.70 beyond
150–300 units).

**In practice the three "α sources" behave like three near-constant weightings:** B4 = 0.5 always,
H ≈ 0.9 always (τ is almost always at its maximum), M ≈ 0.7–0.9 set mainly by target distance. α almost
never drops below B4's 0.5.

### D4 — IGAT-MARL metrics on our models (`output/d4_los_edges.png`)

| Stage | Method | LoS pair-steps per episode | Active edges per step |
|---|---|---|---|
| 2 | B4 | 0.098 ± 0.038 | 0.002 |
| 2 | H | 0.064 ± 0.030 | 0.001 |
| 2 | M | 0.100 ± 0.049 | 0.001 |
| 3 | B4 | 0.215 ± 0.166 | 0.004 |
| 3 | M | 0.185 ± 0.163 | 0.003 |
| 3 | M, no Hungarian | 0.870 ± 0.243 | 0.051 |

Stage 2: mean ± std over 5 seeds. Stage 3: mean ± 95% CI over 200 episodes.
**Drone–drone near-misses are rare** (well under one pair-step per episode). M and B4 do not differ
(intervals overlap). Removing Hungarian raises near-misses ~4.7× and active edges ~15× — assignment is what
keeps drones apart.

## What this means (interpretation — for discussion, nothing decided)

1. **The failures are obstacles; PAH cannot see obstacles.** PAH's τ input comes only from the drone–drone
   conflict graph (`ConflictGraph.update` uses drone positions and velocities only). The dangers that end
   episodes — obstacles — never reach PAH. This is a fact of the code, confirmed by D1.
2. **There is very little for PAH to arbitrate.** The safety reward is on ~1% of the time, drone–drone
   conflicts far less. With α mostly set by target distance and almost never below 0.5, PAH, H and B4 end up
   as three nearly fixed weightings — which is consistent with their tie on success. This strongly supports
   the hypothesis from Section 9.5 (a); it does not prove causation.
3. **Obstacle sensing is the likely bottleneck for success itself.** The obstacle feature is four
   axis-projected clearances (a stand-in for DA-MAPPO's 35-beam LiDAR), and obstacles are where drones fail.
4. **Hungarian assignment keeps drones apart** — consistent with the 20.5-point success drop without it.

Possible v4 directions these numbers point to (Ayesha, Manish and the supervisor decide):
- give PAH the danger that actually matters (obstacle proximity / time-to-collision as an input);
- better obstacle sensing (LiDAR-like rays, as in the base paper);
- a setting with real mission-vs-safety conflict (denser drones, crossing targets) so arbitration has
  something to do — and so the base-paper experiments (density / swarm-size sweeps) are meaningful.

## Caveats

- Training-conditions pass and all Stage 3 numbers: one seed (42). 50 episodes per checkpoint, so the D2
  curves are noisy point to point; the level (≈1% or less) is the finding, not the wiggles.
- Collision kind is read on the step the episode ended; `both` never occurred.
- "Near goal" = a drone involved was within the target radius (25 units) of its assigned target.

## Files

| File | What |
|---|---|
| `diagnostics.ipynb` | the notebook (8 cells; Cell 2 is the gate) |
| `diag.py` | instrumented rollout (`run_episode`) and α per method |
| `output/eval_episodes.csv` | one row per evaluation episode (3600) |
| `output/training_conditions.csv` | one row per checkpoint (95) |
| `output/tables.md`, `output/summary.json` | the tables above, machine-generated |
| `output/d1_…d4_*.png/.svg` | figures |
