# 05 — Critical Analysis: Strengths, Weaknesses, and Open Questions

---

## Genuine Strengths

**1. The dynamic reward function is the paper's most valuable idea.**
The d3/(d1+d2) reward is genuinely clever. Unlike most DQN papers that use simple "+1 for goal, −1 for obstacle, 0 otherwise" (sparse reward), this function provides informative feedback at *every single step*. It encodes both the direction of travel (are you getting closer?) and the efficiency of that step (are you making a big step vs. a small shuffle?). The formula is also intuitive — it's mathematically grounded and easy to explain. This is publishable as a standalone contribution.

**2. The paper rigorously tests across 4 progressively harder scenarios.**
The decision to run 20 independent executions per algorithm per scenario, report Best/Mean/Worst/STD, and use 4 difficulty levels is genuinely thorough for a conference paper. Many comparable papers only show one scenario or one run. The graduated difficulty design reveals exactly where each algorithm breaks — a clean, honest experimental setup.

**3. The practical argument about computational time is valid and important.**
Many papers ignore the training time tradeoff. This paper addresses it directly: yes, DQN takes longer (455 seconds vs. GWO's 29 seconds), but they correctly argue that offline pre-mission planning makes this acceptable when the alternative is a 75% failure rate. This is a mature, pragmatic engineering argument.

**4. Strong performance gap in large-scale scenarios.**
The jump from DQN (85% SR) to the next best (Q-learning, 70%) and then to metaheuristics (20–25%) in Scenario 4 is decisive. This isn't marginal improvement — it's the difference between a usable system and a broken one. The paper earns its claim of superiority in large-scale environments.

**5. The dual Q-network design is correctly motivated.**
The separation of evaluation and target networks is well-justified: it prevents the training instability that would occur if a single network chased its own moving targets. The paper explains this clearly and it's a direct application of the proven DQN stability technique from Mnih et al. (2015), properly adapted for UAV path planning.

---

## Honest Limitations

**Limitations the authors admit themselves:**
- High computational time compared to metaheuristics — explicitly acknowledged
- Future work needed for parallelizing DQN training to reduce this cost
- Paper suggests extending to multi-agent systems, implying the current work handles only one drone

**Weaknesses the authors did NOT mention:**

**1. Obstacles are all static — no moving obstacles.**
All four scenarios use *static* obstacles. Real environments have moving obstacles: other aircraft, birds, humans, vehicles. The paper's MDP formulation (not POMDP) assumes full observability of a fixed environment. In a dynamic environment where obstacles move, the learned policy may fail catastrophically because it was trained on static layouts only.

**2. Single drone only — no multi-UAV coordination.**
The previous paper (Kong et al.) handled 5 UAVs simultaneously. This paper handles only one drone. There is no collision avoidance between UAVs, no target assignment, no coordination. The authors acknowledge this in future work, but it is a significant limitation for practical swarm applications.

**3. This is a very short conference paper (11 pages).**
Published at KES 2025 in Procedia Computer Science — a lower-impact venue compared to top journals like IEEE Transactions or Frontiers. The paper lacks depth in several areas: no ablation study on the reward function, no analysis of why the SLR *improves* from Scenario 2 to Scenario 3 (which is counterintuitive), and no discussion of how the grid cell size affects results.

**4. No ablation study on the reward function.**
The central claim is that the dynamic reward function is the key innovation. Yet the paper never tests a DQN with a standard sparse reward to isolate the contribution of the dynamic reward alone. Without this ablation, we don't know how much of the improvement comes from the reward design vs. the 3D CNN architecture vs. the input normalization.

**5. Q-learning comparison may be unfair.**
Q-learning with a state space explosion problem (millions of states) is expected to fail in Scenario 4. Comparing against a basic Q-learning implementation (not a state-of-the-art DRL baseline like DDPG, PPO, or A3C) understates the difficulty of the comparison. Including modern DRL baselines would make the contribution more convincing.

**6. No real hardware validation.**
Like the previous paper, all experiments are simulation-only. Sim-to-real transfer concerns apply: real UAVs have sensor noise, GPS errors, wind disturbance, and motor dynamics not captured in a discrete grid simulation.

**7. Grid discretization may be too coarse or too fine.**
The paper never specifies the actual grid cell size in absolute terms (it says "equal to R_uav" but never gives R_uav a value in the experiments). The choice of grid resolution fundamentally affects the state space size, path smoothness, and computational cost — yet this is not analyzed.

---

## Missing Experiments

- **Ablation on reward function:** Compare dynamic reward DQN vs. sparse reward DQN to isolate the reward's contribution
- **Comparison with state-of-the-art DRL baselines:** DDPG, PPO, or SAC would be more appropriate RL baselines than basic Q-learning
- **Varying obstacle density:** The paper uses fixed obstacle counts per scenario — testing the same environment size with different obstacle densities would be informative
- **Moving obstacle scenarios:** At least one scenario with dynamic obstacles would demonstrate real-world applicability
- **Training convergence analysis:** No learning curves or convergence plots are shown — we don't know how many episodes are actually needed or whether 2,000 is sufficient
- **Sensitivity to γ and ε:** Different hyperparameter choices might significantly affect results; no sensitivity analysis is provided

---

## Open Questions

1. **Why does SLR improve from Scenario 2 to Scenario 3 for DQN?** In Scenario 3 (24 obstacles), DQN's SLR is 1.1713 — better than Scenario 2's 1.3651. More obstacles should make paths longer, not straighter. The paper doesn't explain this counterintuitive result.

2. **How sensitive is the performance to the reward formula parameters?** The d3/(d1+d2) formula has specific mathematical properties. Would a variant like (d3−d2)/d1 perform differently? This is unexplored.

3. **What happens when the number of obstacles is so large that no path exists?** The paper doesn't discuss dead-end detection or how the algorithm behaves in unsolvable configurations.

4. **Does the trained model generalize across grid sizes?** A policy trained on the specific grid layouts in training might fail on a new environment with differently placed obstacles. Transfer learning across environments isn't discussed.

5. **How does the buffer size of 2,000 affect learning?** The buffer fills up quickly and old experiences are discarded — in a large environment, important early exploration experiences might be overwritten before being fully learned from.

---

## Your Overall Assessment

> "Overall, I think this paper makes a meaningful contribution because its dynamic reward function — d3 divided by (d1 plus d2) — is a genuinely well-motivated design that solves the sparse reward problem in large-scale environments, and the experimental results convincingly demonstrate DQN's superiority in success rate and path quality over both metaheuristics and Q-learning in scenarios with up to 40 obstacles. However, one clear limitation I noticed is the absence of an ablation study — we never see a DQN with a standard sparse reward tested against the same scenarios, so it's impossible to isolate how much of the improvement comes specifically from the dynamic reward versus the 3D CNN architecture or input normalization. A strong direction for future work would be to test this approach in environments with dynamic obstacles and compare against modern DRL baselines like PPO or DDPG, which would be more appropriate comparisons than basic Q-learning."
