# 03 — Methodology: Exactly What the Researchers Did

---

## Research Design

**Type of study:** Simulation-based experimental study with comparative analysis.

**Overall strategy:** Design a DQN with three key enhancements (3D grid encoding, dynamic reward, input normalization), train it in four progressively harder 3D simulation environments, and compare its performance against four baseline algorithms (Q-learning, GWO, SSA, PSO) across four metrics (SLR, CT, PL, SR) over 20 independent runs per algorithm per scenario.

---

## The Data (Simulation Environment)

No real-world dataset is used. The authors construct a custom 3D simulation environment.

**Environment representation:**
- The 3D flight space is discretized into a **grid of cubic cells**
- Each cell's side length = UAV's radius (R_uav) — sized to match the drone's physical dimensions plus safety margin
- The UAV is modeled as a **sphere** circumscribed within one cell
- Obstacles are modeled as groups of occupied cells, with a **buffer zone** of extra cells added around each obstacle for safety margin
- Movements are constrained to stay within the operational boundaries
- At boundaries, all actions are directed inward to keep the drone inside the space

**Four test scenarios (increasing complexity):**

| Scenario | Start point (km) | Target point (km) | Static obstacles |
|----------|-----------------|-------------------|-----------------|
| 1 | (0.5, 0.5, 0.5) | (6.5, 6.5, 3.5) | 6 |
| 2 | (0.5, 0.5, 0.5) | (13.5, 11.5, 3.5) | 10 |
| 3 | (0.5, 0.5, 0.5) | (19.5, 19.5, 3.5) | 24 |
| 4 | (0.5, 0.5, 0.5) | (24.5, 24.5, 24.5) | 40 |

Each scenario runs for **20 independent executions** per algorithm to get statistically reliable results.

**Why this environment is appropriate:** The four scenarios cover progressively harder conditions — from a short 7 km path with 6 obstacles (simple) to a long 25 km path in full 3D space with 40 obstacles (very complex). This graduated difficulty cleanly reveals where each algorithm starts to fail.

---

## The Methods

### Part 1: Problem Formulation as an MDP

The path planning problem is modeled as a Markov Decision Process (MDP) with:

**State Space (S):** All possible drone states in the 3D grid. The state s_t encodes the drone's current position in the grid plus the available environmental information (obstacle layout). This state is encoded into a 3D array suitable for the convolutional neural network.

**Action Space (A): 26 directions**
The drone can move to any adjacent cell — in 3D, there are 26 neighboring cells (the 6 face neighbors, 12 edge neighbors, and 8 corner neighbors of a cube). Diagonal moves are prioritized as they provide more direct paths. When an obstacle is in a direction, that action is automatically excluded.

**Reward Function R (the key innovation):**

```
R = { +1              if next cell is the target
    { -1              if next cell is a forbidden (obstacle) cell
    { d3 / (d1 + d2)  otherwise (dynamic reward)
```

Where:
- **d1** = √[(x_{t+1}−x_t)² + (y_{t+1}−y_t)² + (z_{t+1}−z_t)²] — Euclidean distance the drone just moved (step size)
- **d2** = √[(x_{t+1}−x_T)² + (y_{t+1}−y_T)² + (z_{t+1}−z_T)²] — Distance from next position to target
- **d3** = √[(x_t−x_T)² + (y_t−y_T)² + (z_t−z_T)²] — Distance from current position to target (before moving)

**Intuition behind d3/(d1+d2):**
- d3 is the "how far you were" — the denominator starts from this baseline
- d2 is the "how far you are now" — if d2 < d3, you moved closer → reward increases
- d1 is the "how far you stepped" — a small efficient step toward the target is better than a large diagonal detour
- When the drone moves directly toward the target efficiently: d2 decreases, d1 is small → d3/(d1+d2) is large → high reward
- When the drone moves away: d2 increases → d3/(d1+d2) is small → low reward

**Discount factor:** γ = 0.8 — moderate future discounting, balanced between immediate and future rewards.

**Transition probability T:** Deterministic (in simulation, if the drone moves toward cell X, it arrives at cell X with probability 1, unless blocked).

---

### Part 2: DQN Architecture

**Two-network design:**

**Evaluation Q-Network (QE, parameters θE):**
- Actively selects actions using ε-greedy policy
- Updated every training step by minimizing the MSE loss
- Parameters updated via stochastic gradient descent

**Target Q-Network (QT, parameters θT):**
- Provides stable Q-value targets for training
- Parameters are frozen and only updated (by copying θE → θT) every N episodes
- This prevents the "moving target" instability

**Loss function:**
```
L(θE) = E[(r_t + γ × max QT(s_{t+1}, a_{t+1}|θT) − QE(s_t, a_t|θE))²]
```

**Parameter update rule (stochastic gradient descent):**
```
ΔθE = [r_t + γ × max QT(s_{t+1}, a_{t+1}|θT) − QE(s_t, a_t|θE)] × δQE/δθE
```

**Neural Network Architecture:**

```
Input Layer
   ↓ (3D grid encoding of environment + UAV state)
3D Conv Layer 1: 64 filters, kernel (5×5×5), stride=1, zero-padding, ReLU
   ↓
3D Conv Layer 2: 32 filters, kernel (5×5×5), stride=1, zero-padding, ReLU
   ↓ (spatial feature extraction complete)
Fully Connected Layer 1: 256 neurons
   ↓
Fully Connected Layer 2: 256 neurons
   ↓
Output Layer: 26 neurons (one Q-value per action direction)
   ↓
Regression Layer: optimizes Q-value estimation
```

**Design rationale for 3D CNN:**
- Regular 2D CNNs process flat images; here the environment is inherently 3D
- 3D convolutions capture spatial relationships in all three dimensions simultaneously
- The 5×5×5 kernel is large enough to detect obstacle patterns over a meaningful neighborhood
- Zero-padding preserves spatial dimensions through each conv layer
- 64 → 32 filters: first layer extracts broad spatial features; second layer extracts refined features

---

### Part 3: State Encoding and Normalization

**State encoding:**
- The flight space is converted to a 3D binary grid: 0 = free cell, 1 = obstacle cell
- Buffer zones around obstacles are also marked as occupied
- The drone's current position is encoded as its (x, y, z) grid coordinates
- This grid is the input to the 3D CNN — it gives the network a structured spatial representation

**Input normalization:**
- All state inputs are normalized (divided by their maximum values or range) before feeding into the network
- This ensures all features are on comparable scales — prevents some features from dominating simply because of large numerical values
- Improves training stability and speeds up convergence

**Why encoding matters:** Classic Q-learning encodes each state as a discrete table entry — one row per position. With millions of possible positions in a large environment, this is impossible. The 3D grid encoding lets the CNN generalize: if it learns "move away from nearby obstacles" in one part of the grid, this knowledge transfers to other parts automatically.

---

## The Experiments

**Training configuration:**

| Parameter | Value |
|-----------|-------|
| Max episodes | 2,000 |
| Max steps per episode | 10,000 |
| Discount factor γ | 0.8 |
| Exploration factor ε | 0.9 |
| Batch size κ | 32 |
| Replay buffer size S_M | 2,000 |

**Comparison algorithms:**
- **Q-Learning** (standard tabular RL baseline)
- **GWO** (Grey Wolf Optimizer — fast metaheuristic)
- **SSA** (Salp Swarm Algorithm — bio-inspired metaheuristic)
- **PSO** (Particle Swarm Optimization — classic swarm intelligence)

**Evaluation protocol:**
- 20 independent runs per algorithm per scenario
- Metrics reported: Best, Mean, Worst, and STD for SLR, CT, and PL
- Success Rate (SR) reported as percentage of successful runs out of 20

**Evaluation metrics:**
- **SLR** (Straightness Line Rate): actual path length ÷ straight-line distance. Lower = better.
- **CT** (Computational Time in seconds): planning time. Lower = faster.
- **PL** (Path Length in km): total distance flown. Lower = more efficient.
- **SR** (Success Rate %): percentage of runs reaching the target without collision. Higher = safer.

---

## Full Pipeline Diagram

```
[Define 3D flight environment as grid]
         ↓
[Mark obstacle cells + add buffer zones]
         ↓
[Encode state: UAV position + 3D grid → normalized input tensor]
         ↓
[Initialize Evaluation Q-Network (QE) and Target Q-Network (QT = copy of QE)]
[Initialize Replay Buffer (capacity 2,000)]
         ↓
FOR each episode (1 to 2,000):
  FOR each step (1 to 10,000):
    ↓
    [ε-greedy: 90% random OR best action from QE]
    ↓
    [Execute action → move to next cell]
    ↓
    [Check next cell:
      → Target? → reward = +1, episode ends (success)
      → Obstacle? → reward = -1, episode ends (failure)
      → Free cell? → reward = d3/(d1+d2)]
    ↓
    [Store (s_t, a_t, r_t, s_{t+1}) in replay buffer]
    ↓
    [Sample random batch of 32 from replay buffer]
    ↓
    [Compute target: y_t = r_t + γ × max QT(s_{t+1})]
    ↓
    [Compute loss L = MSE(QE(s_t, a_t), y_t)]
    ↓
    [Update QE weights via gradient descent]
    ↓
    [Every N episodes: copy QE weights → QT (target network update)]
  END FOR
END FOR
         ↓
[Trained QE policy: given any state, output Q-values for all 26 actions]
         ↓
[Deployment: at each step, pick action = argmax Q-values]
         ↓
[Collision-free path from start to target]
```
