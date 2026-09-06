# 04 — Open Questions for the Supervisor

Send this list to Dr. Faisal Rehman (and Mr. Ehzaz Mustafa) **before P0 sign-off**.
Get the answers in writing (email is fine) so there are no surprises at the defense.

Group A is the most urgent (they block coding). Group B (PAH) is the most important for
the research contribution.

---

## A. Deviations from the approved synopsis — need written OK

**Q1. Simulator: PyBullet → custom 2D Gymnasium environment.**
The synopsis says "experiments will be conducted on PyBullet simulation". PyBullet is a
3D rigid-body physics engine; the research is 2D and the question (learned vs fixed α)
does not depend on flight-dynamics fidelity. We propose a lightweight custom 2D
point-mass environment following the Gymnasium API (this is also what DA-MAPPO
effectively does — Gazebo at fixed altitude → 2D). *Is this acceptable, and can we get
it in writing?*

**Q2. Action space: `(vx, vy)` velocity command instead of `(forward speed, yaw rate)`.**
A point-mass model has no heading state, so a 2D velocity command is the natural action.
DA-MAPPO used `(v, ω)` because it modelled a turning vehicle. *Acceptable?*

**Q3. Obstacle sensing: 4 cardinal clearance readings instead of a LiDAR scan.**
DA-MAPPO used a 35-beam LiDAR. For sparse circular obstacles in 2D, 4 directional
clearance values are enough and keep the observation small. *Acceptable, or does the
committee expect a LiDAR-style sensor model?*

---

## B. Priority Arbitration Head — the core research design

Full analysis in `01_pah_design.md`. Summary of the issue: `α` scales the reward the
agent optimizes, and `α` is produced by the agent's own network — so the agent can
raise its return by choosing `α` to up-weight whichever reward term is momentarily
easier, without actually behaving better ("reward hacking"). This could make the
learned α collapse to a constant, which would make PAH equivalent to fixed-α and
undermine the thesis.

**Q4. Where is α applied?**
- Option A (synopsis, literal): α weights the **scalar reward**
  `r = α·r_mission + (1−α)·r_safety`, PAH trained by the same policy-gradient update.
- Option B (our recommended primary): keep **two value heads** and α weights the two
  **advantages** in the actor loss, `α·A_mission + (1−α)·A_safety`. This removes the
  reward-hacking shortcut.
*Which does the supervisor want as the main method?* We propose: build A first (matches
synopsis), switch to B only if A shows reward hacking.

**Q5. The synopsis says PAH "adds no parameters to the centralized critic".** Option B
needs a **second critic output head** (small). *Is a one-line synopsis amendment to
allow this acceptable if A turns out to be unstable?*

**Q6. Regularizing α.** We plan a mild prior pulling α toward 0.5 (and/or clipping α to
`[0.1, 0.9]` so neither objective is ever fully ignored). *Does this conflict with the
committee's expectation of a "purely learned" weight, or is it a reasonable
stability measure?*

---

## C. Target assignment

**Q7. Assignment frequency.** We plan per-step Hungarian (matches DA-MAPPO). If
assignment *thrashing* appears (drone oscillating between near-equidistant targets), we
would add a switching-cost term or move to event-triggered reassignment (DA-MAPPO's
ablation shows every-50-steps costs only 3–5%). *Acceptable as a fallback?*

**Q8. Cost metric.** Squared Euclidean distance (DA-MAPPO) vs plain distance — any
preference?

---

## D. Conflict graph

**Q9. Look-ahead horizon `H` and danger threshold `d_danger`.** We propose `H ≈ 3 s`
and `d_danger ≈ 3·d_col`, to be calibrated. *Any domain guidance on realistic values,
or is calibration-by-experiment fine?*

---

## E. Evaluation

**Q10. Number of seeds.** We propose ≥ 5 training seeds per configuration (10 for the
headline PAH-vs-fixed-α comparison), reporting mean ± 95% CI. *Is this the standard the
committee expects, or do they want more/fewer?*

**Q11. Stage-1 success criterion.** Because our environment differs from DA-MAPPO's, we
cannot target their exact numbers (90–99%). We propose a **qualitative** replication
criterion: (a) assignment-augmented obs clearly beats no-augmentation, and (b) removing
the augmentation collapses success toward zero (matching DA-MAPPO's Table VI ablation).
*Is that an acceptable definition of "DA-MAPPO replication baseline" for Task-I?*

**Q12. The IGAT-style baseline.** IGAT-MARL is a discrete-action DQN with a graph-
attention network. To keep all baselines on the same MAPPO backbone for a fair α
comparison, our "IGAT-style" baseline is **MAPPO with conflict-graph neighbor
features** (no real-time assignment) — i.e. we port the *idea*, not the algorithm.
*Is that acceptable, or does the committee want a faithful IGAT (DQN) reproduction as a
separate baseline?*

---

## F. Scope

**Q13. Moving-target model.** DA-MAPPO's dynamic targets **swap positions** discretely.
Alternative: targets **drift** continuously. Swap is easier and matches DA-MAPPO;
drift is arguably more realistic but interacts badly with per-step assignment
(thrashing). *Preference?*

**Q14. Confirm the curriculum and limits.** 4 stages: (1) 3 drones static, (2) 5 drones
+ moving targets + few obstacles, (3) 8 drones + dynamic + dense, (4) unseen swarm
sizes. Max 8 drones in training. *Confirmed as-is?*

---

## Timeline note to raise

The synopsis Gantt puts "2D env + DA-MAPPO replication" in months 1–2. Realistically:
env with tests ≈ 3–5 weeks, minimal MAPPO ≈ 3–4 weeks, getting Stage 1 to converge ≈
2–4 weeks of debugging. We expect **env + MAPPO running by end of month 2**, full
Stage-1 replication in **month 3**. Flagging now so it is not a surprise later.
