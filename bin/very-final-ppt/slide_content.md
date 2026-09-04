# Slide Content — Final PPT
### Rule: Max 5 bullets per slide. Max 10 words per bullet. Presenter speaks the rest.

---

## SLIDE 1 — Title

**Main Title:**
Joint Target Assignment and Conflict-Aware Collision Avoidance
in Multi-UAV Coordination Using MAPPO with Priority Arbitration

**Subtitle:**
Synopsis Presentation — MS Computer Science

**Name block:**
Ayesha Khalil | SP25-RCS-009
Supervisor: Dr. Faisal Rehman
Co-Supervisor: Dr. Ehzaz Mustafa

---

## SLIDE 2 — Introduction: Why UAVs?

**Headline:** From military tools to critical civilian infrastructure

**Bullets:**
- UAVs now used in disaster response, agriculture, inspection
- Single drone cannot cover complex, large-scale missions
- Teams of drones are faster, redundant, and more effective
- Hardware is ready — coordination is the unsolved problem

---

## SLIDE 3 — Introduction: The Coordination Challenge

**Headline:** Multiple drones, shared airspace, conflicting decisions

**Bullets:**
- Classical planners compute one global solution — too slow
- Dynamic environments break pre-planned paths instantly
- Drones need to adapt in real-time, independently
- Solution: let drones learn coordination through experience

---

## SLIDE 4 — Introduction: DRL and MARL

**Headline:** Learning-based coordination — how it works

**Bullets:**
- DRL: agent receives reward, learns optimal policy
- MARL: extends DRL to teams of cooperating agents
- CTDE: train with shared info, execute independently
- MAPPO: best-performing cooperative MARL algorithm

---

## SLIDE 5 — Motivation: The Gap

**Headline:** Two strong papers — two halves of the same problem

**Bullets:**
- DA-MAPPO: 90–99% mission success, zero collision avoidance
- IGAT-MARL: 44% fewer conflict edges, zero target assignment
- Both use fixed, hand-tuned reward weights — never adapt
- Both cite the other's problem as their own future work
- No framework learns when to prioritize which objective

---

## SLIDE 6 — Related Work (Table)

*Keep existing table — no text changes needed*

---

## SLIDE 7 — Related Work cont (Table)

*Keep existing table — no text changes needed*

---

## SLIDE 8 — Gap in Existing Work

**Headline:** The structural hole no one has filled

**Bullets:**
- Assignment and avoidance always studied in isolation
- No single learned policy handles both simultaneously
- All frameworks use fixed coefficients set before training
- Assignment weight and avoidance weight never change mid-mission
- No mechanism exists to learn priority — this is the gap

---

## SLIDE 9 — Problem Statement

**Headline:** One sentence captures it all

**Display this text (large font, center of slide):**
> In multi-UAV cooperative missions, task allocation and collision avoidance are interdependent — a UAV's path to its assigned target affects proximity to teammates, and any safety maneuver changes whether that target stays reachable. Despite being the two most studied problems in the field, they have never been solved together in a single learned policy.

*No bullets needed. Let the text breathe.*

---

## SLIDE 10 — Research Objectives

**Headline:** Four concrete, measurable goals

**Bullets:**
- Design the Priority Arbitration Head (PAH) jointly trained with MAPPO
- Scale testing: 3 → 5 → 8 drones, measure performance drop
- Ablation: learned α vs fixed α at 0.3, 0.5, 0.7
- Find failure boundary: swarm size, density, speed limits

---

## SLIDE 11 — Proposed Methodology

**Headline:** MAPPO + Priority Arbitration Head — one unified policy

**Section A — What each drone observes (4 inputs):**
- Self-state: 2D position + velocity
- Assignment state: relative position of target via Hungarian algorithm
- Conflict graph: positions of collision-course neighbors only
- Obstacle proximity: distance in 4 directions

**Section B — Priority Arbitration Head:**
- Inputs: time-to-collision · distance to target · conflict neighbor count
- Output: α ∈ [0, 1]  →  learned at every timestep
- Reward: r = α × r_assign + (1−α) × r_avoid
- Trained jointly with MAPPO actor — no separate loop

*Use the Mermaid pipeline diagram as the slide visual*

---

## SLIDE 12 — Training Strategy

**Headline:** Curriculum learning — progressive difficulty

**Bullets:**
- Stage 1: 3 drones, static targets — replicate DA-MAPPO baseline
- Stage 2: 5 drones, moving targets, some obstacles
- Stage 3: 8 drones, high density, fully dynamic targets
- Stage 4: Unseen swarm sizes — test generalization

---

## SLIDE 13 — References

*Keep existing — no changes*

---

## SLIDE 14 — Thank You

*Keep existing — no changes*

---

## QUICK RULES FOR BUILDING SLIDES

| What to put on slide | What to say out loud |
|---|---|
| Bullet keyword (3-5 words) | Full explanation (2-3 sentences) |
| One strong headline | The context and motivation |
| A single diagram | Walk through it step by step |
| A number or result | What it means in plain English |

**Never put a full sentence on a slide if you are going to read it aloud.**
**The slide is a prompt — you are the content.**
