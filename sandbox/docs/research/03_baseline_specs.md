# 03 — Baseline Specifications

The four baselines and what each has switched on/off, plus the parameters extracted
from the two reference papers.

> **Verification status:** the parameter tables below are taken from the paper
> *handbooks* in `bin/` (secondary notes), not yet cross-checked against the PDFs
> page-by-page. Do that in P0 and add page references. PDFs:
> - DA-MAPPO: `bin/91.Dynamic Target Assignment.../Dynamic Target Assignment and Cooperative Decision-Making fo.pdf`
> - IGAT-MARL: `bin/9.Efficient multi-agent.../1-s2.0-S1568494626005934-main.pdf`

---

## 1. The comparison table

| ID | Method | Assignment aug (Hungarian in obs) | Conflict graph | α (mission vs safety) | Purpose |
|----|--------|:-:|:-:|---|---------|
| **B1** | Standard MAPPO | ✗ | ✗ | single reward, no split | floor — plain MAPPO |
| **B2** | DA-MAPPO-2D | ✓ per-step | ✗ | fixed (e.g. 0.5) | isolates the assignment mechanism; our replication of DA-MAPPO |
| **B3** | IGAT-style (MAPPO-adapted) | ✗ (one-shot / static assignment) | ✓ | fixed | isolates the conflict-graph mechanism |
| **B4** | Fixed-weight MAPPO | ✓ | ✓ | **fixed**, swept ∈ {0.3, 0.5, 0.7} | **the decisive comparison** — same as ours but α not learned |
| **M** | Ours (PAH) | ✓ | ✓ | **learned per step** | the thesis contribution |

Reading the results:
- **M vs B4** → does *learning* α beat *fixing* α? (the thesis question)
- **B4 vs B2, B3** → do both mechanisms together beat each alone?
- **B2, B3 vs B1** → does each mechanism help at all?
- **assignment ablation on B2/B4** → does removing the augmented obs collapse success,
  as DA-MAPPO Table VI reports (→ 0%)? (correctness check on our whole stack)

For B1, the drone still needs *some* target — use a fixed nearest-target-at-reset
assignment (no re-solving), so B1 genuinely lacks the dynamic mechanism.

---

## 2. DA-MAPPO (Sheng et al. 2026) — extracted parameters

Source: `bin/91.../03_methodology.md`, `04_results.md`.

### Environment
| Item | Value |
|------|-------|
| Simulator | Gazebo (rigid body, ray-cast LiDAR) — **we replace with our 2D point-mass env** |
| Dimensionality | 3D at fixed altitude → effectively 2D |
| Drones `N` | 3 |
| Targets `M` | 3, one-to-one |
| Static targets | do not move |
| Dynamic targets | **periodically swap positions**; tested up to 3 m/s (6× UAV max speed 0.5 m/s) |
| Obstacle envs | ENV-1 = 30, ENV-2 = 40, ENV-3 = 50 obstacles |
| Episode limit `T_max` | 600 steps |
| Discount `γ` | 0.99 |

### Observation (dim 45)
| Component | Dim | Notes |
|-----------|-----|-------|
| LiDAR ranges | 35 | **we use 4 cardinal clearances instead** |
| Ego motion (v, ω, lin. accel, ang. accel — Kalman-filtered) | 4 | **we use (vx, vy)** |
| Target features: distance + relative bearing to assigned target | 2 | the key augmentation — **we keep this** |
| Swarm topology: relative `(Δx, Δy)` of each teammate | `2(N−1)` = 4 | dense (all teammates); **we use conflict-graph neighbors instead for B3/B4/M** |

### Action
- Continuous `(forward velocity v ∈ [−1,1] m/s, yaw rate ω ∈ [−1,1] rad/s)`
- **We use `(ux, uy) ∈ [−1,1]²`** (point mass, no heading)

### Assignment
- Cost `C[i,j] = squared Euclidean distance`
- Hungarian solved **every step**, from scratch, no memory of previous assignment
- Augmented obs `o = [z, u, g, q]` — `g` (target features) inserted after assignment

### Reward (sum of ~8 components, then `/50`)
| Tier | Terms |
|------|-------|
| Team | `−ω_team · Σ_j d_j` (sum of all drone→target distances) |
| Individual | progress `−κ·(d_prev − d_curr)`; arrival bonus `b_k` decreasing with arrival order; hover `+1` inside zone / `−10` if drifting out |
| Safety | obstacle: `−100` if LiDAR `< d_safe`, `−25` in `[d_safe, 2d_safe]`, `−10` in `[2d_safe, 3d_safe]`; soft continuous cost `< 2d_safe`; inter-drone `−100` if `< d_col` |
| Auxiliary | smoothness `−0.5|accel| − 0.2|ang.accel|`; step `−1`; boundary `−100` outside |
| Safety distance | `d_safe ≥ v_max·Δt + v_max²/(2 a_max)` (stopping distance) |

### Training
| Hyperparameter | Value |
|----------------|-------|
| Policy net | MLP, 3 hidden layers × 256 |
| Learning rate | 1e-5 |
| PPO epochs / update | 10 |
| PPO clip `ε` | 0.2 |
| Entropy coef | 0.1 |
| `γ` | 0.99 |
| Episode length | 600 |
| Total training | 3,000,000 env steps |
| Obstacle curriculum | 0–10 → 10–20 → 20–25 → 25–30 → 30–35 → 35–40 over the 3M steps (6 stages) |
| Hardware | Ryzen 9 7950X, RTX 4090, 64 GB — PyTorch 1.5.1, CUDA 10.1, Python 3.6.1 |

### Baselines they compared against
IPPO, MAPPO, RMAPPO, NavRL, EGO-Planner v2.

### Metrics
`R_success` (primary), `R_collision`, `R_timeout`, `T_ave` (avg steps to complete),
`L_ave` (avg trajectory length). 100 test episodes per env.

### Headline results (their env — **not a target for us**)
- Dynamic: ENV-1 99% / ENV-2 95% / ENV-3 90% success
- Up to **+25 percentage points** over the best baseline
- Near-zero static→dynamic degradation (≤ 2%)
- **Ablation (Table VI): removing the augmented state → 0% success across all envs**
- Reducing assignment frequency to every 50 steps → only 3–5% drop

### What we adopt / change
| Adopt | Change |
|-------|--------|
| Reward structure (progress + arrival + hover + graded safety + step) | env: 2D point-mass, not Gazebo |
| Per-step squared-distance Hungarian augmentation | obs: 4 cardinal clearances, not 35-beam LiDAR |
| PPO hyperparameters as **starting points** | action: `(ux, uy)`, not `(v, ω)` |
| Curriculum idea (staged difficulty) | LR: 1e-5 is very low — may raise to ~3e-4 and tune |
| 600-step episodes, `γ` 0.99 | our curriculum also grows **drone count** (3→5→8), not just obstacles |

### Stage-1 success criterion (given our env differs)
Not "hit 90–99%". Instead **qualitative replication**:
1. B2 (assignment aug) clearly beats B1 (no aug) on Stage-1 mission success, **and**
2. removing the augmented obs from a trained B2-style config **collapses** success
   toward zero (matches their Table VI).
If (2) does not hold, our stack has a bug — stop and investigate before proceeding.

---

## 3. IGAT-MARL (Rezaee et al. 2026) — extracted parameters

Source: `bin/9.../03_methodology.md`, `04_results.md`.

### Environment
| Item | Value |
|------|-------|
| Simulator | BlueSky (open-source ATC sim) |
| Aircraft model | BADA (EuroControl) — **fixed-wing** dynamics |
| Drones `N` | 3 → 10 (curriculum) |
| Episodes | 10,000; scenarios have **guaranteed conflicts** |
| Observation (dim 4) | `[lat/100, lon/100, heading/180 − 1, Mach(speed, altitude)]` — local only |

### Conflict graph
- From BlueSky conflict detection: pair `(i,j)` in `C^t` if `DCPA_ij < RPZ` within the
  look-ahead horizon
- Adjacency `A^t`: `1` for conflict pairs, `0` else, zero diagonal, symmetric
- Rebuilt every step; **example**: `N=5, C^t = {(1,3),(2,5)}` → only those 4 off-diagonal entries are 1

### Network (IGAT)
| Item | Value |
|------|-------|
| Attention heads `H` | 4 |
| Hidden dim | 128 |
| Dropout | 0.6 |
| Structure | 2 IGAT blocks × 2 GAT layers each = 4 attention passes; residual + LayerNorm after each |
| Per-layer | linear transform → pairwise energy `LeakyReLU(aᵀ[h_i‖h_j])` → mask non-neighbors → softmax → weighted aggregate → multi-head concat → residual + LN |

### RL algorithm
- **DQN** (off-policy, replay buffer, target network) — **NOT PPO**
- **Discrete** actions: `{0°, +15°, −15°}` heading change
- ε-greedy in training, greedy in eval
- **Conflict-gated execution**: only drones currently in a conflict receive a command

### Reward (per step, per drone; all terms negative)
```
r_i = −|ψ_i − ψ_ref|/ψ_max      (off-track penalty)
      − n_i                       (active conflict count)
      − (1 − exp(1 − 1/√max(x_ij, ε))),  x_ij = DCPA_ij / RPZ   (CPA proximity risk)
```
Team objective: maximize `E[Σ γ^t · (1/N) Σ_i r_i^t]`.

### Training strategy
- Curriculum + **transfer learning**: train `N=3` to convergence → init `N=4` with those
  weights → ... → `N=10`
- Effect at `N=4`: +280 reward (~34%) and −155 LoS steps (~38%) in the first 2000 episodes

### Metrics
Cumulative reward; `t_loss` (total time steps in loss-of-separation — the safety
metric); action bias (distribution over the 3 actions); number of active edges.

### Headline results
- `N=5`: **+17.56%** reward, **−10.52%** `t_loss`, **−43.93%** edges vs the DGN benchmark
- Edge count grows **sub-quadratically** with `N`
- Architecture ablation: every reduction in attention depth hurts all three metrics

### What we adopt / change
| Adopt | Change |
|-------|--------|
| Conflict-graph construction via DCPA/TCPA (CPA math) | algorithm: we stay on **MAPPO**, not DQN |
| Sparse adjacency, node degree as a feature | actions: continuous `(ux, uy)`, not discrete `±15°` |
| CPA-based continuous proximity term in `r_safety` | dynamics: point-mass, not fixed-wing BADA |
| Curriculum + weight transfer across swarm sizes | GAT depth (2×2): optional; we may start with a lighter neighbor encoder and only use GAT for the B3 baseline |
| "dangerous-proximity time" as a secondary safety metric (our `t_loss` analogue) | conflict-gated execution: optional; our drones always act |

### Important note on B3
B3 is **"IGAT-style", not "IGAT reproduced"**. IGAT is a discrete-action DQN with a GAT
over the conflict graph. Our B3 is MAPPO (continuous) that receives conflict-graph
neighbor features (optionally via a GAT encoder) but has **no real-time Hungarian
assignment**. This deviation is deliberate — we need all baselines on the same
MAPPO backbone for a fair α comparison — and must be stated in the thesis. See `04` Q12.

---

## 4. Where the numbers are NOT comparable

- DA-MAPPO / IGAT success and reward numbers are in **their** simulators with **their**
  dynamics and obs. Do not put "DA-MAPPO: 90%" next to "ours: X%" as if it is a fair
  head-to-head. The fair comparison is **our B2 vs our M**, all in our env.
- The only cross-paper thing we borrow as a *check* is the **shape** of DA-MAPPO's
  ablation result (augmented obs removed → collapse).
