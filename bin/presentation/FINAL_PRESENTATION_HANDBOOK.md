# FINAL PRESENTATION HANDBOOK — Ayesha Khalil
## Har slide ka script + har term ki explanation + poora Q&A
### MS Synopsis | COMSATS Abbottabad | June 2026

---

> **Kal subha ek baar seedha padhna — upar se neeche tak.**
> Presentation ke dauran yeh file open rakhna phone ya laptop pe.
> Har slide ka script yahan hai — word for word.

---

# PART 1 — POORI STORY EK JAGAH

**Yeh 3 lines yaad kar lo — baaki sab isi se nikalta hai:**

> Drones ek team mein kaam karte hain. Team mein do problems hain — kaunsa drone kaunse target pe jaaye (assignment), aur drones ek doosre se takraayein nahi (collision avoidance). Dono problems alag alag solve hui hain, alag alag papers mein, sirf 2D mein. Mere research mein dono ko pehli baar saath 3D mein combine karta hoon.

---

# PART 2 — HAR SLIDE KA SCRIPT

---

## SLIDE 1 — Title

**Slide pe kya hai:**
Dynamic Target Assignment and Collision Avoidance for Multi-UAV Coordination in 3D using MARL
Ayesha Khalil | CIIT/SP25-RCS-009/ATD
Supervisor: Dr. Faisal Rehman | Co-supervisor: Dr. Ehzaz Mustafa

**Exactly yeh bolo:**
> "Good morning Sir. My name is Ayesha Khalil, registration number CIIT/SP25-RCS-009/ATD. Today I am presenting my synopsis on Dynamic Target Assignment and Collision Avoidance for Multi-UAV Coordination in 3D using Multi-Agent Reinforcement Learning. My supervisor is Dr. Faisal Rehman."

---

## SLIDE 2 — Introduction: UAVs

**Slide pe kya hai:**
- From military applications to civilian and industrial use
- A single drone is insufficient
- Real tasks demand multi-UAV teams
- Hardware advances alone cannot solve coordination — it requires intelligent algorithm

**Exactly yeh bolo:**
> "Sir, drones have moved far beyond military use. Today they are deployed in disaster response, search and rescue, agriculture, infrastructure inspection, and logistics. But for any mission of real scale — covering a large area, finding multiple survivors, inspecting a long pipeline — a single drone is simply not enough. You need a team of drones working together simultaneously. And this is where the challenge begins — coordinating a team of drones is not a hardware problem. The drones exist. The sensors exist. What is missing is the intelligent algorithm that tells each drone what to do, when, and how — without crashing into each other."

---

## SLIDE 3 — Introduction Cont: Multi-UAV Coordination

**Slide pe kya hai:**
- Classical Approach — Centralized Planner:
  - Computes globally optimal solution before deployment
  - ❌ Fails when targets move or obstacles appear mid-mission
  - ❌ Recomputing in real time is computationally intractable
- Learning-Based Approach:
  - Drones learn cooperative behavior through trial and error

**Exactly yeh bolo:**
> "Sir, the traditional approach to coordinating drones is called centralized planning. Before the mission starts, a central computer calculates the perfect route for every drone. This works well in a lab — when everything is static and predictable. But in the real world, targets move. New obstacles appear. A drone might fail mid-mission. When that happens, the pre-computed plan breaks — and recomputing the entire plan in real time is computationally impossible for a large team. This is why researchers moved to learning-based methods. Instead of programming rules, we let drones learn how to cooperate by practicing thousands of times in simulation — exactly like how a human learns to ride a bike, not by reading a manual, but by trying and failing until the skill is built."

---

## SLIDE 4 — Introduction Cont: DRL & MARL

**Slide pe kya hai:**
- DRL: Agent interacts with environment → receives rewards → improves policy through experience
- MARL: Extends DRL to teams
- CTDE Architecture: Centralized Training, Decentralized Execution
- MAPPO: proven stable, widely used baseline for cooperative UAV tasks

**Exactly yeh bolo:**
> "Sir, the specific learning approach used is called Deep Reinforcement Learning — DRL. A drone interacts with a simulated environment, takes actions, receives a reward if the action was good and nothing if it was bad, and gradually learns which actions lead to mission success. Extended to a team of drones, this becomes Multi-Agent Reinforcement Learning — MARL. The architecture we use is called CTDE — Centralized Training, Decentralized Execution. During training in simulation, every drone can see all information from all teammates — this makes learning faster and more coordinated. But during the actual mission, each drone acts only on what it can observe locally — it does not need to communicate with a central server. This makes the system robust and practical. The specific algorithm I use is MAPPO — Multi-Agent Proximal Policy Optimization — which has been proven in research to be stable and highly effective for cooperative drone tasks."

---

## SLIDE 5 — Motivation

**Slide pe kya hai:**
- DA-MAPPO: 90–99% mission success with Hungarian assignment — but no collision avoidance
- IGAT-MARL: 44% fewer interaction edges — but no target assignment
- Ablation: removing assignment → 90% drops to 0%
- Both papers cite each other as future work
- Research statement: unified MAPPO framework for 5–8 drones in 3D

**Exactly yeh bolo:**
> "Sir, let me give you the specific evidence that motivated this research. The first paper — DA-MAPPO by Sheng et al. 2026 — achieves 90 to 99 percent mission success for drone target assignment using something called the Hungarian algorithm embedded in each drone's observation. But it has zero collision avoidance between drones, only 3 drones were tested, and it was only in 2D.

> The second paper — IGAT-MARL by Rezaee et al. 2026 — solves inter-drone collision avoidance very efficiently by using a sparse graph that only connects drones predicted to collide. This reduces interaction edges by 44 percent and improves reward by 17 percent. But it has no target assignment at all — drones just avoid each other with no mission goal.

> Here is the critical finding from DA-MAPPO's own experiments: when they removed the assignment information from the drone's observation — everything else kept the same — mission success dropped from 90 percent to zero. That single result tells us how essential the assignment mechanism is.

> Most importantly, Sir — both papers, in their own future work sections, explicitly wrote that the other paper's problem is what they plan to solve next. DA-MAPPO said collision avoidance and 3D extension are left as future work. IGAT-MARL said task allocation integration is a clear future direction. My research is exactly that future work — combining both in a unified 3D framework."

---

## SLIDE 6 — Related Work (Table 1)

**Papers in this slide:**
1. Govinda et al. (2025) — Survey
2. Tang et al. (2024) — D3QN single drone
3. Kong et al. (2024) — TANet-TD3
4. Jarray et al. (2025) — 3D DRL single drone

**Exactly yeh bolo:**
> "Sir, I reviewed eight papers directly relevant to this research. Let me walk you through them in order, building toward the gap my work addresses.

> The first paper, by Govinda et al., is a survey of DRL across UAV systems. Their key conclusion is that no existing framework combines navigation efficiency with inter-agent coordination — the exact gap this research targets.

> Tang et al. showed that a single drone can navigate dynamic environments with 95 percent success using an improved DQN. This establishes that deep RL works for drones — but it is a single drone in 2D.

> Kong et al. took the next step — five drones with joint target assignment and path planning using TD3 and Hungarian algorithm supervision. This is the closest earlier work to mine — but it is 2D only and has no mechanism for drones to avoid colliding with each other.

> Jarray et al. proved that deep RL works in a genuine 3D environment — 98 percent success across 25 square kilometers. But again, single drone only, static obstacles."

---

## SLIDE 7 — Related Work Cont (Table 2)

**Papers in this slide:**
1. Rezaee et al. (2026) — IGAT-MARL ⭐
2. Sheng et al. (2026) — DA-MAPPO ⭐
3. Zhang et al. (2025) — Mean-field MARL
4. Xu et al. (2026) — MRLMN

**Exactly yeh bolo:**
> "Sir, the first two rows of this table are the papers that directly motivate my research — I have highlighted them.

> IGAT-MARL by Rezaee et al. solves inter-drone collision avoidance using a sparse conflict graph — only connecting pairs of drones that are predicted to collide within a time window. This gives 44 percent fewer interaction edges, 17 percent higher reward, 10 percent fewer dangerous events. The limitation: drones have no targets — there is no assignment, no mission, just avoidance.

> DA-MAPPO by Sheng et al. solves target assignment — the Hungarian algorithm runs at every decision step and its output is placed directly into each drone's observation. 90 to 99 percent mission success, robust even to 50 percent communication packet loss. The limitation: no collision avoidance between drones, only 3 drones, only 2D.

> Zhang et al. showed that mean-field theory can scale multi-drone RL to 120 drones with over 90 percent success — proving scalability is achievable, but again in 2D with static obstacles.

> Xu et al. used GPT-4o to guide drone networking — a different direction, focused on communication not navigation, achieving 52 percent higher data rate."

---

## SLIDE 8 — Gap in Existing Work

**Slide pe kya hai:**
- Researchers studying target assignment built methods without collision avoidance
- Researchers studying collision avoidance built methods without any goal/target structure
- All existing work tested in 2D environments only
- Result: capable but partial solutions
- Both most advanced papers cite each other as their own next step

**Exactly yeh bolo:**
> "Sir, this slide summarizes the core gap. Every researcher working on target assignment ignored collision avoidance. Every researcher working on collision avoidance had no target structure. Both groups worked only in 2D. The result is a collection of strong but incomplete solutions — each solving one piece of the problem while assuming the other piece is either trivial or solved somewhere else.

> And the clearest evidence of this gap is the fact that the two most advanced papers — IGAT-MARL and DA-MAPPO — each wrote in their own future work that the other's problem is what they plan to do next. That is not a coincidence. That is a documented gap waiting to be filled. My research fills it."

---

## SLIDE 9 — Problem Statement

**Slide pe kya hai:** (3 paragraphs — read them exactly)

**Exactly yeh bolo — slowly, clearly, one paragraph at a time:**

> "Sir, let me read the problem statement.

> [FIRST PARAGRAPH] Existing approaches to multi-UAV coordination treat dynamic target assignment and collision avoidance as separate problems, each developed and validated independently in two-dimensional environments.

> [SECOND PARAGRAPH] When both mechanisms operate simultaneously in three-dimensional space, they generate competing navigation signals — the assignment directs each drone toward its target without awareness of active collision conflicts, while the collision avoidance module forces course corrections without awareness of current assignments, a tension that becomes structurally significant when vertical flight paths are introduced.

> [THIRD PARAGRAPH] The result is a fundamental tension in three-dimensional multi-UAV deployment: goal-directed navigation and inter-agent collision avoidance pull each drone in opposing directions, and whether a unified policy can hold both objectives in balance — or whether one systematically undermines the other — has not been established."

**Baad mein add karo:**
> "In simple terms Sir — in 3D, when assignment says fly toward your target and avoidance says move away from a drone in your path, these two instructions pull the drone in opposite directions. What happens when both run together in 3D? Nobody knows yet. That is the problem."

---

## SLIDE 10 — Research Objectives

**Slide pe kya hai:**
1. Design a unified observation vector encoding Hungarian assignment state + conflict-aware neighborhood in 3D MAPPO
2. Test scalability across swarm sizes of 3, 5, and 8 drones
3. Find the failure boundary — conditions where the unified policy fails

**Exactly yeh bolo:**
> "Sir, I have three research objectives.

> First — I will design a unified observation vector that encodes both the assignment state, from the Hungarian algorithm, and the conflict neighborhood, from the sparse graph, together in a single input to the MAPPO policy. This combined design is the core engineering contribution — no previous paper has done this.

> Second — I will test the framework at three different swarm sizes: 3 drones, 5 drones, and 8 drones. The question is whether performance degrades as more drones are added and assignment-conflict interactions become more frequent and complex.

> Third — and Sir this is one most researchers skip — I will systematically find the failure boundary. What swarm size, obstacle density, and target speed causes the framework to fail? And how exactly does it fail — does it collide more, or does it miss targets, or both? Knowing the limits of a system is as important as knowing its strengths."

---

## SLIDE 11 — Proposed Methodology

**Slide pe kya hai:**
Each drone's observation includes 4 components (table with 4 rows)

**Exactly yeh bolo:**
> "Sir, the proposed framework is built on MAPPO. The key design decision is what each drone is allowed to observe at each moment — the observation vector.

> I designed four components. First, the drone's own state — its current 3D position and velocity. Second, the assignment state — the relative 3D position of the drone's current assigned target, computed by the Hungarian algorithm at every single decision step, not just at the start. Third, the conflict neighborhood — the positions and velocities of only those drones that the conflict graph predicts will collide with this drone within a time window. Not all drones — only the dangerous ones. Fourth, obstacle proximity — distance readings in all six directions: up, down, left, right, forward, backward.

> All four components go into one vector. That vector is the input to the MAPPO neural network. The network outputs a continuous 3D velocity command — which direction and how fast to fly. All training happens in PyBullet simulation using PyTorch. No real hardware needed.

> Sir, the combination of components 2 and 3 together in one observation is what has never been done before. Assignment state and conflict neighborhood in the same input — this is what allows the policy to potentially balance both objectives."

---

## SLIDE 12 — Training Strategy

**Slide pe kya hai:** Curriculum training (4 stages)

**Exactly yeh bolo:**
> "Sir, I use curriculum training — starting with an easy version of the problem and progressively increasing difficulty. This prevents the policy from giving up early when the full problem is too complex.

> Stage 1: 3 drones, static targets, low obstacles. This also serves as my verification that I have correctly replicated the DA-MAPPO baseline.

> Stage 2: 5 drones, moving targets, medium obstacle density. This is where assignment and avoidance first operate together.

> Stage 3: 8 drones, moving targets, 50 obstacles. The full challenge.

> Stage 4: Testing on swarm sizes the policy has never seen during training — to check generalization.

> Both DA-MAPPO and IGAT-MARL used curriculum training and validated that it works. I follow the same approach, which gives confidence in the training design."

---

## SLIDE 13 — References

**Exactly yeh bolo:**
> "Sir, these are the eight references for this presentation. The two most critical ones are reference 5 — Rezaee et al., IGAT-MARL — and reference 6 — Sheng et al., DA-MAPPO — which are the papers that directly motivate this research. All references are from 2024 to 2026, reflecting the most current state of the field."

---

## SLIDE 14 — Thank You

**Exactly yeh bolo:**
> "Thank you, Sir. I am open for questions."

---

# PART 3 — HAR TERM KI SIMPLE EXPLANATION

---

### UAV
Drone. Flying machine without a human pilot. In this research: a team of 5–8 drones flying together in 3D simulation.

---

### Multi-UAV / Swarm
A team of drones working on the same mission together. One drone covers a small area — a team covers a large mission simultaneously.

---

### 3D Environment
Drones can fly up, down, left, right, forward, backward. All previous papers only used 2D (no altitude). In 3D, a drone above you moving downward is on a collision course — this vertical conflict does not exist in 2D. This is why 3D is a harder and more realistic problem.

---

### Dynamic Target Assignment
Each drone gets a target to fly to. "Dynamic" means the assignment is recalculated at every step — not fixed at the start. If Drone 1 is closer to Target B and Drone 2 is closer to Target A, they should swap. The Hungarian algorithm does this automatically.

---

### Hungarian Algorithm
A mathematical method that finds the minimum-cost pairing between two groups. In our case: pairs each drone with a target to minimize total travel distance for the whole team. Fast enough to run at every decision step. DA-MAPPO proved that embedding its output in the observation causes success to jump from 0% to 90%.

---

### Collision Avoidance
Preventing drones from crashing into each other or into obstacles. Two types: drone-to-drone collision, and drone-to-obstacle collision. IGAT-MARL solved drone-to-drone collision avoidance using a sparse conflict graph.

---

### Competing Navigation Signals
The core problem. Assignment says "fly toward your target." Avoidance says "move away from that drone in your path." In 3D, these two instructions conflict more frequently because of vertical flight paths. Can a single policy learn to balance both? That is the research question.

---

### Deep Reinforcement Learning (DRL)
Teaching a computer to make decisions by letting it try things, get rewards for good actions, and learn from experience — like training a dog. No rules are programmed. The system learns by practicing thousands of times in simulation.

---

### Policy
The drone's "brain." Takes current observation as input, outputs an action. Training the policy means finding the best decision function through experience.

---

### Reward Function
A score given after each action. Good action → positive reward. Bad action → negative reward. DA-MAPPO uses a 4-tier reward: big positive for reaching target, big negative for collision, small negative for each step (encourages efficiency), small positive for moving closer to target.

---

### MARL — Multi-Agent Reinforcement Learning
DRL for a team of agents (drones) sharing the same environment. Each drone has its own policy, but their actions affect each other. Harder than single-agent RL because the environment changes as all agents learn simultaneously.

---

### CTDE — Centralized Training, Decentralized Execution
During training in simulation: every drone's critic sees all teammates' full information → stable, fast learning. During the real mission: each drone acts only on its own local observation → no central server needed, robust to communication failures.

**Simple analogy:** Like a football team — they practice together with a coach watching everyone (centralized training), but during the match each player makes their own decisions in real time (decentralized execution).

---

### PPO — Proximal Policy Optimization
The training algorithm. Updates the policy step by step, but with a safety rule: do not change the policy too drastically in one update. Prevents unstable training. Like learning to ride a bike — small adjustments each time, not huge overcorrections.

---

### MAPPO — Multi-Agent PPO
PPO applied to multiple cooperating agents. Uses a shared centralized critic during training. Yu et al. 2022 showed it is competitive with much more complex algorithms. DA-MAPPO used MAPPO and achieved 90–99% success.

---

### Observation Vector
Everything a drone knows at one moment. Input to the policy network. In my framework: 4 components — own state + assignment state + conflict neighbors + obstacle proximity. The combination of all four in one vector is the key design contribution.

---

### Conflict Graph (Sparse Graph)
Instead of connecting every drone pair (which is noisy and expensive), only connect pairs predicted to collide within a time window. For 8 drones, there are 28 possible pairs — but at any moment maybe only 3–4 are at risk. IGAT-MARL showed this sparse approach reduces interaction edges by 44% without losing avoidance performance.

---

### Graph Attention Network (GAT)
A neural network that processes graph-structured data. Each drone pays "attention" to its connected conflict neighbors, weighting information by how dangerous the neighbor is. IGAT-MARL improved the standard version with stacked double-attention and residual connections.

---

### Curriculum Training
Start with easy problem, progressively increase difficulty. Prevents policy collapse. Like teaching math — basic arithmetic before algebra before calculus. Both DA-MAPPO and IGAT-MARL validated this approach.

---

### Ablation Study
Remove one component at a time, measure the effect. DA-MAPPO removed assignment from observation → 90% to 0%. This proved assignment information is critical. My ablation will isolate conflict graph, assignment mechanism, and 3D extension separately.

---

### Baseline
A comparison method. Instead of just saying "my method is good," prove it by comparing against known methods. My 4 baselines: standard MAPPO (no mechanisms), DA-MAPPO in 3D (assignment only), IGAT-MARL + fixed assignment (avoidance only), original 2D DA-MAPPO (replication check).

---

### DA-MAPPO (Key Paper 1)
Sheng et al. 2026. Solves dynamic target assignment. Hungarian algorithm at every step → embedded in observation → MAPPO policy. 90–99% mission success. Ablation: without assignment in observation, success drops to 0%. Limitation: no collision avoidance, 3 drones only, 2D only. Future work: "3D and collision avoidance."

---

### IGAT-MARL (Key Paper 2)
Rezaee et al. 2026. Solves inter-drone collision avoidance. Sparse conflict graph connects only collision-risk pairs → Improved GAT processes it. 44% fewer interaction edges, 17% higher reward. Limitation: no target assignment, drones have no goals. Future work: "task allocation integration."

---

### Mission Success Rate
Primary metric. Of all episodes run, what percentage did the entire team complete successfully — all drones reached targets, zero collisions, within the time limit. DA-MAPPO achieved 90–99% on this.

---

### PyBullet
Free, open-source physics simulator. Used to simulate drone flight — gravity, collision detection, velocity. All training happens here. No real drones needed.

---

### PyTorch
Free, open-source deep learning library. Used to build and train the neural network policy. Standard tool in all DRL research.

---

# PART 4 — ANTICIPATED Q&A

---

**Q: What is the main contribution?**
> "Sir, the main contribution is combining two mechanisms that have never been combined before — DA-MAPPO's real-time Hungarian assignment and IGAT-MARL's conflict-aware collision avoidance — in a single unified MAPPO policy in 3D. Both papers documented this as their own future work. My research provides the first empirical answer to whether these mechanisms cooperate or compete when combined."

---

**Q: What is the Hungarian algorithm?**
> "Sir, the Hungarian algorithm finds the minimum-cost pairing between two sets — in our case, between drones and targets, to minimize total travel distance. It is fast enough to run at every decision step. DA-MAPPO showed that including its output in the drone's observation causes success to jump from 0% to 90%."

---

**Q: What is the conflict graph? Why sparse?**
> "Sir, the conflict graph connects only drone pairs predicted to come within a dangerous distance within a time window. It is sparse because in a team of 8 drones, there are 28 possible pairs, but at any moment only 3–4 might be on collision courses. Connecting only those 3–4 gives a clean signal and reduces computation by 44%."

---

**Q: Why MAPPO and not QMIX or MADDPG?**
> "Sir, three reasons. First, DA-MAPPO — which I build on — already uses MAPPO and achieved 90–99% success. Second, Yu et al. 2022 showed MAPPO is competitive with QMIX despite being simpler. Third, MADDPG's critic input grows with team size — for 8 drones it becomes very large. MAPPO's simplicity also makes ablation results cleaner."

---

**Q: Why 3D? What changes in 3D?**
> "Sir, in 2D all drones fly at the same height — there are no vertical collision paths. In 3D, a drone directly above you moving downward is on a collision course that simply cannot exist in 2D. The conflict graph must handle 6 directions instead of 4. The assignment must use 3D distances. The competition between assignment and avoidance becomes more frequent and complex. This is why 3D is a meaningful, non-trivial extension."

---

**Q: What are your baselines?**
> "Sir, four baselines. B1 is standard MAPPO with no special mechanisms — this establishes the floor. B2 is DA-MAPPO ported to 3D without the conflict graph — isolates the value of the conflict graph. B3 is IGAT-MARL with a fixed assignment — isolates the value of real-time reassignment. B4 is the original 2D DA-MAPPO — verifies my environment replication is correct."

---

**Q: What are the limitations?**
> "Sir, three main limitations. First, simulation only — PyBullet does not capture all real-world aerodynamics. Second, homogeneous drones — all drones have the same speed and sensor range, real swarms are often mixed. Third, I assume reasonably reliable communication — real environments have packet loss and delay."

---

**Q: Do you expect the mechanisms to cooperate or compete?**
> "Sir, my expectation is they will initially compete during training — assignment routes drones toward targets while avoidance forces detours. But through curriculum training, I expect the policy to learn to anticipate conflicts and route proactively. The interesting result will be whether the combined system beats each mechanism individually — nobody knows the answer yet."

---

**Q: What would you change if you redesigned this?**
> "Sir, I would extend to heterogeneous drones — different speeds and payloads. The Hungarian assignment would then need to account for drone capability, not just distance. That is the most natural next step after establishing baseline results with homogeneous drones."

---

**Q: How is this different from Kong et al. TANet-TD3?**
> "Sir, Kong et al. also combined assignment and path planning for 5 drones — but three key differences. First, it is 2D only. Second, there is no inter-drone collision avoidance — drones only avoid static obstacles. Third, the assignment is a separate pre-computed network, not embedded in the observation at every step. My framework integrates both mechanisms inside a single unified observation vector in 3D."

---

# PART 5 — NUMBERS TO MEMORIZE

| Number | What it means |
|---|---|
| **0% → 90%** | DA-MAPPO ablation — without vs with assignment in observation |
| **90–99%** | DA-MAPPO overall mission success range |
| **44%** | IGAT-MARL reduction in interaction edges |
| **17%** | IGAT-MARL reward improvement |
| **3 drones** | DA-MAPPO was tested on this many |
| **3, 5, 8** | Swarm sizes I will test |
| **4** | Components in my observation vector |
| **4** | Number of baselines |
| **4** | Curriculum training stages |
| **8** | Papers in reference list |
| **14** | Total slides in presentation |
| **12 months** | Research timeline |

---

# PART 6 — RECOVERY LINES (agar bhool jaao)

> "Sir, the exact figure is in the paper — but the key point is..."
> "Sir, let me refer to the slide — the important takeaway here is..."
> "Sir, I would need to verify that exact number, but what I can say is..."
> "Sir, that is a great question — the paper specifically addresses this by..."

**Kabhi mat bolo:** "I don't know."
**Hamesha bolo:** "Sir, the key point is..." — phir jo yaad hai woh bolo.

---

*Ayesha — tum ne yeh sab khud kiya hai. Slides tumhari hain. Research tumhara hai. Script sirf reminder hai — asli kaam tumhara tha.*
*Kal acha jayega. All the best.*
