# Dono Naye Papers — Ayesha ke liye
### Paper A: HPER-D3QN | Paper B: STAAC

---

## Pehle yeh samjho — dono papers kyun aaye

Committee ne reject kiya tha yeh kehte hue ke "comparative study hai." Tab Priority Arbitration ka idea aaya. Phir yeh dono papers mile. Yeh papers isliye important hain kyunki:

- Dono 2025-2026 ke hain — bilkul latest literature
- Dono UAV collision avoidance mein hain — directly related
- **Dono mein bhi wahi limitation hai jo hamari research address karti hai**

Matlab yeh papers reject ka jawab nahi hain — yeh **research gap ka aur zyada proof** hain.

---

## Paper A — HPER-D3QN

**Full Title:** Deep reinforcement learning-based adaptive collision avoidance method for UAV in joint operational airspace

**Authors:** Yan Shen, Xuejun Zhang, Yan Li, Weidong Zhang — Beihang University, Beijing

**Published:** Defence Technology, Vol. 56, 2026, pp. 142–159 (online September 2025)

**Setting:** Ek akela UAV, ek mixed airspace mein jahan manned aircraft (commercial planes), unmanned drones, aur dynamic wind sab saath hain

**Important:** Yeh SINGLE AGENT paper hai — ek hi UAV seekhta hai. Multi-agent nahi.

---

### Problem jo yeh paper solve karta hai

Real battlefield airspace mein UAV ko:
- Manned aircraft se bachna hai (bade, fast, alag dynamics)
- Doosre small drones se bachna hai
- Wind disturbance handle karna hai
- Apne target tak pohanchna bhi hai

Pehle ke papers sirf Euclidean distance se threat measure karte the — jo bahut naive approach hai. Ek airplane jo 200m door hai par seedhi collision course pe hai vs ek airplane jo 50m door hai par alag direction mein ja rahi hai — dono ka same "threat" nahi hota.

---

### Novel Contribution 1 — DTPA (Dynamic Threat Prioritization Assessment)

**Kya karta hai:** Har aircraft ko ek threat score deta hai, sirf distance se nahi, multiple factors se.

**Formula (paper se actual):**
```
S = ωt × normalize(TCPA) + ωd × normalize(DCPA) + ωtype × κ
```

| Parameter | Kya hai | Value |
|---|---|---|
| TCPA | Time to Closest Point of Approach — kitne seconds mein sabse qareeb honge | Weight ωt = 0.4 |
| DCPA | Distance at Closest Point of Approach — us point pe kitni door honge | Weight ωd = 0.4 |
| Aircraft type κ | Manned = 0.75 (bada threat), Unmanned = 0.25 | Weight ωtype = 0.2 |

**Simple samjho:** Agar ek commercial airplane 8 seconds mein 2 meter door se guzregi, uska score bahut high hoga. Ek chhota drone 60 seconds mein 80 meter door se guzrega — low score. DTPA yeh difference pakadta hai. Sirf distance se tum yeh nahi pakad sakte.

Drone ke aaspaas ke airspace ko **8 sectors** mein divide kiya gaya hai. Har sector mein DTPA sabse dangerous aircraft identify karta hai aur usse "intruder" mark karta hai.

---

### Novel Contribution 2 — HPER (Hierarchical Prioritized Experience Replay)

**Problem:** Normal RL mein training experiences randomly sample kiye jaate hain. Lekin 95% time drone safe fly karta hai — safe flight episodes bahut zyada hain, dangerous ones bahut kam. Model safe cases se zyada seekhta hai, dangerous cases se kam.

**Solution:** Teen layers ka replay buffer:

| Layer | Kya store hota hai | Priority |
|---|---|---|
| Ehigh (High) | Arrival at target ∪ Collision ∪ Out-of-bounds | Sabse zyada sample |
| Emedium (Medium) | Warning zone entry (collision approach kar raha hai) | Medium |
| Elow (Low) | Normal safe flight (koi aircraft nearby nahi) | Kam sample |

Har layer ke andar **TD-error based sampling** bhi hai — jis experience se zyada seekhna baaki hai usse zyada sample karo.

**Sampling weight formula:**
```
λlayer = (Mlayer / M) × klayer
```
Jahaan klayer = priority scaling factor. High layer ke liye: scaling 1-3 tak set kiya gaya.

---

### Reward Function — FIXED Weights (Yeh Important Hai!)

Paper ki reward function:
```
r_total = r_goal + r_collision + r_warning + r_boundary + r_efficiency
```

Coefficients jo paper ne set kiye:
- C_goal = +2 (destination reach karna)
- C_collision = -1 (collision penalty)
- C_warning = -0.5 (warning zone entry)
- C_boundary = -0.5 (boundary violation)
- C_step = -0.005 (time penalty)

**Yeh weights hamesha same hain — chahe drone target ke qareeb ho ya collision se 2 seconds door.**

Agar drone clear airspace mein hai aur target 100m door hai, C_goal = +2 aur C_collision = -1.
Agar drone collision course pe hai aur target 100m door hai, STILL C_goal = +2 aur C_collision = -1.

Weights decide nahi karte "is moment mein kya zyada important hai."

---

### Results

| Scenario | HPER-D3QN Success Rate | Next Best (PER-D3QN) |
|---|---|---|
| 3 aircraft | 99.95% | 99.89% |
| 25 aircraft (hardest) | **96.28%** | 94.55% |

Ablation results (highest-density, uncertainty level 5):
- Remove DTPA: success rate drops 8.98%, Frequency of Hazardous Proximity (FHP) increases 92.54%
- Remove HPER: success rate drops 9.27%, FHP increases 87.26%

Also transferred to Unity3D high-fidelity simulation — generalized successfully.

---

### Paper A ka Ek Line Summary

HPER-D3QN kehta hai: **collision avoidance ke andar threats dynamically prioritize karo (DTPA) aur training experiences bhi dynamically prioritize karo (HPER) — dono se performance better hoti hai.** Lekin navigation vs avoidance ke beech balance tab bhi fixed hai.

---

---

## Paper B — STAAC

**Full Title:** Multi-Agent Reinforcement Learning with Spatial-Temporal Attention for Flocking with Collision Avoidance of a Scalable Fixed-Wing UAV Fleet

**Authors:** Chao Yan, Chang Wang, Han Zhou, Xiaojia Xiang, Xiangke Wang, Lincheng Shen — NUAA + NUDT

**Published:** IEEE Transactions on Intelligent Transportation Systems, Vol. 26, No. 2, February 2025, pp. 1769–1782

**Setting:** Multi-agent — ek leader, multiple followers (fixed-wing UAVs), aur external non-cooperative intruder drones

**Environment:** 2D, 1200m × 800m, scalable fleet size

---

### Problem jo yeh paper solve karta hai

Fixed-wing UAVs ek leader ke peeche fly kar rahi hain (flocking). Bahar se kuch non-cooperative intruder drones aa rahi hain. Fleet ka size variable hai — kabhi 5 followers, kabhi 10. Intruders ka number bhi vary karta hai.

Challenge: Ek policy jo 5 followers ke liye train hue woh 10 followers ke saath directly kaam kar sake? Existing methods ne separate models train kiye alag fleet sizes ke liye — wasteful aur impractical.

---

### Novel Contribution 1 — Population-Invariant Architecture

Ek model jo fleet size change hone pe bhi kaam kare — without retraining.

**Entity Clustering:** Har follower apne neighbors ko 4 groups mein divide karta hai:
1. **Self** — apni state
2. **Leader** — leader ki state
3. **Neighbor-followers** — doosre fleet drones
4. **Neighbor-intruders** — external threats

Har group ke liye alag processing — kyunki leader ko follow karna ek cheez hai, intruder se bachna bilkul alag cheez hai.

---

### Novel Contribution 2 — LSA (Local Spatial Attention)

Har group ke andar bhi sab entities equal nahi hain. Jo follower sabse qareeb hai woh zyada important hai. LSA yeh importance weight karta hai.

**Follower group ke liye spatial embedding:**
```
efol_i = Σj αij × FC(ξfol_j)
αij = softmax(βij)
βij = (ξself)ᵀ × Wfol × FC(ξfol_j) / √d
```

Matlab: attention weight (αij) decide karta hai ke j-th neighbor kitna important hai i ke liye. Yeh attention trained hai — manually set nahi.

**Output:** Group embedding jo fleet size ke sath scale karta hai — 5 followers ho ya 10, embedding size same rehti hai.

---

### Novel Contribution 3 — GTA (Global Temporal Attention)

UAV sirf abhi ki state nahi dekhta — **pichle 4 frames bhi dekhta hai**.

**Step 1:** Har group ke 4 historical frames ko ek LSTM process karta hai:
```
hlea_τ = LSTM(elea_τ, hlea_τ-1),   τ ∈ [t-3, t]
```

**Step 2:** Phir temporal attention decide karta hai kaun sa frame zyada important hai:
```
αglo_τ = softmax(FC(hglo_τ))
vi = Σ αglo_τ × hglo_τ
```

**Why this matters:** Agar ek intruder pichle 4 frames se seedha tumhari taraf aa raha hai — trajectory clear hai, threat high hai. Agar suddenly mura — different story. GTA yeh pattern pakadta hai.

---

### Learning Algorithm — STAAC

**Framework:** Dec-POMDP (Decentralized Partially Observable Markov Decision Process)

**Base:** MADDPG (Multi-Agent DDPG) + improvements:
- Parameter sharing — sab followers ek hi policy share karte hain (tabhi scalable hai)
- Clipped double Q-learning — 2 critics, min use karo (overestimation bias reduce)
- Centralized training, decentralized execution

**Reward function:**
```
r_i = r_leader_following + Σ r_UAV-UAV + Σ r_UAV-intruder
```

Where:
- r_leader_following: distance from leader ke basis pe (flocking maintain karne ka reward)
- r_UAV-UAV: collision penalty with neighbor followers
- r_UAV-intruder: collision penalty with intruders

**Critical:** P1, P2, w1, w2 — ye sab FIXED tuning parameters hain. Fleet size, intruder count, situation — kuch bhi ho — same weights. Jab flocking aur avoidance ek saath active hain aur conflict karte hain, fixed coefficients decide karte hain kaun jite.

---

### Results

**Training:** STAAC beats MADDPG, MATD3, HAMA, API-MADDPG, BCDDPG, LSTM-DDQN in all scenarios. Convergence ~1000 episodes (4 hours, NVIDIA RTX 3080).

**Generalization (zero-shot — no retraining):**

| Scenario | STAAC Collision Rate | HAMA (next best) |
|---|---|---|
| n5m15 (5 followers, 15 intruders) | Lowest | 4.76% higher |
| n10m15 | Lowest | 7.69% higher |
| n10m20 (hardest) | **0.34%** | 22.73% higher |

**Ablation (n10m20):**
- TAAC (GTA only, no LSA): worst — entity grouping matters most
- SAAC (LSA only, no GTA): 29.17% higher collision rate than STAAC — temporal matters too
- STAAC: best combination

**HITL (Hardware-in-the-Loop):** Real hardware test kiya — 5 followers, 3 intruders, 100 time steps. Zero collisions. **Average inference: 1.5ms per UAV.**

---

### Paper B ka Ek Line Summary

STAAC kehta hai: **multi-agent UAV fleet mein spatial context (kaun-kaun hai) aur temporal context (kya ho raha tha pehle) dono ek population-invariant architecture mein handle karo.** Lekin jab formation aur avoidance conflict karte hain, trade-off fixed rehta hai.

---

## Dono Papers Side-by-Side — Accurate Comparison

| Cheez | HPER-D3QN (Paper A) | STAAC (Paper B) |
|---|---|---|
| Journal | Defence Technology 2026 | IEEE TITS 2025 |
| Agent type | Single UAV | Multi-agent fleet |
| Environment size | 30km × 30km | 1200m × 800m |
| Novel mechanism | DTPA + HPER | LSA + GTA (STAN) |
| RL backbone | D3QN (discrete action) | MADDPG (continuous action) |
| Framework | MDP | Dec-POMDP |
| Key result | 96.28% success @ 25 aircraft | 0.34% collision @ n10m20 |
| Real hardware test | No (Unity3D simulation) | Yes (HITL, 1.5ms) |
| Reward weights | Fixed (Cgoal=2, Cc=-1, etc.) | Fixed (P1, P2, w1, w2) |
| Dynamic objective balance | ❌ No mechanism | ❌ No mechanism |

---

## The Common Gap — Dono Papers Mein

Paper A ne threat scoring dynamically kiya (DTPA). Paper B ne entity attention dynamically kiya (LSA+GTA). Dono ne apne dimension pe kaafi sophisticated kaam kiya.

Lekin dono papers mein — jab navigation objective aur collision avoidance objective ek saath active hain — **kaun sa zyada important hai, yeh ek fixed number decide karta hai jo training se pehle set kiya gaya tha.**

DTPA itna forward-thinking tha ke collision threats ko dynamically score kiya. Lekin yeh sirf collision avoidance ke andar kaam karta hai. "Is moment mein mujhe target ki zyada zaroorat hai ya collision se bachne ki?" — yeh DTPA nahi decide karta.

STAAC itna sophisticated tha ke 4 frame history temporal attention se process ki. Lekin jab formation maintain karna aur intruder avoid karna ek saath hota hai — weights P1, P2 decide karte hain. Woh context-blind hain.

**Yahi gap hai jo Priority Arbitration Head fill karta hai.**

