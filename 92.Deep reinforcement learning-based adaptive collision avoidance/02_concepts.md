# 02 — Key Concepts Explained

Every technical term, acronym, model name, and metric in this paper — explained so clearly you can define them confidently out loud.

---

## CORE DOMAIN TERMS

---

## UAV (Unmanned Aerial Vehicle) ⭐

> **In one sentence:** A drone — any aircraft that flies without a human pilot on board, controlled remotely or autonomously.

**The analogy:** Think of it as a very sophisticated remote-controlled airplane that can make its own decisions in flight.

**Why it matters in this paper:** The UAV is the "agent" — the learner. The entire paper is about teaching a UAV to dodge other aircraft by itself, without being told what to do.

**If sir asks you to define it, say:**
> "A UAV is an unmanned aerial vehicle — an aircraft that operates without a pilot on board. In this paper, the UAV is the autonomous agent being trained to avoid collisions in a shared military airspace."

---

## Joint Operational Airspace

> **In one sentence:** A shared airspace where aircraft from different military units — both manned jets and drones — fly simultaneously on different missions without a shared communication system.

**The analogy:** Imagine a highway where cars from different cities are driving with no shared radio channel or GPS coordination — each driver only sees what is immediately around them.

**Why it matters in this paper:** This is the exact setting the paper targets. It is more difficult than normal airspace because there is no central coordinator sharing information, making the collision avoidance problem much harder.

**If sir asks you to define it, say:**
> "Joint operational airspace refers to a battlefield airspace where manned aircraft and UAVs from different combat units operate simultaneously without real-time information sharing. The UAV must rely entirely on its own sensors to detect and avoid threats."

---

## Collision Avoidance

> **In one sentence:** The process by which an aircraft automatically detects nearby aircraft that could collide with it and maneuvers to prevent the collision.

**The analogy:** Like a car's automatic emergency braking system, but for aircraft in 3D space with multiple threats.

**Why it matters in this paper:** This is the core task being solved. The UAV must avoid collisions while still completing its mission.

**If sir asks you to define it, say:**
> "Collision avoidance is the ability of an aircraft to autonomously detect potential mid-air collisions and execute maneuvers to prevent them. In this paper, the UAV learns this skill through reinforcement learning."

---

## Partial Observability

> **In one sentence:** A situation where the agent cannot see the full state of the environment — it only has limited, local sensor information.

**The analogy:** Driving at night in fog — you can see what is immediately in front of your headlights but not what is a kilometer ahead or behind you.

**Why it matters in this paper:** UAVs in a battlefield cannot see all aircraft in the airspace. They can only detect aircraft within their sensor range (4,000 meters radius), and even that information has noise and uncertainty. The paper designs the entire observation system around this limitation.

**If sir asks you to define it, say:**
> "Partial observability means the UAV cannot access the global state of the airspace — it only perceives what its onboard sensors can detect within a limited range. This makes decision-making much harder because the UAV must act on incomplete information."

---

## Heterogeneous Aircraft

> **In one sentence:** Aircraft of different types with different speeds, sizes, maneuverability, and sensitivity to wind — specifically manned jets versus unmanned drones.

**The analogy:** Like mixing trucks, motorcycles, and bicycles on the same road — they all move differently and have different safety distances.

**Why it matters in this paper:** Most previous research assumed all aircraft are the same type. This paper explicitly models the difference between manned aircraft (faster: 80–160 m/s, less sensitive to wind, larger warning zones of 800 m) and UAVs (60–110 m/s, more sensitive to wind, smaller warning zones of 400 m). This makes the problem much more realistic.

**If sir asks you to define it, say:**
> "Heterogeneous aircraft means the airspace contains different types of aircraft with different flight characteristics. In this paper, manned aircraft fly faster, have larger safety zones, and are less affected by wind than UAVs, so the collision avoidance strategy must treat them differently."

---

## MDP (Markov Decision Process) ⭐

> **In one sentence:** A mathematical framework for modeling decision-making problems where an agent takes actions in an environment, receives rewards, and the next state depends only on the current state and action.

**The analogy:** Think of a chess game — at each move (action), the board state changes (new state), and you gain or lose points (reward). What matters is only the current board position, not every move in history.

**Why it matters in this paper:** The entire UAV collision avoidance problem is formulated as an MDP. The observation is the state, the maneuver is the action, the collision penalty or goal reward is the reward signal, and the UAV is the agent. This formulation is what allows deep reinforcement learning to be applied.

**If sir asks you to define it, say:**
> "An MDP is a mathematical model where an agent observes a state, takes an action, receives a reward, and transitions to a new state — and this cycle repeats. In this paper, the UAV collision avoidance problem is formulated as an MDP so that the agent can learn optimal strategies through interaction with the environment."

---

## TECHNICAL AND ALGORITHM TERMS

---

## DRL / Deep Reinforcement Learning ⭐

> **In one sentence:** A machine learning approach where a neural network learns to make decisions by trial and error, receiving rewards for good actions and penalties for bad ones.

**The analogy:** Like training a dog with treats and scolding — give the dog a treat when it does the right thing, say no when it does the wrong thing, and eventually it learns the right behavior. Deep reinforcement learning does this but with a neural network instead of a dog brain.

**Why it matters in this paper:** DRL is the entire methodology. Instead of programming rules by hand ("if aircraft is 500m away, turn right"), the UAV learns the best maneuver policy by itself through millions of simulated interactions.

**If sir asks you to define it, say:**
> "Deep reinforcement learning combines deep neural networks with reinforcement learning principles. The agent learns by exploring an environment, receiving positive or negative rewards for its actions, and gradually optimizing its policy to maximize long-term rewards. In this paper, the UAV uses DRL to learn when and how to maneuver to avoid collisions."

---

## DQN (Deep Q-Network) ⭐

> **In one sentence:** A deep reinforcement learning algorithm that uses a neural network to estimate the value (called Q-value) of taking each possible action in a given state.

**The analogy:** Imagine you are at a fork in a road and you want to estimate how good each path is. DQN is like an experience-trained advisor who says "path A scores 8 out of 10, path B scores 3 out of 10" — and you always pick the highest score.

**Why it matters in this paper:** DQN is the baseline algorithm the authors build upon. All improvements (DDQN, Dueling, D3QN, HPER-D3QN) are extensions of DQN. The paper compares HPER-D3QN against basic DQN to show how much the improvements help.

**If sir asks you to define it, say:**
> "DQN is a classic deep reinforcement learning algorithm that uses a neural network to estimate Q-values — the expected future reward for each action from a given state. The agent always picks the action with the highest Q-value. In this paper, basic DQN is the weakest baseline method that HPER-D3QN is compared against."

---

## DDQN (Double Deep Q-Network)

> **In one sentence:** An improved version of DQN that uses two separate networks to prevent overestimating how good actions are, leading to more accurate and stable learning.

**The analogy:** Instead of asking one person to both choose the best restaurant AND rate how good it is (which leads to bias), you ask one person to choose and another person to rate — you get a more honest evaluation.

**Why it matters in this paper:** DDQN's update rule is incorporated into the D3QN foundation used in this paper. It is one component of the final HPER-D3QN algorithm.

**If sir asks you to define it, say:**
> "DDQN reduces overoptimism in Q-value estimation by using two networks: one network selects the best action, and a separate target network evaluates how good that action is. This separation leads to more stable and accurate learning than standard DQN."

---

## Dueling DQN

> **In one sentence:** A network architecture that separately estimates how good a state is (state value) and how much better each action is compared to average (action advantage), then combines them to get the final Q-value.

**The analogy:** When rating a movie, separately scoring "is this a good genre to begin with?" and "is this particular film better than average in that genre?" gives a richer evaluation than one single score.

**Why it matters in this paper:** The dueling architecture helps the UAV make better decisions even in states where different actions have similar outcomes — which is common during normal cruise flight when no threats are nearby.

**If sir asks you to define it, say:**
> "Dueling DQN decomposes the Q-value into two parts: a state value function V(s) that estimates how good it is to be in the current state, and an advantage function A(s,a) that measures the benefit of each specific action over the average. Combining these gives more accurate Q-value estimates."

---

## D3QN (Double-Dueling Deep Q-Network) ⭐

> **In one sentence:** A neural network that combines both DDQN (to prevent overestimation) and the Dueling architecture (to better evaluate states and actions) into one stronger learning system.

**The analogy:** D3QN is like combining both upgrades on a car — better brakes (Double DQN) AND better suspension (Dueling) — instead of choosing just one.

**Why it matters in this paper:** D3QN is the backbone neural network used in the paper's final algorithm. The authors add DTPA and HPER on top of D3QN to create HPER-D3QN.

**If sir asks you to define it, say:**
> "D3QN combines two improvements over basic DQN: the Double DQN update rule to reduce overestimation of Q-values, and the dueling network architecture to separately estimate state values and action advantages. In this paper, D3QN is the base network that is enhanced with the DTPA and HPER mechanisms."

---

## HPER (Hierarchical Prioritized Experience Replay) ⭐

> **In one sentence:** A mechanism that classifies training experiences into three priority levels — high, medium, and low — and samples more frequently from the more important experiences to make training faster and better.

**The analogy:** When studying for an exam, you should spend more time on topics you keep getting wrong (high priority) and less time on topics you have already mastered (low priority). HPER applies this same logic to the AI's training data.

**Why it matters in this paper:** This is the paper's most important innovation. The ablation study shows that removing HPER causes a 9.27% drop in success rate and an 87.26% surge in dangerous proximity events — the largest degradation of any component. HPER makes the system learn dramatically faster and perform better.

**If sir asks you to define it, say:**
> "HPER is a novel experience replay mechanism proposed in this paper that divides training experiences into three hierarchical priority layers. High-priority experiences involving collisions, boundary violations, or destination arrivals are sampled most frequently because they are rare but critical for learning. This targeted sampling accelerates policy convergence and improves the agent's collision avoidance performance."

---

## HPER-D3QN

> **In one sentence:** The complete proposed algorithm in this paper — a D3QN neural network enhanced with both DTPA (for smart threat identification) and HPER (for efficient training).

**The analogy:** Think of D3QN as the engine of a race car. DTPA is the advanced GPS navigation system, and HPER is the expert driving coach. Together they make the car not just fast, but smart and well-trained.

**Why it matters in this paper:** This is the paper's main contribution — the full algorithm that outperforms all baseline methods across every tested condition.

**If sir asks you to define it, say:**
> "HPER-D3QN is the proposed algorithm combining a Double-Dueling Deep Q-Network backbone with two key innovations: the Dynamic Threat Prioritization Assessment for intelligent intruder selection, and Hierarchical Prioritized Experience Replay for efficient training. It is the complete system validated in the paper's experiments."

---

## DTPA (Dynamic Threat Prioritization Assessment)

> **In one sentence:** An algorithm that calculates a threat score for every detected aircraft using three factors — time to collision, distance at closest approach, and aircraft type — then selects the most dangerous one in each sensor sector.

**The analogy:** Instead of panicking about the closest car in traffic (which might be moving away from you), DTPA asks: which car is heading toward you fastest, from what direction, and how big is it? That gives a much smarter danger ranking.

**Why it matters in this paper:** Previous methods only used Euclidean distance to rank threats. DTPA is more realistic because a fast manned jet that is 800 meters away might be a greater threat than a slow UAV that is 300 meters away. The ablation study shows removing DTPA causes an 8.98% drop in success rate.

**If sir asks you to define it, say:**
> "DTPA is a novel threat assessment algorithm proposed in this paper. For each detected aircraft, it computes a weighted score combining time to closest approach, distance at closest approach, and aircraft type. The aircraft with the highest score in each detection sector is selected as the intruder that the UAV monitors and avoids."

---

## Experience Replay

> **In one sentence:** A training technique where the agent stores past interactions (state, action, reward, next state) in a memory buffer and randomly re-samples them during training to learn more efficiently.

**The analogy:** Like reviewing your old exam papers while studying — instead of only learning from today's practice, you revisit past mistakes repeatedly until you truly understand them.

**Why it matters in this paper:** Experience replay is the standard mechanism in DQN. The paper's HPER improves upon it by making the replay non-random and priority-based instead.

**If sir asks you to define it, say:**
> "Experience replay stores each interaction the agent has with the environment as a tuple of observation, action, reward, and next observation. During training, random samples from this stored memory are used to update the neural network. This breaks the correlation between consecutive training samples and improves data efficiency."

---

## PER (Prioritized Experience Replay)

> **In one sentence:** A version of experience replay that samples experiences more frequently when they have a high TD error — meaning the agent was surprised by that outcome.

**The analogy:** Like a student who studies harder on questions they answered wrongly — you spend more time on what you got wrong because those are the most informative.

**Why it matters in this paper:** PER-D3QN is one of the baseline methods compared against HPER-D3QN. HPER outperforms PER because HPER adds the hierarchical categorization layer on top of TD-error-based prioritization, giving two levels of prioritization instead of one.

**If sir asks you to define it, say:**
> "PER samples training experiences proportional to their Temporal-Difference error — experiences where the agent's prediction was furthest from reality are sampled most often. HPER builds on PER by adding a hierarchical layer that classifies experiences by scenario type before applying TD-error prioritization within each layer."

---

## TD Error (Temporal-Difference Error)

> **In one sentence:** The difference between what the agent predicted as the Q-value and what the Q-value actually turned out to be — a measure of how "surprising" an experience was.

**The analogy:** If you thought a restaurant would be rated 7 out of 10 but it turned out to be 10 out of 10, your prediction error was 3. A high TD error means you were very wrong and need to learn more from that experience.

**Why it matters in this paper:** TD error is used within each HPER layer to further prioritize individual experiences. Higher TD error means the experience is more informative for learning.

**If sir asks you to define it, say:**
> "TD error is the difference between the predicted Q-value and the actual target Q-value computed using the Bellman equation. A larger TD error means the agent was more wrong about that situation. In this paper, HPER uses TD error to rank experiences within each priority layer during sampling."

---

## Q-Value (Action-Value Function)

> **In one sentence:** A number that estimates the total expected future reward the agent will receive if it takes a specific action in a specific state and then follows its current policy.

**The analogy:** Like a score on a GPS map — this path scores 85, that path scores 40 — and you always want to take the highest-scored path.

**Why it matters in this paper:** Q-values are what the neural network learns to predict. At each time step, the network outputs Q-values for all 9 possible maneuver actions, and the UAV picks the action with the highest Q-value.

**If sir asks you to define it, say:**
> "A Q-value estimates the long-term reward for taking a specific action in a given state. The D3QN network outputs a Q-value for each of the 9 possible UAV maneuvers, and the agent selects the maneuver with the highest Q-value as its action."

---

## Epsilon-Greedy Policy

> **In one sentence:** A training strategy where the agent sometimes picks a random action (to explore and discover new strategies) and sometimes picks the best known action (to exploit what it has learned).

**The analogy:** Like a food explorer who sometimes tries a completely new restaurant (exploration) and sometimes goes to their favorite (exploitation) — balancing discovery and safety.

**Why it matters in this paper:** The UAV uses an epsilon-greedy policy during training, with epsilon decreasing from 0.995 to 0.001 over 30,000 episodes — starting very exploratory and gradually becoming more decisive.

**If sir asks you to define it, say:**
> "The epsilon-greedy policy balances exploration and exploitation during training. With probability epsilon the agent chooses a random action to discover new strategies, and with probability 1 minus epsilon it chooses the action with the highest Q-value. Epsilon starts high and decreases over training, shifting from exploration to exploitation."

---

## Sector-Based Partial Observation Model

> **In one sentence:** A method of organizing the UAV's sensing by dividing the detection circle around it into K equal-angle slices (sectors), monitoring one threat per sector.

**The analogy:** Like dividing a clock face into 8 pie slices. Instead of trying to track all aircraft in all directions at once, you assign one "most dangerous aircraft" to each slice and monitor that one.

**Why it matters in this paper:** This design makes the observation space fixed-dimension (no matter how many aircraft are around, the observation has exactly K intruder slots), which is necessary for neural networks to function properly. It also reduces computational complexity.

**If sir asks you to define it, say:**
> "The sector-based partial observation model divides the UAV's detection range into 8 equal sectors. Within each sector, the DTPA algorithm identifies the most threatening aircraft as the intruder for that sector. This gives the UAV a structured, fixed-size observation regardless of how many aircraft are present."

---

## CPA (Closest Point of Approach)

> **In one sentence:** The future moment in time when two aircraft will be closest to each other if they both continue on their current paths.

**The analogy:** Like predicting the exact moment two cars driving toward an intersection will be closest to each other, based on their current speeds and directions.

**Why it matters in this paper:** CPA calculations are the foundation of the DTPA threat scoring system. Two key metrics come from CPA: TCPA and DCPA.

**If sir asks you to define it, say:**
> "The Closest Point of Approach is the point where two aircraft are predicted to be closest to each other based on their current velocities. It is used to calculate TCPA and DCPA, which are the main inputs to the DTPA threat assessment algorithm."

---

## TCPA (Time to Closest Point of Approach)

> **In one sentence:** How many seconds until two aircraft will be at their closest point to each other, given their current velocities.

**The analogy:** If two cars are heading toward the same intersection from different directions, TCPA is how many seconds until they are at their closest point.

**Why it matters in this paper:** A small TCPA means a collision is imminent — the aircraft are converging quickly. TCPA gets a weight of 0.4 in the DTPA scoring formula, making it one of the two most important threat indicators.

**If sir asks you to define it, say:**
> "TCPA is the time remaining until two aircraft reach their closest approach point. A small TCPA indicates an imminent threat. In the DTPA algorithm, TCPA is normalized and weighted at 0.4 to contribute to the overall threat score for each detected aircraft."

---

## DCPA (Distance at Closest Point of Approach)

> **In one sentence:** The predicted minimum distance between two aircraft when they reach their closest point, assuming no course change.

**The analogy:** Like predicting how close two cars will pass each other at an intersection — if they are on a collision course, DCPA is near zero.

**Why it matters in this paper:** A small DCPA means the two aircraft will nearly collide if neither changes course. Like TCPA, it receives a weight of 0.4 in the DTPA formula.

**If sir asks you to define it, say:**
> "DCPA is the minimum distance predicted between two aircraft at their closest approach point. A small DCPA means the aircraft are on a near-collision course. It receives equal weight to TCPA in the DTPA threat scoring formula because both time and distance of closest approach determine collision risk."

---

## Dual-Layer Safety Protection Interval Model

> **In one sentence:** A two-ring safety system around each aircraft: an inner "protected zone" (collision if entered) and an outer "warning zone" (alert if entered).

**The analogy:** Like a nuclear plant's two perimeter fences — crossing the outer fence triggers a warning, crossing the inner fence is the actual danger zone.

**Why it matters in this paper:** The paper uses this model to give the UAV graduated feedback: it gets a smaller penalty for entering a warning zone (r_w = -0.5) and a larger penalty for actual collision (r_c = -1). Manned aircraft have a larger warning zone (800 m) than UAVs (400 m).

**If sir asks you to define it, say:**
> "Each aircraft has two concentric safety zones. The inner protected zone has radius 150 meters — entering it counts as a collision. The outer warning zone is 400 meters for UAVs and 800 meters for manned aircraft. Entering the warning zone triggers a penalty that encourages the UAV to leave dangerous proximity early."

---

## Dynamic Wind Field Model

> **In one sentence:** A mathematical model that represents how wind speed and direction change periodically over time using a sinusoidal function.

**The analogy:** Like ocean waves — the wind's strength and direction oscillate up and down with a regular period, not staying constant.

**Why it matters in this paper:** Wind is a key source of uncertainty. UAVs are more sensitive to wind than manned aircraft (sensitivity coefficient η_UAV = 1.0 versus η_manned = 0.8), so the same wind affects them differently. The dynamic wind field is incorporated into the joint error model that makes the simulation realistic.

**If sir asks you to define it, say:**
> "The dynamic wind field model uses sinusoidal functions to represent periodic variations in wind speed and direction. UAVs are assigned a higher wind sensitivity coefficient than manned aircraft, reflecting their greater susceptibility to wind disturbances. This creates realistic uncertainty in the aircraft's actual ground speed and heading."

---

## Wind Field Sensitivity Weighting Coefficient (η_type)

> **In one sentence:** A number that captures how much each type of aircraft is affected by wind — UAVs have η = 1.0 and manned aircraft have η = 0.8, meaning UAVs are more wind-affected.

**Why it matters in this paper:** This coefficient allows the simulation to model heterogeneous aircraft behavior realistically. A lighter, slower UAV is more easily pushed off course by wind than a heavy manned jet.

---

## EVALUATION TERMS

---

## Success Rate

> **In one sentence:** The percentage of test episodes in which the UAV successfully avoids all collisions AND reaches its mission destination.

**The analogy:** Like a test score — out of 300 simulation runs, how many did the UAV pass completely?

**Why it matters in this paper:** This is the primary performance metric. HPER-D3QN achieves 96.28% in 25-aircraft scenarios versus 91.84% for DQN.

**If sir asks you to define it, say:**
> "Success rate is defined as the proportion of test episodes where the agent avoids all collisions and reaches its mission destination. It is the main metric used to compare all methods in the paper, evaluated across 300 simulation runs repeated 10 times for each scenario configuration."

---

## FHP (Frequency of Hazardous Proximity)

> **In one sentence:** The average number of times per episode the UAV enters the warning zone of another aircraft — a measure of how close calls are happening even when there is no outright collision.

**The analogy:** Like counting near-misses on a highway — even if no accident happens, a high number of near-misses tells you the driver is taking too many risks.

**Why it matters in this paper:** FHP captures dangerous behavior that success rate might miss. A method that barely avoids collisions by staying in warning zones all the time would have a high FHP even if success rate looks acceptable.

**If sir asks you to define it, say:**
> "FHP measures how frequently the UAV enters the warning zone of another aircraft per episode, regardless of whether a collision occurs. It captures risky close calls that success rate alone does not reflect. HPER-D3QN consistently achieves the lowest FHP across all tested conditions."

---

## Task Completion Time

> **In one sentence:** The average number of seconds the UAV takes to navigate from its starting position to its mission destination.

**Why it matters in this paper:** A faster completion time means the UAV is finding efficient paths rather than making excessive detours. HPER-D3QN achieves shorter completion times than all baselines.

---

## STATISTICAL AND MATHEMATICAL TERMS

---

## Discount Factor (γ)

> **In one sentence:** A number between 0 and 1 that controls how much the agent values immediate rewards versus future rewards — set to 0.99 in this paper.

**The analogy:** Like how most people value 100 dollars today more than 100 dollars next year. A discount factor of 0.99 means the agent still values future rewards almost as much as immediate ones.

**Why it matters in this paper:** A high γ = 0.99 means the UAV plans for long-term mission success, not just short-term avoidance.

---

## Learning Rate (α)

> **In one sentence:** How large a step the neural network takes toward updating its weights based on each new batch of experience — set to 0.0001 in this paper.

**The analogy:** Like the size of steps when adjusting a dial — too large and you overshoot the right setting, too small and you never get there.

---

## Ablation Study

> **In one sentence:** An experiment where individual components of a system are removed one at a time to measure how much each component contributes to overall performance.

**The analogy:** Like testing a recipe by leaving out one ingredient at a time — first without salt, then without sugar — to see which ingredient matters most.

**Why it matters in this paper:** The ablation study in Section 4.3.5 tests four variants: No DTPA, No HPER, No Dueling, No Double — confirming that HPER and DTPA are the most critical components.

**If sir asks you to define it, say:**
> "An ablation study systematically removes components of the proposed algorithm one at a time to measure their individual contributions to performance. In this paper, the ablation study shows that removing HPER causes the biggest performance drop (9.27% success rate loss, 87.26% FHP increase), confirming it as the most important innovation."

---

## FIFO (First-In, First-Out)

> **In one sentence:** A strategy for managing a memory buffer where the oldest stored experience is removed first when the buffer is full.

**Why it matters in this paper:** HPER uses FIFO within each priority layer to ensure fresh experiences replace old ones while maintaining the hierarchical structure.

---

## α_PER (PER Exponent)

> **In one sentence:** A parameter that controls how much the TD error influences the sampling probability of an experience — set to 0.5 in this paper.

**Why it matters in this paper:** α_PER = 0.5 means sampling is a balanced mix of pure priority-based (α=1) and uniform random (α=0), preventing the agent from ignoring lower-priority experiences entirely.

---

## DATASETS AND PLATFORMS

---

## PyGame (Training Environment)

> **In one sentence:** A Python graphics library used to build the 2D simulation environment where the UAV is trained.

**Why it matters in this paper:** The authors built a custom 30 km × 30 km joint airspace simulator using PyGame as the training environment for the HPER-D3QN agent.

---

## PyTorch

> **In one sentence:** An open-source Python machine learning library used to build and train the neural networks in this paper.

**Why it matters in this paper:** The D3QN network was implemented and trained using PyTorch on a TITAN RTX GPU.

---

## TITAN RTX GPU

> **In one sentence:** A high-performance graphics processing unit manufactured by NVIDIA, used to accelerate neural network training.

**Why it matters in this paper:** All model training was performed on a TITAN RTX GPU — this is the hardware used to run the experiments.

---

## Unity3D (High-Fidelity Simulation Platform)

> **In one sentence:** A professional 3D game engine repurposed as a high-fidelity battlefield airspace simulation system to test the trained model.

**Why it matters in this paper:** The final transfer experiments were conducted on a Unity3D-based platform to validate that the HPER-D3QN algorithm generalizes beyond the PyGame training environment. This is the paper's most important generalization test.

**If sir asks you to define it, say:**
> "Unity3D is a 3D game development engine used here to build a high-fidelity battlefield simulation system. The trained HPER-D3QN model was transferred to this platform and successfully avoided collisions with manned aircraft and other UAVs in realistic 3D scenarios, demonstrating the algorithm's practical applicability."

---

## Live-Virtual-Constructive (LVC) Framework

> **In one sentence:** A military simulation framework that combines real physical assets (Live), simulated platforms (Virtual), and computer-generated forces (Constructive) for integrated training and testing.

**Why it matters in this paper:** The authors mention LVC as the target framework for future hardware-in-the-loop and real flight tests — the next step beyond simulation validation.

---

## BASELINE METHODS MENTIONED

| Method | What it is |
|--------|-----------|
| DQN | Basic Deep Q-Network — simplest baseline |
| DDQN | Double DQN — reduces Q-value overestimation |
| Dueling DQN | Splits Q into state value + action advantage |
| D3QN | Combines DDQN + Dueling |
| PER-D3QN | D3QN with standard Prioritized Experience Replay |
| HPER-D3QN | Paper's proposed method — best performer |
| Rule-Based (NASA DO-365C) | Predefined rules from NASA MOPS standard |
| DP-Based (ACAS Xu) | Dynamic programming-based collision avoidance |
