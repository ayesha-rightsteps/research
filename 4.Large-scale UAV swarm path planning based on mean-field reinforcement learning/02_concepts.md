# 02 — Key Concepts: Every Term Explained

---

## Core Domain Terms

---

## UAV (Unmanned Aerial Vehicle) ⭐

> **In one sentence:** A drone — an aircraft that flies without a human pilot onboard, controlled autonomously or remotely.

**The analogy:** Think of a military reconnaissance drone or a delivery drone. In this paper, each UAV is an autonomous agent that must navigate from a starting position to a target.

**Why it matters in this paper:** The paper trains 80 UAVs simultaneously to fly in coordinated formation through a battlefield environment. Each UAV makes its own decisions based on what it can locally observe.

**If sir asks you to define it, say:**
> "A UAV is an unmanned aircraft that operates without a human pilot onboard. In this paper, we have a swarm of 80 such drones that must autonomously navigate from start positions to assigned targets while avoiding no-fly zones and not colliding with each other."

---

## UAV Swarm

> **In one sentence:** A large group of UAVs working together as a coordinated team to accomplish a shared mission.

**The analogy:** Like a flock of birds, where each bird adjusts its flight based on its neighbors — except here, each drone is trying to reach a specific target while avoiding threats.

**Why it matters in this paper:** The paper specifically addresses *large-scale* swarms (80-120 drones) — a scale where most algorithms fail because the interaction complexity becomes unmanageable.

**If sir asks you to define it, say:**
> "A UAV swarm is a large group of drones that coordinate autonomously to complete a mission. The challenge is that coordinating 80+ drones simultaneously creates enormous computational complexity — this paper's main contribution is solving that scaling problem."

---

## No-Fly Zone (NFZ) ⭐

> **In one sentence:** A restricted area that UAVs must avoid — representing threats like enemy radar, anti-aircraft systems, or protected territory.

**The analogy:** Like a "keep out" zone on a map. If a drone enters one, it fails the mission (or is destroyed in a real scenario).

**Why it matters in this paper:** The 500×500m battlefield environment contains 20 NFZs. Avoiding them while also reaching targets and not colliding with other drones is the core three-way challenge of this paper.

**If sir asks you to define it, say:**
> "A no-fly zone, or NFZ, is a circular restricted area that UAVs must not enter. In this paper, the battlefield contains 20 static NFZs representing threats. One of the experiments also tests moving NFZs to simulate dynamic threats like enemy missiles or maneuvering aircraft."

---

## Path Planning

> **In one sentence:** The problem of finding a safe, efficient route from a starting point to a destination while avoiding obstacles.

**The analogy:** GPS navigation for drones — except instead of avoiding traffic, the drone avoids no-fly zones and other drones.

**Why it matters in this paper:** Each of the 80 UAVs must independently plan its path to its assigned target. The paper solves this using reinforcement learning rather than traditional planning algorithms.

---

## MARL (Multi-Agent Reinforcement Learning) ⭐

> **In one sentence:** A branch of RL where multiple agents learn simultaneously in a shared environment, each adapting to the others' behavior.

**The analogy:** Teaching a sports team to play together — each player learns not just to play well themselves, but to coordinate with teammates.

**Why it matters in this paper:** With 80 drones, you need MARL because each drone's actions affect all other drones. Using independent single-agent RL for each drone ignores these interactions, leading to collisions.

**If sir asks you to define it, say:**
> "Multi-Agent Reinforcement Learning is the framework where multiple agents learn simultaneously in the same environment. The challenge is that each agent's optimal behavior depends on what all other agents are doing — making the problem significantly harder than single-agent RL, especially at scale."

---

## Technical / Algorithm Terms

---

## DDPG (Deep Deterministic Policy Gradient) ⭐

> **In one sentence:** A deep reinforcement learning algorithm designed for continuous action spaces — it learns a deterministic policy that directly outputs the best action, not a probability distribution over actions.

**The analogy:** DDPG is like a self-driving car controller that directly outputs "steer 5° left, accelerate at 2 m/s²" rather than choosing from a menu of pre-set maneuvers.

**Why it matters in this paper:** UAVs need continuous control (smooth changes in speed and heading angle). DDPG handles this naturally. PO-WMFDDPG extends DDPG with mean field theory to handle the multi-agent case.

**If sir asks you to define it, say:**
> "DDPG stands for Deep Deterministic Policy Gradient. It's a reinforcement learning algorithm for continuous action spaces that uses two neural networks — an actor that outputs the action directly and a critic that evaluates how good that action was. The authors use it as the base for their PO-WMFDDPG algorithm because UAV control requires continuous speed and heading adjustments."

---

## PO-WMFDDPG ⭐

> **In one sentence:** The paper's novel algorithm — Partially Observable Weighted Mean Field Deep Deterministic Policy Gradient — which combines DDPG with mean field theory, local observability, and attention weighting for scalable swarm control.

**The analogy:** Instead of each drone tracking 79 others individually (impossible), each drone watches only its nearby neighbors and treats them as one averaged signal — but gives closer, more relevant neighbors more weight in that average.

**Why it matters in this paper:** This is the central contribution. Every other comparison in the paper exists to show how PO-WMFDDPG outperforms simpler alternatives (DDPG alone, or global mean-field DDPG).

**If sir asks you to define it, say:**
> "PO-WMFDDPG stands for Partially Observable Weighted Mean Field DDPG. It's this paper's novel algorithm. The 'PO' means each drone only observes neighbors within its communication range. The 'WMF' means neighboring drones are summarized into a single weighted average action — closer drones get higher weights — rather than modeling all N drones individually. DDPG provides the continuous action control. Together, these make large-scale swarm coordination computationally tractable."

---

## Mean Field Theory / Mean Field Game (MFG) ⭐

> **In one sentence:** A mathematical framework that approximates the collective behavior of N interacting agents as one agent interacting with a single "average agent" — the mean field — dramatically reducing computational complexity.

**The analogy:** Instead of tracking every individual water molecule in a river to predict where the water goes, you model the average flow. Mean field theory does this for agents: instead of N individual interactions, model one interaction with an averaged representative.

**Why it matters in this paper:** Without mean field, coordinating 80 drones requires modeling 80×79 = 6,320 pairwise interactions. With mean field, each drone models just one averaged neighbor action. This is the key that makes 80-drone training feasible.

**If sir asks you to define it, say:**
> "Mean field theory comes from physics — it's a way to approximate a large system of interacting particles by replacing all individual interactions with a single averaged interaction. In this paper, it means each drone doesn't need to track 79 individual neighbors. Instead, it computes one weighted average of their actions and responds to that. This collapses the N-squared interaction complexity into N times one."

---

## Weighted Mean Field (WMF)

> **In one sentence:** An extension of basic mean field where each neighboring agent's contribution to the average is weighted by relevance — typically by distance or attention — so closer agents matter more.

**The analogy:** When deciding what restaurant to go to, you ask 5 nearby friends (weighted heavily) rather than 50 acquaintances across the city (weighted lightly). Closer, more relevant opinions count more.

**Why it matters in this paper:** Basic MFDDPG (the comparison algorithm) weights all neighbors equally. PO-WMFDDPG uses attention weights — a drone 20m away influences the mean field more than a drone 180m away. This is why PO-WMFDDPG outperforms MFDDPG, especially as drone density increases.

---

## Multi-Head Attention Mechanism ⭐

> **In one sentence:** A neural network module that learns to assign different importance weights to different inputs — in this paper, it learns which neighboring drones matter most to each drone's decision.

**The analogy:** Like a person at a busy party who naturally focuses more on the person talking directly to them (high attention) than background conversations across the room (low attention). The mechanism learns who to pay attention to.

**Why it matters in this paper:** The attention module computes weights for each neighbor's contribution to the mean field. It uses 4 attention heads and 32-dimensional key/query vectors. Drones within tight formation or close collision range get high weights; distant drones get low weights. This is the "weighted" part of PO-WMFDDPG.

**If sir asks you to define it, say:**
> "Multi-head attention is a neural network module originally from transformer architectures. Here, it's used to assign a learned weight to each neighboring drone's action in the mean field calculation. Instead of treating all neighbors equally, the attention mechanism learns that closer, more directly relevant drones should influence the mean field more. The 'multi-head' means it computes 4 separate attention patterns simultaneously and combines them, capturing different types of relevance."

---

## POMDP (Partially Observable Markov Decision Process)

> **In one sentence:** An MDP where the agent cannot see the full environment state — it only observes partial information within its sensor range.

**The analogy:** Playing chess while only being able to see the pieces within 3 squares of your own king — you must make decisions without knowing the full board state.

**Why it matters in this paper:** Each drone has a communication range R_a. It only observes neighbors within that range, not the whole swarm. This partial observability is the "PO" in PO-WMFDDPG and makes the algorithm far more realistic than global-knowledge alternatives.

---

## CTDE (Centralized Training, Distributed Execution)

> **In one sentence:** A training paradigm where all agents share information and a global critic during training, but each agent runs independently with only its local information during deployment.

**The analogy:** A sports team practicing together with a coach who sees everything (centralized training) — but during the actual game, each player acts independently based on what they personally observe (distributed execution).

**Why it matters in this paper:** CTDE allows PO-WMFDDPG to train more efficiently (the global critic during training helps each agent learn from other agents' experiences), but the deployed system is realistic — each UAV acts on its own local observations.

---

## Actor-Critic Architecture

> **In one sentence:** A reinforcement learning design with two neural networks: the actor decides what action to take, and the critic evaluates how good that action was.

**The analogy:** An actor in a movie performs (the actor network outputs the action), and a director on set judges the performance (the critic network outputs the quality score, or Q-value).

**Why it matters in this paper:** DDPG uses an actor-critic framework. The actor network (16→64→128→32→2) outputs the two continuous control actions (linear and angular acceleration). The critic network (20→64→192→64→1) evaluates each state-action pair.

---

## Replay Buffer / Experience Replay

> **In one sentence:** A memory system that stores past state-action-reward-next_state tuples so the network can learn from randomly sampled past experiences, breaking the correlation between consecutive training samples.

**The analogy:** Like reviewing game footage from multiple past matches (not just the last game) to train — random sampling from a large pool of experiences leads to more stable, general learning.

**Why it matters in this paper:** PO-WMFDDPG uses a shared replay buffer (batch size 128) to train the actor and critic networks. This is standard DDPG practice but is explicitly mentioned as part of the CTDE training setup.

---

## Soft Update (Polyak Update)

> **In one sentence:** A technique where target network parameters are slowly blended toward the main network's parameters each step (rather than copying them all at once), preventing training instability.

**The formula:** θ_target ← τ·θ_main + (1−τ)·θ_target, where τ is a small number (like 0.005)

**Why it matters in this paper:** Both the actor and critic have target networks updated with soft updates. This is standard DDPG practice that prevents the Q-value oscillation that causes training divergence.

---

## Evaluation Terms

---

## Task Success Rate (SR)

> **In one sentence:** The percentage of UAVs that successfully reach their designated target without entering a no-fly zone or colliding with another drone.

**Why it matters in this paper:** This is the primary evaluation metric. PO-WMFDDPG achieves ~98% SR with 80 drones and maintains >90% SR with 120 drones. The competing algorithms collapse below this as drone count increases.

---

## Scalability Test

> **In one sentence:** An experiment that gradually increases the number of drones (from 20 to 120) to see at what point each algorithm's performance breaks down.

**Why it matters in this paper:** The scalability test is the paper's most critical experiment. It shows that PO-WMFDDPG maintains high SR all the way to 120 drones, while DDPG and MFDDPG collapse significantly earlier.

---

## NFZ Scalability Test

> **In one sentence:** An experiment that gradually increases the number of no-fly zones to test how much obstacle density each algorithm can handle before failing.

**Why it matters in this paper:** With up to 20 NFZs, PO-WMFDDPG stays near 98%. DDPG begins collapsing after 26 NFZs. This demonstrates robustness to varying threat density.

---

## Statistical / Mathematical Terms

---

## Markov Decision Process (MDP)

> **In one sentence:** A mathematical framework for sequential decision-making where the future depends only on the current state and action (not on the full history).

**Why it matters in this paper:** The single-agent version of this paper's problem would be an MDP. But because each drone's state affects others, the full problem is a multi-agent MDP — which is what MARL solves. With partial observability, it becomes a POMDP.

---

## Reward Function

> **In one sentence:** A mathematical formula that tells an agent how well it performed at each step — positive rewards for good behavior, negative for bad.

**This paper's reward structure:**

Long-term rewards:
- r_goal: +large reward for reaching target
- r_bound: −penalty for leaving flight boundaries
- r_crash: −penalty for entering NFZ or collision

Instant rewards:
- r_task = λ(1 − d_{t+1}/d_t) + η·cos(β_t)
  - d_{t+1}/d_t: ratio of new to old distance to target (< 1 = getting closer = positive reward)
  - cos(β_t): cosine of heading angle error (1 = facing target directly = maximum reward)
  - λ and η: weighting coefficients

**Why it matters in this paper:** The instant reward r_task provides dense feedback at every step — rewarding both closing distance to target AND proper heading alignment. This prevents sparse reward problems and guides drones to approach targets efficiently.

---

## Convergence

> **In one sentence:** The point at which a training algorithm's performance stabilizes and stops improving significantly — indicating the neural network has learned as much as it can from the current setup.

**Why it matters in this paper:** PO-WMFDDPG converges to ~98% SR by round 700 (of 1,000 total training rounds). The competing algorithms converge to lower values, with more instability (noisier learning curves).

---

## Communication Range (R_a)

> **In one sentence:** The maximum distance within which a drone can observe neighboring drones and receive their state/action information.

**Why it matters in this paper:** R_a defines the "local neighborhood" for each drone's partial observation. Drones outside R_a are invisible to a given drone. The mean field is computed only over observable neighbors within R_a, making the algorithm partial-observable rather than globally-observable.
