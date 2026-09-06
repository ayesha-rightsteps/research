# Samjho: docs/research/00_problem_formalization.md

## Yeh cheez kya hai
Problem ko maths ki bhaasha mein exactly likhna — drone ko kya dikhta hai, kya action
le sakta hai, reward kaise milta hai, episode kab khatam hota hai.

## Iski zaroorat kyun
Code likhne se pehle ye sab pakka hona chahiye. Warna aadha code likhne ke baad pata
chalega ki reward function to define hi nahi tha. Ye doc supervisor ko bhi dikhana hai.

## Main baatein

- **Duniya:** 2D square (jaise 100×100 ka field). Drone = ek dot jiski position aur
  velocity hai (koi size/weight/tilt nahi — "point-mass"). N drones, N targets
  (har drone ka ek), kuch round obstacles.

- **Observation (drone ko kya dikhta hai) — total ~31 numbers:**
  - apni position + velocity (4)
  - assigned target kahan hai + kitna door (3)
  - 4 sabse kareeb "conflict" drones ki relative position + velocity + ek mask bit
    (5 × 4 = 20) — agar 4 se kam hain to zero se bhar do
  - 4 directions mein obstacle kitna door (4)

- **Action:** `(ux, uy)` — kis direction mein aur kitni speed se jaana. Do numbers,
  −1 se 1 ke beech, phir `v_max` se multiply.

- **Episode khatam kab:** sab target pe pahunch gaye (SUCCESS) / koi takra gaya /
  koi bahar nikal gaya / 600 steps ho gaye (TIMEOUT).

- **Reward do hisson mein:**
  - `r_mission` = target ke kareeb jaane ka reward + pahunchne ka bonus + har step
    thoda minus (jaldi karo) — **sirf mission wali cheezein**
  - `r_safety` = takkar pe bada minus + obstacle ke paas minus + "kareeb aa rahe ho"
    ka smooth minus — **sirf safety wali cheezein**
  - Final: `r = α·r_mission + (1−α)·r_safety`
  - Dono ko alag rakhna zaroori hai taaki α unke beech balance kar sake

- **Sabhi numbers (dt, v_max, d_col, etc.) ek table mein hain** — abhi "starting guess",
  P1 mein tune karenge.

- **Jo cheezein humne DA-MAPPO se hataayi (aur kyun theek hai):** 3D physics, LiDAR,
  communication model — ye sab thesis ke "assumptions" section mein likhenge.

## Mushkil lafz
- **Dec-POMDP** = multi-agent + har agent ko aadhi info wali problem ka formal naam
- **Point-mass** = drone ko sirf ek chalta hua bindu maanna
- **Observation vector** = drone ko dikhne wale numbers ki list
- **Mask bit** = 0/1 flag jo batata hai "ye slot khaali hai ya asli data"
- **Termination** = episode khatam hone ki condition
- **α (alpha)** = mission vs safety ka balance knob (0 se 1)
- Baaki `handbook/glossary.md` mein
