# 04 — Results: What They Found

---

## Key Results

### Result 1: HPER-D3QN converges fastest and to the highest reward during training
During 30,000 training episodes, all methods initially showed declining rewards due to frequent collisions during exploration. Around episode 3,500, all methods began improving. HPER-D3QN showed the fastest growth rate and the smallest standard deviation (most stable training). After approximately 25,000 episodes, all methods converged, with HPER-D3QN converging to a reward of **2.36** — consistently higher than every other method.

**What this means:** The HPER mechanism makes the AI learn faster and more stably than all comparison methods. The hierarchical prioritization ensures the agent spends more training time on the critical experiences (collisions, arrivals) that shape its policy most effectively.

---

### Result 2 ⭐ (Most Impressive): HPER-D3QN achieves 96.28% success rate with 25 aircraft — the smallest degradation of any method
When the number of aircraft in the airspace scales from 3 to 25:

| Method | Success rate (N=3) | Success rate (N=25) | Drop |
|--------|-------------------|--------------------|----|
| **HPER-D3QN** | **99.95%** | **96.28%** | **-3.67%** |
| PER-D3QN | 99.89% | 94.55% | -5.34% |
| D3QN | 99.88% | 93.58% | -6.30% |
| Dueling DQN | 99.86% | 92.61% | -7.25% |
| DDQN | 99.80% | 91.90% | -7.90% |
| DQN | 99.80% | 91.84% | -7.96% |

**What this means:** In sparse airspace, every method works well — the challenge is easy. In dense airspace with 25 aircraft, HPER-D3QN's performance drops by only 3.67 percentage points while DQN drops by nearly 8 percentage points. This gap directly translates to fewer collisions and failed missions in a real battlefield.

---

### Result 3: HPER-D3QN is most time-efficient and generates fewest dangerous close calls
From low-density (N=3) to high-density (N=25):

| Method | Time increase (s) | FHP increase (×10⁻²) |
|--------|------------------|----------------------|
| **HPER-D3QN** | **+42.91** | **+4.84** |
| PER-D3QN | +55.19 | +6.90 |
| D3QN | +51.01 | +7.48 |
| DQN | +65.95 | +8.23 |

**What this means:** When airspace gets crowded, HPER-D3QN takes only 43 more seconds to complete its mission versus DQN's 66 extra seconds. More importantly, HPER-D3QN enters other aircraft's warning zones far less frequently than all other methods — it genuinely finds safer flight paths, not just lucky escapes.

---

### Result 4: HPER-D3QN is the most robust against environmental uncertainty
At the maximum uncertainty level (Level 5: ±10° heading error, ±5 m/s speed error, ±12 m/s wind speed fluctuation):

| Method | Success rate (l=0) | Success rate (l=5) | Drop |
|--------|-------------------|--------------------|----|
| **HPER-D3QN** | **97.16%** | **95.06%** | **-2.10%** |
| PER-D3QN | 95.90% | 92.3% | -3.60% |
| D3QN | 95.40% | 91.00% | -4.40% |
| DQN | 94.00% | 86.93% | -7.07% |

**What this means:** When the environment becomes maximally chaotic — wind blowing hard, all aircraft drifting from their intended paths — HPER-D3QN loses only 2.1% of its success rate while DQN loses 7.07%. In a real military scenario, robustness under uncertainty is everything. A system that works well in the lab but degrades sharply in chaos is useless in combat.

---

### Result 5: HPER-D3QN outperforms NASA's rule-based standard and dynamic programming
Compared to two established industry methods (Rule-Based = NASA DO-365C, DP-Based = ACAS Xu) under uncertainty level 5 with varying aircraft counts:

- HPER-D3QN maintains success rate above 95% at all aircraft densities
- Rule-Based and DP-Based methods show much steeper decline as aircraft count increases
- HPER-D3QN achieves the shortest task completion times across all densities
- Rule-Based and DP-Based show rapidly increasing FHP in dense traffic — they generate many more near-miss events

**What this means:** The proposed method outperforms not just other deep learning approaches but also the current established industry standards for collision avoidance. This is a strong result because Rule-Based and DP-Based are the real-world benchmarks used in aviation today.

---

### Result 6: Ablation study confirms HPER and DTPA are the two most critical components
Results from the ablation experiment (25 aircraft, uncertainty level 5):

| Configuration | Success rate | Success rate drop | FHP increase |
|--------------|-------------|------------------|-------------|
| Full HPER-D3QN (baseline) | 95.82% | 0% | 0% |
| No HPER | 86.93% | **-9.27%** | **+87.26%** |
| No DTPA | 87.21% | -8.98% | +92.54% |
| No Dueling | 91.31% | -4.71% | +33.33% |
| No Double | 92.81% | -3.14% | +31.84% |

**What this means:** Removing HPER causes the single biggest success rate drop (-9.27%) and removing DTPA causes the biggest explosion in dangerous proximity events (+92.54%). Both are essential. By comparison, the DDQN and Dueling architecture improvements help (about 3–5% each) but are less critical than the two main innovations.

---

### Result 7: The trained model successfully transfers to a high-fidelity 3D environment
In the Unity3D simulation with 10 manned + 10 unmanned aircraft:

- At t=125s: UAV detected manned aircraft MA4 and executed a right-turn avoidance maneuver
- At t=216s: UAV encountered UAV5 on its left and accelerated a right-turn to avoid it
- At t=295s: UAV reached its designated mission destination successfully

**What this means:** The algorithm trained purely in the PyGame 2D simulator generalizes to a completely different, more realistic 3D environment. This is called the "sim-to-real gap" — and clearing it is a major milestone for any autonomous system intended for real deployment.

---

## Tables and Figures Explained

### Figure 9: Training Curves
**What it shows:** Smoothed average reward over 30,000 training episodes for all 6 methods. Solid lines are smoothed averages; transparent bands show standard deviation.

**Key takeaway:** HPER-D3QN (red line) climbs fastest, reaches the highest plateau (2.36), and has the narrowest standard deviation band — meaning it trains fastest, performs best, and is most stable.

**What to say to sir:** "Figure 9 shows that HPER-D3QN reaches a higher reward level faster than all other methods, and its smaller standard deviation band shows it trains more consistently — the other methods fluctuate more during training."

---

### Figure 10: Test Trajectories with Different Numbers of Aircraft
**What it shows:** Visual snapshots of the UAV's flight trajectory in simulated airspaces with 3, 5, 10, 15, 20, and 25 aircraft. The UAV's path, protected zones (red circles), and warning zones (orange circles) are shown.

**Key takeaway:** As more aircraft are added, the paths become more tortuous — the UAV must make more diversions. Despite this complexity, HPER-D3QN successfully navigates to its destination.

**What to say to sir:** "Figure 10 visualizes how the collision avoidance trajectories become more complex as more aircraft are added. The UAV has to make more evasive maneuvers in denser scenarios, which is why task completion time increases with aircraft count."

---

### Figure 11: Success Rate Bar Chart — Different Numbers of Aircraft
**What it shows:** Bar chart comparing success rates of all 6 methods at aircraft counts of 3, 5, 10, 15, 20, and 25. Error bars show standard deviation over 10 repetitions.

**Key takeaway:** At N=25, HPER-D3QN (red bar) is clearly the highest bar at 96.28%, while DQN (dark blue) is the lowest at 91.84%. The gap widens as aircraft count increases.

**What to say to sir:** "Figure 11 is the most direct performance comparison. At 25 aircraft, HPER-D3QN's success rate of 96.28% is about 4.4 percentage points higher than DQN's 91.84%. The gap increases in denser scenarios because HPER-D3QN handles the complexity better."

---

### Table 5: Complete Metrics — Different Numbers of Aircraft
**What it shows:** Numerical values for all three metrics (success rate, task completion time, FHP) at N=3 and N=25 for all methods, plus the change (Δ) between them.

**Key takeaway:** HPER-D3QN has the smallest delta on all three metrics — smallest success rate drop, smallest time increase, smallest FHP increase. This confirms it scales best to dense traffic.

**What to say to sir:** "Table 5 shows that HPER-D3QN's task completion time only increases by 42.91 seconds when going from 3 to 25 aircraft, while DQN's increases by 65.95 seconds. HPER-D3QN also has the smallest FHP increase, meaning it creates fewer dangerous close calls in dense traffic."

---

### Table 6: Uncertainty Level Definitions
**What it shows:** The exact error ranges for each of the 6 uncertainty levels — heading errors and speed errors for manned aircraft and UAVs, plus wind direction and speed fluctuations.

**Key takeaway:** This table shows that UAVs have consistently larger error ranges than manned aircraft at every uncertainty level, reflecting UAVs' greater sensitivity to disturbances.

**What to say to sir:** "Table 6 defines the six uncertainty levels used in the experiments. At Level 5, UAVs can have heading errors up to ±10 degrees and speed errors up to ±5 m/s, while manned aircraft have smaller errors — ±5 degrees and ±2.5 m/s. This models the real-world fact that drones are more susceptible to disturbances than manned jets."

---

### Figure 12: Success Rate Under Different Uncertainty Levels
**What it shows:** 6-panel figure showing success rate vs. aircraft count for each of the 6 uncertainty levels (l=0 to l=5).

**Key takeaway:** As uncertainty increases from panel (a) to (f), all methods' curves drop lower. But HPER-D3QN's curve remains the topmost line in every panel, and its decline rate is the smallest.

**What to say to sir:** "Figure 12 shows that HPER-D3QN maintains the highest success rate across all six uncertainty levels. Even at the most chaotic Level 5 with maximum aircraft density, HPER-D3QN achieves 95.06% compared to DQN's 86.93% — a nearly 8-percentage-point advantage."

---

### Table 7: Complete Metrics — Different Uncertainty Levels
**What it shows:** Success rate, task completion time, and FHP at l=0 (no uncertainty) versus l=5 (maximum uncertainty) for all methods.

**Key takeaway:** HPER-D3QN's success rate drops by only 2.10% from l=0 to l=5, while DQN drops by 7.07%. HPER-D3QN's task completion time increases by only 14.36 seconds, while DQN increases by 24.55 seconds.

---

### Figure 13: Success Rate Under Different Manned-to-Unmanned Ratios
**What it shows:** 6-panel figure showing how performance changes when the proportion of UAVs in the airspace ranges from 0% (all manned) to 100% (all UAVs).

**Key takeaway:** Success rates decrease as UAV proportion increases, because UAVs have higher uncertainty and less predictable behavior. HPER-D3QN is always the top line.

**What to say to sir:** "Figure 13 shows that when the airspace contains more UAVs (which have higher uncertainty), collision avoidance becomes harder for all methods. But HPER-D3QN's advantage is consistent across all ratios — it handles heterogeneous airspace composition better than any other method."

---

### Table 8: Metrics Under Different Manned-Unmanned Ratios
**What it shows:** Performance metrics when ρ=0 (all manned) versus ρ=1 (all unmanned).

**Key takeaway:** Interestingly, task completion time decreases when going from all-manned to all-UAV airspace — because manned aircraft have larger warning zones (800 m) that cause more diversions. HPER-D3QN's FHP also decreases (-1.96) in this transition, showing it adapts to the composition change well.

---

### Figure 14: HPER-D3QN vs. Rule-Based vs. DP-Based
**What it shows:** Three-panel comparison of success rate, task completion time, and FHP between HPER-D3QN, the NASA rule-based standard, and the dynamic programming ACAS Xu method.

**Key takeaway:** HPER-D3QN outperforms both traditional methods on all three metrics at every aircraft density. The gap widens as aircraft count increases.

**What to say to sir:** "Figure 14 compares HPER-D3QN against two established industry standards — NASA's rule-based DAA system and the ACAS Xu dynamic programming system. HPER-D3QN outperforms both, particularly in high-density scenarios, which demonstrates that the DRL approach is more scalable than traditional methods in complex environments."

---

### Table 9: Ablation Experiment Results
**What it shows:** Performance loss when each of the four key components (DTPA, HPER, Dueling, Double) is removed from the full HPER-D3QN model.

**Key takeaway:** HPER removal causes the largest success rate drop (-9.27%) and DTPA removal causes the largest FHP increase (+92.54%). Dueling and Double DQN improvements contribute positively but are less critical.

**What to say to sir:** "Table 9 is the most important evidence supporting the paper's claims. It shows that every component contributes to performance, but HPER and DTPA are the most critical. Without HPER, the system is nearly as bad as basic DQN. This confirms the paper's central argument that hierarchical experience prioritization is essential for learning in complex joint airspace."

---

### Figure 15: Unity3D High-Fidelity Simulation Platform
**What it shows:** A screenshot of the Unity3D battlefield simulation environment — a realistic 3D render of airspace with aircraft, terrain, and atmospheric effects.

**Key takeaway:** The simulation looks like a real military airspace, validating that the test environment is a credible high-fidelity test bed.

---

### Figure 16: UAV Trajectories During Transfer Test
**What it shows:** Six panels showing the UAV's trajectory in the Unity3D environment at three critical moments — t=125s (2D and 3D view), t=216s (2D and 3D), t=295s (2D and 3D).

**Key takeaway:** The UAV correctly detects and avoids a manned aircraft at t=125s, then avoids another UAV at t=216s, and finally reaches its destination at t=295s — demonstrating the full collision avoidance capability in a realistic 3D environment.

**What to say to sir:** "Figure 16 shows the UAV's actual flight trajectory during the transfer test on the high-fidelity Unity3D platform. At 125 seconds, it detected manned aircraft MA4 and turned right to avoid it. At 216 seconds, it encountered UAV5 and accelerated its evasive turn. It successfully reached the mission target at 295 seconds — validating that the algorithm trained in a simple 2D environment generalizes to a realistic 3D battlefield simulation."

---

## Comparison with Prior Work

| Method Type | Representative Method | Limitation Overcome by This Paper |
|-------------|----------------------|-----------------------------------|
| Geometry-based | Dubins Paths | Cannot handle multi-aircraft dynamic environments |
| Heuristic optimization | Genetic Algorithm, PSO | Slow convergence, stuck in local optima in complex scenarios |
| Control-based | MPC, ADP | Requires accurate system model; fails under uncertainty |
| DRL (homogeneous) | DQN, DDQN (previous work) | Only handles one aircraft type; no wind; simplified observations |
| DRL (heterogeneous) | Rainbow DQN (Chen et al.) | Does not model wind fields; no heterogeneous type sensitivity |
| Industry standard | NASA DO-365C (Rule-Based) | Rigid rules; performance degrades in dense heterogeneous traffic |
| Industry standard | ACAS Xu (DP-based) | Computationally expensive; not designed for heterogeneous manned/UAV mix |

---

## Real-World Meaning

If this method were deployed in actual military operations, the following would change:

1. **Safer joint manned-UAV missions:** Military UAVs could safely share airspace with manned jets during joint operations without requiring constant human supervision or communication infrastructure. This is critical because communication links are often the first targets of electronic warfare.

2. **Reduced dependence on centralized air traffic control:** Each UAV carries its own intelligence — it does not need a ground station to tell it how to avoid conflicts. This makes the system resilient to command-and-control disruptions that are common in contested environments.

3. **Adaptive to mission conditions:** Unlike rigid rule-based systems, the HPER-D3QN agent adapts to varying aircraft densities, wind conditions, and fleet compositions without needing to be reprogrammed. One trained model handles scenarios from 3 to 25 aircraft.

4. **Foundation for future autonomous swarm operations:** As the paper notes in its conclusion, validating this approach in simulation is the first step toward deploying UAV swarms that can operate independently in complex military airspace — a capability that could fundamentally change how air operations are conducted.
