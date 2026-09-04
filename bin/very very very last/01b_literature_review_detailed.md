# Literature Review — Detailed Version
### Har paper ki poori detail — kya kiya, kaise kiya, kya miss kiya

---

## PEHLE YEH SAMJHO — Literature Review Ka Maqsad

Literature review mein hum yeh dikhate hain:
1. Is problem pe pehle kya kaam hua hai
2. Har paper ne kya contribute kiya
3. Har paper ki limitation kya thi
4. Yeh saab mila k humari research ki zaroorat kyun hai

---

## GROUP 1 — Single UAV Path Planning

### [1] Tang et al. 2024 — Improved D3QN
**Paper:** "Dynamic scene path planning of UAVs based on deep reinforcement learning" — Drones journal

**Problem jo inhone solve ki:**
Ek akela drone dynamic environment mein navigate kare — matlab obstacles move kar rahe hain — aur target tak pahunche.

**Method:**
- **D3QN** = Double DQN + Dueling Network + Prioritized Experience Replay — teeno improvements ek saath
- **Double DQN** (Van Hasselt et al.): Q-values ki overestimation fix karta hai
- **Dueling Network** (Wang et al.): State value aur action advantage ko alag estimate karta hai
- **PER** (Schaul et al.): Important transitions ko zyada sample karta hai — rare but informative events se zyada seekhta hai
- **Heuristic action selection:** Target ki taraf bias — random explore nahi karta blindly

**Results:**
- ~95% success rate in moving threat zones
- A* aur RRT path planning algorithms say better

**Limitation:**
- Sirf ek drone — koi coordination nahi
- Multiple drones k saath yeh approach directly scale nahi hoti
- Koi target assignment nahi — target fixed hota hai

**Table mein:**
Single UAV | Dynamic Obstacles ✓ | Target Assignment ✗ | Collision Avoidance ✗ | Path Optimization ✓ | Fixed Weights

---

### [3] Jarray et al. 2025 — Dynamic Reward DQN
**Paper:** "Dynamic reward-based deep reinforcement learning algorithm for UAV path planning in large-scale environments" — Procedia Computer Science

**Problem jo inhone solve ki:**
Large-scale environments mein — matlab bahut bade map pe — ek drone efficiently navigate kare.

**Method:**
- **Dynamic reward function:** Reward har step pe distance ratio say calculate hoti hai — static reward nahi
- r(t) = d(t-1) / d(t) — agar drone target k qareeeb aaya toh ratio > 1 — positive reward
- **3D CNN:** Environment ki feature extraction k leay — spatial information better capture hoti hai
- Standard DQN policy

**Results:**
- 98% success in low obstacle environments (30 obstacles)
- 85% in high obstacle environments (40 obstacles)
- Particle Swarm Optimization aur Grey Wolf Optimization say better

**Yeh interesting kyun hai:**
Yeh single paper hai jisme **dynamic weights** hain — reward function adapt hoti hai. But yeh dynamic reward hai — policy weights nahi. Aur phir bhi single drone hai.

**Limitation:**
- Single UAV only
- No multi-agent coordination
- Dynamic reward ≠ learned priority — sirf distance ratio hai

**Table mein:**
Single UAV | Dynamic Obstacles ✓ | Target Assignment ✗ | Collision Avoidance ✗ | Path Optimization ✓ | Dynamic Weights

---

## GROUP 2 — Multi-UAV Coordination

### [2] Kong et al. 2024 — TANet-TD3
**Paper:** "Multi-UAV simultaneous target assignment and path planning based on deep reinforcement learning in dynamic multiple obstacles environments" — Frontiers in Neurorobotics

**Problem jo inhone solve ki:**
Multiple drones ko simultaneously target assign bhi karna aur path plan bhi karna — ek saath — dynamic obstacles k saath.

**Method:**
- **TD3** (Twin Delayed Deep Deterministic Policy Gradient): Continuous action space k leay stable algorithm
  - Clipped double Q-learning: overestimation fix
  - Delayed policy updates: critic pehle stable ho, phir actor update
  - Target policy smoothing: noisy targets use karta hai overfit hone say bachne k leay
- **Hungarian algorithm supervision:** Training mein Hungarian algorithm use hota hai correct assignment labels k leay — supervised signal
- **Partial observability:** Drones sirf apni surrounding dekhte hain — poori map nahi

**Environment:**
- 5 drones, 2D environment
- Dynamic obstacles — move karte hain
- Partial observability

**Results:**
- Multiple obstacle densities pe tested
- Target assignment aur path planning simultaneously achay results

**Limitation:**
- Koi explicit inter-drone collision avoidance mechanism nahi
- Drones apne targets tak pahunch jaate hain but ek doosray say takra sakte hain
- 2D only

**Table mein:**
Multi UAV | Dynamic Obstacles ✓ | Target Assignment ✓ | Collision Avoidance ✗ | Path Optimization ✓ | Fixed Weights

---

### [4] Zhang et al. 2025 — Mean-Field DDPG
**Paper:** "Large-scale UAV swarm path planning based on mean-field reinforcement learning" — Chinese Journal of Aeronautics

**Problem jo inhone solve ki:**
Bahut zyada drones — 80 say 120 tak — ek saath coordinate karein. Standard MARL itne agents k saath computationally infeasible ho jaata hai.

**Method:**
- **Mean Field Theory:** Ek agent aur poori population k beech interaction ko ek "mean field" term say approximate karo
- Pairwise interactions O(n²) hoti hain — mean field yeh O(n) kar deta hai
- **DDPG** (Deep Deterministic Policy Gradient): Continuous action space
- **Multi-head attention:** Important agents pe zyada focus

**Results:**
- 90%+ success rate at 120 drones
- Standard MARL baselines fail karte hain is scale pe

**Yeh important kyun hai:**
Scalability problem solve ki — 120 drones coordinate karna ek major achievement hai.

**Limitation:**
- Koi collision avoidance nahi — drones sirf path follow karte hain
- Koi dynamic target assignment nahi — targets fixed hain
- 2D environment

**Table mein:**
Multi UAV | Dynamic Obstacles ✗ | Target Assignment ✗ | Collision Avoidance ✗ | Path Optimization ✓ | Fixed Weights

---

### [5] Poudel & Moh 2026 — MAML-MARL
**Paper:** "MAML-integrated multi-agent reinforcement learning for adaptive coalition-based UAV coordination in disaster scenarios" — Internet of Things journal

**Problem jo inhone solve ki:**
Disaster scenarios mein heterogeneous drone fleets — matlab alag alag capabilities wale drones — coordinate karein. Environment completely naya ho sakta hai — drones ne pehle kabhi nahi dekha.

**Method:**
- **MAML** (Model Agnostic Meta-Learning): "Learning to learn" — drone thodi training mein nayi environment mein adapt ho jaaye
- Fast adaptation: Few gradient steps mein nayi situation mein kaam kare
- **Coalition formation:** Resource constraints k hisaab say drones groups mein kaam karte hain
- Heterogeneous capabilities handle karta hai

**Results:**
- Nayi environments mein fast adaptation
- Standard MARL say better generalization

**Limitation:**
- Target assignment mechanism nahi — koi explicit target-to-drone assignment nahi
- Collision avoidance mechanism nahi
- Path optimization primary focus nahi

**Table mein:**
Multi UAV | Dynamic Obstacles ✓ | Target Assignment ✗ | Collision Avoidance ✗ | Path Optimization ✗ | Fixed Weights

---

## GROUP 3 — Most Related Work (Base Papers)

### [9] Rezaee et al. 2026 — IGAT-MARL
**Paper:** "Efficient multi-agent deep reinforcement learning algorithm for multi-UAV collision avoidance" — Applied Soft Computing

**Yeh hamara BASE PAPER hai collision avoidance k leay.**

**Problem jo inhone solve ki:**
Multiple drones fly kar rahe hain aur ek doosray say collide nahi karna. Existing methods dense all-to-all interaction use karti thein — computationally expensive aur irrelevant information include karti thein.

**Method — detail mein:**

**Step 1 — Conflict Graph Construction:**
- Har timestep pe har drone pair k leay check karo
- Kya yeh dono current trajectory pe ek defined time window mein dangerous distance k andar aa jaayenge?
- Agar haan → edge add karo (conflict pair)
- Result: Sparse graph — sirf actual conflicts

**Step 2 — Improved Graph Attention Network (IGAT):**
- **Standard GAT** (Graph Attention Network): Neighbors ki information attend karo — kuch neighbors zyada important hote hain
- **Stacked double attention:** Pehle ek baar GAT lagao, phir dobaara us output pe — refined representation
- **Residual connections:** Original information preserve karo deep layers mein — vanishing gradient problem avoid
- Har drone apne conflict neighbors ki information aggregate karta hai

**Step 3 — Observation:**
Har drone observe karta hai:
- Apni position aur velocity
- Conflict neighbors ki positions aur velocities (sirf woh jo graph mein hain)
- **Note:** Koi target information nahi

**Step 4 — Policy:**
- MARL policy — koi specific algorithm mention nahi zyada detail mein
- Centralized training, decentralized execution
- Output: 2D velocity commands

**Step 5 — Reward:**
- Positive: Dusray drones say safe distance maintain karo
- Negative: Collision ho jaaye
- Koi target-related reward nahi

**Step 6 — Curriculum Learning:**
- 3 drones say start, 5, 7, 10 drones tak progressively

**Results:**
- 44% fewer interaction edges compared to dense graph baseline
- 17% higher reward than best prior method
- 10% fewer dangerous separation events
- Tested up to 10 drones

**Limitation — Inhone khud kaha:**
> "The proposed framework does not incorporate task allocation. Future work will integrate task assignment mechanisms to enable goal-directed multi-UAV coordination."

**Is research mein contribution:**
Humne IGAT-MARL ka conflict graph mechanism adopt kiya. Sparse conflict-driven graph observation ka part hai. But humne iske upar target assignment add ki aur PAH k through dono balance kiye.

**Table mein:**
Multi UAV | Dynamic Obstacles ✓ | Target Assignment ✗ | Collision Avoidance ✓ | Path Optimization ✗ | Fixed Weights

---

### [10] Sheng et al. 2026 — DA-MAPPO
**Paper:** "Dynamic target assignment and cooperative decision-making for UAV swarms based on multi-agent reinforcement learning" — IEEE Internet of Things Journal

**Yeh hamara BASE PAPER hai target assignment k leay.**

**Problem jo inhone solve ki:**
Multiple drones ko real-time mein targets assign karna — jab targets move karein — aur drones unhe efficiently reach karein. Pehle k assignment methods static thay — ek baar assign karo phir change nahi hoti.

**Method — detail mein:**

**Step 1 — Hungarian Assignment Integration:**
- Har decision step pe (har timestep pe) Hungarian algorithm run hota hai
- Saare drones aur saare targets k beech minimum cost assignment compute hoti hai
- Cost = Euclidean distance (drone-to-target)
- Assignment result: Drone 1 → Target 3, Drone 2 → Target 1, etc.

**Step 2 — Observation Vector:**
Har drone observe karta hai:
- Apni 2D position aur velocity
- Apne **currently assigned target** ki relative position (Hungarian algorithm say real-time update)
- Obstacles ki proximity
- **Note:** Koi conflict graph nahi — inter-drone collision avoidance mechanism nahi

**Step 3 — MAPPO Policy:**
- Centralized critic: Poori swarm ki joint state dekhta hai
- Decentralized actors: Har drone apni local observation say action leta hai
- Output: 2D velocity commands

**Step 4 — Reward:**
- Positive: Assigned target k qareeb aao
- Positive: Target reach karo
- Negative: Obstacle se takrao
- Koi explicit inter-drone collision avoidance reward nahi — sirf ek simple penalty

**Step 5 — Environment:**
- 3 drones, 2D environment
- Static obstacles
- Targets initially static (limited dynamic testing)

**Results:**
- Mission success rate: 90% to 99% across configurations
- **Critical ablation result:** Assignment information remove karne par success 90% → 0%

**Ablation study — yeh bahut important hai:**
Unhone systematically remove kiya:
1. Hungarian assignment → Mission success 0% (sab fail)
2. MAPPO → Performance drop
3. Joint training → Performance drop

**Matlab:** Assignment mechanism is framework ka core hai. Bina assignment k kuch kaam nahi karta.

**Limitation — Inhone khud kaha:**
> "The current framework does not include an explicit mechanism for inter-agent collision avoidance. This is identified as a key direction for future work, along with extension to larger swarm sizes."

**Is research mein contribution:**
Humne DA-MAPPO ka Hungarian assignment mechanism adopt kiya. Yeh observation ka second element hai. But humne iske upar conflict graph add ki (IGAT-MARL say) aur PAH k through dono objectives dynamically balance kiye.

**Table mein:**
Multi UAV | Dynamic Obstacles ✗ | Target Assignment ✓ | Collision Avoidance ✗ | Path Optimization ✓ | Fixed Weights

---

## SABSE IMPORTANT SUMMARY TABLE

| | [9] IGAT-MARL | [10] DA-MAPPO | Our Work |
|---|---|---|---|
| Target Assignment | ✗ | ✓ | ✓ |
| Collision Avoidance | ✓ | ✗ | ✓ |
| Dynamic Priority Weights | ✗ | ✗ | ✓ |
| Conflict Graph | ✓ | ✗ | ✓ |
| Hungarian Assignment | ✗ | ✓ | ✓ |
| Mission Success Rate | N/A (no targets) | 90-99% | To be evaluated |
| What they missed | Assignment | Avoidance | — |
| What they said next | "Add assignment" | "Add avoidance" | We did both |

---

## PRESENTATION MEIN YEH LINE ZAROOR BOLNA:

> "Sir, what makes this research well-motivated is that DA-MAPPO explicitly identifies collision avoidance as future work, and IGAT-MARL explicitly identifies target assignment as future work. These are not vague suggestions — they are direct statements in the conclusion sections of both papers. Our research directly addresses what both papers asked for next."
