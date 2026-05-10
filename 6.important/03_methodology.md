# 03 — Methodology: Exactly What the Researchers Did

---

## Research Design

**Type of study:** Simulation-based experimental study with mathematical formulation and algorithm design.

**Overall strategy:** The researchers (1) formulate the UAV multi-hop networking problem as a formal multi-objective optimization problem, (2) model it as a stochastic game that MARL can be applied to, (3) design the MRLMN framework with three novel modules, (4) implement it in simulation, and (5) rigorously compare it against five baselines across multiple environment scales and ablation conditions. There is no physical hardware involved — the entire evaluation is conducted in a custom simulation environment.

---

## The Data / Environment

There is no external dataset in the traditional machine-learning sense. Instead, the researchers generate simulation data on the fly using a custom environment. Here are the details:

**Simulation environment:**
- Area: approximately 3.5 km × 3.5 km (12.25 km²) for the main experiments, ranging from 6.76 km² to 14.44 km² in scaling experiments
- Users (UEs): approximately 150 user devices
- Drones (UAVs): 18 in main experiments, varying from 12 to 24 in scaling experiments
- Base stations: 3 BSs placed at three corners of the area, specifically positioned so UEs cannot connect directly

**UE mobility model:** Users move according to a Brownian motion process (random walk) at constant speed. Their spatial distribution follows either a uniform pattern or a two-dimensional Gaussian mixture model with multiple clusters. This simulates realistic survivor behavior — people are not evenly spread but are clustered around buildings, roads, and shelters, and they move around over time.

**UAV motion:** Each UAV can move at a fixed speed ω = 30 meters per time slot. It selects one of 9 discrete actions: 8 compass directions (N, NE, E, SE, S, SW, W, NW) or hover. UAVs must stay within the boundary of the environment.

**Communication frequencies and parameters (Table I in the paper):**
- System frequency: ~2.4 GHz
- BS-UAV link bandwidth: 7 MHz
- UAV-UAV link bandwidth: 5 MHz
- UAV-UE link bandwidth: 1 MHz
- UAV transmit power: 1 W; BS transmit power: 10 W; UE transmit power: 0.4 W
- NLoS excess path loss: 20 dB; LoS excess path loss: 1 dB
- Environmental constants a = 9.61, b = 0.16 (urban environment parameters)
- SNR threshold ρ_th: 25 dB
- Noise figure NF: 15 dB

**Why this setup is appropriate:** The parameter choices match real-world urban disaster scenarios. The 2.4 GHz frequency, bandwidth allocations, and path loss parameters are consistent with standard UAV communication modeling literature. Placing BSs at corners with no direct UE coverage forces genuine multi-hop relay behavior, which is exactly the problem being studied.

---

## The Methods

### Step 1: Problem Formulation as Optimization

The researchers define the goal formally: find the UAV trajectory set τ* that maximizes the time-averaged sum of (1) the proportion of connected UEs and (2) the average data rate across all UEs.

**The objective function (P1):**
τ* = argmax over τ of { (1/T) × Σ_t [ (1/M) × Σ_m c_m^UE(t) + κ × (1/M) × Σ_m r_m^UE(t) ] }

Breaking this down:
- (1/M) × Σ_m c_m^UE(t) = the fraction of users connected at time t (coverage term)
- κ × (1/M) × Σ_m r_m^UE(t) = the weighted sum of data rates at time t (quality term)
- κ = 0.025 when data rate is in Mbps, balancing coverage and quality numerically
- T = total time horizon; M = total number of UEs

**Constraints:**
- C1: Each UAV can move at most ∆l_u = ω × ∆t meters per time step (speed limit)
- C2: UAVs must stay within the spatial boundary of the environment
- C3: Connectivity constraints from equations (11) and (12)

**Connectivity rules (equations 11 and 12):**
A UAV is "connected" (c_u^UAV = 1) if it can reach a BS either:
- Directly: its SNR to any BS ≥ ρ_th, OR
- Via relay: there exists another connected UAV v whose SNR to u meets the threshold

A UE is "connected" (c_m^UE = 1) if there exists at least one connected UAV u whose SNR to the UE meets the threshold.

This recursive connectivity definition captures the multi-hop nature: a UAV is only valuable if its entire chain back to the BS is intact.

---

### Step 2: Stochastic Game Formulation

The optimization problem is reformulated as a stochastic game, which is the formal structure that MARL is designed to solve. The tuple is:

**(U, S, A, P, R, γ)**

- **U**: the set of UAV agents (e.g., 18 drones)
- **S (State space)**: includes (a) 3D coordinates of all nodes, (b) SNR and data rates of all links, (c) connectivity status of each UAV
- **A (Action space)**: 9 discrete movement options per UAV (8 directions + hover)
- **P (Transition probability)**: probabilistic state evolution given joint actions of all UAVs and random UE movement
- **R (Reward)**: defined per UAV via reward decomposition (see Step 4)
- **γ (Discount factor)**: balances immediate versus future rewards

---

### Step 3: Information Aggregation

**What it does:** Each drone cannot make good decisions using only its local view. To improve coordination, each drone shares its local observations with all others, and each drone's input to its policy network includes this shared aggregate.

**The shared information ξ(t)** comprises four structured components:
1. Spatial coordinates of all nodes (UAVs, UEs, BSs)
2. SNR values of all pairwise links
3. Data rates currently received by all UEs
4. Connectivity status (connected/disconnected) of each UAV

**Total observation for drone u:**
o_t^u = concat(ξ(t), l_u(t), {ρ_{u,i}(t) for all i in N})

The first part (ξ) gives the drone a global picture; the second part (l_u and ρ_{u,i}) uniquely identifies this specific drone, so the shared-parameter policy network knows which agent it is computing for. Without this local identity component, all drones would receive identical inputs and make identical decisions — destroying coordination.

**Practical feasibility:** The paper notes that in real deployment, drones would exchange only compact coordination messages (position, SNR, connectivity status) — a lightweight overhead compared to the communication service they are providing.

---

### Step 4: Task-Based Agent Grouping and Reward Decomposition

**Why grouping:** Different drones have different roles. Drones near the BSs should prioritize relay duties; drones near UEs should prioritize coverage. Training all drones with the same objective leads to role ambiguity and inefficient learning.

**How grouping works:**
- For each drone u, compute its initial distance to the nearest BS: d_u^G = min over g in G of { distance(u, g) at t=0 }
- Sort all drones by d_u^G
- Partition into N_G groups using quantile-based segmentation
- Drones with smaller d_u^G (closer to BSs) → smaller groups (approximately matching the number of BSs = 3)
- Drones with larger d_u^G (farther from BSs, nearer to UEs) → larger groups (to improve coverage)
- The paper uses 4 groups for 18 UAVs in the main experiments

**Reward decomposition:** Each drone's individual reward is:
R_t^u = R_t + α_1^u × R_u^Conn(t) + α_2^u × R_u^RE(t)

where:
- **R_t** = team reward (equation 14) — global network coverage and data rate
- **R_u^Conn(t)** = connection reward: total data rate that drone u provides directly to its associated UEs. A UE is "associated" to drone u if u provides it the best data rate among all connected drones. This rewards UAVs for being good last-mile providers.
- **R_u^RE(t)** = relay reward: total data traffic flowing through drone u from other downstream drones and their users. This rewards UAVs for being good relay hubs.
- **α_1^u and α_2^u** = role-based weights. For relay-focused groups (close to BS): α_2 is larger. For coverage-focused groups (close to UEs): α_1 is larger. Paper uses α_1=1, α_2=3 as primary settings.

---

### Step 5: Behavioral Constraints for Gateway Drones

**What it does:** Drones in group G_BS (those directly connected to BSs) get a special training penalty if they drift away from BS connectivity.

**The mechanism (equation 30):**
- If a G_BS drone's maximum SNR to any BS drops below ρ_th:
  - Compute the direction toward the BS with the highest SNR: z_u^BC(t) = (l_{g*} - l_u) / ||l_{g*} - l_u||
  - Map this direction to the closest discrete action in the action space using cosine similarity
  - Add a penalty term to the loss: L_u^BC = -1(condition) × w_BC × log π^u(mapped action | o_t^u)
  - The weight w_BC = ||l_{g*}(t) - l_u(t)||_2 scales the penalty with UAV-BS distance (larger penalty when farther away)

**Intuition:** This does not override the drone's policy entirely — it adds a training pressure (a loss term with weight β_2 = 0.3) that gradually nudges the drone's learned policy to avoid connectivity-breaking moves. Other drone groups do not get this constraint because they need more freedom to explore and adapt to dynamic UE positions.

---

### Step 6: LLM Agent and Knowledge Distillation

**Phase 1: Environment simplification for LLM comprehension**
- The continuous 3.5 km × 3.5 km area is divided into a grid
- Grid cell width d^grid = (1/√2) × max{d_{u,v} | ρ_{u,v} ≥ ρ_th}
  - This ensures UAVs at adjacent cell centers can communicate (meet SNR threshold)
- The LLM's environment is described as an 8×8 grid showing UE density per cell
- This simplification converts thousands of precise coordinates into a human-readable density map

**Phase 2: Structured prompt engineering**
The prompt to GPT-4o contains five components:
1. Scenario description (explain the disaster scenario, multi-hop networking, relay constraints)
2. Model behavior and objective (analyze UE distribution, ensure relay connectivity, maximize coverage)
3. Output format (e.g., "list of 3D coordinates in the format [(x1,y1,z1), (x2,y2,z2), ...]")
4. Few-shot examples (representative input-output pairs to guide format)
5. Current state (current UE distribution grid, BS locations)

**Phase 3: Chain-of-Thought reasoning in 3 steps**
The LLM is prompted to reason through three sequential questions:
- Step a: Where are UEs concentrated? Identify candidate positions.
- Step b: Which candidate positions would leave connectivity gaps? Adjust for relay coverage.
- Step c: Finalize the deployment list ensuring connectivity and coverage.

**Phase 4: Rule-based verifier**
Before using LLM output, a verifier checks:
- UAV positions are within operational boundaries and physically reachable
- Multi-hop paths remain connected
- Only a small number of UAVs are isolated
- Sufficient UE coverage is maintained
- Invalid outputs are discarded; the cached previous valid output is reused

**Phase 5: Hungarian algorithm matching (equation 32)**
Given 18 LLM-suggested positions and 18 actual drone positions:
- Compute a cost matrix: cost(u, σ(u)) = Euclidean distance between drone u's current position and LLM-suggested position σ(u)
- The Hungarian algorithm finds the permutation σ* minimizing total cost
- Under σ*, each drone u has an assigned target: the LLM-suggested position σ*(u)

**Phase 6: Soft target distribution construction (equation 34)**
- For drone u, compute z_u^LLM(t) = l_{σ*(u)}^LLM(t) - l_u(t) (direction toward target)
- For each of 9 possible discrete actions a_i, compute cosine similarity between z_u^LLM and the direction vector of a_i
- Apply softmax with temperature Ω=1 to get soft target probabilities p̃_u(z_i, t)
- Actions more aligned with the LLM-inferred direction get higher probability

**Phase 7: Distillation loss (equation 35)**
L_u^KD(t) = -Σ_{z_i in Z^u} p̃_u(z_i, t) × log π^u(map^{-1}(z_i) | o_t^u)

This is a cross-entropy loss between the LLM's soft target distribution and the drone's current policy output. It acts as a supervised signal that nudges the drone's policy to align with the LLM's strategic direction.

**Phase 8: Combined training objective (equation 16)**
max over π^u: L_u^PPO(t) - β_1 × L_u^KD(t) - β_2 × L_u^BC(t)

- β_1 (distillation weight): starts at 0.5, decays to 0.1 toward end of training
  - Reason: early in training, the LLM guide is very valuable; later, the drone's own learned policy should take over
- β_2 (behavioral constraint weight): 0.3
- β_1's gradual reduction ensures the drone ultimately learns its own strategy rather than just mimicking the LLM

---

## The Experiments

**Main comparative experiment:**
- Environment: 3.5 km × 3.5 km, 18 UAVs, ~150 UEs
- Training: 25,000 episodes × 400 time steps = 10 million training steps
- Policy networks: MLP with 5 hidden layers, tanh activation
- Learning rate: starts at 3×10⁻⁴, decays to 1×10⁻⁴
- LLM queries: GPT-4o queried every Q_LLM steps; outputs cached between queries
- Comparison against 5 baselines: GVis, GA2C, MAPPO, IA2C, MAA2C
- Training hardware: The paper does not specify GPU/CPU details

**Scaling experiments (Figure 5):**
- Environment size varied: 6.76, 8.41, 10.24, 12.25, 14.44 km²
- UAV count varied: 12, 15, 18, 21, 24 UAVs
- Both axes compared against GVis, GA2C, MAPPO

**Ablation study (Figure 6):**
- NR: MRLMN without agent grouping and reward decomposition
- NL: MRLMN without knowledge distillation and LLM agent
- NC: MRLMN without behavioral constraints
- All three compared against full MRLMN across same scaling conditions

**Policy sharing experiment (Figure 7):**
- Number of trained policies varied from 4 to 18 within the 4-group framework
- Each configuration run 3 independent times for statistical reliability
- Training time (hours) and performance metrics recorded simultaneously

**Simulation visualization (Figure 8):**
- Single episode visualization at t=1, t=100, t=200, t=400
- Shows network topology evolution and live metrics at each snapshot

---

## Pipeline Diagram

```
[Disaster Environment: 3.5km x 3.5km, 150 UEs, 3 BSs, 18 UAVs]
                          |
                          v
[State Observation: positions, SNR values, link status, connectivity flags]
                          |
                          v
[Information Aggregation: share local observations, form structured xi(t)]
                          |
                    +-----+-----+
                    |           |
                    v           v
         [MARL Branch]      [LLM Branch (offline, periodic)]
                    |           |
                    |     [Simplified grid environment]
                    |           |
                    |     [Structured prompt + CoT reasoning]
                    |           |
                    |     [GPT-4o generates deployment positions]
                    |           |
                    |     [Rule-based verifier: accept or discard]
                    |           |
                    +-----+-----+
                          |
                          v
           [Hungarian Algorithm: match LLM positions to drones]
                          |
                          v
           [Soft target distribution: p_tilde_u(z_i, t)]
                          |
                          v
[Agent Grouping: sort by BS distance, partition into 4 groups]
                          |
                          v
[Reward Decomposition: team + R_Conn + R_RE, weighted by group role]
                          |
                          v
[IPPO Policy Update: L_PPO - beta_1 * L_KD - beta_2 * L_BC]
  (behavioral constraint applied to gateway group only)
                          |
                          v
[Updated drone policies -> Actions -> Environment step]
                          |
                          v
[Evaluation metrics: Connected UE%, Data rate (Mbps), Available UAV%]
```

**At deployment time (no LLM):**
```
[Live disaster environment]
        |
        v
[Each UAV observes local state]
        |
        v
[Shared information aggregation over multi-hop network]
        |
        v
[Each UAV's MLP policy network -> Action (one of 9 directions)]
        |
        v
[Fully decentralized, real-time UAV control]
```
