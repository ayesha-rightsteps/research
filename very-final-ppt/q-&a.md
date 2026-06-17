# Q&A — Supervisor Ke Anticipated Sawaal

---

### Q1: Priority Arbitration Head ki novelty kya hai specifically?

> "Sir, novelty yeh hai ke saare existing frameworks — DA-MAPPO, IGAT-MARL, Kong et al. — mein reward coefficients FIXED hain. Training se pehle manually decide kar lete hain ke assignment ko kitna weight dena hai aur avoidance ko kitna — aur yeh kabhi nahi badlta. Priority Arbitration Head pehli baar is decision ko learned banata hai — har timestep pe current situation dekh ke dynamically weight set karta hai."

---

### Q2: Yeh comparative study nahi hai? Sirf DA-MAPPO aur IGAT-MARL combine kar rahe ho?

> "Sir, agar sirf dono combine karte aur test karte — woh comparative study hota. Lekin hum ek naya mechanism add kar rahe hain jo dono papers mein exist hi nahi karta. Research question specifically yeh hai: 'kya learned weighting fixed weighting se better hai?' — falsifiable hypothesis hai. Ablation mein fixed α = 0.3, 0.5, 0.7 ke against compare karenge — yeh cleanly prove karega PAH ka contribution real hai ya nahi."

---

### Q3: 2D mein kyon? 3D zyada realistic nahi hota?

> "Sir, bilkul 3D zyada realistic hai. Lekin is research ka primary contribution environment complexity nahi — learned priority arbitration hai. 2D mein yeh contribution isolate karke clean test karna possible hai. DA-MAPPO aur IGAT-MARL bhi 2D mein evaluate hue hain — comparison fair rehta hai. 3D extension future work hai."

---

### Q4: DA-MAPPO ablation numbers kahan se hain?

> "Sir, paper mein explicitly likha hai — reference [10]. Unka ablation study dikhata hai ke jab assignment information observation se remove ki jaaye, mission success 90-99% se seedha 0% ho jaati hai. Unka khud ka number hai, mera claim nahi."

---

### Q5: Hungarian algorithm kya hai?

> "Sir, ek combinatorial optimization algorithm jo minimum cost assignment find karta hai. n drones, n targets — algorithm woh assignment find karta hai jisme total cost minimum ho. DA-MAPPO ne dikhaya isko observation vector mein encode karne se mission success dramatically improve hoti hai."

---

### Q6: Conflict graph kya hai?

> "Sir, IGAT-MARL ne propose kiya ke har drone ko sab agents se communicate karne ki zaroorat nahi. Sirf woh drone pairs connect karo jinke beech predicted collision course hai. Isse interaction edges 44% kam hote hain aur avoidance performance better hoti hai. Main isko apne observation vector mein conflict neighborhood ke liye use kar rahi hoon."

---

### Q7: α kaise learn hota hai? Alag loss function hai?

> "Sir, koi alag loss function nahi. PAH MAPPO actor ke saath same policy gradient update mein train hota hai. Reward signal — r_total = α × r_assign + (1−α) × r_avoid — backpropagate hota hai aur PAH ke weights update hote hain. Simple backpropagation, alag training loop nahi, centralized critic mein koi change nahi."

---

### Q8: Baselines kya hain?

> "Sir, 4 baselines: (1) Standard MAPPO — koi assignment, koi conflict graph nahi. (2) DA-MAPPO 2D mein — assignment hai, fixed collision penalty. (3) IGAT-MARL fixed assignment — conflict graph hai, fixed target. (4) Unified framework fixed α (0.3, 0.5, 0.7) — PAH ke bina. Proposed framework — learned α — inhi ke against compare hoga."

---

### Q9: Dec-POMDP kya hai?

> "Sir, Decentralized Partially Observable Markov Decision Process — multi-agent problems ka mathematical framework. 'Partial observability' kyunke har drone sirf local area dekhta hai, complete world state nahi. CTDE isi problem ko solve karta hai: training mein complete joint state use karo, execution mein partial observation se kaam chalo."

---

### Q10: Evaluation metrics kya hain?

> "Sir, primary metric mission success rate — proportion of episodes jisme saare drones apne targets reach kar lein bina collision ke, time limit ke andar. Secondary metrics: inter-drone collision count, obstacle collision count, target reassignments per episode, average trajectory length. 3 swarm sizes (3,5,8) aur 3 obstacle densities (30,40,50) pe test hoga."

---

### Q11: Curriculum learning kyun zaroori hai?

> "Sir, directly 8 drones + high obstacles pe train karna fail ho jaata hai — reward sparse hoti hai. Curriculum learning mein dhire dhire complexity badhate hain — 3 se 5 se 8 drones. DA-MAPPO aur IGAT-MARL dono ne yahi approach use ki hai successfully."

---

### Q12: Research question falsifiable hai? Agar PAH worse perform kare?

> "Sir, bilkul falsifiable hai. Agar learned α fixed α se worse perform kare, yeh bhi valid result hai — matlab dynamic weighting is setting mein help nahi karta, shayad 2D simple environments mein fixed weight sufficient hai. Dono outcomes publishable hain."

---

### Q13: MAPPO kyun choose kiya?

> "Sir, teen reasons: Yu et al. 2022 ne dikhaya MAPPO cooperative MARL mein consistently strong performer hai. DA-MAPPO ne already MAPPO backbone use kiya — comparison clean rehta hai. MAPPO discrete aur continuous action spaces dono handle karta hai, stable convergence deta hai."

---

### Q14: Tumhara actual contribution kya hai, ek line mein?

> "Sir, pehli baar multi-UAV coordination mein ek learned mechanism propose kiya gaya hai jo dynamically decide karta hai ke each drone ko abhi assignment zyada priority deni chahiye ya collision avoidance — instead of pre-set fixed constants jo saare existing frameworks use karte hain."

---

### Q15: Agar sir kuch aisa pooche jo yahan nahi hai

> "Sir, yeh specific detail mujhe abhi exactly yaad nahi — lekin core concept jo main samajhti hoon woh yeh hai: [core concept bolo]. Main specific number baad mein verify kar sakti hoon."

Kabhi mat kaho "mujhe nahi pata." Hamesha core concept se jawab do.
