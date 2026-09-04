# Image Generation Prompts — Ayesha's Presentation
## One prompt per slide that needs a visual

Generate each image using **DALL-E, Midjourney, or Adobe Firefly**.
Style guide for all images: **clean white background, dark navy blue (#1a2744) and electric blue (#3b82f6) color palette, flat infographic style, no gradients, no decorative art, academic/technical feel**.

---

---

## IMAGE 1 — Slide 1 (Title Slide Background / Hero Image)

**File name to save:** `img_01_title.png`

**Prompt:**
> Flat technical illustration, white background. A swarm of 8 small identical quadcopter drones flying in a 3D triangular formation in open sky. Drones are dark navy blue. Faint light blue dotted lines connect drones to show coordination network. Below the swarm, a faint 3D grid floor represents the environment. Minimalist, clean, no text, no gradients, infographic style, suitable for academic presentation title slide.

**Where to place:** Full-width background or top-right corner of title slide, behind the text.

---

---

## IMAGE 2 — Slide 3 (Introduction: UAVs Today)

**File name to save:** `img_02_uav_applications.png`

**Prompt:**
> Flat infographic icon grid, white background. Six square icon panels arranged in a 2x3 grid. Each panel shows one drone use case as a simple flat icon with a label underneath. Panel 1: drone over flooded area (disaster response). Panel 2: drone over a grid of crops (precision agriculture). Panel 3: drone with a camera near a power tower (infrastructure inspection). Panel 4: drone over a forest fire (search and rescue). Panel 5: drone delivering a small box (logistics). Panel 6: multiple drones in formation (multi-UAV coordination). Icons are dark navy blue on white. Labels in dark grey. Clean, minimal, no gradients, flat design, academic style.

**Where to place:** Right half of the slide, next to bullet points.

---

---

## IMAGE 3 — Slide 4 (Classical Approaches Fail)

**File name to save:** `img_03_centralized_fail.png`

**Prompt:**
> Flat technical diagram, white background. Left side: a central server/computer icon labeled "Centralized Planner" with arrows pointing to 5 small drone icons arranged in a circle around it — this represents the old approach. The arrows are solid navy blue. Right side: the same setup but three of the five drones are surrounded by a red dashed X mark, and a moving obstacle (gray block) has appeared in the path, showing the plan has broken. A large red warning icon appears over the central planner. Clean infographic style, no gradients, no decorative elements, academic PowerPoint style.

**Where to place:** Right side of the slide, next to bullet points.

---

---

## IMAGE 4 — Slide 5 (DRL & MARL)

**File name to save:** `img_04_ctde_diagram.png`

**Prompt:**
> Clean flat technical diagram, white background. Two-phase diagram labeled at the top: left phase labeled "TRAINING" in dark navy, right phase labeled "EXECUTION" in dark navy. Left phase: 4 drone icons connected to a central large brain/neural network icon labeled "Centralized Critic" — arrows flow both ways showing information sharing. Right phase: 4 drone icons, each connected to its own small brain icon, no connection between drones — labeled "Decentralized Actor". A vertical dashed line separates the two phases. Below the diagram, a small label: "CTDE — Centralized Training, Decentralized Execution". Color palette: navy blue and electric blue. No gradients, flat style, academic.

**Where to place:** Right half or bottom half of Slide 5.

---

---

## IMAGE 5 — Slide 6 (The Gap — Fragmented Progress)

**File name to save:** `img_05_gap_diagram.png`

**Prompt:**
> Flat conceptual diagram, white background. Two large puzzle pieces side by side, NOT connected. Left puzzle piece: dark navy blue, labeled "DA-MAPPO" in white text, with a small icon of a target/bullseye underneath and the text "Target Assignment". Right puzzle piece: electric blue (#3b82f6), labeled "IGAT-MARL" in white text, with a small collision warning icon underneath and the text "Collision Avoidance". Between the two pieces: a gap with a bright orange question mark and the text "Combined in 3D?" in orange. The pieces clearly fit each other's shape but are separated. Clean, flat, academic infographic style, white background, no gradients.

**Where to place:** Center or right side of Slide 6.

---

---

## IMAGE 6 — Slide 7 (Problem Statement)

**File name to save:** `img_06_conflict_diagram.png`

**Prompt:**
> Flat technical diagram, white background. A 3D grid environment (faint light gray grid lines showing x, y, z axes). Three drone icons positioned at different altitudes (heights). Drone A has a green arrow pointing toward a green star target. Drone B has a red warning arc between itself and Drone A showing predicted collision path. From Drone A, two conflicting arrows: one solid navy blue arrow pointing toward the target (labeled "Assignment says: Go HERE"), one red dashed arrow pointing away from Drone B (labeled "Avoidance says: Go AWAY"). The two arrows point in opposite directions. This visually shows the core conflict. Clean, flat, no gradients, academic style, white background.

**Where to place:** Right side of Problem Statement slide.

---

---

## IMAGE 7 — Slide 8 (Two Key Papers Comparison)

**File name to save:** `img_07_two_papers.png`

**Prompt:**
> Clean flat two-column comparison graphic, white background. Left column header: "DA-MAPPO" in dark navy blue box. Right column header: "IGAT-MARL" in electric blue box. Left column shows: 3 drone icons, a target icon, and an assignment line connecting drones to targets using the Hungarian algorithm (H symbol), a checkmark "90% success", a red X "No collision avoidance". Right column shows: 5 drone icons with a sparse dotted connection graph between only some pairs (not all), a checkmark "44% fewer edges", a red X "No target assignment". At the bottom between both columns: a bright orange double-headed arrow with text "Each cites the other as Future Work". Flat, clean, academic infographic style.

**Where to place:** Right side or bottom of Slide 8.

---

---

## IMAGE 8 — Slide 11 (Framework Design — Observation Vector)

**File name to save:** `img_08_observation_vector.png`

**Prompt:**
> Clean flat infographic, white background. Central icon: one quadcopter drone (navy blue). Four labeled arrows pointing INTO the drone from four directions, each representing one component of the observation vector. Arrow 1 (from above): labeled "Own State — 3D position + velocity" with a coordinate axes icon. Arrow 2 (from left): labeled "Assignment State — target position from Hungarian algorithm" with a bullseye/target icon. Arrow 3 (from right): labeled "Conflict Neighbors — only drones on collision course" with a warning/collision icon. Arrow 4 (from below): labeled "Obstacle Proximity — 6 cardinal directions" with a compass/cube icon. All arrows are electric blue. The drone is at center. Clean, flat, academic PowerPoint style, no gradients.

**Where to place:** Right side of Slide 11.

---

---

## IMAGE 9 — Slide 12 (Framework Pipeline)

**File name to save:** `img_09_pipeline.png`

**Prompt:**
> Vertical flowchart diagram, white background, flat clean style. Five rectangular boxes connected by downward arrows. Box 1 (top, dark navy): "3D Environment — Drones + Targets + Obstacles". Arrow down. Box 2 (electric blue): "Hungarian Assignment — minimum cost, updated every step". Arrow down. Box 3 (electric blue): "Conflict Graph Update — only collision-risk drone pairs connected". Arrow down. Box 4 (electric blue): "Combined Observation Vector — 4 components merged". Arrow down. Box 5 (bottom, dark navy): "MAPPO Policy → 3D velocity command". On the right side of Box 5, a side arrow pointing to a small results box: "Mission Success Rate | Collision Count | Trajectory Length". All boxes have rounded corners. Clean, minimal, academic infographic style.

**Where to place:** Center or right side of Slide 12. Can be used instead of the ASCII diagram in the MD.

---

---

## IMAGE 10 — Slide 13 (Curriculum Training)

**File name to save:** `img_10_curriculum.png`

**Prompt:**
> Flat horizontal progression diagram, white background. Four stages shown left to right with an arrow connecting each. Stage 1 box (lightest blue): "Stage 1 — 3 Drones — Static Targets — Low Obstacles". Stage 2 box (medium blue): "Stage 2 — 5 Drones — Moving Targets — Medium Obstacles". Stage 3 box (dark blue): "Stage 3 — 8 Drones — Moving Targets — 50 Obstacles". Stage 4 box (dark navy): "Stage 4 — Unseen Sizes — Generalization Test". Below each box, a small drone cluster icon showing increasing number of drones. A large horizontal arrow from Stage 1 to Stage 4 at the bottom labeled "Increasing Difficulty". Clean, flat, academic style, no gradients, white background.

**Where to place:** Full width or bottom half of Slide 13.

---

---

## IMAGE 11 — Slide 14 (Evaluation Plan — Test Grid)

**File name to save:** `img_11_eval_grid.png`

**Prompt:**
A clean flat academic infographic on white background. A top-down 3D grid environment showing 8 small navy blue quadcopter drones flying toward 8 distinct green star-shaped target 
markers. Some drones have a solid blue arrow pointing toward their target. Two drones near each other have a small red warning arc between them showing predicted collision. One drone has 
both a blue arrow (toward target) and a red dashed arrow (away from collision) showing the competing signals. The environment has light grey 3D grid lines suggesting a 3D space. In the 
bottom right corner, a small scorecard box shows: "Mission Success Rate", "Collision Count", "Trajectory Length" as three metric labels with small bar icons. No gradients, flat design, 
white background, academic infographic style, no realistic textures.

**Where to place:** Right side of Slide 14.

---

---

## IMAGE 12 — Slide 16 (Contribution / Why It Matters)

**File name to save:** `img_12_contribution.png`

**Prompt:**
> Flat conceptual diagram, white background. Three stages shown left to right. Stage 1: two separate circles, one labeled "Assignment (2D)" in navy, one labeled "Avoidance (2D)" in electric blue, with a gap between them and an X mark between them. Stage 2 (center): the same two circles overlapping as a Venn diagram, labeled "This Research" in orange text above, with "3D" written in the center overlap zone. Stage 3 (right): a single green checkmark circle labeled "Unified Policy (3D)" — representing the outcome. Below Stage 1: "Existing Work". Below Stage 2: "Proposed". Below Stage 3: "Goal". A horizontal arrow runs beneath all three stages showing progression. Clean, flat, academic, white background.

**Where to place:** Right side of Slide 16.

---

---

# HOW TO USE THESE PROMPTS

1. **Copy** the prompt text exactly
2. **Paste** into DALL-E (chat.openai.com), Midjourney, Adobe Firefly, or Canva AI
3. **Save** the image as the specified filename (e.g., `img_01_title.png`)
4. **Add** to the corresponding slide in PowerPoint or Google Slides

**Tip:** If the image is not clean enough, add this to any prompt:
> "flat design, white background, infographic style, no textures, no gradients, no decorative borders, suitable for academic PowerPoint presentation"

**Tip:** For Midjourney, add `--style raw --ar 16:9` at the end for widescreen slide ratio.

---

# SLIDE → IMAGE MAPPING (Quick Reference)

| Slide | Image File | Purpose |
|---|---|---|
| Slide 1 (Title) | img_01_title.png | Hero image / background |
| Slide 3 (UAVs Today) | img_02_uav_applications.png | 6 application icons |
| Slide 4 (Classical Fail) | img_03_centralized_fail.png | Centralized planner breaking |
| Slide 5 (DRL/MARL) | img_04_ctde_diagram.png | CTDE training vs execution |
| Slide 6 (The Gap) | img_05_gap_diagram.png | Two puzzle pieces not connected |
| Slide 7 (Problem) | img_06_conflict_diagram.png | Conflicting arrows in 3D |
| Slide 8 (Two Papers) | img_07_two_papers.png | DA-MAPPO vs IGAT-MARL |
| Slide 11 (Framework) | img_08_observation_vector.png | 4 arrows into drone |
| Slide 12 (Pipeline) | img_09_pipeline.png | Vertical flowchart |
| Slide 13 (Curriculum) | img_10_curriculum.png | 4-stage progression |
| Slide 14 (Evaluation) | img_11_eval_grid.png | 3×3 test grid |
| Slide 16 (Contribution) | img_12_contribution.png | Venn → unified |
