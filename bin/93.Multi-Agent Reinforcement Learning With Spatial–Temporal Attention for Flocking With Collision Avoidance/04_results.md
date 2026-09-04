# 04 — Results: What They Found

---

## Key Results (Numbered)

### Result 1: STAAC achieves the highest convergence reward among all 7 trained algorithms
In training (Figure 3), all 7 learning curves grow rapidly in the first 1,000 episodes and plateau by approximately 5,000 episodes. STAAC reaches the highest final average reward at convergence, outperforming all competitors. Three attention-based algorithms (HAMA, API-MADDPG, STAAC) clearly outperform non-attention methods (MADDPG, MATD3, BCDDPG, LSTM-DDQN), showing that attention mechanisms are crucial for this task.

**What this means in plain language:** After equal training time and equal number of episodes, drones trained with STAAC collectively earn more reward — they are better at following the leader AND better at staying safe — than drones trained with any of the 6 competing methods.

---

### Result 2: STAAC achieves zero collisions in standard testing (10 followers, 10 intruders)
In a 60-step test episode, the followers' minimum mutual distance D^fol_min and minimum follower-intruder distance D^int_min both remain above R_s = 15 m at all times. The distances from leader to followers (rho) are maintained between 50 and 100 m most of the time.

**What this means in plain language:** Not a single collision occurred in the entire test episode. Every drone maintained safe separation from all other drones and all intruders while staying reasonably close to the leader. This is the core task perfectly executed.

---

### Result 3 (★ Most Impressive): STAAC's collision rate is 22.73% lower than the next-best method in the hardest scenario
In the n10m20 scenario (10 followers, 20 intruders — never seen during training), STAAC achieves a collision rate of F = 0.34% ± 0.04%, compared to HAMA's collision rate of approximately 4.57% (the next best). That's approximately a 22.73% absolute reduction.

Additionally, in the n10m15 scenario, STAAC's collision rate is 7.69% lower than HAMA.
In n5m15 it is 4.76% lower than HAMA.

The advantage of STAAC grows as the number of entities increases — exactly when safe collision avoidance matters most.

**What this means in plain language:** As the environment gets harder — more drones, more intruders — STAAC's advantage over all other methods becomes dramatically larger. This is exactly the scalability property the paper claims, and the numbers back it up convincingly.

---

### Result 4: STAAC outperforms classical non-learning methods (APF and ORCA) on all metrics
In all three scenarios, APF and ORCA achieve performance comparable to MADDPG and MATD3 — which are the weaker RL baselines. STAAC significantly outperforms both classical methods in average reward G, collision rate F, and average leader-follower distance rho-bar.

**What this means in plain language:** Even the best-known hand-crafted collision avoidance algorithms (APF and ORCA) cannot match what STAAC learns from simulation. This demonstrates that learned policies can surpass expert-designed rules for complex dynamic environments.

---

### Result 5: Ablation study confirms both LSA and GTA are necessary
- TAAC (GTA only, no LSA): worst performance across all 6 scenarios
- SAAC (LSA only, no GTA): significantly better than TAAC, but worse than full STAAC
- STAAC (both): best performance, with especially large improvement in collision rate in large scenarios

In n10m20: STAAC's collision rate is 29.17% lower than SAAC's, and SAAC's is dramatically lower than TAAC's.

**What this means in plain language:** Both attention mechanisms genuinely contribute. Spatial attention (knowing which nearby entity matters most) is the more important component. But temporal attention (knowing which moment in the past matters most) also significantly reduces collision rates when many entities are present.

---

### Result 6: STAAC works in HITL with only 1.5 ms inference time — zero collisions
In the HITL experiment with 5 followers and 3 intruders over 100 seconds, no collisions occurred. D^fol_min and D^int_min remained above R_s = 15 m throughout. The leader-follower distances stayed between 50 and 150 m for most of the experiment. The most dramatic event: Follower1 started 232.74 m away from the leader but converged to within 100 m after about 50 seconds, and then maintained 50-100 m consistently.

Each drone computed its action in approximately **1.5 milliseconds** — fast enough for real-time flight control.

**What this means in plain language:** The policy transfers directly from numerical simulation to high-fidelity HITL without any retuning. Real-time performance (1.5 ms) is well within the requirements for actual flight hardware. This is strong evidence that STAAC could work on real drones.

---

## Tables and Figures Explained

### Figure 3: Learning Curves
**What it shows:** The average reward received by followers over 5,000 training episodes, for all 7 algorithms. Reward is averaged every 10 episodes.

**Key takeaway:** STAAC's learning curve converges highest (least negative reward) and fastest among all methods. The three attention-based algorithms clearly outperform the non-attention ones. STAAC is the best overall.

**What to say to sir about it:**
> "Figure 3 shows that STAAC not only reaches the highest final reward but also converges at a similar speed to other methods — both quality and efficiency are better. The clear gap between attention and non-attention methods confirms that the attention mechanisms are the key driver of performance."

---

### Figure 4: Testing Trajectories (10 followers, 10 intruders)
**What it shows:** Six snapshots of the 60-second test episode, showing the paths of 10 follower UAVs (colored green-to-red by time) and 10 intruders (colored gray-to-dark by time), along with the leader (blue).

**Key takeaway:** Followers (a) stay close to the leader in both cluttered and open airspace, and (b) visibly diverge around intruder paths (highlighted by purple rectangles) to avoid collisions.

**What to say to sir about it:**
> "Figure 4 shows the qualitative behavior of the learned policy — followers maintain cohesive formation with the leader while making autonomous avoidance maneuvers around intruders, shown by the path deflections near the purple highlighted regions."

---

### Figure 5: Testing Performance Metrics (10 followers, 10 intruders)
**What it shows:** Three time-series plots over 60 seconds: (a) distance from leader to each follower rho; (b) minimum mutual distance among followers D^fol_min; (c) minimum follower-intruder distance D^int_min.

**Key takeaway:** rho stays between 50-100 m for most of the episode (good formation). D^fol_min and D^int_min always remain above 15 m (zero collisions).

**What to say to sir about it:**
> "Figure 5 provides quantitative confirmation of what Figure 4 shows qualitatively: the dashed red line at 15 m represents the safety threshold, and both minimum distance curves always stay above it — meaning no collisions at any time step during the entire test."

---

### Figure 6: Generalization Bar Charts (3 scenarios, 9 methods)
**What it shows:** Bar charts of G (average reward), F (collision rate), and rho-bar (average leader-follower distance) across 9 methods in 3 scenarios (n5m15, n10m15, n10m20).

**Key takeaway:** STAAC bars are consistently best across all 3 charts and all 3 scenarios. The advantage in collision rate F grows as the scenario becomes harder (more entities). Classical methods APF and ORCA perform comparably to the weakest RL baselines.

**What to say to sir about it:**
> "Figure 6 is the key comparison figure. In the collision rate chart, STAAC's bars are the shortest in all scenarios, meaning fewest collisions. Crucially, as we move from n5m15 to n10m20, STAAC's relative advantage increases — the algorithm scales better than all competitors."

---

### Table I: Parameter Settings
**What it shows:** All hyperparameters used in training and simulation, including physical parameters of UAVs and RL training settings.

**Key takeaway:** The setup is realistic: v_min = 12 m/s and v_max = 18 m/s reflect real fixed-wing UAV speed constraints. Collision penalty P2 = 2000 is double the P1 = 1000, reflecting that UAV-UAV collisions are more catastrophic. Batch size = 32, replay buffer = 50,000 are standard RL values.

**What to say to sir about it:**
> "Table I shows that the physical parameters — minimum and maximum speed, heading rate limits, sensing range — are based on realistic fixed-wing UAV specifications cited in earlier literature. The large collision penalty values ensure the RL agent strongly prioritizes safety."

---

### Table II: Generalization Results (numerical)
**What it shows:** The exact numerical values (with standard deviations) of G, F, and rho-bar for all 9 methods across all 3 generalization scenarios.

**Key takeaway:**
- STAAC best G: -51.81 ± 2.09 (n5m15), -76.09 ± 2.89 (n10m15), -90.73 ± 1.06 (n10m20)
- STAAC best F: 0.20% ± 0.03% (n5m15 and n10m15), 0.34% ± 0.04% (n10m20)
- STAAC best rho-bar: 73.37 ± 2.05 m (n5m15), 84.41 ± 1.95 m (n10m15), 86.12 ± 2.03 m (n10m20)
- Worst methods: MADDPG and MATD3 with G around -250 to -280, F up to 6% in hard scenarios

**What to say to sir about it:**
> "Table II is the most important numerical result in the paper. STAAC achieves the best reward, lowest collision rate, and most appropriate leader-follower distance in every single scenario. The small standard deviations indicate consistent, reliable performance across the 100 evaluation episodes."

---

### Figure 7: Ablation Bar Charts
**What it shows:** Same bar chart format as Figure 6 but comparing TAAC, SAAC, and STAAC across 6 scenarios.

**Key takeaway:** TAAC (GTA only, no LSA) is dramatically worse than both SAAC and STAAC. STAAC is consistently better than SAAC, with the gap widening in large-entity scenarios.

**What to say to sir about it:**
> "The ablation results in Figure 7 confirm the necessity of both components. The dramatic performance drop when removing LSA shows that knowing which neighbor matters spatially is more important than knowing which time step matters — but the temporal attention still provides meaningful improvements, especially in crowded scenarios."

---

### Table III: Ablation Numerical Results
**What it shows:** G, F, and rho-bar for TAAC, SAAC, and STAAC across 6 scenarios.

**Key takeaway:**
- In n10m20: TAAC F = 2.63% ± 0.15%, SAAC F = 0.48% ± 0.10%, STAAC F = 0.34% ± 0.04%
- In n10m20: STAAC's collision rate is 29.17% lower than SAAC (0.48% - 0.34% = 0.14% reduction; 0.14/0.48 ≈ 29.17%)
- In n5m10: TAAC F = 0.93% ± 0.17%, SAAC F = 0.10% ± 0.02%, STAAC F = 0.08% ± 0.04%

**What to say to sir about it:**
> "Table III provides the ablation numbers. The key insight is that removing LSA (TAAC) degrades performance far more severely than removing GTA (SAAC). However, STAAC with both mechanisms still achieves a meaningful improvement, especially in the hardest n10m20 scenario, confirming that both components contribute synergistically."

---

### Figure 8: HITL Trajectories
**What it shows:** 8 snapshots from the QGroundControl ground control station screen during the HITL experiment. Each snapshot shows real-time trajectories of 5 follower UAVs, 1 leader, and 3 intruders on a satellite map background.

**Key takeaway:** Followers consistently track the leader even through sharp direction changes (Figures 8d-e). Figures 8f-g show the critical collision avoidance moments: at t=85s, Follower1 turns right; at t=88s, Follower2 turns left — both to avoid Intruder2.

**What to say to sir about it:**
> "Figure 8 shows the HITL experiment running on actual flight hardware against a satellite map. The yellow rectangles highlight the most critical moments — two followers autonomously executing avoidance maneuvers around an intruder. This demonstrates that the learned policy produces meaningful, coordinated behaviors when deployed on real hardware."

---

### Figure 9: HITL Performance Metrics
**What it shows:** Time-series of rho (leader distances), D^fol_min, and D^int_min over 100 seconds in the HITL experiment.

**Key takeaway:** All distances stay above 15 m throughout. Follower1 starts 232.74 m away but converges to within 100 m after 50 seconds, then maintains 50-100 m range. D^int_min shows close approaches but never drops below 15 m.

**What to say to sir about it:**
> "Figure 9 is the HITL performance proof. Even though one follower started at 232 meters from the leader — far outside normal formation — the learned policy automatically brought it back into formation within 50 seconds, with no collisions at any point. This demonstrates both reactive safety and proactive formation-keeping."

---

## Comparison with Prior Work

**Before this paper:**
- Methods like MADDPG/MATD3: Cannot handle variable-size observations; restricted to fixed neighbor counts
- APF/ORCA: Classical methods that work well for simple environments but struggle with complex dynamic scenarios involving many non-cooperative agents
- API-MADDPG (authors' own prior work): Only handled collision-free flocking in free space with no intruders
- All prior methods: Either not designed for fixed-wing UAVs, only tested with static obstacles, or assumed fixed fleet size

**This paper's improvements:**
- First to handle variable-number intruders for fixed-wing UAV flocks
- First population-invariant RL approach for this specific problem
- Zero-shot generalization to unseen fleet sizes and intruder counts
- HITL validation confirming near-real-world readiness

**Where STAAC falls short relative to alternatives:**
- The paper does not specify... any scenario where a baseline method outperforms STAAC on any metric in any tested scenario. However, the advantage is sometimes small in simpler scenarios (n5m15), suggesting STAAC's complexity may not be warranted for small, simple deployments.

---

## Real-World Meaning

If STAAC were deployed on actual fixed-wing UAV fleets:

1. **Military surveillance:** A squadron of fixed-wing reconnaissance UAVs could maintain formation over hostile territory while autonomously dodging enemy interceptors — without any human operator commanding individual avoidance maneuvers.

2. **Disaster response:** Multiple fixed-wing drones covering a large area could follow a lead aircraft while avoiding other aircraft in the emergency response airspace — all without needing dedicated communication channels between drones.

3. **Airspace integration:** As civilian airspace becomes increasingly populated with drones, the ability to handle unknown, non-cooperative intruders (other aircraft following their own paths) is essential for safe UAV fleet operations.

4. **Scalable deployment:** Because the same policy works with 5 or 15 drones (or likely more, extrapolating from results), operators could add or remove drones from a fleet mid-mission without retraining the control system — a critical operational requirement.

The 1.5 ms inference time means this could run on current commercial embedded computing hardware, making deployment practical today.
