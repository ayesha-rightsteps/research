# Related Work — Presentation Slides
## Only papers from the research folder | Logical narrative order

---

> **How to present this:**
> Sir ko puri table ek baar mein nahi padhni. Bolna hai:
> "Sir, I reviewed these papers. Let me walk you through the progression."
> Phir row by row story ki tarah sunao — survey se start karo, key papers pe highlight karo, aur gap close karo.

---

---

## SLIDE A — Related Work (Part 1 of 2)

**Heading:** Building Toward the Gap

| Authors | Contribution | Methodology | Dataset/Samples | Strength | Limitation |
|---|---|---|---|---|---|
| Govinda, Brik & Harous (2025) | Systematic review of DRL for UAV, robotics, transportation | Literature survey across published DRL studies | Published papers (no primary data) | Identifies lack of unified frameworks as the key open gap | Survey only — no new algorithm proposed |
| Tang, Liang & Li (2024) | Single UAV navigation in dynamic obstacle environments | Improved D3QN + Prioritized Experience Replay + heuristic action bias | Custom 2D sim, single UAV, moving obstacles | **95% success rate**, outperforms A* and RRT | Single drone only, 2D, discrete actions |
| Kong, Zhou, Li & Wang (2024) | Joint target assignment + path planning for multi-UAV | TANet-TD3 + Hungarian algorithm supervision + POMDP | Custom 2D sim, 5 UAVs, moving targets | First paper combining assignment + path planning | **2D only, no inter-drone collision avoidance** |
| Jarray, Zaghbani & Bouallègue (2025) | UAV path planning in large-scale 3D environments | DQN + 3D CNN + dynamic reward formula | Custom 3D sim, 25 km² area, 4 obstacle densities | **98% success in 3D**, beats PSO and GWO | Single drone, static obstacles only |

**What to say:**
> "Sir, the survey paper by Govinda et al. sets the stage — their key finding is that no framework combines navigation efficiency and inter-agent coordination. Tang et al. show that a single drone can navigate well in dynamic environments. Kong et al. take the next step — five drones with target assignment — but stay in 2D and have no collision avoidance between drones. Jarray et al. prove 3D is feasible for a single drone."

---

---

## SLIDE B — Related Work (Part 2 of 2)

**Heading:** The Two Key Papers — and What Comes After

| Authors | Contribution | Methodology | Dataset/Samples | Strength | Limitation |
|---|---|---|---|---|---|
| ⭐ **Rezaee et al. (2026) — IGAT-MARL** | Collision avoidance using sparse conflict-aware interaction graph | Conflict-driven sparse graph + Improved GAT (stacked attention + residual) + curriculum | BlueSky sim, 3–10 fixed-wing UAVs, conflict-guaranteed episodes | **44% fewer edges, 17% higher reward**, 10% fewer dangerous events | **No target assignment — drones have no goals** |
| ⭐ **Sheng et al. (2026) — DA-MAPPO** | Real-time dynamic target assignment embedded in drone observation | Hungarian algorithm at every step + MAPPO + 4-tier reward + curriculum | Custom sim, 3 UAVs, 3 dynamic targets, 30–50 static obstacles | **90–99% mission success**, robust to 50% packet loss and 6-step delay | **2D only, 3 drones only, no inter-drone collision avoidance** |
| Zhang et al. (2025) | Large-scale UAV swarm navigation with mean-field RL | Mean-field DDPG + multi-head attention + CTDE | Custom 2D sim, 20–120 UAVs, static obstacles | **>90% success at 120 drones** where baselines collapse | 2D only, static obstacles, homogeneous drones |
| Xu et al. (2026) — *MRLMN* | UAV multi-hop networking with LLM-guided MARL | GPT-4o knowledge distillation + IPPO + role-based reward decomposition | Custom sim, 12–24 UAVs, 150 ground users | **52% higher data rate**, 27% more user coverage | 2D only, GPT-4o dependency, no energy modeling |
| Wang et al. (2025) — *RALLY* | LLM-based role assignment for UAV swarm coordination | LLM semantic consensus + RMIX value mixing (Commander/Coordinator/Executor roles) | MPE sim, 8–11 drones, one adversary | Generalizes to unseen swarm sizes without retraining | 2D, 14-second inference latency, no real hardware |
| Poudel & Moh (2026) | Adaptive coalition formation for heterogeneous UAVs in disaster response | MAML meta-learning + MA-DDPG + resource-aware coalition formation | Custom disaster sim, 10–30 heterogeneous UAVs | Handles heterogeneous drones + drone failures + intermittent communication | 2D only, needs adaptation data, 10–30 drones only |

**What to say:**
> "Sir, these are the two key papers — references 9 and 10 — highlighted with stars. IGAT-MARL solves collision avoidance elegantly using a sparse graph: 44% fewer interaction edges, but no target assignment. DA-MAPPO solves assignment brilliantly: 90–99% success, but no collision avoidance and only in 2D with 3 drones. Both authors explicitly wrote that the other paper's problem is their future work. The remaining papers show that scaling to larger swarms is possible and that the field is moving toward more complex coordination — but the core gap remains. My research addresses that gap directly."

---

---

## THE GAP — ONE SLIDE (put this after Related Work)

**Heading:** What the Literature Has Not Done

```
                    TARGET ASSIGNMENT          COLLISION AVOIDANCE
                    ─────────────────          ──────────────────
DA-MAPPO [10]           ✅ Solved                   ❌ Missing
IGAT-MARL [9]           ❌ Missing                  ✅ Solved
All above papers        2D only                     2D only
─────────────────────────────────────────────────────────────────
THIS RESEARCH           ✅ Integrated               ✅ Integrated
                             in 3D, 5–8 drones
```

**What to say:**
> "Sir, this table says everything. DA-MAPPO has assignment but no avoidance. IGAT-MARL has avoidance but no assignment. Both are 2D. My research combines both in 3D. That is the contribution."

---

---

## SPEAKER NOTES FOR RELATED WORK Q&A

**If Sir asks why you didn't include more foundational papers (PPO, DQN etc.):**
> "Sir, the foundational algorithms like PPO and DQN are referenced in my synopsis — references 12 through 25. For the presentation I focused on the UAV-specific papers because those most directly motivate the research gap."

**If Sir asks about any specific paper:**

| Paper | 10-second answer |
|---|---|
| Govinda et al. [11] | "Survey paper Sir — their main finding is that no unified framework exists combining navigation and inter-agent coordination." |
| Tang et al. [1] | "Single drone, D3QN, 95% success in dynamic environments. Shows DRL works for UAV navigation." |
| Kong et al. [2] | "Five drones, assignment plus path planning together, but 2D and no collision avoidance between teammates." |
| Jarray et al. [3] | "Single drone in a large 3D environment — proves 3D UAV navigation with DRL is feasible." |
| IGAT-MARL [9] ⭐ | "Sparse conflict graph — 44% fewer interactions, 17% better reward. No target assignment. One of my two key papers." |
| DA-MAPPO [10] ⭐ | "Hungarian assignment in observation — 90% to 99% success. No collision avoidance. 2D only. My other key paper." |
| Zhang et al. [4] | "Scales to 120 drones using mean field theory. Impressive scale but 2D and static obstacles." |
| Xu et al. [6] | "Uses GPT-4o to initialize relay positions for UAV networking. LLM-guided MARL — different direction, focuses on communication not navigation." |
| Wang et al. [7] | "Uses LLMs to assign roles to drones. Different direction from my approach — semantic coordination rather than learned policy." |
| Poudel & Moh [5] | "Heterogeneous drones in disaster scenarios with meta-learning. Different focus — adaptation, not the assignment-avoidance gap." |
