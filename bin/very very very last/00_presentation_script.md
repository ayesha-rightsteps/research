# Presentation Script — Slide by Slide
### Yeh parh k bolna hai — apni zaban mein, natural tarike say

---

## SLIDE 1 — Title

**Bolna:**
> "Good morning sir. My name is Ayesha Khalil and my registration number is SP25-RCS-009. Today I am presenting my synopsis titled — MAPPO Framework for Joint Dynamic Target Assignment and Conflict-Aware Collision Avoidance in Multi-UAV Systems. My supervisor is Dr. Faisal Rehman and my co-supervisor is Dr. Ehzaz Mustafa."

---

## SLIDE 2 — Introduction: Why UAVs?

**Bolna:**
> "Sir, UAVs — unmanned aerial vehicles — are now being used in many real-world applications. Disaster response, search and rescue, agriculture, infrastructure inspection — these are all missions where UAVs are being deployed. But a single drone cannot handle a large-scale mission alone. It cannot cover a large area, it has limited battery, and if it fails, the mission fails. That is why we use teams of drones working together. The hardware for this already exists. The problem that remains unsolved is how to coordinate multiple drones effectively."

---

## SLIDE 3 — Introduction: Multi-UAV Coordination

**Bolna:**
> "Sir, when multiple drones fly together in the same airspace, they need to make decisions that are individually correct but also collectively effective. Traditional approaches use a centralized planner — one system plans everything for all drones. But this fails in dynamic environments where obstacles appear suddenly or targets move. A real-time global solution is not feasible for larger teams. So researchers have moved toward learning-based methods — where each drone learns its own policy through experience, without being given fixed rules."

---

## SLIDE 4 — Introduction: DRL & MARL

**Bolna:**
> "Sir, deep reinforcement learning — or DRL — is the foundation of this work. In DRL, an agent interacts with its environment, receives a reward signal, and over time learns a policy that maximizes that reward. Now when we extend this to multiple agents — multiple drones — we get Multi-Agent Reinforcement Learning, or MARL. In MARL, each drone learns how to behave by also observing what other drones are doing. The architecture we use is called CTDE — Centralized Training, Decentralized Execution. This means during training all drones share information, but during an actual mission each drone decides on its own using only local information. The specific algorithm we use is MAPPO — Multi-Agent Proximal Policy Optimization — which has been shown to be the best-performing cooperative MARL algorithm."

---

## SLIDE 5 — Motivation

**Bolna:**
> "Sir, here is the core motivation. Imagine a UAV is flying toward its assigned target using the shortest possible path. Suddenly, an obstacle or another UAV enters that path. The drone must take an evasive maneuver. But now its path has changed — and the target may no longer be reachable. Worse, the new position of this drone may now conflict with another drone's path. That drone also deviates. This cascades through the swarm — one obstacle causes swarm-wide path failure. The reason this happens is that assignment and avoidance are coupled — you cannot solve one without considering the other. Separate solutions are not enough."

---

## SLIDE 6 — Related Work

> (Is slide k leay alag file hai: **01_literature_review.md** — woh parh k bolna)

---

## SLIDE 7 — Gap in Existing Work

**Bolna:**
> "Sir, looking at existing work, we can identify a clear structural gap. The papers that focus only on target assignment — like DA-MAPPO — successfully get UAVs to their targets, but they have no collision avoidance mechanism. Drones end up colliding with each other. On the other hand, papers that focus only on collision avoidance — like IGAT-MARL — successfully prevent collisions, but drones have no target to reach. Targets stay uncovered and the mission is not accomplished. Now if we try to combine both using fixed reward weights — like multiply assignment reward by 0.7 and avoidance reward by 0.3 — one always overrides the other depending on the situation. These weights are set before training and never change. What is missing is a mechanism that learns, at every single timestep, whether assignment should be prioritized or avoidance should be prioritized based on the drone's actual situation at that moment."

---

## SLIDE 8 — Problem Statement

**Bolna:**
> "Sir, this brings us to the problem statement. In multi-UAV cooperative missions, task allocation and collision avoidance are inherently interdependent. A UAV's path to its assigned target directly affects how close it gets to other UAVs. And any safety-driven deviation changes whether that target remains reachable. This coupling means a single avoidance maneuver can leave a critical target uncovered, trigger reassignment conflicts across the swarm, and simultaneously create new collision risks. Despite being the two most studied problems in multi-UAV coordination, they have never been addressed together within a single learned policy. That is the gap this research addresses."

---

## SLIDE 9 — Research Objectives

**Bolna:**
> "Sir, we have four research objectives. First — we want to design a mechanism that dynamically learns to balance assignment and avoidance at every decision step. This is the Priority Arbitration Head, which is the core contribution of this work. Second — we want to test whether this framework scales. We will test with 3 drones, then 5, then 8 — and check whether performance drops as swarm size increases. Third — we want to compare our learned weight alpha against fixed baselines. Does a learned priority mechanism actually perform better than just setting fixed coefficients? We will prove this through ablation experiments. Fourth — we want to find the failure boundary. Under what conditions does our framework break down? What swarm size, obstacle density, or target speed causes failure? Understanding this is important for honest evaluation."

---

## SLIDE 10 — Proposed Methodology

> (Is slide k leay alag file hai: **04_methodology_explained.md** — woh parh k bolna)

---

## SLIDE 11 — References

**Bolna:**
> "Sir, these are the key references that support this work. The two most closely related papers are DA-MAPPO by Sheng et al. and IGAT-MARL by Rezaee et al. — both published in 2026. These two papers are the direct motivation for this research."

---

## SLIDE 12 — Thank You

**Bolna:**
> "Sir, that concludes my presentation. The core contribution of this work is the Priority Arbitration Head — the first learned mechanism in multi-UAV coordination that dynamically resolves the assignment-avoidance trade-off at every decision step. I am happy to answer any questions."

---

## Agar Sir Koi Sawaal Poochein:

**Q: What is your main contribution?**
> "Sir, the main contribution is the Priority Arbitration Head — a lightweight neural module that learns to dynamically weight target assignment and collision avoidance at every timestep based on the drone's current situation. No existing framework does this — all prior work uses fixed, hand-tuned reward coefficients."

**Q: Why MAPPO specifically?**
> "Sir, DA-MAPPO — which is our closest related paper — already validated MAPPO for the target assignment problem. And IGAT-MARL also uses a graph attention based MARL. MAPPO has been shown by Yu et al. to be surprisingly competitive with more complex MARL algorithms. So it is a well-validated baseline and the right choice for this work."

**Q: Why 2D environment?**
> "Sir, both DA-MAPPO and IGAT-MARL operate in 2D environments. Our goal is first to solve the coupling problem in 2D — prove that a learned priority mechanism works — before extending to 3D. The coupling problem exists in 2D as well and has never been solved there."

**Q: What are the limitations?**
> "Sir, the framework is currently 2D only. Extension to 3D adds altitude-based collision risks which we have not addressed. Also, the curriculum learning stages are based on configurations validated by prior work — we have not yet discovered our own optimal curriculum. These are honest limitations we acknowledge."

**Q: What is alpha?**
> "Sir, alpha is the dynamic weight output by the Priority Arbitration Head. It is a single number between 0 and 1. When alpha is close to 1, assignment is prioritized. When alpha is close to 0, avoidance is prioritized. The head learns to set this value appropriately based on time-to-collision, distance to target, and number of conflicting neighbors."
