# 01 — Full Paper Summary

---

## Paper Identity

**Full Title:** Large-scale UAV swarm path planning based on mean-field reinforcement learning

**Authors:** Yaozhong ZHANG, et al.
**Affiliations:** Northwestern Polytechnical University (Xi'an, China) + Zhejiang Normal University (Jinhua, China)

**Venue:** Chinese Journal of Aeronautics, Volume 38, Issue 9, Article 103484 (2025)
**DOI:** 10.1016/j.cja.2025.103484

**Research Domain:** Multi-Agent Deep Reinforcement Learning (MARL) → UAV Swarm Path Planning → Mean Field Game Theory

---

## The Problem

Imagine trying to coordinate 80 drones simultaneously — each needs to fly from its start position to a designated target, avoid 20 no-fly zones, and not collide with any of the other 79 drones sharing the same airspace. Now imagine you need to do this without any central controller, in real time, with each drone only knowing what it can see within its communication radius.

This is the problem. It is genuinely hard, and it gets harder in two ways as you scale up.

**The first obstacle is computational.** Standard multi-agent reinforcement learning requires each agent to model every other agent. With N agents, the interaction space grows as N², making the problem exponentially harder with each additional drone. At 80 drones, this is unsolvable in reasonable time. At 120 drones, it completely collapses — algorithms like plain DDPG fail to even coordinate basic movement.

**The second obstacle is information.** In a real battlefield, drones cannot know the positions and velocities of every other drone in the swarm — they can only observe neighbors within a communication range. Algorithms that assume global observability (all agents knowing everything about all others) are unrealistic and fragile. When that assumption breaks, performance collapses.

Existing solutions fell into three camps, each failing in a different way:

- **Classic MARL methods** (independent Q-learning, MADDPG) don't scale beyond a dozen agents. The interaction complexity crushes them.
- **Metaheuristic methods** (PSO, GA) treat path planning as a static optimization problem, cannot handle dynamic agent interactions, and produce solutions with frequent inter-drone collisions.
- **Basic mean-field methods** (MFDDPG) average *all* agents equally — a drone 10 meters away and a drone 400 meters away contribute the same to the mean field. This ignores proximity and relevance, leading to poor coordination in cluttered environments.
- **DDPG without mean field** treats each agent independently, ignoring swarm-level interactions entirely — which works at small scale but falls apart at 80+ UAVs.

The field lacked an algorithm that could (1) scale to 80-120 drones, (2) handle partial observability realistically, and (3) give closer, more relevant drones more influence on each agent's decisions than distant ones.

---

## The Proposed Solution

The authors propose **PO-WMFDDPG** — Partially Observable Weighted Mean Field Deep Deterministic Policy Gradient.

The core idea is elegant: instead of tracking every individual drone's interaction with every other drone (computationally impossible at scale), the algorithm replaces all drone-to-drone interactions with a single **mean field** — a weighted average of neighboring drones' actions. Each drone then only needs to respond to this one averaged signal instead of N individual signals. This transforms the N² interaction problem into an N × 1 problem.

Three specific innovations make this work:

**Innovation 1 — Mean Field + DDPG for continuous actions.** Previous mean-field RL work focused on discrete action spaces (simple grid movements). UAVs move in continuous space — continuous speed, continuous heading angle. The authors integrate mean field theory directly into DDPG, which handles continuous control, enabling smooth, realistic flight behavior. This is a non-trivial extension: the mean field update equations had to be reformulated for continuous action distributions.

**Innovation 2 — Partial observability.** Rather than using all N drones globally, each drone only considers neighbors within its communication range R_a. This is both more realistic (drones can't sense infinitely far) and computationally better (the mean field averages over a small local group, not the whole swarm). The algorithm is designed explicitly for a POMDP (Partially Observable Markov Decision Process) framework.

**Innovation 3 — Multi-head attention weighting.** Within a drone's communication range, different neighbors should have different influence levels. A drone 20 meters away matters more than one 200 meters away. The authors add a multi-head attention mechanism that assigns a learned weight to each neighbor's contribution to the mean field. Closer, more relevant neighbors get higher attention weights; distant or less relevant neighbors get lower weights. This is the key difference from basic MFDDPG, which treats all neighbors equally.

---

## The Method (in one paragraph)

Each UAV is trained in a centralized training, distributed execution (CTDE) framework: during training, a shared experience replay buffer and a global critic help all agents learn together; during deployment, each drone runs its own local actor network independently. The state space captures the drone's own position/velocity/heading, its task information (distance and angle to target), and up to 5 detected threats within its sensor range — giving a 16-dimensional state vector. Actions are two continuous values: linear acceleration and angular acceleration. The reward function has two components — a long-term term rewarding goal arrival, boundary compliance, and crash avoidance, plus an instant term rewarding progress toward the target and angle alignment. The mean field is computed as a weighted average of neighbors' actions, with weights determined by a multi-head attention module (4 heads, 32-dimensional keys/queries). The actor network is a 5-layer MLP (16→64→128→32→2) and the critic takes the concatenated state, action, and mean field action (20 inputs) through a 4-layer MLP (20→64→192→64→1). Training runs for 1,000 rounds with batch size 128.

---

## The Key Results

**1. 98% task success rate at 80 UAVs — the primary target scale.**
After 700 training rounds, PO-WMFDDPG achieves approximately 98% task completion rate with 80 drones in a 500×500m environment with 20 no-fly zones. This is the algorithm's peak performance point and the main experimental claim.

*What this means:* Nearly all drones reach their assigned targets without crashing — this is reliable enough to be operationally useful.

**2. Maintains >90% success up to 120 UAVs; competitors collapse.**
When swarm size increases from 80 to 120 drones, PO-WMFDDPG stays above 90% success rate throughout. DDPG (no mean field) begins declining sharply at 100+ drones, eventually failing at high counts. MFDDPG (global mean field, no attention weighting) begins declining at 110+ drones.

*What this means:* The combination of local partial observability + attention weighting gives PO-WMFDDPG significantly better scalability than both baselines. It's not just better at 80 drones — it remains better as the problem gets harder.

**3. NFZ robustness: stable up to 20 no-fly zones, declining gradually after 36.**
As the number of no-fly zones increases from 10 to 36, PO-WMFDDPG maintains approximately 98% success. Performance only begins declining after 36 NFZs. DDPG collapses after 26 NFZs; MFDDPG falls between the two. PO-WMFDDPG at 36 NFZs still outperforms DDPG at 20 NFZs.

*What this means:* The algorithm handles moderate threat density very robustly. Real battlefield environments rarely have 36 simultaneous no-fly zones, making this more than sufficient for practical deployment.

**4. Moving no-fly zone test: 75 out of 80 UAVs succeed.**
When the no-fly zones are made dynamic (moving at random velocities), 75 of 80 drones still reach their targets. The 5 failures occur because the drones cannot evade the moving NFZs in time — a genuine limitation. However, a 93.75% success rate with moving threats is still strong performance.

*What this means:* The algorithm can handle some degree of dynamic obstacles, though not perfectly. The partial observability and attention mechanism give drones enough situational awareness to evade most moving threats.

**5. Convergence in ~700 training rounds (out of 1,000).**
The algorithm converges to near-peak performance by round 700. PO-WMFDDPG converges faster and to a higher final reward than both DDPG and MFDDPG baselines, whose reward curves plateau at lower values and show more instability.

*What this means:* The design choices — mean field approximation, attention weighting, partial observability — don't just improve final performance; they also make training more stable and efficient.

---

## The Contribution

This paper's contribution is proving that mean field theory, partial observability constraints, and attention-based weighting can be combined into a single MARL algorithm that remains reliable and scalable where all simpler approaches collapse — enabling practical autonomous coordination of 80-120 drone swarms in obstacle-rich environments.

**One-sentence takeaway Ayesha can quote:**
> "PO-WMFDDPG solves large-scale UAV swarm coordination by treating nearby drone interactions as a weighted mean field rather than N individual interactions, achieving 98% mission success with 80 drones and maintaining above 90% even at 120 — where all competing methods fail."
