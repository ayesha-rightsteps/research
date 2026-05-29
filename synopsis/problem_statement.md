# Research Problem Statement
**Ayesha Khalil | SP25-RCS-009**

---

## Title
**When Assigning Targets and Avoiding Collisions Conflict: Integrating Dynamic Target Assignment and Collision Avoidance for Multi-UAV Navigation in 3D Environments**

---

## Problem Statement

While reviewing recent work on multi-UAV coordination, I found that the two most advanced solutions to this problem — DA-MAPPO (Sheng et al., 2026) and IGAT-MARL (Rezaee et al., 2026) — each solve exactly half of the problem and neither addresses the other half.

DA-MAPPO solved dynamic target assignment for UAV swarms. Its ablation study showed that embedding the current target assignment directly into each drone's observation is the single mechanism responsible for all performance: removing it caused mission success to drop from over 90% to exactly 0%. However, DA-MAPPO was only tested with three drones in a 2D environment and used only a simple penalty term for collision avoidance.

IGAT-MARL solved collision avoidance by building a sparse conflict graph — connecting only drone pairs that are actually on a predicted collision course rather than having every drone monitor every other drone. This reduced interaction overhead by 44% while improving avoidance performance. However, IGAT-MARL has no target assignment component: drones have no goal structure and simply avoid each other.

Both papers explicitly list what the other paper does as their own future work. Neither has taken that step.

**The specific problem I want to study is the interference between these two mechanisms in 3D space.**

When the Hungarian assignment (from DA-MAPPO) sends a drone toward its target, it does so without knowing which drone pairs are currently in a conflict state. When the conflict graph (from IGAT-MARL) identifies a dangerous pair and forces a deviation, it does not know whether that deviation moves one drone away from its assigned target. In 2D this tension is manageable. In 3D it becomes critical — a drone assigned to a target above it may be on a direct collision course with another drone on the same vertical path, and the two mechanisms give it contradictory instructions.

No existing work has placed these two mechanisms in the same policy. No existing work tests whether DA-MAPPO's core mechanism — the assignment-augmented observation — remains effective when drones must also reason about altitude and 3D collision avoidance simultaneously.

**The research question is:** Can a single MAPPO policy trained with both assignment-augmented observations and a conflict-aware interaction graph achieve above 85% mission success for 5–8 UAVs navigating to dynamically assigned targets in a 3D environment — and do the two mechanisms work together, or do they interfere with each other?

This is testable, the gap is documented by both source papers themselves, and the answer is not known.

---

**Key References:**
- Sheng et al. (2026). Dynamic Target Assignment and Cooperative Decision-Making for UAV Swarms. *IEEE Internet of Things Journal.*
- Rezaee et al. (2026). Efficient Multi-Agent DRL for Multi UAV Collision Avoidance. *Applied Soft Computing, Vol. 197.*
