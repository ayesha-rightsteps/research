# 00 — Problem Formalization

The precise MDP for the implementation. **Proposed** — to be reviewed by the supervisor
(see `04_open_questions_for_supervisor.md`). Values marked *(calibrate)* are starting
points to tune in P1.

Grounded in the two closest papers:
- **DA-MAPPO** (Sheng et al. 2026) — per-step Hungarian assignment in the observation,
  MAPPO backbone. Source of our reward structure and hyperparameter starting points.
  Notes: `bin/91.../03_methodology.md`, `04_results.md`.
- **IGAT-MARL** (Rezaee et al. 2026) — sparse conflict-driven graph, DCPA/TCPA.
  Source of our conflict-graph construction and CPA-based safety term.
  Notes: `bin/9.../03_methodology.md`, `04_results.md`.

---

## 1. Framing: Dec-POMDP

Tuple `(N, S, {O_i}, {A_i}, P, R, γ)`:

| Symbol | Meaning |
|--------|---------|
| `N` | number of drones, `N ∈ {3, 5, 8}` in training; `= M` (one target each). Progression rationale: 3 is the minimum for non-trivial multi-agent interaction and replicates the DA-MAPPO baseline regime; 5 makes the conflict graph dense enough that PAH arbitration becomes meaningful; 8 is a stress test for scalability and generalization (tested on unseen swarm sizes in Stage 4). |
| `S` | global state (all drone poses/velocities, all target positions, all obstacle positions) — used by the **centralized critic** only |
| `O_i` | drone `i`'s local observation (Section 4) — used by the **decentralized actor** |
| `A_i` | drone `i`'s action: a 2D velocity command (Section 5) |
| `P` | deterministic point-mass kinematics + collision resolution (Section 6) |
| `R` | per-agent reward, `r_i = α_i · r_mission,i + (1 − α_i) · r_safety,i` (Section 7) |
| `γ` | 0.99 (from DA-MAPPO) |

Centralized training, decentralized execution (CTDE), standard for MAPPO.

---

## 2. World and assumptions

- **2D continuous** workspace, `world_size × world_size` (500 × 500 metres; 1 unit = 1 m).
- **Point-mass kinematics**, fixed timestep `dt` (*calibrate*: 0.1 s). No attitude, no
  aerodynamics. This is the deliberate simplification vs DA-MAPPO's Gazebo rigid-body
  model — justified because the research question (learned vs fixed α) does not depend
  on flight dynamics fidelity. **Needs supervisor sign-off** (synopsis says PyBullet).
- `N` drones, `N` targets (one-to-one), `K` static obstacles (circles).
- Targets: static in Stage 1; **position-swap** dynamics in Stage 2+ (DA-MAPPO style —
  targets periodically exchange positions), *not* continuous drift, unless the
  supervisor prefers drift. See `04`.
- Homogeneous drones (same speed limit, same radius).

### 2.1 Physical scale — unit mapping

**1 simulation unit = 1 metre.**

| Quantity | Sim value | Physical meaning | Justification |
|----------|-----------|-----------------|---------------|
| `world_size` | 500 u | 500 m × 500 m | Half-kilometre operational area — realistic small-UAV mission scale (campus, industrial site, search-and-rescue zone) |
| `v_max` | 5 u/s | 5 m/s | Conservative cruise speed for a small multirotor (e.g. DJI Mini class) in a constrained urban area |
| `d_col` | 2 u | 2 m | Separation threshold — roughly 2 × typical small-drone radius |
| `d_safe` | 3 u | 3 m | ≈ stopping distance at v_max with moderate deceleration |
| `arrival_radius` | 5 u | 5 m | Target acquired when drone centre within 5 m of target — realistic GPS accuracy margin |
| `dt` | 0.1 s | 100 ms control loop | Standard autopilot update rate |
| `T_max` | 300 steps | 30 s per episode | Enough for a drone at v_max to cross the workspace ~1.5 times |

This scale is deliberately small relative to real UAV operations (which can span
kilometres). The choice is justified because: (a) the research question is about the
PAH weighting mechanism, not range or endurance; (b) a 100 m arena allows thousands of
training episodes in minutes on a T4 GPU; (c) the relative ratios (speed / world size /
collision radius) match DA-MAPPO's normalised regime, making our results directly
comparable. A note will be added to the thesis "Scope and Assumptions" section.

### 2.2 Obstacle placement — Poisson disk sampling

Obstacles are placed using **Poisson disk sampling** with a minimum separation
`r_obs_min = 2 × d_safe = 6 m` between any two obstacle centres. The algorithm:

1. Place the first obstacle uniformly at random (with `margin = 10 m` from every edge).
2. For each subsequent obstacle, sample a candidate uniformly at random. Accept it only
   if it is at least `r_obs_min` from every already-placed obstacle **and** at least
   `d_safe` from every drone start position and target.
3. Reject and resample up to `max_tries = 1000` times; if no valid position is found,
   reduce `K` silently for that episode.

**Why Poisson disk, not pure uniform random?**
Pure uniform placement can accidentally cluster obstacles into an impassable wall or
place them on top of drone start positions. Poisson disk guarantees navigable corridors
of width ≥ `r_obs_min` — a physically meaningful constraint. This is the standard
method in robotics path-planning literature (Bridson 2007).

> Implementation note: `_random_layout()` in `multi_uav_env.py` currently uses
> rejection sampling with per-entity minimum distance checks. This must be updated to
> enforce the **inter-obstacle** minimum distance `r_obs_min` explicitly (current code
> only enforces separation from drones/targets). See next-steps in `sessions/`.

---

## 2.3 CTDE deployment model

The system follows **Centralized Training, Decentralized Execution (CTDE)** —
the standard paradigm for cooperative MARL (Lowe et al. 2017, Yu et al. 2022).

### During training (offline / ground station)

| Component | Where it runs | What it sees |
|-----------|--------------|--------------|
| **Centralized critic** | Ground station / training server (Kaggle T4 or local M3) | Full global state `S` = all N drones' observations concatenated |
| **Actor (N copies, shared weights)** | Also on training server | Each drone's local observation `O_i` only |
| **PAH** | Also on training server, jointly trained with actor | `τ_collision`, `d_target`, `n_conflict` per drone |

The ground station collects observations from all drones at each timestep, feeds them
to the critic, computes the centralized value estimate and GAE advantages, then updates
all networks. **This requires a reliable communication channel** — assumed clear and
zero-latency during training (an offline or lab-testing setup, not a live mission).

### During deployment (online / in-flight)

| Component | Where it runs | What it needs |
|-----------|--------------|---------------|
| **Actor** | Onboard each drone (companion computer or flight controller) | Only its own `O_i` — 10 numbers |
| **PAH** | Onboard each drone (runs with actor) | Only its own `τ_collision`, `d_target`, `n_conflict` |
| **Centralized critic** | **NOT deployed** — not needed at execution time | — |

Each drone computes its own action independently. The actor has only ~5,000 parameters
(< 20 kB) — deployable on any ARM Cortex-M class processor.

**Communication assumption for deployment:** Each drone needs only its own local sensor
data. No inter-drone communication is required at execution time. The conflict graph
inputs (`τ_collision`, `n_conflict`) can be computed locally using onboard proximity
sensors (ultrasonic / LiDAR) or via a lightweight broadcast of positions only (< 10
bytes per drone per timestep). We assume a clear channel for this broadcast — no packet
loss or delay model in the current scope.

> This is a standard CTDE assumption shared by MAPPO, MADDPG, and QMIX. The thesis
> "Scope and Assumptions" section will state this explicitly.

---

## 3. Global state `S` (critic input)

Concatenation of:
- every drone: position `(x, y)`, velocity `(vx, vy)` → `4N`
- every target: position `(x, y)` → `2N`
- every obstacle: position `(x, y)`, radius `r` → `3K`

Total `= 6N + 3K`. Normalized (positions / world_size, velocities / v_max).

---

## 4. Observation `O_i` (actor input)

Per drone `i`, following DA-MAPPO's four-component design but simplified:

| Component | Fields | Dim | Notes |
|-----------|--------|-----|-------|
| Ego state | `x/W, y/W, vx/vmax, vy/vmax` | 4 | own position + velocity, normalized |
| Assigned target | `Δx/W, Δy/W, d_target/W` | 3 | relative position + distance to Hungarian-assigned target |
| Conflict neighbors | for each of `K_nbr` slots: `Δx, Δy, Δvx, Δvy` (relative), `+ mask bit` | `5·K_nbr` | the conflict-graph neighbors, **sorted by time-to-collision ascending**, zero-padded, masked. *Proposed `K_nbr = 4`.* |
| Obstacle proximity | clearance in 4 cardinal directions (N/E/S/W), normalized, clipped | 4 | simplified stand-in for DA-MAPPO's 35-beam LiDAR — **needs sign-off** |

**Total (K_nbr = 4):** `4 + 3 + 20 + 4 = 31`.

Design decision — **fixed-K padding + mask** for the variable neighbor count (an MLP
needs fixed input width). Alternative: a permutation-invariant encoder (mean/max pool)
or a graph-attention encoder (as IGAT does). We start with padding+mask for simplicity;
the graph-attention encoder is available for the IGAT-style baseline (B3). See
`02_assignment_and_conflict.md`.

---

## 5. Action `A_i`

2D continuous velocity command `a_i = (ux, uy) ∈ [−1, 1]²`, scaled to `v_max`
(*calibrate*: 5 units/s).

- We use `(ux, uy)` rather than DA-MAPPO's `(forward speed, yaw rate)` because there is
  no heading state in a point-mass model — simpler and sufficient for 2D. **Sign-off.**
- Kinematics: `v_{t+1} = clip(a·v_max, |v| ≤ v_max)`, `p_{t+1} = p_t + v_{t+1}·dt`.
- Optionally an acceleration limit for smoothness (DA-MAPPO penalizes jerk) — add later
  if trajectories look unrealistic.

---

## 6. Transition `P`

Each step:
1. Recompute Hungarian assignment (see `02`).
2. Recompute conflict graph (see `02`).
3. Apply actions → update velocities and positions.
4. Resolve collisions / termination checks.

**Episode ends when:**
| Outcome | Condition |
|---------|-----------|
| SUCCESS | all drones within `arrival_radius` of their assigned target |
| COLLISION | any pair closer than `d_col`, or any drone touches an obstacle |
| BOUNDARY | any drone leaves the workspace |
| TIMEOUT | `t > T_max` (*calibrate*: 600 steps, from DA-MAPPO) |

---

## 7. Reward

Per-agent: `r_i = α_i · r_mission,i + (1 − α_i) · r_safety,i`, where `α_i` is the PAH
output for drone `i` (or a fixed constant for baselines B1–B4). Overall reward scaled
by a constant (DA-MAPPO divides by 50) to keep magnitudes reasonable.

### 7.1 Mission term `r_mission,i` (adapted from DA-MAPPO tiers 1, 2, 4)

| Sub-term | Formula (per step) | Purpose | Start value |
|----------|-------------------|---------|-------------|
| Progress | `κ_prog · (d_prev − d_curr)` | reward closing distance to assigned target | `κ_prog` *(calibrate)* |
| Arrival bonus | `b_k` on first entering the target zone; `b_k` decreases with arrival order | reward finishing, discourage free-riding | from DA-MAPPO |
| Hover | `+1` while inside target zone; `−10` if it drifts back out | hold position once arrived | DA-MAPPO |
| Step penalty | `−1` per step | time pressure | DA-MAPPO |
| (optional) team term | `−ω_team · Σ_j d_j` | collective progress | DA-MAPPO tier 1 — add if needed |

### 7.2 Safety term `r_safety,i` (adapted from DA-MAPPO tier 3 + IGAT CPA term)

| Sub-term | Formula | Purpose | Start value |
|----------|---------|---------|-------------|
| Inter-drone hard penalty | `−100` if any pair distance `< d_col` | hard collision | DA-MAPPO |
| Obstacle graded penalty | `−100` if clearance `< d_safe`; `−25` in `[d_safe, 2 d_safe]`; `−10` in `[2 d_safe, 3 d_safe]` | graded obstacle risk | DA-MAPPO |
| Continuous proximity risk (CPA) | `−(1 − exp(1 − 1/√max(x, ε)))`, `x = DCPA_ij / d_danger` | smooth gradient *before* a collision happens | IGAT eq. in `bin/9.../03` |
| Boundary penalty | `−100` outside; decreasing near the edge | keep in bounds | DA-MAPPO |
| (optional) smoothness | `−0.5·|Δv| − 0.2·|Δω|` analogue | discourage jerky motion | DA-MAPPO tier 4 |

**Note on the split:** for the α-weighting to be meaningful, `r_mission` must contain
*only* task-progress terms and `r_safety` *only* safety terms. Terms like the step
penalty are mission-side. This clean separation is what lets α trade the two off.

---

## 8. Parameter table (proposed starting values)

| Param | Symbol | Start | Source / note |
|-------|--------|-------|---------------|
| World size | `W` | 500 | 500 m × 500 m; 1 unit = 1 metre |
| Timestep | `dt` | 0.1 s | calibrate |
| Max speed | `v_max` | 5 u/s | calibrate |
| Inter-drone collision distance | `d_col` | 2 u | ~ 2× drone radius |
| Obstacle safety distance | `d_safe` | 3 u | DA-MAPPO: `v_max·dt + v_max²/(2 a_max)` (stopping distance) |
| Arrival radius | — | 3 u | calibrate |
| Episode limit | `T_max` | 600 | DA-MAPPO |
| Conflict look-ahead horizon | `H` | 3 s | calibrate; IGAT uses a look-ahead window |
| Danger threshold (graph edge + CPA scale) | `d_danger` | 3·`d_col` | calibrate |
| Neighbor slots in obs | `K_nbr` | 4 | calibrate |
| Discount | `γ` | 0.99 | DA-MAPPO |

---

## 9. What we deliberately drop vs DA-MAPPO / IGAT (and why it's OK)

| Dropped | Why acceptable |
|---------|----------------|
| 3D physics / PyBullet / Gazebo | research question is about α, not dynamics fidelity; synopsis scope is 2D |
| 35-beam LiDAR | 4 cardinal clearances are enough for sparse circular obstacles in 2D |
| Communication model (packet loss, delay) | out of synopsis scope; can be a "future work" line |
| Kalman-filtered acceleration estimates | point-mass model gives exact velocity |
| Fixed-wing BADA dynamics (IGAT) | our drones are holonomic point masses; simpler and matches DA-MAPPO's regime |

All of these are stated explicitly in the thesis "scope and assumptions" section so
they cannot surface as surprises at the defense.
