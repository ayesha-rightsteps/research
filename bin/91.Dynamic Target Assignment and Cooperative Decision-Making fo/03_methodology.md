# 03 — Methodology: Exactly What the Researchers Did

---

## Research Design

**Type of study:** Simulation-based experimental study. The researchers built a high-fidelity simulation environment in Gazebo (a widely used robotics simulator) and trained and evaluated all algorithms within it. No real drones were flown — but the simulation uses rigid-body physics, ray-cast LiDAR, and collision detection, making it significantly more realistic than abstract simulations.

**Overall strategy:** The researchers proposed a new algorithm (DA-MAPPO) and compared it against five baselines across 6 environments (3 static + 3 dynamic, each with different obstacle densities), with 100 test episodes per environment. They also ran ablation studies, reward contribution analysis, and robustness tests to deeply understand what makes the algorithm work.

---

## The Environment / "Data"

This paper does not use a dataset in the traditional sense. Instead, it uses a simulation environment. Here is exactly how that environment is set up:

**The physical world:**
- A bounded 3D workspace, but UAVs fly at a fixed altitude H — effectively a 2D problem
- The workspace is divided into: a Takeoff area, an Obstacle area, and a Goal area
- Each environment has static obstacles scattered in the obstacle area
- Three difficulty levels: ENV-1 (30 obstacles), ENV-2 (40 obstacles), ENV-3 (50 obstacles)

**The agents (UAVs):**
- N = 3 UAVs operating simultaneously
- Each UAV is modeled as a circular rigid body (so physics engine computes real collisions)
- Each UAV has a simulated 2D LiDAR with D = 35 range measurements
- Communication radius: limited (Rcom), so drones only talk to nearby neighbors

**The targets:**
- M = 3 targets (one per drone, one-to-one assignment)
- Static experiments: targets do not move throughout the episode
- Dynamic experiments: targets periodically swap positions, simulating moving targets
- Target moving speed tested up to 3 m/s (6 times the UAV's maximum speed of 0.5 m/s)

**Episode termination:**
An episode ends when:
1. All drones arrive at their targets (SUCCESS)
2. Any drone collides with an obstacle or another drone (COLLISION failure)
3. Any drone goes outside the workspace boundary (BOUNDARY failure)
4. The episode exceeds the maximum time steps Tmax = 600 (TIMEOUT failure)

**Training environment:**
- Progressive curriculum: obstacle count increases across 6 stages over 3 million total environment steps (see Table III in the paper)
- Hardware: AMD Ryzen 9 7950X CPU, NVIDIA RTX 4090 GPU, 64 GB RAM, Ubuntu 18.04
- Framework: PyTorch 1.5.1 + CUDA 10.1, Python 3.6.1

---

## The Methods (Step by Step)

### Step 1: Mathematical Problem Formulation (Dec-POMDP)

The problem is modeled as a Decentralized Partially Observable Markov Decision Process (Dec-POMDP) with components:
- N = set of agents (3 drones)
- S = global state space (all drone positions, target positions, obstacle positions)
- A = joint action space (velocity + angular velocity for each drone)
- O = joint observation space (what each drone locally perceives)
- P = state transition function (physics of drone movement)
- R = reward function
- gamma = 0.99 (discount factor)

The mission objective is to find a policy that minimizes total mission time while satisfying:
- Obstacle safety constraint: each drone must stay at least d_safe from all obstacles
- Inter-drone safety constraint: drones must stay at least d_col from each other
- Communication constraint: drones communicate only within radius R_com

The safety distance d_safe is analytically defined as: d_safe >= v_max * delta_t + v_max^2 / (2 * a_max), which is the minimum stopping distance — the space needed for a drone traveling at max speed to fully stop within one control cycle.

---

### Step 2: Agent Observation Design

Each drone's observation vector has 4 components:

**Component 1 — Obstacle perception (z_t^i):**
- 35 LiDAR range readings, one at each fixed angle
- Encodes how far obstacles are in every direction
- Dimension: D = 35

**Component 2 — Ego-motion state (u_t^i):**
- Forward linear velocity v_t^i
- Yaw angular velocity omega_t^i
- Linear acceleration (estimated via finite-difference, smoothed by Kalman filter)
- Angular acceleration (same method)
- Dimension: 4

**Component 3 — Target features (g_t^i):**
- THIS IS THE KEY INNOVATION
- Distance to assigned target: d_t^i = Euclidean distance to current target
- Relative bearing: Delta_theta_t^i = direction to target relative to drone's current heading
- These are polar coordinates in the drone's own body frame
- Dimension: 2

**Component 4 — Swarm topology (q_t^i):**
- Relative position (delta_x, delta_y) of each teammate
- Concatenated into a fixed-length vector
- Dimension: 2*(N-1) = 4 (for N=3 drones)

**Total observation dimension:** d_loc = 35 + 4 + 2 + 4 = 45

---

### Step 3: Action Space

Each drone outputs a 2D continuous control command:
- Forward linear velocity v^i in [-1, 1] m/s
- Yaw angular velocity omega^i in [-1, 1] rad/s

These are continuous actions (not discrete), which allows smooth flight maneuvers.

---

### Step 4: Online Target Allocation (The Core Innovation)

At EVERY decision time step t:

1. Observe current positions of all N drones: P_t = {p_t^1, p_t^2, ..., p_t^N}
2. Observe current positions of all M targets: Q_t = {q_t^1, q_t^2, ..., q_t^M}
3. Build a cost matrix C_t of size N x M:
   - Element C_t^{i,j} = squared Euclidean distance from drone i to target j
4. Solve the assignment problem using a Hungarian-type algorithm:
   - Find assignment matrix Pi that minimizes total cost
   - Constraint: each drone gets exactly one target, each target gets at most one drone
5. Assignment result phi_t(i) = which target drone i should chase right now

This assignment is solved fresh every single step. If a target moves, the next assignment will reflect the new positions. No memory of previous assignments is kept — each step is solved from scratch.

**Computational complexity:** O(N^3) for the balanced case M=N, which becomes the dominant computational bottleneck as swarm size grows.

---

### Step 5: Constructing the Augmented Observation

Raw observation: o_raw^i = [z_t^i, u_t^i, q_t^i] (obstacles, motion, teammates)

After allocation: augment with g_t^i = [d_t^i, Delta_theta_t^i] (distance and direction to assigned target)

Final observation: o_t^i = [z_t^i, u_t^i, g_t^i, q_t^i]

This augmented observation is the input to the policy network. When target assignment changes, g_t^i changes immediately, and the drone's next action automatically reflects the new target.

---

### Step 6: Hierarchical Reward Function

The reward has 4 tiers, summed and divided by 50 for normalization:

**Tier 1 — Team Coordination:**
- Penalizes the SUM of all drone-to-target distances
- Formula: R_team = -omega_team * sum(d_t^j for all j)
- Effect: pushes the whole swarm to collectively approach targets

**Tier 2 — Individual Navigation:**
- Progress reward: R_prog = -kappa_prog * (d_prev - d_current) — positive when drone is moving toward its target
- Arrival bonus: R_arr = b_k when first entering target zone; b_k decreases with arrival order (rewards arriving early, discourages free-riding)
- Hover reward: +1.0 when inside target zone; -10.0 if the drone drifts out after arriving

**Tier 3 — Safety Constraints:**
- Hard obstacle penalty: -100.0 if any LiDAR reading < d_safe; -25.0 between d_safe and 2*d_safe; -10.0 between 2*d_safe and 3*d_safe
- Soft obstacle penalty: continuous linear cost for all LiDAR readings < 2*d_safe
- Inter-drone penalty: -100.0 if any two drones get closer than d_col

**Tier 4 — Auxiliary Regularization:**
- Smoothness penalty: -0.5 * |acceleration| - 0.2 * |angular_acceleration| (discourages jerky flight)
- Step penalty: -1.0 per step (time pressure to complete mission quickly)
- Boundary penalty: -100 if outside workspace; decreasing penalty near boundary

**Final per-agent reward:** R_t^i = (1/50) * [all 8 components summed]

---

### Step 7: The DA-MAPPO Training Algorithm

The training loop (Algorithm 1 in the paper):

1. Initialize policy network (actor) with parameters theta, value network (critic) with parameters phi
2. For each training episode:
   a. Reset environment, get initial state
   b. For each time step t:
      - Observe all drone and target positions
      - Build cost matrix C_t
      - Solve assignment: phi_t = Assign(C_t) — Hungarian algorithm
      - For each drone i: build augmented observation o_t^i, sample action a_t^i from policy
      - Execute joint action, observe reward r_t, new state s_{t+1}
      - Solve assignment for s_{t+1}, build next observations o_{t+1}
      - Store transition in replay buffer
   c. After collecting trajectories, compute advantage estimates using GAE:
      - A_hat_t = r_t + gamma * V(s_{t+1}) - V(s_t)
      - Full GAE: sum over l of (gamma*lambda)^l * temporal differences
   d. Update actor by maximizing: min(r_t(theta) * A_hat_t, clip(r_t(theta), 1-eps, 1+eps) * A_hat_t) + sigma * H(policy)
   e. Update critic by minimizing clipped MSE loss against discounted returns

**Key hyperparameters:**
- MLP layers: 3 hidden layers, dimension 256 each
- Learning rate: 1e-5
- PPO epochs per update: 10
- Clipping parameter: 0.2
- Entropy coefficient: 0.1
- Discount factor: 0.99
- Episode length: 600 steps
- Total training: 3 million environment steps

---

### Step 8: Progressive Curriculum Training

| Training Steps | Number of Obstacles |
|---|---|
| 0 — 400,000 | 0 – 10 |
| 400,000 — 800,000 | 10 – 20 |
| 800,000 — 1,200,000 | 20 – 25 |
| 1,200,000 — 1,600,000 | 25 – 30 |
| 1,600,000 — 2,000,000 | 30 – 35 |
| 2,000,000 — 3,000,000 | 35 – 40 |

This gradual increase means the policy first learns basic navigation, then collision avoidance in sparse environments, then dense coordination, building capability incrementally.

---

## The Experiments

**Experiment 1: Static Multi-Target Navigation**
- Targets stay fixed throughout each episode
- Environments: ENV-1 (30 obstacles), ENV-2 (40 obstacles), ENV-3 (50 obstacles)
- 100 test episodes per environment
- Purpose: evaluate baseline coordination and collision avoidance

**Experiment 2: Dynamic Multi-Target Navigation**
- Targets periodically swap positions during the episode
- Same 3 environments as above
- 100 test episodes per environment
- Purpose: evaluate adaptability to moving targets — the core contribution

**Experiment 3: Ablation Studies**
- Tested in dynamic scenarios
- Variant 1: allocation every 50 steps instead of every step
- Variant 2: remove team reward term
- Variant 3: remove augmented state entirely
- Purpose: isolate the contribution of each design choice

**Experiment 4: Reward Contribution Analysis**
- Record cumulative reward for each component across all evaluation episodes
- Separate episodes by termination type (SUCCESS vs. COLLISION)
- Purpose: understand what drives behavior in successful vs. failed episodes

**Experiment 5: Robustness Analysis**
- Sensor noise: additive Gaussian noise on velocity/angular velocity (sigma_v up to 0.50)
- Communication interference: packet loss up to 50%, delay up to 6 steps
- Computational feasibility: inference time profiling on NVIDIA Jetson Orin Nano edge device
- Target speed variation: target speed from 0.5 m/s up to 3 m/s

**Baselines compared:**
1. IPPO — fully independent, no shared critic
2. MAPPO — standard centralized critic, no dynamic assignment
3. RMAPPO — MAPPO with recurrent memory
4. NavRL — RL-based safe navigation with safety shield
5. EGO-Planner v2 — state-of-the-art optimization-based trajectory planner

**Evaluation metrics:**
- R_success: mission success rate (primary)
- R_collision: collision-caused failure rate
- R_timeout: timeout-caused failure rate
- T_ave: average decision steps to completion
- L_ave: average trajectory length

---

## Pipeline Diagram

```
[UAV Swarm + Moving Targets in Gazebo Environment]
                        |
                        v
[Step 1: Environmental Perception]
  - Each UAV: 35-beam LiDAR scan (obstacle distances)
  - Each UAV: velocity, angular velocity, accelerations (Kalman-filtered)
  - Each UAV: relative positions of neighboring drones
  → Raw observation: o_raw = [z_t, u_t, q_t]
                        |
                        v
[Step 2: Online Target Allocation (Every Step)]
  - Observe all UAV positions and target positions
  - Build cost matrix C_t (squared Euclidean distances)
  - Solve Hungarian assignment: phi_t = argmin total cost
  - Each drone gets one target, each target gets at most one drone
  → Assignment result: g_t^i = [distance, bearing to assigned target]
                        |
                        v
[Step 3: Augment Observations]
  - Combine raw perception with target features
  → Augmented observation: o_t^i = [z_t, u_t, g_t, q_t] (dim=45)
                        |
                        v
[Step 4: Shared Policy Network (Actor)]
  - 3-layer MLP, hidden dim 256
  - Input: augmented observation (45-dim)
  - Output: action distribution → sample action a_t^i = (v, omega)
  → Continuous control commands for all 3 drones
                        |
                        v
[Step 5: Execute Actions in Gazebo]
  - Drones move according to commands
  - Physics engine computes collisions
  - Environment transitions to next state
                        |
                        v
[Training: Centralized Critic + PPO Updates]
  - Critic sees global state (all positions, all targets)
  - Compute GAE advantages
  - Clipped PPO loss + entropy bonus
  - Update actor and critic parameters
                        |
                        v
[Repeat until episode ends — then start next episode]
                        |
                        v
[Evaluation: 100 episodes per environment, 5 metrics reported]
```
