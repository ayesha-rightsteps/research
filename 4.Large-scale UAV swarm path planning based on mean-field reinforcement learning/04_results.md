# 04 — Results: What They Found and Why It Matters

---

## Key Results

**Result 1: PO-WMFDDPG achieves ~98% task success rate with 80 UAVs** ⭐

With the primary experimental setup (80 UAVs, 20 NFZs, 500×500m battlefield), PO-WMFDDPG converges to approximately 98% task success rate after around 700 training rounds. The competing algorithms (DDPG and MFDDPG) converge to meaningfully lower success rates and show more instability (noisier reward curves) during training.

*What this means in plain language:* In a mission with 80 drones, roughly 78 out of 80 will reach their targets without entering a no-fly zone or colliding. This is operationally meaningful — a loss rate of only 2 drones out of 80 is acceptable for most military or surveillance applications.

*Why it's impressive:* At 80 agents, standard MARL methods fail to coordinate at all. The fact that PO-WMFDDPG achieves 98% is remarkable and directly demonstrates the effectiveness of the mean-field + attention approach.

---

**Result 2: Scalability to 120 UAVs while competitors collapse**

The scalability experiment gradually increases the swarm size from 20 to 120 drones:

| Drone Count | PO-WMFDDPG SR | MFDDPG SR | DDPG SR |
|-------------|---------------|-----------|---------|
| 20 | ~98% | ~97% | ~96% |
| 40 | ~98% | ~96% | ~95% |
| 60 | ~98% | ~95% | ~92% |
| 80 | ~98% | ~93% | ~88% |
| 100 | ~95% | ~88% | ~75% |
| 120 | ~91% | ~82% | ~65% |

*(Note: Exact values from the paper's figure — these represent the approximate trends shown in Figure results. The key point is the relative ordering and that PO-WMFDDPG maintains >90% throughout.)*

*What this means:* PO-WMFDDPG is the only algorithm that maintains above 90% success all the way to 120 drones. DDPG drops sharply at 100+ because it cannot model the dense interaction between 100 agents without a mean-field approximation. MFDDPG drops more gradually because it uses mean field, but without attention weighting it treats all neighbors equally — the wrong neighbors contaminate the signal.

*Why it's impressive:* The paper's stated goal was to handle 80 drones. Maintaining >90% at 120 shows the algorithm scales well beyond its design target.

---

**Result 3: NFZ robustness — stable to 36 no-fly zones, DDPG collapses at 26**

The NFZ density experiment increases the number of no-fly zones:

| NFZ Count | PO-WMFDDPG SR | MFDDPG SR | DDPG SR |
|-----------|---------------|-----------|---------|
| 10 | ~98% | ~96% | ~95% |
| 20 | ~98% | ~94% | ~90% |
| 26 | ~97% | ~90% | ~82% |
| 30 | ~95% | ~85% | ~72% |
| 36 | ~92% | ~79% | ~62% |
| 40+ | declining | declining | collapsed |

*(Approximate values from the paper's trend figures)*

*What this means:* The battlefield scenario the paper targets has 20 NFZs — at this level, all three algorithms perform well, but PO-WMFDDPG has the highest margin. As NFZ count increases to 36 (nearly double the training density), PO-WMFDDPG is still at ~92% while DDPG has already declined significantly. This shows the algorithm is robust to environments that are harder than what it was trained on.

*Why it's impressive:* Real combat environments don't have fixed threat densities. An algorithm that gracefully degrades (rather than suddenly collapsing) when encountering more obstacles than expected is far more practically useful.

---

**Result 4: Moving NFZ test — 75/80 UAVs succeed (93.75%)**

When the 20 no-fly zones are made dynamic (moving at random velocities), 75 of the 80 UAVs still complete their missions. The 5 failures occur because those drones encounter a moving NFZ at close range and cannot evade in time.

*What this means:* The algorithm was NOT trained on moving NFZs — it was trained only with static ones. Yet it still achieves 93.75% success when tested on a harder problem. This suggests the learned policy generalizes somewhat to dynamic obstacles.

*Why it's notable:* This is an unexpected positive result. The paper mentions it as preliminary evidence that the approach has some robustness to dynamic environments, while appropriately noting it as a limitation and direction for future work.

---

**Result 5: PO-WMFDDPG converges faster and more stably than baselines**

The convergence curves (success rate vs. training round) show:
- PO-WMFDDPG reaches ~98% by round 700 and stays there
- MFDDPG converges more slowly and to a lower value (~90-93% final)
- DDPG shows the most instability and reaches the lowest final value (~85-88%)

*What this means:* The attention mechanism and partial observability don't just improve final performance — they also make training more stable. When the mean field is computed from only relevant nearby neighbors (rather than all agents globally), the gradient signal is cleaner and the policy updates are more focused.

---

**Result 6: Visualization confirms coordinated flight — no collisions in demonstrated trajectories**

The paper includes trajectory visualization figures showing all 80 UAVs' flight paths from start positions to targets. The paths are smooth, avoid all 20 NFZs, and the drones do not collide. This visual confirmation supports the quantitative success rate numbers.

*What this means:* The algorithm doesn't just achieve high success rates statistically — the actual flight behaviors look like coherent, coordinated swarm movement, which is what would be required in a real deployment.

---

## Figures Explained

### Figure: Training Convergence Curves
**What it shows:** Task success rate (y-axis) plotted over 1,000 training rounds (x-axis) for all three algorithms (PO-WMFDDPG, MFDDPG, DDPG).

**Key takeaway:** PO-WMFDDPG rises fastest and plateaus highest (~98%). MFDDPG rises more slowly to a lower plateau. DDPG is the slowest and noisiest, reaching the lowest final performance.

**What to say to sir:** "This figure shows that PO-WMFDDPG not only achieves the best final performance but also converges approximately 100-150 rounds earlier than the baselines, suggesting the attention-weighted mean field provides cleaner, more informative learning signals during training."

---

### Figure: UAV Scalability
**What it shows:** Task success rate (y-axis) as drone count increases from 20 to 120 (x-axis).

**Key takeaway:** All three algorithms start at similar high values at low drone counts. As count increases, DDPG declines fastest, MFDDPG declines moderately, PO-WMFDDPG maintains above 90% throughout.

**What to say to sir:** "This is the paper's most important result figure. It shows that DDPG's performance degrades sharply once the drone density exceeds what it can handle without any interaction modeling. MFDDPG handles more drones because it uses mean field, but degrades because it ignores distance when averaging neighbors. PO-WMFDDPG's attention mechanism correctly down-weights irrelevant distant neighbors, maintaining performance even at 120 drones."

---

### Figure: NFZ Scalability
**What it shows:** Task success rate as no-fly zone count increases.

**Key takeaway:** DDPG collapses first. MFDDPG degrades next. PO-WMFDDPG is the most robust to increasing obstacle density.

**What to say to sir:** "This figure demonstrates environmental robustness — not just agent scalability. Even when the obstacle density is nearly double the training configuration, PO-WMFDDPG is still above 90%, while DDPG has already dropped substantially. This suggests the attention mechanism helps drones identify and respond to nearby threats even when there are many more of them."

---

### Figure: Trajectory Visualization
**What it shows:** 2D top-down map of the 500×500m environment with 80 UAV paths drawn from start to target, overlaid on 20 NFZ circles.

**Key takeaway:** All paths successfully navigate around NFZs and reach their targets. Paths are smooth and do not intersect NFZ boundaries or each other.

**What to say to sir:** "This visualization is the qualitative confirmation of the quantitative results. You can see the paths curve around no-fly zones and spread out to avoid each other, showing genuine emergent coordination rather than a pre-programmed formation."

---

## Comparison with Prior Work

**Against standard DDPG:**
- DDPG for multi-agent: treats agents independently — no interaction modeling
- PO-WMFDDPG advantage: ~10-13% higher SR at 80 drones, widening to ~33% at 120 drones
- Why: DDPG cannot scale because it has no mechanism to approximate the N-agent joint action space

**Against MFDDPG:**
- MFDDPG: uses global mean field, equally weights all N agents (including distant irrelevant ones)
- PO-WMFDDPG advantage: ~5-9% higher SR at 80 drones, maintained through 120 drones
- Why: Equal weighting includes irrelevant far-away agents, diluting the useful local neighborhood signal

**Against prior mean-field RL work (Yang et al., 2018 — the foundational MFQ paper):**
- Yang et al.'s MFQ: discrete action spaces only, relatively small-scale demonstrations
- PO-WMFDDPG: extends to continuous actions (DDPG base), works at 80-120 agents, adds partial observability and attention

**Against metaheuristic approaches:**
- Not directly benchmarked in this paper (different focus from Papers 2 and 3)
- But in principle: PSO/GWO cannot model dynamic agent interactions in a 500×500m real-time continuous-space problem

---

## Real-World Meaning

**If this were deployed in a real mission:**

A military operation planning to deploy 80 attack or reconnaissance drones simultaneously could use this algorithm to autonomously assign flight paths to all drones, with each drone navigating its own path while automatically avoiding designated no-fly zones (enemy radar coverage areas, civilian zones) and not colliding with other drones. No human operator would need to individually plan 80 paths.

The partial observability design makes this realistic — each drone only needs to communicate with nearby drones, not broadcast to all 79 others. With a sufficient communication range R_a, the swarm self-coordinates without any central command node.

The scalability to 120 drones means the same algorithm could be used for larger operations without retraining. The NFZ robustness means unexpected threats (a newly activated radar system) can be accommodated dynamically.

The paper was directly inspired by the Russo-Ukrainian conflict, which demonstrated that cheap UAV swarms (100+ drones) have become decisive battlefield tools — this algorithm is a step toward making such swarms fully autonomous.
