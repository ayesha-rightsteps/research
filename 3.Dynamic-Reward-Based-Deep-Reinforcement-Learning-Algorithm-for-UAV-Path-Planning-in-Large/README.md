# Ayesha's Research Handbook
### Paper: Dynamic Reward-Based Deep Reinforcement Learning Algorithm for UAV Path Planning in Large-Scale Environments

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

**Algorithm:** DQN (Deep Q-Network) with dynamic reward function d3/(d1+d2)

**Problem solved:** Single UAV path planning in large-scale 3D environments (up to 25 km, 40 obstacles) where Q-learning fails due to state space explosion and metaheuristics fail due to local optima.

**Three innovations:** (1) 3D grid state encoding + 3D CNN, (2) dynamic distance-based reward for dense feedback, (3) input normalization for training stability.

**Key result:** 85–98% success rate across 4 scenarios vs. 20–75% for metaheuristics; shortest paths and lowest STD in complex scenarios; only weakness is longer computational time (acceptable for offline pre-mission planning).

**Published:** Procedia Computer Science 270 (2025), KES 2025 Conference

---

*Generated from: `Dynamic-Reward-Based-Deep-Reinforcement-Learning-Algorithm-for-UAV-Path-Planning-in-Large.pdf`*
