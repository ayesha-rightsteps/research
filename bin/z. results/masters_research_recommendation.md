# Masters Research Problem Recommendation

> **For:** Ayesha
> **Based on:** Analysis of all 10 papers in this folder
> **Purpose:** Help you pick ONE focused, achievable, and publishable research problem

---

## First — What a Masters Research Problem Must Be

Before the recommendation, here are the four filters every good masters problem must pass:

| Filter | What it means |
|---|---|
| **Focused** | One specific gap — not "solve everything" |
| **Achievable** | Can be done in 12–18 months with a laptop + simulation |
| **Novel** | Not already solved by any of the 10 papers you read |
| **Publishable** | Clear baseline to beat, clear metric to measure improvement |

---

## My Recommendation

### ✅ Target This Problem:

> **"Multi-UAV collision-free navigation to dynamic (moving) targets in a 3D environment, scaled to 5–10 drones — combining real-time target reassignment with collision avoidance in a single learning framework."**

---

## Why This Specific Problem? (The Logic)

Here is how I eliminated the other options and arrived at this one.

---

### Step 1: Eliminate problems that are already well-solved

| Problem | Already Solved By | Verdict |
|---|---|---|
| Single-UAV path planning in 2D | Paper 1 (D3QN) — handles moving obstacles well | ❌ Skip |
| Large-scale 2D swarm coordination (80–120 drones) | Paper 4 (PO-WMFDDPG) — scales to 120, strong results | ❌ Skip |
| Multi-hop UAV networking with LLMs | Paper 6 (MRLMN) — well-executed, strong baseline | ❌ Skip |
| LLM + MARL role assignment | Paper 7 (RALLY) — well-executed, theoretical proof included | ❌ Skip |
| Multi-agent framework comparison | Paper 8 — definitive comparison already done | ❌ Skip |

These are too mature. You would be building on top of them, not creating a new problem.

---

### Step 2: Eliminate problems that need too much compute or data

| Problem | Why it's out of scope for a masters |
|---|---|
| Disaster response with 100+ heterogeneous drones | Needs massive simulation, complex scenario design — Paper 5 territory |
| LLM-MARL integration | Requires GPT-4o API budget + LoRA fine-tuning infrastructure |
| Full urban air traffic management | Too many moving parts — 3+ years of work minimum |
| Real hardware validation | Needs drones, lab space, hardware budget |

---

### Step 3: Identify what is genuinely open and achievable

After eliminating what's already done and what's too large, three problems remain:

---

#### Option A: Scale DA-MAPPO (Paper 91) from 3 to 10+ drones
**What's open:** Paper 91 (DA-MAPPO) only tested with exactly 3 drones. The paper proves the concept but never validates it at larger swarm sizes. Scaling to 5, 8, 10 drones with the same real-time dynamic assignment is experimentally uncharted.

**Achievable?** Yes — the codebase concept is clear, the environment (Unity/custom 2D sim) is manageable, the baseline is Paper 91 itself.

**Limitation:** Still 2D, still static obstacles. The contribution is "scaling" only — that is thin for a masters if the environment doesn't change.

**Score: 7/10**

---

#### Option B: Add dynamic obstacles to Paper 91's framework
**What's open:** Paper 91 uses static obstacles only. The real world has moving obstacles (vehicles, other aircraft, debris). A system that handles dynamic targets AND dynamic obstacles simultaneously is genuinely new.

**Achievable?** Yes — simulating moving obstacles is not technically hard; the challenge is designing a reward and observation space that handles both.

**Limitation:** Still 3 drones only. Not a significant enough jump unless you also scale.

**Score: 7/10**

---

#### ⭐ Option C: Combine real-time dynamic target assignment + collision avoidance in 3D, for 5–10 drones

**What's open:**
- Paper 91 (dynamic assignment) — only 3 drones, 2D, static obstacles
- Paper 9 (collision avoidance IGAT) — only collision avoidance, no target assignment, 2D
- Paper 3 (3D path planning) — only 1 drone, no multi-agent

**These three papers each solved one piece. No paper has combined all three.**

A system that simultaneously does:
1. Real-time dynamic target reassignment (contribution of Paper 91)
2. Collision avoidance between drones (contribution of Paper 9)
3. In a 3D environment (contribution of Paper 3)
4. For 5–10 drones (bigger than Paper 91, smaller than Paper 4)

...does not exist yet.

**Achievable?** Yes — this is exactly the right scope for a masters:
- Use MAPPO or MADDPG as your RL backbone
- Extend the assignment-augmented observation vector from Paper 91
- Add altitude as a dimension (trivial in simulation)
- Use conflict-aware interaction model from Paper 9 to handle collision avoidance
- Environment: PyBullet, Unity ML-Agents, or custom gym — all free

**Publishable?** Very clearly — you have 3 baselines to beat (Papers 9, 91, and a combined vanilla MAPPO), clear metrics (success rate, collision rate, trajectory efficiency), and a gap that every one of these papers explicitly mentions in their future work sections.

**Score: 9/10** ← This is my recommendation

---

## The Recommendation in One Sentence

> **"Extend DA-MAPPO's real-time dynamic target assignment to a 3D environment with 5–10 drones, integrating collision avoidance directly into the learning framework — the problem that Papers 9 and 91 each solve halfway but neither solves together."**

---

## What Your Contribution Would Be

| Current state (from existing papers) | Your contribution |
|---|---|
| Paper 91: real-time assignment works for 3 drones, 2D, static obstacles | Same assignment mechanism extended to 5–10 drones |
| Paper 9: collision avoidance works but has no target assignment | Collision-aware interaction integrated with the assignment-augmented observation |
| Paper 3: 3D path planning works for 1 drone | Multi-drone version in 3D |
| No paper: combination of all three in one framework | **Your paper** |

Your title could be something like:
> *"Collision-Aware Dynamic Target Assignment for Multi-UAV Navigation in 3D Environments Using Multi-Agent Proximal Policy Optimization"*

---

## How to Scope it for 12–18 Months

**Phase 1 (Months 1–3): Environment Setup**
- Build a 3D simulation in PyBullet or custom gym
- Implement Hungarian algorithm for minimum-cost assignment (already in Paper 91 — open source logic)
- Replicate Paper 91's baseline with 3 drones to confirm your setup works

**Phase 2 (Months 4–8): Core Contribution**
- Extend observation space to 3D (add altitude, 3D relative positions)
- Integrate conflict-aware interaction (inspired by Paper 9) — only model drone-drone pairs within a conflict radius
- Train MAPPO with assignment-augmented state on 5 drones, then 8, then 10
- Progressive curriculum: start with static targets + sparse obstacles, gradually add moving targets + more obstacles

**Phase 3 (Months 9–12): Experiments + Writing**
- Run comparison against Paper 91 baseline (3-drone version + yours)
- Run comparison against Paper 9 baseline (collision avoidance only vs. yours)
- Ablation: does assignment-augmentation help? Does conflict-aware graph help? Does 3D matter?
- Write up

**Phase 4 (Months 13–18): Buffer for revisions + submission**

---

## What You Will Need

| Resource | Notes |
|---|---|
| Python + PyTorch | Free |
| PyBullet or custom gym | Free, many open source examples exist |
| A GPU | Even a mid-range GPU handles 5–10 drones in simulation |
| Papers 9 and 91 as your primary references | You already have them |
| Paper 4 (mean-field) as reference if you need to scale higher | Already in your folder |

---

## One Last Thing — Why NOT to Pick These

| Alternative | Why to avoid it |
|---|---|
| "Combine LLMs with MARL for UAVs" | Papers 6 and 7 already did this well; you need GPT-4o budget; hard to surpass |
| "Real hardware experiments" | Needs physical drones, lab access, safety protocols — beyond masters scope without a lab |
| "Scale to 100+ drones" | Mean-field theory required; Papers 4 and 5 already did this; much harder baseline to beat |
| "Coalition formation for disaster response" | Paper 5 already covered this very thoroughly; hard to add meaningful novelty |
| "Build a better framework (CrewAI vs AutoGen)" | Paper 8 already did the comparison; not a UAV/RL problem |

---

## Final Answer

**Work on this:**

> Multi-UAV navigation in 3D with real-time dynamic target reassignment and integrated collision avoidance — tested on 5–10 drones — using MAPPO with assignment-augmented observations and a conflict-aware interaction model.

This problem is:
- ✅ Focused: one framework, one environment type, one metric suite
- ✅ Achievable: simulation-only, free tools, clear implementation path
- ✅ Novel: no existing paper combines Papers 9 + 91 + 3D
- ✅ Publishable: three clear baselines, three papers that explicitly name this gap as future work

The gap is real, the tools are ready, and the scope fits a masters timeline perfectly.

---

*Written based on analysis of: Papers 1, 2, 3, 4, 5, 6, 7, 8, 9, and 91 | Date: 2026-05-28*
