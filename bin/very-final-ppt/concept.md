# Concepts — Har Term Samjho
### Source: CUI_Synopsis_AYESHA_KHALIL-SP25-RCS-009_FIXED.docx

---

## ⭐ MAPPO (Multi-Agent Proximal Policy Optimization)

**Ek line:** Algorithm jo multiple drones ko saath kaam karna sikhata hai, trial-and-error se.

**Analogy:** PPO ek single student hai jo exam ke baad apna approach thoda adjust karta hai. MAPPO ek class hai — sab students apna kaam karte hain, lekin teacher (centralized critic) sab ka performance dekhta hai.

**Is research mein:** Backbone algorithm. PAH MAPPO actor ke saath jointly train hota hai.

---

## ⭐ Priority Arbitration Head (PAH) — MAIN CONTRIBUTION

**Ek line:** Chhota neural network jo har second decide karta hai — target ki taraf jaana zyada zaroori hai ya collision se bachna — aur yeh seekhta hai, fix nahi hota.

**Architecture:** 2 layers, 64 neurons, sigmoid output (range 0 to 1)

**Inputs:**
- τ_collision — time-to-collision (seconds)
- d_target — distance to assigned target (meters)
- n_conflict — conflict neighbor count

**Output:** α ∈ [0,1]

**Formula:** `r_total = α × r_assignment + (1−α) × r_avoidance`

**Why novel:** Existing frameworks (DA-MAPPO, IGAT-MARL) use FIXED weights. PAH learns the weight dynamically.

---

## ⭐ CTDE (Centralized Training, Decentralized Execution)

**Ek line:** Training mein sab drones ka data use karo, deployment mein har drone apna local data use kare.

**Analogy:** Army training camp (centralized — commander dekhta hai sab kuch) vs actual battle (decentralized — har soldier khud decide karta hai).

**Is research mein:** Centralized critic training mein full joint state dekhta hai. Deployment mein har drone sirf apna observation vector use karta hai.

---

## ⭐ Hungarian Algorithm

**Ek line:** Minimum-cost assignment find karne ka mathematical method — n drones, n targets, optimal pairing.

**Is research mein:** Har decision step pe chalaya jaata hai, drone ke observation vector mein target ki relative position daalta hai.

**DA-MAPPO connection:** DA-MAPPO ne pehli baar yeh real-time observation mein encode kiya — 90-99% success achieve hua.

---

## ⭐ Conflict Graph

**Ek line:** Ek graph jisme sirf woh drone pairs connected hain jo collision course pe hain — sab se connection nahi.

**Is research mein:** Observation vector ka element 3 — sirf conflict neighbors ki position/velocity include hoti hai.

**IGAT-MARL connection:** IGAT-MARL ne yeh propose kiya — 44% interaction edges kam, better avoidance.

---

## ⭐ Dec-POMDP

**Ek line:** Multi-agent problems ka formal framework jahan har agent partial information rakhta hai, independently decide karta hai.

**Breakdown:**
- Decentralized — koi central authority nahi
- Partially Observable — koi bhi drone poori duniya nahi dekhta
- Markov — future sirf present state pe depend karta hai
- Decision Process — sequence of actions aur rewards

---

## ⭐ Curriculum Learning

**Ek line:** Simple se shuru karo, dhire dhire complexity badhao.

**4 Stages (is research mein):**
1. 3 drones, static targets, 2D — DA-MAPPO replicate, baseline validate
2. 5 drones, moving targets, kuch obstacles
3. 8 drones, high obstacle density, dynamic targets
4. Generalization — unseen swarm sizes test

---

## ⭐ Fixed Reward Coefficients vs Learned α — THE CORE GAP

**Existing frameworks:**
```
r_total = C1 × r_assignment + C2 × r_avoidance
```
C1, C2 = constants, never change

**Proposed framework:**
```
r_total = α × r_assignment + (1−α) × r_avoidance
```
α = PAH ka output, changes every timestep

**Yahi gap hai. Yahi novelty hai.**

---

## ⭐ DA-MAPPO (Sheng et al., 2026) — Primary Baseline

- Real-time Hungarian assignment + MAPPO
- Mission success: 90-99%
- Ablation: bina assignment ke success 0%
- Weakness: collision avoidance = fixed penalty constant
- 2D environment

---

## ⭐ IGAT-MARL (Rezaee et al., 2026) — Secondary Baseline

- Sparse conflict graph + Graph Attention Network
- 44% fewer interaction edges
- 17% higher cumulative reward
- 10% fewer separation violations
- Weakness: fixed targets assumed, fixed reward weights
- 2D environment

---

## ⭐ Mission Success Rate

**Ek line:** Percentage of episodes jisme SAARE drones apne target reach karein, ZERO collisions, time limit ke andar.

**Secondary metrics:** inter-drone collision count, obstacle collision count, target reassignments per episode, average trajectory length.

---

## ⭐ Ablation Study

**Ek line:** Ek ek component hatao, dekho performance kitni girti hai.

**Is research ka plan:** Learned α vs Fixed α (0.3, 0.5, 0.7) — yeh comparison PAH ka contribution prove karta hai.
