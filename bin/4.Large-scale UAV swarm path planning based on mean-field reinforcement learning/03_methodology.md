# 03 — Methodology: Exactly What the Researchers Did

---

## Research Design

**Type of study:** Simulation-based experimental study using multi-agent deep reinforcement learning.

**Overall strategy:** The authors formulate the UAV swarm coordination problem as a Partially Observable Markov Decision Process (POMDP) within a mean-field game framework. They design the PO-WMFDDPG algorithm, implement it in simulation, train it on a 80-drone scenario, and then systematically test its performance under increasing drone counts, increasing no-fly zone counts, and moving no-fly zones. All results are compared against two baselines (DDPG and MFDDPG) to isolate the contribution of each algorithmic innovation.

---

## The Environment

**Simulation environment:** 500 × 500 meter 2D battlefield (a top-down overhead view of a flight space)

**Obstacles:** 20 circular No-Fly Zones (NFZs) randomly distributed in the environment. In most experiments these are static; one experiment tests moving NFZs.

**Agents:** 80 UAVs (primary experimental scale). Each starts at a random position and has an assigned target.

**Coordinate system:** 2D (x, y) position with a heading angle α and speed v. The problem is simplified to 2D horizontal flight — vertical (altitude) dynamics are not modeled.

**Primary experiment:** 80 UAVs, 20 static NFZs, 500×500m space.

**Comparison baselines:**
- **DDPG** — standard single-agent DDPG adapted to multi-agent, no mean-field interaction modeling
- **MFDDPG** — mean-field DDPG with global (non-weighted, non-partial) mean field across all agents

---

## POMDP Formulation

The problem is modeled as a POMDP because each drone cannot observe the full swarm — only drones within communication range R_a.

**Formal definition:** (N, S, O, A, R, P, γ)
- N = number of agents (UAVs)
- S = true global state space
- O = partial observation space per agent
- A = continuous action space
- R = reward function
- P = state transition probability
- γ = discount factor (0.98)

### State Space (Observation) — 16 dimensions total

Each UAV observes three components:

**Component 1: Self-state I_uav** (4 dimensions)
| Variable | Meaning |
|----------|---------|
| x | UAV's x-coordinate in environment |
| y | UAV's y-coordinate in environment |
| v | Current flight speed |
| α | Current heading angle |

**Component 2: Task information I_task** (2 dimensions)
| Variable | Meaning |
|----------|---------|
| d | Distance from UAV to its assigned target |
| β | Angle between UAV heading and direction to target |

**Component 3: Threat detection I_detect** (up to 10 dimensions = 5 threats × 2 values)

For each detected NFZ within sensor range (up to 5 NFZs):
| Variable | Meaning |
|----------|---------|
| d_i | Distance from UAV to NFZ i |
| β_i | Angle between UAV heading and direction to NFZ i |

**Total state dimension: 4 + 2 + 5×2 = 16**

---

### Action Space — 2 dimensions (continuous)

| Variable | Meaning | Range |
|----------|---------|-------|
| a_v | Linear acceleration (speed change) | [a_min, a_max] |
| a_α | Angular acceleration (heading change) | [a_min, a_max] |

Both are continuous values. This is why DDPG (not DQN) is used — DQN only handles discrete actions.

---

### Reward Function

The reward has two components:

**Long-term rewards (sparse — only triggered by terminal events):**
- r_goal: positive reward for reaching the target
- r_bound: negative penalty for leaving the 500×500m boundary
- r_crash: negative penalty for entering an NFZ or colliding with another UAV

**Instant reward (dense — computed at every step):**

```
r_task = λ(1 − d_{t+1}/d_t) + η·cos(β_t)
```

Variable definitions:
- d_t = distance from UAV to target at current timestep
- d_{t+1} = distance from UAV to target at next timestep
- β_t = angle between current heading and direction to target
- λ = weight for distance progress component
- η = weight for heading alignment component

**How r_task works:**
- The term (1 − d_{t+1}/d_t): if d_{t+1} < d_t, the UAV got closer to target → value is positive (up to 1.0). If the UAV moved away, value is negative.
- The term cos(β_t): equals 1.0 when UAV is flying directly toward target; equals 0 when flying perpendicular; equals −1 when flying directly away.
- Together: the drone gets a meaningful reward signal every single step — rewarding both getting closer AND facing the right direction. No sparse reward problem.

---

## Mean Field Computation

This is the algorithmic core. For each UAV i at timestep t:

**Step 1: Identify neighbors.**
Find all UAVs j ≠ i that are within communication range R_a of UAV i.

**Step 2: Compute attention weights.**
For each neighbor j, compute attention weight w_{ij} using the multi-head attention module:
- The attention module takes neighbor state features as keys and the current agent's state as query
- 4 attention heads, 32-dimensional key/query vectors
- Output: a weight w_{ij} for each neighbor, summing to 1 across all neighbors

**Step 3: Compute weighted mean field.**
```
ā_i^t = Σ_j w_{ij} · a_j^t
```
Where:
- ā_i^t = mean field action (the weighted average of all visible neighbors' actions)
- w_{ij} = attention weight for neighbor j (higher = more influential)
- a_j^t = action taken by neighbor j at time t

**Result:** Each UAV replaces tracking N individual neighbors with responding to one 2-dimensional mean field vector ā_i^t.

---

## Neural Network Architecture

### Actor Network (Decision maker — what action to take)

```
Input: 16-dim state
       ↓
Hidden Layer 1: 64 neurons, ReLU activation
       ↓
Hidden Layer 2: 128 neurons, ReLU activation
       ↓
Hidden Layer 3: 32 neurons, ReLU activation
       ↓
Output: 2 neurons (a_v, a_α), Tanh activation
```

Tanh activation on output constrains actions to [−1, +1] range, which is then scaled to the actual [a_min, a_max] range.

### Critic Network (Evaluator — how good was that action)

```
Input: 20-dim concatenated vector
       [state (16) + action (2) + mean_field_action (2)]
       ↓
Hidden Layer 1: 64 neurons, ReLU
       ↓
Hidden Layer 2: 192 neurons, ReLU
       ↓
Hidden Layer 3: 64 neurons, ReLU
       ↓
Output: 1 neuron (Q-value estimate)
```

Note: The critic takes the mean field action as input — this is what makes it a mean-field critic rather than a standard DDPG critic.

### Target Networks
Both actor and critic have separate target networks updated via soft update:
```
θ_target ← τ·θ_main + (1−τ)·θ_target
```
where τ is small (typically 0.005), ensuring stable learning targets.

---

## Training Algorithm (PO-WMFDDPG Step by Step)

```
INITIALIZATION:
  - Initialize actor network μ_θ and critic network Q_φ with random weights
  - Initialize target networks μ_θ' and Q_φ' with same weights
  - Initialize replay buffer D (capacity = buffer_size)
  - Set hyperparameters: lr=0.005, γ=0.98, batch=128, τ=0.01

FOR each training round (1 to 1,000):
  FOR each episode step:

    1. Each UAV i observes local state s_i (16-dimensional)
    
    2. Each UAV computes neighbors within R_a
       → Compute attention weights w_{ij} via multi-head attention
       → Compute mean field: ā_i = Σ_j w_{ij}·a_j
    
    3. Each UAV selects action:
       a_i = μ_θ(s_i) + OU_noise  (add Ornstein-Uhlenbeck exploration noise)
    
    4. All UAVs execute actions → environment transitions to next state
       → Compute reward r_i for each UAV
    
    5. Store transition (s_i, a_i, ā_i, r_i, s_i') in replay buffer D
    
    6. IF buffer has enough samples:
       → Sample random mini-batch of 128 transitions
       → Compute target Q-value: y = r + γ·Q_φ'(s', μ_θ'(s'), ā')
       → Update critic by minimizing: L = (Q_φ(s,a,ā) − y)²
       → Update actor using policy gradient:
          ∇J = E[∇_a Q_φ(s,a,ā)|_{a=μ_θ(s)} · ∇_θ μ_θ(s)]
       → Soft update target networks

  END episode
END training
```

**OU Noise (Ornstein-Uhlenbeck noise):** Temporally correlated exploration noise — unlike random Gaussian noise, OU noise is smooth over time, which is better for physical systems like UAVs that cannot change direction instantly.

---

## Hyperparameters Table

| Hyperparameter | Value | Purpose |
|----------------|-------|---------|
| Training rounds | 1,000 | Total training episodes |
| Discount factor γ | 0.98 | Long-term reward weighting (high = plans far ahead) |
| Learning rate | 0.005 | Speed of neural network parameter updates |
| Batch size | 128 | Samples per training step from replay buffer |
| Soft update τ | 0.01 | Rate of target network parameter blending |
| Attention heads | 4 | Multi-head attention heads for mean field weighting |
| Attention key dim | 32 | Dimension of attention key/query vectors |
| UAVs (primary) | 80 | Main experimental agent count |
| NFZs (primary) | 20 | Main experimental obstacle count |
| Environment | 500×500m | Flight space dimensions |

---

## Experimental Setup (All Tests Run)

**Experiment 1: Convergence and baseline comparison**
- 80 UAVs, 20 NFZs, 500×500m
- Compare: PO-WMFDDPG vs. DDPG vs. MFDDPG
- Metric: Task success rate (SR) over 1,000 training rounds
- Result: PO-WMFDDPG converges to ~98% SR by round 700

**Experiment 2: UAV scalability test**
- Vary UAV count: 20 → 40 → 60 → 80 → 100 → 120
- Fixed: 20 NFZs
- Metric: SR at each drone count
- Result: PO-WMFDDPG maintains >90% SR at 120 UAVs; DDPG and MFDDPG collapse earlier

**Experiment 3: NFZ scalability test**
- Vary NFZ count: 10 → 20 → 26 → 30 → 36 → 40+
- Fixed: 80 UAVs
- Metric: SR at each NFZ count
- Result: PO-WMFDDPG stable to ~36 NFZs; DDPG collapses after 26 NFZs

**Experiment 4: Moving NFZ test**
- 80 UAVs, NFZs move at random velocities
- Metric: How many UAVs complete the mission
- Result: 75/80 UAVs succeed (5 fail to evade moving NFZs)

---

## Full Pipeline Diagram

```
┌─────────────────────────────────────────────┐
│          TRAINING ENVIRONMENT               │
│  500×500m battlefield, 80 UAVs, 20 NFZs    │
└──────────────────────┬──────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────┐
│         PARTIAL OBSERVATION                 │
│  Each UAV observes only within range R_a    │
│  State: 16-dim [I_uav + I_task + I_detect]  │
└──────────────────────┬──────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────┐
│      MULTI-HEAD ATTENTION MODULE            │
│  Input: neighbor state features             │
│  4 heads, 32-dim keys/queries               │
│  Output: attention weights w_{ij}           │
└──────────────────────┬──────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────┐
│      WEIGHTED MEAN FIELD COMPUTATION        │
│  ā_i = Σ_j w_{ij} · a_j                   │
│  (weighted average of neighbor actions)     │
└──────────────────────┬──────────────────────┘
                       │
              ┌────────┴────────┐
              ▼                 ▼
┌─────────────────┐    ┌─────────────────────┐
│  ACTOR NETWORK  │    │   CRITIC NETWORK     │
│ 16→64→128→32→2  │    │ 20→64→192→64→1      │
│ Outputs (a_v,aα)│    │ Inputs: s, a, ā_i   │
│ + OU noise      │    │ Outputs: Q-value     │
└────────┬────────┘    └─────────────────────┘
         │                       │
         ▼                       ▼
┌─────────────────────────────────────────────┐
│           REPLAY BUFFER (D)                 │
│  Stores (s, a, ā, r, s') tuples            │
│  Random sampling for training               │
└──────────────────────┬──────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────┐
│         NETWORK UPDATES                     │
│  Critic: minimize TD error                  │
│  Actor: maximize Q via policy gradient      │
│  Target networks: soft update (τ=0.01)      │
└──────────────────────┬──────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────┐
│    TRAINED POLICY → DEPLOYMENT              │
│  Each UAV runs its local actor network      │
│  No central controller needed (CTDE)        │
│  98% task success rate, 80 UAVs             │
└─────────────────────────────────────────────┘
```
