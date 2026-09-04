# 06 — Presentation Guide: Script + Q&A

---

## Suggested Opening (word for word)

> "Good morning/afternoon, sir. Today I'd like to present a paper titled 'Large-scale UAV Swarm Path Planning Based on Mean-Field Reinforcement Learning' by Yaozhong Zhang and colleagues from Northwestern Polytechnical University and Zhejiang Normal University, published in the Chinese Journal of Aeronautics in 2025.
>
> This paper addresses the problem of coordinating a swarm of 80 drones to simultaneously navigate a battlefield — avoiding no-fly zones and not colliding with each other — at a scale where standard multi-agent reinforcement learning completely breaks down. The authors propose PO-WMFDDPG, an algorithm that uses mean-field theory with attention-based neighbor weighting to make large-scale swarm coordination computationally tractable. Their experiments show the algorithm achieves approximately 98% task success rate with 80 drones and maintains above 90% success even with 120 drones, where both comparison algorithms fail significantly."

---

## Main Points to Cover (in order)

```
1. THE PROBLEM
   Say: "The fundamental challenge is scale. Multi-agent reinforcement learning requires
   each agent to model every other agent's behavior. With N agents, the number of
   interactions grows as N-squared — with 80 drones, that's over 6,000 pairwise
   interactions to track simultaneously, which is computationally infeasible. And the
   problem is compounded by observability: in a real battlefield, drones can only
   communicate with nearby neighbors within their radio range — they can't know what all
   79 other drones are doing at every moment. Algorithms designed for small groups of
   agents — 5 or 10 drones — completely collapse when you try to scale them to 80."

2. WHY EXISTING SOLUTIONS WEREN'T ENOUGH
   Say: "Standard DDPG applied to multi-agent settings simply treats each drone
   independently — it ignores the interactions between agents entirely. This works at
   small scales but falls apart as drone density increases, because collisions and
   coordination failures multiply. The other approach — MFDDPG, which uses mean-field
   theory — improves on this by averaging all agents' behaviors into a single signal.
   But it averages them equally: a drone 500 meters away contributes as much to the
   average as one 5 meters away. This is clearly wrong. Distant drones are irrelevant to
   your immediate decision; only nearby drones matter. That equal-weighting error is what
   this paper fixes."

3. THE PROPOSED APPROACH
   Say: "The authors propose PO-WMFDDPG — Partially Observable Weighted Mean Field DDPG.
   The key idea is this: instead of modeling 79 individual drones, each drone computes a
   single weighted average of its nearby neighbors' actions — the mean field. Closer,
   more relevant neighbors get higher weights determined by a multi-head attention
   mechanism. And crucially, 'nearby' is defined by the drone's actual communication
   range — not the entire swarm. So instead of N-squared interactions, each drone only
   responds to one weighted average from its local neighborhood. This transforms the
   problem from exponentially hard to linear in N."

4. KEY METHODOLOGY
   Say: "Each UAV observes a 16-dimensional state: its own position, speed, and heading;
   its distance and angle to its target; and up to 5 detected no-fly zones within sensor
   range. From this, it selects two continuous actions: linear acceleration and angular
   acceleration — smooth, realistic flight control. The mean field is computed by a
   multi-head attention module with 4 heads, which learns which neighbors are most
   relevant and assigns them higher weights. The actor network outputs the action from a
   5-layer MLP, and the critic evaluates state-action pairs incorporating the mean field.
   Training uses the CTDE framework — centralized training with shared experience, but
   each drone executes its own policy independently in deployment."

5. THE RESULTS
   Say: "In the primary experiment with 80 drones and 20 no-fly zones, PO-WMFDDPG
   converges to approximately 98% task success rate by round 700 of training. In the
   scalability test, this performance holds as drone count increases: at 100 drones, it's
   still around 95%; at 120 drones, it's still above 90%. In comparison, DDPG without
   mean field drops sharply beyond 100 drones, and even MFDDPG — the equal-weight mean
   field — begins collapsing around 110 drones. For no-fly zone density, PO-WMFDDPG
   remains near 98% with up to 36 NFZs, while DDPG collapses after just 26 NFZs.
   A bonus result: even when NFZs were made dynamic — moving randomly during the
   mission — 75 out of 80 drones still succeeded, despite the algorithm being trained
   only with static NFZs."

6. SIGNIFICANCE AND CONTRIBUTION
   Say: "The paper's contribution is demonstrating that mean-field theory, partial
   observability, and learned attention weighting can be combined to make large-scale
   swarm coordination tractable in deep RL. The three innovations work together: partial
   observability makes the algorithm realistic, mean-field approximation makes it
   scalable, and attention weighting makes it accurate. The result is an algorithm that
   maintains over 90% success at 120 drones — a scale where all simpler alternatives
   fail — while remaining deployable on real hardware in principle, since each drone only
   needs local observations to execute its policy."
```

---

## Anticipated Questions & Model Answers

| Question Sir Might Ask | What Ayesha Should Say |
|---|---|
| **What is the main contribution of this paper?** | "The main contribution is PO-WMFDDPG — an algorithm that combines three innovations to make large-scale UAV swarm coordination tractable. First, it uses mean-field theory to approximate 80 drone interactions as a single averaged signal, replacing N-squared complexity with N times one. Second, it restricts this mean field to locally observable neighbors within communication range, making it both realistic and computationally efficient. Third, it uses a multi-head attention mechanism to weight nearby, more relevant drones higher in the mean field — fixing the key flaw of previous equal-weight mean-field methods. The result is 98% task success with 80 drones and above 90% with 120, where both baseline algorithms fail significantly earlier." |
| **What is mean field theory and why is it used here?** | "Mean field theory is a mathematical framework from physics where instead of tracking every individual particle's interaction with every other particle — which scales as N-squared — you approximate all those interactions as a single 'mean field': one averaged representative behavior. In this paper, each drone doesn't track 79 others individually. It computes a weighted average of its visible neighbors' actions and responds to that single averaged signal. This reduces the interaction modeling from 80×79 pairs down to 80 times one — the same work regardless of how many drones there are. That's what makes scaling to 120 drones computationally feasible." |
| **How does the attention mechanism work?** | "The multi-head attention module takes the current drone's state as a query and each neighbor's state features as keys. For each neighbor, it computes a dot-product similarity between the query and key, then applies softmax to get attention weights that sum to 1 across all neighbors. A neighbor whose state features are more similar to what the current drone is attending to — typically one that's nearby and on a collision-risk trajectory — gets a higher weight. The 'multi-head' part means this attention is computed 4 times in parallel with different learned transformations, capturing different notions of relevance simultaneously. The result is a weighted mean field where the closest, most dangerous neighbors have the most influence." |
| **What is CTDE and why is it appropriate here?** | "CTDE stands for Centralized Training, Distributed Execution. During training, all 80 drones share a common experience replay buffer and a global critic that can see everything — this helps each drone learn better policies because it has access to information from all its teammates' experiences. But during deployment, each drone runs only its own local actor network using only what it can personally observe. This is the right design because real swarms can't have a central controller in the field — each drone must act independently. CTDE gives you the learning benefits of centralization without the deployment limitations." |
| **What are the limitations of this work?** | "The main limitations I see are: first, everything is in 2D simulation — real UAVs fly in 3D, and have sensor noise, GPS errors, and wind disturbance that aren't modeled. Second, all obstacles are circular and either static or randomly moving — real no-fly zones have irregular shapes and strategic movement. Third, all 80 drones are identical — real swarms mix different drone types with different capabilities. Fourth, targets are fixed in advance — there's no replanning if a target moves or is reassigned mid-mission. Fifth, the mean-field communication assumes perfect, instant message passing — real radio communication has latency and packet loss. The authors do acknowledge the 2D limitation and the static target problem as future work directions." |
| **How does this compare to DDPG and MFDDPG?** | "DDPG with no mean field treats each drone independently — it ignores drone-to-drone interactions. This works at small scales but collapses at 100+ drones because the collisions and coordination failures the algorithm can't anticipate pile up. MFDDPG fixes this by adding mean-field averaging, but uses all agents globally with equal weights — including drones 400 meters away that have no relevance to your current decision. PO-WMFDDPG addresses both problems: the partial observability constraint filters to only relevant nearby neighbors, and the attention mechanism correctly weights closer, more dangerous neighbors higher. The experimental gap confirms this: at 120 drones, PO-WMFDDPG outperforms DDPG by roughly 25 percentage points in success rate." |
| **What evaluation metrics were used?** | "The primary metric is task success rate — the percentage of UAVs that reach their assigned target without entering a no-fly zone or colliding with another drone. This is the appropriate metric for this problem because the mission is binary for each drone: you either complete it or you don't. The experiments vary drone count and NFZ count to test scalability, and there's a separate moving-NFZ test for robustness. I would add that the paper could have benefited from also reporting path length, inter-drone minimum distance, and a breakdown of failure causes — whether failures came from NFZ entry or inter-drone collisions — to give a more complete picture." |
| **What is the state space? Can you explain the 16 dimensions?** | "The 16-dimensional state has three components. The first 4 dimensions are the drone's own state: x-coordinate, y-coordinate, current speed, and current heading angle. The next 2 dimensions are task information: the drone's distance to its target and the angle between its heading and the direction to the target. The remaining 10 dimensions cover up to 5 detected no-fly zones within sensor range — for each NFZ, the drone records the distance to it and the angle toward it. If fewer than 5 NFZs are detectable, the remaining entries are zero-padded. This design lets the drone know where it is, where it's going, and what threats are nearby — everything needed for safe navigation." |
| **What future work do the authors suggest?** | "The authors suggest three directions: first, extending to 3D environments to capture realistic altitude dynamics; second, handling heterogeneous swarms where different drones have different speeds and capabilities; and third, testing with constrained communication — lower bandwidth, higher latency, packet loss — to validate the algorithm's robustness in realistic radio conditions. I would add that hardware validation on even a small physical drone platform, and testing with dynamic target reassignment, would be important next steps to bridge the simulation-to-reality gap." |
| **Why is partial observability an improvement over global mean field?** | "Global mean field — like in the MFDDPG baseline — averages the actions of all N agents, including ones far away that have no bearing on your immediate decisions. At 80 drones spread across a 500×500m space, most drones are irrelevant to any given drone's next action. Including them pollutes the mean field with noise. Partial observability fixes this by computing the mean field only from neighbors within communication range R_a. You get a local, relevant signal rather than a diluted global average. This is both more computationally efficient (fewer neighbors to aggregate) and more accurate (the signal is more informative). The experimental results confirm it: PO-WMFDDPG consistently outperforms MFDDPG, which outperforms DDPG." |
| **Do you find the results convincing? Why or why not?** | "I find the relative results convincing — PO-WMFDDPG outperforms both baselines consistently across all test conditions, and the performance gap is large enough to be meaningful, not marginal. The graduated scalability experiments showing where each algorithm starts to fail are honest and informative. However, I'd want to see two things before calling it fully convincing: first, a comparison against more competitive modern baselines like MAPPO or MADDPG rather than just DDPG and MFDDPG; and second, some form of hardware validation or at minimum a realistic physical simulation with flight dynamics, sensor noise, and communication latency. The 2D point-mass simulation without any of these real-world complications makes the results somewhat optimistic." |

---

## What NOT to Say

1. **Don't say** "each drone tracks all other drones." The entire point of the paper is that this is computationally impossible at scale — the mean field replaces individual tracking with a weighted average. Saying drones track each other would contradict the paper's core motivation.

2. **Don't say** "the algorithm achieves 100% success rate." The primary result is approximately 98% with 80 drones — about 2 drones out of 80 still fail. In the 120-drone case it's above 90%. The algorithm is not perfect.

3. **Don't say** "the drones can avoid any obstacle." The moving-NFZ test shows 5 out of 80 drones fail when obstacles are dynamic. The algorithm handles static NFZs robustly but has partial limitations with moving ones.

4. **Don't say** "this works in 3D." The entire environment is 2D — a horizontal flight plane. The state space has no altitude component. The 3D extension is explicitly listed as future work.

5. **Don't say** "the drones communicate directly with each other." In the paper's model, drones share action information for mean-field computation within communication range, but this is a simplified communication model — there's no actual wireless protocol, no message passing protocol, no latency modeling.

---

## Closing Statement

> "In summary, this paper presents PO-WMFDDPG — a multi-agent reinforcement learning algorithm that makes large-scale UAV swarm coordination tractable by combining mean-field approximation, partial observability, and attention-based neighbor weighting. The results demonstrate clear advantages over both a no-mean-field baseline and a uniform-mean-field baseline, maintaining 98% success with 80 drones and above 90% with 120, a scale where all simpler approaches fail. While the evaluation is simulation-only and restricted to 2D, the algorithmic contribution is principled and the scalability results are compelling. Thank you, sir."

---

## If You Forget Something

> "If you blank on a specific number, say: 'The paper demonstrates that PO-WMFDDPG maintains high task success rate at scales where both comparison algorithms — DDPG and MFDDPG — show significant performance degradation. The key innovation is the attention-weighted mean field, which allows each drone to focus on its most relevant nearby neighbors rather than averaging over the entire swarm or ignoring inter-drone interactions entirely.'"
