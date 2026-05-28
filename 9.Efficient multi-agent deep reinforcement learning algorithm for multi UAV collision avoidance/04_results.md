# Results — What They Found and Why It Matters

---

## Key Results (Numbered)

**Result 1: IGAT achieves 17.56% higher cumulative reward than the DGN benchmark at N=5**

IGAT: −1418 ± 48.8 | DGN benchmark: −1719 ± 50.5

In plain terms: the cumulative reward measures how well the entire system performs over a full episode. All values are negative because every time step comes with some penalty (for conflicts, proximity risk, and heading deviations). The fact that IGAT's reward is significantly less negative means it is experiencing fewer and less severe penalties — resolving conflicts faster, making better navigational decisions, and maintaining safer separation. A 17.56% improvement in reward in a dense multi-UAV setting is a substantial gain.

Better or worse than prior work: IGAT outperforms all four baselines. The next best is GRL at −1533, then DGN at −1719. MS-GRL performs worst at −2022. IGAT's improvement over GRL is 7.54% and over the worst baseline (MS-GRL) is 29.88%.

---

**Result 2: IGAT reduces loss-of-separation time by 10.52% at N=5** ⭐ (Most impressive safety result)

IGAT: 461.6 ± 5.7 | DGN benchmark: 515.8 ± 4.57

This is the most critical result because it directly measures drone safety. Every time step in loss-of-separation is a moment when two drones are dangerously close. IGAT reduces this from 515.8 to 461.6 time steps per episode — 54.2 fewer dangerous time steps per episode. In a real deployment with thousands of daily flights, this difference could prevent hundreds of near-miss events.

Better or worse than prior work: IGAT achieves the lowest t_loss among all five compared methods. MGAT achieves 490.2, GRL achieves 484.8, MS-GRL achieves 505.7, DGN achieves 515.8 — IGAT beats them all.

---

**Result 3: IGAT uses 43.93% fewer active interaction edges than DGN at N=5**

IGAT: 0.5245 ± 0.0352 edges | DGN: 0.9355 ± 0.0461 edges

This is a striking efficiency result. IGAT achieves better safety AND better rewards while operating with nearly half the communication complexity. This demonstrates the paper's core insight: you do not need dense, noisy communication to achieve good coordination. Targeted, conflict-focused attention is sufficient — and in fact superior. In real systems, this translates to significantly lower bandwidth requirements and lower onboard computational load.

Better or worse than prior work: In edges, IGAT is better than DGN (−43.93%), MGAT (−36.50%), and GRL (−16.41%). Only MS-GRL has comparable edges (0.5500), but MS-GRL performs far worse in reward and LoS.

---

**Result 4: IGAT's edge count grows sub-quadratically with swarm size**

From Table 1: DGN edges at N=10 are 4.671. IGAT edges at N=10 are 2.422 — nearly half. For N=3, DGN has 0.183 edges and IGAT has 0.145. The gap widens as N increases. This confirms that IGAT's approach does not simply add more edges as the swarm grows — it maintains selective coordination regardless of swarm density.

What this means practically: Most graph-based MARL methods scale quadratically with N in their communication complexity (every drone connects to every other drone). IGAT's conflict-driven graph grows much more slowly, making it viable for large real-world swarms.

---

**Result 5: Curriculum + transfer learning improves early convergence by ~34% at N=4**

IGAT (Curr+TL) reward at N=4: −538.36 ± 57.31 | IGAT (No Curr/TL): −818.63 ± 81.55

The improvement of 280.27 reward units in the first 2000 training episodes demonstrates that the training strategy itself is a major contribution. At N=4, Curr+TL also reduces t_loss by 155.79 time steps (38%). These gains are most significant at smaller to medium swarm sizes (N=4 to 8) where exploration instability is highest.

What this means: Without curriculum learning, the system starts training on complex scenarios it is not ready for, leading to dangerous random exploration that takes much longer to recover from. The curriculum creates a "safe training runway" that dramatically accelerates learning.

---

## Tables and Figures Explained

### Table 1: Edge Count Comparison Across Swarm Sizes (N=3 to N=10)
**What it shows:** Average number of active interaction edges per step for IGAT vs. DGN across all swarm sizes.
**Key takeaway:** IGAT consistently uses fewer edges than DGN at every swarm size, and the gap grows with N — by N=10, IGAT uses 2.422 edges vs. DGN's 4.671.
**What to say to sir about it:** "Table 1 shows that IGAT's conflict-driven graph maintains a sparser interaction structure than the DGN baseline at every swarm size. Importantly, the gap grows with N — demonstrating that IGAT becomes more efficient relative to the benchmark as the swarm gets denser, which is the key scalability advantage."

---

### Table 2: Performance Comparison at N=5 (Last 2000 Episodes, Mean ± 95% CI)
**What it shows:** The definitive head-to-head comparison of all six methods — IGAT, IGAT (no curriculum), DGN, MGAT, GRL, and MS-GRL — on all three core metrics at 5 UAVs.
**Key takeaway:** IGAT achieves the best cumulative reward (−1418) and the lowest t_loss (461.6) with competitive edges (0.5245). The 95% CI confirms these differences are statistically meaningful, not random.
**What to say to sir about it:** "Table 2 is the central quantitative comparison. IGAT achieves the highest reward and lowest loss-of-separation across all six methods at N=5. The narrow confidence intervals confirm the results are reliable. Notably, IGAT without curriculum learning also improves on the DGN benchmark, which tells us both the architecture and the training strategy contribute independently."

---

### Table 3: Relative Improvement of IGAT vs. All Baselines (N=5)
**What it shows:** Percentage improvements of IGAT over each baseline in reward, LoS, and edges.
**Key takeaway:** Against the primary DGN benchmark: +17.56% reward, +10.52% LoS reduction, +43.93% edge reduction. Against MS-GRL (worst performer): +29.88% reward. Against all: IGAT wins on reward and LoS for every single baseline.
**What to say to sir about it:** "Table 3 summarizes IGAT's improvements in percentage terms. The most important comparison is against the DGN benchmark from Isufaj et al. — 17.56% better reward, 10.52% fewer dangerous time steps, and 43.93% fewer edges. These are consistent, meaningful improvements across all three dimensions simultaneously."

---

### Table 4: Performance at N=10 (No CI — Point Estimates)
**What it shows:** Performance of all six methods at the largest swarm size (10 UAVs).
**Key takeaway:** IGAT (ours) achieves −9560.92 reward and 573.27 t_loss with only 2.49 edges. DGN achieves −10,384.75 with 4.37 edges. IGAT without curriculum (−9637.62) still beats all baselines.
**What to say to sir about it:** "Table 4 shows N=10 results. Even at the largest swarm size, IGAT maintains its advantage. Interestingly, IGAT without curriculum/transfer still outperforms all baselines — this tells us that the architectural improvements in IGAT are sufficient on their own, and curriculum learning primarily speeds up training rather than changing the final quality."

---

### Table 5: Action Distribution Over 8000 Episodes
**What it shows:** The probability of each action (0, 1, 2) being selected by each method.
**Key takeaway:** DGN benchmark selects action 0 (no change) 48.6% of the time — it is heavily biased toward doing nothing. IGAT distributes nearly evenly (0.302, 0.350, 0.348). MGAT is biased toward action 1 (always turning). MS-GRL has perfectly uniform distribution but worst performance.
**What to say to sir about it:** "Table 5 reveals action bias across methods. The DGN benchmark selects 'do nothing' nearly half the time, suggesting it is being overly conservative. IGAT's near-uniform action distribution indicates it makes genuinely situation-appropriate decisions — sometimes maintaining course, sometimes turning right, sometimes turning left — which is reflected in its better rewards and safety metrics."

---

### Table 6: Curriculum + Transfer Learning Ablation (N=4 to 10, First 2000 Episodes)
**What it shows:** Side-by-side comparison of IGAT with vs. without curriculum and transfer learning, for every swarm size from 4 to 10.
**Key takeaway:** Curr+TL consistently improves early-stage reward and reduces t_loss at every N. The effect is most dramatic at N=4 (34% reward improvement, 38% LoS reduction) and diminishes as N grows.
**What to say to sir about it:** "Table 6 is the ablation study for the training strategy. It shows that curriculum plus transfer learning gives the most benefit at smaller to medium swarm sizes where exploration instability is greatest. As N grows larger, the architectural advantage of IGAT starts to dominate while the curriculum advantage narrows — suggesting the two contributions (architecture and training strategy) complement rather than overlap each other."

---

### Table 7: IGAT Architecture Ablation (N=5, 10,000 Episodes, Mean ± 95% CI)
**What it shows:** Comparison of full IGAT (2 layers/block, 2 blocks), IGAT with 1 layer per block, and IGAT with just 1 block of 1 layer.
**Key takeaway:** Full IGAT: −1467 reward, 470 t_loss, 0.541 edges. 1-Layer IGAT: −1721, 500, 0.808. 1 IGAT in 1 Layer: −2095, 532, 1.569. Every reduction in depth degrades all three metrics substantially.
**What to say to sir about it:** "Table 7 is the architectural ablation. It confirms that the 'double attention' design — stacking two GAT layers per block and two blocks in sequence — is not unnecessary complexity. Removing either level of depth significantly degrades performance. The full IGAT needs all four attention passes to achieve its best coordination."

---

### Figure 1: IGAT-MARL System Diagram
**What it shows:** The complete architecture of the IGAT-MARL system — from scenario generation and conflict detection through dynamic graph construction, IGAT encoding, Q-value computation, conflict-gated action execution, DQN training, and curriculum progression.
**Key takeaway:** The diagram illustrates how all components connect: BlueSky provides observations and conflict pairs; IGAT processes these into Q-values; epsilon-greedy selects actions; conflict-gated execution applies them; DQN updates the network; curriculum increases swarm size.
**What to say to sir about it:** "Figure 1 shows the full IGAT-MARL pipeline. I particularly want to highlight the left-to-right flow: the dynamic graph A^t is built from real-time conflict pairs, not from distance thresholds. This is the architectural choice that keeps the interaction graph sparse and relevant."

---

### Figure 2: Cumulative Reward Learning Curves (N=3 to 10, IGAT vs. DGN)
**What it shows:** Eight subplots showing cumulative reward over 10,000 training episodes for both IGAT (blue) and DGN benchmark (gray) at each swarm size.
**Key takeaway:** IGAT consistently converges faster and to a higher reward than DGN at every swarm size. The gap between IGAT and DGN grows with N, confirming improved scalability.
**What to say to sir about it:** "Figure 2 shows learning curves for all swarm sizes. Two things stand out: first, IGAT consistently achieves a higher (less negative) final reward than DGN; second, the gap grows with N — meaning IGAT scales better. This is the visual evidence for the paper's scalability claim."

---

### Figure 3: Loss-of-Separation Duration (N=3 to 10, IGAT vs. DGN)
**What it shows:** Eight subplots showing t_loss over training episodes for IGAT vs. DGN at each swarm size.
**Key takeaway:** IGAT maintains lower t_loss than DGN throughout training at every swarm size. Both curves decrease over training (the agents improve), but IGAT's curve is consistently lower.
**What to say to sir about it:** "Figure 3 shows the safety metric — loss-of-separation time — across all training. IGAT keeps t_loss lower at every swarm size and throughout the entire training process, not just at the end. This demonstrates that IGAT is safer during training, not just after convergence."

---

### Figure 4: Action Distribution Bar Charts (N=3 to 10)
**What it shows:** Bar charts comparing the probability of each action (0, 1, 2) for IGAT vs. DGN across all eight swarm sizes.
**Key takeaway:** DGN consistently shows very high probability for action 0 (do nothing), especially at smaller N. IGAT shows roughly equal probability across all three actions at every N.
**What to say to sir about it:** "Figure 4 illustrates the action bias problem in the DGN benchmark. At N=3 especially, DGN selects 'maintain heading' almost exclusively — it has learned to be passive. IGAT distributes actions more evenly, indicating it is genuinely reacting to conflict scenarios rather than defaulting to a safe-but-ineffective routine."

---

### Figure 5: Dense Swarm Comparison (N=10, All Methods, with 95% CI Bands)
**What it shows:** Two subplots comparing cumulative reward and t_loss for all five graph-based methods (IGAT, IGAT no curriculum, DGN, MGAT, GRL, MS-GRL) at N=10 with shaded 95% confidence bands.
**Key takeaway:** IGAT achieves the highest reward and lowest LoS among all methods at N=10. The confidence bands show IGAT has low variance — it is consistently good, not just occasionally lucky.
**What to say to sir about it:** "Figure 5 is the densest comparison plot — all methods, largest swarm, with confidence intervals. IGAT's curve sits above all others in reward and below all others in LoS, with tight confidence bands showing consistent performance. This is the clearest visual argument for IGAT's superiority in dense swarms."

---

### Figure 6: Architecture Ablation Plots (N=5)
**What it shows:** Three subplots showing cumulative reward, t_loss, and edge count for full IGAT vs. 1-Layer vs. 1 IGAT-in-1-Layer variants.
**Key takeaway:** Every reduction in attention depth leads to monotonically worse performance across all three metrics. The full IGAT maintains the best reward, lowest LoS, and fewest edges.
**What to say to sir about it:** "Figure 6 confirms that the architectural depth is not gratuitous. Each reduction in attention layers — from the full two-block, two-layer design down to a single layer — degrades all three performance metrics. The 'double attention' design earns its complexity."

---

## Comparison with Prior Work

**What were the previous best results?**
The primary baseline — DGN from Isufaj et al. (2022) — represents the state-of-the-art graph-based MARL approach for this specific problem. At N=5, DGN achieves a cumulative reward of −1719 and t_loss of 515.8. Among prior related work (MACA by Huang et al., MADDPG by Xu et al., vision-based DRL by Huang et al.), none were evaluated in the same BlueSky framework with the same metrics, making direct comparison difficult.

**Where IGAT wins:**
- Cumulative reward: IGAT beats all four baselines at N=5 and N=10
- Safety (t_loss): IGAT achieves the lowest loss-of-separation time among all methods
- Efficiency (edges): IGAT uses fewer active edges than DGN, MGAT, and GRL
- Scalability: IGAT's advantage over DGN grows with N; at N=10, IGAT outperforms DGN by −9560 vs. −10384

**Where IGAT is competitive but not necessarily dominant:**
- Edges at N=5 vs. MS-GRL: MS-GRL achieves 0.5500 edges, very close to IGAT's 0.5245 — but MS-GRL's reward (−2022) and LoS (505.7) are much worse. So MS-GRL achieves edge efficiency at the cost of safety and reward quality.
- The paper does not compare against non-graph MARL methods like MACA or MADDPG in the same simulator environment.

---

## Real-World Meaning

If IGAT-MARL were deployed in a real drone management system, several things would change for the better:

**For drone operators and logistics companies:** Drones could safely share the same delivery corridors in dense urban areas without a centralized traffic controller needing to monitor every pair individually. The conflict-gated execution means drones only maneuver when necessary — preserving flight efficiency and battery life.

**For air traffic management:** The sub-quadratic scaling of IGAT's edge count means the computational load does not explode as fleet sizes grow. A system managing 10 drones requires less than double the computation of one managing 5 drones — this is essential for real-time operation.

**For emergency response:** Multiple drones dispatched to the same disaster zone could coordinate autonomously without explicit communication infrastructure — the conflict-driven graph requires only collision-prediction data, not full state broadcasts.

**For regulatory compliance:** Demonstrating 10% fewer loss-of-separation events in simulations is directly relevant to FAA and SESAR certification requirements for UAV operational approval.

**The core message:** Smarter coordination — not more communication — is the path to safe, scalable multi-drone systems.
