# Technical Terms — Detailed Version
### Har term ko poori depth mein samjho

---

## 1. UAV — Unmanned Aerial Vehicle

**Kya hota hai:**
UAV ek aisi aircraft hai jisme koi insaan andar nahi baith kar fly karta. Yeh ya toh remote control say chalti hai ya khud apne onboard computer say autonomously fly karti hai. Aaj kal commonly "drone" kaha jaata hai.

**Real world mein:**
- Amazon deliveries k leay
- Disaster zones mein search aur rescue
- Military surveillance
- Kheton mein pesticide spray karna
- Infrastructure inspection — bridges, power lines

**Is research mein:**
Hum multiple UAVs ko coordinate karna chahte hain — ek saath fly karte hue — taake woh mission complete kar sakein bina ek doosray say takraaye.

**Agar sir poochhein define karo:**
> "An unmanned aerial vehicle is an aircraft that operates without an onboard human pilot, either remotely controlled or autonomously guided by onboard computing systems. In this research, UAVs are quadcopters operating in a shared 2D airspace."

---

## 2. Deep Reinforcement Learning (DRL)

**Aam zindagi mein analogy:**
Socho aik bacha pehli baar cycle chalana seekh raha hai. Koi usse step-by-step instructions nahi deta. Woh khud try karta hai — girta hai, uthta hai, adjust karta hai — aur waqt k saath seekh jaata hai. DRL exactly yahi karta hai, but machine k leay.

**Technical matlab:**
- **Agent** = drone (jo seekh raha hai)
- **Environment** = simulation jahan drone fly karta hai
- **State** = agent ki current situation (position, velocity, obstacles)
- **Action** = agent kya karta hai (move left, right, up, down)
- **Reward** = feedback — acha kiya toh positive number, bura kiya toh negative
- **Policy** = learned rules — given this state, take this action

**Kaise seekhta hai:**
1. Agent state observe karta hai
2. Action leta hai
3. Environment response deta hai (nayi state + reward)
4. Agent apni policy update karta hai
5. Repeat — hazaaron baar — until policy optimal ho jaaye

**Deep ka matlab:**
Policy ko represent karne k leay deep neural network use hoti hai — isliye "Deep" reinforcement learning.

**Agar sir poochhein:**
> "Deep reinforcement learning is a machine learning paradigm where an agent learns an optimal policy by interacting with an environment, receiving scalar reward signals, and updating its neural network parameters to maximize cumulative reward over time — without requiring an explicit model of the environment dynamics."

---

## 3. Multi-Agent Reinforcement Learning (MARL)

**Aam zindagi mein analogy:**
DRL ek akele khiladi k leay tha. MARL poori football team k leay hai. Har player apna role seekhta hai, but saath mein coordinate bhi karta hai taake team goal score kare.

**Technical matlab:**
- Multiple agents ek shared environment mein hote hain
- Har agent apni state observe karta hai
- Har agent apna action leta hai
- Actions sab mili k environment ko affect karti hain
- Reward cooperative ho sakta hai (sabko milta hai) ya competitive

**Challenges jo MARL mein aate hain:**
1. **Non-stationarity:** Jab ek agent seekh raha hota hai, doosra bhi seekh raha hota hai — environment effective mein change ho raha hai dono k leay
2. **Credit assignment:** Agar team ne goal kiya, kis agent ka contribution tha?
3. **Scalability:** Agents badhne say complexity exponentially badhti hai

**Is research mein:**
Sare drones ek cooperative team hain — saath mein targets cover karne chahte hain bina collision k. Koi competitive element nahi.

**Agar sir poochhein:**
> "Multi-Agent Reinforcement Learning extends DRL to environments with multiple simultaneously learning agents. Each agent has its own observation, action, and policy, but agents share the environment and may cooperate or compete. MARL introduces challenges like non-stationarity and credit assignment that do not exist in single-agent settings."

---

## 4. CTDE — Centralized Training, Decentralized Execution

**Aam zindagi mein analogy:**
Ek football team ki practice mein coach saare players ko ek saath strategy batata hai — full information share hoti hai. But match k waqt coach field pe nahi hota. Har player khud apne judgment say khelta hai — sirf jo woh apni aankhon say dekh sakta hai.

CTDE exactly yahi hai.

**Training phase (Centralized):**
- Saare drones ek doosray ki full information dekhte hain
- Centralized critic poori joint state use karta hai value estimate karne k leay
- Agents better coordination seekhte hain kyunki unhe pata hai doosre kya kar rahe hain

**Execution phase (Decentralized):**
- Real mission mein har drone sirf apni local observation use karta hai
- Koi central server nahi chahiye
- Practical deployment k leay suitable — real drones ko communication k bina bhi kaam karna hota hai

**Yeh kyun important hai:**
Agar training bhi decentralized ho, agents sirf apni limited info say seekhte hain — suboptimal policies milti hain. CTDE training quality improve karta hai while keeping deployment practical.

**Agar sir poochhein:**
> "CTDE is an architectural paradigm where during training each agent's critic has access to the global joint state of all agents, enabling better value estimation and coordinated policy learning. During execution, each agent's actor uses only its own local observation, making the system scalable and deployable without requiring inter-agent communication."

---

## 5. PPO — Proximal Policy Optimization

**Simple matlab:**
PPO ek training algorithm hai jo policy ko update karta hai — but carefully. Ek dum bada step nahi leta. Ek clipping mechanism use karta hai jo ensure karta hai k nayi policy pehli policy say bahut zyada alag na ho.

**Kyun zaroori hai:**
Agar policy update bahut bada ho toh training unstable ho jaati hai — agent bohot achay say perform karna start karta hai phir suddenly bilkul kharab ho jaata hai. PPO yeh prevent karta hai.

**Technical detail:**
PPO ka clipped surrogate objective:
- Policy ratio r = (new policy probability) / (old policy probability)
- Clip(r, 1-ε, 1+ε) — ratio ko ek range mein rakhta hai
- ε usually 0.2 hota hai — matlab policy 20% say zyada change nahi ho sakti ek step mein

**Agar sir poochhein:**
> "PPO is a policy gradient algorithm that constrains the size of policy updates using a clipped surrogate objective. This prevents large destabilizing updates while maintaining training stability and sample efficiency, making it one of the most widely used reinforcement learning algorithms."

---

## 6. MAPPO — Multi-Agent Proximal Policy Optimization

**Simple matlab:**
PPO ka multi-agent version. Har agent PPO use karta hai apni policy update karne k leay. But ek shared centralized critic hoti hai jo poori team ki joint state dekhti hai.

**Structure:**
- **Actor (per agent):** Local observation → Action. Har drone ka apna actor hota hai.
- **Critic (shared/centralized):** Joint state of all agents → Value estimate. Training mein help karta hai.

**Yu et al. 2022 ne kya discover kiya:**
MAPPO surprisingly competitive hai bahut complex MARL algorithms k saath — jaise QMIX, MADDPG — cooperative benchmarks pe. Simple hone k bawajood effective hai.

**Is research mein kyun choose kiya:**
DA-MAPPO — humara base paper — already MAPPO use karta hai target assignment k leay aur 90-99% success rate achieve karta hai. Isliye MAPPO hamara natural choice tha.

**Agar sir poochhein:**
> "MAPPO applies PPO in a multi-agent cooperative setting using a centralized critic that takes the joint state of all agents during training, while each agent's actor uses only its local observation during execution. Yu et al. 2022 demonstrated that MAPPO achieves competitive performance with significantly more complex algorithms on cooperative multi-agent benchmarks."

---

## 7. Hungarian Algorithm

**Aam zindagi mein analogy:**
5 delivery riders hain aur 5 locations. Har rider ki har location tak distance alag hai. Kaunsa rider kahan jaaye taake total travel time minimum ho? Hungarian algorithm yeh optimal assignment ek second mein compute kar deta hai.

**Mathematical basis:**
- Assignment problem — bipartite graph mein minimum cost perfect matching
- Polynomial time solution: O(n³) complexity — n drones k leay
- Optimal solution guaranteed — koi better assignment possible nahi

**Is research mein kaise use hota hai:**
- Har decision step pe — matlab har 0.1 second pe ya jitna bhi timestep hai
- Saare drones aur saare targets k beech minimum total distance assignment compute hoti hai
- Yeh assignment har drone ki observation mein jaati hai — drone ko pata hota hai uska current target kaunsa hai
- Jab target move kare ya environment change ho, assignment automatically update hoti hai

**DA-MAPPO ne kya prove kiya:**
Jab unhone Hungarian assignment remove kiya apnay ablation study mein, success rate 90% say 0% ho gayi. Yeh prove karta hai k dynamic real-time assignment kitni critical hai.

**Agar sir poochhein:**
> "The Hungarian algorithm is a combinatorial optimization algorithm that solves the minimum-cost bipartite matching problem in O(n³) time. In our framework, it runs at every decision step to compute the optimal one-to-one assignment between drones and targets, ensuring that the total assignment cost across all drones is minimized. This assignment is included in each drone's observation vector."

---

## 8. Priority Arbitration Head (PAH)

**Yeh kya hai — core contribution:**
Ek chota feedforward neural network (2 layers, 64 neurons) jo har timestep pe ek sawaal ka jawab deta hai: "Is drone k leay is waqt, kya zyada zaroori hai — apne target tak pahunchna ya collision say bachna?"

**Kyun zaroori hai:**
Pehle k saare methods mein reward weights fixed the. Matlab training say pehle decide karo k assignment reward ko 0.7 weight do aur avoidance reward ko 0.3 weight do. Yeh weights kabhi nahi badlte. But real situations mein:
- Kabhi drone target k qareeb hota hai — tab assignment urgent
- Kabhi doosra drone bilkul saamne aa jaata hai — tab avoidance urgent
- Fixed weights yeh distinction nahi kar sakti

PAH yeh distinction siikhti hai — dynamically.

**3 Inputs:**
1. **τ_collision (time-to-collision):** Nearest conflict neighbor say kitne waqt mein collision ho sakti hai. Agar 2 second hain toh danger high. Agar 10 second hain toh danger low.
2. **d_target (distance to target):** Assigned target kitna door hai. Agar 5 meter door hai, urgency high. Agar 50 meter door hai, urgency lower.
3. **n_conflict (conflict neighbor count):** Abhi kitne drones conflict zone mein hain. 3 drones saamne hain toh avoidance zyada urgent hai 1 drone k comparison mein.

**Output:**
- **α (alpha):** Single number 0 say 1 k beech
- α = 0.9 → assignment pe 90% focus, avoidance pe 10%
- α = 0.1 → avoidance pe 90% focus, assignment pe 10%
- α = 0.5 → equal balance

**Reward formula:**
```
r_total = α × r_assignment + (1 − α) × r_avoidance
```

**Training:**
- MAPPO actor k saath jointly train hota hai
- Same policy gradient update dono ko update karta hai
- PAH k weights alag say train nahi hote — ek hi loss function

**Deployment:**
- Har drone pe locally run hota hai
- Centralized information nahi chahiye
- 3 scalar inputs hi kaafi hain — computationally lightweight

**Agar sir poochhein:**
> "The Priority Arbitration Head is a two-layer feedforward network with 64 neurons per layer, jointly trained with the MAPPO actor through the same policy gradient update. At each decision step, it takes three scalar inputs — time-to-collision, distance to assigned target, and conflict neighbor count — and outputs a single scalar alpha between 0 and 1. This alpha dynamically weights the assignment and avoidance components of the reward signal, replacing the fixed hand-tuned coefficients used in all prior work."

---

## 9. Conflict Graph

**Simple matlab:**
Imagine karo 8 drones hain. Agar hum saare 8 ko ek doosray say connect karein toh 28 connections banenge (8×7/2). Yeh bahut expensive hai computationally aur zyaada tar connections irrelevant hain — woh drones actually collision course pe hain hi nahi.

Conflict graph ek smarter approach hai: sirf un drones ko connect karo jo actually ek certain time window mein collide karne wale hain.

**Kaise banta hai:**
- Har timestep pe, har drone pair k leay check karo
- Kya yeh dono apni current trajectory pe chal rahe hain toh ek defined time window mein dangerous distance k andar aa jaayenge?
- Agar haan — edge add karo graph mein
- Agar nahi — ignore karo

**Faida:**
- 44% fewer edges (IGAT-MARL result)
- Sirf relevant information process hoti hai
- Computationally efficient
- Graph attention network ko better quality input milta hai

**Is research mein:**
Conflict graph say milne wali information drone ki observation ka third element hai — "positions and velocities of conflict neighbors."

**Agar sir poochhein:**
> "A conflict graph is a sparse graph where nodes represent drones and directed edges connect pairs of drones predicted to enter a dangerous proximity within a specified time horizon. This replaces the dense all-to-all interaction graph, reducing computational complexity and focusing the graph attention network on actually relevant interactions."

---

## 10. Curriculum Learning

**Aam zindagi mein analogy:**
Primary school mein pehle 1+1 sikhate hain, phir multiplication, phir algebra. Direct calculus say start nahi karte. Yahi principle curriculum learning mein use hota hai.

**Is research mein 4 stages:**

| Stage | Kya sikhte hain | Kyun |
|---|---|---|
| Stage 1 | 3 drones, static targets, basic obstacles | DA-MAPPO replicate karo — validate karo k framework kaam karta hai |
| Stage 2 | 5 drones, moving targets, kuch obstacles | Complexity badhao — assignment harder ho jaati hai |
| Stage 3 | 8 drones, high obstacle density, dynamic targets | Near-real-world difficulty |
| Stage 4 | Unseen swarm sizes | Generalization test |

**Kyun zaroori hai:**
Agar seedha 8 drones aur high obstacle density say start karein toh agent kuch nahi seekhta — reward itna sparse hota hai k koi meaningful gradient nahi milti. Easy say start karo, phir mushkil banao — stable aur effective learning hoti hai.

**Agar sir poochhein:**
> "Curriculum learning is a training strategy where task difficulty is progressively increased as the agent's competence improves. We start with 3 drones in a simple environment to establish a validated baseline, then progressively increase swarm size and environmental complexity to develop robust coordination behavior."

---

## 11. Ablation Study

**Simple matlab:**
Aap nay ek framework banaya jisme 3 parts hain: A, B, C. Claim hai k saare teeno important hain. Ablation study mein aap prove karte hain:
- A remove karo → performance drop hoti hai
- B remove karo → performance drop hoti hai  
- C remove karo → performance drop hoti hai
- Sab saath → best performance

Yeh prove karta hai k har component actually contribute kar raha hai.

**Is research mein ablation:**
- PAH remove karo (fixed alpha use karo) — kitna drop?
- Conflict graph remove karo — kitna drop?
- Hungarian assignment remove karo — kitna drop?
- Learned alpha vs fixed alpha (0.3, 0.5, 0.7) — kaunsa better?

**Agar sir poochhein:**
> "An ablation study systematically removes or replaces individual components of the proposed framework to isolate and quantify each component's contribution to overall performance. We will compare the full framework against versions with the PAH replaced by fixed alpha values of 0.3, 0.5, and 0.7."

---

## 12. Dec-POMDP

**Full form:** Decentralized Partially Observable Markov Decision Process

**Simple matlab:**
Yeh ek formal math framework hai jo multi-agent problems ko rigorously define karta hai.

- **Decentralized:** Har agent apna decision khud leta hai — koi central controller nahi
- **Partially Observable:** Har agent sirf apne around ki information dekh sakta hai — poori world nahi
- **Markov:** Current state mein saari zaroori information hai — past history ki zaroorat nahi
- **Decision Process:** Agents decisions lete hain sequence mein — time step by time step

**Is research mein:**
Hamara problem naturally Dec-POMDP hai. Har drone sirf apni local observation dekhta hai (partial), decisions independently karta hai (decentralized), aur current state sufficient hai future planning k leay (Markov).

**Agar sir poochhein:**
> "Our problem is formally modeled as a Dec-POMDP — a Decentralized Partially Observable Markov Decision Process — where each UAV has its own local observation space, acts independently during execution, and the joint state satisfies the Markov property. This is the standard formal framework for cooperative multi-agent coordination problems."

---

## 13. Mission Success Rate

**Simple matlab:**
Total episodes mein say kitne percent episodes mein SAARE drones apne assigned targets tak pahunche — bina kisi collision k aur time limit k andar.

**Example:**
100 episodes run kiye. 87 mein saare drones successful rahe. Mission success rate = 87%.

**Kyun yeh main metric hai:**
Yeh ek complete measure hai — assignment aur avoidance dono simultaneously achay hone chahiye. Agar sirf avoidance achay karein lekin targets na pohonchen — 0%. Agar sirf targets pohonchen lekin collide karein — 0%.

---

## 14. Observation Vector

**Simple matlab:**
Woh saari information ka set jo ek drone ko har timestep pe diya jaata hai taake woh decide kar sake kya karna hai.

**Is research mein har drone ka observation:**
```
o_i = [self_state, assignment_state, conflict_neighbors, obstacle_proximity]
```

1. **self_state:** Drone ki 2D position (x,y) + velocity (vx,vy)
2. **assignment_state:** Assigned target ki relative position — Hungarian algorithm say
3. **conflict_neighbors:** Conflict graph mein connected drones ki positions aur velocities
4. **obstacle_proximity:** 4 directions mein nearest obstacles ki distances

Yeh sab mila k ek vector banta hai jo actor network ko input jaata hai.
