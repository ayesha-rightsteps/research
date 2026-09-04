# 04 — Results: What They Found and Why It Matters

---

## Key Results (Numbered)

### Result 1: DA-MAPPO achieves 90%–99% success in dynamic multi-target environments
- In ENV-1 (30 obstacles, dynamic targets): **99% success rate, 1% collision rate**
- In ENV-2 (40 obstacles, dynamic targets): **95% success rate, 5% collision rate**
- In ENV-3 (50 obstacles, dynamic targets): **90% success rate, 10% collision rate**

**What this means practically:** Even in the hardest tested scenario — 50 obstacles scattered throughout the flying area, targets constantly moving — the drone team successfully completes its mission 9 out of 10 times. This is remarkable because the environment is genuinely complex: the drones have limited sensors, imperfect communication, and no central controller.

**Compared to prior work:** The best competing method (RMAPPO) achieves 67% success in ENV-3 dynamic — DA-MAPPO beats it by 23 percentage points. NavRL achieves only 32% (58 points worse). EGO-Planner v2 achieves only 43% (47 points worse).

---

### Result 2: Up to 25 percentage points improvement over baselines ⭐ MOST IMPRESSIVE

**The headline number from the abstract:** DA-MAPPO "outperforms representative baselines by up to 25 percentage points."

Looking at ENV-1 dynamic scenario specifically:
- IPPO: 78% | RMAPPO: 85% | MAPPO: 83%
- NavRL: 63% | EGO-Planner v2: 53%
- DA-MAPPO: **99%**

The gap between DA-MAPPO (99%) and the nearest competitor RMAPPO (85%) is 14 points in ENV-1. In ENV-3, the gap between DA-MAPPO (90%) and RMAPPO (67%) is 23 points.

**Why this is impressive:** A 5–10% improvement in machine learning is typically considered a meaningful contribution. A 23-point improvement in a head-to-head comparison is extraordinary and clearly demonstrates the value of the core design choice — real-time assignment augmentation.

---

### Result 3: Near-zero static-to-dynamic degradation (only ~2% drop in the hardest setting)

**The key comparison:**
| Environment | DA-MAPPO Static | DA-MAPPO Dynamic | Drop |
|---|---|---|---|
| ENV-1 (30 obstacles) | 99% | 99% | 0% |
| ENV-2 (40 obstacles) | 95% | 95% | 0% |
| ENV-3 (50 obstacles) | 92% | 90% | 2% |

Meanwhile, baseline degradations going static → dynamic:
- IPPO: 87% → 53% (34-point drop in ENV-3)
- MAPPO: 89% → 64% (25-point drop in ENV-3)
- NavRL: 41% → 32% (9-point drop even from an already-weak baseline)

**What this means:** DA-MAPPO essentially does not care whether targets are static or moving. It adapted to dynamic targets at the same rate it handled static ones because its per-step allocation mechanism continuously updates who chases what. The baselines are fundamentally broken for dynamic targets because they were designed (or converged on strategies) that assume targets stay put.

---

### Result 4: Shortest trajectories and fewest steps in dynamic environments

In ENV-2 dynamic:
- MAPPO: T_ave = 50.14 steps, L_ave = 23.96 units
- DA-MAPPO: T_ave = **38.32 steps**, L_ave = **18.50 units**

This means DA-MAPPO is roughly 24% faster and produces trajectories 23% shorter than MAPPO in this environment.

**What this means:** DA-MAPPO is not just safer — it is more efficient. Because it always assigns the closest drone to each target, drones are not flying long detours chasing targets they have been "locked in" to from the start of the episode. The reallocation constantly improves the team-level assignment, reducing total travel distance.

---

### Result 5: Robust to sensor noise, communication failures, and fast-moving targets

**Sensor noise test (ENV-2 dynamic, 40 obstacles):**
- Baseline (no noise): 95% success
- Noise sigma_v = 0.20: 94% — barely changes
- Noise sigma_v = 0.50 (very strong): 90% — only 5% drop

**Communication interference test:**
- Baseline: 95% success
- 50% packet loss + 6-step delay: 94% — virtually no change

**Target speed test:**
- Target at 0.5 m/s: 95% success
- Target at 3 m/s (6x max UAV speed): still 95% — completely unaffected

**What this means:** The system degrades gracefully rather than catastrophically when things go wrong. This is critical for real-world deployment where sensors are noisy, radios drop packets, and targets do not move at convenient speeds.

---

## Tables and Figures Explained

### Table IV: Static Multi-Target Navigation Results

**What it shows:** Performance of all 5 algorithms in environments with 30, 40, and 50 obstacles, with targets that stay fixed.

**Key takeaway:** DA-MAPPO (99%, 95%, 92%) consistently tops every row, with MAPPO (98%, 92%, 89%) being the next best for MARL methods. NavRL and EGO-Planner v2 deteriorate severely as density increases — NavRL drops to 41% in ENV-3.

**What to say to sir about it:** "Even in the simpler static setting, DA-MAPPO outperforms all baselines, but more importantly, it degrades the least as obstacle density increases — only dropping from 99% to 92% across the three environments compared to much steeper drops in competing methods."

---

### Table V: Dynamic Multi-Target Navigation Results

**What it shows:** The same 5 algorithms now tested when targets move — the main experiment of the paper.

**Key takeaway:** The performance gap between DA-MAPPO and all baselines becomes dramatically larger in dynamic settings. In ENV-3, IPPO and MAPPO drop to 53% and 64% respectively, while DA-MAPPO holds at 90%.

**What to say to sir about it:** "This is the most important table in the paper. The moment targets start moving, all baselines deteriorate significantly, but DA-MAPPO barely changes at all — confirming that the per-step allocation is exactly what prevents the degradation."

---

### Table VI: Ablation Study Results

**What it shows:** What happens when you remove individual components of DA-MAPPO.

**Key takeaway:** Removing the augmented state causes a 100% failure rate (0% success). Reducing allocation frequency to every 50 steps causes a 3–5% drop. Removing the team reward causes a 4–6% drop.

**What to say to sir about it:** "The ablation study is the most telling experiment — when they remove the assignment-augmented observation, the success rate goes to zero across all environments. This proves the policy has learned to depend on knowing its target, and that the system is not just running a simple heuristic."

---

### Table VII & VIII: Reward Contribution Analysis

**What it shows:** For successful versus failed (collision) episodes, how much does each reward term contribute?

**Key takeaway:** In successful episodes: distance progress (56.5%) dominates, arrival bonus (10.1%) is present, all penalties are moderate. In collision episodes: distance progress (56.8%) still present but crash penalty (13.8%) is much larger, and the arrival bonus is zero (they never arrived).

**What to say to sir about it:** "The reward analysis shows the policy is primarily driven by making progress toward targets, which is exactly what was intended. The clear difference between success and collision episodes confirms the reward function is well-calibrated — it strongly differentiates good outcomes from bad ones."

---

### Table IX: Noise Robustness Results

**What it shows:** How performance degrades as increasing Gaussian noise is added to velocity and angular velocity observations.

**Key takeaway:** Success rate drops only from 95% to 90% even at the highest noise level tested — a 5% drop. The Kalman filter on acceleration estimates and the LiDAR redundancy (35 beams) help absorb the noise.

**What to say to sir about it:** "The robustness to sensor noise is important for real-world applicability. The 5% drop at the highest noise level suggests the policy is not brittle to imperfect sensing, which is a key requirement for deployment."

---

### Table X: Communication Interference Results

**What it shows:** How performance responds to stochastic packet loss (up to 50%) and communication delays (up to 6 steps).

**Key takeaway:** Performance metrics are virtually identical to the baseline across all tested interference levels — 94% success vs. 95% baseline.

**What to say to sir about it:** "This result is particularly impressive. Even with half of all communication packets dropped and messages delayed by 6 steps, the system performs as well as with perfect communication. This happens because the exchanged information is only relative positions — low-dimensional data that does not catastrophically change the policy when delayed."

---

### Table XI: Target Speed Variation Results

**What it shows:** How performance changes as target moving speed increases from 0.5 m/s up to 3 m/s.

**Key takeaway:** Success rate remains constant at 95% regardless of target speed, with only tiny increases in T_ave (38.32 → 38.90) and L_ave (18.50 → 18.69).

**What to say to sir about it:** "Even when targets move 6 times faster than the UAVs' maximum speed, the system maintains 95% success. This seems counter-intuitive, but makes sense because the allocation is updated every step — the drone always knows the current position of its target and immediately adapts."

---

### Figure 4: Trajectory Visualization in Static Scenarios

**What it shows:** 2D trajectory plots of all three drones (one per color) for each algorithm in ENV-1 static.

**Key takeaway:** IPPO shows oscillatory, overlapping paths. MAPPO and RMAPPO show some trajectory crossings. NavRL shows locally smooth but globally inefficient paths. EGO-Planner v2 has smooth individual paths but frequent inter-drone conflicts. DA-MAPPO shows clean, well-separated coordinated paths with no crossings.

**What to say to sir about it:** "Figure 4 visually confirms the quantitative results. DA-MAPPO's trajectories show the drones proactively taking separate lanes — each drone's path is guided by knowing exactly which target it is heading to and where its teammates are."

---

### Figure 5: Trajectory Visualization in Dynamic Scenarios

**What it shows:** Same visualization but with moving targets (shown as stars moving in a direction). In panel (f) for DA-MAPPO, color changes in a single drone's path indicate real-time target reassignment.

**Key takeaway:** Baselines show redundant, erratic paths because drones pursue outdated or inefficient targets. DA-MAPPO shows the most organized behavior, with color changes showing live reassignment happening mid-flight.

**What to say to sir about it:** "In DA-MAPPO's panel, you can literally see where a drone switched targets mid-flight — the line changes color. This real-time reassignment is what prevents drones from pursuing the wrong target for too long, which is exactly why it outperforms all baselines in dynamic settings."

---

### Figure 6: Computation Time vs. Number of Agents

**What it shows:** A bar chart of total per-step computation time on an NVIDIA Jetson Orin Nano edge device, for agent counts 1, 3, 5, 10, 20, 30, 40.

**Key takeaway:** For 1 agent: 1.496 ms. For 5 agents: 10.531 ms. For 40 agents: 13.586 ms. Growth is sub-linear, and even for 40 agents the latency is well under 100 ms.

**What to say to sir about it:** "The computation time scales sub-linearly with agent count, which means the framework is practically feasible for real-time deployment even on resource-constrained edge hardware. At 5 agents — a more realistic deployment size — the per-step latency is about 10 milliseconds."

---

## Comparison with Prior Work

**Before this paper:**
- Best optimization-based methods (like EGO-Planner): strong in static, clean environments; can produce theoretically optimal paths but are brittle in dynamic settings (43% in ENV-3 dynamic)
- Best MARL methods (MAPPO/RMAPPO): good coordination but assumed fixed targets; 64–67% in ENV-3 dynamic
- Safe RL (NavRL): good collision avoidance for single agents; but only 32% in ENV-3 dynamic

**This paper:**
- 90% in ENV-3 dynamic — the hardest scenario
- Near-zero static-to-dynamic degradation
- Better efficiency (shorter paths, fewer steps) than all methods in dynamic settings
- Robust to noise, communication failures, and fast-moving targets

**Where it falls short (honest):**
- Tested with only N = 3 drones — scalability to larger swarms is not tested in full
- Complexity is O(N^3) due to the Hungarian algorithm, which may bottleneck at very large swarm sizes
- No real physical drone flights — only Gazebo simulation (physics realistic but no wind, no aerodynamic effects)

---

## Real-World Meaning

If DA-MAPPO were deployed in the real world, the following would change:

1. **Disaster response:** A swarm of 5–10 drones could be deployed to search for survivors in a collapsed building. As survivors move or are discovered, the assignment updates automatically — no human operator needs to reassign drones one by one.

2. **Military/surveillance operations:** Drones intercepting or tracking multiple moving targets (vehicles, people) in cluttered urban environments could do so without a centralized command post, reducing reliance on communication infrastructure.

3. **Environmental monitoring:** UAVs tracking wildlife or environmental anomalies that move could adaptively redirect without requiring pre-planned routes or human intervention.

4. **Infrastructure inspection:** Swarms inspecting large structures (bridges, pipelines, wind farms) could dynamically reallocate inspection zones as conditions change, completing missions faster with fewer collisions.

The key real-world benefit is **robustness with no central controller** — the swarm works even if individual drones lose GPS, communication degrades, or targets change position unexpectedly. This is the kind of reliability needed for practical deployment beyond controlled environments.
