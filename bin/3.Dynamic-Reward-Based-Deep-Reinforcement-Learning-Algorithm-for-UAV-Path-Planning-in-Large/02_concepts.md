# 02 — Key Concepts Explained

Every technical term in this paper, explained so you can define it confidently.

---

## CORE DOMAIN TERMS

---

## UAV Path Planning ⭐

> **In one sentence:** Computing a safe, efficient route for a drone from a starting position to a destination while avoiding all obstacles.

**The analogy:** Like GPS navigation, but in 3D space and the "roads" are empty air — you have to figure out which paths are blocked by buildings (obstacles) and find a route around them.

**Why it matters in this paper:** This is the entire problem the paper solves. The challenge is doing this in *large-scale* environments (up to 25 km) with many obstacles without needing a pre-programmed map.

**If sir asks you to define it, say:**
> "UAV path planning is the problem of computing an optimal trajectory from a start to a goal destination while avoiding obstacles. In this paper, the challenge is scaling path planning to large 3D environments where traditional algorithms fail — either because they can't store enough information or because they get stuck on local solutions."

---

## State Space Explosion

> **In one sentence:** The problem in reinforcement learning where the number of possible states becomes so large that storing a value for each one is computationally infeasible.

**The analogy:** Imagine trying to memorize a different answer for every possible position on a 25 km × 25 km × 25 km 3D grid divided into 1-meter cells. That's over 15 trillion possible positions — impossible to store in a table.

**Why it matters in this paper:** This is the core reason classic Q-learning fails for large environments. Q-learning stores a table with one row per state — when the environment is large, this table becomes impossibly huge. DQN solves this by using a neural network as a function approximator instead of a table.

**If sir asks you to define it, say:**
> "State space explosion occurs when the number of distinct states in an environment grows exponentially with problem size, making it impossible for Q-learning to store a Q-value for every state. The DQN in this paper addresses this by using a neural network to estimate Q-values from input features, rather than maintaining an explicit lookup table."

---

## Local Optima

> **In one sentence:** A solution that appears to be the best in its immediate neighborhood but is not the globally best solution overall.

**The analogy:** Imagine climbing hills in the dark. You feel around and find the highest point nearby — but you might be on a small hill, not the tallest mountain. Metaheuristic algorithms like PSO and GWO face this problem in complex environments.

**Why it matters in this paper:** PSO, GWO, and SSA — the metaheuristic competitors — all suffer from getting trapped in local optima in large environments, leading them to generate paths that pass through obstacles (failure). DQN avoids this because it learns adaptively from environment feedback.

---

## TECHNICAL / ALGORITHM TERMS

---

## Deep Q-Network (DQN) ⭐

> **In one sentence:** A reinforcement learning algorithm that uses a deep neural network to estimate Q-values — eliminating the need for a Q-table and enabling learning in large, complex environments.

**The analogy:** Instead of memorizing the value of every possible position in a city (Q-table), DQN trains a GPS-like AI that can *estimate* the value of any position it hasn't explicitly visited, based on patterns it learned from experience.

**Key components in this paper:**
- **Evaluation Q-network (QE):** Active network that selects actions and gets updated every step
- **Target Q-network (QT):** A periodically-updated copy of QE used as a stable reference for computing target values
- **Replay buffer:** Stores past experiences (state, action, reward, next-state)
- **ε-greedy policy:** Balances exploration (random actions) and exploitation (best known action)

**Why it matters:** DQN replaces the Q-table entirely. The neural network generalizes from seen situations to unseen ones, allowing it to work in large environments where the Q-table would be impossibly large.

**If sir asks you to define it, say:**
> "A Deep Q-Network is a reinforcement learning method that uses a deep neural network to approximate the Q-value function — the estimated long-term reward for taking a specific action in a specific state. This eliminates the Q-table, making the approach scalable to large, high-dimensional environments. In this paper, a 3D convolutional DQN is used so the network can directly process the spatial structure of the 3D flight environment."

---

## Dynamic Reward Function ⭐

> **In one sentence:** A reward formula that gives the drone a different, distance-dependent reward at every step — not just at the destination — continuously guiding it toward the goal.

**The formula:**
```
R = { +1          if next cell is the target
    { -1          if next cell is an obstacle (forbidden)
    { d3/(d1+d2)  otherwise (the dynamic part)
```

Where:
- **d1** = distance the drone just moved (current → next position)
- **d2** = distance from next position to target
- **d3** = distance from current position to target (before the move)

**Why this works:** The ratio d3/(d1+d2) is higher when the drone moves toward the target efficiently. If the drone moves closer to the target (d2 decreases) with a small step (d1 is small), the reward increases. This provides dense, informative feedback at every single step — far more informative than just rewarding arrival at the destination.

**The analogy:** Think of it like a hot/cold game — you get a score at every step saying "you're getting warmer" (high reward) or "you're getting colder" (low reward), rather than only cheering when you touch the goal.

**Why it matters:** Standard sparse rewards (+1 at goal, 0 elsewhere) make it very hard to learn in large environments — the drone rarely reaches the goal by accident, so it rarely gets positive feedback. The dynamic reward ensures it always gets a meaningful signal.

**If sir asks you to define it, say:**
> "The dynamic reward function provides continuous feedback based on the drone's distance progress toward the target. Instead of only rewarding arrival, it gives a score of d3 divided by (d1+d2) at every step, where d3 is the drone's previous distance to the target and d2 is the new distance. Moves that efficiently reduce the distance to the target receive higher rewards, which significantly accelerates learning and prevents the agent from wandering aimlessly."

---

## MDP — Markov Decision Process ⭐

> **In one sentence:** A mathematical framework for sequential decision-making where the next state depends only on the current state and action — not on the full history.

**The analogy:** A chess game is almost an MDP — your next move depends on the current board position, not on every move that led to it. The "Markov property" means the current state contains all the information you need.

**Components in this paper:**
- **State space S:** All possible drone positions/configurations in the 3D grid
- **Action space A:** 26 possible movement directions
- **Reward function R:** Dynamic reward based on distances
- **Transition probability T:** How likely each action is to lead to each next state
- **Discount factor γ = 0.8:** How much future rewards are weighted vs. immediate ones

**Note:** This paper uses a full MDP (not a POMDP like the previous paper) — the drone is assumed to have full knowledge of its current position and the obstacle layout within the grid. There is no partial observability.

**If sir asks you to define it, say:**
> "An MDP is a Markov Decision Process — the standard mathematical framework for reinforcement learning problems. It specifies the state space, action space, reward function, and state transition probabilities. In this paper, the UAV path planning problem is modeled as an MDP where the state encodes the drone's 3D grid position and the action is a movement in one of 26 directions."

---

## Evaluation Q-Network (QE) and Target Q-Network (QT)

> **In one sentence:** Two separate neural networks — one actively learning, one periodically frozen — used together to stabilize DQN training.

**The analogy:** Imagine trying to aim at a moving target while also being the target. That's what happens if you use a single Q-network for both updating and evaluating — the target you're chasing keeps shifting. By freezing the target network (QT) and only updating it every N episodes, you give the learning network (QE) a stable reference to learn from.

**Why it matters:** Using two networks prevents the "deadly triad" instability of DQN — where updates to the network cause its own training targets to shift, creating oscillations and divergence. The paper explicitly says: "This approach mitigates the issue of excessive data correlation during updates in a single network, thereby enhancing algorithm convergence."

---

## ε-Greedy Policy

> **In one sentence:** A strategy that balances exploration (trying random actions) and exploitation (using the best known action) by using a probability parameter ε.

**In this paper:** ε = 0.9. This means:
- With probability 0.9 (90%): take a random action → explore
- With probability 0.1 (10%): take the best known action → exploit

**Why it matters:** If the drone always picks the best known action, it never discovers better routes. If it always acts randomly, it never learns. ε-greedy balances these. Over training, ε typically decays so the drone explores more at first and exploits more later.

---

## 3D Convolutional Neural Network (3D CNN)

> **In one sentence:** A neural network that applies filters to 3D volumetric data, detecting spatial patterns in all three dimensions simultaneously.

**The analogy:** A regular (2D) CNN recognizes patterns in images (like detecting edges or faces). A 3D CNN does the same for volumetric data — detecting spatial patterns in a 3D environment like "there's an obstacle cluster in this direction" or "there's open space ahead."

**Architecture in this paper:**
- Layer 1: 64 filters, kernel size 5×5×5, stride 1, zero-padding, ReLU activation
- Layer 2: 32 filters, kernel size 5×5×5, stride 1, zero-padding, ReLU activation
- FC Layer 1: 256 neurons
- FC Layer 2: 256 neurons
- Output: 26 neurons (one per action direction)

**Why it matters:** The 3D CNN allows the DQN to directly process the 3D grid representation of the environment, extracting spatial features about obstacles and free space that a flat (tabular or 1D) approach would miss.

---

## Replay Buffer

> **In one sentence:** A memory bank that stores past experiences so the network can learn from them in random order, preventing correlations between consecutive training samples.

**In this paper:** Buffer size = 2,000 experiences. When full, newest experiences replace oldest. Training samples κ = 32 experiences at random from the buffer.

**Why it matters:** If you train on consecutive experiences, each one is very similar to the previous — this introduces correlations that destabilize learning. Random sampling from a replay buffer breaks these correlations, making training more stable and efficient.

---

## EVALUATION METRICS

---

## SLR — Straightness Line Rate ⭐

> **In one sentence:** The ratio of the actual path length to the straight-line (Euclidean) distance between start and goal — lower is better (1.0 is a perfectly straight line).

**Formula:** SLR = Actual Path Length ÷ Euclidean Distance (start to goal)

**Interpretation:** SLR = 1.0 means the drone flew in a perfect straight line (impossible when obstacles exist). SLR = 2.0 means the drone flew twice the minimum possible distance. Lower SLR = more efficient, smoother path.

**DQN's best result:** SLR = 1.0697 in Scenario 4 — the closest to a straight line of any algorithm, meaning DQN finds the most direct obstacle-free route.

**If sir asks you to define it, say:**
> "SLR is the Straightness Line Rate — the ratio of the actual path length to the direct Euclidean distance from start to goal. A value of 1.0 is a perfect straight line; higher values indicate more detours. The DQN achieves the lowest SLR in complex scenarios, confirming it finds the most direct feasible path."

---

## SR — Success Rate

> **In one sentence:** The percentage of runs (out of 20 independent executions) in which the drone successfully reached the target without hitting any obstacle.

**Why it matters:** This is the most critical metric — a path planning algorithm that fails 50% of the time is dangerous in practice. DQN's 85% success rate in the hardest scenario versus PSO's 20% is the starkest contrast in the paper.

---

## CT — Computational Time

> **In one sentence:** The wall-clock time in seconds required to compute the path from start to goal.

**Trade-off:** DQN takes 133–456 seconds (longest of all algorithms). GWO takes 13–29 seconds (fastest). However, the authors argue that for UAV missions, path quality and safety outweigh planning speed, especially when planning is done offline before launch.

---

## PL — Path Length

> **In one sentence:** The total distance traveled by the drone along the computed path, measured in kilometers.

**Key result:** In Scenario 4, DQN's mean PL = 44.466 km vs. Q-Learning's 64.195 km — DQN's path is 31% shorter despite the environment being more complex. This confirms the dynamic reward function guides the drone to more efficient routes.

---

## STD — Standard Deviation

> **In one sentence:** A measure of how much the performance varies across repeated runs — lower STD means more reliable, consistent results.

**Why it matters:** A low STD confirms the algorithm is *robust* — it doesn't just get lucky sometimes. DQN's STD for SLR is 0.0052–0.0063, far lower than PSO (0.044–0.194) or Q-Learning (up to 0.205). This is one of DQN's strongest arguments for real-world use.

---

## BASELINE ALGORITHMS

---

## Q-Learning

> **In one sentence:** The classical reinforcement learning algorithm that stores Q-values in an explicit table and updates them via the Bellman equation.

**Why it's a baseline:** Q-learning is DQN's direct predecessor. It works well in small environments but fails in large ones due to state space explosion. In this paper, Q-learning achieves reasonable success rates (70–95%) but produces zig-zagging paths with poor SLR and has inconsistent performance (high STD in large scenarios).

---

## GWO — Grey Wolf Optimizer

> **In one sentence:** A metaheuristic optimization algorithm inspired by the hunting behavior of grey wolves — it maintains a pack hierarchy to guide search toward optimal solutions.

**Why it's a baseline:** GWO is the fastest algorithm in the comparison (13–29 seconds). However, its success rate collapses to 25% in Scenario 4 — it generates paths that pass through obstacles in large environments. Fast but unreliable.

---

## PSO — Particle Swarm Optimization

> **In one sentence:** A metaheuristic algorithm where a swarm of particles explores the solution space, updating their positions based on their own best known position and the swarm's best known position.

**Performance in this paper:** PSO has the worst success rate of all algorithms in complex scenarios (20% in Scenario 4) despite having moderate computational time. It gets severely trapped in local optima in large environments.

---

## SSA — Salp Swarm Algorithm

> **In one sentence:** A bio-inspired metaheuristic mimicking the swarming behavior of salps (marine organisms) that chain together to navigate ocean currents.

**Performance in this paper:** Similar to PSO — success rate collapses to 25% in Scenario 4. All three metaheuristics (PSO, GWO, SSA) fail to handle the dimensionality of large-scale environments.
