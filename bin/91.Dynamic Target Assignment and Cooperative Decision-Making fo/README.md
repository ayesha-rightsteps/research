# Ayesha's Research Handbook
### Paper: Dynamic Target Assignment and Cooperative Decision-Making for UAV Swarms Based on Multi-Agent Reinforcement Learning

**Authors:** Yuanyuan Sheng, Xianan Xie, Huanyu Liu, Junbao Li
**Venue:** IEEE Internet of Things Journal, 2026
**DOI:** 10.1109/JIOT.2026.3686066

---

## Reading Guide

| # | File | Purpose | Est. Time |
|---|------|---------|-----------|
| 0 | `00_START_HERE.md` | Orientation — read this first | 2 min |
| 1 | `01_summary.md` | Full paper overview — problem, solution, results | 8 min |
| 2 | `02_concepts.md` | All key terms explained with analogies | 10 min |
| 3 | `03_methodology.md` | Exactly how the research was done, step by step | 10 min |
| 4 | `04_results.md` | What they found, every table explained | 7 min |
| 5 | `05_critical_analysis.md` | Strengths, limitations, missing experiments | 5 min |
| 6 | `06_presentation.md` | Your complete presentation script + Q&A answers | 10 min |
| 7 | `07_cheat_sheet.md` | One-page reference — keep this open while presenting | 1 min |

---

## Recommended path if time is short

`00_START_HERE.md` → `07_cheat_sheet.md` → `06_presentation.md` → done.

---

## The Paper in Three Sentences

UAV swarms need to reach multiple moving targets in cluttered environments, but existing methods break when targets move because they solve target assignment separately from navigation. DA-MAPPO fixes this by running a Hungarian assignment algorithm at every decision step and feeding the result directly into each drone's observation, so the navigation policy is always conditioned on a current (not outdated) assignment. In high-fidelity simulation, this achieves 90–99% mission success in dynamic environments, outperforming all baselines by up to 25 percentage points, with near-zero degradation when switching from static to dynamic targets.

---

## Key Numbers to Remember

| Scenario | DA-MAPPO | Best Baseline | Advantage |
|---|---|---|---|
| Dynamic, 30 obstacles | 99% success | 85% (RMAPPO) | +14 pts |
| Dynamic, 40 obstacles | 95% success | 70% (MAPPO) | +25 pts |
| Dynamic, 50 obstacles | 90% success | 67% (RMAPPO) | +23 pts |

---

*Generated from: Dynamic Target Assignment and Cooperative Decision-Making fo.pdf*
