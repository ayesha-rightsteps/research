# 02 — Target Assignment and Conflict Graph

The two mechanisms that feed the observation and the PAH inputs. Both are recomputed
**every decision step**.

---

## Part 1 — Target Assignment (Hungarian)

### 1.1 Cost matrix

`C ∈ ℝ^{N×M}` with `M = N` (one target per drone). DA-MAPPO uses **squared** Euclidean
distance:

```
C[i, j] = || p_drone_i − p_target_j ||²
```

Squared vs plain distance: squared penalizes far assignments more and is what DA-MAPPO
used — match it for the replication baseline.

### 1.2 Solve

```python
from scipy.optimize import linear_sum_assignment

def assign_targets(drone_pos, target_pos):
    # drone_pos: [N, 2], target_pos: [M, 2]
    diff = drone_pos[:, None, :] - target_pos[None, :, :]      # [N, M, 2]
    cost = (diff ** 2).sum(-1)                                  # [N, M]
    rows, cols = linear_sum_assignment(cost)                    # optimal matching
    # assignment[i] = index of the target assigned to drone i
    assignment = cols[rows.argsort()]
    return assignment
```

`O(N³)`. Negligible for `N ≤ 8` (DA-MAPPO: still fast at 40 agents).

### 1.3 The assignment-thrashing problem

Recomputing the optimal matching every step means that when two targets are near-
equidistant from a drone, the assignment can **oscillate** step to step. The drone then
dithers between them and makes no progress. "Target reassignments per episode" is a
secondary metric precisely because this is a known failure mode.

DA-MAPPO ran per-step assignment and reported it works — but note their dynamic targets
**swap positions discretely** rather than drifting continuously, so the assignment is
piecewise-stable between swaps. Our Stage 2+ target model matters here (see
`00_problem_formalization.md` §2 and `04` Q13).

### 1.4 Anti-thrashing options (in order of preference)

1. **Do nothing first.** Match DA-MAPPO (per-step, no hysteresis). Log the
   reassignment metric. Only act if thrashing actually shows up.
2. **Switching cost.** Add a penalty to the cost matrix for any assignment that differs
   from the current one:
   `C'[i, j] = C[i, j] + λ_switch · 1[j ≠ current_assignment[i]]`.
   Simple, keeps the assignment optimal-with-inertia.
3. **Hysteresis / margin.** Keep the current assignment unless a new one is better by
   more than a margin `δ` in total cost.
4. **Event-triggered.** Reassign only every `K` steps or when a target moves. DA-MAPPO's
   ablation: assigning every 50 steps instead of every step cost only **3–5%** success —
   so this is cheap insurance if needed.

DA-MAPPO's own ablation (Table VI) shows the **augmented observation** is what matters
(removing it → 0% success); assignment *frequency* is a softer knob.

### 1.5 What goes into the observation

From the assignment, drone `i` gets (see `00` §4, "Assigned target"):
- relative position of its assigned target: `Δx = x_target − x_i`, `Δy = y_target − y_i`
- distance `d_target = ||Δ||` (also a PAH input)

Optionally relative bearing (DA-MAPPO uses polar `[distance, bearing]`) — with a
point-mass model there is no heading, so cartesian relative position is the natural form.

---

## Part 2 — Conflict Graph (from IGAT-MARL)

### 2.1 Idea

Instead of connecting every drone to every other drone (dense, `O(N²)`, noisy), connect
**only pairs on a collision course** within a look-ahead horizon. Keeps the graph
sparse and safety-relevant as `N` grows. IGAT reports **44% fewer edges** than a dense
graph at `N = 5`, with better safety.

### 2.2 Closest-point-of-approach (CPA) math — do this properly

For a pair `(i, j)`, with relative position and velocity

```
p = p_i − p_j            # [2]
v = v_i − v_j            # [2]
```

If `v·v ≈ 0` (near-parallel, same speed) → they stay at constant separation; use
current distance. Otherwise the **time of closest approach** is

```
t* = − (p · v) / (v · v)
```

Clamp to the look-ahead window: `t*_clamped = clip(t*, 0, H)`.

The **distance at closest point of approach**:

```
DCPA = || p + v · t*_clamped ||
```

**Edge rule:** add edge `(i, j)` if `DCPA < d_danger` **and** `0 ≤ t* ≤ H`
(i.e. the close approach is in the future, within the horizon — not already past).

> ⚠️ The guide's version (`implementation_guide.md` §3) only checks the distance at
> exactly `t = H`. That misses pairs that pass close *before* `H` and separate again.
> Use the CPA formula above.

### 2.3 Adjacency matrix

```
A[i, j] = A[j, i] = 1  if edge(i, j)   else 0
A[i, i] = 0                                        # no self-loops (IGAT)
```

Rebuilt every step. `n_conflict_i = Σ_j A[i, j]` (node degree) — this is a PAH input.

### 2.4 Parameters

| Param | Symbol | Start | Note |
|-------|--------|-------|------|
| Look-ahead horizon | `H` | 3 s | calibrate; longer = more edges, more anticipation |
| Danger threshold | `d_danger` | `3 · d_col` | also the CPA scale in the safety reward term |

### 2.5 What goes into the observation

Drone `i`'s conflict neighbors (the `j` with `A[i,j] = 1`):
- **sorted by `t*` ascending** (most imminent first)
- take the first `K_nbr` (proposed 4); zero-pad if fewer; **mask bit** per slot
- per neighbor: relative position `Δp` and relative velocity `Δv` (4 numbers) + mask

If a graph-attention encoder is used instead (for the B3 IGAT-style baseline), `A` is
fed directly and the encoder pools over the true neighbor set — no fixed `K_nbr`.

### 2.6 Time-to-collision for PAH

`τ_collision,i` = the **smallest `t*`** among drone `i`'s conflict edges (the most
imminent threat). If `i` has no conflict edges, set `τ_collision = H` (normalized → 1,
"safe"). This is PAH input 1.

---

## Part 3 — How the three consumers connect

```
                 ┌─────────────────────────────┐
   positions ───►│ Hungarian assignment (§1)    │──► assigned target  ──┐
                 └─────────────────────────────┘                        │
                 ┌─────────────────────────────┐                        ▼
 pos + vel  ───► │ Conflict graph / CPA (§2)   │──► neighbor list ──►  Observation O_i
                 └─────────────────────────────┘        │                ▲
                        │           │                   │                │
                        ▼           ▼                   ▼                │
                  τ_collision   n_conflict          (d_target) ──────────┘
                        │           │                   │
                        └───────────┴───────┬───────────┘
                                            ▼
                                   ┌──────────────────┐
                                   │  PAH  →  α ∈ [0,1]│
                                   └──────────────────┘
```
