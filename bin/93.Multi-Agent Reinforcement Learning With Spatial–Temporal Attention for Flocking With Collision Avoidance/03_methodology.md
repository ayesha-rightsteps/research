# 03 — Methodology: What the Researchers Did

---

## Research Design

**Type of study:** Experimental simulation study with hardware-in-the-loop (HITL) validation.

**Overall strategy:** The authors design a new multi-agent reinforcement learning algorithm (STAAC) from scratch and validate it through: (1) a training comparison against 6 baseline methods, (2) zero-shot generalization tests across different fleet sizes, (3) ablation studies removing individual components, and (4) a high-fidelity HITL experiment using real flight hardware.

The study is entirely in simulation — no real outdoor flights were conducted — but the HITL stage significantly bridges the gap to real deployment.

---

## The Environment / Data

**No external dataset is used.** The environment is fully simulated using the authors' own kinematic models. Every episode generates fresh data.

**Simulation setup:**
- 2D flight environment (fixed altitude — drones fly in a horizontal plane)
- Training environment: rectangular area of 1200 m x 800 m
- Testing environment (typical scenario): rectangular area of 1200 m x 400 m
- 1 leader UAV follows a pre-planned path with random heading rate and acceleration changes
- n follower UAVs (variable; trained with n = 10) learn to flock with the leader
- m non-cooperative intruders (variable; trained with m = 15) fly on random pre-planned paths

**Episode structure:**
- Maximum 60 time steps per episode (each time step = 1 second)
- Leader heading rate randomly sampled from -5 to +5 degrees per step
- Leader forward acceleration randomly sampled from -1 to +1 m/s per step
- Intruder speeds randomly sampled from 10 to 15 m/s
- Initial positions of all entities randomly initialized each episode

**UAV physical parameters (from Table I):**
- Sensing range R_c = 100 m
- Safety radius R_s = 15 m
- Alert radius R_a = 50 m
- Max forward speed v_max = 18 m/s; Min forward speed v_min = 12 m/s
- Max heading rate omega_max = pi/12 rad/s
- Max forward acceleration u_max = 1 m/s²
- Undamped natural frequency mean omega-bar_n = 6.3 rad/s
- Damping ratio mean zeta-bar = 0.55
- Discount factor gamma = 0.95

**Training hardware:** NVIDIA RTX 3080 laptop GPU. Training converges in approximately 1,000 episodes (~4 hours wall-clock time for 5,000 episodes total).

---

## The Methods

### Step 1 — Problem Formulation as Dec-POMDP

The authors first frame the problem mathematically. They define:

**State:** The full system state at time t is all entities' 4-tuples (x, y, heading psi, speed v) stacked across the last 4 time steps:
s^t = union from tau=(t-3) to t of {leader state, all followers' states, all intruders' states}

**Observation (per follower i):** Each follower can only see within 100 m. Its stacked observation is:
o^t_i = union from tau=(t-3) to t of {leader state at tau, follower i's own state at tau, neighbor-followers' states at tau, neighbor-intruders' states at tau}

Why stack 4 frames? Because a single snapshot doesn't tell you which way an intruder is heading — you need a history to estimate velocity and trajectory.

**Action (per follower i):** A pair of continuous values:
a^t_i = (omega^t_i, u^t_i)
- omega^t_i is the heading rate setpoint, bounded by [-pi/12, +pi/12] rad/s
- u^t_i is the forward acceleration, bounded by [-1, +1] m/s²

**Kinematic model for each UAV:** The state evolves according to:
dx/dt = v * cos(psi) + noise_x
dy/dt = v * sin(psi) + noise_y
d(psi)/dt = heading dynamics (2nd-order system, stochastic parameters)
dv/dt = speed dynamics (linear model with stochastic average speed)

The noise terms follow normal distributions N(0, sigma^2) to simulate wind disturbances. This stochasticity means traditional model-based control is impractical, motivating model-free RL.

---

### Step 2 — Reward Function Design

The reward for follower i at time t is the sum of three terms:

**Term 1 — Leader following reward (r^lea):**
- If follower i is within safety radius of leader (rho^t_i <= R_s = 15 m): penalty of -P1 = -1000 (too close — collision risk)
- If follower i is in alert zone (15 m < rho^t_i <= 50 m): linear reward w1*(rho^t_i - R_a), pulling it to stay in range, w1 = 5
- If follower i is far from leader (rho^t_i > 50 m): penalty of -(rho^t_i - R_a), proportional to how far it drifted

**Term 2 — UAV-UAV collision avoidance reward (r^fol, summed over all j neighbor-followers):**
- If distance D^t_{i,j} <= 15 m: penalty of -P2 = -2000 (collision)
- If 15 m < D^t_{i,j} <= 50 m: linear penalty w2*(D^t_{i,j} - R_a), w2 = 10
- If D^t_{i,j} > 50 m: 0 (safe, no penalty)

**Term 3 — UAV-intruder collision avoidance reward (r^int, summed over all k neighbor-intruders):**
- Same structure as Term 2 but using P1 = 1000

The total reward: r^t_i = r^lea_{i,t} + sum_j(r^fol_{i,j,t}) + sum_k(r^int_{i,k,t})

The intuition: drones are pulled toward the ideal formation range (50-100 m from leader), pushed away from each other and intruders, and heavily penalized for actual collisions.

---

### Step 3 — Population-Invariant Network Architecture

This is the core technical innovation. The problem: each follower's observation has a variable number of neighbor-followers and neighbor-intruders. Standard neural networks need fixed input sizes.

**Solution: Entity Clustering + Local Spatial Attention (LSA) + Global Temporal Attention (GTA)**

#### 3a — Entity Clustering
Each follower partitions its observed entities into 4 groups:
1. **Self (ego-follower):** Always exactly 1 entity — the follower itself
2. **Leader:** Always exactly 1 entity
3. **Neighbor-followers:** Variable — 0 to (n-1) other followers within 100 m
4. **Neighbor-intruders:** Variable — 0 to m intruders within 100 m

Each group is handled by a separate LSA module. This is critical because each group plays a different role: the leader sets the direction, neighbor-followers are to be avoided, intruders are threats, and the ego provides self-awareness.

#### 3b — Local Spatial Attention (LSA)
For each group with variable membership, LSA computes a fixed-size spatial embedding.

**For neighbor-followers** (the math, explained in plain English):
1. Each neighbor-follower j's state is passed through an FC layer (128 neurons, ReLU): FC(xi^fol_{j,t})
2. An attention score beta^fol_{i,j,t} is computed as the dot product of follower i's own state with the FC-transformed state of follower j, scaled by the square root of the embedding dimension:
   beta = (xi_i)^T * W_fol * FC(xi_j) / sqrt(d_fol)
   - What this computes: how "relevant" is follower j to follower i right now? Followers heading on a collision course get high scores.
3. These scores are converted to attention weights alpha via softmax: alpha_{i,j} = exp(beta_{i,j}) / sum_j(exp(beta_{i,j}))
4. The spatial embedding e^fol_{i,t} = sum_j(alpha^fol_{i,j,t} * FC(xi^fol_{j,t}))

This is a weighted average of all neighbors' features, where the weights reflect their importance. Result: a fixed-size 128-dimensional vector, regardless of how many neighbors there are.

**The same process is applied to neighbor-intruders** (with separate learned weights W_int, also 128 neurons).

**For single-entity groups** (leader and ego-follower), LSA degenerates to a simple FC layer (64 neurons each) since there's only one entity and attention weight is trivially 1.

#### 3c — Global Temporal Attention (GTA)
After LSA, we have 4 spatial embeddings per group per time step (t-3, t-2, t-1, t). Total: 4 groups × 4 time steps = 16 LSA output vectors.

**Step 1: LSTM temporal feature extraction**
For each of the 4 groups, a separate LSTM layer processes the sequence of LSA embeddings across 4 time steps:
- Leader LSTM: 64 hidden units
- Ego-follower LSTM: 64 hidden units
- Neighbor-followers LSTM: 128 hidden units
- Neighbor-intruders LSTM: 128 hidden units

The LSTM equations follow the standard formulation: forget gate f, input gate l, output gate g, cell state C, and hidden state h. The hidden state h^lea_tau at each time tau summarizes the temporal information for the leader up to that point.

**Step 2: Concatenate across groups**
At each time step tau, the 4 groups' hidden states are concatenated into a global temporal embedding:
h^glo_{i,tau} = [h^lea_tau || h^ego_{i,tau} || h^fol_{i,tau} || h^int_{i,tau}]

**Step 3: Temporal attention**
Raw temporal scores are computed: beta^glo_{i,tau} = FC(h^glo_{i,tau})
Attention weights: alpha^glo_{i,tau} = softmax(beta^glo_{i,tau})
Final global embedding: v^t_i = sum_{tau=t-3}^{t} alpha^glo_{i,tau} * h^glo_{i,tau}

The intuition: some time steps carry more information than others — for example, the moment an intruder changed direction is more important than normal moments. GTA learns to upweight those critical moments.

---

### Step 4 — Policy Network (Actor)

Input: Local observation o^t_i
Processing: Pass through STAN(·) — the spatial-temporal attention network combining LSA + GTA
Output: v^t_i — a fixed-size global temporal attention embedding

Then: a^t_i = MLP(v^t_i)
- The MLP has 2 hidden layers, each with 256 neurons
- Output layer has 2 neurons (heading rate + forward acceleration), activated by tanh to bound outputs
- tanh maps to [-1, +1], which is then scaled to action bounds

---

### Step 5 — Value Network (Critic)

The critic operates during training only (centralized). It processes the global state s^t (all entities' information) and all agents' joint actions a^t = (a^t_1, ..., a^t_n).

Structure (same as actor + additional action encoder):
1. Global state passed through STAN(·): z^t_i = STAN(s^t)
2. Joint actions encoded: c^t_i = FC(a^t)
3. Q-value approximated: q^t_i = MLP(z^t_i || c^t_i)
   - MLP: 2 hidden layers of 256 neurons each; output: 1 neuron (Q-value), linear activation

Two separate critics Q1 and Q2 are maintained (for clipped double Q-learning).

---

### Step 6 — STAAC Training Algorithm

The full training loop (Algorithm 1 in the paper):

1. **Initialize** policy network (theta_mu), two critic networks (theta_Q1, theta_Q2), and their target network copies
2. **Initialize** replay buffer D with capacity N = 50,000 transitions

For each training episode (max 5,000 episodes):
  - Randomly initialize all entities in the environment
  - For each time step t = 1 to 60:
    a. Each agent selects action: a^t_i = mu(o^t_i) + exploration_noise, where noise ~ N(0, 0.5) decaying exponentially to N(0, 0.05)
    b. All agents execute joint actions; environment transitions to s^{t+1}
    c. Compute reward r^t_i using equation (9)
    d. Store tuple (s^t, o^t, a^t, r^t, o^{t+1}, s^{t+1}) in D
    e. Sample minibatch of N_b = 32 tuples from D
    f. Update both critics by minimizing MSE loss (equation 37) using clipped double Q target:
       y^t_i = r^t_i + gamma * min_{l=1,2} Q^-_l(s^{t+1}, smoothed_target_actions)
       Smoothed target: a~^{t+1}_j = mu^-(o^{t+1}_j) + clip(N(0,0.2), -0.5, 0.5)
    g. Every C = 2 steps: update actor using deterministic policy gradient (equation 36)
    h. Soft update target networks: theta^- <- 0.01*theta + 0.99*theta^-

Learning rates: Actor = 0.0001; Critic = 0.001

---

## Pipeline Diagram

```
TRAINING PHASE
==============

[Simulation Environment]
  One Leader + n Followers + m Intruders
         |
         | (each step t)
         v
[Each Follower i receives observation o^t_i]
  (4 frames: leader state, own state,
   neighbor-followers' states, neighbor-intruders' states)
         |
         v
[Entity Clustering]
  Split into 4 groups:
  Self | Leader | Neighbor-Followers | Neighbor-Intruders
         |
         v
[Local Spatial Attention (LSA)]
  For each group: FC -> scaled dot-product -> softmax -> weighted sum
  -> 4 fixed-size spatial embeddings (one per group, per time step)
         |
         v
[Global Temporal Attention (GTA)]
  4 separate LSTM networks (one per group) across 4 time steps
  -> Concatenate 4 groups -> h^glo (4 time steps)
  -> FC -> softmax (temporal weights alpha^glo)
  -> Weighted sum -> v^t_i (single fixed-size embedding)
         |
         v
[Policy Network (Actor) - DECENTRALIZED]
  MLP(v^t_i) -> action a^t_i = (heading rate, acceleration)
         |
         v
[Execute Action in Environment]
  -> New state s^{t+1}, reward r^t_i
         |
         v
[Replay Buffer] <- Store (s^t, o^t, a^t, r^t, o^{t+1}, s^{t+1})
         |
         v
[Sample Minibatch]
         |
  ┌──────┴──────────────┐
  v                     v
[Critic Update]    [Actor Update]
Clipped double Q   Policy gradient
(every step)       (every 2 steps)
         |
         v
[Soft Target Network Update]

EXECUTION PHASE
===============
Each follower independently:
  o^t_i -> LSA -> GTA -> MLP -> a^t_i
  (No communication, no global state, ~1.5 ms per decision)
```

---

## The Experiments

### Experiment 1: Training Comparison (7 algorithms)
**Baselines:**
1. MADDPG — classic centralized critic / decentralized actor RL
2. MATD3 — twin-delayed deep deterministic policy gradient for multi-agent
3. HAMA — hierarchical graph attention multi-agent RL
4. API-MADDPG — authors' own prior work (attention, no entity clustering, no GTA, no intruders)
5. BCDDPG — dueling double recurrent Q-learning for collision avoidance
6. LSTM-DDQN — discrete action collision avoidance with LSTM; only sees 2 closest followers and 1 closest intruder

**Environment:** 10 followers, 15 intruders, 1200 m × 800 m area

**Metric:** Average reward per episode (averaged over 10 episodes, plotted over 5,000 training episodes)

---

### Experiment 2: Generalization Testing (Zero-Shot)
**Scenarios:** n5m15, n10m15, n10m20
**Evaluation:** 100 episodes × 60 steps per scenario for all 7 RL methods + APF + ORCA
**Metrics:** Average reward G, collision rate F, average leader-follower distance rho-bar

---

### Experiment 3: Ablation Study
**Variants:**
- TAAC: GTA only (LSA removed, mean embedding used instead)
- SAAC: LSA only (GTA removed, all 4 time steps weighted equally)
- STAAC: Full method

**Scenarios:** 6 scenarios: n5m10, n5m15, n5m20, n10m10, n10m15, n10m20
**Evaluation:** 100 episodes × 60 steps each
**Metrics:** G, F, rho-bar

---

### Experiment 4: HITL Experiment
**Setup:** 5 followers (UAV11-UAV15) + 1 leader (UAV10) + 3 intruders (UAV21-UAV23)
**Hardware per node:** X-plane 10 simulator + Onboard computer (Ubuntu 16.04 LTS + ROS) + Pixhawk autopilot (PX4 stack) + QGroundControl
**Duration:** 100 time steps (seconds)
**Key test:** Policy learned from numerical simulation is applied directly — no parameter retuning
**Metrics:** Distances to leader (rho), minimum inter-follower distance (D^fol_min), minimum follower-intruder distance (D^int_min)
