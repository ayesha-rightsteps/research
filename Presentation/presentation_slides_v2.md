# Synopsis Presentation — Ayesha Khalil
## Formatted to match SP25-RCS-008 style
**13 Slides | Concise bullets | ❌ ✅ symbols | Numbered**

---

---

## SLIDE 1 — Title

**[Full width, centered]**

Integrating Real-Time Target Assignment and Conflict-Aware Collision Avoidance for Multi-UAV Navigation in Three-Dimensional Environments Using Multi-Agent Reinforcement Learning

By **Ayesha Khalil**
Supervisor: **Dr. Faisal Rehman**
Co-Supervisor: **Dr. Ehzaz Mustafa**
COMSATS University Islamabad, Abbottabad Campus

---

---

## SLIDE 2 — Introduction to Multi-UAV Systems

**Goal: Enable coordinated, autonomous navigation of multiple drones in shared 3D airspace**

**[LEFT COLUMN — text]**
- UAVs have evolved from military tools to civilian platforms
- Key uses: disaster response, search & rescue, agriculture, inspection
- Single drone is insufficient for large-scale missions
- Multi-UAV teams are required — but coordination is the hard problem
- Hardware alone cannot solve this — **intelligent algorithms are needed**

**[RIGHT COLUMN — image]**
→ Use `img_02_uav_applications.png`

**[Bottom right corner: slide number 1]**

---

---

## SLIDE 3 — Multi-UAV Coordination: The Core Challenge

**Goal: Move from centralized planners to adaptive, learning-based coordination**

**[LEFT COLUMN — text]**

**Classical Approach — Centralized Planner:**
- Computes globally optimal solution before deployment
- ❌ Fails when targets move or obstacles appear mid-mission
- ❌ Recomputing in real time is computationally intractable

**Learning-Based Approach — MARL:**
- Drones learn cooperative behavior through trial and error
- CTDE: train together, execute independently
- **MAPPO** — most stable cooperative MARL baseline (Yu et al., 2022)

**[RIGHT COLUMN — image]**
→ Use `img_04_ctde_diagram.png`

**[Bottom right corner: slide number 2]**

---

---

## SLIDE 4 — Introduction Cont. — The Fragmented Progress

**Goal: Identify the exact gap this research fills**

**[LEFT COLUMN — Problems with existing work]**

**Fragmented Literature:**
- ❌ Target assignment methods ignore collision avoidance
- ❌ Collision avoidance methods have no goal/target structure
- ❌ All existing work is tested in 2D only
- ❌ No framework combines both mechanisms in 3D

**Our Contribution:**
- ✅ Identifies two complementary papers each pointing to the other as future work
- ✅ Proposes unified MAPPO policy combining both in 3D
- ✅ First empirical test: do the mechanisms cooperate or compete?

**[RIGHT COLUMN — image]**
→ Use `img_05_gap_diagram.png`

**[Bottom right corner: slide number 3]**

---

---

## SLIDE 5 — Motivation

**[4 bullet points, then the research statement at bottom]**

- DA-MAPPO [10] achieves **90–99% mission success** using real-time Hungarian assignment — but **has no collision avoidance**
- IGAT-MARL [9] reduces interaction edges by **44%** using a conflict-aware graph — but **has no target assignment**
- DA-MAPPO ablation: removing assignment information causes success to drop from **90% → 0%**
- Both papers explicitly name the other's problem as **their own future work** — this research is that future work

**This research proposes a unified MAPPO-based framework that integrates real-time target assignment and conflict-aware collision avoidance in a single policy for 5–8 drones in a 3D environment.**

**[RIGHT COLUMN — image]**
→ Use `img_07_two_papers.png`

**[Bottom right corner: slide number 4]**

---

---

## SLIDE 6 — Related Works

**[Table — first 13 papers]**

| Ref | Author & Year | Method | Key Result | Limitation |
|---|---|---|---|---|
| [1] | Tang et al., 2024 | Improved D3QN + PER | 95% success in dynamic obstacles | Single drone, 2D, discrete actions |
| [2] | Kong et al., 2024 | TANet-TD3 + Hungarian supervision | Joint assignment + path planning | 5 drones only, 2D, no collision avoidance |
| [3] | Jarray et al., 2025 | DQN + dynamic reward | 98% success in 3D large-scale env | Single drone, static obstacles |
| [4] | Zhang et al., 2025 | Mean-field DDPG + attention | Scales to 120 drones | 2D only, homogeneous drones |
| [5] | Poudel & Moh, 2026 | MAML + MA-DDPG + coalition | Handles failures, heterogeneous drones | 2D only, 10–30 drones |
| [6] | Xu et al., 2026 | IPPO + GPT-4o distillation | 52% higher data rate | 2D, no energy modeling |
| [7] | Wang et al., 2025 | RALLY: LLM + RMIX roles | Generalizes to unseen swarm sizes | 2D, 14s inference latency |
| [8] | Khan et al., 2026 | LLM framework comparison | 96.1% success, 76% lower token cost | Wildfire domain only |
| [9] | Rezaee et al., 2026 | IGAT-MARL: conflict graph + GAT | 44% fewer edges, 17% higher reward | **No target assignment** |
| [10] | Sheng et al., 2026 | DA-MAPPO + Hungarian obs | 90–99% success, robust to 50% loss | **2D only, 3 drones, no collision avoidance** |
| [11] | Govinda et al., 2025 | Survey: DRL for autonomous systems | Identifies lack of unified frameworks | Survey only |
| [12] | Mnih et al., 2015 | DQN: CNN + experience replay | Human-level on Atari | Discrete actions, overestimation |
| [13] | Van Hasselt et al., 2016 | Double DQN | Reduces Q-value overestimation | Discrete actions only |

**[Bottom right corner: slide number 5]**

---

---

## SLIDE 7 — Related Works Cont.

**[Table — remaining 12 papers]**

| Ref | Author & Year | Method | Key Result | Limitation |
|---|---|---|---|---|
| [14] | Wang et al., 2016 | Dueling Network: V(s) + A(s,a) | Better evaluation in low-variance states | Discrete actions |
| [15] | Schaul et al., 2016 | Prioritized Experience Replay | Faster learning from rare transitions | Priority overhead |
| [16] | Schulman et al., 2017 | PPO: clipped surrogate objective | Stable training, simple implementation | On-policy, sample inefficient |
| [17] | Lowe et al., 2017 | MADDPG: CTDE, centralized critic | Handles cooperative + competitive | Scales poorly to large teams |
| [18] | Fujimoto et al., 2018 | TD3: clipped double Q + delayed update | Reduces overestimation in continuous control | Hard to extend to multi-agent directly |
| [19] | Rashid et al., 2018 | QMIX: monotonic value factorization | Strong on StarCraft cooperative tasks | Monotonicity limits expressiveness |
| [20] | Yang et al., 2018 | Mean Field MARL | O(N) complexity, scales to 200 agents | Loses individual agent information |
| [21] | Yu et al., 2022 | MAPPO: shared centralized critic | Competitive with QMIX, much simpler | On-policy, needs global state for training |
| [22] | Sunehag et al., 2018 | VDN: additive Q factorization | Simple cooperative training | Too restrictive; QMIX outperforms it |
| [23] | Aggarwal & Kumar, 2020 | Survey: UAV path planning | DRL is best for dynamic environments | Survey only |
| [24] | Oliehoek & Amato, 2016 | Dec-POMDP framework | Formal multi-agent problem formulation | Exact solutions intractable at scale |
| [25] | Gronauer & Diepold, 2022 | Survey: multi-agent DRL | Scalability + partial observability = open gaps | Survey only |

**[Bottom right corner: slide number 6]**

---

---

## SLIDE 8 — Problem Statement

**[Single block of text, centered, slightly larger font]**

Existing approaches to multi-UAV coordination treat dynamic target assignment and collision avoidance as separate problems, each developed and validated independently in two-dimensional environments.

When both mechanisms operate simultaneously in three-dimensional space, they generate competing navigation signals — the assignment directs each drone toward its target without awareness of active collision conflicts, while the collision avoidance module forces course corrections without awareness of current assignments, a tension that becomes structurally significant when vertical flight paths are introduced.

No existing framework has addressed this interference jointly in three-dimensional space, leaving it unknown whether a unified policy can sustain both assignment optimality and collision safety simultaneously, or whether the mechanisms degrade each other when combined.

**[RIGHT — small image]**
→ Use `img_06_conflict_diagram.png`

**[Bottom right corner: slide number 7]**

---

---

## SLIDE 9 — Research Objectives

**[4 numbered points]**

**1.** Design a unified observation vector encoding both the Hungarian-algorithm assignment state and the conflict-aware neighborhood for each drone in a 3D MAPPO policy

**2.** Test scalability across swarm sizes of **3, 5, and 8 drones** — determine if performance degrades as simultaneous assignment-conflict interactions increase

**3.** Run controlled ablation experiments isolating the contribution of:
- The conflict graph alone
- The assignment mechanism alone
- The 3D extension alone
- All combined

**4.** Find the failure boundary — identify swarm size, obstacle density, and target speed conditions where the unified policy fails, and characterize the failure mode

**[Bottom right corner: slide number 8]**

---

---

## SLIDE 10 — Proposed Methodology

**[LEFT — observation vector diagram]**
→ Use `img_08_observation_vector.png`

**Each drone's observation includes 4 components:**
| # | Component | Source |
|---|---|---|
| 1 | Own 3D position + velocity | Onboard sensors |
| 2 | Current target position | Hungarian algorithm (updated every step) |
| 3 | Conflict neighbor positions + velocities | Conflict graph (sparse, collision-risk pairs only) |
| 4 | Obstacle proximity (6 directions) | Proximity sensors ±x ±y ±z |

**Policy:** MAPPO — Centralized Critic (training) | Decentralized Actor (execution)
**Actions:** Continuous 3D velocity commands
**Simulator:** PyBullet | **Framework:** PyTorch

**[RIGHT — pipeline image]**
→ Use `img_09_pipeline.png`

**[Bottom right corner: slide number 9]**

---

---

## SLIDE 11 — Training Strategy & Evaluation

**[LEFT COLUMN — Curriculum Training]**

**4-Stage Curriculum:**

| Stage | Drones | Obstacles | Goal |
|---|---|---|---|
| 1 | 3 | Low | Replicate DA-MAPPO baseline in 3D |
| 2 | 5 | Medium | Assignment + avoidance together |
| 3 | 8 | 50 (high) | Full challenge |
| 4 | Unseen sizes | Various | Generalization |

→ Use `img_10_curriculum.png`

---

**[RIGHT COLUMN — Evaluation]**

**Primary Metric:** Mission success rate (all drones reach targets, zero collisions, within time limit)

**Secondary Metrics:** Inter-drone collisions | Obstacle collisions | Reassignments per episode | Trajectory length

**4 Baselines:**
- B1: Standard MAPPO (no mechanisms)
- B2: DA-MAPPO ported to 3D (no conflict graph)
- B3: IGAT-MARL + fixed assignment (no real-time assignment)
- B4: Original 2D DA-MAPPO (replication check)

→ Use `img_11_eval_grid.png`

**[Bottom right corner: slide number 10]**

---

---

## SLIDE 12 — References

**[Two columns, small font]**

**[LEFT]**
[1] Tang et al. Drones, 2024.
[2] Kong et al. Front. Neurorobot., 2024.
[3] Jarray et al. Procedia Comput. Sci., 2025.
[4] Zhang et al. Chin. J. Aeronaut., 2025.
[5] Poudel & Moh. Internet of Things, 2026.
[6] Xu et al. arXiv:2505.08448, 2026.
[7] Wang et al. IEEE OJ-VT, 2025.
[8] Khan et al. IEEE Access, 2026.
[9] Rezaee et al. Appl. Soft Comput., 2026.
[10] Sheng et al. IEEE IoT J., 2026.
[11] Govinda et al. IEEE TITS, 2025.
[12] Mnih et al. Nature, 2015.
[13] Van Hasselt et al. AAAI, 2016.

**[RIGHT]**
[14] Wang et al. ICML, 2016.
[15] Schaul et al. ICLR, 2016.
[16] Schulman et al. arXiv, 2017.
[17] Lowe et al. NeurIPS, 2017.
[18] Fujimoto et al. ICML, 2018.
[19] Rashid et al. ICML, 2018.
[20] Yang et al. ICML, 2018.
[21] Yu et al. NeurIPS, 2022.
[22] Sunehag et al. AAMAS, 2018.
[23] Aggarwal & Kumar. Comput. Commun., 2020.
[24] Oliehoek & Amato. Springer, 2016.
[25] Gronauer & Diepold. Artif. Intell. Rev., 2022.

**[Bottom right corner: slide number 11]**

---

---

## SLIDE 13 — Thank You

**[Centered, large font]**

**Thank You**

*Open for Questions*

---

Ayesha Khalil | CIIT/SP25-RCS-009/ATD
Supervisor: Dr. Faisal Rehman | Co-Supervisor: Dr. Ehzaz Mustafa
COMSATS University Islamabad — Abbottabad Campus

---

---

# QUICK SPEAKER NOTES — KEY THINGS TO SAY PER SLIDE

| Slide | One thing to always say |
|---|---|
| 2 | "Sir, the core challenge is not the drone hardware — it is the coordination algorithm." |
| 3 | "Sir, MAPPO trains all drones together but each drone acts on its own. That is the key design." |
| 4 | "Sir, every researcher working on assignment ignored avoidance. And vice versa. No one combined them." |
| 5 | "Sir, when DA-MAPPO removed the assignment from the observation, success went from 90% to zero. That one number tells you how important the mechanism is." |
| 6–7 | "Sir, I reviewed 25 papers. The two most important ones are [9] and [10] — I will explain them now." |
| 8 | "Sir, the problem is that in 3D, when assignment says go left and avoidance says stop, they conflict. No one has tested what happens." |
| 9 | "Sir, Objective 4 is the one most researchers skip — finding where the framework fails is as important as where it succeeds." |
| 10 | "Sir, the key design decision is what each drone is allowed to see — I am combining assignment state and conflict neighborhood in one vector." |
| 11 | "Sir, I am using the same curriculum approach that both key papers used — this is a validated training strategy." |

---

# KEY NUMBERS — MEMORIZE THESE

| Number | What it means |
|---|---|
| 0% → 90% | DA-MAPPO success without vs. with assignment info (ablation) |
| 44% | Reduction in interaction edges from IGAT-MARL conflict graph |
| 17% | Reward improvement from IGAT-MARL |
| 25 | Total papers reviewed |
| 11/25 | Papers from last 3 years (44% recency) |
| 3, 5, 8 | Swarm sizes tested |
| 30, 40, 50 | Obstacle densities tested |
| 4 | Number of baselines |
| 12 months | Research timeline |
