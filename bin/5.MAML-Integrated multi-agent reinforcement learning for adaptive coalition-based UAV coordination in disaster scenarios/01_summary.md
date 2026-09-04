# 01 — Full Paper Summary

---

## Paper Identity

**Full Title:** MAML-Integrated multi-agent reinforcement learning for adaptive coalition-based UAV coordination in disaster scenarios

**Authors:** Sabitri Poudel, Sangman Moh (Corresponding author)
**Affiliation:** Department of Computer Engineering, Chosun University, Gwangju 61452, South Korea

**Venue:** Internet of Things (Elsevier), Volume 37, Article 101930 (2026)
**DOI:** 10.1016/j.iot.2026.101930
**Published online:** 24 March 2026 | Published in issue: May 2026

**Keywords:** UAV swarm, UAV coordination, Multi-agent reinforcement learning, Model-agnostic meta-learning, Coalition formation, Task assignment, Path planning

**Research Domain:** Multi-Agent Reinforcement Learning (MARL) + Meta-Learning → Heterogeneous UAV Swarm Coordination → Disaster Response

---

## The Problem

Think about a disaster scenario — a major earthquake has just hit a city. Emergency teams need to deploy a fleet of UAV drones immediately to search for survivors, map damaged areas, and relay communication for rescue teams on the ground. The drones are not all the same: some are fast scouts with cameras, some carry heavier sensors, some have longer battery life. You have maybe 30 drones and dozens of tasks spread across a devastated urban landscape.

Now the real problems begin.

**The environment is completely new.** The drones have never seen this specific city in this specific state of destruction. Roads are blocked, buildings have collapsed, the airspace is full of smoke and debris. Whatever they learned in training, they now need to apply to a scenario they have never encountered before. Algorithms that need thousands of training episodes to adapt to new environments are useless in a disaster — there is no time.

**The drones are all different.** A fast lightweight scout drone cannot carry heavy imaging equipment. A heavy-payload drone cannot hover in tight spaces. Assigning the right drone to the right task is itself a complex optimization problem that must be solved in real time as conditions change. The other papers in this folder either assume all drones are identical (Papers 2, 3, 4) or only have one drone (Papers 1, 3) — none of them handle mixed fleets.

**Communication is unreliable.** In a disaster zone, buildings block radio signals. Drones switch between line-of-sight (LoS) and non-line-of-sight (NLoS) communication constantly. Algorithms that assume perfect, instant communication between all agents — like standard MARL approaches — fail when the network is intermittent.

**Drones will fail.** Batteries die, motors malfunction, drones get damaged. When a drone drops out mid-mission, its assigned tasks need to be immediately redistributed to surviving drones. Most MARL papers assume all agents complete the episode — no dropouts. This assumption is unrealistic.

**The sensors are noisy.** Real drones in smoke-filled, cluttered environments get uncertain, noisy position and target readings. Most simulated RL training uses clean, perfect sensor data, then fails catastrophically when deployed in real conditions.

Existing solutions all fail on at least one of these five fronts: standard MARL algorithms (MA-DDPG alone, PPO, DQN) cannot adapt quickly to new scenarios and cannot handle heterogeneity. Meta-learning methods exist but were designed for single-agent settings. Coalition formation algorithms exist but don't integrate with path planning. No single framework previously combined all five challenges simultaneously.

---

## The Proposed Solution

The authors propose **RCTP** — Resource-aware Coalition-based Task and Path-planning framework.

RCTP is built on two pillars working together:

**Pillar 1: MAML (Model-Agnostic Meta-Learning)**
MAML is a meta-learning algorithm that trains the drones not to be good at one specific scenario, but to be good at *learning new scenarios fast*. After MAML training, a drone only needs a few gradient updates (a tiny amount of new training) to adapt its policy to a brand-new disaster environment it has never seen before. This is the "rapid adaptation" capability. In the context of disaster response, where every situation is different, this is critical.

**Pillar 2: MA-DDPG (Multi-Agent Deep Deterministic Policy Gradient)**
MA-DDPG handles the actual continuous control decisions — what speed, what direction, how to form coalitions, how to assign tasks. It produces smooth, continuous actions suited for real UAV flight dynamics.

**The Coalition Mechanism:**
Rather than every drone acting independently, RCTP groups drones into *coalitions* — small teams assigned to specific tasks. Coalition formation is guided by *resource-aware suitability scores* — a score computed for each drone based on its current capabilities (battery, speed, sensor type) and the task requirements. These scores are updated online (continuously during the mission), so if a drone fails, its coalition automatically reforms with the remaining drones. This enables fault tolerance and load balancing without a central controller.

**What makes this different from everything else:**
- Unlike Papers 2 and 4: explicitly handles heterogeneous drones with different capabilities
- Unlike Papers 1, 2, 3, 4: uses meta-learning so the policy can rapidly adapt to unseen scenarios
- Unlike all other papers: models drone failures and automatic task reassignment
- Unlike all other papers: explicitly models intermittent LoS/NLoS communication
- Unlike all other papers: application is disaster response, not military path planning

---

## The Method (in one paragraph)

The RCTP framework models the UAV coordination problem as a decentralized MARL problem with heterogeneous agents. MAML pre-trains a meta-policy across a distribution of disaster scenarios, so each UAV starts from a policy that is close to optimal for any new scenario and only needs a few gradient steps to fine-tune. During a mission, each UAV computes a resource-aware suitability score based on its current battery level, sensor type, and proximity to each task — this score determines coalition membership and task assignments. MA-DDPG handles the continuous path planning, coalition formation, and energy-aware movement decisions. The system explicitly models LoS/NLoS communication switching, meaning drones adapt their coordination based on whether they can currently communicate directly. When a drone fails, the suitability scores are recomputed and tasks are automatically reassigned to surviving coalition members. Simulations test 10–30 heterogeneous UAVs across scenarios with dynamic obstacles, noisy sensors, and multiple drone failures.

---

## The Key Results

**1. 30–40% faster mission completion compared to PPO, DQN, and MA-DDPG baselines.**
RCTP completes the same disaster response missions significantly faster than all three comparison algorithms. This is the paper's headline result.

*What this means:* In time-critical disaster response, faster mission completion directly translates to more survivors found. A 30–40% reduction in mission time is not a marginal improvement.

**2. 10–20% lower energy consumption.**
RCTP's energy-aware path planning and coalition formation use significantly less battery power per mission compared to baselines.

*What this means:* Lower energy consumption means drones can cover more area per charge cycle, or stay airborne longer — critical for extended disaster operations where recharging is difficult.

**3. Higher task success rates under drone failures.**
When drones fail mid-mission, RCTP's automatic coalition reformation and task reassignment enables surviving drones to complete the mission at higher success rates than baselines, which either fail or require manual intervention.

*What this means:* The algorithm is robust to the kind of hardware failures that are inevitable in real disaster deployments.

**4. Improved robustness under multiple simultaneous failures.**
RCTP maintains performance even when multiple drones fail simultaneously — a scenario where baseline algorithms collapse.

*What this means:* The fault tolerance is not just for single failures but for cascading failures, which is what actually happens in harsh disaster environments.

**5. Millisecond-level per-agent inference — real-time feasible.**
Complexity analysis confirms that each UAV can run its decision-making in milliseconds, making real-time deployment on actual hardware computationally feasible.

*What this means:* Unlike many RL papers where the trained model is too slow to run onboard a real drone, RCTP's computational profile is lightweight enough for practical use.

---

## The Contribution

RCTP is the first framework to simultaneously address heterogeneous UAV coordination, rapid adaptation to new scenarios (MAML), fault tolerance under drone failures, intermittent communication, and energy-aware path planning — all in a single end-to-end learning framework for disaster response.

**One-sentence takeaway Ayesha can quote:**
> "RCTP combines meta-learning and multi-agent reinforcement learning to coordinate heterogeneous UAV swarms in disaster scenarios, achieving 30–40% faster mission completion and 10–20% lower energy use than existing methods, while automatically recovering from drone failures and adapting to environments the drones have never seen before."
