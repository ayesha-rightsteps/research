# Synopsis Presentation — Ayesha Khalil
## Slide-by-Slide Guide with Speaker Notes
**CIIT/SP25-RCS-009/ATD | MS Computer Science | COMSATS Abbottabad**

---

---

## SLIDE 1 — Title Slide

**TITLE:**
Integrating Real-Time Target Assignment and Conflict-Aware Collision Avoidance for Multi-UAV Navigation in Three-Dimensional Environments Using Multi-Agent Reinforcement Learning

**SUBTITLE / DETAILS:**
- Presented by: Ayesha Khalil
- Registration No.: CIIT/SP25-RCS-009/ATD
- Supervisor: Dr. Faisal Rehman
- Co-Supervisor: Dr. Ehzaz Mustafa
- COMSATS University Islamabad, Abbottabad Campus
- Date: June 2026

> **Say:** "Good morning/afternoon, Sir. My name is Ayesha Khalil and today I will be presenting my synopsis titled [read title]. My supervisor is Dr. Faisal Rehman."

---

---

## SLIDE 2 — Agenda

**Outline:**
1. Introduction & Background
2. Problem Statement
3. Literature Review
4. Research Objectives
5. Proposed Methodology
6. Tentative Schedule
7. Conclusion

> **Say:** "Sir, I will take you through the background of the problem, what gap I identified in the literature, what I plan to do, and how I plan to do it."

---

---

## SLIDE 3 — Introduction: UAVs Today

**Heading:** From Military Tools to Everyday Use

**Bullet Points:**
- UAVs evolved from military applications to civilian and industrial use
- Key applications: disaster response, search & rescue, precision agriculture, infrastructure inspection, emergency communications
- A single drone is insufficient for large-scale missions
- Real tasks demand **multi-UAV teams** — coordinated, simultaneous coverage
- Hardware advances alone cannot solve coordination — it requires intelligent algorithms

**Visual suggestion:** Simple diagram — single drone on left, multi-drone swarm on right

> **Say:** "Sir, drones are no longer just military tools. They are used everywhere — from finding survivors in floods to inspecting power lines. But for any mission of real scale, one drone is not enough. You need a team of drones working together. And that coordination is where the hard problem begins."

---

---

## SLIDE 4 — Introduction: Why Coordination is Difficult

**Heading:** Classical Approaches Fail in Dynamic Environments

**Bullet Points:**
- Traditional solution: centralized planner computes optimal paths before deployment
- **Works for:** static, controlled environments
- **Fails when:** targets move, obstacles appear, or drones fail mid-mission
- Recomputing global solutions in real time is computationally intractable
- Need: drones that **learn** to coordinate, not drones that follow pre-written plans

> **Say:** "Sir, the old approach was to compute everything before the mission starts — like giving every drone a GPS route. But if a target moves, or a new obstacle appears, the plan breaks. There is no way to recompute in real time. So researchers moved toward learning-based methods."

---

---

## SLIDE 5 — Introduction: Deep Reinforcement Learning & MARL

**Heading:** The Dominant Paradigm — MARL

**Bullet Points:**
- **DRL:** Agent interacts with environment → receives rewards → improves policy through experience
- No need for an explicit model of the world
- **MARL (Multi-Agent RL):** extends DRL to teams — each drone learns to cooperate with others
- **CTDE Architecture:** Centralized Training, Decentralized Execution
  - Train with full team information
  - Execute independently using only local observations
- **MAPPO** (Multi-Agent PPO): proven stable, widely used baseline for cooperative UAV tasks

> **Say:** "Sir, the solution is to let drones learn by trial and error — deep reinforcement learning. Extended to multiple drones, this is called MARL. The standard approach trains drones together but lets each one act independently during deployment. MAPPO is the most reliable version of this and is what I will use as my policy backbone."

---

---

## SLIDE 6 — Introduction: The Gap in Existing Work

**Heading:** Progress Has Been Fragmented

**Bullet Points:**
- Researchers studying **target assignment** built methods without collision avoidance
- Researchers studying **collision avoidance** built methods without any goal/target structure
- All existing work tested in **2D environments only**
- Result: capable but **partial** solutions — each solves one piece, ignores the rest
- The two most advanced recent papers each explicitly cite the other's problem as their **own next step**

**Key fact:**
> DA-MAPPO [10]: "3D extension and collision avoidance are left as future work"
> IGAT-MARL [9]: "task allocation integration is a clear future direction"

> **Say:** "Sir, this is the core observation. The people working on target assignment did not consider collisions. The people working on collision avoidance did not consider targets. Both groups tested in 2D only. And when I read both papers, I found that each one literally points to the other's problem as their future work. No one has combined them. That is the gap."

---

---

## SLIDE 7 — Problem Statement

**Heading:** The Problem

**Problem Statement (3 lines — read exactly as written):**

Existing approaches to multi-UAV coordination treat dynamic target assignment and collision avoidance as separate problems, each developed and validated independently in two-dimensional environments.

When both mechanisms operate simultaneously in three-dimensional space, they generate competing navigation signals — the assignment directs each drone toward its target without awareness of active collision conflicts, while the collision avoidance module forces course corrections without awareness of current assignments, a tension that becomes structurally significant when vertical flight paths are introduced.

No existing framework has addressed this interference jointly in three-dimensional space, leaving it unknown whether a unified policy can sustain both assignment optimality and collision safety simultaneously, or whether the mechanisms degrade each other when combined.

> **Say:** "Sir, let me read the problem statement directly — [read it]. In simple terms: assignment says go left, avoidance says stop, and in 3D, with drones flying at different altitudes, this conflict becomes a structural problem. No one has tested what happens when both run together."

---

---

## SLIDE 8 — Literature Review: The Two Key Papers

**Heading:** Two Papers — Each Solving Half the Problem

| | DA-MAPPO [Sheng et al., 2026] | IGAT-MARL [Rezaee et al., 2026] |
|---|---|---|
| **Solves** | Dynamic target assignment | Collision avoidance |
| **How** | Hungarian algorithm at every step | Conflict-aware sparse interaction graph |
| **Key result** | 0% → 90% success with assignment info | 44% fewer interaction edges, 17% higher reward |
| **Environment** | 2D, 3 drones | 2D/3D (fixed-wing), 3–10 drones |
| **Missing** | No collision avoidance | No target assignment |
| **Future work (their own words)** | "3D extension + collision avoidance" | "Task allocation integration" |

> **Say:** "Sir, these are the two papers most directly related to my work. DA-MAPPO solves assignment beautifully — their ablation study shows that when you remove the assignment information, success drops from 90% to zero. IGAT-MARL shows that by only connecting drones that are predicted to collide — not all drones — you reduce unnecessary communication by 44%. Both are excellent. Both are incomplete. And they point to each other."

---

---

## SLIDE 9 — Literature Review: Broader Context

**Heading:** What the Rest of the Literature Shows

**Foundational algorithms used (building blocks):**
- **DQN** [Mnih, 2015] — first deep RL from pixels
- **PPO** [Schulman, 2017] — stable policy gradient, backbone of MAPPO
- **MADDPG** [Lowe, 2017] — first multi-agent actor-critic (CTDE)
- **MAPPO** [Yu, 2022] — PPO for cooperative MARL, outperforms more complex methods
- **QMIX** [Rashid, 2018] — value decomposition for cooperative tasks

**UAV-specific contributions:**
- Tang et al. [1]: D3QN single drone, 95% success in dynamic obstacles
- Kong et al. [2]: TANet-TD3, 5 drones, simultaneous assignment + path (2D only)
- Zhang et al. [4]: Mean-field MARL, scales to 120 drones (2D only)
- Jarray et al. [3]: 3D UAV navigation with dynamic reward (single drone)

**Summary from surveys:**
- Govinda et al. [11]: "lack of unified frameworks combining navigation and inter-agent coordination is the key open gap"

> **Say:** "Sir, I reviewed 25 papers in total. The foundational algorithms like PPO and MAPPO are well established. For UAVs specifically, Kong et al. came closest — they did assignment and path planning together, but in 2D with only 5 drones. No paper, including the surveys, has combined assignment and collision avoidance in 3D."

---

---

## SLIDE 10 — Research Objectives

**Heading:** What This Research Will Do

1. **Design a unified observation vector** that encodes both the Hungarian-algorithm-based assignment state and the conflict-aware neighborhood for each drone in a 3D MAPPO policy

2. **Test scalability** — evaluate the framework on swarm sizes of 3, 5, and 8 drones to check if performance degrades as simultaneous assignment-conflict interactions increase

3. **Run controlled ablation experiments** — isolate the contribution of the conflict graph, the assignment mechanism, and the 3D extension separately, then together

4. **Find the failure boundary** — identify the exact conditions (swarm size, obstacle density, target speed) under which the unified policy fails, and characterize how it fails

> **Say:** "Sir, I have four objectives. First, build the combined representation. Second, test it at different swarm sizes. Third, run ablations to see what each component contributes. Fourth, find where the framework breaks — because knowing the limits is as important as knowing the successes."

---

---

## SLIDE 11 — Proposed Methodology: Framework Design

**Heading:** How the Framework Works

**Each drone's observation vector includes 4 components:**

| Component | What it encodes |
|---|---|
| 1. Own state | 3D position + velocity of the drone |
| 2. Assignment state | Relative 3D position of current target (from Hungarian algorithm, updated every step) |
| 3. Conflict neighbors | Positions + velocities of only those drones predicted to collide within a time horizon |
| 4. Obstacle proximity | Distance readings in 6 cardinal directions (±x, ±y, ±z) |

**Policy:** MAPPO — centralized critic during training, decentralized actor during execution

**Actions:** Continuous 3D velocity commands

> **Say:** "Sir, the key design decision is what each drone is allowed to see. The drone knows its own position, where its current target is — updated every step using the Hungarian algorithm — which teammates it is likely to collide with — not all teammates, just the dangerous ones — and how close obstacles are in all six directions. This is what goes into the policy. The MAPPO architecture trains all drones together but each drone acts on its own."

---

---

## SLIDE 12 — Proposed Methodology: Framework Pipeline

**Heading:** Pipeline — Step by Step

```
[3D Environment]
   Drones (5–8) + Dynamic Targets + Obstacles
         |
         v
[Step 1: Hungarian Assignment]
   Minimum-cost assignment computed at every decision step
   → Each drone gets a target
         |
         v
[Step 2: Conflict Graph Update]
   Only drone pairs predicted to collide within time horizon are connected
   → Each drone gets its conflict neighborhood
         |
         v
[Step 3: Combined Observation Vector]
   Own state + Assignment state + Conflict neighbors + Obstacle proximity
         |
         v
[MAPPO Policy]
   Centralized critic (training) | Decentralized actor (execution)
         |
         v
[Output: Continuous 3D velocity commands]
         |
         v
[Evaluation]
   Mission success rate | Collision count | Trajectory length
```

> **Say:** "Sir, here is the pipeline. Every decision step, two things happen simultaneously: the Hungarian algorithm updates target assignments, and the conflict graph updates which drone pairs are at risk. Both feed into each drone's observation. The MAPPO policy processes this and outputs a 3D velocity command. This repeats until all drones reach their targets or the episode ends."

---

---

## SLIDE 13 — Proposed Methodology: Training Strategy

**Heading:** Curriculum Training — 4 Stages

| Stage | Drones | Targets | Obstacles | Goal |
|---|---|---|---|---|
| Stage 1 | 3 | Static | Low density | Replicate DA-MAPPO baseline in 3D |
| Stage 2 | 5 | Moving | Medium density | Test assignment + avoidance together |
| Stage 3 | 8 | Moving | High density (50) | Full challenge — curriculum peak |
| Stage 4 | Unseen sizes | Moving | Various | Generalization test |

**Why curriculum?**
- Both DA-MAPPO and IGAT-MARL used curriculum — it works
- Prevents policy collapse when starting with full complexity
- Stage 1 also serves as replication verification

> **Say:** "Sir, I will not train directly on the hardest scenario. I will start with 3 drones and easy conditions — this also verifies I have correctly replicated DA-MAPPO. Then I progressively increase difficulty. By Stage 3, we have 8 drones, moving targets, and 50 obstacles. This curriculum approach is validated by both key papers."

---

---

## SLIDE 14 — Proposed Methodology: Evaluation Plan

**Heading:** How I Will Measure Success

**Primary Metric:**
- Mission success rate — all drones reach assigned targets, no collisions, within time limit

**Secondary Metrics:**
- Inter-drone collision count
- Obstacle collision count
- Target reassignments per episode
- Average trajectory length per drone

**Test Conditions:**
- Swarm sizes: 3, 5, 8 drones
- Obstacle densities: 30, 40, 50 obstacles
- 4 Baselines:

| Baseline | Description |
|---|---|
| B1: Standard MAPPO | No assignment, no conflict graph |
| B2: DA-MAPPO in 3D | Assignment only, no conflict graph |
| B3: IGAT-MARL + fixed assignment | Conflict graph only, no real-time assignment |
| B4: Original DA-MAPPO (2D) | Replication verification |

**Tools:** PyBullet (simulation) + PyTorch (training) — both free and open source

> **Say:** "Sir, I will test my framework against four baselines. This is rigorous — I am not just comparing to a single method but isolating each component individually. If my unified framework beats all four baselines, it confirms both mechanisms work better together than apart."

---

---

## SLIDE 15 — Tentative Schedule

**Heading:** 12-Month Research Plan

| Task | M 1–2 | M 3–4 | M 5–7 | M 8–9 | M 10–11 | M 12 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| Task I: 3D environment setup + DA-MAPPO baseline replication | ● | | | | | |
| Task II: Assignment obs + conflict graph integration | | ● | | | | |
| Task III: Curriculum training (3 → 5 → 8 drones) | | | ● | | | |
| Task IV: Evaluation vs. 4 baselines | | | | ● | | |
| Task V: Ablation experiments + failure analysis | | | | | ● | |
| Task VI: Thesis writing + revision + submission | | | | | | ● |

> **Say:** "Sir, the total duration is 12 months. I start by replicating the existing work to confirm I have the right environment. Then I build and integrate. Evaluation runs in months 8–9. The final two months are for ablations, failure analysis, and writing. This is a realistic timeline."

---

---

## SLIDE 16 — Why This Research Matters

**Heading:** Contribution to the Field

**What this research contributes:**
- First empirical test of combining real-time assignment and conflict-aware avoidance in a single policy in **3D space**
- First result answering: do these two mechanisms cooperate or compete when combined?
- Framework scalable from 3 to 8 drones with curriculum-validated training
- 4-baseline ablation provides clean, interpretable evidence of each component's contribution

**Real-world impact:**
- Search & rescue drones that navigate to survivors while avoiding mid-air collisions
- Delivery swarms that reassign routes dynamically without crashing into each other
- Any multi-UAV mission in 3D that requires both coordination and safety

**The research gap in one sentence:**
> Both mechanisms were built independently, both work in 2D, and both authors said the other's problem is their future work — this research is that future work.

> **Say:** "Sir, to summarize the contribution: the two best papers on assignment and on collision avoidance each said the other's problem is their future work. I am doing that future work. I will find out, for the first time, whether these two mechanisms help or hurt each other in 3D. That answer does not exist in the literature."

---

---

## SLIDE 17 — Thank You / Q&A

**Heading:** Thank You

**On slide:**
- Title (short version): Multi-UAV Navigation using MARL — Integrating Assignment and Collision Avoidance in 3D
- Ayesha Khalil | CIIT/SP25-RCS-009/ATD
- Supervisor: Dr. Faisal Rehman
- "Open for questions"

---

---

# ANTICIPATED QUESTIONS & MODEL ANSWERS

---

**Q: What is the main contribution of this paper?**
> "Sir, the main contribution is combining two mechanisms that have never been combined before — real-time target assignment from DA-MAPPO and conflict-aware collision avoidance from IGAT-MARL — in a single unified MAPPO policy that operates in 3D. No existing paper has done this. Both original authors pointed to this as their future work."

---

**Q: What is the Hungarian algorithm and why are you using it?**
> "Sir, the Hungarian algorithm is a classical optimization method that finds the minimum-cost assignment between a set of agents and a set of tasks. In my framework, at every decision step, it assigns each drone to the target that minimizes total travel cost for the whole swarm. DA-MAPPO showed that including this real-time assignment in the observation vector caused success rate to jump from 0% to 90%. That is why I use it."

---

**Q: What is the conflict graph?**
> "Sir, instead of giving each drone information about all other drones — which is expensive and noisy — the conflict graph only connects drone pairs that are predicted to be on a collision course within a certain time window. IGAT-MARL showed this reduced unnecessary interaction edges by 44% while maintaining avoidance performance. I use the same sparse graph in my framework."

---

**Q: What is MAPPO?**
> "Sir, MAPPO is Multi-Agent Proximal Policy Optimization. It is an extension of PPO — a stable policy gradient algorithm — to multi-agent settings. During training, each drone's critic has access to the full team's state, which improves coordination. During deployment, each drone acts only on its own local observation. Yu et al. showed in 2022 that MAPPO is surprisingly competitive with much more complex methods on cooperative tasks."

---

**Q: Why 3D? What is different about 3D compared to 2D?**
> "Sir, in 2D, all drones fly on the same horizontal plane. The collision graph and the assignment only need to consider movement in x and y. In 3D, drones at different altitudes can be on a vertical collision course that simply does not exist in 2D. The conflict graph must now account for 6 directions of movement. The assignment must consider 3D distances. The competition between these two mechanisms becomes structurally more complex when altitude is added. This is why 3D is a meaningful step beyond prior work."

---

**Q: What are your baselines and why those four?**
> "Sir, I have four baselines. First, standard MAPPO with no special mechanisms — this is the floor. Second, DA-MAPPO ported to 3D but without a conflict graph — this isolates the value of the conflict graph. Third, IGAT-MARL with a fixed assignment — this isolates the value of real-time reassignment. Fourth, the original 2D DA-MAPPO — this verifies I have replicated the baseline correctly. Together, these four baselines let me separate the contribution of each component."

---

**Q: What are the limitations of your proposed work?**
> "Sir, I see three limitations. First, I am using simulation only — PyBullet does not capture all real-world aerodynamics. Second, my drones are homogeneous — they all have the same speed and sensor range. Real swarms are often heterogeneous. Third, I assume perfect communication — in real deployments, packet loss and delay would affect both the assignment updates and the conflict graph. DA-MAPPO tested robustness to 50% packet loss and 6-step delay, which gives me confidence, but I should replicate those tests too."

---

**Q: What would you change if you could redesign this?**
> "Sir, I would extend to heterogeneous drones earlier — the current framework assumes all drones are identical. In real missions, you often have faster drones for scouting and slower drones for carrying payloads. The Hungarian assignment would need to account for drone capability differences, not just distance. That is the most interesting extension I can see."

---

**Q: Do you expect the two mechanisms to cooperate or compete?**
> "Sir, my honest expectation is that they will initially compete during training — because the assignment is trying to move drones efficiently while the conflict graph is trying to slow them down or reroute them. But through curriculum training, I expect the policy to learn to balance both. The interesting finding will be whether the success rate with both mechanisms together is higher, lower, or the same as each mechanism alone. That is what no one knows yet."

---

**Q: Why MAPPO and not QMIX or MADDPG?**
> "Sir, MAPPO was chosen because Yu et al. showed in 2022 that it is surprisingly competitive with QMIX despite being much simpler. DA-MAPPO also uses MAPPO and achieved 90–99% success, which validates it as a strong backbone. MADDPG requires continuous actions and a larger critic input that grows with team size, which makes it harder to scale to 8 drones. MAPPO's simplicity also means the ablation experiments will be cleaner — changes in performance are more clearly attributable to the observation design, not the algorithm itself."

---

---

# QUICK REFERENCE — KEY NUMBERS TO REMEMBER

| Fact | Number |
|---|---|
| DA-MAPPO success without assignment | 0% |
| DA-MAPPO success with assignment | 90–99% |
| IGAT-MARL reduction in interaction edges | 44% |
| IGAT-MARL reward improvement | 17% |
| My swarm sizes | 3, 5, 8 drones |
| My obstacle densities | 30, 40, 50 obstacles |
| Number of baselines | 4 |
| Total papers reviewed | 25 |
| Papers from last 3 years (2023–2026) | 11 (44%) |
| Timeline | 12 months |

---

*Ayesha — tum yeh kar sakti ho. Sir ko batao ke yeh idea tumhara nahi hai, yeh papers ka hi kaha hua tha. Tum woh kaam kar rahi ho jo researchers ne khud chhoda tha.*
