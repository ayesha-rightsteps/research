# Ayesha's Presentation Handbook
### Kal ka presentation — poori tayyari ek file mein
### Based strictly on: CUI_Synopsis_AYESHA_KHALIL-SP25-RCS-009_FIXED.docx

---

## SABSE PEHLE YEH PADHO — 2 MINUTE

**Teri research ek line mein:**
> Multi-UAV missions mein drones ko target assign bhi hote hain aur collision bhi avoid karni hoti hai — yeh dono kaam aaj tak kisi bhi framework mein ek saath ek learned policy mein nahi hue. Teri research mein ek naya mechanism hai — **Priority Arbitration Head (PAH)** — jo dynamically decide karta hai har second "abhi target ki taraf jaana zyada zaroori hai ya collision se bachna."

**Presentation ki soul (yeh yaad rakh):**
- Problem: **Coupling** — assignment aur avoidance ek doosre ko affect karte hain
- Gap: **Fixed weights** — koi bhi framework dynamically decide nahi karta kab kya priority
- Solution: **Priority Arbitration Head** — learned α, not fixed constant
- Evidence: DA-MAPPO aur IGAT-MARL dono ne ek doosre ke kaam ko future work kaha

---

## OPENING — Word for Word Script

> "Good [morning/afternoon], sir. Mera naam Ayesha Khalil hai, registration SP25-RCS-009. Aaj main apna research synopsis present karne aayi hoon jiska title hai:
>
> *'Joint Target Assignment and Conflict-Aware Collision Avoidance in Multi-UAV Coordination Using MAPPO with Priority Arbitration'*
>
> Sir, is research ka core idea yeh hai: multi-UAV missions mein target assignment aur collision avoidance do alag problems nahi hain — yeh structurally coupled hain. Aur aaj tak kisi bhi framework ne inhe ek saath ek learned policy mein solve nahi kiya. Main propose kar rahi hoon ek naya mechanism — Priority Arbitration Head — jo is gap ko fill karta hai."

---

## SLIDE-BY-SLIDE SCRIPT

---

### SLIDE 1 — Title
Sirf introduction — script upar diya hai.

---

### SLIDE 2 — Introduction: UAV Applications

> "Sir, briefly — UAVs pehle sirf military mein the. Ab disaster response, agriculture, infrastructure inspection — sab mein use ho rahe hain. Ek akela drone kaafi nahi — real missions mein teams chahiye. Aur teams ko coordinate karna sirf hardware se nahi hota — intelligent algorithm chahiye."

---

### SLIDE 3 — Introduction: Multi-UAV Coordination

> "Purana approach tha centralized planner — pehle sab kuch plan karo, phir execute karo. Problem yeh hai ke jab targets move karein ya obstacles aayein, yeh plan fail ho jaata hai aur real-time mein recalculate karna computationally impossible hai. Isliye hum learning-based approach use karte hain — drones khud seekhte hain cooperation kaise karein."

---

### SLIDE 4 — DRL & MARL

> "DRL mein agent environment mein play karta hai, rewards milti hain, aur gradually policy improve hoti hai bina explicit world model ke. MARL is ko multiple agents tak extend karta hai. CTDE — Centralized Training, Decentralized Execution — matlab training mein sab agents ka joint state use karo, lekin execution mein har drone apni local observation se kaam kare. MAPPO is ka proven, stable implementation hai."

---

### SLIDE 5 — Motivation (MOST IMPORTANT SLIDE)

> "Sir, yahan se actual research start hoti hai.
>
> DA-MAPPO — 2026 ka paper — 90 to 99 percent mission success achieve karta hai real-time target assignment se. Lekin collision avoidance mein woh sirf ek **fixed constant penalty** use karta hai. Yeh penalty kabhi nahi badlti — chahe drone collision course pe ho ya nahi.
>
> IGAT-MARL — bhi 2026 ka — collision avoidance mein conflict-aware graph use karta hai, 44 percent interaction edges reduce karta hai. Lekin yeh assume karta hai ke targets already assigned hain — assignment ka koi mechanism hi nahi hai isme.
>
> Sabse important baat: DA-MAPPO ke apne ablation study mein jab assignment information remove ki gayi — mission success **90 percent se zero percent** ho gayi. Matlab assignment non-negotiable hai.
>
> Aur sir — dono papers ne ek doosre ke kaam ko apna future work kaha hai. DA-MAPPO ne collision avoidance ko future work kaha, IGAT-MARL ne target assignment ko. Yeh research wahi future work hai.
>
> Lekin sirf dono combine karna kaafi nahi — **dono papers mein weights FIXED hain**. Koi bhi framework nahi seekhta ke abhi assignment zyada important hai ya avoidance. Mera proposed Priority Arbitration Head yahi kaam karta hai — har timestep pe yeh dynamically decide karta hai."

---

### SLIDE 8 — Gap in Existing Work

> "Sir, gap clearly yeh hai: researchers jo target assignment pe kaam karte the, unhone collision avoidance ignore ki. Jo avoidance pe kaam karte the, unhone assignment ignore ki. Result: har framework ek half problem solve karta hai.
>
> Lekin isse bhi important gap yeh hai: **saare existing frameworks mein reward weights FIXED hain** — DA-MAPPO mein C_collision constant hai, IGAT-MARL mein P1 aur P2 fixed constants hain. Koi framework nahi hai jo **learn kare** ke har situation mein assignment aur avoidance ka balance kya hona chahiye.
>
> Yahi structural gap hai jo mera research address karta hai."

---

### SLIDE 9 — Problem Statement

> "Sir, problem statement yeh hai:
>
> Multi-UAV missions mein task allocation aur collision avoidance interdependent hain — ek drone ka target ki taraf jaana seedha affect karta hai ke woh doosre drones ke kitna paas aata hai. Aur agar usne collision avoid karne ke liye course change kiya, toh woh original target reach kar pata hai ya nahi — yeh bhi change ho jaata hai.
>
> Iska matlab yeh hai ke ek avoidance maneuver se ek critical target uncovered ho sakta hai, doosre drones mein reassignment conflicts aa sakte hain, aur simultaneously naye collision risks create ho sakte hain.
>
> Aur sir — in dono problems pe alag alag bohot kaam hua hai, lekin inhe ek saath ek single learned policy mein aaj tak address nahi kiya gaya."

---

### SLIDE 10 — Research Objectives

> "Sir, mere research ke 4 objectives hain:
>
> Pehla — Priority Arbitration Head design aur implement karna. Yeh ek lightweight neural module hai jo MAPPO actor ke saath jointly train hota hai. Input mein time-to-collision, target se distance, aur conflict neighborhood count hain. Output ek dynamic weight α hai jo decide karta hai abhi assignment zyada important hai ya avoidance.
>
> Doosra — framework ko 3, 5, aur 8 drones ke saath test karna — dekhna ke performance deteriorate hoti hai ya stable rehti hai jab simultaneous conflicts badhte hain.
>
> Teesra — controlled ablation experiments. Specifically, learned α ko fixed baselines α = 0.3, 0.5, 0.7 ke against compare karna. Yeh directly test karega ke learned weighting fixed weighting se better hai ya nahi.
>
> Chautha — failure boundary find karna — kis combination of swarm size, obstacle density, aur target speed pe framework fail karta hai aur kyun."

---

### SLIDE 11 — Proposed Methodology

> "Sir, methodology mein main framework design explain karti hoon.
>
> Har drone 4 cheezein observe karta hai: apni khud ki 2D position aur velocity; apne assigned target ki relative position — jo har step pe Hungarian minimum-cost algorithm se compute hoti hai; apne conflict neighbors ki positions — jo dynamic conflict graph se decide hote hain, woh drones jo predicted collision course pe hain; aur 4 directions mein obstacle proximity.
>
> In sab ko ek joint observation vector mein combine kiya jaata hai.
>
> Is observation vector se do cheezein parallel mein hoti hain: MAPPO actor 2D velocity action decide karta hai; aur Priority Arbitration Head — 2-layer, 64 neuron network — ek single number α output karta hai between 0 aur 1.
>
> Total reward formula hai: r_total = α × r_assignment + (1−α) × r_avoidance.
>
> Jab α 1 ke paas hota hai — assignment dominant. Jab 0 ke paas — avoidance dominant. Aur α **khud seekhta hai** — koi manually set nahi karta.
>
> Training mein centralized critic saare drones ka joint state dekhta hai. MAPPO actor aur Priority Arbitration Head dono ek hi policy gradient update mein train hote hain — koi alag training loop nahi."

---

### SLIDE 12 — Training Strategy

> "Sir, training ke liye 4-stage curriculum use kar rahi hoon.
>
> Stage 1: 3 drones, 2D, static targets — DA-MAPPO replicate karo validation ke liye.
> Stage 2: 5 drones, moving targets, kuch obstacles.
> Stage 3: 8 drones, high obstacle density, dynamic targets.
> Stage 4: Generalization test — swarm sizes jo training mein nahi the unpe test.
>
> Yeh curriculum design DA-MAPPO aur IGAT-MARL dono papers ne validate kiya hai apni training mein."

---

## SUPERVISOR KE ANTICIPATED QUESTIONS — Q&A

---

### Q1: "Priority Arbitration Head ki novelty kya hai specifically?"

> "Sir, novelty yeh hai ke saare existing frameworks — DA-MAPPO, IGAT-MARL, Kong et al. — mein reward coefficients FIXED hain. Matlab training se pehle manually decide kar lete hain ke assignment ko kitna weight dena hai aur avoidance ko kitna — aur yeh training ke dauran kabhi nahi badlta.
>
> Priority Arbitration Head pehli baar is decision ko **learned** banata hai. Har timestep pe current situation — collision kitni door hai, target kitna door hai, kitne drones conflict pe hain — dekhke dynamically weight set karta hai. Yeh kisi bhi existing multi-UAV framework mein nahi hai."

---

### Q2: "Yeh comparative study nahi hai? Sirf DA-MAPPO aur IGAT-MARL combine kar rahe ho?"

> "Sir, agar sirf dono combine karte aur test karte — woh comparative study hota. Lekin hum ek **naya mechanism add kar rahe hain** jo dono papers mein exist hi nahi karta. Priority Arbitration Head alag se design kiya gaya hai, alag inputs hain, alag output hai, aur research question specifically yeh hai: 'kya learned weighting fixed weighting se better hai?' — yeh ek falsifiable hypothesis hai. Ablation mein hum fixed α = 0.3, 0.5, 0.7 ke against compare karenge — yeh cleanly prove karega ke PAH ka contribution real hai ya nahi."

---

### Q3: "2D mein kyon? 3D zyada realistic nahi hota?"

> "Sir, bilkul — 3D zyada realistic hai. Lekin is research ka primary contribution environment complexity nahi hai — **learned priority arbitration** hai. 2D mein yeh contribution isolate karke test karna zyada clean hai. DA-MAPPO aur IGAT-MARL bhi 2D mein evaluate hue hain — iska matlab comparison fair hoga. 3D extension future work hai."

---

### Q4: "DA-MAPPO ablation numbers kahan se hain? Paper mein clearly likha hai?"

> "Sir, haan — DA-MAPPO ke paper mein explicitly likha hai. Unka ablation study dikhata hai ke jab assignment information observation vector se remove ki jaaye, mission success rate 90-99% se seedha 0% ho jaati hai. Yeh unka khud ka number hai, mera claim nahi — paper ka reference [10] hai."

---

### Q5: "Hungarian algorithm kya hai?"

> "Sir, Hungarian algorithm ek combinatorial optimization algorithm hai jo minimum cost assignment find karta hai. Is case mein — n drones hain, n targets hain — algorithm woh assignment find karta hai jisme total cost (jaise total distance) minimum ho. DA-MAPPO ne dikhaya ke isko observation vector mein encode karne se mission success dramatically improve hoti hai."

---

### Q6: "Conflict graph kya hai? IGAT-MARL se kaise aaya?"

> "Sir, IGAT-MARL ne propose kiya ke har drone ko saare agents ke saath communicate karne ki zaroorat nahi. Sirf woh drone pairs connect karo jinke beech predicted collision course hai — is 'sparse conflict graph' se unnecessary interaction edges 44% kam ho jaate hain aur avoidance performance better hoti hai. Main is graph ko apne observation vector mein use kar rahi hoon conflict neighborhood ke liye."

---

### Q7: "α kaise learn hota hai? Alag loss function hai?"

> "Sir, koi alag loss function nahi hai. PAH MAPPO actor ke saath same policy gradient update mein train hota hai. Reward signal — r_total = α × r_assign + (1−α) × r_avoid — backpropagate hota hai aur PAH ke weights update hote hain. Simple backpropagation. Alag training loop nahi, centralized critic mein koi change nahi."

---

### Q8: "Baselines kya hain? Kis cheez ke against compare karoge?"

> "Sir, 4 baselines hain:
> 1. Standard MAPPO — koi assignment mechanism nahi, koi conflict graph nahi
> 2. DA-MAPPO 2D mein port kiya — assignment hai, lekin fixed collision penalty
> 3. IGAT-MARL with fixed assignment — conflict graph hai, lekin fixed target
> 4. Unified framework with fixed α (0.3, 0.5, 0.7) — PAH ke bina
>
> Proposed framework — learned α wala — inhi ke against compare hoga. Especially baseline 4 vs proposed directly test karega ke PAH ka contribution kya hai."

---

### Q9: "Dec-POMDP kya hai? Framework mein kahan apply hota hai?"

> "Sir, Dec-POMDP — Decentralized Partially Observable Markov Decision Process — multi-agent problems ka mathematical framework hai. 'Partial observability' isliye kyunke har drone sirf apna local area dekhta hai — complete world state nahi. Is framework ka formal setting yahi hai. CTDE is problem ko solve karta hai: training mein complete joint state use karo, execution mein partial observation se kaam chalo."

---

### Q10: "Evaluation metrics kya hain? Mission success kaise define kiya?"

> "Sir, primary metric hai mission success rate — woh proportion of episodes jisme saare drones apne assigned targets reach kar lein bina kisi collision ke, ek defined time limit ke andar. Secondary metrics hain: inter-drone collision count, obstacle collision count, target reassignments per episode, aur average trajectory length per drone. Teeno swarm sizes (3, 5, 8) aur teeno obstacle densities (30, 40, 50 obstacles) pe test hoga."

---

### Q11: "Curriculum learning kyun zaroori hai?"

> "Sir, directly 8 drones + high obstacles pe train karna practically fail ho jaata hai — reward signal sparse hoti hai, agents kuch nahi seekhte. Curriculum learning mein dhire dhire complexity badhate hain — 3 drones se start, phir 5, phir 8 — taake policy gradually develop ho. DA-MAPPO aur IGAT-MARL dono ne yahi approach use ki hai successfully."

---

### Q12: "Research question falsifiable hai? Agar PAH worse perform kare?"

> "Sir, bilkul falsifiable hai. Agar learned α fixed α se worse perform kare — woh bhi ek valid result hai. Matlab yeh ki dynamic weighting is specific setting mein help nahi karta, shayad 2D simple environments mein fixed weight sufficient hai. Dono outcomes publishable hain — ek affirms the hypothesis, doosra opens a new question for 3D or more complex settings. Research ka kaam sirf success confirm karna nahi, reliable testing karna hai."

---

### Q13: "MAPPO kyun choose kiya? SAC, TD3 kyun nahi?"

> "Sir, MAPPO choose kiya kyunki:
> Pehli baat — Yu et al. 2022 ka paper 'The Surprising Effectiveness of PPO in Cooperative Multi-Agent Games' ne dikhaya ke MAPPO cooperative MARL settings mein consistently strong performer hai.
> Doosri baat — DA-MAPPO ne already MAPPO backbone use kiya hai — mere baselines mein comparison clean rehti hai agar same backbone use karoon.
> Teesri baat — MAPPO discrete aur continuous action spaces dono handle karta hai, stable convergence deta hai."

---

### Q14: "Sir agar poochhe: tumhara actual contribution kya hai, ek line mein?"

> "Sir, mera contribution yeh hai: pehli baar multi-UAV coordination mein ek learned mechanism propose kiya gaya hai jo dynamically decide karta hai ke each drone ko abhi assignment zyada priority deni chahiye ya collision avoidance — instead of using pre-set fixed constants like all existing frameworks do."

---

## KEY NUMBERS — YAAD RAKH

| Number | Kahan se | Kya matlab |
|---|---|---|
| 90–99% | DA-MAPPO mission success | Strong assignment framework |
| 0% | DA-MAPPO ablation (no assignment) | Assignment non-negotiable hai |
| 44% | IGAT-MARL edge reduction | Sparse graph effective hai |
| 3, 5, 8 | Swarm sizes tested | Scalability range |
| 30, 40, 50 | Obstacle counts tested | Difficulty range |
| 0.3, 0.5, 0.7 | Fixed α baselines | PAH ko compare karenge inse |
| 64 | PAH hidden neurons | Architecture simple hai |
| 2-layer | PAH depth | Lightweight, not complex |
| 4 | Observation elements | Self, target, neighbors, obstacles |
| 4 | Training stages | Curriculum progression |

---

## TERMS — EK LINE MEIN

| Term | Ek line mein |
|---|---|
| **MAPPO** | Multi-Agent PPO — multiple drones ke liye stable RL algorithm |
| **CTDE** | Training mein sab drones ka data, execution mein sirf apna data |
| **PAH** | Priority Arbitration Head — learned α, assignment vs avoidance balance |
| **α (alpha)** | Dynamic weight: 1=assignment dominant, 0=avoidance dominant |
| **Hungarian algorithm** | Minimum-cost assignment — kon sa drone, kon sa target |
| **Conflict graph** | Sirf collision-course drone pairs connect karo, not all |
| **Dec-POMDP** | Multi-agent math framework where each agent has partial view |
| **Curriculum learning** | Simple se hard — 3 drones se 8 drones dhire dhire |
| **Ablation study** | Ek ek component hatao, effect dekho |
| **DA-MAPPO** | Dynamic Assignment MAPPO — Sheng et al. 2026, primary baseline |
| **IGAT-MARL** | Conflict-graph avoidance — Rezaee et al. 2026, secondary baseline |
| **τ_collision** | Time-to-collision — PAH input 1 |
| **d_target** | Distance to assigned target — PAH input 2 |
| **n_conflict** | Conflict neighbor count — PAH input 3 |

---

## CLOSING STATEMENT

> "Sir, yeh research pehli baar yeh question experimentally address karti hai: kya ek learned dynamic weighting mechanism — jo real-time state ke hisaab se assignment aur avoidance objectives balance kare — fixed coefficient approaches se better results deta hai multi-UAV coordination mein?
>
> Priority Arbitration Head is question ka specific, testable, falsifiable answer provide karta hai — aur agar results positive hain, yeh directly us structural gap ko close karta hai jo DA-MAPPO aur IGAT-MARL dono ne khud identify kiya tha lekin solve nahi kiya.
>
> Thank you, sir."

---

## AGAR BHOOL JAO TO

Yeh 3 sentences yaad rakh — inse kisi bhi sawaal ka jawab milega:

1. **Problem:** "Assignment aur avoidance coupled hain — ek ke baghair doosra properly kaam nahi karta."
2. **Gap:** "Saare existing frameworks fixed weights use karte hain — koi nahi seekhta kab kya priority deni hai."
3. **Solution:** "Priority Arbitration Head yeh decision learn karta hai — har timestep pe, current state dekhke."

---

## CONFIDENCE BOOSTER

Ayesha — teri research mein:
- Ek clear gap hai (fixed weights in ALL papers — provable from papers themselves)
- Ek specific mechanism hai (PAH — not just "combine two methods")
- Ek falsifiable question hai ("does learned α beat fixed α?")
- Evidence hai (DA-MAPPO aur IGAT-MARL dono ne ek doosre ko future work kaha)

Sir ke paas is research ko reject karne ka valid reason nahi hai. Confident jao. 💙
