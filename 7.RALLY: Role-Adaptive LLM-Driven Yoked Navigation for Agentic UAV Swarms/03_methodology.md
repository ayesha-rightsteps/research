# 03 — Methodology: What the Researchers Did, Step by Step

---

## Research Design

**Type of study:** This is an experimental study combining algorithmic design, mathematical analysis, and empirical simulation validation.

**Overall strategy:** The authors design a novel hybrid framework (RALLY) and validate it through two complementary simulation environments: a lightweight 2D particle simulation (MPE) for controlled comparison experiments, and a high-fidelity 3D physics simulator (Gazebo-ROS-PX4 SITL) for real-world viability testing. The study also includes ablation experiments to isolate the contribution of each component.

The research is organized in three phases:
1. **Framework design:** Define the DS-CEFC task formally, then build RALLY's two core modules (LLM consensus reasoning + RMIX role assignment)
2. **Training and fine-tuning:** Collect offline data using GPT-4o, train RMIX, and fine-tune a lightweight local LLM for deployment
3. **Evaluation:** Compare against three baselines, test generalization, perform ablation studies, and validate in SITL

---

## The Data

**Simulation environments used:**
- **Multi-Agent Particle Environment (MPE):** A standard 2D continuous-space simulator for multi-agent research. No real-world dataset — the environment generates interactions dynamically.
- **Gazebo-ROS-PX4 SITL:** A full 3D physics simulation with actual PX4 autopilot firmware, ROS communication middleware, and quadrotor dynamics. Again, no external dataset — the environment generates physics-based interactions.

**Offline LLM training data:**
- Collected by running GPT-4o (via API) in the MPE environment with 8 agents
- GPT-4o's role suggestions and navigation decisions are recorded as training samples
- A filtering mechanism retains only high-quality samples based on four criteria:
  1. The suggested target region must belong to the valid target set
  2. The inference content must not contain anomalous symbols
  3. The inference length must fall within bounds [Lmin=-3000, Lmax=400] tokens
  4. The reward achieved must meet a quality threshold tau_r = 200
- **Final filtered dataset size:** 8,231 high-quality samples (|B_fil| = 8,231)
- This dataset is used to fine-tune Qwen2.5 models via LoRA

**Few-shot corpus:** 50 manually labeled examples created by the authors to serve as the few-shot corpus for guiding GPT-4o's data generation (rho = 1 few-shot sample used per inference during data collection)

**Why this data is appropriate:** Since DS-CEFC is a novel simulated task with no existing real-world dataset, generating training data from GPT-4o's zero-shot capability is a practical and principled approach. The filtering step ensures only valid, high-reward demonstrations reach the fine-tuning stage.

---

## The Methods

### Method 1: Three-Layer Hierarchical Policy Architecture

**What it does:** Divides the UAV control problem into three levels:
- **High-level policy (πH):** Infers consensus navigation goals (which target to fly to) — this is RALLY's domain
- **Mid-level policy (πM):** Handles obstacle avoidance and formation maintenance using MARL-based navigation
- **Low-level policy (πL):** Controls raw flight dynamics using a PID (Proportional-Integral-Derivative) controller

**Why it is used:** Separating concerns makes each level simpler to design and optimize. The paper assumes πM and πL are already available from prior work (reference [2], CIHRL) and focuses entirely on learning πH — the high-level navigation goal consensus.

**How it fits:** RALLY is the πH module. Its output (target region consensus) feeds into πM, which translates it into obstacle-avoiding trajectories, which πL then executes as rotor commands.

---

### Method 2: Two-Stage LLM-Based Consensus Inference (LLMHC)

This is RALLY's first core module. It operates in two sequential steps every 50 simulation steps.

**Stage 1: Intention Generation (LLMinit)**

Each drone independently generates an initial navigation intention.

The inputs to LLMinit are:
- **Xtask (Background Prompt):** Describes the mission — "8 collaborating nodes, 1 mobile enemy node, 2 target points. Mission: evade attacks and cover target areas in clusters of 3 or more."
- **Yinit(oi^t) (Observation Prompt):** Describes this specific drone's current situation in natural language — current position, teammates' positions within range, out-of-range teammates count, enemy position and velocity
- **MCoT (Chain-of-Thought Guide):** Structured reasoning instructions including: "Analyze the relationship between you and neighbors based on the definition," "Analyze enemy threats based on enemy's position and velocity," "Scoring point coverage needs cluster with other two teammates," "Cluster or disperse based on the threats from enemy"

The LLM outputs a natural language decision, for example: "My priority is 1, next target point is [-8,8]." This is parsed into a numeric coordinate g'i^t.

**Stage 2: Neighborhood Consensus Refinement (LLMcons)**

After Stage 1, each drone broadcasts its initial intention and role to neighbors within communication range (delta_obs = 3 meters in simulation). The drone then constructs a new prompt Ycons that includes:
- Its own current position and role
- Neighbors' roles and their preferred targets
- Enemy's position and velocity
- The same Xtask and MCoT

The LLM refines its decision given this broader context and outputs: "I recommend going to the destination point [-8, 8]." which is parsed into the final numeric consensus goal gi^t.

**Handling illegal LLM outputs (robustness mechanism):**
- Commander: maintains its initial intention
- Coordinator: defers to a valid Commander's decision; if none, reverts to its own
- Executor: follows any available Commander or Coordinator

**Theorem 1 (Two-Stage Superiority):** The paper proves mathematically that under monotonic value factorization (Assumption 1) and the property that additional context improves Q-values (Assumption 2), the two-stage policy always achieves strictly higher expected cumulative return than a one-stage policy.

---

### Method 3: RMIX-Based Role Assignment (RLHI)

This is RALLY's second core module — the credit-assignment mechanism for dynamic role selection.

**The problem it solves:** In a team of 8 drones, each choosing from 3 roles, there are 3^8 = 6,561 possible joint role combinations. Combined with sparse adversarial rewards and the high inference latency of LLMs, purely online exploration of this space is impractical.

**The solution — Hybrid Offline-Online Training:**

**Phase 1: Offline Data Collection via GPT-4o**
- Run GPT-4o via API in the MPE environment for N_pre episodes
- At each step, GPT-4o assigns a role to each drone based on its local observation
- Store the experience tuple (state s, observations {oi}, GPT-assigned roles {kiGPT}, reward R, next state s') in a replay buffer BR
- This seeds the buffer with sensible role assignments, eliminating the cold-start problem

**Phase 2: Online Cooperative RMIX Training (Algorithm 1)**
- Each drone has its own MLP (parameterized by theta) that maps its local observation to Q-values for each of the 3 roles
- The drone selects the role with the highest Q-value: ki^t = argmax_k Qi(oi^t, k)
- All drones' Q-values [Q1, Q2, ..., QN] are aggregated into a global value Q_tot via the RMIX mixing network
- The mixing network enforces non-negative weights (via ReLU activations) to satisfy the monotonic value factorization constraint
- Training minimizes the squared temporal difference error between Q_tot and target values y_tot = R^t + gamma_rmix * max_k' Q_bar(s', k'; theta_bar)
- Target network parameters theta_bar are updated with soft updates at rate tau = 0.01

**RMIX Network Architecture:**
- Two-layer MLP with hidden dimension E = 128
- Weight vectors W1 (E x N) and W2 (E x 1), biases b1 (E x 1) and b2 (scalar)
- All weights constrained to be non-negative via ReLU
- Trained with batch size 256, learning rate alpha = 1e-5, discount factor gamma_rmix = 0.95

**Equation explained — Qtot:**
Q_tot = ReLU(W2^T * (ReLU(W1 * Q^t + b1)) + b2)

This computes a weighted combination of individual role-value estimates. Because all weights are non-negative, increasing any drone's individual Q-value cannot decrease the global Q_tot — this is the monotonicity guarantee.

---

### Method 4: Context-Based LLM Fine-Tuning (Capacity Migration)

**Why it is needed:** GPT-4o provides excellent reasoning quality but requires internet API access, has high latency, and is impractical for onboard UAV deployment. A smaller local model is needed.

**The process (Algorithm 2):**

1. **Data generation:** Call GPT-4o API to generate navigation decisions and reasoning chains for DS-CEFC scenarios. For each observation, GPT-4o outputs a navigation decision g*i and intermediate reasoning text I*i.

2. **Quality filtering:** Apply the Check function to retain only samples where:
   - The target g*i belongs to the valid target set (weight w1,g = 0.45)
   - The reasoning text I*i contains no anomalous symbols (weight w2,g = 0.25)
   - The reasoning length is within [-3000, 400] tokens (weight w3,g = 0.2)
   - The achieved reward R >= tau_r = 200 (weight w4,g = 0.1)
   - Result: 8,231 high-quality samples retained

3. **Fine-tuning via LoRA:** Use LLaMA-Factory with LoRA to fine-tune Qwen2.5 models (tested at 0.5B, 1.5B, 3B, 7B parameters). Minimize MSE loss between model outputs and GPT-4o reference answers.

4. **Model selection:** Qwen2.5-1.5B is chosen as the deployment model — 2.9 GB memory footprint, 14.48 seconds average inference time, 4.13 GB runtime overhead on NVIDIA RTX 4090. This fits within onboard UAV GPU constraints.

---

## The Experiments

### Experiment 1: Overall Performance Comparison (Figure 6)

**What was tested:** RALLY vs. three baselines on the DS-CEFC task
**Baselines:**
- **CIHRL [2]:** State-of-the-art MARL approach with multi-agent communication, no role assignment — represents the best pure MARL baseline
- **CoNavGPT [30]:** LLM-based global planner with no training — represents the pure LLM baseline
- **DITTO [51]:** LLM with fixed role-based heterogeneity — represents an LLM+roles baseline without online learning

**Metric:** Average reward over 30 test episodes (higher = better; rewards are negative due to heavy collision/interference penalties)
**Setup:** 8 UAVs, 1,000 steps per episode, target selection every 50 steps, 8 NVIDIA RTX 4090 GPUs

---

### Experiment 2: Generalization to Different Swarm Sizes (Figure 9)

**What was tested:** RALLY vs. CIHRL with swarm sizes of 8, 9, 10, and 11 UAVs
**Why this matters:** Models are trained on 8 UAVs. Testing on 9-11 reveals how well each approach generalizes to unseen configurations.

---

### Experiment 3: Generalization to Different Target Configurations (Figure 10)

**What was tested:** RALLY across three target area layouts: 3x3 grid (original), 2x4 grid, and 4x2 grid
**Why this matters:** Real missions involve variable target distributions; consistent performance across layouts validates RALLY's environmental adaptability

---

### Experiment 4: RMIX vs. VDN Ablation (Figure 7)

**What was tested:** RMIX mixing network vs. VDN (Value Decomposition Network, a simpler aggregation method that sums individual values linearly: Q_tot = sum(wi * Qi))
**What this shows:** Whether the more complex RMIX architecture is justified over the simpler VDN baseline

---

### Experiment 5: Role Number Ablation (Figure 12)

**What was tested:** RALLY's performance with 1, 2, 3, and 4 roles:
- 1 role: Executor only
- 2 roles: Commander + Executor
- 3 roles: Commander + Coordinator + Executor
- 4 roles: Commander + Coordinator + Executor + Decoy (designed to divert enemy attention)

---

### Experiment 6: LLM Fine-Tuning Performance (Figures 13, 14; Table 3)

**What was tested:** Performance after fine-tuning Qwen2.5 at 0.5B, 1.5B, 3B, 7B parameters; comparison with non-fine-tuned base model and direct API-GPT-4o
**Table 3 metrics:** Average Inference Time (s), Memory Footprint (GB), Runtime Overhead (GB) on NVIDIA RTX 4090

---

### Experiment 7: SITL Validation (Figures 15-17)

**What was tested:** RALLY integrated into a full Gazebo-ROS-PX4 SITL environment with 8 physical quadrotor simulations
**Platform details:** Gazebo-Classic physics simulator + ROS communication middleware + PX4 autopilot firmware + MAVROS command interface + Newton-Euler quadrotor dynamics
**Communication:** Each UAV publishes state and sensor data via ROS topics; subscribes to peer updates; RALLY consensus output converted to horizontal accelerations broadcast to PX4 via ROS; PX4 connected to Gazebo via TCP

---

## Pipeline Diagram

```
[Environment Initialization]
         |
         | Each drone receives local observation oi^t:
         | - Own position and velocity
         | - Enemy position and velocity
         | - Target positions and urgency levels
         v
[STAGE 1: Intention Generation]
         |
         | LLMinit(Xtask, Yinit(oi^t), MCoT)
         | → Each drone independently generates
         |   initial target intention g'i^t
         |
         | Simultaneously:
         | RMIX Role Selection Policy RLHI(oi^t, g'i^t)
         | → Assigns role ki^t to each drone
         |   (Commander / Coordinator / Executor)
         v
[NEIGHBORHOOD COMMUNICATION]
         |
         | Each drone broadcasts (g'i^t, ki^t, oi^t)
         | to neighbors within delta_obs = 3m
         | Receives neighbors' (g'j^t, kj^t, oj^t)
         | → Constructs combined local information zi^t
         v
[STAGE 2: Consensus Refinement]
         |
         | LLMcons(Xtask, MCoT, Ycons(zi^t))
         | → Each drone refines target intention
         |   into final consensus goal gi^t
         v
[CONSENSUS OUTPUT: Target Region Gt]
         |
         | High-level policy outputs navigation goals
         | for all drones
         v
[MID-LEVEL POLICY (πM)]
         |
         | MARL-based formation + obstacle avoidance
         | Translates target goals into desired
         | horizontal accelerations u = [ux, uy]
         v
[LOW-LEVEL POLICY (πL)]
         |
         | PID flight controller (PX4)
         | Converts accelerations to thrust and
         | rotor commands
         v
[UAV EXECUTES ACTION → NEW OBSERVATION]
         |
         | Receive reward R^t, advance to t+1
         | Store (s^t, {ki^t}, R^t, s^(t+1)) in buffer BR
         v
[RMIX TRAINING UPDATE]
         |
         | Sample batch from BR (offline + online)
         | Compute Q_tot via mixing network
         | Minimize TD-error loss L(theta)
         | Soft update target network theta_bar
         v
[REPEAT EVERY 50 SIMULATION STEPS]
```

**Parallel track — LLM Fine-Tuning Pipeline:**

```
[GPT-4o API Calls on MPE Environment]
         |
         | Generate (oi, ki, g*i, I*i, R) samples
         v
[Quality Filtering: Check Function]
         |
         | Retain samples where target is valid,
         | reasoning is clean, length is appropriate,
         | and reward meets threshold
         | → |B_fil| = 8,231 samples
         v
[LoRA Fine-Tuning of Qwen2.5 via LLaMA-Factory]
         |
         | Minimize MSE between model output
         | and GPT-4o reference decisions
         | Validation convergence at step 500
         v
[Deployed on SITL: Qwen2.5-1.5B]
         |
         | 2.9 GB memory, 14.48s inference,
         | runs on onboard UAV GPU
```
