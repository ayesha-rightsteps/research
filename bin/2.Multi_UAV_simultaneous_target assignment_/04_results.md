# 04 — Results: What They Found and Why It Matters

---

## Key Results

**Result 1: TD3 outperforms DDPG for basic path planning**
- In single-UAV scenario: TD3 achieves **95% average arrival rate** vs. lower DDPG rate
- In multi-UAV scenario (3 UAVs, 1 target): TD3 achieves **90% average arrival rate**
- TD3 converges faster and more stably than DDPG in both scenarios

*What this means:* Before building the full TANet-TD3 system, the authors needed to confirm that TD3 is a better foundation than DDPG. These results justify the choice of TD3 as the navigation backbone. A 95% arrival rate in a moving-obstacle environment is impressive for a drone that only sees 0.5 units ahead in a 2-unit-wide space.

---

**Result 2: TANet-TD3 outperforms all baselines in training (Table 2)** ⭐

At Episode 5,000 (mid-training):

| Algorithm | Dynamic Env: Completion | Dynamic Env: Reward |
|-----------|------------------------|---------------------|
| **TANet-TD3** | **81.54%** | **−241.4** |
| TANet-DDPG | 71.20% | −303.5 |
| DDPG(distance) | 51.07% | −301.0 |
| TD3(distance) | 55.27% | −296.5 |

Over last 1,000 episodes (fully converged):

| Algorithm | Dynamic: Mean Completion | Mixed: Mean Completion |
|-----------|--------------------------|------------------------|
| **TANet-TD3** | **83.77%** | **84.27%** |
| TANet-DDPG | 80.70% | 80.38% |
| DDPG(distance) | 73.06% | 73.78% |
| TD3(distance) | 75.10% | 76.28% |

*What this means:* Even at the halfway point (episode 5,000), TANet-TD3 already surpasses the final performance of DDPG(distance). The largest gap — over 10 percentage points — is between TANet methods and pure distance-based methods, confirming that Q-value-based assignment (which accounts for obstacles) is fundamentally better than naive distance-based assignment.

---

**Result 3: TANet-TD3 converges significantly faster**
- TANet-TD3 converges at approximately episode **5,000**
- TANet-DDPG converges at approximately episode **5,500** (~500 episodes slower)
- TD3(distance) and DDPG(distance) converge at approximately episode **7,000** (~2,000 episodes slower)

*What this means:* Faster convergence means the algorithm needs less computation/training time to reach its best performance. The TANet assignment method is not only better at the task — it also helps the algorithm learn faster.

---

**Result 4: In direct deployment tests, TANet-TD3 achieves perfect mission completion (Table 3)**

| Environment | TANet-DDPG: Targets Reached | TANet-TD3: Targets Reached |
|-------------|-----------------------------|-----------------------------|
| Dynamic (5 UAVs, 5 targets, 20 moving obstacles) | 4/5 | **5/5** |
| Mixed (5 UAVs, 5 targets, 10 static + 10 moving obstacles) | 2/5 | **5/5** |

Reward comparison:

| Environment | TANet-DDPG | TANet-TD3 |
|-------------|------------|-----------|
| Dynamic | −256.87 | **−141.97** |
| Mixed | −452.70 | **−335.05** |

*What this means:* TANet-DDPG dramatically fails in the mixed environment — only 2 out of 5 targets covered. This is because two UAVs collide with moving obstacles and a third flies to the wrong target. TANet-TD3 handles all five perfectly. The reward difference (−141.97 vs. −256.87 in dynamic) also shows TANet-TD3 flies shorter total paths.

---

**Result 5: TANet-TD3 scales better with more UAVs**

With 20 obstacles, varying UAV count:
- At 3 UAVs: TANet-TD3 ~95%, TANet-DDPG ~95% (roughly equal)
- At 5 UAVs: TANet-TD3 ~84%, TANet-DDPG ~81% (3% gap)
- At 7 UAVs: TANet-TD3 **~71%**, TANet-DDPG **~64%** (7% gap)

*What this means:* As complexity increases, TANet-TD3's advantage grows. At 7 UAVs — where collision avoidance, assignment, and path planning become extremely challenging simultaneously — TANet-TD3 maintains viability while TANet-DDPG degrades sharply. For real-world large drone swarms, this scalability matters enormously.

---

**Result 6: TANet-TD3 scales better with more obstacles**

With 5 UAVs, varying obstacle count:
- At 10 obstacles: both algorithms ~86%
- At 25 obstacles: TANet-TD3 ~82%, TANet-DDPG ~79%
- At 30 obstacles: TANet-TD3 **>81%**, TANet-DDPG **<80%**

*What this means:* Dense obstacle environments are a hard test. TANet-TD3 maintains above 81% even with 30 moving obstacles, while TANet-DDPG drops below 80%. The absolute improvement is modest here, but consistent across all conditions — no scenario where TANet-DDPG beats TANet-TD3.

---

## Tables and Figures Explained

### Table 1: Hyperparameters of TANet-TD3
**What it shows:** The training configuration: 10,000 episodes max, 100 steps per episode, γ=0.9, learning rates, buffer size, batch size, soft update factor.
**Key takeaway:** The Actor learning rate (1E-4) is 10× smaller than the Critic learning rate (1E-3) — standard practice to prevent Actor from updating too aggressively before the Critic has a stable estimate.
**What to say to sir:** "The hyperparameters follow standard DRL practice, with a smaller actor learning rate for stability. The 10,000-episode training budget reflects the complexity of the simultaneous two-problem formulation."

---

### Table 2: Training Results of TANet-DDPG and TANet-TD3
**What it shows:** Head-to-head comparison of four algorithms in dynamic and mixed environments — both at the midpoint (episode 5,000) and averaged over the final 1,000 episodes.
**Key takeaway:** TANet-TD3 leads in all four metrics across both environments. The bold entries highlight TANet-TD3's superiority.
**What to say to sir:** "Table 2 shows that TANet-TD3 achieves the highest mean average target completion rate of 83.77% in dynamic and 84.27% in mixed environments, outperforming all baselines. The improvement over pure distance-based methods is particularly striking — over 10 percentage points — confirming that Q-value-based assignment is fundamentally superior."

---

### Table 3: Test Statistical Results
**What it shows:** In concrete test episodes with fixed initial conditions, how many targets each algorithm's converged policy actually reaches.
**Key takeaway:** TANet-TD3 achieves 5/5 in both environments. TANet-DDPG achieves 4/5 in dynamic but crashes to 2/5 in mixed — a catastrophic failure mode.
**What to say to sir:** "Table 3 is the most striking result — in the mixed environment with static and moving obstacles, TANet-DDPG only covers 2 out of 5 targets due to collision failures and wrong target assignments, while TANet-TD3 successfully completes all 5. This shows TANet-TD3's robustness to complex mixed environments."

---

### Figure 9: Convergence Curves
**What it shows:** Learning curves for all algorithms over training episodes — average target completion rate and average reward.
**Key takeaway:** TANet-TD3's curve rises faster and plateaus higher. The shaded 95% confidence intervals show TANet-TD3 is also more stable (less variance).
**What to say to sir:** "Figure 9 shows TANet-TD3 converges approximately 2,000 episodes before the distance-based methods and achieves a higher final performance plateau. The tighter confidence intervals indicate more consistent training."

---

### Figure 11 & 12: Trajectory Comparison in Dynamic Environment
**What it shows:** 3D trajectory paths and 2D views at t=4s, t=8s, t=12s — TANet-DDPG (Figure 11) vs. TANet-TD3 (Figure 12).
**Key takeaway:** In Figure 11, UAV 1 and UAV 4 converge to the same target. In Figure 12, every UAV goes to a distinct target with clear, obstacle-aware paths. UAV 2 and UAV 5 in Figure 12 visibly detour around obstacles.
**What to say to sir:** "Figures 11 and 12 visually confirm the algorithmic difference. TANet-DDPG produces an incomplete assignment — two drones collide at the same target — while TANet-TD3 achieves a perfect one-to-one assignment with obstacle-aware trajectories. UAV 2 and UAV 5 can be seen deliberately choosing longer but safer routes around obstacles."

---

### Figure 13 & 14: Trajectory Comparison in Mixed Environment
**What it shows:** Same comparison in the harder mixed-obstacle environment.
**Key takeaway:** TANet-DDPG fails badly — UAV 2 and UAV 3 collide with moving obstacles; UAV 1 flies to UAV 5's target. TANet-TD3 succeeds in all five.
**What to say to sir:** "Figure 13 and 14 show TANet-DDPG's critical weakness in mixed environments. Two of five drones crash into obstacles, and one goes to the wrong target — a 60% failure rate. TANet-TD3 handles all five targets correctly, demonstrating its superior adaptability to mixed obstacle conditions."

---

### Figure 15: Statistical Comparison (UAV Count + Obstacle Count)
**What it shows:** Four line graphs showing how target completion rate changes as you add more UAVs (3→7) or more obstacles (10→30), in dynamic and mixed environments.
**Key takeaway:** Both algorithms degrade as the problem gets harder, but TANet-TD3's degradation is slower and the gap widens. Particularly dramatic at 7 UAVs.
**What to say to sir:** "Figure 15 demonstrates that TANet-TD3 scales better than TANet-DDPG. The performance gap is small with 3 UAVs but grows to approximately 7 percentage points at 7 UAVs. This suggests TANet-TD3's Q-value-based assignment provides increasingly larger benefits as the coordination problem becomes more complex."

---

## Comparison with Prior Work

**Previous best approaches:**
- Qie et al. (2019) used MADDPG but produced incomplete target coverage when two agents were equidistant from one target
- Han et al. (2020) used PPO with distance-based assignment — doesn't account for obstacles
- Traditional methods (A*, RRT, PSO) require full global map knowledge and don't handle dynamic obstacles

**Where TANet-TD3 wins:**
- Complete target assignment in every test scenario (vs. incomplete in prior methods)
- Works with partial observability (no global map required)
- Operates in 3D dynamic environments (prior work often 2D or static)
- Simultaneous assignment and planning (not sequential)

**Where it falls short:**
- Only tested in simulation, not on real drones
- Only up to 7 UAVs tested — scalability to 20+ UAVs unclear
- No communication between UAVs (fully decentralized)

---

## Real-World Meaning

If TANet-TD3 were deployed on real drone swarms:
- **Search and rescue missions** could send 5 drones to cover 5 different sectors of a disaster zone simultaneously, dynamically re-routing around fallen debris or other hazards
- **Military strikes** could assign 5 drones to 5 targets in a contested airspace with anti-aircraft threats moving unpredictably, ensuring every target is hit exactly once
- **Agricultural monitoring** could send a drone fleet to cover different fields automatically, without human target-assignment planning

The core value proposition: reliable, complete mission execution without human coordination intervention, even when the environment actively fights against you.
