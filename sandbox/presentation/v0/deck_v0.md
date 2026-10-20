# Presentation deck — v0 (markdown draft, not a PPT yet)

**Thesis:** Multi-Agent Proximal Policy Optimization for Joint Dynamic Target Assignment and Collision Avoidance in UAV Systems
**Student:** Ayesha Khalil (CIIT/SP25-RCS-009/ATD) · **Supervisor:** Dr. Faisal Rehman · **Co-supervisor:** Mr. Ehzaz Mustafa
**Draft by:** Manish's Claude, 2026-10-20, from everything in the repo up to commit `1ea5a21` (sessions 2026-10-12 to 2026-10-17).

## How to use this file

- One `## Slide N` block = one PPT slide. **On slide** = what goes on the slide (short). **Say** = speaker notes in English (not on the slide). **Image** = file in `images/` (copied from the repo, so the deck folder is self-contained).
- Slide text is English (panel-facing). Method names are always the **full names** (no B4/H/M nicknames).
- Target length: **22 main slides ≈ 25–30 minutes**, then the appendix is only for questions.
- Every number comes from the repo: `v4/03-base-paper-baselines/REPORT.md`, `v4/04-base-paper-experiments/REPORT.md`, `docs/research/11_thesis_reporting_notes.md`, `docs/research/12_supervisor_progress_v4.html`. Source of each figure is in the table at the end.
- **PPT rules for v1 (when we build the real deck):** one idea per slide, max ~25 words of body text, the figure is the slide. Same colour = same method on every slide (blue = MAPPO + PAH, grey = base-paper methods, light blue = our other methods; this is already how the figures are drawn).

## Storyline in one breath

1. Assignment and collision avoidance are solved separately in the literature → conflicts.
2. We propose one MAPPO framework with a Priority Arbitration Head (PAH) that learns the mission-vs-safety weight α.
3. First version (v3) tied with a fixed weight; **diagnostics told us why**, so we redesigned the environment and the learning rule (v4).
4. Under the same environment, budget and seeds, **MAPPO + PAH is first of 9 methods at both stages**, above every base-paper method.
5. PAH's own gain over a fixed weight is **+8.6 points (95% CI +1.7 to +15.4)** at 8 drones — proven, but modest; the rest of the gap comes from the conflict graph and the two value heads, and we say so.
6. The same base-paper experiments (density, swarm size, static targets, noise…) re-run on the trained models: the lead holds in **31 of 31 settings**.

---

## Slide 1 — Title

**On slide:** thesis title · Ayesha Khalil · supervisors · date · COMSATS University Islamabad, Abbottabad.

**Say:** Good morning. Today I will present the progress and results of my thesis: one MAPPO framework for target assignment and collision avoidance together, and its new component, PAH.

---

## Slide 2 — The problem

**On slide:**
- Multi-UAV missions need two decisions at once: **who goes to which target** (assignment) and **how to avoid collisions** (obstacles + other drones).
- In the literature they are solved **separately** → assignments that ignore danger, avoidance that ignores the mission.
- Result: conflicts, slow or incomplete missions.

**Say:** When the two tasks are solved separately, a drone can pick the right target and still crash into an obstacle or another drone on the way. Our question: can one policy do both?

---

## Slide 3 — Idea and contribution

**On slide:**
- One **unified MAPPO** framework: assignment (Hungarian algorithm) + conflict graph + learning.
- **PAH — Priority Arbitration Head:** a small network that learns, from the situation, how much to weight *mission* vs *safety*: α ∈ [0.1, 0.9].
- Reward the agent learns from: `α · mission + (1 − α) · safety`.
- Existing work uses a **fixed** α (e.g. 0.5). Our claim: a situation-dependent α is better.

**Say:** With a fixed weight, a drone weighs mission and safety equally whether danger is near or far. PAH puts more weight on safety near danger and more on the mission when it is far. That is the novel part of this work.

---

## Slide 4 — System overview (draw this one)

**On slide (diagram to draw in PPT):** five blocks left → right:
1. 2D multi-UAV environment (drones, moving targets, obstacle discs, 24-ray LiDAR)
2. Hungarian assignment (every step) → **assigned target**
3. Conflict graph (DCPA/TCPA) → nearby conflicting drones
4. MAPPO (shared actor, centralised critic with **separate mission and safety value heads**)
5. **PAH** → α → mixes the mission and safety advantages

**Say:** Each drone takes its observation and the actor chooses an action. Assignment and conflict-graph information enter through the observation. PAH works only during training: α mixes the advantages. So the actor's decision time is the same as Fixed-weight MAPPO's (slide 21).

---

## Slide 5 — PAH in one picture

**On slide:**
- Inputs (as in the synopsis): **τ** (time to the nearest collision, drone *or* obstacle, capped at 3 steps), **d_target**, **n_conflict**.
- Network: 3 → 32 → 1. Output: predicted **risk p**; **α = 0.9 − 0.8 · p**.
- PAH learns the risk by regression on the safety cost that actually followed — from experience, not a formula.
- No gradient reaches PAH from the actor loss (explained on slide 9).

**Say:** In plain words: PAH looks at the situation and estimates how large the next safety cost will be. The higher the risk, the lower α, which means more weight on safety.

---

## Slide 6 — What the base papers did, and what we take from them

**On slide (table):**

| | DA-MAPPO (Internet of Things J.) | IGAT-MARL | **Ours** |
|---|---|---|---|
| Problem | Assignment + navigation | Collision avoidance only (no targets) | Assignment + collision avoidance + PAH |
| Algorithm | MAPPO | DQN + graph attention | MAPPO + PAH |
| Drones / obstacles | 3 drones, 30–50 cylinders (3D Gazebo) | 3–10 aircraft (BlueSky) | 5 and 8 drones, 10 and 20 discs (2D) |
| Metrics | success, collision, timeout, T_ave, L_ave | reward, loss of separation, edges | the same as DA-MAPPO + loss of separation, edges |
| What we reuse | Hungarian assignment, success definition, Table V comparison | conflict graph, scalability 3→10, metrics | |

**Say:** Our supervisor's principle is that we should do what the base papers did. So we trained their methods in our own environment (slide 11) and repeated their experiments on our trained models (slides 17–21). We do not copy their numbers, because their environment is different (3D, 3 drones).

---

## Slide 7 — Version 3: what happened and what the diagnostics showed

**On slide:**
- v3 (5 and 8 drones, point obstacles): the three α methods **tied** — 89.2 / 87.5 / 89.5 % at Stage 2 (Fixed-weight MAPPO / Hand-coded τ-rule MAPPO / MAPPO + PAH, 5 seeds).
- Removing the optimal assignment cost **20.5 points** at 8 drones (v3, one seed) — the biggest effect we saw.
- Diagnostics on the trained v3 models (no new training):
  1. **94–100 % of collisions are with obstacles**, not other drones.
  2. PAH's τ came only from drone–drone conflicts → **it could not see obstacles**.
  3. Removing the mixing entirely (Plain MAPPO, 89.9 %) did **not** hurt → the α mixing had no measurable effect.

**Image:** `images/s07_v3_collision_type.png` (v3 models: what did the drones hit?)

**Say:** This is the honest outcome of our first attempt: PAH did not fail, the environment gave it no chance. The collisions were with obstacles, and PAH could not see obstacles. This diagnosis is what led to the redesign.

---

## Slide 8 — Redesign (v4): four changes + one bug

**On slide:**
1. **Separate mission and safety value heads** (the safety advantage becomes a real safety signal).
2. **Obstacle danger in PAH's τ** (τ = nearest drone *or* obstacle; PAH's three inputs unchanged).
3. **24-ray LiDAR** instead of four axis distances.
4. **Sized obstacle discs** (radius 12): 10 at Stage 2, 20 at Stage 3.
- Found and fixed an environment bug (targets bounced into obstacles). A hand-written LiDAR rule then reached 82 % with zero obstacle collisions → the task is solvable.
- Reward shaping (danger zone 20, collision −10) and density were tuned **once, on Plain MAPPO only, on separate seeds, then frozen for every method**.
- The supervisor approved the redesign (*per Ayesha; there is no written record in the repo — confirm before saying it on stage*).

**Say:** When we found the bug we stopped tuning and first wrote a hand-made rule to check that the task is solvable. Tuning was done on one baseline only, so that no method could benefit from it.

---

## Slide 9 — The first PAH was biased — and we fixed the cause

**On slide:**
- First v4 PAH learned α through the actor's policy-gradient loss. The gradient of `α·A_mission + (1−α)·A_safety` w.r.t. α is `A_mission − A_safety` → in danger `A_safety` is very negative → **α pushed towards the mission exactly when danger is close** (measured: +0.200, the maximum, when τ < 1).
- Fix (done **once**, then design frozen): PAH predicts the risk and learns by regression; no gradient from the actor loss.
- Learned α now tracks danger (right):

**Image:** `images/s09_alpha_by_tau.png`

**On slide, small:** the biased v1 result is kept as a finding: *"a learned α trained through the policy objective is biased against safety"* (single seed, training-time numbers).

**Say:** This is the honest part: the first PAH learned the wrong direction. We found the cause from the mechanism, not by tuning on performance. In the figure: in danger (τ < 1) PAH's α is about 0.13–0.19, when safe about 0.8, and it turns towards safety earlier than the hand-coded rule.

---

## Slide 10 — Experimental protocol (why you can trust the numbers)

**On slide:**
- **Same** environment, **same** budget (8,000 episodes), **same** hyperparameters for all 9 methods.
- **10 training seeds** (42–51) per method and stage; **186 trained models** (RMAPPO: 6, see slide 22).
- Test: 200 episodes per model, deterministic actions, evaluation seed 7001 → every model sees the **same 200 layouts**.
- Success = every drone reaches its assigned target, no collision, within 500 steps (as in DA-MAPPO).
- **Primary question fixed before training:** Stage 3, MAPPO + PAH vs Fixed-weight MAPPO. Everything else is secondary (no multiple-testing correction, stated).
- Reproducibility: all 186 evaluations re-run → **186/186 byte-identical**; tables generated by script.

**Say:** This slide tells the examiner how we stopped ourselves from chasing results: the question was written first, settings were frozen, seeds were fixed. Stage 2 = 5 drones, 10 obstacles; Stage 3 = 8 drones, 20 obstacles.

---

## Slide 11 — Main result: all methods, both stages

**Image:** `images/s11_success_all_methods.png`

**On slide (call-outs):**
- MAPPO + PAH: **86.8 %** (Stage 2) and **82.7 %** (Stage 3) — **first of 9 methods at both stages**.
- Grey = the four base-paper methods trained in our environment.

**Say:** Each bar is the average of 10 seeds, dots are individual seeds, the line is the 95% confidence interval. The base-paper methods (IGAT-style, DA-MAPPO 2D, MAPPO, IPPO) are all below.

---

## Slide 12 — How much better, and how sure are we

**Image:** `images/s12_pah_vs_each_method.png`

**On slide:**
- **Primary (Stage 3): MAPPO + PAH − Fixed-weight MAPPO = +8.6 points, 95 % CI [+1.7, +15.4]** → better.
- Stage 2 vs Hand-coded τ-rule MAPPO: +2.0 [−2.6, +6.6] → **not settled** (stated openly).
- All other comparisons are secondary.
- Robustness: without seed 42 (the seed on which the first PAH's bias was seen): +7.9 [+0.7, +15.1].

**Say:** To be direct: the gain is settled but modest, plausibly between 2 and 15 points. At Stage 2 we are not clearly better than the hand-coded rule; the learned α is clearly better with 8 drones.

---

## Slide 13 — Where does the gap to DA-MAPPO (2D) come from?

**Image:** `images/s13_gap_breakdown.png`

**On slide:**
- Three **controlled** steps (each changes one thing), Stage 3: conflict-graph observation **+15.4**, separate value heads **+30.0**, PAH's learned α **+8.6**.
- PAH's own contribution is the last step — **we do not claim the whole 53.9-point gap as PAH's effect.**

**Say:** This slide shows our honesty. Most of the gap comes from the conflict graph and the two value heads, both part of our framework. PAH's own contribution is +8.6.

---

## Slide 14 — How the episodes end

**Image:** `images/s14_outcomes.png`

**On slide:**
- Failures are mostly **obstacle collisions**, in every method; MAPPO + PAH has the fewest (collision 17 %).
- Without any assignment (drone i → target i), drone–drone collisions rise (6 % of episodes) and paths are ~2× longer.
- Timeouts are small (at most 6 %, IPPO).

**Say:** This is where the safety effect shows: 17% collisions against 26% for Fixed-weight MAPPO.

---

## Slide 15 — Compared with the DA-MAPPO paper: ranking, not absolute numbers

**Image:** `images/s15_ranking_vs_paper.png`

**On slide:**
- Same colour = same method. Paper: 3 drones, 3D Gazebo, ~3 M steps with curriculum. Ours: 2D, 8 drones, 8,000 episodes, no curriculum.
- **Absolute numbers are not comparable. The order is:** dynamic assignment above fixed assignment, IPPO the weakest, and our MAPPO + PAH above all base-paper methods.

**Say:** The examiner will ask why their method gets 90% and our DA-MAPPO (2D) gets 28.9%. Answer: their setting has 3 drones, 3D, long training and a curriculum; ours has 8 drones and a much smaller training budget. So we compare the order of methods, not the numbers.

---

## Slide 16 — A comparison that does not depend on the simulator

**Image:** `images/s16_gain_over_mappo.png`

**On slide:**
- Gain over MAPPO (fixed assignment) in each study. **Same direction in both:** dynamic assignment helps (ours settled at Stage 3: +7.0 [+2.3, +11.6]); IPPO is not better than MAPPO.
- MAPPO + PAH adds a much larger gain.

**Say:** When absolute numbers cannot be compared, we compare how much each method gains over MAPPO. The direction is the same in both studies.

---

## Slide 17 — Phase 3 intro: the base papers' experiments on our trained models

**On slide:**
- **No new training.** 180 trained models re-evaluated with *one* test condition changed at a time (200 episodes, seed 7001).
- DA-MAPPO: obstacle density 30–50, static vs moving targets, assignment every step vs every 50 steps.
- IGAT-MARL: swarm size 3→10, loss of separation, active edges.
- Extra: sensor noise, computation time.
- No new primary claim — all secondary; models trained at one setting, so these are **generalisation tests** (every method is expected to drop).
- Question asked: **does MAPPO + PAH stay ahead of Fixed-weight MAPPO?**

**Say:** In total 2,390 result files, 1 hour 41 minutes on a laptop. This answers the supervisor's point: the base papers' experiments, repeated in our environment.

---

## Slide 18 — Obstacle density (DA-MAPPO ENV-1/2/3)

**Image:** `images/s18_density.png`

**On slide:**
- Every method drops as discs are added (Stage 3, MAPPO + PAH: 93.5 → 82.7 → 70.3 → 51.3 → 40.4 at 10/20/30/40/50 discs).
- The **order of methods is the same at every density**; MAPPO + PAH first everywhere.
- Same trend as the paper: methods without a conflict graph fall towards zero.

**Optional second image (same slide, small):** `images/s18_density_vs_paper.png` — paper (left) vs ours (right); honest caveat: our DA-MAPPO (2D) is far below the paper's at 30–50 obstacles (8 drones, no curriculum).

**Say:** Every method drops as obstacles are added, but the order stays the same and MAPPO + PAH stays first. The second figure puts the paper next to ours; we show it openly: our DA-MAPPO (2D) is far below the paper's, because we have 8 drones, no curriculum and far fewer training steps.

---

## Slide 19 — Swarm size 3 → 10 (IGAT-MARL)

**Image:** `images/s19_swarm_size.png`

**On slide:**
- Models used as trained on 3–10 drones (only methods whose observation does not depend on the swarm size).
- Stage 3: MAPPO + PAH degrades least (**−10.0 points** from 3 to 10 drones), Fixed-weight MAPPO −17.4, IGAT-style MAPPO −44.8.
- IGAT-MARL metrics: loss of separation (and active conflict edges) grow with swarm size — same trend as the paper. **Careful:** MAPPO + PAH does **not** have clearly fewer near-misses than Fixed-weight MAPPO (0.63 vs 0.55 per episode) — its advantage is mission success, not fewer close passes.

**Images (second row):** `images/s19_loss_of_separation.png`, `images/s19_edges_vs_igat_paper.png`

**Say:** Loss of separation is IGAT-MARL's metric, and we measure it on our own methods. The honest point: PAH's advantage is in success, not in fewer near-misses.

---

## Slide 20 — Static targets and assignment every 50 steps

**Image:** `images/s20_static_targets.png` and `images/s20_assign_every_50.png`

**On slide:**
- **Assignment every 50 steps** instead of every step: every method loses a little (−0.7 to −3.8 points) — real-time re-assignment helps, but modestly here.
- **Static targets:** every method does **worse** (all trained on moving targets); MAPPO + PAH loses less (Stage 3: −7.0 vs −15.0 for Fixed-weight MAPPO), so its lead grows to **+16.6**.
- In the paper static is *easier* (their "dynamic" = targets swap places; ours = targets drift) — we report this as an **observation, not explained** (`images/s20_static_vs_paper.png` in appendix).

**Say:** This result is unexpected and we are not hiding it: every method does worse on static targets. We have not tested why, so it is written as an observation only.

---

## Slide 21 — Robustness and cost

**Images:** `images/s21_noise.png`, `images/s21_timing.png`

**On slide:**
- **LiDAR noise** up to 10 % of the ray range changes success by at most about 3 points for any method; MAPPO + PAH 82.7 → 80.8; lead over Fixed-weight MAPPO +8.5 to +8.7.
- **Decision time** per step for the whole swarm (laptop, 1 thread): MAPPO + PAH = Fixed-weight MAPPO ≈ 0.04–0.05 ms; IGAT-style MAPPO ≈ 6× slower (graph attention). PAH is used for the training reward, not for choosing actions → **no run-time cost**.

**Say:** Noise barely matters up to 10% of the ray range. And PAH costs nothing at run time: it shapes the training reward, it does not choose actions.

---

## Slide 22 — The lead holds everywhere we looked

**Image:** `images/s22_pah_lead_everywhere.png`

**On slide:**
- MAPPO + PAH minus Fixed-weight MAPPO: **CI entirely above 0 in all 31 settings** (14 at Stage 2, 17 at Stage 3): densities, static targets, assignment every 50, swarm sizes 3–10, sensor noise.
- Weakest case: the smallest swarm, N = 3 (+3.5 at Stage 2; +4.8 [+0.1, +9.5] at Stage 3) — with three drones there are few conflicts for a learned balance to resolve.
- The lead tends to grow when the task gets harder (denser obstacles, larger swarms at Stage 3).

**Say:** This is the evidence that the result is not specific to one test setting. Remember that these are all secondary comparisons, not a new primary claim.

---

## Slide 23 — What we claim, and what we do not

**On slide (two columns):**

| We claim | We do **not** claim |
|---|---|
| MAPPO + PAH is better than Fixed-weight MAPPO at 8 drones: +8.6 [+1.7, +15.4]; plausibly 2–15 points | That PAH explains the whole gap to DA-MAPPO (2D) (+53.9) |
| It ranks first of 9 methods at both stages, with the same budget and settings as the base-paper methods | That we reproduced the base papers' numbers (different simulator, sensors, training length) |
| The lead holds in 31 of 31 test settings | That PAH reduces close approaches (loss of separation is similar) |
| A policy-gradient-trained α was biased against safety (finding); a risk-learning α fixes it | That PAH is clearly better than the hand-coded rule at 5 drones (+2.0, not settled) |
| | Anything about 3D or real hardware |

**Say:** We state the limits of our claims ourselves, before the panel does. That builds trust.

---

## Slide 24 — Limits (state them before the panel does)

**On slide:**
- The primary confidence interval is wide; its lower end is +1.7 points.
- At 5 drones the learned α is not clearly better than the hand-coded τ-rule.
- Base-paper methods use **our shared settings**, tuned on Plain MAPPO — not tuned one by one; their absolute scores are below the papers' 3D results.
- **RMAPPO** did not learn under the shared settings (exploration collapsed; 0 % on 6 seeds at Stage 3; no implementation bug found) → appendix with the reason, **not** a performance number.
- A mechanism check (advantage-signal correlation) does **not** explain where PAH's gain comes from — we do not claim "PAH reshapes the advantage".
- One 2D simulated environment.

**Say:** Say each of these ourselves before anyone asks. RMAPPO is in the appendix with the reason.

---

## Slide 25 — Conclusion

**On slide:**
1. A unified MAPPO + PAH framework for joint assignment and collision avoidance.
2. First of 9 methods at both stages; PAH's own gain **+8.6 [+1.7, +15.4]** over a fixed weight at 8 drones.
3. Diagnosis-driven redesign: obstacles, not other drones, cause failures; a policy-gradient PAH is biased against safety.
4. Base-paper experiments re-run on our models: the lead holds in 31/31 settings.

**Say:** Four points: the framework, the result with its confidence interval, the diagnosis-driven redesign, and the base-paper experiments.

---

## Slide 26 — Next steps and questions for the panel

**On slide:**
- Thesis writing (methodology and literature review can start now); results tables in the base papers' format.
- Optional strengthening: re-run the primary comparison on **10 fresh seeds** (~2.5 h on the laptop) to narrow the CI; RMAPPO with its original large-batch setting (~one night).
- **Questions for the panel:** (1) Is the experiment list sufficient for the comparison chapter? (2) RMAPPO in the appendix, or re-run it? (3) Present the v3 study as the first stage that motivated the redesign?

**Say:** Ask the panel these three questions explicitly; it keeps the conversation under our control.

---

# Appendix (for questions only)

## A1 — Difficulty, ours vs paper
**Image:** `images/a1_difficulty_vs_paper.png` — success as the task gets harder in the paper (30 → 50 obstacles) and in ours (Stage 2 → Stage 3).

## A2 — Learning curves (training-time evaluation)
**Image:** `images/a2_learning_curves.png` — **training-time** numbers (20 episodes every 100, seed 999): not the final numbers (those are lower); the ordering is the same. Never mix the two in one table.

## A3 — Time and path length
**Image:** `images/a5_phase1b_time_path.png` — T_ave and L_ave over successful episodes only (survivor bias: methods with low success are measured on few episodes). MAPPO + PAH finishes fastest of all methods (61 steps vs 76 for Fixed-weight MAPPO at Stage 3).

## A4 — Static vs moving: paper vs ours
**Image:** `images/s20_static_vs_paper.png` — in the paper moving is worse than static (swap of targets); ours: models trained on drifting targets are worse on static. Different meaning of "dynamic".

## A5 — Mechanism check
Advantage-correlation check on 80 two-head models: the actor signal of every method stays 92–99 % correlated with Plain MAPPO's; closeness to Plain does **not** track success (MAPPO + PAH is *closer* than Fixed-weight MAPPO yet better). Conclusion: "not explained by a large change in the actor's learning signal." Source: `v4/05-mechanism-check/REPORT.md`.

## A6 — Method list (full names used everywhere)

| Full name | What it is |
|---|---|
| MAPPO + PAH | MAPPO + learned α (thesis method) |
| Fixed-weight MAPPO | α = 0.5 fixed, two value heads |
| Hand-coded τ-rule MAPPO | α = 0.1 + 0.8·τ/3, nothing learned |
| MAPPO + PAH (Hungarian off) | no assignment mechanism: drone i → target i |
| Plain MAPPO | one value head, combined reward |
| IGAT-style MAPPO | MAPPO + graph attention over the conflict graph (width 64, no dropout) |
| DA-MAPPO (2D) | MAPPO with all-teammate observation, Hungarian every step |
| MAPPO | MAPPO with assignment fixed at the start (rigid) |
| IPPO | independent PPO, local critic |
| RMAPPO | recurrent MAPPO — appendix only (did not learn) |

---

# Prepared answers to likely questions

**Q1. Why not use graph attention like IGAT-MARL?**
We use IGAT's *conflict graph* (DCPA/TCPA). We also trained an **IGAT-style MAPPO with graph attention** as a baseline in our environment (46.8 % vs MAPPO + PAH 82.7 % at Stage 3). PAH does not depend on the encoder: it works on τ, d_target and n_conflict.

**Q2. Is PAH just a learned τ-rule?**
Same three inputs, but PAH learns the risk from the safety cost that followed, and it turns towards safety earlier than the rule (α 0.32 vs 0.51 at 1 ≤ τ < 2). Stage 3: **+11.3 [+4.6, +17.9]** over Hand-coded τ-rule MAPPO. Stage 2: +2.0, not settled — we say so.

**Q3. You changed PAH after seeing seed 42. Is that tuning on the test set?**
The change was made **once**, because of a mechanism (the gradient sign, measured +0.200 at τ < 1), and tested on synthetic data and a 300-episode smoke run — not on seed performance. Then all runs used the frozen design. Without seed 42: +7.9 [+0.7, +15.1]. On seed 42 itself the new PAH is *below* the τ-rule (79.5 vs 82.0 %), so the design was not shaped to win that seed. (A fresh-seed replication is the optional next step.)

**Q4. Why are the base-paper numbers so much lower than in the papers?**
Different simulator (3D Gazebo vs 2D), 3 vs 8 drones, ~3 M steps with a curriculum vs 8,000 episodes, and our shared settings were tuned on Plain MAPPO only. We compare the **order** and the **gain over MAPPO**, not absolute numbers.

**Q5. Why is RMAPPO missing?**
It did not learn under the shared settings (exploration collapsed, no bug found, 6 seeds, 0 %). Reporting it as a performance number would be misleading, so it goes to an appendix with the reason. We can re-run it with its original large-batch setting (about one night).

**Q6. Is the 8.6-point gain real? The interval starts at +1.7.**
By the rule fixed before training, yes (whole interval above 0, 9 of 10 seeds higher). It is modest and we give the CI everywhere. The lead is also positive in 31/31 other settings.

**Q7. Where does the big gap to DA-MAPPO (2D) come from, then?**
Conflict-graph observation (+15.4) and the two value heads (+30.0) — both part of our framework — and PAH's α (+8.6). Steps are roughly additive.

**Q8. Why 2D? Why not PyBullet / 3D?**
The research question (joint assignment + collision avoidance + arbitration) does not need 3D, and 2D allowed 186 trained models on a laptop with 10 seeds each. We make no 3D or hardware claims.

**Q9. Why does everything get worse on static targets?**
We do not know; the models were trained only on moving targets and may rely on target motion. Reported as an observation, not explained without a test.

**Q10. Multiple comparisons?**
Only the Stage 3 comparison with Fixed-weight MAPPO was pre-registered as primary. All others are labelled secondary, no correction applied (stated in the figures).

**Q11. What does "success" mean?**
All drones reach their assigned targets, no collision, within 500 steps (as in DA-MAPPO). A unit test checks that the definition is identical for every assignment mode.

**Q12. Is it reproducible?**
10 seeds per method, fixed evaluation seed, all 186 evaluations re-run byte-identical, tables generated by script, hardware and settings recorded.

---

# Figure sources (all copied into `images/`)

| Slide | File in `images/` | Original location (under `code/notebooks/v4/`) |
|---|---|---|
| 7 | `s07_v3_collision_type.png` | `00-diagnostics/output/collision_type_check.png` |
| 9 | `s09_alpha_by_tau.png` | `02-redesign/output/fig3_alpha_by_tau.png` |
| 11 | `s11_success_all_methods.png` | `03-base-paper-baselines/output/figures/fig1_success_all_methods.png` |
| 12 | `s12_pah_vs_each_method.png` | `…/fig2_pah_vs_each_method.png` |
| 13 | `s13_gap_breakdown.png` | `…/fig3_gap_breakdown.png` |
| 14 | `s14_outcomes.png` | `…/fig4_outcomes.png` |
| 15 | `s15_ranking_vs_paper.png` | `…/fig6_ranking_vs_paper.png` |
| 16 | `s16_gain_over_mappo.png` | `…/fig8_gain_over_mappo.png` |
| 18 | `s18_density.png`, `s18_density_vs_paper.png` | `04-base-paper-experiments/output/figures/p3_fig1_density.png`, `p3_cmp1_density.png` |
| 19 | `s19_swarm_size.png`, `s19_loss_of_separation.png`, `s19_edges_vs_igat_paper.png` | `…/p3_fig5_swarm.png`, `p3_fig6_swarm_los.png`, `p3_cmp3_edges.png` |
| 20 | `s20_static_targets.png`, `s20_assign_every_50.png`, `s20_static_vs_paper.png` | `…/p3_fig3_static.png`, `p3_fig4_assign50.png`, `p3_cmp2_static_dynamic.png` |
| 21 | `s21_noise.png`, `s21_timing.png` | `…/p3_fig7_noise.png`, `p3_fig8_timing.png` |
| 22 | `s22_pah_lead_everywhere.png` | `…/p3_fig2_pah_lead.png` |
| A1 | `a1_difficulty_vs_paper.png` | `03-base-paper-baselines/output/figures/fig7_difficulty_vs_paper.png` |
| A2 | `a2_learning_curves.png` | `…/fig5_learning_curves.png` |
| A3 | `a5_phase1b_time_path.png` | `02-redesign/output/fig2_time_path.png` |

Vector (SVG) versions of all v4 figures sit next to the PNGs in the original folders — use those when building the real PPT.

---

# Notes for building the real PPT (v1)

1. **Check the figures are readable at slide size.** The figures were made for reports (small text). Slides 11, 12, 18, 19, 22 are fine at full width; slide 22 (31-setting forest plot) is tall — give it the whole slide.
2. **Not used on purpose:** the v3 figures (`results-table/output/fig1–fig11`) still use the short names B4/H/M. If you want the v3 story as a figure, regenerate it with full names first (slide 7 uses a table instead).
3. **The old Claude artifacts** (`GQTD3VBaacCbfNuvEh3cB6`, the v3 one) contain a wrong ablation framing and the superseded "0.2 points" figure — **do not show it**. The current ones are the supervisor report (`docs/research/12_supervisor_progress_v4.html`) and the Phase 3 report (`04-base-paper-experiments/output/phase3_report.html`).
4. **Open points to decide before the real deck:** (a) run the optional fresh-seed replication first (a narrower CI would make slide 12 stronger); (b) RMAPPO: appendix vs re-run; (c) whether slide 18's second image (our DA-MAPPO (2D) far below the paper) should be shown or kept in the appendix — showing it is more honest and was already in the Phase 3 report.
5. **Time check:** 26 slides × ~1 minute = 26 minutes. If only 15 minutes: keep slides 1–3, 7–9, 11–13, 18–19, 22–23, 25.
