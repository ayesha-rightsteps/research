# Ayesha's Research Handbook
### Paper: Deep Reinforcement Learning-Based Adaptive Collision Avoidance Method for UAV in Joint Operational Airspace

**Authors:** Yan Shen, Xuejun Zhang, Yan Li, Weidong Zhang — Beihang University, 2026
**Journal:** Defence Technology, Vol. 56, pp. 142–159
**Algorithm proposed:** HPER-D3QN | **Key result:** 96.28% success rate with 25 aircraft

---

## Reading Guide

| # | File | Purpose | Est. Time |
|---|------|---------|-----------|
| 0 | `00_START_HERE.md` | Orientation — read this first | 2 min |
| 1 | `01_summary.md` | Full paper overview: problem, solution, results, contribution | 8 min |
| 2 | `02_concepts.md` | Every term, acronym, model, and metric explained simply | 12 min |
| 3 | `03_methodology.md` | Step-by-step: what the researchers did and how | 10 min |
| 4 | `04_results.md` | All results explained with plain-English interpretations | 8 min |
| 5 | `05_critical_analysis.md` | Strengths, hidden weaknesses, missing experiments | 6 min |
| 6 | `06_presentation.md` | Word-for-word script + model answers to every likely question | 10 min |
| 7 | `07_cheat_sheet.md` | One-page quick reference — keep open while presenting | 1 min |

---

## Recommended path if time is short

`00_START_HERE.md` → `07_cheat_sheet.md` → `06_presentation.md` → done.

This path gives you: orientation (2 min) + key numbers and terms (1 min) + complete presentation script (10 min) = 13 minutes total and you are ready to walk in.

---

## The Three-Sentence Version

A drone flying in a military battlefield cannot avoid other aircraft if it cannot communicate with them and the wind keeps pushing it off course. This paper proposes HPER-D3QN — a deep reinforcement learning system that teaches the drone to identify the most dangerous nearby aircraft using time-to-collision, separation distance, and aircraft type, and then learn from the most critical past experiences first. The result is a 96.28% mission success rate even with 25 mixed manned-unmanned aircraft in the airspace, outperforming all existing methods.

---

## The One-Sentence Contribution

This paper is the first to combine heterogeneous aircraft type handling, sector-based partial observability, dynamic wind uncertainty, and hierarchical experience replay into a single deep reinforcement learning system for military UAV collision avoidance — and validates it against both DRL baselines and established industry standards.

---

*Generated from: 1-s2.0-S2214914725002715-main.pdf*
