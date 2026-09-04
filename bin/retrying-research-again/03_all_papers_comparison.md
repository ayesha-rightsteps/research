# All Papers — Complete Comparison Table
### Sab papers ek jagah — accurate, paper se verified

---

## Master Comparison Table

| # | Paper | Year | Journal/Venue | Problem | Agents | Assignment | Avoidance | Dynamic Obj. Weight | Algorithm | Key Result |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | DA-MAPPO (Sheng et al.) | 2026 | IEEE IoT Journal | Dynamic target assignment + cooperative navigation | Multi (swarm) | ✅ Dynamic | Partial (penalty only) | ❌ Fixed | MAPPO + min-cost allocation | 90–99% mission success |
| 2 | IGAT-MARL (Rezaee et al.) | 2026 | Applied Soft Computing | Multi-UAV collision avoidance | Multi | ❌ | ✅ GAT-based | ❌ Fixed | MARL + Graph Attention | 17% higher reward, 10% fewer separation violations |
| 3 | HPER-D3QN (Shen et al.) | 2026 | Defence Technology | Single-UAV avoidance in joint airspace | Single | ❌ | ✅ DTPA + HPER | ❌ Fixed | D3QN + hierarchical replay | 96.28% success at 25 aircraft |
| 4 | STAAC (Yan et al.) | 2025 | IEEE TITS | Flocking + avoidance for scalable fixed-wing fleet | Multi | ❌ (flocking) | ✅ LSA + GTA | ❌ Fixed | MADDPG + spatial-temporal attention | 0.34% collision @ n10m20, 1.5ms HITL |
| 5 | Kong et al. | 2024 | Frontiers Neurorobot. | Multi-UAV simultaneous assignment + path planning | Multi | ✅ Static targets | ✅ Basic (3D) | ❌ Fixed | TD3 + assignment network | Collision-free in 3D dynamic obstacles |
| 6 | Zhang et al. (Mean Field) | 2025 | Chinese J. Aeronautics | Large-scale UAV swarm path planning | Multi (large) | ❌ | Partial (NFZ only) | ❌ Fixed | PO-WMFDDPG (Mean Field) | Higher task success vs DDPG baseline |
| 7 | Tang et al. | 2024 | Drones (MDPI) | Single-UAV path planning in dynamic scenes | Single | ❌ | Obstacle only | ❌ Fixed | D3QN + PER + heuristic | Better real-time performance |
| 8 | Xu et al. (MRLMN) | 2024 | IEEE (preprint) | UAV multi-hop networking (communication) | Multi | ❌ (routing) | ❌ | ❌ | MARL + LLM + Hungarian | Better network coverage vs MAPPO |
| 9 | RALLY (Wang et al.) | 2025 | IEEE OJ-VT | LLM-driven UAV swarm navigation + coverage | Multi | Partial (roles) | Obstacle only | ❌ | LLM + MARL hybrid | Better coverage + generalization |
| 10 | Beyond Single Framework | 2026 | IEEE Access | LLM framework comparison (CrewAI/AutoGen/LangChain) | Multi (LLM) | Task designation | ❌ | ❌ | Hybrid LangGraph-CrewAI | 96.1% success, 76.2% token reduction |
| 11 | Govinda et al. (Survey) | 2025 | IEEE TITS | Survey: DRL in autonomous systems | N/A (survey) | N/A | N/A | N/A | Survey | Identifies gaps in multi-objective drone coordination |
| **Proposed** | **Priority Arbitration (Ayesha)** | **2026** | **MS Thesis → Journal** | **Joint assignment + avoidance with learned priority** | **Multi (5–8)** | **✅** | **✅** | **✅ LEARNED α** | **MAPPO + Arbitration Head** | **TBD** |

---

## Papers Directly Relevant to Research (Top 4)

### 1. DA-MAPPO — Why It Is a Baseline

**What it does:** Dynamic target assignment to UAV swarms using MAPPO. Integrates real-time minimum-cost allocation into the observation. Has a "hierarchical cooperative reward" that includes collision avoidance.

**Why it is NOT a complete solution:**
- Collision avoidance is a penalty term — not a sophisticated mechanism
- Both assignment and avoidance components use fixed reward coefficients
- Paper's own statement: "existing methods decouple target assignment and path planning into hand-engineered pipelines" — they tried to couple them but with fixed weights

**Role in our research:** Primary baseline for target assignment. Our approach should outperform it in combined assignment+avoidance scenarios.

---

### 2. IGAT-MARL — Why It Is a Baseline

**What it does:** Multi-agent collision avoidance using Graph Attention Network. Curriculum learning for scalability. Continuous action space.

**Why it is NOT a complete solution:**
- Zero target assignment — assumes drones already have navigation targets
- Future work statement: "accounting for additional dynamic and static impediments" — no mention of assignment
- Graph attention only for collision conflict modeling — no temporal context, no objective balancing

**Role in our research:** Primary baseline for collision avoidance. Our approach should handle both simultaneously while IGAT-MARL handles only avoidance.

---

### 3. HPER-D3QN — Why It Supports Our Gap Claim

**What it does:** Single-UAV collision avoidance in joint airspace (manned + unmanned + wind). DTPA for multi-dimensional threat scoring. HPER for intelligent experience stratification.

**Key relevance:**
- DTPA uses TCPA and DCPA as inputs — these directly parallel our time-to-collision input to the arbitration head
- HPER proves that priority-based mechanisms improve performance — validates our concept at a higher level
- Reward: C_goal=+2, C_collision=-1, C_warning=-0.5 — ALL FIXED — confirms the gap

**Role in our research:** Supporting literature — not a baseline (different task), but validates inputs and philosophy.

---

### 4. STAAC — Why It Supports Our Gap Claim

**What it does:** Multi-agent scalable fixed-wing UAV flocking + collision avoidance. LSA for spatial entity attention. GTA for temporal attention over 4 frames.

**Key relevance:**
- HITL validation at 1.5ms proves RL-based mechanisms are real-time feasible
- Population-invariant architecture proves per-agent mechanisms scale
- Reward: P1, P2, w1, w2 all fixed tuning parameters — confirms the gap
- Flocking objective vs avoidance objective — same structural conflict as assignment vs avoidance

**Role in our research:** Supporting literature — validates scalability and computational feasibility of our approach.

---

## The Gap — Visualized Across All Papers

```
                    ASSIGNMENT    AVOIDANCE    DYNAMIC BALANCE
                    ──────────    ─────────    ───────────────
DA-MAPPO              ✅            Partial          ❌
IGAT-MARL             ❌            ✅               ❌
HPER-D3QN             ❌            ✅               ❌
STAAC                 ❌            ✅               ❌
Kong et al.           ✅            Basic            ❌
Zhang et al.          ❌            Partial          ❌
Tang et al.           ❌            Obstacle         ❌
────────────────────────────────────────────────────────────
PROPOSED              ✅            ✅               ✅ ← NOVEL
```

**No paper occupies the bottom row except the proposed work.**

---

## Papers NOT Directly Relevant (But In Literature)

| Paper | Why Included | Why Not Core |
|---|---|---|
| Tang et al. (2024) | DRL for UAV path planning — background | Single agent, no assignment, no inter-agent avoidance |
| Xu et al. MRLMN | MARL + LLM for UAV networking | Communication networking problem, not navigation/avoidance |
| RALLY (2025) | LLM + MARL for UAV swarm | Coverage task, LLM-based, not comparable approach |
| Beyond Single Framework | LLM framework comparison | Not a UAV navigation paper at all |
| Govinda Survey | Background on DRL in autonomous systems | Survey — identifies gaps but does not propose solutions |

---

## What The Survey Paper (Govinda et al., 2025) Says

Published in IEEE TITS, July 2025. Specifically identifies as a gap in the drone section:

> Multi-objective coordination in drone swarms remains an open problem — existing approaches handle navigation, collision avoidance, and task allocation as separate modules, and unified frameworks that dynamically balance competing objectives are lacking.

**Yeh directly hamari research gap ko validate karta hai — ek survey paper se, 2025 mein.**

---

## Summary Table for Sir

| Aspect | Existing Best | Proposed Work |
|---|---|---|
| Target assignment method | DA-MAPPO (2026) — dynamic, MAPPO-based | Same backbone (MAPPO) |
| Collision avoidance method | IGAT-MARL (2026) — GAT-based, multi-agent | Same setting |
| Threat scoring | HPER-D3QN (2026) — DTPA, time+distance | TTC input to arbitration head |
| Fleet scalability | STAAC (2025) — population-invariant, 1.5ms | Per-agent, parameter sharing |
| **Objective balancing** | **None — all use fixed coefficients** | **Learned α — NOVEL** |

