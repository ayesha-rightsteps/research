# Hey Ayesha — Read This First

## What is this paper about?
This paper tackles a problem the other 4 papers ignore: what happens when your drones are all different types (heterogeneous), some break down mid-mission, and the communication is unreliable? The authors build a framework called RCTP that combines two algorithms — MAML (a meta-learning technique that lets drones quickly adapt to brand new disaster scenarios) and MA-DDPG (a multi-agent RL algorithm for continuous drone control) — to coordinate 10–30 drones for search and rescue missions in disaster environments. Unlike the other papers in this folder, this one also assigns drones into teams (coalitions) based on what each drone is capable of, and reassigns tasks on the fly when drones fail.

## Why does it matter?
Real disaster response — earthquakes, floods, wildfires — requires drones to be deployed fast in environments nobody has seen before, with unreliable GPS and communication, and where some drones will inevitably fail. No previous paper in this folder handles all of this simultaneously, which is why this paper is directly relevant to your teacher's question about heterogeneous drones and scalability.

## How to use this handbook

⏱ If you have 10 minutes:
   → Read this file + `07_cheat_sheet.md`

⏱ If you have 30 minutes:
   → Add `02_concepts.md` + `06_presentation.md`

⏱ If you have 1 hour:
   → Read all files in order (01 → 07)

## Files in this folder
| File | What it contains | When to read it |
|------|-----------------|-----------------|
| 01_summary.md | Big picture — what, why, how | First |
| 02_concepts.md | Every term explained simply | Before presenting |
| 03_methodology.md | Exactly what the researchers did | If sir asks "how" |
| 04_results.md | What they found and why it matters | For Q&A prep |
| 05_critical_analysis.md | Strengths, weaknesses, gaps | To impress sir |
| 06_presentation.md | Script + Q&A for your presentation | Day of presentation |
| 07_cheat_sheet.md | One-page summary to keep open | During presentation |

## How this paper connects to your research
Your teacher asked about **scalability** and **heterogeneous drones** — this paper addresses both directly. It is the only paper in this folder that:
- Models drones with different capabilities (heterogeneous)
- Handles drone failures during a mission
- Uses meta-learning so drones can adapt to scenarios they have never seen before
- Handles real communication failures (LoS/NLoS)

You've got this!
