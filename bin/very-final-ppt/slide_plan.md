# PPT Slide Plan — Updated Version
### Based on: CUI_Synopsis_AYESHA_KHALIL-SP25-RCS-009_FIXED.docx
### Old PPT: synnopsis presentation_compressed.pptx (14 slides)

---

## OVERVIEW: Kya Badla, Kya Nahi

| Slide | Title | Status | Reason |
|---|---|---|---|
| 1 | Title | CHANGE | Remove "3D", add PAH to title |
| 2 | Introduction | KEEP | Same content |
| 3 | Intro cont — Multi-UAV | KEEP | Same content |
| 4 | Intro cont — DRL & MARL | KEEP | Same content |
| 5 | Motivation | MAJOR CHANGE | 3D→2D, add PAH, add fixed-weights gap |
| 6 | Related Work | KEEP | Same content |
| 7 | Related Work cont | KEEP | Same content |
| 8 | Gap in existing work | CHANGE | Remove "3D only" point, add fixed-weights gap |
| 9 | Problem Statement | CHANGE | New PS from synopsis |
| 10 | Research Objectives | CHANGE | Add PAH objective, update Obj 1 and Obj 3 |
| 11 | Proposed Methodology | MAJOR CHANGE | Add PAH as core component |
| 12 | Training Strategy | MINOR | Just change 3D → 2D |
| 13 | References | KEEP | Same |
| 14 | Thank You | KEEP | Same |

---

## SLIDE-BY-SLIDE DETAILS

---

### SLIDE 1 — TITLE
**Status: CHANGE**

**Heading:**
> Joint Target Assignment and Conflict-Aware Collision Avoidance in Multi-UAV Coordination Using MAPPO with Priority Arbitration

**Subtext:**
> Ayesha Khalil | CIIT/SP25-RCS-009/ATD
> Supervisor: Dr. Faisal Rehman | Co-supervisor: Dr. Ehzaz Mustafa

**Why changed:** Old title said "3D" — now 2D. Title should also hint at PAH (Priority Arbitration).

**Image prompt (if needed):**
> A dark background with 4-5 UAV drones flying in formation over a 2D grid map, with glowing trajectory lines and a small neural network icon in the corner. Professional, IEEE conference style. No text in image.

---

### SLIDE 2 — Introduction: UAV Applications
**Status: KEEP**

Content stays:
- Military → civilian evolution
- Single drone insufficient
- Real tasks need teams
- Hardware ≠ coordination

**Existing image: Keep Picture 4**

---

### SLIDE 3 — Introduction cont: Multi-UAV Coordination
**Status: KEEP**

Content stays:
- Classical centralized planner → fails when dynamic
- Learning-based approach: drones learn through trial and error

---

### SLIDE 4 — Introduction cont: DRL & MARL
**Status: KEEP**

Content stays:
- DRL: agent → reward → policy
- MARL: extends to teams
- CTDE architecture
- MAPPO: proven baseline

---

### SLIDE 5 — Motivation
**Status: MAJOR CHANGE**

**Old content had:** "3D environment" reference → REMOVE

**New content:**

**Bullet 1 (keep):**
> DA-MAPPO achieves 90–99% mission success using real-time Hungarian assignment — but uses a FIXED collision penalty (C_collision = constant) that never adapts

**Bullet 2 (keep):**
> IGAT-MARL reduces interaction edges by 44% using a conflict-aware graph — but uses FIXED reward weights and assumes targets are already assigned

**Bullet 3 (keep):**
> DA-MAPPO ablation: removing assignment information causes success to drop from 90% → 0% — confirming assignment is non-negotiable

**Bullet 4 (keep):**
> Both papers explicitly name the other's problem as their own future work — this research is that future work

**Bullet 5 (NEW — MOST IMPORTANT):**
> Neither framework learns WHEN to prioritize assignment over avoidance — both use hand-tuned fixed constants. The Priority Arbitration Head is the first mechanism that learns this decision dynamically at every timestep.

**Bullet 6 (NEW):**
> This research proposes a unified MAPPO-based framework for 5–8 drones in a 2D environment, with a learned Priority Arbitration Head that dynamically weights both objectives based on each drone's real-time state.

**Image prompt:**
> A side-by-side comparison diagram: Left box labeled "DA-MAPPO" with fixed weight = constant shown as a frozen/locked icon. Right box labeled "IGAT-MARL" with fixed weight = constant locked icon. Center arrow pointing down to "Priority Arbitration Head" with a dynamic slider/graph showing α changing over time. Clean, minimal, white background with blue and orange accents.

---

### SLIDE 6 — Related Work
**Status: KEEP**

Existing table/content unchanged.

---

### SLIDE 7 — Related Work cont
**Status: KEEP**

Existing table/content unchanged.

---

### SLIDE 8 — Gap in Existing Work
**Status: CHANGE**

**Remove this bullet:**
> ~~All existing work tested in 2D environments only~~ ← We are also 2D now, so this is no longer a differentiator

**Keep:**
> Researchers studying target assignment built methods without collision avoidance
> Researchers studying collision avoidance built methods without any goal/target structure
> Result: capable but partial solutions — each solves one piece, ignores the rest
> The two most advanced recent papers each explicitly cite the other's problem as their own next step

**Add (THE CORE GAP):**
> All existing frameworks apply FIXED reward coefficients — assignment weight and avoidance weight are constants set before training and never change, regardless of the drone's current situation
> No framework has a mechanism that LEARNS when assignment must dominate and when avoidance must dominate — this is the structural gap this research addresses

**Image prompt:**
> A visual showing three rows: DA-MAPPO (α_assign = 0.7 FIXED, locked padlock icon), IGAT-MARL (α_avoid = 1.0 FIXED, locked padlock icon), Proposed Framework (α = learned, dynamic curve showing it changing, unlocked icon). Clean table-style layout, red locked icons vs green dynamic icon.

---

### SLIDE 9 — Problem Statement
**Status: CHANGE**

**New PS (from FIXED.docx para 40):**
> In multi-UAV cooperative missions, task allocation and collision avoidance are interdependent — a UAV's path to its assigned target directly affects its proximity to other UAVs, and any safety-driven course correction changes whether that target remains reachable.
>
> This interdependence means a single avoidance maneuver can leave a critical target uncovered, trigger reassignment conflicts across the swarm, and create new collision risks simultaneously.
>
> Despite being the two most studied problems in multi-UAV coordination, task allocation and collision avoidance have never been addressed together within a single learned policy.

**No image needed — clean text slide.**

---

### SLIDE 10 — Research Objectives
**Status: CHANGE**

**Objective 1 (UPDATED):**
> Design and implement a Priority Arbitration Head — a lightweight neural module jointly trained with the MAPPO actor — that dynamically weights assignment and avoidance objectives at each timestep using time-to-collision, distance to target, and conflict neighbor count as inputs

**Objective 2 (keep):**
> Test the proposed framework across swarm sizes of 3, 5, and 8 drones — determine if performance degrades as simultaneous assignment-conflict interactions increase

**Objective 3 (UPDATED):**
> Perform controlled ablation experiments comparing the learned α against fixed baselines at α = 0.3, 0.5, and 0.7 — isolating the contribution of the Priority Arbitration Head, conflict graph, and Hungarian assignment mechanism

**Objective 4 (keep):**
> Find the failure boundary — identify swarm size, obstacle density, and target speed combinations where the unified policy fails, and characterize the failure mode

**Image prompt:**
> A simple diagram of the Priority Arbitration Head: 3 inputs (τ_collision, d_target, n_conflict) going into a small neural network box, outputting α ∈ [0,1]. Below: r_total = α × r_assign + (1−α) × r_avoid. Clean, minimal, white or light grey background. Use orange for the PAH box.

---

### SLIDE 11 — Proposed Methodology
**Status: MAJOR CHANGE**

**Section A — Observation Vector (keep structure, update to 2D):**
Each drone observes 4 elements:
1. 2D position + velocity (self-state)
2. 2D relative position of assigned target [via Hungarian allocation]
3. Positions + velocities of conflict neighbors [via dynamic conflict graph]
4. Obstacle proximity in 4 cardinal directions

**Section B — Priority Arbitration Head (NEW — this is the main slide):**
> A 2-layer feedforward network (64 neurons) jointly trained with the MAPPO actor
> Inputs: τ_collision (time-to-collision), d_target (distance to target), n_conflict (conflict neighbor count)
> Output: α ∈ [0,1]
> Reward: r_total = α × r_assignment + (1−α) × r_avoidance
> Training: Same policy gradient update as MAPPO actor — no separate loop
> Critic: Unchanged — centralized critic receives full joint state of all drones

**Image prompt:**
> Full pipeline diagram (2D): On left, a drone icon with 4 observation arrows (self, target, neighbors, obstacles) feeding into "Joint Observation Vector" box. This splits into two: "MAPPO Actor" (blue box) and "Priority Arbitration Head" (orange box). Both feed into "Reward Computation" (green box) showing the formula. Below: "Centralized Critic" (grey box) with dotted arrow showing training. Right side: "2D Environment" with drone icons. Clean, professional, IEEE-style.

---

### SLIDE 12 — Training Strategy
**Status: MINOR CHANGE**

Change "3D" to "2D" wherever it appears in the existing slide.

4-stage curriculum:
- Stage 1: 3 drones, 2D, static targets — validate baseline
- Stage 2: 5 drones, moving targets, some obstacles
- Stage 3: 8 drones, high obstacle density, dynamic targets
- Stage 4: Generalization to unseen swarm sizes

**Keep existing image (Picture 5)**

---

### SLIDE 13 — References
**Status: KEEP**

No changes needed.

---

### SLIDE 14 — Thank You
**Status: KEEP**

No changes needed.

---

## SUMMARY OF CHANGES TO TELL AYESHA

1. **Slide 1** — Title: remove "3D", add "Priority Arbitration" in title
2. **Slide 5** — Motivation: add PAH as novel contribution, change "3D environment" to "2D environment", add fixed-weights gap bullet
3. **Slide 8** — Gap: remove "all existing work in 2D" bullet (we're 2D too now), replace with "all existing work uses FIXED weights" bullet
4. **Slide 9** — PS: replace with new short, clean PS from FIXED synopsis
5. **Slide 10** — Objectives: update Obj 1 to mention PAH, update Obj 3 to mention learned α vs fixed α ablation
6. **Slide 11** — Methodology: add PAH as core component with its formula
7. **Slide 12** — Training: change "3D" → "2D"
