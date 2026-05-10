# 03 — Methodology: Exactly What the Researchers Did

---

## Research Design

**Type of study:** Computational/simulation experimental study.

**Overall strategy:** Design a novel DRL algorithm (TANet-TD3), train it in a custom 3D simulation environment, and compare it against four baseline algorithms across multiple scenarios — varying number of UAVs (3–7) and number of obstacles (10–30) — to validate effectiveness.

---

## The Data (Simulation Environment)

There is no real-world dataset. The authors built their own simulation environment from scratch using the **OpenAI Gym** platform.

**Environment specifications:**
- 3D cubic space: 2 × 2 × 2 units
- UAVs, targets, and obstacles are all modeled as spheres
- All positions and velocities are randomly initialized at the start of every episode

**Object parameters:**

| Object | Radius | Max detection range | Motion |
|--------|--------|--------------------|----|
| UAV | 0.02 units | 0.5 units (spherical) | Controlled by agent |
| Target | 0.12 units | — | Static |
| Obstacle | 0.10 units | — | Static OR moving linearly |

**Obstacle motion:** In mobile mode, obstacles move in a straight line with randomly initialized direction and speed v ∈ [−0.05, 0.05] in each axis. When they hit a wall, they bounce back in the opposite direction.

**Why this environment is appropriate:** It captures the core challenges — dynamic obstacles, partial observability (UAVs can't see beyond 0.5 units), 3D movement, and multi-agent interactions — while being fully controllable for systematic testing.

---

## The Methods

### Part 1: Problem Formulation as a POMDP

The multi-UAV problem is formalized as a POMDP tuple: ⟨N, S, O, A, P, R⟩

**State Space (what each UAV knows at time t):**

Each UAV's state = Internal state + Environmental observations

*Internal state of UAV i:*
- Position: (x_i, y_i, z_i)
- Velocity: v_i
- Radius: r_i

*Environmental observations (within detection range):*
- Target info: relative position to target + target radius
- Other UAV info: relative positions, velocities, radii of all other UAVs
- Obstacle info (if within range): relative position, velocity, radius — if outside range, the entry is filled with ±d_det (boundary sentinel values)

**Action Space:**
Each UAV selects a force vector: a_i = (F_x, F_y, F_z). Force generates acceleration (F/m), which changes velocity, which changes position. This is a *continuous* action space — not discrete left/right/up/down commands.

**Reward Function:**
The total reward is a sum of three components:

| Reward type | When active | Formula |
|-------------|-------------|---------|
| Approaching target (R_t) | Every step | 0 if reached (d < r_u + r_t); else −d |
| Avoiding UAVs (R_j) | When UAVs too close | −1 if d_ij ≤ 2r_u; else 0 |
| Avoiding obstacles (R_o) | When obstacles within range | −(d_det − d_o) if d_o < d_det; −1 if d_o ≤ r_u + r_o; else 0 |

**Design rationale:** All guided rewards are negative — every extra step costs the UAV something. This means minimizing negative reward = flying shorter, safer paths. There is no artificially large "arrival bonus," which avoids the sparse reward problem. The reward naturally reflects flight path length.

---

### Part 2: TD3 Algorithm (the navigation backbone)

TD3 uses an Actor-Critic architecture with four networks plus two target networks:

**Networks:**
- Actor (π_φ): State → Action (the flight decision-maker)
- Critic 1 (Q_θ1), Critic 2 (Q_θ2): (State, Action) → Q-value
- Actor Target (π_φ'), Critic Target 1 (Q_θ1'), Critic Target 2 (Q_θ2')

**Three key innovations over DDPG:**

**① Clipped Double-Q Learning**
Instead of one critic Q-value, compute two and use the *minimum*:
```
y = R(s,a) + γ × min[Q_θ1'(s',a'), Q_θ2'(s',a')]
```
Why: Using the minimum prevents the over-optimistic Q-value estimates that plague DDPG.

**② Delayed Policy Update**
The Actor is only updated every 2 Critic updates. This lets the value function become accurate before it's used to update the policy. An inaccurate critic would mislead the actor.

**③ Target Policy Smoothing**
Noise is added to the target action:
```
a'(s') = π_φ'(s') + ε,   ε ~ clip(N(0,σ̃), −c, c)
```
This prevents the policy from overfitting to sharp peaks in Q-values that might be artifacts of function approximation.

**Network architecture:**
- Actor: s_i × 64 × 128 × 64 × a_i (first 3 layers: ReLU activation; last layer: Tanh, to bound output in [−1, 1])
- Critic: (s_i + a_i) × 64 × 128 × 64 × Q_i (3 layers with ReLU)

---

### Part 3: TANet — Target Assignment Network

This is the novel contribution. TANet runs in parallel with TD3 and answers: "Given my current state, which target should I fly toward right now?"

**Network architecture:**
- Input: state of UAV i with dimension (7 + 4(N_U−1) + 4N_T + 7N_O)
  - 7 = UAV's own internal state
  - 4(N_U−1) = relative info about other UAVs
  - 4N_T = info about all targets
  - 7N_O = info about obstacles in detection range
- Hidden layers: 64 → 128 → 64 (fully connected)
- Output: N_T scores → Softmax → probabilities (P_iT1, P_iT2, …, P_iTNT)
- The target with the highest probability is the current assignment

**How TANet is trained (construction of assignment labels):**

Step 1: For each UAV i and each possible target j, temporarily set target j as UAV i's destination and execute the TD3 actor to get the Q-value Q_ij.

Step 2: Form a N_U × N_T Q-value matrix (one row per UAV, one column per target).

Step 3: Apply the **Hungarian algorithm** to find the optimal complete one-to-one assignment that maximizes the total Q-value across all UAVs. This gives a permutation matrix (zeros and ones only) where a "1" in row i, column j means "UAV i is assigned to target j."

Step 4: Use this permutation matrix as the training label. Train TANet using cross-entropy loss:
```
H(L, P) = −Σ l_j × log(p_ij)
```

**Why use Q-values instead of pure distance?**
Distance ignores obstacles. A target that looks close may be blocked by moving obstacles. Q-values capture the full long-term expected reward, automatically accounting for obstacles, other UAVs, and future dynamics.

**Construction of new environmental state sequence:**
After TANet assigns target T_j to UAV i, the target sequence in the observation is reordered — T_j is placed *first* in the list. This tells the TD3 path planner "this is your primary target." TD3 then plans the flight accordingly.

---

## The Experiments

**Training experiments (Section 5.2):**

*Phase 1 — TD3 vs DDPG for path planning alone:*
- Scenario I: 1 UAV, 1 target, 20 moving obstacles → 5,000 episodes
- Scenario II: 3 UAVs, 1 target, 20 moving obstacles → 5,000 episodes
- Goal: confirm TD3 is a better base than DDPG before building TANet on top

*Phase 2 — TANet-TD3 vs comparison algorithms:*
- Dynamic environment: 5 UAVs, 5 targets, 20 *moving* obstacles → 10,000 episodes
- Mixed environment: 5 UAVs, 5 targets, 10 static + 10 moving obstacles → 10,000 episodes
- Baselines: TANet-DDPG, DDPG(distance), TD3(distance)
- 50 verification episodes every 10 training episodes

**Testing experiments (Section 5.3):**
- Convergence: use saved weights, run 1 episode visually in each environment
- Compare UAV trajectories, target coverage, collision rate

**Statistical experiments (Section 5.4):**
- Vary UAVs: 3, 4, 5, 6, 7 (20 obstacles fixed) × 1,000 episodes each
- Vary obstacles: 10, 15, 20, 25, 30 (5 UAVs fixed) × 1,000 episodes each
- Compare TANet-TD3 vs TANet-DDPG in both dynamic and mixed environments

**Evaluation metrics:**
- Average reward = total reward across episodes ÷ number of verification episodes
- Average arrival rate = UAVs reaching targets ÷ (episodes × N_U)
- Average target completion rate = targets covered ÷ (episodes × N_T)

**Hardware/Software:**
- OpenAI Gym-based custom 3D simulation environment
- Hardware not explicitly specified in the paper

---

## Hyperparameters

| Parameter | Value |
|-----------|-------|
| Max training episodes (TD3) | 5,000 |
| Max training episodes (TANet-TD3) | 10,000 |
| Max episode length | 100 steps |
| Discount factor γ | 0.9 |
| Critic learning rate | 1×10⁻³ |
| Actor learning rate | 1×10⁻⁴ |
| Replay buffer size | 5×10⁵ |
| Batch size | 256 |
| Soft update factor τ | 0.01 |

---

## Pipeline Diagram

```
[UAV Onboard Sensors]
        ↓
[Local Observation: own state + targets + other UAVs + obstacles within range]
        ↓
[TANet: Assignment Network]
  Input: full state observation
  Hidden: 64 → 128 → 64 neurons
  Output: probabilities over all targets → argmax → assigned target T_j
        ↓
[Reorder observation: put T_j first in target sequence]
        ↓
[TD3: Path Planning]
  Actor network: s → 64 → 128 → 64 → force (Fx, Fy, Fz)
  Execute action → UAV moves → receives reward R
        ↓
[Store (s, a, R, s') in Replay Buffer]
        ↓
[Sample mini-batch from Replay Buffer]
        ↓
[TD3 Training:
  For each target j: compute Q-value of going to T_j → Q matrix (N_U × N_T)
  Hungarian algorithm on Q matrix → permutation matrix (assignment labels)
  Update Critic networks (minimize MSE with Bellman target)
  Every 2 steps: Update Actor (maximize Q)]
        ↓
[Cross-entropy loss: TANet predictions vs. Hungarian labels → Update TANet]
        ↓
[Soft update: target networks slowly track main networks]
        ↓
[Repeat for 10,000 episodes]
        ↓
[Convergence → Deployed policy]
```
