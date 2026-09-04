# The Assignment Oscillation Problem — Deep Dive

---

## What Is Actually Happening?

Imagine three drones and three moving targets. At every single step, the system runs a Hungarian algorithm that asks: "given current distances, which drone should chase which target?" It reassigns based on whoever is closest.

Now watch what happens when two targets are roughly equidistant from two drones:

```
Step 1:  Drone A is 10m from Target 1,  Drone B is 12m from Target 2
         Assignment: A → Target 1,  B → Target 2

Step 2:  Targets move slightly. Now Drone A is 11m from Target 1, Drone B is 10m from Target 1
         Assignment flips: A → Target 2,  B → Target 1

Step 3:  Targets shift again.
         Assignment flips back: A → Target 1,  B → Target 2

Step 4:  Flips again.
```

Both drones are turning around constantly. Neither is making real progress. The algorithm is "working correctly" at every individual step, but the collective behavior is useless.

This is assignment oscillation.

---

## Why Does It Happen?

The Hungarian algorithm is greedy in one sense: it is optimal for the current snapshot in time. It has no memory of what the assignment was one step ago. It does not know or care that drone A was already heading toward target 1 and was almost there.

Every step is treated as if the mission just started.

When targets are moving, the cost matrix (a table of distances between every drone and every target) changes every step. Small movements in targets cause the optimal assignment to flip back and forth when two drones are in a near-tie for a target. The algorithm picks the globally optimal assignment at each snapshot, but the sequence of snapshots creates chaotic switching.

---

## Why Is This Worse at Scale?

With 3 drones: maybe 1 pair of drones is in a near-tie at any given moment.

With 10 drones: statistically, several pairs are in near-ties at once. More oscillation, more drones spinning around, lower overall efficiency.

With 20 drones: the problem compounds. In dense swarms, drones are close together and targets are relatively nearby multiple drones simultaneously. The near-tie condition becomes the normal condition rather than the exception.

This is exactly why this is a scalability problem, not just a small-swarm problem. It gets worse as N grows.

---

## What Does DA-MAPPO Say About This?

DA-MAPPO (the 2026 paper that introduced per-step reassignment) raises this concern explicitly in its open questions section:

> "Does per-step allocation help when assignments become unstable? If targets oscillate back and forth, the allocation might also oscillate, causing drones to constantly switch targets."

The paper never answers this. It does not measure how often oscillation occurs. It does not test at fast target speeds where oscillation would be more severe. It only tested with three drones where the probability of near-ties is low. The problem is documented and then left open.

---

## What Does Oscillation Look Like in the Numbers?

Here is a simple way to see it. Define:

- **Assignment switches per episode (ASE):** how many times any drone changes its assigned target during one mission
- **Net progress per step:** how much closer the average drone gets to its target each step
- **Mission success rate:** fraction of episodes where all drones reach their targets

When oscillation is absent:
- ASE is low (drones stick to assignments)
- Net progress is steady and positive
- Success rate is high

When oscillation is severe:
- ASE is very high (drones flip constantly)
- Net progress is near zero or even negative (drones move away from targets they were just approaching)
- Success rate drops significantly

Nobody has measured these three things together across a range of target speeds. That measurement itself is a research contribution.

---

## The Specific Research Question

> At what target speed does per-step minimum-cost assignment cause assignment oscillation severe enough to meaningfully reduce mission success rate, and can a stability-aware assignment criterion prevent this degradation?

Break that into two parts:

**Part 1 (Diagnosis):** Run experiments with varying target speeds. Measure ASE and success rate at each speed. Find the threshold where the system breaks down. This produces a curve showing exactly where and how fast performance degrades. No existing paper has this curve.

**Part 2 (Fix):** Design a stability constraint. The simplest version: do not reassign drone A from target X to target Y unless the cost improvement exceeds a threshold T. This is called a hysteresis constraint (borrowed from control systems — a thermostat uses hysteresis so it does not turn on and off every second). Measure whether this simple constraint eliminates the degradation from Part 1.

---

## What Would the Fix Look Like?

The current assignment rule (pure Hungarian):

```
At each step, assign drones to targets by minimizing total distance.
Always pick the globally optimal assignment.
```

The proposed stability-aware rule:

```
At each step, compute the optimal assignment.
For each drone, only switch its assignment if the cost saving
from switching exceeds a threshold T.
Otherwise, keep the current assignment.
```

This is a small but non-obvious change. It introduces a trade-off:
- Too small T: still oscillates (threshold not strict enough)
- Too large T: drones never reassign even when they should (misses legitimate target movements)
- Right T: prevents oscillation while still reacting to real positional changes

Finding the right T — and whether it should be fixed or learned — is the interesting research question.

There is also a more sophisticated version: instead of a fixed threshold, train a small neural network that decides whether to reassign at each step based on the history of past assignments, current distances, and target velocities. This is a learned hysteresis policy. It is harder to implement but potentially better because it adapts to the environment rather than using a hand-tuned threshold.

---

## What Makes This Novel?

| Aspect | What exists | What this adds |
|--------|-------------|----------------|
| Per-step assignment | DA-MAPPO (2026) introduced it | Studies its failure mode which DA-MAPPO never investigated |
| Assignment stability | Control systems use hysteresis | Never applied to multi-UAV MARL assignment |
| Scalability of assignment | Paper 4 scales using mean-field (no assignment) | Studies how assignment quality degrades as N grows |
| Target speed sensitivity | No paper measures this | First characterization of the speed-oscillation relationship |

This is not reproducing DA-MAPPO. It is specifically studying the failure case that DA-MAPPO left open and providing a fix.

---

## What Are the Experiments?

**Experiment 1: Characterize the failure (the diagnosis)**
- Fix N=5 drones, 5 targets
- Vary target speed from 0 (static) to fast (targets move as fast as drones)
- At each speed, measure: ASE, net progress per step, mission success rate
- Expected result: a clear breakpoint where success drops sharply
- This alone is publishable as a negative result showing where current methods fail

**Experiment 2: The hysteresis fix**
- Same setup as Experiment 1
- Add the stability threshold T to the assignment rule
- Sweep T values and measure the same metrics
- Expected result: an optimal T that recovers most of the lost performance

**Experiment 3: Learned vs. fixed threshold**
- Compare fixed T (hand-tuned) vs. learned threshold (small network)
- Measure performance across different environments
- Expected result: learned threshold generalizes better to unseen target movement patterns

**Experiment 4: Scalability**
- Fix a moderate target speed (somewhere in the failure zone from Experiment 1)
- Vary N from 3 to 15 drones
- Compare: pure per-step assignment vs. stability-constrained assignment
- Expected result: the gap between them widens as N grows, confirming this is a scalability problem

---

## How Is This Different from What the Teacher Rejected?

The previous proposal said: "combine paper X and paper Y in 3D."
A reviewer could reject that by saying: "just run them sequentially, what is your actual scientific contribution?"

This proposal says: "current assignment methods fail in a specific, measurable way when targets move fast, and we have a specific hypothesis about why and a specific fix to test."
A reviewer cannot reject that with the same argument. The failure mode is real. The question is falsifiable. The fix is non-trivial.

---

## One-Line Summary for Your Teacher

> "Per-step Hungarian assignment in multi-UAV coordination produces oscillation when targets move fast — drones constantly switch targets and make no progress. No existing paper has measured when this happens or how to prevent it. This research characterizes that failure and proposes a stability constraint to fix it."

---

## What You Should Know Before Presenting This

1. **Hungarian algorithm** — an algorithm that finds the optimal one-to-one assignment between two sets (drones and targets) by minimizing total cost (usually distance). Runs in O(N³) time.

2. **Oscillation** — when a system keeps switching between two states without settling. In this context, drones keep swapping assignments back and forth.

3. **Hysteresis** — a principle from control systems where you only trigger a change if the signal crosses a threshold, preventing rapid back-and-forth switching. A thermostat is the classic example: it turns on at 18°C and turns off at 22°C, not at exactly 20°C both ways.

4. **Assignment stability** — a property of an assignment mechanism where small changes in the input (target positions) do not cause large changes in the output (who chases whom).

5. **Near-tie condition** — when two drones are almost equally far from a target, so the optimal assignment is extremely sensitive to tiny movements.

---

*Read this file fully before we proceed to the proposal document.*
