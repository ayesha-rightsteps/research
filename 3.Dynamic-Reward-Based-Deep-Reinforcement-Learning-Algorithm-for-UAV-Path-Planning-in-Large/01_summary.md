# 01 — Full Paper Summary

---

## Paper Identity

- **Full Title:** Dynamic Reward-Based Deep Reinforcement Learning Algorithm for UAV Path Planning in Large-Scale Environments
- **Authors:** Raja Jarray (corresponding), Imen Zaghbani, Soufiene Bouallègue
- **Year:** 2025
- **Venue:** *Procedia Computer Science* 270 (2025) 692–702; presented at the 29th International Conference on Knowledge-Based and Intelligent Information & Engineering Systems (KES 2025)
- **DOI:** 10.1016/j.procs.2025.09.189
- **Affiliations:** Research Laboratory in Automatic Control (LARA), National Engineering School of Tunis (ENIT); University of Gabès, Tunisia
- **Research Domain:** Deep reinforcement learning; UAV autonomous navigation; path planning

---

## The Problem

Getting a drone safely from point A to point B seems simple — until the environment gets large. In a small, neat space, classic Q-learning can memorize a complete table of what action to take in every possible situation. But in a large 3D environment with many obstacles spread over tens of kilometers, the number of possible drone positions explodes into millions. The Q-table becomes impossibly large to store and train — a problem called *state space explosion*. Classic Q-learning breaks down entirely.

The other common approach — metaheuristic optimization algorithms like Particle Swarm Optimization (PSO), Grey Wolf Optimizer (GWO), and Salp Swarm Algorithm (SSA) — treat path planning as a fixed optimization problem: find the best route given everything you know upfront. These work fine in small, clean environments but are prone to getting stuck in *local optima* as environments grow larger and more cluttered. In scenarios 2, 3, and 4 of this paper (environments stretching to 14–25 km), these methods literally generate paths that pass straight through obstacles — a failure rate of 55–80% in the hardest scenario.

What was missing was a method that could handle large-scale 3D environments *adaptively* — learning from experience, generalizing to new obstacle configurations, and producing consistently safe, efficient paths without requiring a pre-built map or a complete Q-table.

---

## The Proposed Solution

The authors propose a **Deep Q-Network (DQN)** algorithm with three innovations tailored for UAV path planning:

1. **3D Grid State Encoding:** The flight environment is discretized into a 3D grid of cubic cells. Obstacles are represented by groups of cells, with buffer zones for safety. The drone's state (current position + environment layout) is encoded into this grid format and fed as input to a convolutional neural network — eliminating the need for a massive Q-table.

2. **Dynamic Reward Function:** Instead of giving the drone only a big reward when it reaches the goal (sparse reward — too little feedback to learn from), the authors design a reward formula that gives the drone a *continuous signal* at every step based on three distances: how far it just moved (d1), how far it is now from the target (d2), and how far it was from the target before moving (d3). The reward is d3/(d1+d2) — meaning moves that bring the drone closer to the target earn higher rewards, and the formula naturally rewards efficiency.

3. **Input Normalization:** The drone's state inputs are normalized before being fed to the network, ensuring that all features are on comparable scales. This improves training stability and speeds up convergence.

The result is a drone that learns — through trial and error across 2,000 training episodes — to navigate any path from start to goal, even in dense obstacle fields spanning 25 km.

---

## The Method (in one paragraph)

The UAV path planning problem is formulated as a Markov Decision Process (MDP). The 3D flight space is divided into a grid of cubic cells sized to the drone's radius plus safety margin. At each step, the drone observes its current state (a 3D grid encoding of its surroundings and position), selects an action from 26 possible movement directions using an ε-greedy policy, receives a dynamic reward calculated from distances to the next cell and the target, and stores this experience in a replay buffer. Two neural networks run in parallel — an evaluation Q-network (for action selection) and a target Q-network (for stable training updates). The evaluation network uses two 3D convolutional layers (64 filters, then 32 filters, kernel size 5×5×5) followed by two fully-connected layers of 256 neurons each and a 26-neuron output layer. The evaluation network is trained by minimizing the mean squared error between predicted Q-values and target Q-values; every N episodes, the evaluation network's weights are copied to the target network to prevent unstable feedback loops. This is tested across four scenarios with 6 to 40 static obstacles in environments spanning 7 to 25 km.

---

## The Key Results

1. **DQN achieves the highest success rate in all four scenarios:** 98%, 93%, 88%, and 85% for scenarios 1–4 respectively. Q-learning (the nearest competitor) scores 95%, 85%, 80%, 70% — meaning DQN's advantage grows in harder scenarios. Metaheuristics collapse: PSO achieves only 20% success rate in the hardest scenario.

2. **DQN produces the shortest paths in large-scale scenarios:** In Scenario 4 (40 obstacles, 25 km environment), DQN achieves a mean path length of 44.466 km vs. Q-Learning's 64.195 km — 31% shorter. GWO produces a mean path of 55.810 km but at only 25% success rate. ⭐

3. **DQN has the most consistent performance (lowest standard deviation):** DQN's STD for SLR is 0.0052–0.0063 across all scenarios, dramatically smaller than PSO (0.044–0.194) and Q-Learning (0.006–0.205). This means DQN gives reliably similar results every time it runs — the others are unpredictable.

4. **DQN generates smoother, straighter paths:** Unlike Q-learning which produces zig-zagging paths with sharp turns, DQN's paths have gradual transitions between waypoints. In Scenario 4, DQN's mean SLR of 1.0697 is the closest to 1.0 (perfect straight line) of any algorithm.

5. **DQN's only weakness is computational time:** Training takes 132–456 seconds vs. GWO's 13–29 seconds. However, the authors argue this is acceptable because path planning is typically done offline before mission launch — path quality matters more than planning speed.

---

## The Contribution

This paper contributes a practical, scalable DQN-based path planner for UAVs that introduces a novel dynamic distance-based reward function and a 3D grid state encoding, solving the state space explosion of Q-learning and the local optima failures of metaheuristics — demonstrated to be superior in success rate, path length, and consistency across four progressively harder large-scale scenarios.

**One-sentence takeaway:** By replacing the Q-table with a 3D convolutional neural network and designing a dynamic reward that continuously guides the drone toward its goal, the proposed DQN makes collision-free UAV path planning reliable and efficient in large, obstacle-dense environments where all competing methods fail.
