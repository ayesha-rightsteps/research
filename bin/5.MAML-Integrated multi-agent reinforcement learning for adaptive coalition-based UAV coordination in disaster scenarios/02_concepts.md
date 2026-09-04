# 02 — Key Concepts: Every Term Explained

---

## Core Domain Terms

---

## Heterogeneous UAV Swarm ⭐

> **In one sentence:** A group of drones where each drone has different capabilities — different speed, battery life, sensors, or payload capacity.

**The analogy:** Like a hospital emergency team where some members are surgeons, some are nurses, and some drive ambulances — each has different skills, and you need to assign the right person to the right task.

**Why it matters in this paper:** All 4 other papers in this folder assume all drones are identical. This paper is the first to handle mixed drone types — a drone with a thermal camera is assigned to search tasks, a fast drone is assigned to reconnaissance, a drone with a strong radio is assigned to communication relay. Coalition formation must respect these differences.

**If sir asks you to define it, say:**
> "A heterogeneous UAV swarm is a group of drones that are not all identical — they differ in speed, sensor type, battery capacity, or payload. This paper is specifically designed for this realistic scenario. Most other multi-UAV papers assume all drones are the same, which doesn't reflect real disaster deployments where you have mixed fleets."

---

## Coalition Formation ⭐

> **In one sentence:** The process of dynamically grouping drones into small teams, where each team is assigned to a specific task based on the combined capabilities of its members.

**The analogy:** Like forming project teams in a company — you group people with complementary skills to tackle a specific project. If one team member leaves (drone failure), you reform the team with the remaining members.

**Why it matters in this paper:** Instead of every drone acting alone or all drones working as one big group, RCTP forms coalitions — small teams matched to specific tasks. A search task might need a thermal drone + a fast mapping drone in the same coalition. When a drone fails, its coalition is automatically reformed.

**If sir asks you to define it, say:**
> "Coalition formation is the process of grouping drones into small teams, where each team is matched to a specific task based on combined capabilities. In this paper, coalitions are formed using resource-aware suitability scores and can be reformed automatically when drones fail, providing fault tolerance without a central controller."

---

## MAML (Model-Agnostic Meta-Learning) ⭐

> **In one sentence:** A training technique that teaches a model not to be good at one specific task, but to be good at *learning new tasks quickly* — after MAML training, only a few additional training steps are needed to adapt to any new scenario.

**The analogy:** Instead of training a student to know every answer, you train them to be a fast learner — after meta-training, they can read 3 pages of a new subject and already perform well, instead of needing 300 pages of study.

**Why it matters in this paper:** Disaster scenarios are unpredictable — every earthquake site, flood zone, or fire is different. You cannot train drones on the exact environment they'll face. MAML solves this: drones are trained across many varied disaster scenarios, producing a "meta-policy" that can be fine-tuned to any new disaster with only a few gradient updates. This is the key innovation that no other paper in this folder has.

**If sir asks you to define it, say:**
> "MAML stands for Model-Agnostic Meta-Learning. It's a training algorithm that optimizes the model's initial parameters to be a good starting point for learning any new task quickly. In this paper, the UAVs are meta-trained across diverse disaster scenarios so that when deployed in a new, unseen disaster, they only need a few gradient updates to adapt — rather than training from scratch. This rapid adaptation capability is critical for time-sensitive disaster response."

---

## MA-DDPG (Multi-Agent Deep Deterministic Policy Gradient) ⭐

> **In one sentence:** A multi-agent extension of DDPG where multiple agents each have their own actor and critic, and critics can access other agents' information during training.

**The analogy:** Each drone has its own driver (actor) making local decisions, but a shared coach (global critic during training) helps all drivers learn better by seeing the whole picture.

**Why it matters in this paper:** MA-DDPG handles the continuous-action control — smooth speed and direction changes — for each drone. MAML provides the fast-adaptation initialization, and MA-DDPG is the actual RL algorithm that executes within each scenario.

**If sir asks you to define it, say:**
> "MA-DDPG is Multi-Agent DDPG — it extends the single-agent DDPG algorithm to multiple agents. Each agent has its own actor network making local decisions, while during training, critics can access global information to produce better learning signals. In this paper, MA-DDPG handles the continuous path planning and coalition actions, while MAML provides the fast-adaptation initialization."

---

## RCTP Framework

> **In one sentence:** The paper's complete system — Resource-aware Coalition-based Task and Path-planning — combining MAML + MA-DDPG with coalition management, fault tolerance, and energy-aware routing.

**Why it matters in this paper:** RCTP is the name of the entire contribution. MAML and MA-DDPG are components; RCTP is the integrated framework that also adds coalition formation logic, suitability scoring, task reassignment, and communication modeling.

---

## Resource-Aware Suitability Score

> **In one sentence:** A score computed for each drone for each task, based on the drone's current resources (battery, capabilities) and the task requirements — used to decide which drones form which coalitions.

**The analogy:** Like a compatibility score on a job matching platform — a drone's "resume" (capabilities, battery, sensor) is matched against a task's "requirements," and the score determines the best match.

**Why it matters in this paper:** This score is updated online (continuously during the mission). When a drone fails, the scores are recomputed and tasks are reassigned to the best remaining drones automatically. This is the mechanism for fault tolerance and load balancing.

---

## Technical / Algorithm Terms

---

## Meta-Learning

> **In one sentence:** Learning how to learn — a training approach where the model optimizes itself to be a fast learner across many tasks, rather than mastering one specific task.

**The analogy:** The difference between cramming one exam (task-specific training) and developing good study habits that help you on any exam (meta-learning).

**Why it matters in this paper:** The disaster response domain requires rapid adaptation. Meta-learning is what enables RCTP to deploy in scenarios it hasn't specifically trained on.

---

## LoS / NLoS Communication (Line-of-Sight / Non-Line-of-Sight) ⭐

> **In one sentence:** LoS means a drone can communicate directly with another drone or ground station without obstruction; NLoS means a building, debris, or terrain blocks the direct signal, degrading communication quality.

**The analogy:** Like a phone call in an open field (LoS — clear signal) versus a call from inside a thick concrete building (NLoS — weak or dropped signal).

**Why it matters in this paper:** In disaster zones, collapsed buildings and rubble constantly block radio signals. RCTP explicitly models when communication switches between LoS and NLoS and adjusts drone coordination accordingly. No other paper in this folder models communication reliability.

**If sir asks about this, say:**
> "LoS means line-of-sight — the drone can communicate directly with clear radio signal. NLoS means non-line-of-sight — the signal is blocked by obstacles. In disaster zones with collapsed buildings, drones constantly switch between these modes. RCTP explicitly models this switching, which means its coordination algorithms degrade gracefully when communication is intermittent — unlike standard MARL approaches that assume perfect communication."

---

## Fault Tolerance

> **In one sentence:** The system's ability to continue functioning correctly when some components (drones) fail.

**Why it matters in this paper:** RCTP is designed so that if drones fail mid-mission, remaining drones automatically detect the failure, recompute suitability scores, reform coalitions, and continue the mission. This is the "fault tolerance" capability that makes the algorithm practically deployable.

---

## Decentralized Coordination

> **In one sentence:** Each drone makes its own decisions using only locally observable information — there is no central computer telling every drone what to do.

**Why it matters in this paper:** In a disaster zone, a central command node would be a single point of failure. RCTP is fully decentralized — each drone runs its own MAML-adapted policy and computes its own coalition assignments without needing to contact a central server.

---

## Evaluation Terms

---

## Task Success Rate

> **In one sentence:** The percentage of assigned tasks that are successfully completed by the UAV swarm.

**Why it matters in this paper:** RCTP achieves higher task success rates than PPO, DQN, and MA-DDPG — particularly under drone failure scenarios where baselines collapse.

---

## Mission Completion Time

> **In one sentence:** How long it takes the entire swarm to complete all assigned tasks.

**Why it matters in this paper:** RCTP completes missions 30–40% faster than baselines. In disaster response, this directly translates to survival rates — faster completion means earlier rescue.

---

## Energy Consumption

> **In one sentence:** Total battery power used by the swarm to complete the mission.

**Why it matters in this paper:** RCTP uses 10–20% less energy than baselines because of energy-aware path planning — routing drones to minimize battery drain while still completing tasks efficiently.

---

## Per-Agent Inference Time

> **In one sentence:** How many milliseconds it takes for each drone to compute its next action using its policy network.

**Why it matters in this paper:** RCTP achieves millisecond-level inference, meaning it is fast enough to run in real time on actual drone hardware — a practical requirement that many RL papers fail to address.

---

## Comparison Baselines

**PPO (Proximal Policy Optimization):** A popular policy gradient RL algorithm. Works well for single agents but struggles with multi-agent coordination and heterogeneity.

**DQN (Deep Q-Network):** Discrete-action RL algorithm used in Papers 2 and 3. Cannot handle continuous drone control as naturally as DDPG-based methods.

**MA-DDPG (standalone):** The multi-agent DDPG without the MAML meta-learning layer. Used to show that the MAML component adds meaningful improvement.
