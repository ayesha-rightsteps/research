# 06 — Presentation Guide: Your Complete Script

This is the most important file. Read it aloud before your presentation. Every word here is chosen to sound natural when spoken.

---

## Suggested Opening (Word for Word)

> "Good morning, sir. Today I would like to present a paper titled 'Dynamic Target Assignment and Cooperative Decision-Making for UAV Swarms Based on Multi-Agent Reinforcement Learning' by Yuanyuan Sheng, Xianan Xie, Huanyu Liu, and Junbao Li from Harbin Institute of Technology, published in IEEE Internet of Things Journal in 2026.
>
> This paper addresses the problem of coordinating a swarm of drones to reach multiple moving targets in cluttered environments — without any central controller and without perfect information. The authors propose DA-MAPPO, a framework that continuously updates which drone should chase which target at every decision step, and embeds that assignment directly into each drone's observations. In their experiments, DA-MAPPO achieves 90 to 99 percent mission success in dynamic environments and outperforms the best competing methods by up to 25 percentage points."

---

## Main Points to Cover (In Order)

---

### 1. THE PROBLEM

**Say:**
> "Imagine you have a team of three drones that need to fly through a room full of obstacles and each reach a different target. Now imagine those targets start moving. The classic approach — decide who goes where at the start, then each drone flies its pre-planned path — completely breaks down because the drone might be flying toward where the target used to be, not where it is now. On top of this, each drone can only sense a limited area with its LiDAR sensor and can only communicate with nearby drones — it never sees the full picture. This combination of dynamic targets, partial information, and tight safety requirements in multi-drone systems is the core challenge this paper addresses."

---

### 2. WHY EXISTING SOLUTIONS WERE NOT ENOUGH

**Say:**
> "Traditional optimization-based approaches, like EGO-Planner, can compute beautiful, smooth trajectories — but they need global information and a centralized controller, and they struggle to replan fast enough when targets keep changing. Existing reinforcement learning approaches improved adaptability, but almost all of them either assumed targets don't move, or treated target assignment as a separate pre-processing step disconnected from the navigation policy. So when targets changed, the drones kept flying toward outdated goals."

---

### 3. THE PROPOSED APPROACH

**Say:**
> "The key insight of DA-MAPPO — and what makes it different from everything before it — is that it solves the target assignment problem at every single decision step and immediately feeds the result into each drone's observation. So at every moment, each drone knows its currently assigned target — not from a fixed assignment made at the beginning, but from a continuously updated one. If a target moves, the next step's observation reflects the new assignment. The drones do not need to be told that things have changed — they simply get updated information and their learned policy handles it naturally."

---

### 4. KEY METHODOLOGY

**Say:**
> "The system runs three stages at each step. First, environmental perception — each drone uses its 35-beam LiDAR to sense nearby obstacles, records its own velocity and heading, and picks up relative positions of nearby teammates. Second, target allocation — the system builds a cost matrix of squared distances between every drone and every target, then solves a Hungarian assignment problem to find the pairing that minimizes total travel cost. The result — distance and direction to assigned target — is added to each drone's observation vector, making what the paper calls an assignment-augmented state. Third, cooperative decision-making — the augmented observation goes into a shared neural network that outputs continuous velocity commands for all three drones. The entire system is trained using MAPPO with a centralized critic and a hierarchical reward that balances collision avoidance, individual progress, and team-level coordination."

---

### 5. THE RESULTS

**Say:**
> "In high-fidelity Gazebo simulation with three drones and three moving targets, DA-MAPPO achieved 99%, 95%, and 90% success in environments with 30, 40, and 50 obstacles respectively — always under dynamic target conditions. The next best method, RMAPPO, achieved only 85%, 69%, and 67% — so the gap is 14 to 23 percentage points. What is particularly striking is that when the researchers switched targets from static to dynamic, DA-MAPPO's performance barely changed — only a 2% drop in the hardest environment. All other methods degraded by 20 to 34 percentage points under the same switch. The system also proved robust: even with 50% communication packet loss and heavy sensor noise, performance was almost unchanged."

---

### 6. SIGNIFICANCE AND CONTRIBUTION

**Say:**
> "This paper demonstrates for the first time that tightly coupling real-time target assignment with multi-agent policy learning — rather than treating them as separate modules — is the key to handling dynamic, cluttered, multi-drone scenarios. The ablation study makes this especially clear: removing the assignment-augmented observation caused a 100% failure rate, proving the policy fundamentally depends on this connection. For IoT-edge applications like disaster response or environmental monitoring, this matters because it shows we can build drone swarms that adapt to changing conditions in real time, on resource-constrained edge hardware, without any central controller."

---

## Anticipated Questions and Model Answers

*(Every answer is specific to this paper — read each one aloud before your presentation)*

---

| Question Sir Might Ask | What Ayesha Should Say |
|---|---|
| **What is the main contribution of this paper?** | "The main contribution is a unified framework called DA-MAPPO that integrates an online minimum-cost target allocator with multi-agent PPO. At every decision step, the system solves a Hungarian assignment problem and embeds the result — distance and bearing to the assigned target — directly into each drone's observation. This makes the navigation policy explicitly aware of the current assignment, enabling it to instantly adapt when targets move. The ablation study shows this is not just a nice-to-have — without it, the system achieves zero percent success." |
| **What makes this approach different from previous work?** | "Most previous approaches either assumed targets do not move, or treated target allocation as a separate offline step performed before flight begins. DA-MAPPO updates the assignment at every single decision step — not once, not every 50 steps, but every step — and directly feeds that assignment into what each drone observes. The result is a policy that is always conditioned on its current target, so it cannot get stuck chasing an outdated one. No previous MARL paper for UAV swarms had done this in a fully integrated, end-to-end trainable way." |
| **What are the limitations of this work?** | "The paper has a few honest limitations. First, all experiments use exactly 3 drones — performance at larger scales is not tested, even though the authors do analyze computational complexity and show it scales as O of N-cubed due to the Hungarian algorithm. Second, the simulation assumes no wind or aerodynamics, so there is a sim-to-real gap that the authors acknowledge and list as future work. Third, obstacles are all static — the system handles moving targets but not moving obstacles, which would be important in real-world scenarios like urban environments." |
| **What evaluation metric did they use? Is it appropriate?** | "The primary metric is mission success rate — the percentage of episodes where all three drones successfully reach their targets without any collision or timeout. It is a strict all-or-nothing metric: even one collision fails the entire episode. This is conservative and arguably demanding, because in practice completing two of three missions might still be acceptable. But for this paper's purpose of demonstrating cooperative coordination — where the whole team must work together — it is the right metric. They also report collision rate, timeout rate, average trajectory length, and average time steps for a complete picture." |
| **What dataset was used and why?** | "This paper does not use a dataset — it uses a simulation environment built in Gazebo, which is a high-fidelity robotics simulator with rigid-body physics and ray-cast LiDAR. The environments are procedurally generated with 30, 40, or 50 randomly placed static obstacles and 3 randomly positioned targets. They ran 100 independent test episodes per environment to get statistically meaningful results. Gazebo was chosen because it handles actual collision geometry and physics, making it more realistic than purely abstract simulations." |
| **Could this approach be applied to other problems?** | "Yes, I think so. Any problem where you have multiple agents that need to reach multiple goals that can change over time — and where agents have limited sensing and communication — could benefit from this framework. For example, multi-robot warehouse sorting, drone delivery coordination, or even multiplayer game AI where agents need to switch targets dynamically. The key requirement is that the assignment can be formulated as a minimum-cost matching problem, which covers a broad range of scenarios." |
| **What would you change if you were the author?** | "I would test with larger swarm sizes — the paper only evaluates 3 drones, but the framework should theoretically scale. I would also compare against other methods that do handle dynamic assignment in MARL, such as attention-based or graph neural network methods, which the related work mentions but does not directly compare against. And I would add a real physical flight experiment, even a simple one, to show that the sim-to-real gap is manageable." |
| **What future work do the authors suggest?** | "The authors specifically mention two directions: first, real-world UAV deployment for sim-to-real validation — actually flying physical drones to confirm the policy transfers from Gazebo to reality. Second, communication-efficient coordination under stricter bandwidth and latency constraints — the current setup assumes drones can exchange position data, but future work would explore what happens when bandwidth is severely limited or when only a fraction of neighbors can be reached." |
| **Do you find the results convincing? Why?** | "Yes, I find them convincing for several reasons. The comparison set is diverse — it includes not just MARL variants but also a specialized safe RL method and a state-of-the-art optimization planner. The ablation study provides strong mechanistic evidence — the zero-percent failure without the augmented state removes any doubt about whether the mechanism matters. And the robustness experiments show graceful degradation under realistic imperfections rather than a sudden cliff. The main caveat is that it is only tested with 3 drones, so I would want to see larger-scale experiments before feeling fully confident." |
| **How does this compare to MAPPO?** | "MAPPO is one of the baselines in this paper, and DA-MAPPO is built on top of MAPPO. Standard MAPPO uses a centralized critic and decentralized actors, which is already a strong baseline. But in the dynamic multi-target scenario, MAPPO drops to 64% success in the hardest environment because it has no mechanism to update which target each drone is pursuing — it works with whatever assignment it had at the start of the episode. DA-MAPPO adds the per-step allocation and augmented observation on top of MAPPO's architecture, and that addition alone accounts for the 26-percentage-point improvement." |

---

## What NOT to Say

1. **Do not say "the paper proves that UAVs are better than humans."** The paper is a simulation study about a specific algorithmic framework — no such comparison is made.

2. **Do not say "this is the first ever multi-agent reinforcement learning paper."** MARL is a well-established field. This paper's novelty is specifically about real-time assignment integration into the observation, not MARL itself.

3. **Do not overstate the sim-to-real applicability.** The paper itself acknowledges it runs under "ideal windless assumption" with no aerodynamics. Say the results are from simulation and real-world validation is future work.

4. **Do not say the Hungarian algorithm is a neural network or learning method.** It is a classical combinatorial optimization algorithm that runs at each step. The learning only happens in the policy network.

5. **Do not confuse collision rate with collision avoidance.** A 1% collision rate means 1 in 100 episodes ended in a collision — it does not mean the drone avoided 99% of individual obstacles. These are different numbers.

---

## Closing Statement

> "In summary, DA-MAPPO demonstrates that continuously embedding real-time target assignment into each agent's observation is a simple but powerful change that fundamentally improves multi-drone coordination in dynamic environments. The 90 to 99 percent success rates and near-zero degradation from static to dynamic targets, combined with strong robustness properties, suggest this framework is a meaningful step toward practically deployable UAV swarm intelligence for IoT-edge applications. Thank you, sir."

---

## If You Forget Something

> "If you blank on a detail mid-presentation, you can always say: 'The paper specifies the exact number — but the key point is that DA-MAPPO substantially outperforms all baselines here, and I can walk through the specific figures if you would like.' This keeps the presentation moving while giving you a moment to collect your thoughts."
