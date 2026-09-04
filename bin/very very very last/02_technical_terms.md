# Technical Terms — Explained Simply
### Har term yahan hai — parho, samjho, confidently bolo

---

## UAV — Unmanned Aerial Vehicle
**Simple matlab:**
Drone. Koi pilot andar nahi hota. Remote ya automatically fly karta hai.

**Agar sir poochhein:**
> "An unmanned aerial vehicle is an aircraft that operates without a human pilot on board. It can be remotely controlled or fly autonomously using onboard computing."

---

## DRL — Deep Reinforcement Learning
**Simple matlab:**
Ek drone khud sikhta hai kya karna chahiye. Koi rule nahi diya jaata. Har action k baad reward milta hai — acha karo toh positive, bura karo toh negative. Waqt k saath seekh jaata hai.

**Agar sir poochhein:**
> "Deep reinforcement learning is a machine learning approach where an agent learns a policy by interacting with an environment and receiving reward signals. It uses neural networks to approximate the optimal policy without needing an explicit model of the environment."

---

## MARL — Multi-Agent Reinforcement Learning
**Simple matlab:**
DRL ko ek team k leay extend karna. Ab sirf ek drone nahi, poori team seekhti hai — ek doosray k saath kaam karna seekhti hai.

**Agar sir poochhein:**
> "Multi-Agent Reinforcement Learning extends DRL to settings where multiple agents interact in a shared environment. Each agent learns its own policy while also responding to the behavior of other agents."

---

## CTDE — Centralized Training, Decentralized Execution
**Simple matlab:**
Training k waqt sab drones ek doosray ki poori information dekhte hain — jaise team meeting. But jab actual mission hota hai, har drone sirf apni local information use karta hai — akela decide karta hai. 

**Analogy:**
Jaise football team practice mein coach sab ko strategy batata hai, but match mein har player apne judgment say khelta hai.

**Agar sir poochhein:**
> "CTDE is an architecture where during training each agent has access to the global joint state of all agents, which helps learn better coordinated policies. But during execution, each agent acts only on its own local observation — making it feasible for real deployment."

---

## MAPPO — Multi-Agent Proximal Policy Optimization
**Simple matlab:**
Ek specific MARL algorithm. PPO ka multi-agent version. Centralized critic use karta hai training k leay — matlab ek brain jo sab drones ki state dekhta hai — but har drone ka actor independent hota hai.

**Agar sir poochhein:**
> "MAPPO is a cooperative multi-agent algorithm based on PPO. It uses a centralized critic that takes the joint state of all agents to estimate value functions, while each agent's actor uses only local observations. Yu et al. showed that MAPPO is surprisingly competitive with more complex algorithms on cooperative benchmarks."

---

## PPO — Proximal Policy Optimization
**Simple matlab:**
Ek training algorithm jo policy ko slowly update karta hai. Ek dum bada jump nahi leta — gradual aage badhta hai. Isse training stable rehti hai.

**Agar sir poochhein:**
> "PPO is a policy gradient algorithm that limits the size of policy updates using a clipped surrogate objective. This prevents large destabilizing updates and makes training more stable compared to earlier policy gradient methods."

---

## Hungarian Algorithm
**Simple matlab:**
Ek math algorithm jo best assignment find karta hai. Agar 5 drones hain aur 5 targets hain, toh kaunsa drone kaunse target ko assign ho — minimum total cost mein — yeh Hungarian algorithm decide karta hai. Optimal one-to-one matching.

**Analogy:**
Jaise 5 delivery riders hain aur 5 locations — kaunsa rider kaunsi location pe jaaye taake total travel time minimum ho.

**Agar sir poochhein:**
> "The Hungarian algorithm is a combinatorial optimization algorithm that solves the assignment problem in polynomial time. It finds the minimum-cost one-to-one matching between two sets — in our case, drones and targets."

---

## Priority Arbitration Head (PAH)
**Simple matlab:**
Yeh is research ki main contribution hai. Ek chota sa neural network jो har timestep pe decide karta hai — abhi zyada zaroori kya hai, target tak pahunchna ya collision say bachna? Yeh decision ek number alpha k form mein aata hai.

**Agar sir poochhein:**
> "The Priority Arbitration Head is a two-layer feedforward neural network jointly trained with the MAPPO actor. At each decision step, it takes three inputs — time-to-collision, distance to assigned target, and conflict neighbor count — and outputs a single scalar alpha between 0 and 1. This alpha dynamically weights the assignment and avoidance rewards."

---

## Alpha (α)
**Simple matlab:**
Ek number 0 say 1 k beech. PAH yeh output karta hai.
- Alpha = 1 matlab: abhi target assignment zyada important hai, go to target
- Alpha = 0 matlab: abhi collision avoidance zyada important hai, turn away
- Alpha = 0.6 matlab: thoda assignment, thoda avoidance — balance

**Agar sir poochhein:**
> "Alpha is the dynamic arbitration weight output by the Priority Arbitration Head. The blended reward is computed as r = alpha times r-assignment plus 1 minus alpha times r-avoidance. When alpha is high, assignment dominates. When alpha is low, avoidance dominates."

---

## Conflict Graph
**Simple matlab:**
Ek graph jisme sirf woh drone pairs connected hote hain jo collision course pe hain. Saare drones ko saare drones say connect karna expensive hai. Toh sirf woh pairs connect karo jo actually conflict mein hain — sparse graph.

**Agar sir poochhein:**
> "A conflict graph is a sparse graph where nodes represent drones and edges connect only those drone pairs that are predicted to come within a dangerous distance within a specified time horizon. This replaces the dense all-to-all interaction graph used in earlier work, reducing computational complexity significantly."

---

## Curriculum Learning
**Simple matlab:**
Pehle asaan cheez seekho, phir mushkil. Jaise school mein pehle addition seekhte hain phir multiplication. Drones k leay: pehle 3 drones, simple environment. Phir 5 drones, moving targets. Phir 8 drones, bahut obstacles.

**Agar sir poochhein:**
> "Curriculum learning is a training strategy where the difficulty of the training environment is progressively increased. The agent first masters simpler scenarios before being exposed to more complex ones. This leads to more stable and effective learning compared to training directly on the hardest configuration."

---

## Dec-POMDP — Decentralized Partially Observable Markov Decision Process
**Simple matlab:**
Ek formal math framework jisme multiple agents hote hain, har agent sirf apnay around ki information dekh sakta hai (partial), aur decisions independently leta hai (decentralized).

**Agar sir poochhein:**
> "Dec-POMDP is the formal mathematical framework for multi-agent decision making under partial observability. Each agent has its own local observation and must act without seeing the full global state. Our problem is naturally formulated as a Dec-POMDP."

---

## Reward Function
**Simple matlab:**
Yeh batata hai drone ko kab acha kiya aur kab bura. Positive reward = target tak pahuncha. Negative reward = collision hui. Is research mein reward blend hoti hai — r = alpha times r-assign plus (1-alpha) times r-avoid.

---

## Ablation Study
**Simple matlab:**
Ek experiment jisme aap ek ek component hatate jao aur dekhte jao kya performance drop hoti hai. Isse prove hota hai k har component actually zaroori hai.

**Agar sir poochhein:**
> "An ablation study systematically removes components of a framework one at a time to measure each component's individual contribution to the overall performance."

---

## Observation Vector
**Simple matlab:**
Woh saari information jo ek drone ko di jaati hai taake woh decision le sake. Is research mein har drone ko 4 cheezein pata hoti hain: apni position, target ki position, conflict neighbors ki position, obstacles ki proximity.

---

## Baseline
**Simple matlab:**
Comparison k leay ek simple ya existing method. Hum apna method baseline say compare karte hain yeh prove karne k leay k hamara better hai.

---

## Mission Success Rate
**Simple matlab:**
Kitne percent episodes mein saare drones apne targets tak pahunche — bina kisi collision k, time limit k andar. Yeh main performance metric hai.
