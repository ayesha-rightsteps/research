# Methodology — What the Researchers Did, Step by Step

---

## Research Design

**Type of study:** Simulation-based experimental study with ablation analysis.

**Overall strategy:** The authors designed a new multi-agent deep reinforcement learning algorithm (IGAT-MARL) and evaluated it systematically in a controlled simulation environment. They compared it against four existing graph-based MARL approaches, conducted ablation studies to isolate the contribution of individual components (curriculum learning, attention depth), and tested scalability from 3 to 10 UAVs.

There are no real-world drone flights. Everything is done inside the **BlueSky** open-source air traffic simulator, making the research reproducible and safe to test at scale.

---

## The Data

**Dataset used:** BADA (Base of Aircraft Data) from EuroControl.

**Source:** EuroControl, a European organisation for the safety of air navigation. BADA is a standard industry dataset widely used in air traffic management research.

**Format and content:** BADA provides detailed aerodynamic and performance parameters for aircraft models — including small fixed-wing aircraft that closely resemble fixed-wing UAVs. Parameters include speed envelopes, climb rates, turn constraints, and fuel consumption models.

**Role in the paper:** BADA data is integrated into the BlueSky simulator to give UAV agents realistic physical flight constraints. Without BADA, the simulation would be abstract and the results might not transfer to real-world conditions. With BADA, each UAV behaves like a real fixed-wing aircraft.

**Training volume:** Models were trained for 10,000 episodes, with swarm sizes from 3 to 10 UAVs. Each episode is a complete flight scenario where UAVs are placed in the airspace with guaranteed conflicts and must navigate to their goals.

**Preprocessing:** The raw UAV state (latitude, longitude, heading, calibrated airspeed, altitude) is normalized before being fed to the network. Specifically, latitude is divided by 100, longitude by 100, heading is divided by 180 and shifted by −1 to center it, and speed is converted to Mach number using altitude-dependent formulas. This normalization ensures inputs are in a consistent numerical range for stable neural network training.

**Why this data is appropriate:** Using a physics-based simulator with real aircraft performance data ensures the results are grounded in realistic flight dynamics. This is far more representative of actual UAV behavior than toy grid-world environments.

---

## The Methods

### Step 1: Environment Setup — BlueSky Simulator

**What it does:** BlueSky is an open-source Air Traffic Control simulator. At each simulation time step (Δt_sim), it moves all UAVs according to their current heading and speed, checks for conflicts using look-ahead conflict detection, and computes DCPA (distance at closest point of approach) and TCPA (time to closest point of approach) for every pair of UAVs.

**Why used:** BlueSky is an established, validated, open-source simulator with realistic physics. It is the same tool used in the primary baseline (Isufaj et al., 2022), enabling fair comparisons.

**How it fits the pipeline:** BlueSky acts as the environment. The MARL controller communicates with it by sending discrete heading instructions every K simulation steps.

---

### Step 2: State Representation — Local Observation Vector

**What it does:** Each UAV receives its own local observation vector:

  o_i^t = [latitude/100, longitude/100, heading/180 − 1, Mach(speed, altitude)]

This is a 4-dimensional vector describing the drone's current position, normalized heading, and speed as a Mach number.

**Why this design:** The observation is local — each UAV only sees its own state, not the full global state. This is realistic (drones have onboard sensors) and matches the decentralized nature of the problem (no central authority knows everything).

**How it fits:** The observation vector is the input to each UAV's encoder, which transforms it into a node embedding used by the IGAT network.

---

### Step 3: Dynamic Conflict Graph Construction

**What it does:** At each decision step t, the simulator provides the set of conflict pairs C^t — all pairs (i,j) where DCPA^t_ij < RPZ within the look-ahead horizon. The system builds an adjacency matrix A^t where A^t_ij = 1 if (i,j) is a conflict pair, and 0 otherwise. The diagonal is always 0 (no self-loops). The graph changes every step as conflicts appear and resolve.

**Why this design instead of distance-based graphs:** Distance-based graphs connect all UAVs within a fixed radius, which grows dense and noisy as the swarm grows. Conflict-driven graphs only connect pairs that are actually on a collision course — keeping the graph sparse, focused, and safety-relevant regardless of swarm size.

**Mathematical example from the paper:** If N=5 and C^t = {(1,3), (2,5)}, the adjacency matrix has 1s only at positions [1,3], [3,1], [2,5], [5,2] — all other entries are 0. This is a very sparse graph. At the next step if C^{t+1} = {(1,2)}, the matrix completely changes to reflect only that new conflict.

**How it fits:** A^t is the structural input to the IGAT network, determining which message-passing edges are active in the attention computation.

---

### Step 4: IGAT Network Architecture — Encoding and Attention

**What it does:** The IGAT (Improved Graph Attention Network) processes the node embeddings and the conflict graph through two stacked IGAT blocks. Each block contains two GAT layers in sequence, each followed by residual connection and layer normalization. Here is the step-by-step computation inside one GAT layer:

**4a. Linear Transformation**
Each UAV's node feature h_i is multiplied by a learnable weight matrix W to produce a transformed feature h_i^(W) = W * h_i. This projects the raw embedding into the attention space.

**4b. Pairwise Attention Energy**
For every conflict pair (i,j) in the graph, a "conflict energy score" is computed:
  e_ij = LeakyReLU( a^T * [h_i^(W) || h_j^(W)] )
where a is a learnable vector and || means concatenating the two transformed features. LeakyReLU is an activation function that handles both positive and negative values (unlike regular ReLU which kills negatives). This score measures how important drone j is to drone i.

**4c. Masked Attention**
Non-neighboring nodes (pairs not in conflict) are masked to negative infinity, so their softmax attention weight becomes zero. Only conflict pairs can influence each other.

**4d. Softmax Normalization**
The attention scores for all active neighbors are normalized using softmax, producing attention weights α_ij that sum to 1 for each drone i. These weights represent "how much attention drone i should pay to drone j."

**4e. Message Aggregation**
Each drone's new representation is computed as a weighted sum:
  h'_i = Σ_{j ∈ N(i)} α_ij * h_j^(W)
This aggregates information from all conflict neighbors, weighted by their attention scores.

**4f. Multi-Head Attention**
The above process is run K times in parallel with different weight matrices. Each "head" learns a different aspect of the relationship. Outputs from all heads are concatenated to form a richer representation.

**4g. Residual Connection and Layer Normalization**
  h_i^IGAT = LayerNorm(h'_i + Res(h_i))
The original input is added back (residual connection) before applying layer normalization. This prevents information loss and stabilizes training.

**The "Double Attention" Design:** Two GAT layers are stacked within each IGAT block (GAT1 → LN → GAT2 → LN). Then two such blocks are stacked. This gives four total attention passes over the conflict graph, allowing the network to refine its understanding of conflict relationships progressively.

---

### Step 5: Q-Value Estimation and Action Selection

**What it does:** After the IGAT network produces a final embedding h_i^IGAT for each UAV, a linear "head" network maps this to Q-values for each action:
  Q_i(o_i^t) = W_q * h_i^IGAT + b_q

Each UAV has three possible actions:
- Action 0: maintain current heading (Δψ = 0°)
- Action 1: turn right 15° (Δψ = +15°)
- Action 2: turn left 15° (Δψ = −15°)

**Conflict-Gated Execution:** Heading commands are only sent to UAVs currently in a conflict. If a UAV is not in any conflict at time t, its heading is unchanged regardless of what its Q-values suggest. This prevents unnecessary maneuvers for conflict-free drones.

**Action Selection:** During training, epsilon-greedy selects either the greedy best action or a random action. During evaluation, always the greedy best action is selected.

---

### Step 6: Reward Design

**What it does:** Each UAV receives a reward at each step based on three components:

  r_i^t = −(heading deviation penalty) − (conflict count penalty) − (CPA proximity risk)

- **Off-track penalty:** −|ψ_i^t − ψ_i,ref| / ψ_max — penalizes deviating too far from a reference heading. This discourages unnecessary turns and encourages efficient routing.
- **Conflict count penalty:** −n_i^t — penalizes for each active conflict involving UAV i. More conflicts = bigger penalty.
- **CPA proximity risk:** A nonlinear term based on DCPA relative to RPZ. As two drones get closer (DCPA → 0), this penalty grows exponentially toward −1. The formula uses an exponential decay: −(1 − exp(1 − 1/sqrt(max(x_ij, ε)))) where x_ij = DCPA_ij / RPZ.

**Why this reward design:** The three-part reward balances safety (minimize conflicts and proximity risk) with efficiency (minimize heading deviations). Using the CPA-based nonlinear term ensures the reward signal is more informative than a simple collision count — it provides gradient signal even before a collision occurs.

**Team objective:** The learning objective is to maximize the expected discounted average team reward:
  max_θ J(θ) = E[Σ_{t=0}^{T} γ^t * (1/N) * Σ_{i=1}^{N} r_i^t]
This averages reward across all N agents, ensuring all drones share the same collective safety goal.

---

### Step 7: DQN Training Loop with Replay Buffer

**What it does:** The system uses an off-policy DQN training loop:
1. Each episode begins with a reset of the environment
2. At each step, IGAT computes Q-values for all agents using the current observations and conflict graph A^t
3. Actions are selected via epsilon-greedy
4. Conflict-gated heading commands are sent to BlueSky
5. The simulator steps forward, returning new observations, rewards, and updated adjacency A^{t+1}
6. The full transition (o^t, a^t, r^t, o^{t+1}, A^t, A^{t+1}) is stored in a replay buffer
7. A random minibatch is sampled from the replay buffer and used to compute TD loss and update the online network
8. Periodically, the target network (a delayed copy of the online network) is updated

**Why replay buffer:** Training on consecutive transitions introduces correlation that destabilizes learning. A replay buffer randomizes the training data, breaking correlations and stabilizing training.

**Why target network:** Using a separate "target" network to compute TD targets prevents the oscillation that arises when the same network is both updated and used to generate targets simultaneously.

---

### Step 8: Curriculum and Transfer Learning

**What it does:** Instead of training on 10 UAVs from the start, the curriculum:
- Stage 1: Train on 3 UAVs until convergence
- Stage 2: Initialize network with Stage 1 weights; train on 4 UAVs
- Stage 3: Initialize with Stage 2 weights; train on 5 UAVs
- ... continues up to 10 UAVs

This is curriculum learning (progressively harder tasks) plus transfer learning (carrying forward learned weights).

**Why this matters:** Dense MARL training is non-stationary — as each agent learns, the optimal policy for every other agent changes. Starting with 10 UAVs immediately produces an overwhelmingly complex, unstable learning problem with high rates of dangerous random exploration. Starting with 3 UAVs allows the system to first learn reliable conflict resolution in a manageable setting. Transfer learning then preserves these coordination skills as the swarm grows.

**Measured effect:** For N=4, curriculum+transfer (Curr+TL) improves early-stage reward by 280 points (~34%) and reduces LoS by 155 time steps (~38%) within the first 2000 training episodes.

---

## The Experiments

**Experiment 1: Scalability with increasing swarm size (N=3 to 10)**
Runs IGAT vs. DGN benchmark across all swarm sizes. Evaluates cumulative reward and t_loss learning curves over 10,000 episodes. Shows that IGAT's advantage over the benchmark grows as N increases.

**Experiment 2: Comparison against four graph-based baselines (N=5 and N=10)**
Compares IGAT against DGN (benchmark), MGAT, GRL, and MS-GRL in the same environment with identical observation/action spaces, reward functions, and replay buffers. Only the graph aggregation module differs.

**Experiment 3: Ablation on curriculum and transfer learning (N=4 to 10)**
Compares IGAT with Curr+TL vs. IGAT without Curr/TL, measured over the first 2000 training episodes. Quantifies how much of IGAT's performance comes from the training strategy vs. the architecture.

**Experiment 4: Ablation on attention depth (N=5)**
Compares three architectural variants: Full IGAT (2 layers per block, 2 blocks), IGAT 1-Layer (1 layer per block), and IGAT (1 IGAT block with 1 layer). Tests whether the stacked "double attention" design is necessary.

**Baselines compared against:**
- DGN (Isufaj et al., 2022) — primary benchmark, conflict-masked QKV attention
- MGAT — vanilla multi-head GAT (Velickovic et al., 2018)
- GRL — graph RL with multi-head dot-product attention (Li et al., 2024)
- MS-GRL — multiscale risk-fusion block with gated graph convolution (Li et al., 2025)
- IGAT (no curriculum/transfer) — architectural ablation

**Evaluation metrics:**
1. Cumulative Reward — overall policy quality
2. t_loss — total time steps in loss of separation (safety metric)
3. Action Bias — distribution of actions 0, 1, 2 (adaptability metric)
4. Number of Active Edges — interaction complexity (efficiency metric)

**Hardware and software:**
- Hardware: Ubuntu computer with NVIDIA A40 GPU
- Simulator: BlueSky (open-source ATC simulator)
- Aircraft model: BADA dataset (EuroControl) for fixed-wing UAVs
- IGAT specifications: 4 attention heads (H=4), hidden dimension 128, dropout 0.6, residual + LayerNorm, 2 IGAT blocks × 2 GAT layers each

---

## Pipeline Diagram

```
[BlueSky Simulator]
Scenario generator: place N UAVs with guaranteed conflict scenarios
        |
        v
[Conflict Detection]
Compute DCPA^t_ij and TCPA^t_ij for all UAV pairs
        |
        v
[Dynamic Graph Construction]
Build A^t: set A^t_ij = 1 if (i,j) ∈ conflict pairs C^t, else 0
Identify conflict-active agents (conf_ac set)
        |
        v
[Local Observation Encoding]
Each UAV i: encode o^t_i = [lat/100, lon/100, heading/180−1, Mach]
FC encoder → node embedding h^t_i ∈ R^d
        |
        v
[IGAT Block 1: Double Attention Pass]
GAT Layer 1: Pairwise energy → masked softmax → aggregate neighbors → residual + LayerNorm
GAT Layer 2: Second attention pass → residual + LayerNorm
        |
        v
[IGAT Block 2: Second Refinement Pass]
Same double-attention structure as Block 1
→ Final node embeddings h^IGAT_i per UAV
        |
        v
[Per-Agent Q-Head]
Q_i = W_q * h^IGAT_i + b_q
Three Q-values per UAV: Q(a=0), Q(a=1), Q(a=2)
        |
        v
[Action Selection]
ε-greedy: with prob ε → random action; else → argmax Q
Conflict-gated: only send commands to UAVs in conf_ac
Commands: 0° | +15° | −15° heading offset
        |
        v
[BlueSky Execution]
Apply heading commands → step simulator
Receive: new observations, rewards, updated A^{t+1}
        |
        v
[DQN Update]
Store (o^t, a^t, r^t, o^{t+1}, A^t, A^{t+1}) in replay buffer
Sample minibatch → compute TD loss → update online network
Periodically update target network (soft/hard copy)
        |
        v
[Curriculum Progression]
After N UAVs converge: transfer weights → retrain with N+1 UAVs
Repeat: 3 → 4 → 5 → 6 → 7 → 8 → 9 → 10 UAVs
        |
        v
[Evaluation]
Metrics: Cumulative Reward, t_loss, Action Bias, Number of Edges
Comparison: IGAT vs. DGN, MGAT, GRL, MS-GRL
```
