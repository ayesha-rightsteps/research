# Related Work — Speaking Script
## Exactly what to say for Slides 6 and 7

---

# SLIDE 6 — Related Work (first table)

**Opening line — say this before pointing at any row:**

> "Sir, I reviewed eleven papers directly relevant to this research. Let me walk you through them in order — starting from the big picture, then narrowing down to the specific gap my work addresses."

---

**Row 1 — Govinda, Brik & Harous (2025)**

> "The first paper is a survey by Govinda et al. — they reviewed all DRL-based work across UAVs, robotics, and transportation. Their key finding — and this directly motivates my research — is that no existing framework combines navigation efficiency with inter-agent coordination. The gap I am targeting was identified by a survey paper first."

---

**Row 2 — Tang, Liang & Li (2024)**

> "Tang et al. showed that a single drone can navigate dynamic environments very well — 95% success rate using an improved DQN with prioritized experience replay. This establishes that deep reinforcement learning works for UAV navigation. But it is a single drone, in 2D."

---

**Row 3 — Kong, Zhou, Li & Wang (2024)**

> "Kong et al. took the next step — they combined target assignment and path planning for five drones together using TD3 and Hungarian algorithm supervision. This is the closest earlier work to mine. But it is 2D only and has no mechanism for drones to avoid crashing into each other."

---

**Row 4 — Jarray, Zaghbani & Bouallègue (2025)**

> "Jarray et al. proved that deep RL works in a genuine 3D large-scale environment — 98% success across 25 square kilometers. But again, single drone only, static obstacles. The 3D extension works for one drone — my research extends it to a team."

---

**Transition to Slide 7:**

> "Sir, these four papers show the progression — from single drone navigation to multi-drone coordination — but all in 2D and none with both assignment and collision avoidance together. The next slide has the two papers that most directly motivate my research."

---
---

# SLIDE 7 — Related Work Cont. (second table)

**Opening — draw attention to the first two rows:**

> "Sir, I want to highlight the first two rows of this table. These are the two papers my research builds directly on."

---

**Row 1 — Rezaee et al. (2026) — IGAT-MARL ⭐**

> "IGAT-MARL by Rezaee et al. solves inter-drone collision avoidance very elegantly. Instead of giving every drone information about all other drones, they build a sparse graph — only connecting pairs of drones that are predicted to collide within a time window. This gave 44% fewer interaction edges and 17% higher reward compared to the previous best. The key limitation: the drones have no targets. They only avoid each other — there is no assignment, no goal, no mission to complete."

---

**Row 2 — Sheng et al. (2026) — DA-MAPPO ⭐**

> "DA-MAPPO by Sheng et al. solves target assignment. They embed the output of the Hungarian algorithm — which computes the minimum-cost assignment — directly into each drone's observation at every single step. Their ablation study showed that when this assignment information is removed, mission success drops from 90% to zero. That one result tells us how critical the mechanism is. The limitation: no collision avoidance between drones, only 3 drones tested, and only in 2D."

---

**The key point — say this clearly:**

> "Sir, both papers wrote in their future work sections that the other paper's problem is their next step. IGAT-MARL said task allocation is a clear future direction. DA-MAPPO said 3D extension and collision avoidance are left as future work. My research is exactly that future work — combining both in a unified policy in 3D."

---

**Row 3 — Zhang et al. (2025)**

> "Zhang et al. showed that mean-field theory can scale multi-UAV RL to 120 drones with over 90% success. This proves scalability is achievable — but again, 2D only and no collision avoidance between drones."

---

**Row 4 — Xu et al. (2026) — MRLMN**

> "Xu et al. used GPT-4o to guide UAV networking — not navigation. They distill LLM knowledge into a MARL policy for relay positioning. 52% higher data rate. A different direction from mine — their focus is communication, not coordinated navigation."

---

**Closing line for the related work section:**

> "Sir, taken together, these papers show a clear pattern — excellent progress on individual sub-problems, always in 2D, always in isolation. No paper has combined dynamic target assignment and conflict-aware collision avoidance in a 3D environment. That is the gap this research addresses."

---
---

# IF SIR ASKS ABOUT ANY SPECIFIC PAPER

**"What is IGAT-MARL?"**
> "Sir, IGAT stands for Improved Graph Attention — MARL for multi-agent reinforcement learning. It uses a conflict graph that only connects drone pairs on predicted collision courses, and an improved attention network to process this graph. 44% fewer interactions, 17% better reward — but no target assignment."

**"What is DA-MAPPO?"**
> "Sir, DA stands for Dynamic Assignment. It embeds the Hungarian algorithm's output — which drone should go to which target — directly into each drone's observation at every decision step. MAPPO is the policy backbone. Without the assignment in the observation, success drops from 90% to 0% — proven by their own ablation."

**"What is the Hungarian algorithm?"**
> "Sir, it is a classical optimization method that finds the minimum-cost pairing between two sets — in our case, between drones and targets. It minimizes total travel distance for the whole team. It is fast enough to run at every decision step."

**"Why did you choose these specific papers?"**
> "Sir, because these are the two most advanced recent solutions to the two sub-problems I am combining — one for assignment, one for avoidance — and both explicitly identify the other's problem as their own future work. The choice was natural."

**"What if Sir asks about Wang et al. / RALLY?"**
> "Sir, RALLY uses large language models to assign command, coordinator, and executor roles to drones. It is an interesting direction but fundamentally different from mine — it relies on LLM inference at decision time which has 14-second latency, and it is 2D only. My approach is a learned end-to-end policy with no LLM dependency at execution."
