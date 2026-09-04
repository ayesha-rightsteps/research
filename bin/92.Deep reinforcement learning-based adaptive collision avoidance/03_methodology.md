# 03 — Methodology: What the Researchers Did

---

## Research Design

**Type of study:** Simulation-based experimental study with transfer validation.

The authors designed and evaluated a novel deep reinforcement learning algorithm in a custom simulation environment, then transferred the trained model to a high-fidelity 3D simulation platform. There is no real-world flight test in this paper — everything is simulation. The study follows an engineering research design: propose a method, build a simulation, run controlled experiments, compare against baselines, and validate generalization.

**Overall strategy:** Design a realistic joint airspace environment → train the UAV agent using HPER-D3QN → evaluate performance under multiple conditions (aircraft density, uncertainty level, aircraft type ratio) → compare with 5 baseline DRL methods and 2 traditional methods → validate on a high-fidelity platform.

---

## The Data

**No external dataset is used.** All training and testing data is generated procedurally by the simulation environment itself.

**Training Environment Details:**
- Platform: Custom simulator built with Python's **PyGame** library
- Airspace size: 30 km × 30 km (2D horizontal plane)
- Maximum aircraft: Up to 25 (excluding the UAV agent)
- Number of aircraft per episode: Randomly selected during training (between 3 and 25)
- Manned-to-unmanned ratio: Randomly selected per episode
- Uncertainty level: Randomly selected per episode from 3 levels
- Time step: 1 second per step
- Episode ends: When UAV collides, reaches destination, or exits airspace

**Aircraft Parameters (Table 3 in paper):**

| Parameter | Value |
|-----------|-------|
| UAV speed range | 60–110 m/s |
| Manned aircraft speed range | 80–160 m/s |
| Destination radius | 100 m |
| Protected zone radius | 150 m |
| UAV warning zone radius | 400 m |
| Manned aircraft warning zone radius | 800 m |
| UAV detection range radius | 4,000 m |
| Number of detection sectors | 8 |
| Speed adjustment per action | 5 m/s |
| Heading adjustment per action | 3 degrees/second |

**Preprocessing:** None in the traditional sense. Aircraft positions and initial states are generated randomly at the start of each episode according to predefined combat plans and motion capability constraints. Uncertainty is injected via the joint error model (see below).

---

## The Methods

### Step 1: Joint Airspace Environment and Uncertainty Model

**What it does:** Creates a realistic simulation of a contested airspace with manned and unmanned aircraft subject to wind and state uncertainty.

**Why they used it:** A realistic environment is essential for the trained policy to have any chance of working in a real deployment. Oversimplified environments (no wind, all aircraft same type) produce agents that fail in the real world.

**How it works:**

The UAV's motion is governed by second-order kinematic equations (Equation 1 in the paper):
- Speed rate of change: dv/dt = a_v (linear acceleration)
- x position: dx/dt = v × cos(φ)
- y position: dy/dt = v × cos(φ) — (Note: the paper uses this formulation for the 2D plane)
- Heading change: dφ/dt = ω (angular velocity)

**Wind model (Equation 4):** Wind speed and direction follow sinusoidal time variations:
- v_w(t) = v_base + v_var × sin(2πt/T) — wind speed oscillates around a baseline
- φ_w(t) = φ_base + φ_var × sin(2πt/T) — wind direction oscillates similarly

**Aircraft type sensitivity:** UAVs are more affected by wind than manned aircraft. The ground speed of any aircraft is:
- v_s = v_o + η_type × v_w

where η_UAV = 1.0 and η_manned = 0.8. A UAV with η = 1.0 feels the full wind effect; a manned jet at η = 0.8 is more resistant.

**State uncertainty (Equations 7–8):** Each aircraft also has random heading and speed errors modeled as normal distributions. UAVs have larger error ranges (±10 degrees heading, ±5 m/s speed at Level 5) than manned aircraft (±5 degrees, ±2.5 m/s at Level 5) — reflecting that manned pilots can compensate for disturbances better.

**Six levels of uncertainty (Table 6 in paper):**

| Level | Manned heading error | Manned speed error | UAV heading error | UAV speed error | Wind speed |
|-------|---------------------|-------------------|-------------------|-----------------|------------|
| 0 | 0° | 0 m/s | 0° | 0 m/s | 0 m/s |
| 1 | ±1° | ±0.5 m/s | ±2° | ±1 m/s | 4 m/s amplitude |
| 3 | ±3° | ±1.5 m/s | ±6° | ±3 m/s | 8 m/s amplitude |
| 5 | ±5° | ±2.5 m/s | ±10° | ±5 m/s | 12 m/s amplitude |

---

### Step 2: Sector-Based Partial Observation Model and Observation Space

**What it does:** Defines exactly what the UAV can see and how that information is structured for input to the neural network.

**Why they used it:** Global observation (knowing every aircraft's position and state at all times) is computationally infeasible in a battlefield and incompatible with fixed-dimension neural network inputs. The sector model makes observations compact and fixed-dimension regardless of how many aircraft are present.

**How it works:**

The UAV's 4,000-meter detection range is divided into 8 equal sectors (45 degrees each), starting from north and going clockwise. In each sector, only the most dangerous aircraft (selected by DTPA) is tracked as the "intruder."

The full observation vector O^t consists of two parts:

**(A) Ownship observation O^t_O:**
- v^t_own — current speed of the UAV
- D^t_g — distance from UAV to its mission destination
- φ^t_g — heading angle toward the destination
- v^t_w — current wind speed
- φ^t_w — current wind direction

**(B) Intruder observation O^t_I (one per sector, 8 sectors total):**
For each sector d:
- D^t_int — distance from UAV to intruder in sector d
- θ^t_int — relative bearing angle to intruder (where intruder is relative to UAV heading)
- ψ^t_int — angle between the intruder's heading and the UAV's heading
- o^t_it — aircraft type flag: 1 if manned, 0 if unmanned
- v^t_int — intruder's current speed

**Total observation dimension:** 1 (speed) + 2 (destination) + 2 (wind) + 8 × 5 (intruder per sector) = 45 inputs to the neural network — which matches the network's input layer size (45 × 128 × 64 × 32 × 9).

---

### Step 3: Action Space Design

**What it does:** Defines what maneuvers the UAV can make at each time step.

**How it works:**

The UAV has 9 discrete actions — all combinations of:
- Linear acceleration a_v ∈ {-5 m/s², 0, +5 m/s²} (decrease speed, maintain, increase)
- Angular velocity a_ω ∈ {-3°/s, 0, +3°/s} (turn left, go straight, turn right)

3 speed choices × 3 heading choices = 9 total actions.

After each action, the UAV's state updates as:
- v^(t+1) = Clip(v^t + a_v × Δt) — speed clipped to [60, 110] m/s range
- φ^(t+1) = φ^t + a_ω × Δt — heading updated

---

### Step 4: Reward Function Design

**What it does:** Tells the UAV how good or bad each decision was, so it can learn from experience.

**How it works:**

Five reward components (Equations 20–25):

| Component | Trigger | Value |
|-----------|---------|-------|
| Mission destination reward (r_goal) | Reaching destination | +2 |
| Warning zone penalty (r_w) | Entering another aircraft's warning zone | -0.5 |
| Collision penalty (r_c) | Entering protected zone (distance < 150 m) | -1 |
| Boundary violation penalty (r_out) | Exiting the 30 km × 30 km airspace | -0.5 |
| Efficiency reward (r_e) | Every time step | -0.005 base, plus penalties for distance increase and heading deviation |

The warning zone penalty is adaptive — manned aircraft have a larger warning zone (800 m), so the threshold for triggering r_w is larger when the intruder is a manned aircraft.

The efficiency reward at each step is: r_e = C_step + C_dis(D^t_g - D^(t-1)_g) + C_angle × |φ^t_g|
This penalizes the UAV for moving away from its destination and for flying at a large angle away from the goal direction — pushing it to be goal-directed.

Total reward: r_total = r_goal + r_ca + r_w + r_out + r_e

---

### Step 5: Dynamic Threat Prioritization Assessment (DTPA)

**What it does:** Within each of the 8 detection sectors, selects the one aircraft that poses the greatest collision threat to the UAV.

**Why they used it:** Simply tracking the closest aircraft in each sector is insufficient. A fast manned aircraft 700 meters away might be more dangerous than a slow UAV 400 meters away that is actually flying away. DTPA captures this by using multiple factors.

**How it works (Algorithm 1):**

For each detected aircraft i within a sector:
1. Calculate T_CPA and D_CPA using the relative position and velocity vectors (Equation 3)
2. Determine the aircraft type coefficient κ: 0.75 for manned, 0.25 for unmanned (manned aircraft get higher threat score because they are harder to avoid and cause more damage)
3. Compute threat score (Equation 28):

   **S = ω_t × (T_CPA - T_min)/(T_max - T_min) + ω_d × (D_CPA - D_min)/(D_max - D_min) + ω_type × κ**

   where:
   - ω_t = 0.4 (weight for time factor)
   - ω_d = 0.4 (weight for distance factor)
   - ω_type = 0.2 (weight for aircraft type)
   - T_max = 200 s, T_min = 20 s (time thresholds)
   - D_max = 4,000 m, D_min = 150 m (distance thresholds)

4. Rank all aircraft by score S (descending order)
5. Select the aircraft with the highest S as the intruder for that sector

**Why these weights?** Time and distance are the most direct physical predictors of collision risk, so they each get 0.4. Aircraft type provides an adjustment factor to give priority to avoiding the more dangerous manned aircraft, so it gets 0.2.

---

### Step 6: HPER Mechanism

**What it does:** Classifies all training experiences into three hierarchical priority layers and samples from them with different probabilities during training.

**Why they used it:** Standard uniform experience replay wastes time on boring "nothing happened" experiences while rarely encountering critical collision or arrival events. This slows convergence and produces a poorly calibrated policy.

**How it works (Algorithm 2):**

**Experience classification:**

Each experience e_i = (O_i, a_i, O'_i, r_i) is classified by extracting a feature vector from the observation:
[e_d, e_w, e_c, e_out, e_g]

where each component is 1 (yes) or 0 (no):
- e_d: UAV detects other aircraft
- e_w: UAV is in warning zone
- e_c: UAV is in protected zone (collision)
- e_out: UAV exceeded airspace boundary
- e_g: UAV reached destination

**Three priority layers:**

| Layer | Scenarios | Capacity | Rationale |
|-------|-----------|----------|-----------|
| High-priority E_high | Collision (O_c), Destination arrival (O_arrival), Boundary violation (O_out) | 4,000 | Terminal events — rare but critical for learning |
| Medium-priority E_medium | Warning zone entry (O_w) | 6,000 | Near-miss events — important for threat avoidance |
| Low-priority E_low | Safe cruise (O_safe only) | 10,000 | Routine flight — needed for basic navigation |

**Sampling within layers (Equations 39–42):**
- Layer sampling weight: λ_layer = (M_layer / M) × k_layer where k_layer is a priority scaling factor [1, 2, 3 for low, medium, high respectively]
- Within each layer, individual experience i is sampled with probability proportional to |δ_i|^α_PER + ε (higher TD error → higher probability)
- When a layer's buffer is full, old experiences are removed using FIFO (first-in, first-out)

---

### Step 7: D3QN Neural Network

**Architecture:** 5-layer fully connected network: 45 → 128 → 64 → 32 → 9 neurons

- Input layer (45 neurons): Full observation vector
- Three hidden layers (128, 64, 32 neurons) with nonlinear activations
- Output layer (9 neurons): Q-values for each of the 9 maneuver actions

**Two networks maintained simultaneously:**
- Prediction (online) network with parameters θ: Selects actions, updated every training step
- Target network with parameters θ⁻: Evaluates Q-values, updated every 50 steps (soft copy from prediction network)

**DDQN update rule (Equation 26):**
y = r + γ × Q(O', argmax_{a'} Q(O', a'; θ); θ⁻)

- Action is selected using the prediction network (θ)
- Action's value is evaluated using the target network (θ⁻)
- This separation prevents overestimation

**Dueling architecture (Equation 27):**
Q(O, a; θ, α, β) = V(O; θ, β) + [A(O, a; θ, α) - (1/|A|) × Σ A(O, a'; θ, α)]

- V: State value — how good is this situation regardless of action?
- A: Action advantage — how much better is this specific action than average?
- Subtracting mean advantage ensures identifiability of V and A

---

### Step 8: Training Process (Algorithm 3)

**How it works:**
1. Reset environment, initialize time step
2. Get observation O^t using DTPA (Algorithm 1)
3. Evaluate Q-values using prediction network
4. Select action using ε-greedy policy (ε starts at 0.995, decays to 0.001)
5. Execute action, receive reward r^t, observe O^(t+1)
6. Form experience tuple (O^t, a^t, O^(t+1), r^t)
7. Classify and store in appropriate HPER layer
8. Sample mini-batch of 128 experiences using HPER (Equation 40)
9. Compute DDQN target Q-values
10. Update prediction network θ via TD loss (minimize |y - Q(O, a; θ)|²)
11. Every 50 steps: copy θ → θ⁻ (update target network)
12. Repeat until episode ends; then start next episode

**Training hyperparameters (Table 4):**

| Parameter | Value |
|-----------|-------|
| Network | 45 × 128 × 64 × 32 × 9 |
| Mini-batch size | 128 |
| Total replay buffer size | 20,000 |
| Layer sizes [high, medium, low] | [4,000, 6,000, 10,000] |
| Learning rate | 0.0001 |
| Discount factor γ | 0.99 |
| Epsilon decay | 0.995 → 0.001 |
| Priority scaling factors | [1, 2, 3] for [low, medium, high] |
| α_PER | 0.5 |
| Target update cycle | Every 50 steps |
| Training duration | ~30,000 episodes |

---

## The Experiments

**Baselines compared (DRL methods):**
- DQN, DDQN, Dueling DQN, D3QN, PER-D3QN

**Baselines compared (traditional methods):**
- Rule-Based: NASA DO-365C Detect and Avoid (DAA) standard
- DP-Based: ACAS Xu (Next-Generation Airborne Collision Avoidance System based on dynamic programming, RTCA DO-386)

**Evaluation metrics:**
1. **Success rate** — percentage of episodes where UAV avoids collision AND reaches destination
2. **Task completion time (seconds)** — average mission duration
3. **FHP** — Frequency of Hazardous Proximity (average warning zone entries per episode × 10⁻²)

**Test conditions (3 independent experiments):**
1. Section 4.3.1: Different aircraft densities (N = 3, 5, 10, 15, 20, 25), 300 runs × 10 repetitions
2. Section 4.3.2: Different uncertainty levels (l = 0, 1, 2, 3, 4, 5)
3. Section 4.3.3: Different manned-to-unmanned ratios (ρ = 0, 0.2, 0.4, 0.6, 0.8, 1.0)

**Ablation experiment (Section 4.3.5):** Tested in hardest scenario (25 aircraft, uncertainty level 5):
- No DTPA (replace DTPA with distance-only threat selection)
- No HPER (replace with uniform experience replay)
- No Dueling (remove dueling architecture)
- No Double (remove double Q-learning update)

**Transfer experiment (Section 4.4):** Trained model transferred to Unity3D high-fidelity platform with 10 manned + 10 unmanned aircraft, testing whether the model generalizes to a completely different simulation environment.

---

## Pipeline Diagram

```
[Joint Operational Airspace Simulation]
            |
            v
[UAV Onboard Sensors: 4000m detection range, 8 sectors]
            |
            v
[DTPA Algorithm]
  - Compute TCPA and DCPA for all detected aircraft
  - Score each aircraft: S = 0.4×TCPA_norm + 0.4×DCPA_norm + 0.2×κ
  - Select highest-score aircraft per sector = "intruder"
            |
            v
[Observation Vector O^t (45 dimensions)]
  - UAV own state: speed, distance to goal, heading to goal
  - Wind: speed, direction
  - 8 × intruder: distance, bearing, heading angle, type flag, speed
            |
            v
[D3QN Prediction Network (45→128→64→32→9)]
  - Dueling architecture: V(s) + A(s,a)
  - Output: Q-values for 9 maneuver actions
            |
            v
[ε-Greedy Action Selection]
  - High ε early (explore) → Low ε late (exploit)
  - Select action a^t = argmax Q(O^t, a)
            |
            v
[Execute Action in Environment]
  - Update UAV speed and heading
  - Wind and state uncertainty applied
  - Observe next state O^(t+1) and reward r^t
            |
            v
[HPER Mechanism]
  - Classify experience (O^t, a^t, O^(t+1), r^t) into:
      HIGH layer: collision, arrival, boundary violation
      MEDIUM layer: warning zone entry
      LOW layer: safe cruise
  - Sample mini-batch (128) weighted by layer + TD error
            |
            v
[DDQN Training Update]
  - Compute target: y = r + γ × Q(O', argmax Q(O',a;θ); θ⁻)
  - Update θ via TD loss minimization
  - Every 50 steps: θ⁻ ← θ
            |
            v
[Evaluation on Test Scenarios]
  - 300 runs × 10 repetitions per condition
  - Metrics: Success rate, Task completion time, FHP
            |
            v
[Transfer to Unity3D High-Fidelity Platform]
  - 10 manned + 10 unmanned aircraft
  - 3D realistic battlefield environment
  - Validate generalization capability
```
