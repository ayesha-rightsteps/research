# The Concept — in plain language

Read this first. It explains what this research actually is, with no jargon.
The precise version is in `00_problem_formalization.md`; this is the "so what
are we even building" version.

---

## 1. The real-world problem

Picture an earthquake. A building has collapsed. Five drones are sent over the
rubble — each one has to reach a different spot (where someone might be trapped).

Every drone has to do two things at the same time:

- **Reach its spot** — the *mission*
- **Not crash** into another drone or a wall — *safety*

## 2. These two jobs fight each other

Two drones are heading toward each other:

- If a drone only thinks about its destination → it flies straight → **crash**
- If a drone only thinks about not crashing → it swerves away → **destination
  missed, mission fails**

So every moment, each drone has to decide: **"right now, what matters more —
getting there, or staying safe?"**

## 3. How this is done today

People set one fixed number. For example:

> "always 70% attention on the destination, 30% on avoiding collisions"

That number is called **α (alpha)**.

The problem: the number **never changes**. When the path is clear, 30% is wasted
on avoidance. When a crash is about to happen, 30% is nowhere near enough. One
setting for every situation — it can't be right for all of them.

## 4. The idea (this is the thesis)

> Don't fix α. Add a small "brain" that decides α **every moment**, based on the
> situation.

This small brain is called the **Priority Arbitration Head (PAH)**. It looks at
three things:

1. How much time is left before a collision
2. How far away the destination is
3. How many other drones are nearby

…and it moves α up and down:

- Path clear → α ≈ 0.9 (focus on the destination)
- Collision close → α ≈ 0.2 (focus on avoiding it)
- Danger passed → back to α ≈ 0.9

That's the whole contribution: a **knob that turns itself** based on the
situation, instead of a knob fixed by hand.

## 5. What "learning" means here

The drone is given no rulebook. It plays a video-game version of the problem
thousands of times:

- Did well (reached the spot, no crash) → **+points**
- Did badly (crashed) → **−points**

After thousands of games it works out the pattern on its own. This is
**reinforcement learning** — like a child learning to ride a bike by falling
over and over. PAH learns, the same way, when to set α high and when to set it
low.

## 6. How we'll know if the idea works

Build two versions and race them in the same simulation:

- **Version A:** fixed α (the old way)
- **Version B:** PAH's self-adjusting α (the new way)

Run both 200 times. Count how often *all* drones reach their spots with *no*
collisions.

- B beats A → the thesis claim holds ✓
- B ≈ A or worse → the claim doesn't hold; we write up honestly why (still a
  valid thesis)

## 7. Scope — what this is and isn't

- It is a **2D simulation**: dots on a flat grid. Drones are points — no size,
  no weight, no wind.
- 3 to 8 drones. Small on purpose.
- No real drone, no deployment, no user. The output is a **thesis** (and maybe a
  paper).
- It is a modest, well-scoped piece of research — one small improvement on an
  existing method. That is exactly what an MS thesis should be.

## 8. The one thing currently wrong in the code

PAH is built, but the way it is being *taught* has a bug.

Right now the code tells PAH: *"each moment, see which reward is bigger and turn
α toward it."* That is a shortcut — the drone doesn't actually get better, it
just games its own score.

Result: α gets stuck at one value (~0.1), and PAH becomes a **bad fixed knob** —
which means the new idea doesn't get a fair test.

The fix: teach PAH from **how the whole episode turned out**, not from the
reward of the current step. This is the open question for the supervisor
(`04_open_questions_for_supervisor.md`, Q4–Q5) and it should be settled before
the PAH experiments are run.
