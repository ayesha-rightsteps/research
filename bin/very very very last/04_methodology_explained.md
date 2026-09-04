# Proposed Methodology — Detailed Explanation
### Slide 10 k leay — poori methodology simple alfaz mein

---

## Pehle Ek Line Mein Bolna:
> "Sir, our framework is MAPPO-based and has one central new component — the Priority Arbitration Head. Let me explain how the entire system works."

---

## FRAMEWORK KA OVERVIEW

Humara framework 4 main parts mein hai:
1. **2D Simulation Environment** — jahan drones fly karte hain
2. **Observation Builder** — har drone ko kya pata hota hai
3. **MAPPO Actor + Priority Arbitration Head** — drone kya decide karta hai
4. **Centralized Critic** — training k waqt sab ki state dekhta hai

---

## PART 1 — Environment

**Simple matlab:**
- 2D simulation environment — jaise ek flat map
- Drones: pehle 3, phir 5, phir 8 (curriculum learning)
- Targets: dynamic — move bhi kar sakte hain
- Obstacles: static aur dynamic dono
- Time limit: har episode mein drones ko time limit k andar targets tak pahunchna hai

---

## PART 2 — Observation Builder
### Har Drone Ko Yeh 4 Cheezein Pata Hoti Hain:

**① Self-State**
- Drone ki apni 2D position: (x, y)
- Drone ki apni velocity: (vx, vy)
- Matlab: mujhe pata hai main kahan hoon aur kitni speed se ja raha hoon

**② Assignment State — Hungarian Algorithm**
- Har decision step pe Hungarian algorithm run hota hai
- Yeh decide karta hai kaunsa drone kaunse target ko jaaye — minimum total cost
- Drone ko apne assigned target ki relative position pata hoti hai
- Matlab: mujhe pata hai mera target kahan hai aur kitna door hai

**③ Conflict Graph — Collision-Course Pairs**
- Har decision step pe check hota hai — kaunse drones collision course pe hain
- Sirf woh drones observe karo jو actually conflict mein hain (sparse graph — IGAT-MARL say liya)
- Matlab: mujhe pata hai kaun kaun mere raaste mein aa sakta hai

**④ Obstacle Proximity**
- 4 directions mein obstacles ki proximity
- Matlab: mujhe pata hai mere aas paas kya obstacles hain

**Yeh sab mila k banta hai Joint Observation Vector.**

---

## PART 3A — MAPPO Decentralized Actor

**Simple matlab:**
- Joint observation vector leta hai
- Output deta hai: 2D velocity action — kahan jaana hai aur kitni speed se
- Har drone ka apna actor hota hai
- Deployment mein akela decide karta hai — centralized information nahi chahiye

---

## PART 3B — Priority Arbitration Head (PAH)
### Yeh Is Research Ki Core Contribution Hai

**Simple matlab:**
Ek chota neural network jo ek sawaal ka jawab deta hai:
> "Abhi is waqt, is drone k leay — zyada zaroori kya hai? Target tak pahunchna ya collision say bachna?"

**PAH k 3 Inputs:**
1. **τ_collision (time-to-collision)** — kitne waqt mein collision ho sakti hai nearest conflict neighbor say. Kam waqt = zyada danger
2. **d_target (distance to target)** — assigned target kitna door hai. Door = urgent nahi
3. **n_conflict (conflict neighbor count)** — kitne drones abhi conflict zone mein hain. Zyada = avoidance urgent

**PAH ka Output:**
- **Alpha (α)** — ek number 0 say 1 k beech
- Alpha = 1: assignment dominant — target pe focus karo
- Alpha = 0: avoidance dominant — collision say bacho
- Alpha = 0.5: balanced — dono equally important

**Reward Formula:**
```
r_total = α × r_assignment + (1−α) × r_avoidance
```

**Matlab:** Alpha decide karta hai kitna weight assignment reward ko dena hai aur kitna avoidance reward ko.

**Training:**
- PAH MAPPO actor k saath jointly train hota hai
- Ek hi policy gradient update dono ko update karta hai
- Koi alag training loop nahi

---

## PART 4 — Centralized Critic

**Simple matlab:**
- Sirf training k waqt use hota hai
- Deployment mein nahi hota
- Training mein saare drones ki poori state dekhta hai
- Value estimate karta hai — yeh decision kitna acha tha?
- Is information say MAPPO actor aur PAH dono better seekhte hain

---

## TRAINING STRATEGY — Curriculum Learning

**4 Stages:**

| Stage | Drones | Environment | Targets |
|---|---|---|---|
| 1 | 3 | Static obstacles | Static — validate baseline |
| 2 | 5 | Some obstacles | Moving targets |
| 3 | 8 | High obstacle density | Dynamic targets |
| 4 | Unseen sizes | Generalization test | — |

**Matlab:** Pehle asaan seekho, phir mushkil. Stage 1 mein DA-MAPPO ko replicate karo as baseline. Phir progressively mushkil banao.

---

## EVALUATION — Kaise Results Measure Hain

**Primary Metric:**
- **Mission Success Rate** — kitne percent episodes mein saare drones targets tak pahunche, bina collision k, time limit k andar

**Secondary Metrics:**
- Inter-drone collision count
- Obstacle collision count
- Target reassignments per episode
- Average trajectory length per drone

**Test Configurations:**
- 3 swarm sizes: 3, 5, 8 drones
- 3 obstacle densities: 30, 40, 50 obstacles

**4 Baselines:**
1. Standard MAPPO — no assignment, no conflict graph
2. DA-MAPPO ported to our environment — no conflict graph
3. IGAT-MARL with fixed assignment — no PAH
4. Fixed alpha baselines — α = 0.3, 0.5, 0.7 (hand-tuned, not learned)

**Matlab:** Hum apna PAH (learned alpha) compare karein gay fixed alpha say. Agar learned alpha better hai — research proven.

---

## Methodology Ko Ek Line Mein Bolna

> "Sir, our framework extends MAPPO with a Priority Arbitration Head that learns at every timestep whether to prioritize reaching the target or avoiding a collision, replacing the fixed reward coefficients used in all prior work."

---

## Agar Sir Methodology Pe Sawaal Poochhein

**Q: Why jointly train PAH with the actor?**
> "Sir, if PAH were trained separately, there would be a mismatch — the actor would not know how to respond to the alpha values PAH produces, and PAH would not know how the actor uses its output. Joint training ensures both modules are optimized together for the same objective."

**Q: Why three specific inputs to PAH?**
> "Sir, these three inputs capture the complete situational context for the arbitration decision. Time-to-collision tells how urgent the safety concern is. Distance to target tells how urgent the assignment concern is. Conflict neighbor count tells how many simultaneous conflicts exist. Together these three scalars are sufficient to make the priority decision."

**Q: How is this different from just tuning the reward weights?**
> "Sir, tuned fixed weights are set once before training and never change. In a scenario where a drone is very close to a collision, a fixed weight of 0.5 still gives equal importance to assignment — which may cause the drone to keep moving toward the target and collide. Our learned alpha adapts — in that same scenario alpha would approach 0, giving full priority to avoidance. This situational adaptability is what makes PAH novel."
