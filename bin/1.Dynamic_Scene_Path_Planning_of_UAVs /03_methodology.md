# Methodology — Exactly What the Researchers Did

---

## Research Design

- **Type of study:** Simulation-based experimental study using deep reinforcement learning
- **Overall strategy:** Model the UAV path planning problem mathematically (as an MDP), design an improved DRL algorithm, train it in simulation (first static, then dynamic environments), and compare results against classical and DRL baselines

---

## The Environment (Simulation Setup)

**Mission Area:**
- A 2D rectangular region measuring **60 × 60 km**
- The UAV flies at constant altitude, so only (x, y) coordinates matter — no 3D complexity
- One reconnaissance **target** at position (52, 52)
- Three circular **obstacle/no-fly zones** (modeled as SAM + radar systems)

**Obstacle Zone Parameters:**

| Obstacle | Center Location (km) | Detection Radius Rmax (km) | Kill Radius RMmax (km) |
|----------|---------------------|-----------------------------|------------------------|
| Obstacle 1 | (20, 22) | 6 | 5 |
| Obstacle 2 | (30, 40) | 10 | 9 |
| Obstacle 3 | (40, 18) | 8 | 7 |

**The No-Fly Zone Threat Model:**
Each obstacle zone has two radii:
- **Rmax (detection radius):** If the UAV enters this zone, the radar detects it and the SAM is activated
- **RMmax (kill radius / no-escape zone):** If the UAV enters this inner zone, destruction probability is 100%

Between the two radii, danger increases as distance decreases. The danger level (Tp) for a single obstacle is:

- If distance D ≥ Rmax: Tp = 0 (safe)
- If RMmax ≤ D < Rmax: Tp = 2 − (D − RMmax) / (Rmax − RMmax) → gradually increasing danger
- If D < RMmax: Tp = 1 (certain destruction)

For multiple overlapping threat zones, the combined danger level is:

**Ts = 1 − ∏(1 − Tp_i)** for all obstacle zones i

This computes the probability that the UAV survives all k threat zones simultaneously.

---

## MDP Element Design

The path planning problem is translated into a Markov Decision Process with three key elements:

### State Space
The UAV's state is its current position in the 2D grid:
**S = (x, y)**

The environment is discretized into a grid. The UAV knows where it is, where the target is, and can detect nearby threat zones.

### Action Space
The UAV can move to any of its **8 neighboring grid cells** (north, northeast, east, southeast, south, southwest, west, northwest):
**A = {0, 1, 2, 3, 4, 5, 6, 7}**

- 0 = North, 1 = Northeast, 2 = East, 3 = Southeast, 4 = South, 5 = Southwest, 6 = West, 7 = Northwest (based on programming convention)
- Each action moves the UAV one grid step in the corresponding direction

### Reward Function
A five-component reward function drives learning:

**R = r1 + r2 + r3 + r4 + r5**

| Component | Condition | Value |
|-----------|-----------|-------|
| r1 | UAV in obstacle area | −10·Ts − 0.5 (if Ts ≤ threshold Tσ) OR −50 (if Ts > Tσ) |
| r2 | UAV reaches target area | +200 |
| r3 | UAV exits environment boundary | −50 |
| r4 | UAV exceeds maximum steps (500) | −50 |
| r5 | Any other state (normal flight) | −0.5 |

**Why this design works:**
- The large +200 for reaching the target is the mission objective signal
- The −0.5 per step encourages the UAV to find the *shortest* path, not just any safe path
- The proportional penalty for obstacle proximity (−10·Ts) teaches the UAV to prefer flying *far* from threats
- The −50 for boundary/step-limit violations trains the UAV to stay within operational constraints

An episode terminates when any of the first four conditions are met.

---

## The Methods

### Step 1: Heuristic Action Selection Policy

**What it does:** Limits random exploration to a geometrically sensible subset of actions based on the relative position of the target.

**Why:** Standard ε-greedy exploration wastes many training episodes choosing directions that move away from the target. The heuristic fixes this.

**How it works:**
- Compare current UAV position (x1, y1) with target position (x2, y2)
- Based on which quadrant the target is in relative to the UAV, restrict random actions to 5 of the 8 directions
- Example: if target is to the southeast (x2 > x1 and y2 < y1), random actions are chosen from {1, 3, 5, 6, 7} — not all 8
- The subspace always includes 3 "direct" directions toward the target + 2 "boundary" directions (to prevent local optima traps)

**Fits into the pipeline:** Applied during the exploration phase of ε-greedy — replaces pure random selection with informed random selection.

### Step 2: Improved D3QN Neural Network

**Architecture:**
- **Input layer:** 2 neurons (x, y state)
- **Hidden layers:** Two fully connected layers — L1 (100 neurons, ReLU) and L2 (80 neurons, ReLU)
- **Output layer (dueling split):**
  - Value stream: 1 output → V(S) — how good is this state?
  - Advantage stream: 8 outputs → A(S, a) for each action — how much better is each action?
  - Combined Q-value: Q(S, A) = V(S) + [A(S, A) − mean of all A(S, a')]

**Two network instances:**
- **Evaluation network** (parameters w): selects actions + updated via gradient descent
- **Target network** (parameters w'): computes target Q-values; updated to match w every N' steps (every 8 steps in static / every update steps in dynamic)

### Step 3: Target Q-Value Computation (DDQN style)

Instead of the standard DQN formula (which overestimates):
> yj = Rj + γ · max_a' Q'(S'j, a', w')

The paper uses the DDQN decoupled formula:
> yj = Rj + γ · Q'(S'j, argmax_a' Q(S'j, a, w), w')

**Plain English:** The evaluation network (w) decides *which* action is best; the target network (w') evaluates *how good* that action is. Separating these two roles prevents overestimation.

### Step 4: Prioritized Experience Replay

**What it does:** Assigns higher sampling probability to transitions where the agent's Q-value prediction was most wrong.

**How it works:**
1. After each training step, compute TD error for each sample: δj = |yj − Q(Sj, Aj, w)|
2. Store δj as the priority pj for that transition in a **Sum Tree** data structure
3. When sampling a mini-batch of 32 transitions, sample with probability Pj ∝ pj
4. To correct the statistical bias introduced by non-uniform sampling, apply importance-sampling weights ωj to the loss function

**Modified loss function:**
> Loss = (1/n) · Σ ωj · [yj − Q(Sj, Aj, w)]²

---

## The Experiments

### Static Scene Training
- UAV starts at a random position: x ∈ (0, 30) km, y ∈ (0, 15) km
- Maximum steps per episode: 500
- Training rounds: 10,000
- Pre-training: 200 rounds (to populate the replay buffer)
- ε annealed from 1.0 to 0.1 over 2,000 rounds, then held at 0.1
- Compared against: DQN, DDQN, A* (8-neighborhood), RRT-GoalBias (step=1, goal bias=0.1, max iter=250)

### Dynamic Scene Training
- Same environment, but all three obstacle centers move along pre-defined trajectories
  - Two move back and forth in the X direction
  - One moves back and forth along a diagonal
  - One moves slower than the others
- Training rounds: 20,000 (no pre-training)
- **Transfer learning:** Starts from the best weights trained in the static scene — not random initialization
- Key hyperparameter changes: learning rate 0.00005 (reduced from 0.0005), replay buffer capacity 50,000 (increased from 10,000)

### Evaluation Metrics
| Metric | What it measures |
|--------|-----------------|
| Cumulative reward | Total reward per episode — higher is better |
| Success rate | Fraction of episodes where target is reached |
| Path length / UAV steps | Number of grid steps to reach target — fewer is better |
| Planning time | Computation time to produce a path — less is better |
| Number of turning points | Path smoothness — fewer turns = less energy needed |
| Convergence speed | How many training rounds until performance stabilizes |

### Hardware/Software
- **Programming language:** Python
- **Deep learning framework:** TensorFlow (with TensorBoard for visualization)
- **Optimizer:** Adam
- **Platform:** Same computer used for all algorithm comparisons (for fair timing results)

---

## Pipeline Diagram

```
[UAV Starting Position (random within training zone)]
              ↓
[Environment: 60×60 km 2D grid with 3 threat zones + 1 target]
              ↓
[State: current (x, y) position]
              ↓
[Action Selection via Heuristic ε-greedy Policy]
    ↓                           ↓
[Random action from             [Greedy action = argmax Q(S,a)]
 heuristic-narrowed subspace]
              ↓
[Execute action → new state (x', y')]
              ↓
[Compute Reward R using 5-component reward function]
              ↓
[Store (S, A, R, S', done) in Prioritized Experience Replay Buffer]
              ↓
[Sample mini-batch (size 32) — weighted by TD-error priority]
              ↓
[Compute Target Q-value using DDQN formula (eval net selects, target net evaluates)]
              ↓
[Compute Weighted Loss → Backpropagation → Update Evaluation Network]
              ↓
[Update TD errors and Sum Tree priorities]
              ↓
[Every N' steps: Copy evaluation network weights → Target network]
              ↓
[Repeat until 10,000 rounds (static) or 20,000 rounds (dynamic)]
              ↓
[Evaluate trained model on test scenarios → Compare vs baselines]
```
