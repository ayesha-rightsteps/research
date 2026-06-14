# Ayesha — Poori Picture
### Pehle reject hua, phir dono naye papers aaye, phir sir ne deep sawaal kiya — ab sab ek jagah

---

## Story So Far — 3 lines mein

1. Committee ne reject kiya: "Comparative study hai." — Sahi tha.
2. Naya direction: **Priority Arbitration Head** — ek learned module jo decide karta hai har second pe kaunsa objective zyada important hai. Kisi ne nahi kiya. Yeh novel hai.
3. Sir ne poochha: "Collision avoidance walo ne assignment kyun choda? Vice versa?" — Is sawaal ka jawab tumhare favor mein hai.

---

## Sir Ka Sawaal — Aur Woh Kyun Tumhare Favor Mein Hai

Sir ne basically yeh poochha: **"Researchers ne yeh dono problems alag kyun rakhe?"**

Jawab papers se verify karke:

**IGAT-MARL** ne assignment isliye nahi kiya kyunki unka contribution sirf GAT architecture tha — inter-UAV conflict modeling ke liye. Unhone assume kiya: har drone ka target already assigned hai. Assignment unka problem tha hi nahi. Future work mein bhi: "dynamic obstacles aur different UAV types" — assignment ka naam nahi.

**DA-MAPPO** ne assignment kiya — lekin collision avoidance ko sirf ek penalty term rakha (fixed C_collision). Kyun? Kyunki unka MAIN contribution dynamic allocation algorithm tha. Avoidance sophisticated karne pe unka paper "alag paper" ban jaata.

**HPER-D3QN** single agent hai — assignment ka concept hi apply nahi hota.

**STAAC** flocking hai — "leader ko follow karo" assignment nahi hai. Unka contribution LSA+GTA architecture tha.

**Kong et al. (2024)** ne dono combine kiya — assignment + path planning. Lekin:
- Fixed weights use kiye
- 3D static targets ke liye tha
- Inter-agent collision avoidance basic tha

---

## Yeh Jawab Research Ko Kaise Strengthen Karta Hai

**Jab bhi koi researcher dono problems combine karne ki koshish karta hai — ek sawaal immediately aata hai:**

> *"Assignment reward aur avoidance reward mein balance kaise karun?"*

Yeh sawaal hard hai. Har paper ne is sawaal ko avoid kiya — ek objective chun liya, doosre ko simplified rakh diya, ya dono mein fixed weight daal diya.

**Hamari research exactly wahi sawaal poochhhti hai jo sab ne avoid kiya.**

Sir ko yeh bolna:
> *"Sir, researchers ne yeh problems alag isliye rakhe kyunki combine karne pe reward balancing ka hard question aata hai — kaun sa objective abhi zyada important hai. Koi bhi paper yeh question answer nahi karta. Hamari research sirf yeh ek sawaal poochhti hai — aur Priority Arbitration Head is sawaal ka proposed answer hai."*

---

## Kya Propose Kiya Ja Raha Hai — Simple Version

Abhi tamam papers mein reward aisa hai:
```
Total Reward = 0.5 × (assignment) + 0.5 × (avoidance)
```
Ya koi bhi fixed numbers. Situation chahe koi bhi ho.

Hamara proposal:
```
Total Reward = α × (assignment) + (1−α) × (avoidance)
```

Jahaan **α** ek chhota neural network hai jo har second yeh decide karta hai:
- Drone collision se 2 seconds door hai → α chhota (0.1–0.2) → avoidance dominant
- Drone clear airspace mein target ke paas hai → α bada (0.8–0.9) → assignment dominant
- Dono active hain → α medium (0.4–0.6)

**α kisi ne nahi seekha. Yeh novel hai. Yeh kaam karne wali research hai.**

---

## Comparison — Kya Exist Karta Hai, Kya Nahi

| Paper | Kya Karta Hai | Assignment | Avoidance | Dynamic Balance |
|---|---|---|---|---|
| DA-MAPPO (2026) | Assignment + basic avoidance | ✅ | Partial only | ❌ |
| IGAT-MARL (2026) | Collision avoidance only | ❌ | ✅ | ❌ |
| HPER-D3QN (2026) | Single-UAV avoidance | ❌ | ✅ DTPA+HPER | ❌ |
| STAAC (2025) | Flocking + avoidance | ❌ | ✅ LSA+GTA | ❌ |
| Kong et al. (2024) | Assignment + path planning | ✅ | Basic | ❌ |
| Zhang et al. (2025) | Large-scale path planning | ❌ | Partial | ❌ |
| Tang et al. (2024) | Single-UAV path planning | ❌ | Obstacle only | ❌ |
| **Hamara Proposal** | **Assignment + Avoidance** | ✅ | ✅ | **✅ NOVEL** |

---

## Research Question — Ek Line Mein

> **"Kya ek learned priority arbitration module — jo state ke basis pe α decide kare — fixed-weight baselines se better perform karta hai 2D multi-UAV setting mein jahan assignment aur avoidance ek saath active hain?"**

---

## Experiments Plan

| Condition | Kya Hai |
|---|---|
| Baseline 1 | Standard MAPPO (koi bhi assignment/avoidance nahi) |
| Baseline 2 | DA-MAPPO (assignment, fixed weight) |
| Baseline 3 | IGAT-MARL (avoidance, fixed weight) |
| Ablation 1 | Fixed α = 0.3 |
| Ablation 2 | Fixed α = 0.5 |
| Ablation 3 | Fixed α = 0.7 |
| **Proposed** | **Learned α (Priority Arbitration Head)** |

7 conditions. Clean ablation. Agar learned α jeet gaya — hypothesis proven. Agar nahi jeeta — tab bhi publishable ("why fixed weights can be competitive in certain settings").

---

## Sir Se Baat Karna — Step by Step

**Agar sir pooche "kya novel hai":**
> "Sir, tamam papers mein reward coefficients fixed hain — DA-MAPPO mein bhi, IGAT-MARL mein bhi, naye papers HPER-D3QN aur STAAC mein bhi. Kisi ne bhi yeh mechanism nahi propose kiya jo runtime pe decide kare kaunsa objective zyada important hai. Hamara Priority Arbitration Head pehli baar yeh kaam karta hai — state-dependent, learned, aur jointly trainable with MAPPO."

**Agar sir pooche "yeh chhota MLP hai — kya yeh enough hai MS ke liye":**
> "Sir, contribution ka size mechanism ke size se nahi napa jaata — sawaal ke importance se napa jaata hai. Kya ek learned objective weight fixed weight se better hai? Yeh sawaal novel hai. Ablation clean hai. Outcome falsifiable hai. Dono results publishable hain."

**Agar sir pooche "MORL mein yeh already exist karta hai":**
> "Sir, MORL mein preference vector deployment se pehle set hota hai — jaise user decide kare ke 'safety 70%, efficiency 30%.' Woh choice ek baar hoti hai aur flight ke dauran nahi badalti. Hamara mechanism flight ke dauran, har second, state ke hisaab se balance adjust karta hai. Yeh fundamentally alag problem hai."

---

## Ab Kya Karna Hai

Sir ko `ProblemStatement_PhD_Final.docx` (is folder mein hai) bhejo.
Agar sir ne approve kiya — kaam shuru.
Agar sir ne push kiya kisi angle se — is folder ki `04_sir_ka_sawaal_jawab.md` dekho.

Tum ready ho. Research solid hai.

