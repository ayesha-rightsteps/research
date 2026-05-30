# COMSATS University Islamabad
## Synopsis for MS ☑   Ph.D. ☐

---

| | |
|---|---|
| **Name:** Ayesha Khalil | **Registration No.:** SP25-RCS-009 |
| **Program:** MS Computer Science | **Area of Specialization:** Multi-Agent Systems / Intelligent Autonomous Systems |
| **Department:** Computer Science | **Campus:** Islamabad |
| **Date of Admission:** _______________ | **Date of Synopsis Submission:** May 30, 2026 |

**Proposed Title of the Thesis:**

> Integrating Real-Time Target Assignment and Conflict-Aware Collision Avoidance for Multi-UAV Navigation in Three-Dimensional Environments Using Multi-Agent Reinforcement Learning

---

### Supervisory Committee

| Name and Designation | Role |
|---|---|
| _______________ | Supervisor |
| _______________ | Co-supervisor / Member |
| _______________ | Member |
| _______________ | Member |

**Student's Signature:** ________________________________

---

## Summary of the Research

Multi-UAV coordination using deep reinforcement learning has advanced significantly, yet a specific and documented gap persists: no existing framework simultaneously handles dynamic target assignment and conflict-aware collision avoidance in three-dimensional environments. The two most advanced contributions to these sub-problems — DA-MAPPO (Sheng et al., 2026) for target assignment and IGAT-MARL (Rezaee et al., 2026) for collision avoidance — were developed independently, each tested in two-dimensional environments with at most ten drones, and each explicitly identifies the other paper's contribution as its own future work. DA-MAPPO demonstrated that embedding real-time Hungarian-algorithm-based target assignments into each drone's observation vector is the sole mechanism responsible for successful navigation: its own ablation study shows 0% mission success when this assignment information is removed. IGAT-MARL demonstrated that sparse conflict-aware interaction graphs, which connect only drone pairs on a predicted collision course, reduce unnecessary communication by 44% while improving avoidance performance. This research proposes a unified MAPPO-based framework that integrates both mechanisms in a single policy trained in a 3D simulation environment. The central research problem is the interference that arises in 3D space: the assignment module re-routes drones toward their targets without awareness of active conflict states, while the conflict graph forces course deviations without awareness of current target assignments. In three dimensions, altitude introduces vertical collision courses absent from planar environments, making this competition structurally significant. The proposed framework encodes both assignment state and conflict neighborhood in each drone's observation, trained via curriculum learning from 3 to 8 drones with progressive obstacle density. Evaluation will compare against four controlled baselines across three swarm sizes and three obstacle densities, yielding the first empirical answer to whether these two mechanisms cooperate or interfere when operating jointly in 3D.

*[Introduction must start from next page]*

---

## 1.   Introduction

Autonomous unmanned aerial vehicle (UAV) systems have attracted substantial research attention over the past decade, driven by their demonstrated value in disaster response, search-and-rescue operations, infrastructure inspection, and time-sensitive logistics. In these applications, the relevant challenge is rarely one of controlling a single drone; it is coordinating groups of drones that must collectively accomplish missions — each agent pursuing its assigned goal while sharing airspace with teammates and avoiding obstacles in a dynamic environment.

Deep reinforcement learning (DRL) has emerged as the dominant paradigm for training UAV navigation policies. Unlike classical path-planning algorithms such as A* and rapidly-exploring random trees (RRT), which require complete environment knowledge and fail when conditions change mid-flight, DRL agents learn adaptive policies through interaction with a simulated environment. When multiple agents must be coordinated simultaneously, multi-agent deep reinforcement learning (MARL) extends this framework, allowing groups of agents to develop cooperative behaviors through joint or decentralized training.

Despite rapid progress, the MARL literature on UAV coordination has developed along parallel tracks that have not been integrated. Work on dynamic target assignment has been developed separately from work on collision avoidance between drones in flight. Work on large-scale swarm coordination has been conducted in two-dimensional environments, while work on three-dimensional path planning has focused on single drones. This research addresses one specific intersection that no existing work has studied: the combination of real-time dynamic target assignment and conflict-aware collision avoidance in a three-dimensional multi-drone setting.

---

## 2.   Literature Review

The foundation of modern deep reinforcement learning was established by Mnih et al. [12], who demonstrated that a convolutional neural network trained with Q-learning could achieve human-level performance on Atari games directly from pixel inputs. Subsequent refinements addressed key instabilities: Van Hasselt et al. [13] introduced Double DQN to reduce systematic overestimation of action values; Wang et al. [14] proposed the Dueling Network architecture, which separately estimates state values and action advantages; and Schaul et al. [15] introduced Prioritized Experience Replay, which samples transitions in proportion to their temporal-difference error. These contributions form the basis of the Improved D3QN architecture used by Tang et al. [1] for single-UAV dynamic scene navigation.

Policy gradient methods provided an alternative naturally suited to continuous action spaces. Schulman et al. [16] proposed Proximal Policy Optimization (PPO), which constrains policy updates through a clipped surrogate objective, achieving training stability without trust-region complexity. Fujimoto et al. [18] developed Twin Delayed Deep Deterministic Policy Gradient (TD3), addressing overestimation in actor-critic methods through clipped double-Q learning and delayed updates. TD3 was adopted by Kong et al. [2] as the policy backbone for multi-UAV target assignment.

The extension to multi-agent settings introduced new coordination challenges. Lowe et al. [17] proposed MADDPG, a centralized-training decentralized-execution framework in which each agent's critic observes the full joint state during training but the actor relies only on local observations at execution time. Rashid et al. [19] introduced QMIX, which factorizes the joint action-value function subject to a monotonicity constraint. Yang et al. [20] applied mean-field theory to MARL, reducing computational complexity from quadratic to linear in the number of agents. Yu et al. [21] established that MAPPO — PPO with a shared critic — is surprisingly competitive with more complex MARL algorithms on cooperative benchmarks, motivating its use as the policy backbone in recent UAV coordination work [10].

Surveys have provided systematic overviews of progress in this domain. Govinda et al. [11] identified the absence of unified frameworks addressing both navigation efficiency and inter-agent coordination as a persistent limitation. Aggarwal and Kumar [23] highlighted DRL as the most promising direction for real-time adaptive UAV path planning. Gronauer and Diepold [25] identified scalability and partial observability as the two most persistent open challenges in multi-agent DRL.

For single-UAV navigation, Tang et al. [1] proposed an Improved D3QN achieving approximately 95% success rates in environments with moving threat zones, outperforming A* and RRT on path quality. Jarray et al. [3] introduced a dynamic reward function providing dense step-by-step feedback in a 25 km² 3D grid, achieving 98% success in low-obstacle conditions, substantially outperforming particle swarm and grey wolf optimization baselines.

Multi-UAV coordination introduced target assignment alongside path planning. Kong et al. [2] proposed TANet-TD3, performing target assignment and path planning simultaneously using Hungarian algorithm labels, evaluated on five drones in a 2D environment. Zhang et al. [4] scaled swarm coordination to 80–120 drones using PO-WMFDDPG, combining mean-field DDPG with multi-head attention, maintaining above 90% success at 120 drones where standard MARL baselines collapse.

The most directly relevant precursor is DA-MAPPO (Sheng et al. [10]), which embeds real-time Hungarian-algorithm-based assignments directly into each drone's observation vector, updated at every decision step. Its ablation study shows mission success drops from over 90% to exactly 0% when this assignment-augmented state is removed — establishing that this mechanism alone drives the framework's effectiveness. DA-MAPPO was evaluated on three drones in a 2D environment with static obstacles; its authors explicitly list 3D extension and larger swarm sizes as future work.

For collision avoidance, Rezaee et al. [9] proposed IGAT-MARL, replacing dense all-to-all interaction graphs with a sparse conflict-driven graph connecting only drone pairs predicted to be on a collision course within a defined time horizon. The framework achieves 17% higher reward, 10% fewer dangerous separation events, and 44% fewer interaction edges compared to the prior best baseline. Critically, IGAT-MARL has no target assignment component, and the authors list incorporating task allocation as a clear future direction.

Recent work has explored integrating large language models into UAV coordination. Xu et al. [6] proposed MRLMN using GPT-4o to reduce the cold-start problem in multi-hop UAV networking. Wang et al. [7] developed RALLY, using LLM semantic consensus to assign roles to drones before refining coordination through an RMIX network. Poudel and Moh [5] addressed heterogeneous drone fleets in disaster scenarios using MAML for rapid adaptation combined with resource-aware coalition formation. Khan et al. [8] provided a systematic comparison of LLM-based multi-agent frameworks.

Taken together, the literature reveals a consistent structural gap: the mechanisms that solve target assignment (DA-MAPPO) and collision avoidance (IGAT-MARL) have never been combined, and neither has been evaluated in three-dimensional space. Both papers document this gap in their own future work sections. No published work provides an empirical answer to whether these two mechanisms, when placed inside the same policy in 3D, cooperate or interfere with each other.

---

## 3.   Problem Statement

DA-MAPPO [10] and IGAT-MARL [9] are the two most advanced solutions to the sub-problems of dynamic target assignment and collision avoidance in multi-UAV coordination. DA-MAPPO demonstrated that its assignment-augmented observation is the sole mechanism driving performance (0% success without it), but tested only three drones in a 2D environment without an explicit collision-avoidance component. IGAT-MARL demonstrated that sparse conflict-driven interaction graphs improve collision avoidance at scale, but contains no target assignment. Both papers explicitly name the other's contribution as their next step, confirming that the gap is acknowledged and unresolved in the existing literature.

The specific problem addressed in this research arises in three-dimensional space: the assignment module sends each drone toward its target without awareness of which drone pairs are in active conflict states, while the conflict graph forces course deviations without awareness of current target assignments. In 2D, this interference is limited to the horizontal plane. In 3D, altitude introduces vertical collision trajectories — a drone assigned to a target directly above it may be on a collision course with another drone on the same vertical path — and the two mechanisms issue contradictory navigation commands. No existing work has placed these mechanisms in the same policy or tested whether the assignment-augmented observation that is critical in 2D remains effective when drones must simultaneously reason about altitude and collision avoidance.

**Research Question:** Can a single MAPPO policy, trained with both assignment-augmented observations and a conflict-aware interaction graph, achieve above 85% mission success for 5–8 UAVs navigating to dynamically assigned targets in a 3D environment — and do the two mechanisms reinforce or degrade each other?

---

## 4.   Research Objectives

1. To design a unified observation representation that encodes both the current Hungarian-algorithm-based target assignment and the current conflict-aware neighborhood for each drone in a 3D MAPPO policy.

2. To train and evaluate the proposed framework across swarm sizes of 3, 5, and 8 drones and assess whether performance degrades as the number of simultaneous assignment-conflict interactions increases.

3. To conduct controlled ablation experiments isolating the contribution of the assignment mechanism, the conflict graph, and the 3D extension — determining whether each component helps independently and whether they help more in combination.

4. To identify the failure boundary: the specific conditions of swarm size, obstacle density, and target movement speed under which the combined policy fails, and to characterize the nature of that failure.

---

## 5.   Research Methodology

The proposed research follows a quantitative, experimental methodology using multi-agent deep reinforcement learning in a controlled 3D simulation environment. The framework is built on MAPPO (Multi-Agent Proximal Policy Optimization), selected on the basis of its validated performance in the target assignment setting by DA-MAPPO and its known stability under partial observability.

### 5.1   Framework Design

Each drone's observation vector consists of four components: (1) its own 3D position and velocity; (2) the 3D relative position of its currently assigned target, derived from a minimum-cost Hungarian assignment computed at every decision step; (3) the positions and velocities of conflict neighbors only, determined by a dynamic conflict graph connecting drone pairs predicted to enter a collision threshold within a defined time horizon; and (4) obstacle proximity readings in six cardinal directions. Actions are continuous 3D velocity commands processed by a shared MAPPO actor-critic network with centralized training and decentralized execution.

### 5.2   Training Strategy

A four-stage curriculum is applied. Stage 1 replicates DA-MAPPO with 3 drones in 3D with static targets as a validation baseline. Stage 2 introduces 5 drones with moving targets and moderate obstacle density. Stage 3 scales to 8 drones with high obstacle density and dynamic targets. Stage 4 tests generalization across varied swarm sizes not seen during training.

### 5.3   Evaluation Measures

The primary metric is mission success rate: the fraction of episodes in which all drones reach their assigned targets without any inter-drone or obstacle collision within a fixed time limit. Secondary metrics include inter-drone collision count, obstacle collision count, number of target reassignments per episode, and average trajectory length per drone. Evaluation is conducted across three obstacle densities (30, 40, and 50 obstacles) and three swarm sizes (3, 5, and 8 drones).

**Four baselines:**
- Standard MAPPO — no assignment, no conflict graph
- DA-MAPPO ported to 3D — assignment only, no conflict graph
- IGAT-MARL with fixed assignment — conflict graph only, no dynamic reassignment
- Original DA-MAPPO (2D, 3 drones) — replication verification

### 5.4   Research Pipeline

**Table 2. Proposed Framework Pipeline**

| Step | Description |
|---|---|
| Input | 3D Environment — Drones, Dynamic Targets, Obstacles |
| Step 1 | Hungarian Assignment — minimum-cost, runs every decision step |
| Step 2 | Conflict Graph Update — connects only collision-predicted drone pairs |
| Step 3 | Combined Observation Vector — assignment state + conflict neighbors + obstacle proximity |
| Step 4 | MAPPO Policy — continuous 3D velocity commands |
| Output | Evaluation — Mission Success Rate, Collision Count, Trajectory Length |

---

## References

*(Font: Times New Roman, Size 11, Single spacing — IEEE format)*

[1]  J. Tang, Y. Liang, and K. Li, "Dynamic scene path planning of UAVs based on deep reinforcement learning," *Drones*, vol. 8, no. 2, p. 60, 2024.

[2]  X. Kong, Y. Zhou, Z. Li, and S. Wang, "Multi-UAV simultaneous target assignment and path planning based on deep reinforcement learning in dynamic multiple obstacles environments," *Front. Neurorobot.*, vol. 17, p. 1302898, 2024.

[3]  R. Jarray, I. Zaghbani, and S. Bouallègue, "Dynamic reward-based deep reinforcement learning algorithm for UAV path planning in large-scale environments," *Procedia Comput. Sci.*, vol. 270, pp. 692–702, 2025.

[4]  Y. Zhang et al., "Large-scale UAV swarm path planning based on mean-field reinforcement learning," *Chin. J. Aeronaut.*, vol. 38, no. 9, p. 103484, 2025.

[5]  S. Poudel and S. Moh, "MAML-integrated multi-agent reinforcement learning for adaptive coalition-based UAV coordination in disaster scenarios," *Internet of Things*, vol. 37, p. 101930, 2026.

[6]  Y. Xu et al., "Scalable UAV multi-hop networking via multi-agent reinforcement learning with large language models," arXiv:2505.08448, 2026.

[7]  Y. Wang et al., "RALLY: Role-adaptive LLM-driven yoked navigation for agentic UAV swarms," *IEEE Open J. Veh. Technol.*, vol. 6, 2025.

[8]  M. S. Khan, M. J. Khan, M. Sharif, and S. Yasmin, "Beyond single-framework architectures: A systematic evaluation and hybrid design for scalable multi-agent coordination," *IEEE Access*, vol. 14, 2026.

[9]  M. R. Rezaee, N. A. W. A. Hamid, M. Hussin, and Z. A. Zukarnain, "Efficient multi-agent deep reinforcement learning algorithm for multi UAV collision avoidance," *Appl. Soft Comput.*, vol. 197, p. 115145, 2026.

[10] Y. Sheng, X. Xie, H. Liu, and J. Li, "Dynamic target assignment and cooperative decision-making for UAV swarms based on multi-agent reinforcement learning," *IEEE Internet Things J.*, doi: 10.1109/JIOT.2026.3686066, 2026.

[11] S. Govinda, B. Brik, and S. Harous, "A survey on deep reinforcement learning applications in autonomous systems," *IEEE Trans. Intell. Transp. Syst.*, vol. 26, no. 7, 2025.

[12] V. Mnih et al., "Human-level control through deep reinforcement learning," *Nature*, vol. 518, pp. 529–533, 2015.

[13] H. Van Hasselt, A. Guez, and D. Silver, "Deep reinforcement learning with double Q-learning," in *Proc. AAAI*, 2016, pp. 2094–2100.

[14] Z. Wang et al., "Dueling network architectures for deep reinforcement learning," in *Proc. ICML*, 2016, pp. 1995–2003.

[15] T. Schaul, J. Quan, I. Antonoglou, and D. Silver, "Prioritized experience replay," in *Proc. ICLR*, 2016.

[16] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov, "Proximal policy optimization algorithms," arXiv:1707.06347, 2017.

[17] R. Lowe et al., "Multi-agent actor-critic for mixed cooperative-competitive environments," in *Proc. NeurIPS*, 2017, pp. 6379–6390.

[18] S. Fujimoto, H. Hoof, and D. Meger, "Addressing function approximation error in actor-critic methods," in *Proc. ICML*, 2018, pp. 1587–1596.

[19] T. Rashid et al., "QMIX: Monotonic value function factorisation for deep multi-agent reinforcement learning," in *Proc. ICML*, 2018, pp. 4295–4304.

[20] Y. Yang et al., "Mean field multi-agent reinforcement learning," in *Proc. ICML*, 2018, pp. 5571–5580.

[21] C. Yu et al., "The surprising effectiveness of PPO in cooperative multi-agent games," in *Proc. NeurIPS*, 2022.

[22] P. Sunehag et al., "Value-decomposition networks for cooperative multi-agent learning based on team reward," in *Proc. AAMAS*, 2018.

[23] S. Aggarwal and N. Kumar, "Path planning techniques for unmanned aerial vehicles: A review, solutions, and challenges," *Comput. Commun.*, vol. 149, pp. 270–299, 2020.

[24] F. A. Oliehoek and C. Amato, *A Concise Introduction to Decentralized POMDPs*. Springer, 2016.

[25] A. Gronauer and K. Diepold, "Multi-agent deep reinforcement learning: A survey," *Artif. Intell. Rev.*, vol. 55, pp. 895–943, 2022.

---

## Tentative Schedule

**Table 3. Tentative Research Schedule**

| Tasks | M 1–3 | M 4–6 | M 7–9 | M 10–11 | M 12–13 | M 14–18 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| Task-I: 3D environment setup + DA-MAPPO baseline replication | ● | | | | | |
| Task-II: Assignment obs + conflict graph integration into MAPPO | | ● | | | | |
| Task-III: Curriculum training (3 → 5 → 8 drones) | | | ● | | | |
| Task-IV: Evaluation vs. 4 baselines (3 sizes × 3 densities) | | | | ● | | |
| Task-V: Ablation experiments + failure case analysis | | | | | ● | |
| Task-VI: Thesis writing, revision, and submission | | | | | | ● |

---

## Details of Completed Coursework
*(or attach provisional transcript)*

**Table 4. Completed Coursework**

| # | Course Code and Title | Credit Hours | Grade / Semester |
|---|---|---|---|
| 1. | | | |
| 2. | | | |
| 3. | | | |
| 4. | | | |
| 5. | | | |
| 6. | | | |

---

### Formatting Guidelines (for Word submission)
- **Heading Level-1:** Times New Roman, Size 12, Bold
- **Heading Level-2:** Times New Roman, Size 11, Bold
- **Body text:** Times New Roman, Size 12, Line Spacing 1.5
- **References:** Times New Roman, Size 11, Single spacing
- **Table content:** Times New Roman, Size 10
- Table captions go **above** the table
- Figure captions go **below** the figure

---

*Ayesha Khalil  |  SP25-RCS-009  |  May 30, 2026*
