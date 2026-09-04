# Ayesha's Research Handbook
### Paper: Large-scale UAV Swarm Path Planning Based on Mean-Field Reinforcement Learning

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

**Algorithm:** PO-WMFDDPG (Partially Observable Weighted Mean Field DDPG)

**Problem solved:** Coordinating 80+ UAVs simultaneously in a battlefield with no-fly zones, where standard MARL collapses due to N-squared interaction complexity and existing mean-field methods fail by treating all neighbors equally regardless of distance.

**Three innovations:** (1) Mean field theory + DDPG for continuous action UAV control, (2) partial observability — only neighbors within communication range R_a contribute to the mean field, (3) multi-head attention mechanism to weight closer/more relevant neighbors higher.

**Key results:** ~98% task success rate with 80 UAVs; >90% maintained up to 120 UAVs where DDPG and MFDDPG both collapse. Stable to 36 NFZs vs. DDPG collapsing at 26. Moving-NFZ test: 75/80 succeed.

**Published:** Chinese Journal of Aeronautics, 38(9): 103484 (2025)

---

*Generated from: `1-s2.0-S1000936125000901-main.pdf`*
