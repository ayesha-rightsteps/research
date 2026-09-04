# 03 — Methodology

Exactly what the researchers did, step by step, in plain language.

---

## Research Design

**What type of study is this?**
This is a **Systematic Literature Review (SLR)** — not an experimental study. The researchers did not create a new algorithm or run their own experiments. Instead, they systematically gathered, organized, analyzed, and compared existing published research to create a comprehensive, structured map of the field.

**What was the overall strategy?**
The strategy was to cast a wide net across major academic databases, apply strict selection criteria to identify the most relevant and high-quality papers, organize those papers into a logical classification scheme by domain and subtopic, and then compare them systematically using structured tables — revealing patterns, trends, strengths, and gaps across the field.

---

## The Data

**What "data" was used?**
The "data" in this survey is the body of existing research literature on DRL in autonomous systems. The researchers gathered published papers from 2018–2024 — the six years of most rapid growth in this area.

**Where did the data come from?**
Papers were collected from seven major academic databases:
- **IEEE Xplore** — the primary source for engineering and computer science papers
- **ACM Digital Library** — a major computing research archive
- **Google Scholar** — a broad academic search engine
- **ProQuest** — a multidisciplinary database
- **EBSCO** — a research database widely used in universities
- **ScienceDirect (Elsevier)** — a major scientific journal platform
- **MDPI** — an open-access publisher of peer-reviewed journals

**Search keywords used:**
"Deep Reinforcement Learning-DRL," "autonomous systems," "autonomous cars," "robotics," "drones," "drone," and "ADAS"

**Selection criteria:**
Papers were selected based on three factors: relevance to DRL in autonomous systems, citation impact (how often other researchers cited the paper — a proxy for importance), and publication date (prioritizing 2018–2024 to focus on recent advancements).

---

## The Methods

### Classification Scheme
The core methodological innovation of this survey is its classification scheme. Selected papers were organized into a two-level hierarchy:

**Level 1 — Application Domain (4 domains):**
- Autonomous Cars
- Autonomous Robotics
- Autonomous Drones
- Advanced Driver Assistance Systems (ADAS)

**Level 2 — Subtopics within each domain:**

For **Autonomous Cars:**
- Lane Following and Parking Maneuvering
- Urban Navigation and Vehicle Routing
- Obstacle and Collision Avoidance
- Braking Systems

For **Autonomous Robotics:**
- Swarm Behaviour
- Collision Avoidance
- Trajectory Planning

For **Autonomous Drones:**
- Security and Pollution Control
- Stability and Trajectory Planning
- Collision Avoidance

For **ADAS:**
- Lane Departure Warning/Correction
- Pedestrian Detection and Collision Avoidance
- Adaptive Cruise Control

**Why this classification works:** By grouping papers this way, the researchers could compare methods working on the same problem — rather than comparing apples to oranges — and identify where multiple papers converged on the same conclusions (strong evidence) versus where only one or two papers had explored a topic (research gap).

### Comparative Analysis Tables
For each domain, the authors created structured comparison tables (Tables III through VI in the paper) organizing each reviewed paper across four standard dimensions:
1. **DRL Technique Used** — which algorithm (DDPG, DQN, PPO, SAC, etc.)
2. **Objective** — what specific task the paper was trying to solve
3. **Experimental Setup** — what simulator or environment was used, what hardware
4. **Results** — what was achieved, measured against what baselines

This consistency allows direct comparison between papers and makes it possible to see which algorithms work best for which types of tasks.

---

## The Experiments (within reviewed papers)

Since this is a survey, the "experiments" are those conducted by the papers being reviewed. Here is a summary of the experimental approaches used across the literature:

### Simulators Used
- **CARLA** — photorealistic urban autonomous driving simulator (used by multiple car papers)
- **TORCS** — racing car simulator for highway-like driving
- **MATLAB/SIMULINK** — mathematical modeling software (used for lane following and parking)
- **CoppeliaSim** — 3D robot simulation environment (used for trajectory planning and navigation)
- **PyBullet** — physics engine for robot and swarm simulations
- **AirSim / Unreal Engine** — photorealistic aerial simulation for drones
- **NVIDIA Isaac Gym** — GPU-accelerated robot simulation
- **AWS DeepRacer** — miniature car platform + cloud simulation

### Common Baselines (what DRL was compared against)
- **Traditional PID controllers** — classic feedback control algorithms that use math equations rather than learning
- **Pure Pursuit (PP) control** — a path-following algorithm with constant speed
- **Traditional Adaptive Cruise Control (ACC)** — rule-based systems for maintaining following distance
- **Standard DQN** — older, less sophisticated versions of the DRL algorithms
- **CADRL, LSTM-RL, SARL** — competing DRL-based crowd navigation algorithms
- **Model Predictive Control (MPC)** — an optimization-based control method
- **Dynamic Window Approach** — a motion planning algorithm for robots

### Evaluation Metrics Explained
- **Success Rate / Completion Rate** — percentage of tasks completed without failure (collision, going off-road, etc.)
- **Collision Rate / Miss Rate** — how often the system failed dangerously
- **Cross-Track Error** — how far off the desired path the vehicle/robot strayed
- **Travel Time / Path Length** — efficiency measure — did the system find a fast, direct route?
- **Cumulative Reward** — the total score accumulated during training; higher = better learned policy
- **Episode Steps** — how many decision-making steps occurred before reaching a goal or terminal state
- **Q-values** — the estimated action values, tracked to verify the agent is learning correctly
- **Detection Accuracy / Miss Rate** — for ADAS tasks: how accurately pedestrians or lane markings are detected
- **Headway Distance** — for cruise control: how well the car maintained the correct following distance

---

## Pipeline Diagram

```
[Research Question]
"How is DRL being applied to autonomous systems, and what works?"
          ↓
[Database Search]
IEEE Xplore, ACM, Google Scholar, ProQuest,
EBSCO, ScienceDirect, MDPI
Keywords: DRL + autonomous cars/robotics/drones/ADAS
Publication years: 2018–2024
          ↓
[Paper Selection]
Filter by: relevance + citation impact + recency
          ↓
[Classification]
Organize by domain → subdomain → specific task
          ↓
[Comparative Analysis]
For each paper: DRL technique, objective, setup, results
          ↓
[Structured Comparison Tables]
Tables III–VI comparing methods within each domain
          ↓
[Synthesis + Insights]
Common patterns, emerging trends, open challenges
          ↓
[Output: Challenges + Future Directions]
Scalability, safety, Sim-to-Real, hybrid architectures,
LLMs, ethical/regulatory frameworks
```

---

## Specific Highlighted Methods (from reviewed papers)

### In Autonomous Cars:
- **DDPG in MATLAB/SIMULINK** for lane following — evaluates using episode steps, rewards, and Q0 values across diverse driving scenarios
- **D-A3C Urban Planner** — pre-trained with Imitation Learning, tested in real-world conditions to close the Sim-to-Real gap
- **DQN for Multi-Objective Vehicle Routing** — optimizes at intersections in mixed traffic, compared to conventional methods using travel time, waiting time, and driving distance
- **D2QN with PID controller** in CARLA — hierarchical: PID handles normal driving, DRL activates for dangerous pedestrian scenarios

### In Autonomous Robotics:
- **PPO in PyBullet** — trains multi-legged swarm robots for collective behavior on flat and rough terrain
- **SAC vs DDPG comparison** in CoppeliaSim — 6,000-episode test on a Panda robot manipulator, measuring safety rate and consistency
- **CAM-RL (GRU + MLP + Attention)** — tested in simulated crowded environments with varying numbers of pedestrians

### In Autonomous Drones:
- **Dueling Double DQN** in AirSim/Unreal Engine — for drone interception, compared against standard DQN
- **MARL + Gaussian Processes (DQN-C51)** — for pollution plume characterization with a drone fleet, validated through simulations
- **D3QN with heuristic search and ε-greedy** — for path planning in dynamic environments with threats
- **DDPG with soft/hard margin rewards** — for vision-guided collision avoidance, tested in simulated indoor environments

### In ADAS:
- **GAN + LSTM (VILDS)** — tested under diverse road and weather conditions, evaluated on lane detection and departure warning accuracy
- **AVS-RL with CARLA + real drivers** — validated using data from wearable devices (Oura Ring) and CARLA simulator
- **DDPG in CoMoVe simulation** — for adaptive cruise control, compared to traditional ACC and CACC systems
- **SIFRCNN + RPN** — evaluated on KAIST, CityPerson, and Caltech datasets for nighttime pedestrian detection
