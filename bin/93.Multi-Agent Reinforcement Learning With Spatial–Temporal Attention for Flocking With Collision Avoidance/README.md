# Ayesha's Research Handbook
### Paper: Multi-Agent Reinforcement Learning With Spatial–Temporal Attention for Flocking With Collision Avoidance of a Scalable Fixed-Wing UAV Fleet

**Authors:** Chao Yan, Chang Wang, Han Zhou, Xiaojia Xiang, Xiangke Wang, Lincheng Shen
**Published:** IEEE Transactions on Intelligent Transportation Systems, Vol. 26, No. 2, February 2025

---

## Reading Guide

| # | File | Purpose | Est. Time |
|---|------|---------|-----------|
| 0 | `00_START_HERE.md` | Orientation — read this first to know what you're dealing with | 2 min |
| 1 | `01_summary.md` | Full paper overview — problem, solution, results, contribution | 8 min |
| 2 | `02_concepts.md` | Every term, acronym, and algorithm explained clearly | 12 min |
| 3 | `03_methodology.md` | Exactly what they built and how they tested it, step by step | 10 min |
| 4 | `04_results.md` | What they found, every figure explained, real-world meaning | 8 min |
| 5 | `05_critical_analysis.md` | Strengths, hidden limitations, missing experiments — impress sir | 5 min |
| 6 | `06_presentation.md` | Word-for-word script + full Q&A table | 10 min |
| 7 | `07_cheat_sheet.md` | One-page quick reference — keep open while presenting | 1 min |

---

## Recommended Paths

**If you have 10 minutes:**
`00_START_HERE.md` → `07_cheat_sheet.md`

**If you have 30 minutes:**
`00_START_HERE.md` → `07_cheat_sheet.md` → `06_presentation.md` → `02_concepts.md`

**If you have 1 hour:**
Read all files in order: `00` → `01` → `02` → `03` → `04` → `05` → `06` → `07`

---

## Key Paper Facts at a Glance

| Item | Detail |
|------|--------|
| Core algorithm | STAAC (Spatial-Temporal Attention Multi-Agent Actor-Critic) |
| Problem type | Distributed flocking + collision avoidance for scalable fixed-wing UAV fleets |
| Key innovation | Population-invariant network with Local Spatial Attention + Global Temporal Attention |
| Training setup | 10 followers, 15 intruders, 1200m x 800m simulation, 5000 episodes, ~4 hours |
| Best result | 0.34% collision rate in n10m20 scenario — 22.73% better than next-best (HAMA) |
| HITL result | Zero collisions, 5 followers + 3 intruders, 100 seconds, 1.5 ms inference time |
| Baselines beaten | MADDPG, MATD3, HAMA, API-MADDPG, BCDDPG, LSTM-DDQN, APF, ORCA |
| Venue | IEEE Trans. Intelligent Transportation Systems, Feb 2025 |

---

*Generated from:* `Multi-Agent-Reinforcement-Learning-With-Spatial-Temporal-Attention-for-Flocking-With-Collision-Avoidance-of-a-Scalable-Fixed-Wing-UAV-Fleet.pdf`
