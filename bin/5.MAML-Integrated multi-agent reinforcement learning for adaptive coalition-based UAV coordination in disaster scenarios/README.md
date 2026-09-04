# Ayesha's Research Handbook
### Paper: MAML-Integrated Multi-Agent Reinforcement Learning for Adaptive Coalition-Based UAV Coordination in Disaster Scenarios

---

## Reading Guide

| # | File | Purpose | Est. Time |
|---|------|---------|-----------|
| 0 | `00_START_HERE.md` | Orientation — read this first | 2 min |
| 1 | `01_summary.md` | Full paper overview | 8 min |
| 2 | `02_concepts.md` | All key terms explained | 10 min |
| 3 | `03_methodology.md` | How the research was done | 10 min |
| 4 | `04_results.md` | What they found | 7 min |
| 5 | `05_critical_analysis.md` | Strengths & limitations | 5 min |
| 6 | `06_presentation.md` | Your presentation script + Q&A | 10 min |
| 7 | `07_cheat_sheet.md` | One-page reference | 1 min |

---

**Recommended path if time is short:** `00` → `07` → `06` → done.

---

## Quick Paper Summary

**Framework:** RCTP (Resource-aware Coalition-based Task and Path-planning)

**Algorithm:** MAML + MA-DDPG + suitability-score coalition formation

**Problem solved:** Heterogeneous UAV swarm coordination in disaster scenarios — handling mixed drone types, mid-mission failures, intermittent LoS/NLoS communication, dynamic obstacles, and unseen environments, all in one framework.

**Three key innovations:** (1) MAML meta-training for rapid adaptation to new disaster environments with just a few gradient steps, (2) resource-aware suitability scores for coalition formation matching drone capabilities to task requirements, (3) automatic coalition reformation when drones fail — no central controller needed.

**Key results:** 30–40% faster mission completion; 10–20% lower energy; robust under multiple simultaneous drone failures; millisecond inference per agent; 10–30 UAVs tested.

**Why it's relevant to your research:** Directly addresses your teacher's questions about **scalability** (coalition-based approach as an alternative to mean-field) and **heterogeneous drones** (the only paper in this folder that models different drone types).

**Published:** Internet of Things (Elsevier), Vol. 37, Article 101930 (2026)

---

**Note:** This handbook was generated from the paper's abstract (ScienceDirect HTML page). Full-text access would provide additional experimental details, specific figures, and exact hyperparameter tables.

---

*Generated from: `MAML-Integrated multi-agent reinforcement learning for adaptive coalition-based UAV coordination in disaster scenarios .html`*
