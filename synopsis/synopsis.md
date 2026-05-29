# Synopsis
## MS Research — Computer Science
**Student:** Ayesha Khalil
**Registration No:** SP25-RCS-009

---

## Title

**When Assigning Targets and Avoiding Collisions Conflict: A Multi-Agent Reinforcement Learning Framework for 3D UAV Swarm Navigation**

---

## 1. Introduction

Coordinating a group of UAVs to simultaneously reach different targets without colliding is one of the central unsolved challenges in autonomous systems. The difficulty is not in teaching a single UAV to fly — that problem is largely solved. The difficulty is that in a group of five or more drones, two objectives are always competing: each drone is told to go somewhere (target assignment), and each drone is told to stay away from others (collision avoidance). When these two objectives are handled separately — first assign, then avoid — the system breaks down under dynamic conditions, because a new assignment may send a drone directly into a collision course that the avoidance module was not expecting.

I reviewed ten recent papers on this topic and found that the most advanced work on these two problems comes from two separate papers published in 2026. DA-MAPPO (Sheng et al., 2026) solved the assignment problem but tested only three drones and used a simple penalty for collisions. IGAT-MARL (Rezaee et al., 2026) solved the collision problem using a sparse conflict graph but had no assignment component. Both papers explicitly state that what the other paper does is their next step. Neither paper has taken that step. This research proposes to take it — specifically in a 3D environment, where the interaction between these two mechanisms has not been studied.

---

## 2. Problem Statement

DA-MAPPO showed that embedding a real-time target assignment directly into each drone's observation — updated at every step using the Hungarian algorithm — is the single mechanism responsible for its performance. Its own ablation study confirmed this: removing the assignment-augmented state caused mission success to drop from over 90% to exactly 0%. This means the assignment information is not a nice addition; it is the entire basis of the policy.

IGAT-MARL showed that the correct way to handle collision avoidance in a multi-drone environment is not to have every drone monitor every other drone, but to build a sparse graph that only connects drone pairs currently on a predicted collision course. This reduced unnecessary communication by 44% while improving avoidance performance.

The problem I am proposing to study is this: **these two mechanisms have never been placed inside the same policy, and in a 3D environment, they directly compete.**

When the Hungarian assignment sends a drone toward its target, it does so without knowing which other drones are currently in a conflict state. When the conflict graph identifies a dangerous pair and tries to make them deviate, it does not know whether that deviation moves one drone away from its assigned target. In 2D, this tension is manageable because drones only move laterally. In 3D, a drone assigned to a target that is above and to the right must also manage altitude — and a conflict drone may be directly above it on the same vertical path.

No paper has tested whether the assignment-augmented observation that makes DA-MAPPO work in 2D remains informative when drones must also reason about altitude, or whether the conflict-aware graph that reduces communication overhead in IGAT-MARL remains effective when target assignments are changing at every step.

**The concrete research problem is:** Can a single MAPPO policy, trained with both assignment-augmented observations and a conflict-aware interaction graph, achieve above 85% mission success for a swarm of five to eight UAVs navigating to dynamically assigned targets in a 3D environment with obstacles — and does each mechanism contribute independently, or do they interfere with each other?

---

## 3. Research Objectives

1. Design a unified observation representation that combines DA-MAPPO's assignment augmentation and IGAT-MARL's conflict-aware neighborhood into a single input vector for a MAPPO policy operating in 3D space.

2. Train and evaluate the proposed framework across swarm sizes of 3, 5, and 8 drones to determine whether performance degrades as the number of simultaneous assignment-conflict interactions increases.

3. Run controlled ablation experiments to isolate the individual contribution of the assignment mechanism, the conflict graph, and the 3D extension — specifically to answer whether each component helps, and whether they help more together than separately.

4. Identify the failure modes: under what conditions (swarm size, obstacle density, target movement speed) does the combined policy fail, and why.

---

## 4. Research Questions

1. When target assignment and collision avoidance are handled by the same policy in a 3D environment, does the assignment-augmented state remain the critical mechanism that DA-MAPPO's ablation identified — or does the addition of 3D collision constraints reduce its importance?

2. At what swarm size does the interaction between real-time reassignment and conflict graph updates become a bottleneck — is there a point where reassigning targets too frequently creates instability in the conflict graph, or does the sparse graph naturally absorb this?

3. Is a 3D extension of DA-MAPPO + IGAT-MARL sufficient for a Masters-level contribution, or do the results reveal a further open problem that points toward a clearer future direction?

---

## 5. Proposed Methodology

### 5.1 Framework Design

The core algorithm is MAPPO (Multi-Agent Proximal Policy Optimization), selected because DA-MAPPO already validated it for the assignment setting and it is known to be stable under partial observability.

Each drone's observation vector contains:
- Its own 3D position and velocity
- The 3D relative position of its currently assigned target (from Hungarian assignment)
- The positions and velocities of conflict neighbors only (from the dynamic conflict graph, not all drones)
- Obstacle proximity readings in six directions (up, down, north, south, east, west)

At every decision step:
1. The Hungarian algorithm computes the minimum-cost assignment from current 3D positions to targets
2. The conflict graph updates — only drone pairs predicted to be within a collision threshold in the next T steps are connected
3. Each drone runs its MAPPO policy using the combined observation
4. Continuous 3D velocity commands are output

### 5.2 Training Strategy

Curriculum training in four stages:
- Stage 1: 3 drones, static targets, few obstacles (replicate DA-MAPPO as sanity check)
- Stage 2: 5 drones, moving targets, moderate obstacles
- Stage 3: 8 drones, moving targets, high obstacle density
- Stage 4: Varied swarm sizes to test generalization

### 5.3 Evaluation

**Primary metric:** Mission success rate (all drones reach targets without collision, within time limit)

**Secondary metrics:** Inter-drone collision count, obstacle collision count, number of target reassignments per episode, average trajectory length

**Baselines:**
- Standard MAPPO (no assignment, no conflict graph) — to measure the combined contribution
- DA-MAPPO in 3D (assignment only, no conflict graph) — to isolate the collision component
- IGAT-MARL with fixed assignment (conflict graph only, no dynamic assignment) — to isolate the assignment component
- DA-MAPPO original (2D, 3 drones) — to verify replication

**Simulation environment:** PyBullet or custom OpenAI Gym environment. All tools free and open source.

---

## 6. Why This Is Not Already Done

The gap between Papers 9 and 91 is documented by both papers themselves.

DA-MAPPO (Paper 91) states in its limitations: *"The current framework only tested three agents... future work should extend to larger swarms and 3D environments."*

IGAT-MARL (Paper 9) states: *"The absence of a target assignment component means agents have no goal structure... incorporating task allocation is a clear next step."*

Paper 3 (3D path planning) works with a single drone and explicitly calls for multi-agent extension.

The reason none of them filled this gap is that combining the assignment mechanism with the collision mechanism in 3D requires resolving the interference described in Section 2 above — which is a non-trivial design problem, not just a straightforward implementation task. That interference is the concrete technical contribution of this research.

---

## 7. Expected Contributions

1. A working, reproducible 3D multi-UAV simulation framework combining dynamic target assignment and conflict-aware collision avoidance — which does not currently exist in the literature.

2. An empirical answer to whether DA-MAPPO's core mechanism (assignment-augmented state) scales to 3D and to swarm sizes beyond three — a question the original paper explicitly left open.

3. A systematic ablation across three swarm sizes and three obstacle densities, providing more comprehensive evidence than the existing papers which each test only one or two configurations.

4. Identification of the failure boundary: the specific conditions under which the assignment-collision interference becomes the dominant problem, which directly points toward the next research step.

---

## 8. Timeline

| Period | Activity |
|--------|----------|
| Months 1–3 | 3D simulation environment setup in PyBullet; replicate DA-MAPPO (3 drones, 2D) as baseline validation |
| Months 4–6 | Implement assignment-augmented observations in 3D; implement conflict graph; integrate into MAPPO |
| Months 7–10 | Full curriculum training (3 → 5 → 8 drones); systematic evaluation against all four baselines |
| Months 11–13 | Ablation experiments; failure case analysis; sensitivity to obstacle density and target speed |
| Months 14–18 | Writing, revision, submission |

---

## 9. Key References

1. Sheng, Z. et al. (2026). Dynamic Target Assignment and Cooperative Decision-Making for UAV Swarms Based on Multi-Agent Reinforcement Learning. *IEEE Internet of Things Journal.*

2. Rezaee, H. et al. (2026). Efficient Multi-Agent Deep Reinforcement Learning Algorithm for Multi UAV Collision Avoidance. *Applied Soft Computing, Vol. 197.*

3. Fan, X. et al. (2025). Dynamic Reward-Based Deep Reinforcement Learning Algorithm for UAV Path Planning in Large-Scale Environments. *Procedia Computer Science (KES 2025).*

4. Poudel, S. & Moh, M. (2026). MAML-Integrated Multi-Agent Reinforcement Learning for Adaptive Coalition-Based UAV Coordination in Disaster Scenarios. *Internet of Things, Elsevier.*

5. Wang, Y. et al. (2025). RALLY: Role-Adaptive LLM-Driven Yoked Navigation for Agentic UAV Swarms. *IEEE Open Journal of Vehicular Technology, Vol. 6.*

---

*Ayesha Khalil | SP25-RCS-009*
