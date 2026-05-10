# 06 — Presentation Guide: Script + Q&A

---

## Suggested Opening (word for word)

> "Good morning/afternoon, sir. Today I'd like to present a paper titled 'Multi-UAV Simultaneous Target Assignment and Path Planning Based on Deep Reinforcement Learning in Dynamic Multiple Obstacles Environments' by Kong, Zhou, Li, and Wang, published in Frontiers in Neurorobotics in January 2024.
>
> This paper addresses the problem of how a team of drones can decide which target each drone should fly to, and how to get there safely — both at the same time — in a 3D environment where obstacles are constantly moving. The authors propose a novel deep reinforcement learning algorithm called TANet-TD3 and demonstrate that it achieves complete target coverage and collision-free navigation significantly better than existing methods."

---

## Main Points to Cover (in order)

```
1. THE PROBLEM
   Say: "When we send multiple drones on a mission, there are two key decisions to make:
   first, which drone goes to which target — this is target assignment — and second,
   how does each drone actually fly there without hitting things — this is path planning.
   Traditional systems do these one after the other: assign first, then plan. But in
   a dynamic environment where obstacles are moving, the initial assignment quickly
   becomes outdated. Two drones may end up heading for the same target, or a drone
   may be assigned to a target that's now blocked by obstacles. The challenge is making
   both decisions simultaneously, in real time, with limited sensor vision."

2. WHY EXISTING SOLUTIONS WEREN'T ENOUGH
   Say: "Classical algorithms like A-star, RRT, and PSO require a complete global map of
   the environment, which isn't available when obstacles are moving unpredictably.
   Prior deep reinforcement learning approaches either assigned targets first and planned
   later — which fails in dynamic settings — or used simple distance-based assignment
   that ignores obstacles entirely. One prior work using MADDPG could assign targets
   but sometimes had two drones reach the same target, leaving one target uncovered.
   None of the prior work handled simultaneous assignment and planning in 3D dynamic
   environments with partial observability."

3. THE PROPOSED APPROACH
   Say: "The authors propose TANet-TD3 — a Twin-Delayed Deep Deterministic Policy
   Gradient algorithm enhanced with a Target Assignment Network. The key idea is
   that instead of assigning targets once at the start, the system re-evaluates which
   target each drone should go to at every single step. A neural network — the TANet —
   continuously outputs the probability of each target being the best assignment for
   each drone. The TD3 algorithm then handles the actual navigation — computing
   which direction and force to apply to fly toward the assigned target while
   avoiding obstacles and other drones."

4. KEY METHODOLOGY
   Say: "The clever part is how the TANet is trained. You can't hand-label 'correct
   assignments' manually for millions of steps. Instead, the system generates its own
   labels. At each step, the TD3 algorithm computes Q-values — long-term expected
   rewards — for every possible drone-target pairing, forming a matrix. The Hungarian
   algorithm then finds the optimal one-to-one assignment that maximizes total
   Q-values across all drones. This becomes the training label for the TANet. So the
   path planner teaches the assignment network, and the assignment network guides the
   path planner — they improve each other simultaneously."

5. THE RESULTS
   Say: "In training experiments with five drones, five targets, and twenty moving
   obstacles, TANet-TD3 achieves a mean target completion rate of 83.77 percent in
   dynamic environments and 84.27 percent in mixed environments — outperforming the
   best baseline by over 3 percentage points, and outperforming distance-based methods
   by over 10 percentage points. More dramatically, in direct test scenarios, TANet-TD3
   successfully covers all five targets with zero collisions, while the best prior
   method covers only four out of five in dynamic environments and just two out of five
   in the harder mixed environment. TANet-TD3 also converges approximately 2,000
   episodes faster than distance-based methods."

6. SIGNIFICANCE AND CONTRIBUTION
   Say: "The paper makes three contributions: it's the first method to solve target
   assignment and path planning simultaneously in 3D dynamic environments with partial
   observability; it introduces a self-supervised label generation mechanism using
   Q-values and the Hungarian algorithm to train the assignment network; and it
   demonstrates robust scalability — even with 7 drones and 30 moving obstacles,
   the method maintains above 71 percent target completion. This work has clear
   applications in military operations, search and rescue, and autonomous delivery
   swarms where reliable, complete mission execution in unpredictable environments
   is critical."
```

---

## Anticipated Questions & Model Answers

| Question Sir Might Ask | What Ayesha Should Say |
|---|---|
| **What is the main contribution of this paper?** | "The main contribution is TANet-TD3 — the first method to solve target assignment and path planning *simultaneously* in 3D dynamic environments under partial observability. Previous methods separated these two problems, which fails when the environment changes. The novel part is how training labels are generated: by running TD3 across every possible target assignment and using the Hungarian algorithm to find the optimal complete matching, which becomes the label for the assignment neural network. This way the path planner and assignment network train each other." |
| **What makes this approach different from previous work?** | "Two main differences. First, existing methods like Qie et al. assign targets first, then plan paths — TANet-TD3 does both at every single timestep. Second, existing assignment methods use distance as the deciding factor, which ignores obstacles. TANet-TD3 uses Q-values from TD3 which naturally encode obstacle information, distance, and the presence of other drones — so the assignment is obstacle-aware. In testing, Qie et al.'s approach caused two drones to reach the same target; TANet-TD3 guarantees a complete one-to-one assignment via the Hungarian algorithm." |
| **What are the limitations of this work?** | "The main limitation is that all experiments are simulation-only — there's no real hardware testing. Sim-to-real transfer is very challenging in robotics because real drones have sensor noise, wind, battery constraints, and actuator imperfections that simulators don't model. The paper also only tests up to 7 drones, so we don't know how it scales to larger swarms. Additionally, targets are stationary — extending to moving targets like pursuit scenarios would require further work." |
| **What evaluation metric did they use? Is it appropriate?** | "The main metric is average target completion rate — the fraction of targets that get a drone assigned and arrived across all test episodes. This is appropriate because the core mission goal is complete target coverage. They also track average reward, which reflects path length and collision rate combined, and average arrival rate, which measures individual drone success. Together these three metrics capture the key aspects: mission success, efficiency, and safety. I think the metrics are well-chosen for this problem." |
| **What dataset was used and why?** | "There is no external dataset — the authors built their own 3D simulation environment using the OpenAI Gym platform. All data is generated through simulation: drones, targets, and obstacles are randomly initialized each episode. This is standard practice for DRL research because the algorithm needs millions of interaction samples to learn, which would be impossible to collect on real hardware. The simulation environment covers a 2-by-2-by-2 cubic space with 5 UAVs, 5 targets, and up to 30 obstacles." |
| **Could this approach be applied to a related problem?** | "Yes, definitely. The framework could be extended to multi-robot warehouse logistics — where robots need to be assigned to packages and plan routes through a dynamic warehouse with human workers as moving obstacles. The TANet component could be adapted for any multi-agent task assignment problem, and the TD3 path planner is applicable to any continuous navigation problem. The authors themselves suggest extending to multi-UAV target search and target-tracking tasks in future work." |
| **What would you change if you were the author?** | "I would add a real hardware validation component, even on a small scale with 2–3 physical drones, to test sim-to-real transfer. I'd also compare against MADDPG from Qie et al., which is the most directly comparable prior work but is curiously absent from the baselines. Finally, I'd add a computational efficiency analysis — the paper doesn't report inference time per step, which matters greatly for real-time drone control." |
| **What future work do the authors suggest?** | "The authors suggest three directions: first, applying the method to multi-UAV target search and target-tracking tasks where targets are not stationary. Second, studying how to compute the Q-value matrix efficiently for high-dimensional scenarios with many targets — currently the method traverses all targets for each drone at every step, which becomes expensive with many targets. Third, building a more realistic simulation environment with complex obstacle shapes and movement patterns." |
| **Do you find the results convincing? Why?** | "Mostly yes. The results are convincing because the comparison is systematic and well-controlled — four algorithms tested across two environments, with 1,000 episodes per statistical experiment. The qualitative trajectory figures (Figures 11–14) visually confirm the quantitative numbers. The most convincing result is the test scenario where TANet-DDPG fails 60% of targets in the mixed environment while TANet-TD3 succeeds completely. What I find less convincing is the absence of real hardware validation — simulation results don't always transfer to physical systems." |
| **How does this compare to the Hungarian algorithm alone?** | "The Hungarian algorithm alone needs the full Q-value matrix computed upfront — which requires knowing the global environment. In TANet-TD3, the Hungarian algorithm is used *during training* only, to generate labels. At *deployment time*, the trained TANet network makes assignments in a single forward pass based only on local sensor observations, with no Hungarian computation needed. So the deployed system is fully decentralized and fast, even though training uses the Hungarian algorithm." |

---

## What NOT to Say

1. **Don't say** "the drones communicate with each other." They don't — each drone only observes nearby objects with sensors. There is no explicit communication channel.
2. **Don't say** "this was tested on real drones." It was simulation only.
3. **Don't say** "TD3 is the only algorithm that works here." TD3 is *better* than DDPG, but both can be made to work with TANet; TANet-TD3 is simply more effective.
4. **Don't say** "the method guarantees 100% mission completion." It achieves 84% completion rate, not 100%. Even the best case leaves ~16% episodes incomplete.
5. **Don't overstate the scale:** This is tested with up to 7 drones and 30 obstacles — not hundreds of drones in real airspace.

---

## Closing Statement

> "In summary, this paper presents TANet-TD3, a deep reinforcement learning framework that simultaneously solves two traditionally separate problems — target assignment and path planning — for drone swarms in dynamic 3D environments. The system learns robust coordination strategies purely from simulation experience, without any manually designed rules or global map requirements. The results show consistent superiority over all baselines across varied conditions, with the most dramatic improvement seen in complex mixed-obstacle environments. Thank you, sir."

---

## If You Forget Something

> "If you blank on a detail, you can always say: 'The paper mentions that — let me recall the exact figure, but the key point is that TANet-TD3 outperforms all baselines across every tested condition, with the largest gaps appearing in the most challenging scenarios.'"
