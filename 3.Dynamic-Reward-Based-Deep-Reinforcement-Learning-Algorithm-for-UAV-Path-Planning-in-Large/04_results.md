# 04 — Results: What They Found and Why It Matters

---

## Key Results

**Result 1: DQN achieves the highest success rate in every scenario** ⭐

| Algorithm | Scenario 1 (6 obs) | Scenario 2 (10 obs) | Scenario 3 (24 obs) | Scenario 4 (40 obs) |
|-----------|-------------------|--------------------|--------------------|--------------------|
| **DQN** | **98%** | **93%** | **88%** | **85%** |
| Q-Learning | 95% | 85% | 80% | 70% |
| GWO | 75% | 45% | 40% | 25% |
| SSA | 70% | 40% | 35% | 25% |
| PSO | 60% | 40% | 35% | 20% |

*What this means:* In the hardest scenario (40 obstacles, 25 km environment), DQN successfully reaches the target 17 out of 20 runs. PSO only manages 4 out of 20. This is the most important metric — a path planner that fails 75–80% of the time is dangerous for real operations. DQN maintains viable performance even when the environment gets dramatically harder.

---

**Result 2: DQN produces the shortest paths in complex scenarios**

Mean Path Length (km):

| Algorithm | Scenario 1 | Scenario 2 | Scenario 3 | Scenario 4 |
|-----------|-----------|-----------|-----------|-----------|
| **DQN** | 10.542 | 23.604 | **31.668** | **44.466** |
| Q-Learning | 11.601 | 24.806 | 35.107 | 64.195 |
| GWO | 10.061 | 21.258 | 35.215 | 55.810 |
| SSA | 11.016 | 23.985 | 44.170 | 72.700 |
| PSO | 11.479 | 33.512 | 75.930 | 139.30 |

*What this means:* GWO has slightly shorter paths than DQN in Scenarios 1 and 2, but at only 45% and 25% success rates — it crashes the other 55–75% of the time. Among algorithms that actually work reliably, DQN produces the shortest paths in the hard scenarios. In Scenario 4, DQN's mean path (44.466 km) is 31% shorter than Q-Learning (64.195 km) and 20% shorter than GWO (55.810 km) — and GWO only succeeds 25% of the time anyway.

---

**Result 3: DQN is the most consistent — lowest standard deviation by far**

STD of Path Length (km):

| Algorithm | Scenario 1 | Scenario 2 | Scenario 3 | Scenario 4 |
|-----------|-----------|-----------|-----------|-----------|
| **DQN** | **0.0052** | **0.0049** | **0.0063** | **0.0054** |
| Q-Learning | 0.0058 | 0.0416 | 0.0852 | 0.2054 |
| GWO | 0.0140 | 0.0137 | 0.0161 | 0.0145 |
| PSO | 0.0440 | 0.1046 | 0.1951 | 0.1938 |

*What this means:* DQN gives almost identical results every single run (STD ≈ 0.005 km). Q-Learning's STD explodes to 0.2054 in Scenario 4 — meaning its path length varies wildly between runs (sometimes 53 km, sometimes 83 km). For a real UAV mission, you need reliable, predictable behavior. DQN delivers this; the others don't.

---

**Result 4: DQN generates the straightest paths in hard scenarios**

Mean SLR (lower = straighter, 1.0 = perfect straight line):

| Algorithm | Scenario 1 | Scenario 2 | Scenario 3 | Scenario 4 |
|-----------|-----------|-----------|-----------|-----------|
| **DQN** | 1.1714 | 1.3651 | **1.1713** | **1.0697** |
| Q-Learning | 1.2890 | 1.4346 | 1.2985 | 1.5443 |
| GWO | 1.1179 | 1.2294 | 1.3025 | 1.3426 |
| SSA | 1.2241 | 1.3871 | 1.6337 | 1.7489 |
| PSO | 1.2755 | 1.9381 | 2.8084 | 3.3512 |

*What this means:* In Scenario 4 (the hardest), DQN achieves SLR = 1.0697 — meaning it flies only 6.97% more than the minimum straight-line distance. Q-Learning has SLR = 1.5443 (54% more than minimum). PSO has SLR = 3.35 (flying 235% more than necessary — wildly inefficient). DQN finds remarkably direct routes even in complex environments. The DQN SLR actually *improves* going from Scenario 2 to Scenarios 3 and 4, suggesting it learns better strategies for dense environments.

---

**Result 5: DQN's only weakness is computational time**

Mean CT (seconds):

| Algorithm | Scenario 1 | Scenario 2 | Scenario 3 | Scenario 4 |
|-----------|-----------|-----------|-----------|-----------|
| **DQN** | **132.88** | **256.93** | **344.88** | **455.59** |
| Q-Learning | 16.583 | 93.596 | 78.816 | 160.71 |
| GWO | 12.771 | 19.063 | 23.603 | 28.652 |
| SSA | 15.231 | 22.476 | 29.690 | 35.302 |
| PSO | 112.23 | 222.22 | 314.11 | 403.42 |

*What this means:* DQN takes the longest to plan a path (455 seconds in Scenario 4 vs. GWO's 29 seconds). However, the authors correctly point out that in practice, path planning is done *offline* before the mission launches — not in real-time. A 7-minute planning time is entirely acceptable if the resulting path is safe and efficient. GWO is 16× faster but fails 75% of the time in Scenario 4.

---

**Result 6: Metaheuristics generate obstacle-crossing paths in large scenarios**

*What the trajectory plots (Figures 7–10) show:*
- **Scenario 1:** All algorithms find feasible, collision-free paths. All are roughly comparable.
- **Scenarios 2, 3, 4:** GWO, SSA, and PSO generate paths that visually cross through obstacle regions — they fail to avoid obstacles in large environments. This directly explains their low success rates (20–45%).
- **Q-Learning:** Avoids obstacles in all scenarios but produces noticeably zig-zagging, erratic paths with sharp corners. The path lacks smoothness.
- **DQN:** Avoids obstacles cleanly in all scenarios, with smooth curves and gradual direction changes. The path quality is visually and quantitatively superior to Q-learning.

*What this means:* The difference between DQN and Q-learning isn't just raw numbers — DQN produces physically better paths. A zig-zagging path is harder for a real drone to track (requires more aggressive attitude changes) and is less energy-efficient. DQN's smooth paths are more practical for real hardware.

---

## Tables and Figures Explained

### Table 1: Summary of UAV Path Planning Approaches
**What it shows:** A categorized literature review of path planning methods: conventional (A*, RRT, APF, D*, Voronoï), metaheuristics (PSO, GWO, MVO, SSA), reinforcement learning (Q-learning variants), and deep RL (DQN variants).
**Key takeaway:** The paper places itself in the deep RL category and is compared with representatives from all four categories in the experiments.
**What to say to sir:** "Table 1 contextualizes the paper within the broader field. The authors demonstrate awareness of all major approaches and justify their DQN choice by showing that conventional and metaheuristic methods have known limitations in large-scale environments that deep RL can overcome."

---

### Table 2: Flight Environment Parameters
**What it shows:** The four test scenarios with start/end coordinates and obstacle counts.
**Key takeaway:** Scenarios escalate from 7 km with 6 obstacles to 25 km in full 3D space with 40 obstacles — a deliberate difficulty ladder to stress-test all algorithms.
**What to say to sir:** "Table 2 shows the four test environments. The progression from 6 to 40 obstacles, and from a short 7 km path to a 25 km 3D mission, is designed to reveal where each algorithm breaks down. DQN is the only method that maintains above 80% success rate in all four scenarios."

---

### Table 3: DQN Hyperparameters
**What it shows:** Training configuration — 2,000 episodes, 10,000 max steps, γ=0.8, ε=0.9, batch size 32, replay buffer 2,000.
**Key takeaway:** The training budget is modest (2,000 episodes). The high ε=0.9 means heavy exploration early in training, which helps the agent discover paths in large environments before exploiting learned knowledge.
**What to say to sir:** "Table 3 shows the DQN training parameters. The exploration rate ε=0.9 is notably high — the agent tries random actions 90% of the time. This is intentional: in a large environment, the drone needs to explore extensively before it can reliably find the target."

---

### Table 4: Complete Performance Results (all algorithms, all scenarios)
**What it shows:** The most important table — full quantitative comparison with Best, Mean, Worst, STD for SLR, CT, PL, and SR for all 5 algorithms across all 4 scenarios.
**Key takeaway:** DQN wins on SR, SLR (Scenarios 3 & 4), and PL (Scenarios 3 & 4). GWO wins on CT. DQN has the lowest STD across all metrics, confirming superior robustness.
**What to say to sir:** "Table 4 is the comprehensive results table. The most striking pattern is the success rate — DQN is the only algorithm with above 80% success rate in all scenarios, while metaheuristics collapse to 20–25% in Scenario 4. The STD values also confirm DQN is far more consistent than all competitors."

---

### Figure 3: SLR Comparison Across 20 Runs
**What it shows:** Line plots of SLR values for all 5 algorithms across 20 runs per scenario.
**Key takeaway:** DQN's line (bottom) is consistently flat and low — showing stable, predictable performance. Other algorithms, especially PSO and GWO, have widely varying SLR values across runs.
**What to say to sir:** "Figure 3 visually demonstrates DQN's consistency advantage. While other algorithms fluctuate significantly between runs, DQN's SLR line stays nearly flat — confirming the low standard deviation in Table 4. This stability is critical for reliable real-world deployment."

---

### Figure 5: Box-and-Whisker Plots for SLR
**What it shows:** Statistical distribution of SLR across 20 runs — box shows interquartile range, whiskers show full range.
**Key takeaway:** DQN's box is the narrowest and lowest (Scenarios 3 and 4), confirming minimal variation. Other algorithms have wide boxes and outliers, especially in complex scenarios.
**What to say to sir:** "Figure 5 shows the distribution of SLR values. DQN's box is narrow and low, meaning consistent, near-optimal straightness. The wide boxes for PSO and GWO in Scenarios 3 and 4 reveal highly unpredictable performance — sometimes decent, sometimes terrible."

---

### Figures 7–10: Trajectory Visualizations
**What it shows:** 3D and 2D side-view plots of the paths generated by all algorithms in each scenario.
**Key takeaway:** In Scenarios 2–4, metaheuristics visibly pass through obstacle areas (colored cylinders). Q-learning avoids obstacles but zig-zags. DQN avoids obstacles with smooth, near-direct routes.
**What to say to sir:** "Figures 7 through 10 provide visual confirmation. In Scenario 2 onwards, you can see PSO, GWO, and SSA paths passing through obstacles — explaining their low success rates. Q-learning avoids obstacles but produces jagged paths. DQN consistently produces smooth, obstacle-free trajectories that closely follow the most direct feasible route."

---

## Comparison with Prior Work

**Previous best approaches:**
- Q-learning-based methods required explicit experience replay and heuristic rewards to work in 3D (Xie et al., 2020)
- GWO performed well in structured environments (Jarray, 2022) but was developed by the same group — DQN now outperforms their own prior work in large scenarios
- Heuristic DQN (Yao et al., 2022) used weighted rewards — this paper's dynamic distance-based reward is a cleaner, more principled approach

**Where DQN wins:** Success rate (all scenarios), path quality (Scenarios 3 & 4), consistency (all scenarios)

**Where DQN falls short:** Computational time — all metaheuristics are faster for path generation, though most fail at the actual task

---

## Real-World Meaning

If this DQN were deployed on a real UAV:
- A delivery drone could navigate through a dense urban environment (many buildings = many obstacles) reliably, without needing a pre-programmed obstacle map
- A military reconnaissance drone could plan a safe 25 km route through a contested area with 40 known threat zones, achieving an 85% success rate vs. PSO's 20%
- The smooth, efficient paths DQN produces would reduce battery consumption (shorter, smoother flight) and reduce mechanical wear from sharp attitude changes
- Because planning is offline, the 455-second planning time is entirely acceptable — set it running before the mission, deploy with the optimized path
