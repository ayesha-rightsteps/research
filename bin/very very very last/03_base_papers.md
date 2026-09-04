# Base Papers — Detailed Explanation
### DA-MAPPO aur IGAT-MARL — poori detail mein

---

# PAPER 1 — DA-MAPPO
### Sheng et al. 2026 — IEEE Internet of Things Journal

---

## Yeh paper kya hai?
DA-MAPPO ka matlab hai Dynamic Assignment MAPPO. Yeh paper multi-drone coordination k leay MAPPO use karta hai aur isme real-time target assignment add ki gayi hai Hungarian algorithm k through.

---

## Problem Jo Inhone Solve Ki
Multiple drones hain, multiple targets hain. Kaunsa drone kaunse target ko jaaye — yeh assignment problem hai. Pehle k methods mein assignment pehle fix hoti thi aur phir drones move karte the. Agar environment change ho — target move kare — toh assignment outdated ho jaati thi.

DA-MAPPO ne yeh solve kiya: har decision step pe assignment recalculate karo.

---

## Inhone Kya Kiya — Step by Step

**Step 1 — Environment**
- 3 drones, 2D environment
- Static obstacles
- Targets start pe fixed hain

**Step 2 — Observation Vector**
Har drone ko yeh pata hota hai:
- Apni position aur velocity (x, y, vx, vy)
- Apne assigned target ki relative position — Hungarian algorithm se compute hoti hai har step pe
- Obstacles ki proximity

**Step 3 — Hungarian Algorithm**
- Har decision step pe — matlab bahut baar — Hungarian algorithm run hota hai
- Yeh decide karta hai kaunsa drone kaunse target ko assign ho — minimum total cost mein
- Yeh assignment directly drone ki observation mein jaati hai

**Step 4 — MAPPO Training**
- Centralized critic: poori swarm ki state dekhta hai, value estimate karta hai
- Decentralized actor: har drone apni observation say action leta hai — 2D velocity command
- CTDE architecture

**Step 5 — Reward**
- Positive: target k qareeb aao
- Negative: collision ho (sirf penalty, koi avoidance mechanism nahi)
- Episode end: target reach karo

---

## Key Results
- Mission success rate: 90% say 99% across different configurations
- Ablation study: jab assignment information remove ki — success 90% say 0% ho gayi
- Yeh prove karta hai k Hungarian assignment is framework ki soul hai

---

## Limitation — Inhone Khud Kaha
> "Collision avoidance between teammate UAVs is not explicitly modeled. Future work includes integrating explicit inter-agent collision avoidance."

**Matlab:** Drones target tak pahunchtay hain, but dono ek hi direction mein ho saktay hain aur ek doosray say takra saktay hain. Koi mechanism nahi jo actively collision avoid kare.

---

## Connection to Our Research
DA-MAPPO ne prove kiya k real-time Hungarian assignment kaam karta hai. Humne yeh mechanism adopt kiya. But collision avoidance add ki aur PAH k through dono ko dynamically balance kiya.

---
---

# PAPER 2 — IGAT-MARL
### Rezaee et al. 2026 — Applied Soft Computing

---

## Yeh paper kya hai?
IGAT-MARL ka matlab hai Improved Graph Attention multi-agent Reinforcement Learning. Yeh paper multi-drone collision avoidance k leay ek smart graph-based approach use karta hai.

---

## Problem Jo Inhone Solve Ki
Jab bahut saare drones ek saath fly karte hain toh collision risk hota hai. Pehle k methods mein saare drones ek doosray say connected hote the — dense graph. Yeh computationally expensive tha aur irrelevant information bhi include karta tha.

IGAT-MARL ne yeh solve kiya: sirf woh drones connect karo jo actually collision course pe hain.

---

## Inhone Kya Kiya — Step by Step

**Step 1 — Conflict Graph**
- Har decision step pe check karo — kaunse drone pairs itne qareeb hain k collision ho sakti hai specified time window mein
- Sirf unhe connect karo — sparse graph
- Yeh dense all-to-all graph say bahut chota aur efficient hai

**Step 2 — Improved Graph Attention Network (IGAT)**
- Stacked double attention: ek baar graph attention lagao, phir dobaara — zyada refined representation milti hai
- Residual connections: information loss nahi hoti deep layers mein
- Har drone apne conflict neighbors ki information process karta hai aur decide karta hai kaise avoid karna hai

**Step 3 — Observation**
Har drone ko pata hota hai:
- Apni position aur velocity
- Conflict neighbors ki position aur velocity (sirf woh jo conflict graph mein hain)
- Koi target assignment nahi — drones ka koi goal structure nahi

**Step 4 — Training**
- Curriculum learning: pehle 3 drones, phir 5, phir 10
- Centralized training, decentralized execution

**Step 5 — Reward**
- Positive: dusray drones say door raho
- Negative: collision ho
- Koi target reward nahi kyunki koi target hi nahi

---

## Key Results
- 44% fewer interaction edges compared to dense graph methods
- 17% higher total reward
- 10% fewer dangerous separation events
- Trained with up to 10 drones

---

## Limitation — Inhone Khud Kaha
> "Target allocation is not incorporated in this framework. Future work includes integrating task allocation mechanisms."

**Matlab:** Drones bahut achay collision avoid karte hain, but unka koi goal nahi. Woh sirf fly karte aur bachte rehte hain — kisi target tak nahi pahunchte. Mission success rate measure karna meaningless hai kyunki koi mission hi nahi hai.

---

## Connection to Our Research
IGAT-MARL ne prove kiya k sparse conflict graph effective hai. Humne yeh mechanism adopt kiya. But target assignment add ki aur PAH k through dono ko dynamically balance kiya.

---

## Sabse Important Point — Dono Papers Ko Yaad Karo

| | DA-MAPPO | IGAT-MARL | Our Work |
|---|---|---|---|
| Target Assignment | ✓ | ✗ | ✓ |
| Collision Avoidance | ✗ | ✓ | ✓ |
| Dynamic Weights | ✗ | ✗ | ✓ |
| What they missed | Collision avoidance | Target assignment | Nothing |
| What they said | "Add avoidance next" | "Add assignment next" | We did both |

**Yeh line zaroor yaad karo:**
> "DA-MAPPO explicitly states collision avoidance as future work. IGAT-MARL explicitly states target assignment as future work. Our research is that future work — we are doing exactly what both papers asked for next."
