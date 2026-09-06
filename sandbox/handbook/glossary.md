# Glossary — saare technical words, simple Hinglish mein

Jab bhi koi word samajh na aaye, yahan dekho. Alphabet order.

---

**Ablation study** — ek experiment jismein tum apne system ka ek hissa **nikaal** ke
dekhte ho ki performance kitni giri. Isse pata chalta hai ki wo hissa actually kitna
zaroori tha. Jaise gaadi se ek pehiya nikaal ke dekhna.

**Actor (MAPPO mein)** — har drone ka "decision-maker" neural network. Input: drone ko
kya dikh raha hai. Output: ab kahan move karna hai.

**Advantage** — "ye action average se kitna behtar tha?" Number. Positive = expected se
achha, negative = bura. RL isse seekhta hai ki kaunse action encourage karne hain.

**Alpha (α)** — 0 aur 1 ke beech ka ek number. Batata hai ki abhi drone ka focus kitna
mission pe (target tak pahunchna) aur kitna safety pe (takkar se bachna). α = 0.9 →
90% mission, 10% safety. **PAH isko har step pe khud decide karta hai — yehi thesis ka
naya kaam hai.**

**Baseline** — ek "comparison ke liye rakha gaya system". Tumhara naya method kitna
achha hai, ye tabhi pata chalega jab usse kisi purane/simple method se compare karo.

**Centralized critic** — training ke waqt ek network jo **poori duniya** dekhta hai
(saare drones, targets, obstacles) aur batata hai "ye situation kitni achhi hai".
Sirf training mein use hota hai, deployment mein nahi.

**Checkpoint** — training ke beech mein model ko file mein **save** karna, taaki agar
session band ho jaaye to dobara zero se shuru na karna pade.

**Collision avoidance** — drones ko aapas mein ya obstacle se **takrane se bachaana**.

**Conflict graph** — ek diagram jo sirf un drone-pairs ko jodta hai jinki **aane wale
kuch second mein takkar ho sakti hai**. Baaki sab ignore. Isse cheezein simple rehti
hain jab drones zyada ho.

**CPA (Closest Point of Approach)** — do drones apne raaste pe chalte rahein to wo
ek dusre ke **sabse kareeb** kis waqt aur kitni doori pe aayenge. Do numbers:
DCPA (doori) aur TCPA/`t*` (kitni der mein).

**CTDE (Centralized Training, Decentralized Execution)** — training ke waqt sab kuch
pata hota hai (global info), lekin asli use ke waqt har drone sirf apni local info se
kaam karta hai. MAPPO isi tarah kaam karta hai.

**Curriculum learning** — pehle aasaan level, phir dheere-dheere mushkil. Jaise school —
pehle jodना, phir guna. Hum: pehle 3 drones no obstacles, phir 8 drones dense obstacles.

**Dec-POMDP** — "multiple agents, sab ko sirf apni aadhi-adhoori info dikhti hai" wale
problem ka formal naam. Poora: Decentralized Partially Observable Markov Decision Process.

**Discount factor (γ, gamma)** — "future reward abhi ke reward se kitna kam important".
0.99 = future kaafi important. RL ka standard parameter.

**Episode** — ek poora "game" — reset se lekar (sab drones apne target pe pahunch gaye
YA koi takra gaya YA time khatam) tak.

**GAE (Generalized Advantage Estimation)** — advantage (upar dekho) ko smooth tarike se
calculate karne ka tareeqa. Kam shor, better training.

**Gymnasium** — Python ki ek library jo RL environments ka ek **standard shape** deti
hai (`reset()`, `step()` functions). Pehle iska naam "OpenAI Gym" tha.

**Hungarian algorithm** — ek pakka (optimal) tareeqa "kaun sa drone kaun sa target le"
decide karne ka, taaki total doori sabse kam ho. SciPy mein already bana hua hai
(`linear_sum_assignment`).

**Hyperparameter** — training se pehle haath se set kiya jaane wala setting
(learning rate, batch size, etc.). Model inhe khud nahi seekhta.

**LiDAR** — laser se doori naapne wala sensor. DA-MAPPO ne 35 beams use kiye. Hum simple
rakhte hain — 4 directions mein doori.

**Loss of separation / dangerous-proximity time** — kitne steps do drones "khatarnak
tarike se kareeb" the. Safety ka measure (kam = achha).

**MAPPO (Multi-Agent PPO)** — PPO ka multi-agent version. Har drone ka apna actor,
ek shared critic. Hamare research ka main "brain".

**Mission Success Rate (MSR)** — kitne percent episodes mein **saare** drones apne
target pe pahunche **bina kisi takkar ke**, time limit ke andar. Hamara main score.

**Observation vector** — ek list of numbers jo ek drone ko dikhte hain: apni position,
velocity, target kahan hai, aas-paas ke drones, obstacle kitni door. Actor ka input.

**Off-policy / On-policy** — On-policy (PPO/MAPPO): sirf abhi ki policy se collect kiya
data use karo. Off-policy (DQN): purana data bhi replay buffer se use karo. IGAT-MARL
off-policy hai, hum on-policy.

**PAH (Priority Arbitration Head)** — hamara naya chhota network. Input: 3 numbers
(takkar mein kitni der hai, target kitna door, kitne drones kareeb). Output: α.
Thesis ka novel contribution.

**PPO (Proximal Policy Optimization)** — ek popular, stable RL algorithm. "Policy ko ek
baar mein zyada mat badlo" — isi rule se stability aati hai (clipping).

**Point-mass model** — drone ko ek **bindu (dot)** maan lena jiski sirf position aur
velocity hai — koi size, weight, tilt nahi. 2D research ke liye kaafi.

**Policy (π)** — drone ka "rulebook": is situation mein kya karna hai. Neural network
ke andar seekha hua hota hai.

**PyBullet** — 3D physics engine (gravity, weight, wind). Synopsis mein likha tha lekin
2D research ke liye zaroorat nahi — hum custom simple env banayenge.

**Reward** — har step pe environment jo number deta hai: "ye achha tha (+)" ya "bura
tha (−)". RL isi ko maximize karne ki koshish karta hai.

**Reward hacking** — jab agent reward ko "cheat" karke badhaata hai, actually achha
behave kiye bina. PAH mein risk hai kyunki agent khud α choose karta hai jo uska reward
banata hai. `research/01_pah_design.md` mein poora explained.

**Reward shaping** — reward ko aise design karna ki seekhna aasaan ho (jaise har chhota
progress reward karna, sirf end pe nahi).

**Rollout / rollout buffer** — training ke liye kuch episodes chala ke experience
(observation, action, reward) ko ek buffer mein jama karna, phir usse seekhna.

**Seed** — random number generator ka starting point. Same seed = same random cheezein =
experiment repeat ho sakta hai. Hum har run ka seed fix karte hain.

**Target assignment** — kaun sa drone kaun sa target lega, ye decide karna.
(Hungarian algorithm se karte hain.)

**TensorBoard** — training ke graphs (reward badh raha hai ya nahi, etc.) dekhne ka
free tool.

**Time-to-collision (τ_collision)** — "abhi jaise chal raha hoon, kitni der mein kisi se
takraaonga". PAH ka pehla input. Chhota number = khatra kareeb.

**Vectorized environment** — ek saath 32-64 copies of environment parallel chalana,
taaki data jaldi jama ho. Hamare case mein GPU se zyada isse speed aati hai.
