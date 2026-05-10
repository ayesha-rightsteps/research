# 06 — Presentation Guide: Script + Q&A

---

## Suggested Opening (word for word)

> "Good morning/afternoon, sir. Today I'd like to present a paper titled 'Dynamic Reward-Based Deep Reinforcement Learning Algorithm for UAV Path Planning in Large-Scale Environments' by Raja Jarray, Imen Zaghbani, and Soufiene Bouallègue, published in Procedia Computer Science in 2025 at the KES International Conference.
>
> This paper addresses the problem of navigating a single drone from a start to a destination in a large, obstacle-filled 3D environment — without crashing. The authors propose a Deep Q-Network with a novel dynamic reward function that continuously guides the drone based on its real-time distance to the target. Simulation results show that the proposed DQN outperforms four competing algorithms — including Q-learning and three metaheuristics — in success rate, path quality, and consistency across environments with up to 40 obstacles spanning 25 kilometers."

---

## Main Points to Cover (in order)

```
1. THE PROBLEM
   Say: "The fundamental challenge in UAV path planning is scaling to large environments.
   Classic Q-learning works by storing a table of values for every possible position —
   but in a large 3D environment, this table becomes impossibly large. Metaheuristic
   algorithms like PSO and GWO treat path planning as a one-shot optimization problem,
   but they often get trapped in suboptimal solutions when the environment is cluttered
   or large-scale. The result is either an algorithm that can't store enough information,
   or one that generates paths that pass straight through obstacles."

2. WHY EXISTING SOLUTIONS WEREN'T ENOUGH
   Say: "As the authors demonstrate in their experiments, metaheuristic methods like
   GWO, PSO, and SSA achieve only 20–25% success rates in large environments with
   40 obstacles — meaning they fail 75–80% of the time. Q-learning avoids obstacles
   but produces erratic, zig-zagging paths due to the state space explosion. The key
   gap was a method that could generalize across large environments, produce smooth
   efficient paths, and handle increasing obstacle density without failing."

3. THE PROPOSED APPROACH
   Say: "The authors propose a Deep Q-Network — or DQN — that replaces the Q-table
   with a 3D convolutional neural network. The flight space is discretized into a
   3D grid of cubic cells sized to the drone's dimensions, and this grid is fed
   directly to the network as input. The key innovation is a dynamic reward function:
   instead of only rewarding the drone when it reaches the destination, the authors
   give it a reward at every step equal to d3 divided by d1 plus d2, where d3 is how
   far the drone was from the target, d2 is how far it is now, and d1 is how far it
   just moved. This continuously rewards efficient progress toward the goal."

4. KEY METHODOLOGY
   Say: "The DQN uses two neural networks running in parallel. The evaluation network
   selects actions and gets trained every step. The target network is a frozen copy
   that's only updated every N episodes — this prevents the training instability
   that comes from a network chasing its own moving targets. The network architecture
   uses two 3D convolutional layers to extract spatial features from the 3D grid,
   followed by two fully connected layers, and outputs Q-values for all 26 possible
   movement directions. Input states are also normalized before entering the network,
   which improves convergence stability."

5. THE RESULTS
   Say: "The DQN was tested in four scenarios with 6, 10, 24, and 40 static obstacles,
   spanning environments from 7 km to 25 km. Compared against Q-learning, GWO, SSA,
   and PSO — each run 20 times per scenario — the DQN achieves success rates of
   98%, 93%, 88%, and 85% in scenarios 1 through 4. The next best algorithm,
   Q-learning, achieves 95%, 85%, 80%, and 70% — and the gap grows as the problem
   gets harder. Critically, PSO only achieves 20% success in Scenario 4.
   DQN also produces the shortest paths in complex scenarios and has the lowest
   standard deviation by far — meaning its behavior is consistent and predictable
   across all runs."

6. SIGNIFICANCE AND CONTRIBUTION
   Say: "The paper's main contribution is showing that a DQN with a well-designed
   dynamic reward function can solve large-scale UAV path planning where all existing
   methods fail. The three specific innovations — 3D grid state encoding to solve
   state space explosion, the dynamic d3/(d1+d2) reward to provide dense feedback,
   and input normalization for training stability — work together to produce an
   algorithm that is simultaneously the most successful, the most efficient in path
   quality, and the most consistent. The authors acknowledge the higher computational
   cost but argue it's acceptable for offline pre-mission planning."
```

---

## Anticipated Questions & Model Answers

| Question Sir Might Ask | What Ayesha Should Say |
|---|---|
| **What is the main contribution of this paper?** | "The main contribution is a DQN for UAV path planning with three innovations: a 3D grid state encoding that solves the state space explosion problem of Q-learning, a dynamic reward function d3/(d1+d2) that provides dense guidance at every step rather than only at the destination, and input normalization for training stability. Together, these enable reliable, efficient path planning in large-scale environments with up to 40 obstacles where all competing methods — metaheuristics and Q-learning — either fail or produce poor-quality paths." |
| **What is the dynamic reward function and why is it novel?** | "The dynamic reward is d3 divided by (d1 plus d2). d1 is the step size the drone just took, d2 is its new distance to the target, and d3 is its previous distance to the target. This is novel because standard RL approaches use sparse rewards — only +1 at the goal, −1 at obstacles. With sparse rewards in a large environment, the drone rarely reaches the goal by chance and gets almost no feedback to learn from. The dynamic reward gives a meaningful signal at every single step: if you moved efficiently toward the target, your reward is high; if you moved away or took a large detour, your reward is low. This dramatically accelerates learning." |
| **How is DQN different from regular Q-learning?** | "Q-learning stores a table with one value per possible state — in a large 3D environment, this means millions of entries, which becomes impossible to store and train. DQN replaces the table with a neural network that estimates Q-values from state features. The network generalizes — if it learns in one part of the environment to avoid obstacles and head toward the target, this knowledge transfers automatically to other parts. This is why DQN scales to large environments where Q-learning breaks down." |
| **Why use a 3D convolutional network specifically?** | "The environment is represented as a 3D grid — a volumetric spatial structure. A 3D convolutional neural network applies filters across all three dimensions simultaneously, detecting spatial patterns like 'obstacle cluster ahead' or 'open corridor to the left' in 3D space. A regular (2D) CNN or a flat fully-connected network would lose the spatial structure of the 3D environment. The 3D convolution is architecturally matched to the 3D input representation." |
| **What evaluation metrics were used? Are they appropriate?** | "Four metrics were used: Success Rate (SR) — percentage of runs reaching the target without collision; SLR or Straightness Line Rate — actual path length divided by Euclidean distance, measuring path efficiency; Path Length (PL) in km; and Computational Time (CT) in seconds. Each metric captures a different aspect: SR measures safety, SLR and PL measure efficiency, CT measures practicality. I think these are well-chosen. The paper is careful to report all four rather than cherry-picking the one where DQN wins, which makes the comparison honest." |
| **What are the limitations of this work?** | "The main limitations I see are: first, all obstacles are static — there's no testing with moving obstacles, which limits real-world applicability. Second, only a single drone is studied — no multi-UAV coordination. Third, there's no ablation study — the paper never tests DQN with a standard sparse reward to isolate the contribution of the dynamic reward specifically. Fourth, all experiments are simulation-only with no real hardware validation. The authors acknowledge the computational time disadvantage and mention future work on parallelization and multi-agent extensions." |
| **Why is the computational time of DQN acceptable despite being the slowest?** | "The authors argue — and I agree — that UAV path planning is typically performed offline, before the drone launches. A pilot or operator sets up the mission, the algorithm plans the route, then the drone executes it. In this workflow, taking 455 seconds to produce a high-quality, reliable plan is entirely acceptable. The alternative — using GWO which plans in 29 seconds but fails 75% of the time in Scenario 4 — is not a real option for safety-critical missions. Path safety and success rate outweigh planning speed." |
| **What dataset was used?** | "There is no external dataset — the authors built custom 3D simulation environments. The flight space is discretized into a 3D grid with cubic cells, and obstacles are placed at specific locations in each of the four test scenarios. The experiments run 20 independent executions per algorithm per scenario, producing statistically meaningful results. This is standard practice for path planning research where generating real flight data for thousands of trials would be infeasible." |
| **What future work do the authors suggest?** | "The paper suggests two directions: parallelizing DQN training to reduce the high computational cost, which is currently a bottleneck compared to faster metaheuristics; and extending to multi-agent systems where multiple drones coordinate to enhance adaptability and robustness. I would add that testing with dynamic obstacles and comparing against more modern DRL baselines like PPO or DDPG would be important next steps." |
| **How does this compare to the metaheuristic methods?** | "The comparison is dramatic in large-scale scenarios. In Scenario 4 with 40 obstacles, DQN achieves 85% success rate; PSO achieves 20%, GWO 25%, SSA 25%. The metaheuristics also generate paths that literally cross through obstacle regions — visible in the trajectory plots. GWO is the fastest (28 seconds) but the least reliable in complex scenarios. The key difference is that metaheuristics are one-shot optimization — they search for a static solution without learning from the environment. DQN learns through trial and error, allowing it to generalize to complex obstacle configurations that defeat fixed optimization strategies." |

---

## What NOT to Say

1. **Don't say** "the drone can see everything around it in real time like a sensor." In this paper, the drone's state is the 3D grid encoding — a map-based representation, not real-time sensor data. There is no limited detection range (unlike the previous TANet-TD3 paper).
2. **Don't say** "this handles multiple drones." The paper is strictly single-UAV path planning.
3. **Don't say** "DQN is faster than metaheuristics." DQN has the *longest* computational time of all algorithms. It wins on path quality and success rate, not speed.
4. **Don't say** "the obstacles are moving." All four scenarios use *static* obstacles only.
5. **Don't overstate the success rate.** Even DQN fails 15% of the time in Scenario 4. It's the best available, but not perfect.

---

## Closing Statement

> "In summary, this paper presents a DQN-based path planner with a dynamic reward function that makes deep reinforcement learning reliable for large-scale UAV navigation. The three innovations — 3D grid encoding, dynamic distance-based reward, and input normalization — address the core limitations of both Q-learning and metaheuristic approaches. The results across four progressively harder scenarios with up to 40 obstacles confirm DQN's superiority in success rate and path quality, while acknowledging the computational cost tradeoff. Thank you, sir."

---

## If You Forget Something

> "If you blank on a detail, say: 'The paper reports that — let me recall the specific figure — but the key finding is that DQN achieves the highest success rate in all four scenarios and the most consistent performance, with a standard deviation roughly 10 to 40 times smaller than the competing algorithms.'"
