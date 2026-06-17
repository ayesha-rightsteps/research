# Deep Concepts — Har Word Samjhao
### Ayesha ke liye — agar sir koi bhi cheez pooche, yahan jawab hai
### Strictly based on FIXED synopsis — koi bahar ki baat nahi

---

## PART 1: RESEARCH KI CORE STORY — SEEDHI BAAT

Pehle poori story simple language mein samjho. Phir technical terms aayenge.

**Imagine karo:**
Tumhare paas 5 drones hain. 5 targets hain. Mission hai — har drone apne target tak pahunche, bina kisi se takraaye.

Abhi kya hota hai real world mein?
- Drone 1 apne target ki taraf ja raha hai
- Drone 2 bhi apne target ki taraf ja raha hai
- Raste mein dono ka path cross hota hai — collision course pe aa jaate hain

**Kya karna chahiye drone 1 ko?**
- Option A: Target ignore karo, collision avoid karo (safe, lekin mission fail)
- Option B: Collision ignore karo, target pe jao (mission complete, lekin crash)
- Option C: **Situation dekh ke decide karo** — target kitna door hai, collision kitna imminent hai, neighbors mein se kaun handle kar sakta hai — THEN decide

**Option C yahi hai Priority Arbitration Head.**

Existing frameworks (DA-MAPPO, IGAT-MARL) kya karte hain?
- Woh Option A ya B decide karte hain TRAINING SE PEHLE — ek fixed number set karte hain aur phir woh kabhi nahi badlta
- Yeh sirf ek half problem solve karta hai

Teri research kya karti hai?
- Framework ko seedhata hai: **"tum khud seekho ke kab kya important hai"**
- Yahi Priority Arbitration Head ka kaam hai

---

## PART 2: TERMS — HAR WORD DEPTH MEIN

---

## ⭐ MAPPO — Multi-Agent Proximal Policy Optimization

### Ek line mein:
MAPPO ek algorithm hai jo multiple agents (drones) ko sikhata hai saath mein kaam karne ka — trial and error se, real-world model ke bina.

### Thoda aur:
**PPO kya hai?** PPO (Proximal Policy Optimization) ek single agent ke liye RL algorithm hai. Schulman et al. 2017 ka paper hai. Yeh guarantee karta hai ke har update mein policy zyada nahi badlti — ek "clip" lagata hai. Isse training stable rehti hai.

**MAPPO kya hai?** PPO ko multiple agents pe extend karo — har drone apna actor hai, lekin ek shared centralized critic hai jo saare agents ka state dekhta hai training mein.

### Analogy:
PPO ek single student ki tarah hai jo exam mein har question ke baad apna approach thoda adjust karta hai — bohot zyada nahi, ek limited range mein.
MAPPO ek class ki tarah hai jahan sab students apna apna kaam karte hain, lekin teacher (centralized critic) poori class ka performance dekhta hai aur feedback deta hai sab ko simultaneously.

### Is research mein kya karta hai:
MAPPO backbone hai — central algorithm. Priority Arbitration Head MAPPO ke upar ek extra module hai. Har drone ka MAPPO actor action decide karta hai (velocity), PAH α decide karta hai (weighting). Dono ek saath train hote hain.

### Sir agar pooche "MAPPO kyun, SAC ya TD3 kyun nahi?":
> "Sir, Yu et al. 2022 ne specifically cooperative multi-agent tasks pe MAPPO test kiya aur dikhaya ke yeh surprisingly effective hai simple SAC ya TD3 se — even in complex coordination scenarios. DA-MAPPO ne bhi MAPPO backbone use kiya hai — is se mera comparison fair aur clean rehta hai same backbone pe."

---

## ⭐ Priority Arbitration Head (PAH)

### Ek line mein:
PAH ek chhota neural network hai jo har second decide karta hai: abhi target zyada important hai ya collision avoid karna — aur yeh KHUD SEEKHTA HAI, manually set nahi hota.

### Bilkul simple:
Soch ke tumhara ek dimag ka hissa (PAH) yeh keh raha hai:
- "Abhi collision 0.5 second mein hoga, target 10 meter door hai, 3 drones conflict pe hain → bhai pehle bhaago (α=0.1)"
- "Abhi collision ka koi risk nahi, target sirf 2 meter door hai → seedha target pe jao (α=0.9)"

Yeh number α hi sab kuch decide karta hai:
```
Total Reward = α × (target reach karne ka reward) + (1−α) × (collision avoid karne ka reward)
```

### Architecture ka matlab:
- **2-layer:** 2 hidden layers hain neural network mein — matlab 2 intermediate "thinking steps"
- **64 neurons:** Har layer mein 64 processing units — chhota enough to be fast, bada enough to be useful
- **ReLU activation:** Standard non-linearity jo network ko complex patterns seekhne deta hai
- **Sigmoid output:** Final layer pe sigmoid lagata hai taake output 0 aur 1 ke beech rahe — α range [0,1]

### 3 Inputs ka matlab:

**τ_collision (tau_collision) — Time-to-collision:**
- Kitne seconds mein nearest conflict neighbor se collision hoga
- Agar τ_collision = 0.3 seconds → bohot urgent → PAH avoidance ko zyada weight dega (α down)
- Agar τ_collision = 10 seconds → koi urgency nahi → PAH assignment ko zyada weight de sakta hai (α up)

**d_target — Distance to assigned target:**
- Assigned target kitna door hai meters mein
- Agar d_target = 1 meter → almost pahunch gaye → assignment zyada important (α up)
- Agar d_target = 50 meters → abhi door hai → pehle safe raho (α can be lower)

**n_conflict — Conflict neighborhood count:**
- Kitne drones abhi tumhare conflict graph mein hain (collision course pe)
- n_conflict = 0 → koi conflict nahi → assignment dominant safely
- n_conflict = 3 → bohot crowded → avoidance critical (α down)

### Yeh novel kyun hai:
DA-MAPPO ka collision weight = -1 (fixed, kabhi nahi badla)
IGAT-MARL ka reward weight = P1, P2 (fixed constants, manually tuned)
Kong et al. = fixed weights
**Kisi bhi existing framework mein α nahi seekhta → PAH pehla hai**

### Sir agar pooche "yeh sirf ek weighted sum hai, novel mechanism kaise hai?":
> "Sir, weighted sum simple hai, lekin novelty WEIGHTS mein hai. Saare existing frameworks mein weights constant hain — training se pehle decide. Main propose kar rahi hoon ke weights khud optimize hon situation ke hisaab se. Yeh small change structurally significant hai: ek ek drone ab contextually decide kar sakta hai ke abhi kya zyada zaroori hai, instead of following a static rule."

---

## ⭐ CTDE — Centralized Training, Decentralized Execution

### Ek line mein:
Training mein sab drones ka poora data use karo (centralized), lekin real deployment mein har drone sirf apni local information se kaam kare (decentralized).

### Analogy:
Training = Army training camp. Sab soldiers ek saath train karte hain, commander (centralized critic) poori team ka performance dekhta hai, feedback deta hai saare ko together.

Deployment = Actual battle. Har soldier apni position, apna radar, apni information — commander ka real-time guidance available nahi. Khud decide karna hai.

### Is research mein:
**Training (Centralized):**
- Centralized Critic saare 5-8 drones ki positions, velocities, targets, conflict state — sab kuch ek saath dekhta hai
- Yeh information use karke "kitna achha kar rahe ho sab?" ka accurate estimate deta hai
- Is estimate se MAPPO actor aur PAH dono ke weights update hote hain

**Execution (Decentralized):**
- Deploy karo toh har drone sirf apna observation vector use karta hai
- Apni 2D position, apna target, apne conflict neighbors, apni obstacle readings
- Centralized critic deployment mein use nahi hota

### Sir agar pooche "real drones pe deploy ho sakta hai?":
> "Sir, CTDE isi liye use kiya gaya hai. Training mein centralized data use karke better policy seekh sakte hain, lekin deployment mein har drone sirf apna on-board sensor data use karta hai — no communication overhead, no central coordinator required. Yeh real UAV deployment ke liye practical hai."

---

## ⭐ Hungarian Algorithm

### Ek line mein:
Hungarian algorithm ek mathematical method hai jo minimum total cost wala assignment find karta hai — n drones ko n targets assign karo taake total distance (ya cost) minimum ho.

### Bilkul simple example:
3 drones: D1, D2, D3
3 targets: T1, T2, T3

Distance matrix:
```
        T1    T2    T3
D1      5     9     1
D2      10    3     2
D3      8     7     4
```

Agar randomly assign karein: D1→T1(5) + D2→T2(3) + D3→T3(4) = 12
Hungarian algorithm: D1→T3(1) + D2→T2(3) + D3→T1(8) = 12
Actually: D1→T3(1) + D2→T2(3) + D3→T1(8) — ya better combinations check karta hai

**Optimal assignment woh hoti hai jisme total cost minimum ho.**

### Is research mein kaise use hota hai:
DA-MAPPO ne pehli baar yeh idea use kiya: har decision step pe Hungarian algorithm chalao, assignment result ko drone ke observation vector mein daal do. Matlab drone "jaanta" hai uska target kaun sa hai aur woh kahan hai.

Meri research mein bhi yahi: observation vector mein element (2) hai — target ki 2D relative position, jo Hungarian assignment se compute hoti hai har step pe.

### Dynamic aspect:
"Dynamic" isliye kyunke assignment har step pe recalculate hoti hai. Agar ek target reach ho jaaye, ya drone bahut door chala jaaye kisi aur target se — assignment badal sakti hai. Real-time adaptive.

### Sir agar pooche "Hungarian algorithm computationally expensive nahi hai?":
> "Sir, Hungarian algorithm O(n³) complexity ka hai — n agents aur n targets ke liye. 5-8 drones ke case mein yeh negligible hai — microseconds mein compute hota hai. DA-MAPPO ne 2026 mein real-time results dikhaye hain — computational feasibility confirmed hai."

---

## ⭐ Conflict Graph / Sparse Conflict Graph

### Ek line mein:
Ek graph jisme sirf woh drone pairs connected hote hain jo predicted collision course pe hain — baaki sabse connection nahi.

### Problem jo yeh solve karta hai:
Pehle MARL mein — har drone har doosre drone ko observe karta tha (all-to-all). 8 drones mein 28 pairs. Zyada information → computationally expensive, noise zyada.

IGAT-MARL ka observation: "Zyada tar drones ka ek doosre se collision ka risk nahi hota at a given timestep. Sirf woh pairs connect karo jinka actual collision risk hai."

### Kaise banta hai conflict graph:
Har timestep pe:
- Har drone pair ke liye: predicted trajectory calculate karo
- Agar yeh trajectories ek defined time window ke andar ek defined distance threshold se paas aayengi → yeh pair "conflict" mein hai
- Inhe graph mein connect karo

Result: Sparse graph — sirf relevant connections.

### Is research mein:
Observation vector ka element (3): sirf apne conflict neighbors ki positions aur velocities include hoti hain. Agar koi conflict neighbor nahi → woh part empty/zero.

### IGAT-MARL ka GAT (Graph Attention Network):
IGAT-MARL mein conflict graph pe Graph Attention Network run hota hai. Attention mechanism decide karta hai ke kaun sa neighbor zyada important hai (zyada collision risk wala → zyada attention).

Main bhi conflict graph use kar rahi hoon lekin PAH ke through — n_conflict count directly PAH ko batata hai kitne conflict neighbors hain.

### Sir agar pooche "conflict graph threshold kaise decide karte ho?":
> "Sir, time horizon threshold — matlab kitne seconds mein predicted collision hoga — IGAT-MARL mein bhi ek hyperparameter hai. Is research mein bhi yeh tuned hoga experiments mein. DA-MAPPO aur IGAT-MARL dono ne specific values use ki hain jinhe main starting point ke roop mein use karungi."

---

## ⭐ Dec-POMDP — Decentralized Partially Observable Markov Decision Process

### Ek line mein:
Multi-agent problems ka formal mathematical framework jahan har agent partial information rakhta hai aur independently decide karta hai.

### Full form tod ke samjho:

**Decentralized:**
Koi central authority nahi jo sab drones ko bata rahi ho kya karna hai. Har drone apna decision khud leta hai.

**Partially Observable:**
Koi bhi drone poori duniya nahi dekh sakta. D1 sirf apna paas waala area dekhta hai, apne conflict neighbors dekhta hai, apna target dekhta hai — D5 ki exact state shayad nahi pata real-time mein.

**Markov:**
"Markov property" — future depend karta hai sirf present state pe, not complete history. Matlab: agar current state pata hai toh optimal decision ke liye history ki zaroorat nahi.

**Decision Process:**
Sequence of decisions — har step pe action lo, reward milti hai, state change hota hai, agli action lo.

### Kyun zaroori hai yeh term:
CTDE specifically Dec-POMDP problems ko solve karta hai. Training mein "complete" information use karo (centralized) taake better critic mil sake, lekin actual problem Dec-POMDP hai (partial observation, decentralized).

### Sir agar pooche:
> "Sir, Dec-POMDP is research ka formal setting hai. Har drone partially observes the environment — apna state, apne conflict neighbors, apna target, obstacles. Complete joint state kisi bhi single drone ko available nahi hoti deployment mein. MAPPO ka CTDE framework specifically Dec-POMDP settings ke liye designed hai."

---

## ⭐ Curriculum Learning

### Ek line mein:
Pehle simple problems seekho, dhire dhire complexity badhao — bilkul jaise school mein Class 1 se start karte hain, Class 10 se nahi.

### Is research mein 4 stages:

**Stage 1 — Class 1 (3 drones, static targets, 2D):**
- Sabse simple: targets move nahi karte, sirf 3 drones
- Goal: DA-MAPPO ko replicate karo, baseline validate karo
- PAH kya seekhta hai: basic assignment vs avoidance tradeoff

**Stage 2 — Class 3 (5 drones, moving targets, kuch obstacles):**
- Thoda complex: targets ab move karte hain, 5 drones
- PAH kya seekhta hai: dynamic reassignment ke saath avoidance balance

**Stage 3 — Class 8 (8 drones, high obstacle density, dynamic targets):**
- Full complexity: zyada drones, zyada obstacles, moving targets
- PAH kya seekhta hai: crowded environment mein priority decisions

**Stage 4 — Board exam (unseen swarm sizes):**
- Generalization test: swarm sizes jo training mein nahi the
- Goal: policy ne sirf memorize nahi ki, genuinely seekha hai

### Kyun zaroori hai:
Directly Stage 3 pe train karo toh policy kuch nahi seekhti — reward sparse hoti hai (koi success nahi milti), policy random rehti hai. Curriculum se dhire dhire policy develop hoti hai.

### Sir agar pooche:
> "Sir, curriculum learning standard practice hai cooperative MARL mein. Direct high-complexity training mein reward signal itni sparse hoti hai ke agents kuch nahi seekhte. DA-MAPPO aur IGAT-MARL dono ne staged curriculum use ki hai — main same approach follow kar rahi hoon, unhi stage definitions ke saath."

---

## ⭐ DA-MAPPO — Dynamic Assignment MAPPO (Sheng et al., 2026)

### Paper kya karta hai:
Real-time target assignment + MAPPO. Hungarian algorithm ko observation vector mein encode karo, har step pe recalculate karo. Result: 90-99% mission success.

### Strongest point:
Ablation study — jab assignment information observation se remove ki → success 90% → 0%. Yeh prove karta hai ke assignment non-negotiable hai.

### Weakness (jo main address karti hoon):
- Collision avoidance = sirf ek fixed constant penalty (-1)
- Yeh penalty kabhi nahi badlti
- Agar 5 drones ek saath collision course pe hon — penalty wahi -1 rehti hai jab ek bhi ho tab bhi
- Assignment aur avoidance ka balance NEVER adapts

### Quote from paper (approximately):
"Collision avoidance is implemented as a fixed penalty term in the reward function" — yeh exactly wo gap hai jo PAH fill karta hai.

### Sir agar numbers pooche:
- Mission success: 90-99% in dynamic multi-target scenarios
- Ablation: 0% without assignment encoding
- Collision avoidance: fixed C_collision = constant penalty
- Environment: 2D (same as our research)
- Reference: [10] in synopsis

---

## ⭐ IGAT-MARL — Incremental Graph Attention MARL (Rezaee et al., 2026)

### Paper kya karta hai:
Collision avoidance using sparse conflict-driven graph + Graph Attention Network. Connect only collision-course pairs, not all pairs. Result: 44% fewer interaction edges, better avoidance.

### Strongest point:
Sparse graph efficiently handles crowded scenarios — zyada communication nahi, sirf relevant pairs.

### Weakness (jo main address karti hoon):
- Fixed targets assumed — assignment problem ka concept hi nahi hai
- Fixed reward weights P1, P2 — kabhi nahi badlte
- Future work: "task allocation as a clear future direction" — unhone khud kaha

### Key numbers:
- 17% higher cumulative reward vs baseline MARL
- 10% fewer separation violations (near-collisions)
- 44% reduction in interaction edges
- Environment: 2D
- Reference: [9] in synopsis

---

## ⭐ Policy Gradient

### Ek line mein:
Neural network ke weights update karne ka method — "agar is action ne achha reward diya, future mein is action ki probability badhao."

### Simple math:
```
θ_new = θ_old + α × ∇(Expected Reward)
```
- θ = neural network weights
- α = learning rate (kitna zyada update karna hai)
- ∇ = gradient (kaunsi direction mein weights change karne se reward badhega)

### PPO ka "Proximal" part kyun:
Normal policy gradient mein ek problem hai — ek update mein weights bahut zyada badal sakte hain, policy unstable ho jaati hai. PPO "clip" lagata hai: maximum allowed change limit karo per update. Isliye PPO stable hai.

### Is research mein PAH ke liye:
PAH ke weights bhi same policy gradient update mein train hote hain. Separate loss function nahi — reward signal r_total = α × r_assign + (1−α) × r_avoid hi backpropagate hoti hai through PAH bhi. Isliye PAH automatically seekhta hai ke kaun sa α achhe reward deta hai.

---

## ⭐ Centralized Critic

### Ek line mein:
Training mein ek shared evaluator jo SAARE drones ka complete state dekhta hai aur estimate karta hai "is state se kitna total future reward milega."

### MAPPO mein role:
Actor: action decide karta hai (based on own observation only)
Critic: "value estimate" deta hai — is state mein expected future reward kitna?

Critic ka estimate use karta hai policy gradient: agar actual reward > critic ka estimate → yeh action good tha, probability badhao. Agar actual reward < estimate → yeh action bad tha, probability ghataao.

### Centralized kyun:
Agar har drone ka sirf apna critic hota → partial information se bad estimates → slow/wrong learning.
Ek shared critic jo sab drones ka state dekhta hai → accurate value estimates → better learning.

### Meri research mein:
Centralized critic mein koi change nahi. PAH sirf MAPPO actor ke saath jointly train hota hai. Critic ko PAH ki knowledge bhi nahi chahiye explicitly — reward signal already PAH ke through computed hai.

---

## ⭐ Observation Vector

### Ek line mein:
Jo information har drone ko "dikhti hai" — ek vector (list of numbers) jo drone ke neural network ko input milta hai.

### Is research mein 4 elements:

**Element 1: 2D position + velocity (self)**
- x position, y position, velocity x component, velocity y component
- 4 numbers
- "Main kahan hoon aur kitni speed se kahan ja rahi hoon"

**Element 2: 2D relative position of assigned target**
- Target ka position minus apna position
- Hungarian algorithm se pata chala hai kaun sa target apna hai
- "Mera target mujhse kitna door hai aur kahan hai"
- Updated har step pe — target move kare ya assignment change ho → yeh update hota hai

**Element 3: Conflict neighbors ki positions aur velocities**
- Sirf wo drones jo conflict graph mein connected hain (collision course pe hain)
- Variable size — 0 conflict neighbors bhi ho sakte hain, 4 bhi
- "Mujhse takraane wale drones kahan hain aur kaise move kar rahe hain"

**Element 4: Obstacle proximity — 4 cardinal directions**
- North, South, East, West mein obstacle distance
- 4 numbers
- "Mujhse north mein kitne meter pe obstacle hai, south mein, etc."

### Poora vector:
Yeh sab numbers ek flat vector mein concatenate hote hain → MAPPO actor aur PAH dono ko input milta hai.

---

## ⭐ Mission Success Rate

### Ek line mein:
Percentage of episodes jisme saare drones apne assigned targets reach kar lein — zero collisions, time limit ke andar.

### Strictly defined kya hai "success":
- SARE drones (not some) → apne assigned targets reach karein
- ZERO inter-drone collisions
- ZERO obstacle collisions
- Time limit ke andar (pre-defined max steps per episode)

### Agar ek bhi fail → whole episode fail.

### Secondary metrics:
- **Inter-drone collision count:** Kitni baar drones ek doosre se takraaye
- **Obstacle collision count:** Kitni baar kisi obstacle se takraaye
- **Target reassignments per episode:** Kitni baar Hungarian algorithm ne assignment change ki
- **Average trajectory length:** Har drone ne average kitna path travel kiya (efficiency measure)

### Testing grid:
- 3 swarm sizes: 3, 5, 8 drones
- 3 obstacle densities: 30, 40, 50 obstacles
- Total: 3 × 3 = 9 test configurations

---

## ⭐ Ablation Study

### Ek line mein:
Ek ek component hataate jao model se, dekhte jao performance kitni girती hai — yeh confirm karta hai ke har component genuinely kaam kar raha hai.

### Is research ka ablation plan:

| Configuration | Assignment Mechanism | Conflict Graph | PAH |
|---|---|---|---|
| Baseline 1 (Standard MAPPO) | ❌ | ❌ | ❌ |
| Baseline 2 (DA-MAPPO 2D) | ✅ Hungarian | ❌ | ❌ (fixed weight) |
| Baseline 3 (IGAT-MARL fixed assign) | ✅ Fixed | ✅ | ❌ (fixed weight) |
| Ablation A (Unified + α=0.3) | ✅ | ✅ | ❌ (fixed 0.3) |
| Ablation B (Unified + α=0.5) | ✅ | ✅ | ❌ (fixed 0.5) |
| Ablation C (Unified + α=0.7) | ✅ | ✅ | ❌ (fixed 0.7) |
| **Proposed (Unified + Learned α)** | ✅ | ✅ | ✅ **Learned** |

### Yeh ablation kyun important hai:
"PAH ne kuch nahi kiya, sirf unified framework hi kaafi tha" — yeh objection pre-empt karta hai.
Agar Ablation A/B/C (fixed α) vs Proposed (learned α) mein clear difference aata hai → PAH ka contribution proven.

### Sir agar pooche "agar PAH worse perform kare?":
> "Sir, agar learned α fixed α se worse perform kare, yeh bhi valid aur publishable result hai. Iska matlab hoga ke 2D simple environment mein fixed weight sufficient hai — adaptive mechanism ko benefit nahi milta. Yeh finding future work ke liye important hogi: maybe 3D ya more dynamic environments mein PAH ka advantage milega. Negative result bhi science hai."

---

## ⭐ Fixed Reward Coefficients vs Learned α — THE CORE GAP

### Yeh ek slide pe explain karo:

**Existing frameworks (DA-MAPPO, IGAT-MARL, Kong et al.):**
```
r_total = C1 × r_assignment + C2 × r_avoidance
```
- C1 = 1.0, C2 = -1.0 (ya kuch bhi — but CONSTANT)
- Yeh numbers training se pehle set hote hain
- Training ke dauran kabhi nahi badlte
- Deployment mein bhi kabhi nahi badlte
- Chahe drone 0.1 second mein collision pe ho, C2 wahi -1 rehta hai
- Chahe drone 0.001 meter door target se ho, C1 wahi 1.0 rehta hai

**Proposed framework:**
```
r_total = α × r_assignment + (1−α) × r_avoidance
```
- α = PAH ka output = f(τ_collision, d_target, n_conflict)
- τ_collision = 0.1 sec → α close to 0 (avoidance urgent)
- d_target = 0.5 meter → α close to 1 (almost there, finish it)
- n_conflict = 5 → α lower (bohot crowded, be careful)
- Yeh dynamically changes har timestep pe

**Yahi gap hai. Yahi novelty hai. Yahi PAH hai.**

---

## PART 3: NUMBERS JO YAAD RAKHNE HAIN

```
90–99%    → DA-MAPPO mission success (best existing)
0%        → DA-MAPPO without assignment (ablation)
44%       → IGAT-MARL edge reduction
17%       → IGAT-MARL reward improvement over baseline
10%       → IGAT-MARL separation violation reduction
3, 5, 8   → Drone counts tested
30,40,50  → Obstacle counts tested
0.3,0.5,0.7 → Fixed α baselines
64        → PAH neurons
2         → PAH layers
4         → Observation vector elements
4         → Training curriculum stages
```

---

## PART 4: CONNECTIONS — SAB KUCH EK SAATH

```
Sir ka paragraph (coupling problem)
         ↓
Gap identify kiya:
  DA-MAPPO (assignment) → fixed collision weight
  IGAT-MARL (avoidance) → fixed assignment → assumed fixed
  Both cited each other as future work
         ↓
Proposed Solution:
  Unified observation (Hungarian + Conflict Graph + PAH input)
         ↓
  MAPPO Actor → 2D velocity action
  PAH → α (learned, dynamic)
         ↓
  r_total = α × r_assign + (1−α) × r_avoid
         ↓
Research Question:
  "Does learned α outperform fixed α?"
         ↓
Ablation proves it:
  Fixed 0.3 vs Fixed 0.5 vs Fixed 0.7 vs Learned α
```

---

## PART 5: 10 BAAR REPEAT KARO YEH LINE

Ayesha — yeh ek line itni baar padho ke sapne mein bhi aa jaaye:

> **"Saare existing frameworks mein reward coefficients fixed hain — koi bhi framework nahi seekhta ke abhi kis objective ko priority deni hai. Priority Arbitration Head pehla mechanism hai jo yeh decision har timestep pe current state dekh ke dynamically learn karta hai."**

---

## AGAR SIR NE KUCH AISA POOCH LIYA JO YAHAN NAHI HAI

Yeh kaho confidently:
> "Sir, yeh specific detail mujhe abhi exactly yaad nahi — lekin core concept jo main samajhti hoon woh yeh hai: [core concept bolо]. Main specific number baad mein verify kar sakti hoon."

Kabhi mat kaho "mujhe nahi pata." Hamesha core concept se jawab do.
