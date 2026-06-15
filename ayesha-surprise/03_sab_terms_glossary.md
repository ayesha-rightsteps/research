# Complete Glossary — Har Term, Zero Se Explain
### Koi bhi term confuse kare — yahan aao. Har acronym poora likha hai, har concept zero-knowledge se explain hai.

---

## SECTION A: Reinforcement Learning Basics (Pehle Yeh Samjho)

### Reinforcement Learning (RL) ⭐
**Kya hai:** Ek tarika hai AI ko sikhane ka — jaise hum kisi bachche ko cycle chalana sikhate hain. Bachcha try karta hai, agar acha balance rakha to "good job!" (reward), agar gir gaya to "oops" (penalty/no reward). Bachcha dheere-dheere seekhta hai kaunse actions acha result dete hain.

**Key words:**
- **Agent** = woh "cheez" jo decision le rahi hai (yahan: drone)
- **Environment** = jis duniya mein agent hai (yahan: airspace with other drones, obstacles, targets)
- **State** = abhi ki situation (drone ki position, speed, nearby drones kaha hain, etc.)
- **Action** = agent kya kar sakta hai (turn left, speed up, etc.)
- **Reward** = number jo batata hai action acha tha ya bura (+ya − value)
- **Policy** = agent ka "brain"/strategy — state dekh kar action decide karne ka rule

**Real-life analogy:** GPS navigation jaisa — lekin GPS fixed rules follow karta hai, RL agent EXPERIENCE se seekhta hai ke kaunsa route acha hai.

---

### MARL — Multi-Agent Reinforcement Learning ⭐
**Kya hai:** RL jab MULTIPLE agents (jaise multiple drones) EK SAATH seekh rahe hote hain, aur unke actions ek doosre ko affect karte hain.

**In this paper/research:** Hamare 5-8 drones sab MARL se seekhte hain — har drone ka action doosre drones ke "environment" ka part ban jaata hai.

**Real-life analogy:** Ek hi football team ke 11 players sab apna game seekh rahe hain, lekin har player ka decision baaki players ke liye situation badal deta hai.

---

### PPO — Proximal Policy Optimization
**Kya hai:** Ek POPULAR RL training algorithm. Yeh policy ko "thode-thode steps mein" improve karta hai — bohot bada, risky change ek baar mein nahi karta, isliye training STABLE rehti hai.

**Easy way to remember:** "Proximal" = paas-paas, chhote steps.

---

### MAPPO — Multi-Agent PPO ⭐
**Full form:** Multi-Agent Proximal Policy Optimization
**Kya hai:** PPO ka multi-agent version. **Centralized Training, Decentralized Execution (CTDE)** use karta hai:
- **Training ke time:** Ek "centralized critic" SAARE drones ki info dekh kar seekhta hai ke kaunsa action overall acha tha
- **Execution (real flight) ke time:** Har drone APNI hi local information se decision leta hai — koi central commander nahi chahiye

**In this paper/research:** Hamara backbone algorithm hai. Priority Arbitration Head iske saath jointly train hota hai.

**Real-life analogy:** Training camp mein coach (centralized critic) sabko dekh ke feedback deta hai. Match ke din (execution), har player apne decisions khud leta hai bina coach se baat kiye.

---

### Dec-POMDP — Decentralized Partially Observable Markov Decision Process
**Kya hai:** Ek MATHEMATICAL FRAMEWORK jo describe karta hai multi-agent problems jaha:
- **Decentralized:** Har agent apna decision khud leta hai
- **Partially Observable:** Koi agent POORI duniya nahi dekh sakta — sirf apne nearby area ka pata hai
- **Markov:** Future sirf "abhi ki state" pe depend karta hai, purani history pe nahi (simplifying assumption)

**Real-life analogy:** Ek bade mall mein har security guard sirf apna floor dekh sakta hai (partially observable), aur apne decisions khud leta hai (decentralized).

---

### Policy Gradient
**Kya hai:** Training ka tarika jaha policy (agent ka "brain") ke parameters ko THODA-THODA adjust kiya jaata hai is direction mein jo reward BADHAYE. "Gradient" matlab — "kis direction mein change karna hai" ka mathematical signal.

---

### Actor-Critic
**Kya hai:** Ek architecture jaha do parts hote hain:
- **Actor** = decision leta hai (kaunsa action lena hai)
- **Critic** = batata hai ke woh decision kitna acha tha (value estimate deta hai)

MAPPO mein "Centralized Critic" sab agents ka combined information dekh kar critic ka kaam karta hai.

---

### MLP — Multi-Layer Perceptron
**Kya hai:** Ek SIMPLE neural network — kuch layers of "neurons" jo input lekar output deti hain. Sabse basic type ka neural network.

**In this paper/research:** Priority Arbitration Head ek chhota MLP hai — 2-3 layers, 32-64 neurons per layer. Bohot lightweight hai.

---

## SECTION B: Baseline Paper Concepts

### DA-MAPPO ⭐
**Full form:** Dynamic-Assignment MAPPO
**Paper:** Sheng et al., 2026, IEEE Internet of Things Journal
**Kya karta hai:** MAPPO + ek **minimum-cost allocation module** — yeh module real-time mein decide karta hai "kaunsa drone kaunsa target le" taake total "cost" (jaise total distance) minimum ho.

**Easy way to remember:** "DA" = Dynamic Assignment — targets REAL-TIME mein assign hote hain, fixed nahi.

---

### IGAT-MARL
**Full form:** Improved Graph Attention MARL (Graph Attention Network based MARL)
**Paper:** Rezaee et al., 2026, Applied Soft Computing
**Kya karta hai:** Collision avoidance ke liye **Graph Attention Network** use karta hai.

---

### GAT / GNN — Graph Attention Network / Graph Neural Network
**Kya hai (from scratch):** Pehle samjho **Graph** kya hai — yeh "nodes" (points, jaise drones) aur "edges" (connections, jaise "kaunse drones ek doosre ke paas hain") ka structure hai.

**GNN** ek neural network hai jo is graph structure ko samajh kar har node ke liye decision banata hai — har drone apne "connected" (nearby) drones ki info combine karta hai.

**GAT** GNN ka advanced version hai — yeh decide karta hai ke kaunsa connected neighbor ZYADA important hai (attention weight deta hai). Jaise: ek drone jo bohot paas hai aur collision-course pe hai, usko zyada "attention" milegi us drone se jo door hai.

**Real-life analogy:** Class mein group discussion — GNN matlab sab apne paas baithe logo ki baat sunte hain. GAT matlab — jo zyada relevant baat kar raha hai (jaise group leader), usko zyada dhyaan dete hain.

---

### HPER-D3QN
**Full form:** Hierarchical Prioritized Experience Replay + Double Dueling Deep Q-Network
**Paper:** Shen et al., 2026, Defence Technology
**Kya karta hai:** Single-UAV collision avoidance, complex airspace (manned + unmanned aircraft) mein.

---

### DQN / D3QN
**DQN (Deep Q-Network):** Ek RL algorithm jo "Q-value" seekhta hai — Q-value batata hai "is state mein yeh action lena kitna acha hai" (ek number).

**D3QN (Double Dueling DQN):**
- **Double:** Do separate networks use karta hai overestimation error kam karne ke liye (DQN ki ek common problem)
- **Dueling:** Q-value ko do parts mein todta hai — "yeh state overall kitni achi hai" + "yeh specific action us state mein kitna extra acha hai"

**Easy way to remember:** D3QN = DQN ka "upgraded, more stable" version.

---

### DTPA — Dynamic Threat Prioritization Assessment ⭐
**Paper:** HPER-D3QN (Shen et al., 2026)
**Kya hai:** Ek FORMULA jo batata hai "yeh nearby aircraft kitna BADA threat hai":

```
S = 0.4 × normalize(TCPA) + 0.4 × normalize(DCPA) + 0.2 × κ
```

**In this paper/research:** Yeh formula PROVE karta hai ke "time-to-collision" aur "distance" jaise signals MEANINGFUL hote hain threat assess karne ke liye. Hamara Priority Arbitration Head bhi aise hi signals use karta hai (τ_collision).

---

### TCPA — Time to Closest Point of Approach
**Kya hai (from scratch):** Agar do aircraft apni current speed/direction pe chalte rahein, **kitne SECONDS baad woh sabse paas (closest) honge** — yeh number TCPA hai.

**Real-life analogy:** Do gaadiyan road pe aa rahi hain — TCPA batata hai "kitne second mein yeh dono sabse kareeb honge agar koi na mude."

---

### DCPA — Distance at Closest Point of Approach
**Kya hai (from scratch):** Jab woh do aircraft apne "closest point" pe honge (TCPA wala moment), **unke beech KITNI DISTANCE hogi** — yeh DCPA hai.

**Real-life analogy:** Wahi do gaadiyan — DCPA batata hai "us closest moment pe kitni gap hogi unke beech" (collision hoga ya bas paas se nikal jayengi).

---

### κ (kappa) — Aircraft Type Factor
**Kya hai:** HPER-D3QN ke DTPA formula mein ek factor jo batata hai aircraft "kitna important/sensitive" hai:
- Manned aircraft (insaan baitha hai) → κ = 0.75 (zyada door rehna zaroori)
- Unmanned aircraft (drone) → κ = 0.25 (kam strict)

---

### HPER — Hierarchical Prioritized Experience Replay
**Kya hai (from scratch):** Pehle "Experience Replay" samjho — RL training mein agent apne PURANE experiences (state, action, reward) ek "memory" mein store karta hai aur unhe dobara training mein use karta hai (jaise revision karna).

**Prioritized** = sab purane experiences EQUALLY important nahi hote — jo experiences "surprising" the (jaha agent ka prediction galat tha — TD-error high), unko zyada baar revise karo.

**Hierarchical** = HPER-D3QN mein experiences teen categories mein bante hain:
- **E_high:** arrival (target tak pohoncha) ∪ collision ∪ out-of-bounds — sabse important events
- **E_medium:** warning zone mein tha (danger tha but collision nahi hua)
- **E_low:** sab safe tha, normal flying

Har category ke andar bhi, TD-error ke hisaab se prioritize karte hain.

**Real-life analogy:** Exam revision — sabse pehle woh questions revise karo jo exam mein aa sakte hain AUR jinme tum weak ho.

---

### TD-error — Temporal Difference Error
**Kya hai:** "Agent ne predict kiya tha ke is action ka result X hoga, lekin actual result Y nikla — TD-error = |X - Y|." Jab yeh error BADA hota hai, matlab agent ka "samajh" galat tha — is experience se zyada seekhne ko hai.

---

### STAAC
**Full form:** Spatial-Temporal Attention for Adherence and Collision-avoidance (flocking architecture name)
**Paper:** Yan et al., 2025, IEEE TITS
**Kya karta hai:** Bade fixed-wing UAV fleets ke liye flocking (formation mein flying) + collision avoidance.

---

### MADDPG — Multi-Agent Deep Deterministic Policy Gradient
**Kya hai:** Ek MARL algorithm (jaise MAPPO ka "cousin") jo continuous actions (jaise exact angle/speed values, discrete choices nahi) ke liye use hota hai. STAAC ka backbone hai.

---

### LSA — Local Spatial Attention
**Paper:** STAAC
**Kya hai (from scratch):** Har drone apne aas-paas ke entities (doosre drones, obstacles) ko **4 groups** mein dekhta hai:
1. Self (khud)
2. Leader (jisko follow kar raha hai)
3. Neighbor-followers (apne jaise doosre followers)
4. Neighbor-intruders (potential threats)

Har group ke liye ALAG attention calculate hota hai — yeh "spatial" hai kyunki yeh PHYSICAL positions/groups pe based hai.

**Population-invariant:** Yeh design kitne bhi drones ho (10 ya 50), kaam karta hai — kyunki groups ka structure fixed hai, sirf count badalta hai.

---

### GTA — Global Temporal Attention
**Paper:** STAAC
**Kya hai (from scratch):** "Temporal" = time se related. GTA, LSTM (ek type ka neural network jo SEQUENCES/history ko yaad rakhta hai) use karke **last 4 timesteps** ki history dekhta hai, aur attention deta hai ke kaunsa PURANA moment abhi important hai decision lene ke liye.

**Real-life analogy:** Driving karte waqt — sirf abhi ka traffic nahi, last few seconds mein kya hua (koi sudden brake?) — yeh bhi yaad rakhna.

---

### HITL — Hardware-in-the-Loop
**Kya hai:** Testing ka tarika jaha REAL HARDWARE (actual drone computer/chip) ko simulation ke saath connect karke test karte hain — pure software simulation se zyada REALISTIC hai, lekin actual flight se safer/cheaper hai.

**In this paper/research:** STAAC ka HITL test = 1.5ms inference time. Yeh PROVE karta hai ke complex attention mechanisms REAL hardware pe FAST chal sakte hain — hamara (simpler) arbitration head bhi feasible hai.

---

## SECTION C: Hamare Proposed Mechanism Ke Terms

### Priority Arbitration Head ⭐
**Kya hai:** Hamara PROPOSED naya mechanism — ek chhota neural network (MLP, 2-3 layers) jo MAPPO actor ke saath jointly train hota hai. Har timestep pe yeh decide karta hai **kitna weight assignment ko, kitna avoidance ko de.**

**"Arbitration" ka matlab:** Jab do parties (yahan: assignment-objective aur avoidance-objective) mein "disagreement" ho, arbitration = ek neutral decision-maker jo decide kare kiska kitna sunna hai.

**Inputs:**
1. τ_collision (time-to-collision — TCPA jaisa concept)
2. d_target (distance to assigned target)
3. n_conflict (number of nearby drones on conflict-course)

**Output:** α (alpha) — ek number between 0 aur 1

---

### α (alpha) ⭐
**Kya hai:** Priority Arbitration Head ka OUTPUT — ek number 0 se 1 ke beech.

```
Total Reward = α × (assignment reward) + (1 − α) × (avoidance reward)
```

- α close to 1 → "assignment zyada important abhi" (target ki taraf jao)
- α close to 0 → "avoidance zyada important abhi" (collision se bacho)

**Sabse important baat:** α **FIXED nahi hai** — yeh HAR TIMESTEP, drone ki current situation dekh kar, NAYA calculate hota hai. Yehi "learned, state-conditioned" hai.

---

### State-Conditioned
**Kya hai:** "Conditioned on state" = current situation pe depend karta hai. α state-conditioned hai matlab α ki value drone ki ABHI ki situation (state) pe depend karti hai — har timestep pe alag ho sakti hai.

---

### Fixed Reward Coefficients (THE GAP)
**Kya hai:** Jab reward formula mein numbers (weights/coefficients) TRAINING SE PEHLE decide kar diye jaate hain aur kabhi NAHI badalte — chahe situation kaisi bhi ho.

**Example (DA-MAPPO/HPER-D3QN/STAAC sab mein):** C_goal = +2 (hamesha), C_collision = -1 (hamesha) — drone collision se 5 minute door ho ya 2 second door, yeh numbers SAME rehte hain.

**Yeh exactly woh GAP hai jo hamari research address karti hai.**

---

### MORL — Multi-Objective Reinforcement Learning ⭐
**Kya hai:** RL ka ek branch jaha agent ko MULTIPLE objectives (jaise "speed" aur "safety") ke beech **preference** diya jaata hai — jaise "70% safety, 30% speed."

**MORL aur Priority Arbitration mein FARK (yeh bohot important hai committee ke liye):**

| | MORL | Priority Arbitration |
|---|---|---|
| Preference kab set hoti hai? | DEPLOYMENT se PEHLE (training start hone se pehle hi decide) | Har TIMESTEP pe, FLIGHT ke dauran |
| Kya CONSTANT rehta hai? | Preference poori flight mein same | α har second badal sakta hai |
| Kis tarah ka decision hai? | "User ki choice" (jaise settings mein ek slider) | "Reactive, real-time decision" (jaise reflex) |

**Real-life analogy:** MORL = aap car kharidte waqt decide karte ho "main fuel-efficiency 70%, speed 30% prioritize karunga" — yeh ek baar ki choice hai. Priority Arbitration = car drive karte waqt, har moment decide karna "abhi brake lagao ya accelerate karo" — based on current traffic.

---

### Ablation Study
**Kya hai (from scratch):** "Ablation" medically matlab "kisi part ko hata kar dekhna ke uska kya effect hai." Research mein: ek system ke EK COMPONENT ko change/remove karke dekhna — "yeh component kitna FARK la raha hai?"

**In this paper/research:** Hum "learned α" vs "fixed α = 0.3, 0.5, 0.7" compare karenge — sirf YEH EK CHEEZ (learned vs fixed) badal kar, baaki sab same rakh kar. Yeh "clean ablation" hai.

---

### Baseline
**Kya hai:** Ek EXISTING method jisse hum apna naya method COMPARE karte hain — "hamara naya approach is OLD approach se better hai ya nahi?"

**In this paper/research:** DA-MAPPO aur IGAT-MARL hamare baselines hain.

---

### Falsifiable Hypothesis
**Kya hai (from scratch):** Ek statement jo TEST karke GALAT (false) prove ho sakti hai — agar wrong hai to experiment se pata chal jayega.

**In this paper/research:** "Learned α, fixed α se BETTER perform karega" — yeh falsifiable hai, kyunki experiment se ya to TRUE nikalega ya FALSE. Dono outcomes useful/publishable hain.

---

## SECTION D: Evaluation Metrics

### Mission Success Rate
**Kya hai:** Kitne % missions mein drone(s) apna target successfully reach kar paye, bina kisi major failure ke.

### Collision Frequency / Collision Rate / Separation Violation
**Kya hai:** Kitni baar drones EK DOOSRE ke "safe distance" se zyada paas aaye (ya takra gaye). Kam = better.

### Task Completion Time
**Kya hai:** Target tak pohochne mein kitna time lga. Kam = better (zyada efficient).

### Conflict Neighborhood Density (n_conflict)
**Kya hai:** Ek drone ke aas-paas, ABHI, kitne doosre drones "conflict course" (collision-risk wali direction) pe hain — yeh count.

---

## 5 SABSE IMPORTANT TERMS (Agar Sirf 5 Yaad Rakhne Hain)

1. **⭐ Priority Arbitration Head** — naya mechanism, har timestep pe weight decide karta hai
2. **⭐ α (alpha)** — woh weight, 0-1 ke beech, state-dependent
3. **⭐ MAPPO** — backbone algorithm jis pe arbitration head add hota hai
4. **⭐ Fixed Reward Coefficients (the gap)** — sab existing papers mein numbers fixed hain
5. **⭐ MORL vs Priority Arbitration** — deployment-time preference vs real-time reactive decision

---

Sab ready hai. Agla file: `00_ayesha_ke_liye.md` — overview kaise sab use karna hai.
