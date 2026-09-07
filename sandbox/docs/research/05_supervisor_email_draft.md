# Email to Supervisor — P0 Sign-off Request

> **Bhejne se pehle:** `[PLACEHOLDER]` wali jagahein fill karo.
> Email Sir aur Mr. Ehzaz dono ko bhejna hai (CC field mein ek ka naam daalo).

---

**To:** `[Dr. Faisal Rehman ka email]`
**CC:** `[Mr. Ehzaz Mustafa ka email]`
**Subject:** MS Synopsis Implementation — Clarifications Required Before Coding Phase (CIIT/SP25-RCS-009/ATD)

---

Respected Sir,

I hope this email finds you well.

My synopsis for "Multi-Agent Proximal Policy Optimization for Joint Dynamic Target Assignment and Collision Avoidance in UAV Systems" has been approved and I am now beginning the implementation phase.

Before writing any code, I want to seek your written guidance on a few design decisions. Some of these are minor deviations from the approved synopsis (with justification), and one concerns the core research contribution (the Priority Arbitration Head). I want to make sure everything is aligned with the committee's expectations before I proceed.

I have grouped the questions below for ease of review.

---

## Group A — Deviations from the Approved Synopsis

**Q1. Simulator: PyBullet → Custom 2D Gymnasium Environment**
The synopsis mentions PyBullet simulation. However, PyBullet is a 3D rigid-body physics engine, and my research is in 2D. Using it would add significant complexity without contributing to the research question. I propose building a lightweight custom 2D environment using the standard Gymnasium API — this is consistent with how DA-MAPPO is effectively implemented (Gazebo at fixed altitude, reduced to 2D).
*Request: Written approval for this deviation.*

**Q2. Action Space: `(vx, vy)` velocity command**
The synopsis implies a `(forward speed, yaw rate)` action space following DA-MAPPO's vehicle model. Since our environment uses a point-mass model (no heading state), a direct 2D velocity command `(vx, vy)` is the natural and simpler choice.
*Request: Is this acceptable?*

**Q3. Obstacle Sensing: 4 Cardinal Clearance Readings**
DA-MAPPO used a 35-beam LiDAR scan. For sparse circular obstacles in 2D, four directional clearance values (North, South, East, West) are sufficient and keep the observation vector small and interpretable.
*Request: Is this acceptable, or does the committee expect a LiDAR-style sensor model?*

---

## Group B — Priority Arbitration Head (Core Research Design)

This is the most important group. The PAH produces a dynamic weight `α ∈ [0,1]` that balances the mission reward and the safety reward at each step. A potential issue is that because `α` is produced by the agent's own network, the agent could exploit it to inflate its reward without actually behaving better — this is known as reward hacking. I want your guidance before committing to a formulation.

**Q4. Where should `α` be applied?**
- **Option A** *(synopsis, literal)*: `α` weights the scalar reward — `r = α·r_mission + (1−α)·r_safety`. PAH is trained by the same policy-gradient update as the actor. Risk: reward hacking is possible.
- **Option B** *(our recommended fallback)*: Maintain two value heads; `α` weights the two advantages in the actor loss — `α·A_mission + (1−α)·A_safety`. This removes the reward-hacking incentive but requires a small amendment to the critic.

*My plan: Begin with Option A (matches the synopsis). If reward hacking is observed during training, switch to Option B. Is this approach acceptable?*

**Q5. Second Critic Head (Option B only)**
The approved synopsis states that PAH "adds no parameters to the centralized critic." Option B would require a second output head on the critic (a small addition). *If Option A proves unstable, may I make this amendment without a formal synopsis revision?*

**Q6. Regularizing `α`**
I plan to clip `α` to the range `[0.1, 0.9]` so that neither objective is ever fully ignored during training. I may also add a mild prior pulling `α` toward 0.5 for stability.
*Is this a reasonable engineering measure, or does the committee expect `α` to be fully unconstrained?*

---

## Group C — Target Assignment

**Q7. Anti-Thrashing Fallback**
I plan to use per-step Hungarian assignment (matching DA-MAPPO). If assignment thrashing appears (drones oscillating between near-equidistant targets), I propose adding a switching-cost term or moving to event-triggered reassignment.
*Is this fallback acceptable if needed?*

**Q8. Cost Metric for Hungarian Assignment**
DA-MAPPO uses squared Euclidean distance. Plain Euclidean distance is also common.
*Do you have a preference, or shall I decide based on training behaviour?*

---

## Group D — Conflict Graph

**Q9. Look-Ahead Horizon and Danger Threshold**
I propose `H ≈ 3 seconds` look-ahead and `d_danger ≈ 3 × d_collision` as initial values, to be calibrated through experiments.
*Do you have domain-specific guidance, or is calibration by experiment appropriate?*

---

## Group E — Evaluation

**Q10. Number of Training Seeds**
I propose running each configuration with at least 5 independent random seeds (10 seeds for the headline PAH vs. fixed-α comparison), reporting mean ± 95% confidence interval.
*Is this the standard the committee expects?*

**Q11. Stage-1 Success Criterion**
DA-MAPPO reports 90–99% mission success. Because our environment will differ in implementation details, I do not expect to match their exact numbers. I propose a qualitative criterion: (a) assignment-augmented observations clearly outperform no augmentation, and (b) removing the augmentation collapses success toward zero — matching DA-MAPPO's Table VI ablation finding.
*Is this an acceptable definition of "DA-MAPPO replication baseline" for Task-I?*

**Q12. IGAT-Style Baseline**
IGAT-MARL uses a discrete-action DQN with a graph-attention network. To enable a fair comparison across all baselines, I propose porting the IGAT *idea* (conflict-graph neighbour features) onto the MAPPO backbone rather than reproducing the original DQN architecture.
*Is this acceptable, or does the committee require a faithful IGAT-DQN reproduction as a separate baseline?*

---

## Group F — Scope Confirmation

**Q13. Moving-Target Model**
DA-MAPPO's dynamic targets swap positions discretely. An alternative is continuous drift. I lean toward the discrete swap (matches DA-MAPPO, avoids thrashing), but I want your preference.
*Discrete position swap or continuous drift?*

**Q14. Curriculum and Scale Confirmation**
Please confirm the following is approved as-is:
- Stage 1: 3 drones, static targets, no obstacles
- Stage 2: 5 drones, moving targets, few obstacles
- Stage 3: 8 drones, dynamic targets, high obstacle density
- Stage 4: Unseen swarm sizes (generalization test)
- Maximum 8 drones in training

---

## Timeline Note

The approved Gantt places "2D env + DA-MAPPO replication" in months 1–2. Realistically, building and testing the environment will take 3–5 weeks, implementing MAPPO will take 3–4 weeks, and getting Stage-1 to converge will take 2–4 weeks of debugging. I expect the environment and MAPPO to be running by end of month 2, with full Stage-1 replication completed in month 3. I am flagging this now so it is not a surprise later.

---

I would greatly appreciate written responses to the above — even brief ones — so that I have a clear record going into the implementation. I am happy to meet in person or on a call if any of these require discussion.

Thank you for your time and continued guidance.

Warm regards,
Ayesha Khalil
CIIT/SP25-RCS-009/ATD
MS (CS) — Artificial Intelligence
COMSATS University Islamabad, Abbottabad Campus
