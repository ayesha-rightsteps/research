# Results — What They Found and Why It Matters

---

## Key Results

**1. Improved D3QN produces the shortest path in static scenes.**
- Improved D3QN: **51 steps** to reach target | Cumulative reward: **175.0**
- DDQN: 53 steps | Reward: 174.5
- DQN: 53 steps | Reward: 174.0
- A* and RRT-GoalBias: paths were longer than all DRL methods
- *In practice, fewer steps means less fuel consumed, less exposure time to threats, and a more efficient mission.*

**2. ⭐ Improved D3QN achieves ~95% path planning success rate in dynamic (moving obstacle) scenarios.**
- After approximately 10,000–12,000 training rounds (out of 20,000), the success rate curve crosses 90% and stabilizes near 95%
- Before 10,000 rounds, success rate is essentially 0% — the agent is still too immature to navigate moving threats
- *This is the most impressive result: no classical algorithm can achieve anything close to this in a truly dynamic environment, because they would need to replan from scratch every time an obstacle moves.*

**3. Improved D3QN achieves the least planning time and fewest turning points.**
- All DRL methods require less planning time than A* and RRT (since the policy is already trained — execution is just a forward pass through the network)
- Improved D3QN has the fewest turning points among all compared methods
- *Fewer turns = smoother path = less post-processing needed for real UAV deployment*

**4. The D3QN algorithm converges to a higher final reward than DQN and DDQN in static scenes.**
- DDQN reaches peak reward after ~4,000 rounds (fast but lower ceiling)
- DQN reaches peak reward after ~6,000 rounds (slow, with more fluctuation)
- Improved D3QN also takes ~6,000 rounds to converge, but achieves a **higher final reward** than both
- *This shows the trade-off: the enhancements (dueling, PER) make training slightly slower but produce a better policy in the end.*

**5. The model generalizes well to non-training starting positions (static scene).**
- 8 different starting positions were tested, including 5 outside the training region
- Paths 1–7: all successfully reached the target
- Path 8 (starting from (10, 30)): UAV was destroyed — path planning failure
- *7 out of 8 non-training starting positions succeeded. The single failure (Path 8) indicates a limitation in generalization that the authors acknowledge.*

---

## Tables and Figures Explained

### Table 1: The Reward Function
**What it shows:** The five reward components (r1–r5) and their corresponding values for different UAV states.
**Key takeaway:** The reward of +200 for reaching the target is much larger than the penalties, creating a clear incentive hierarchy.
**What to say to sir about it:** "The reward function is carefully designed to balance mission success (+200 for reaching the target), safety (proportional penalties for entering threat zones), and efficiency (−0.5 per step to encourage shorter paths). This is called reward shaping."

---

### Table 2: Obstacle Area Parameters
**What it shows:** The location, detection radius (Rmax), and kill radius (RMmax) of the three no-fly zones.
**Key takeaway:** Obstacle 2 is the largest threat — with a 10 km detection radius and a 9 km kill radius, it leaves a very narrow "safe margin" of only 1 km before immediate destruction.
**What to say to sir about it:** "The obstacle parameters define the danger gradient around each no-fly zone. Obstacle 2 at (30, 40) is the most dangerous, sitting along a natural flight corridor to the target, which forces the algorithm to plan a careful detour."

---

### Table 3: Simulation Hyperparameters (Static Scene)
**What it shows:** All tunable settings for the algorithm — learning rate, replay buffer size, epsilon decay schedule, etc.
**Key takeaway:** The exploration rate (ε) decays linearly from 1.0 to 0.1 over 2000 rounds — meaning the first 2000 rounds are dominated by exploration, the remaining 8000 by exploitation of learned policy.
**What to say to sir about it:** "Hyperparameter tuning was based on extensive numerical experiments. Key choices: a small learning rate (0.0005) for stable convergence, a discount factor of 0.96 to prioritize long-term survival, and a mini-batch size of 32 for efficient gradient updates."

---

### Table 4: Comparison of RL Algorithms (Static Scene)
**What it shows:** Side-by-side comparison of DQN, DDQN, and Improved D3QN on steps to target and cumulative reward.

| Algorithm | Steps | Cumulative Reward |
|-----------|-------|-------------------|
| DQN | 53 | 174.0 |
| DDQN | 53 | 174.5 |
| Improved D3QN | **51** | **175.0** |

**Key takeaway:** Improved D3QN wins on both metrics — shorter path and higher reward.
**What to say to sir about it:** "The improved D3QN consistently outperforms DQN and DDQN in the static scenario. The 2-step reduction in path length corresponds to a more direct route that keeps the UAV further from threat zones — validated by the higher reward score."

---

### Table 5: Non-Training Scenario Results (Generalization Test)
**What it shows:** 8 paths from different starting positions, with steps taken and cumulative reward.
**Key takeaway:** The trained model generalizes to 7 of 8 untrained starting positions. The single failure (Path 8, starting at (10, 30)) is the only failure case — the UAV flew into an obstacle zone.
**What to say to sir about it:** "The generalization test demonstrates that the algorithm didn't just memorize specific routes — it learned a general navigation policy. However, Path 8's failure reveals that the policy is not perfect for all starting positions, which is an honest limitation the authors acknowledge."

---

### Table 6: Dynamic Scene Hyperparameters
**What it shows:** Key hyperparameter changes for dynamic scene training vs. static.
**Key takeaway:** The learning rate is reduced 10× (from 0.0005 to 0.00005) and the replay buffer is increased 5× (10,000 → 50,000) to handle the greater complexity and variability of the dynamic environment.
**What to say to sir about it:** "For the dynamic scene, the learning rate is lowered significantly to avoid forgetting the static scene knowledge (transfer learning), and the replay buffer is enlarged to store more diverse dynamic experiences."

---

### Figure 5: Training Reward Curves (DQN vs DDQN vs Improved D3QN)
**What it shows:** Smoothed cumulative reward over 10,000 training rounds for the three DRL algorithms.
**Key takeaway:** DDQN converges fastest (4000 rounds), DQN is slowest and noisiest (6000 rounds), and Improved D3QN converges in ~6000 rounds but reaches a higher final reward plateau than both.
**What to say to sir about it:** "The reward curves show that the improved D3QN trades a slightly slower convergence for a higher final performance. This is the expected behavior of PER — it spends more time on hard examples, which slows early learning but produces a better final policy."

---

### Figure 6: Terminal States and UAV Steps During Training
**What it shows:** How the distribution of terminal states (success, collision, out-of-bounds, step-limit exceeded) changes over 10,000 training rounds, alongside average flight distance.
**Key takeaway:** After 5000 rounds, success rate exceeds 90%. Collision probability drops below 10%. Both metrics reflect a qualitative transition from "random wanderer" to "skilled navigator."
**What to say to sir about it:** "This figure visualizes the learning curve in terms of outcomes. The inflection point around 5000 rounds is where the policy becomes competent — before that, the UAV is mostly failing. The decrease in average steps over time also shows path length optimization."

---

### Figure 7: Trajectory Comparison (Multiple Algorithms, Static Scene)
**What it shows:** Visual path plots for all 6 algorithms from the same starting point (5, 8) to target (52, 52).
**Key takeaway:** All algorithms find a safe path, but the Improved D3QN path stays *furthest* from obstacle zones — a qualitative safety advantage beyond just "not entering the red zones."
**What to say to sir about it:** "Visually, the improved D3QN's path is not only collision-free but actively avoids proximity to threat zones — staying in the safer outer margins. This reflects the reward function's continuous danger penalty, which teaches the UAV to prefer distance from threats even when it's technically still safe."

---

### Figure 8: Quantitative Comparison (Path Length, Planning Time, Turning Points)
**What it shows:** Bar charts comparing the 6 algorithms across three efficiency metrics.
**Key takeaway:** Improved D3QN is shortest on all three metrics — path length, planning time, and turning points.
**What to say to sir about it:** "The bar charts confirm the quantitative superiority of the proposed algorithm. Notably, the planning time for DRL methods is very low because the policy is pre-trained — execution is just a forward pass through the network, which takes milliseconds."

---

### Figure 11: Visualized Action Field (Before and After Training)
**What it shows:** A map of the entire task area where each grid cell shows the action direction the trained policy would recommend.
**Key takeaway:** Before training: only 3 colors, random distribution, no meaningful structure. After training: diverse colors, coherent global pattern orienting toward the target, with clear detour patterns around obstacle zones.
**What to say to sir about it:** "The action field visualization is an innovative diagnostic tool introduced in this paper. It shows that the trained policy has learned a globally coherent navigation strategy — not just a memorized path. Almost every grid cell has a rational action direction, which proves the policy generalizes across the workspace."

---

### Figure 12: Dynamic Scene Training (Reward and Success Rate)
**What it shows:** Smoothed reward and success rate curves over 20,000 training rounds in the dynamic scene.
**Key takeaway:** For the first 10,000 rounds, average reward is ~−55 and success rate is essentially 0. After 10,000 rounds, rapid improvement leads to ~95% success rate by the end of training.
**What to say to sir about it:** "The dynamic scene is significantly harder — the algorithm needs 10,000+ rounds just to start learning. This is expected because the moving obstacles create a constantly changing landscape. The eventual 95% success rate demonstrates that transfer learning from the static scene provides a useful foundation."

---

### Figure 13: Dynamic Scene Test — Motion Trajectory Sequence
**What it shows:** A sequence of animation frames showing the UAV navigating around moving obstacle zones in a dynamic test scenario.
**Key takeaway:** The UAV successfully reaches the target while reactively avoiding obstacle zones that are simultaneously moving.
**What to say to sir about it:** "This figure validates real-time performance in a dynamic scenario. The UAV tracks the target while the obstacle zones shift — it's not following a pre-computed path but executing a learned policy that adapts to the current state, which is the core capability this paper develops."

---

## Comparison with Prior Work

**Previous best for static UAV path planning (DRL):** DQN and DDQN
- DQN: 53 steps, reward 174.0
- DDQN: 53 steps, reward 174.5

**This paper:** 51 steps, reward 175.0 — improvements in both dimensions.

**Classical algorithms (A*, RRT-GoalBias):** Longer paths, more turning points, comparable or slower planning time — and fundamentally unable to handle dynamic environments without full replanning.

**Where Improved D3QN wins:** Path quality (shorter, smoother), safety (stays further from threats), and — critically — the ability to handle *moving* obstacles at all.

**Where it falls short:** Generalization isn't perfect (Path 8 failure); convergence is slower than simpler baselines; dynamic training requires 20,000 rounds which is computationally intensive.

---

## Real-World Meaning

If this method were deployed on a real UAV:
- The drone could navigate through a hostile airspace with radar and missile systems without pre-programmed route data
- It could adapt in real-time as enemy defenses reposition
- The 95% success rate means 1 in 20 missions would result in loss — acceptable for high-value reconnaissance in extremely hostile environments, but not yet reliable enough for civilian use
- The short planning time (milliseconds for the trained network to execute) means the system could operate in scenarios requiring near-instant decision-making
