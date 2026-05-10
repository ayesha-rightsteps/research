# Hey Ayesha — Read This First

## What is this paper about?
This paper tackles the problem of sending multiple drones (UAVs) on missions where they need to decide *which target to fly to* AND *how to get there safely* — at the same time, in a 3D environment full of moving obstacles. The researchers built a new deep reinforcement learning algorithm called **TANet-TD3** that trains drones to make both decisions simultaneously, without needing a pre-planned map. The result is a swarm of drones that can navigate to all their assigned targets, avoid each other, dodge moving obstacles, and complete every mission without missing a single target.

## Why does it matter?
In the real world — military strikes, search & rescue, agricultural spraying — drones can't afford to assign targets first and then plan routes, because the environment keeps changing and that two-step approach leads to failed missions. This work shows that letting drones decide "where to go" and "how to get there" at every single step, in real time, dramatically improves how reliably a drone swarm completes its mission.

---

## How to use this handbook

⏱ **If you have 10 minutes:**
→ Read this file + `07_cheat_sheet.md`

⏱ **If you have 30 minutes:**
→ Add `02_concepts.md` + `06_presentation.md`

⏱ **If you have 1 hour:**
→ Read all files in order (01 → 07)

---

## Files in this folder

| File | What it contains | When to read it |
|------|-----------------|-----------------|
| `01_summary.md` | Big picture — what, why, how | First |
| `02_concepts.md` | Every term explained simply | Before presenting |
| `03_methodology.md` | Exactly what the researchers did | If sir asks "how" |
| `04_results.md` | What they found and why it matters | For Q&A prep |
| `05_critical_analysis.md` | Strengths, weaknesses, gaps | To impress sir |
| `06_presentation.md` | Script + Q&A for your presentation | Day of presentation |
| `07_cheat_sheet.md` | One-page summary to keep open | During presentation |

You've got this! 💙
