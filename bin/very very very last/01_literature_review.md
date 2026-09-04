# Literature Review — Detailed Script
### Slide 6 k leay — yeh parh k bolna

---

## Slide pe aanay say pehlay ek line bolna:

> "Sir, I will now briefly walk through the related work. I have organized these papers into three groups — UAV path planning, multi-agent coordination, and the two most closely related papers."

---

## GROUP 1 — UAV Path Planning

### [1] Tang et al. 2024 — Improved D3QN
> "Tang et al. worked on single UAV navigation in dynamic environments. They used an improved version of Double Dueling DQN with Prioritized Experience Replay. Their UAV successfully navigates around moving obstacles with about 95% success rate. But this is a single drone — no coordination with other drones, no target assignment."

### [2] Kong et al. 2024 — TANet-TD3
> "Kong et al. tackled a more complex problem — multiple UAVs must both find their targets and plan their paths at the same time. They used TD3 as the policy and the Hungarian algorithm to supervise target assignment. This is close to our work but still missing collision avoidance between drones."

### [3] Jarray et al. 2025 — Dynamic Reward DQN
> "Jarray et al. proposed a dynamic reward function for UAV path planning in large environments. Their reward changes based on distance ratio at each step. They achieve 98% success in low-obstacle environments. However, again this is a single UAV — no multi-agent setting."

### [4] Zhang et al. 2025 — Mean-Field DDPG
> "Zhang et al. scaled up to 80-120 drones using mean-field theory, which reduces the complexity of multi-agent interaction from quadratic to linear. They achieve above 90% success rate even at 120 drones. But there is no collision avoidance mechanism and no dynamic target assignment."

### [5] Poudel & Moh 2026 — MAML-MARL
> "Poudel and Moh addressed disaster scenarios with heterogeneous drone fleets. They use MAML — Model Agnostic Meta Learning — to help drones adapt quickly to new environments. The focus is on coalition formation. But again, no explicit target assignment or collision avoidance mechanism."

---

## GROUP 2 — Most Related Work

### [9] Rezaee et al. 2026 — IGAT-MARL
> "Sir, this is one of our two base papers. Rezaee et al. introduced a sparse conflict-driven graph for collision avoidance. Instead of connecting all drones to each other — which is expensive — they only connect drone pairs that are predicted to collide within a certain time window. They use an Improved Graph Attention Network to process this sparse graph. Results: 44% fewer interaction edges, 17% higher reward, 10% fewer dangerous separation events compared to prior methods. The key limitation — and the authors explicitly state this — is that there is no target assignment. Drones just avoid each other with no goal structure."

### [10] Sheng et al. 2026 — DA-MAPPO
> "Sir, this is our second base paper. Sheng et al. introduced real-time Hungarian algorithm-based target assignment directly into each drone's observation. At every decision step, the Hungarian algorithm computes the optimal assignment — which drone should go to which target — and this information is given to each drone as part of what it observes. The ablation study is very revealing — when they remove the assignment information, mission success drops from 90% to 0%. This confirms that the assignment mechanism is the key contribution. The limitation — also explicitly stated by the authors — is that there is no collision avoidance mechanism other than a simple penalty reward."

---

## Yeh line zaroor bolna at the end:

> "Sir, what is interesting is that DA-MAPPO explicitly mentions collision avoidance as future work, and IGAT-MARL explicitly mentions target assignment as future work. These two papers each solve one half of the same problem and point to each other's contribution as what needs to be done next. My research is that next step — solving both together in a single unified policy."

---

## Agar Sir Sawaal Poochhein Literature Review Par:

**Q: Why did you select these specific papers?**
> "Sir, these papers represent the full landscape of the problem. Papers [1] to [5] show the evolution from single UAV path planning to multi-UAV coordination. Papers [9] and [10] are the most directly related — they are the two most advanced recent papers that each solve one side of our research problem."

**Q: What about LLM-based approaches?**
> "Sir, there are recent papers using GPT-4o and LLMs for UAV coordination — like Xu et al. and Wang et al. However, those papers focus on networking and role assignment — not on the specific coupling between trajectory optimization and collision avoidance. They are not directly comparable to our work."
