# Samjhein: docs/research/00_problem_formalization.md

## Yeh cheez kya hai
Problem ko maths ki bhaasha mein exactly likhna — drone ko kya dikhta hai, kya action
le sakta hai, reward kaise milta hai, episode kab khatam hota hai.

## Iski zaroorat kyun
Code likhne se pehle ye sab pakka hona chahiye. Warna aadha code likhne ke baad pata
chalega ki reward function to define hi nahi tha. Ye doc supervisor ko bhi dikhana hai.

## Main baatein

- **Duniya:** 2D square — **500m × 500m** (1 unit = 1 metre). Half-kilometre ka area —
  jaise ek chhota campus, industrial site, ya search-and-rescue zone. Yeh scale real UAV
  missions se milta hai aur supervisor ko bhi credible lagega.
  Drone = ek dot jiski position aur velocity hai (koi size/weight/tilt nahi —
  "point-mass"). N drones, N targets (har drone ka ek), kuch round obstacles.

- **Drones kitne — aur kyun yeh numbers:**
  | Stage | Drones | Kyun |
  |-------|--------|------|
  | 1 | 3 | Minimum jab multi-agent interaction meaningful ho — DA-MAPPO baseline |
  | 2 | 5 | Conflict graph dense hone lagta hai — PAH ka kaam shuru hota hai |
  | 3 | 8 | Stress test — kitne drones tak system kaam karta hai? |

- **Obstacles kahan rakhein — Poisson Disk Sampling:**
  Pure random placement se obstacles ek doosre ke upar aa sakte hain ya raasta band ho
  sakta hai. Isliye **Poisson disk sampling** use karte hain:
  > "Obstacles randomly rakhein, lekin koi bhi do obstacles 6 metre se paas nahi honge"
  
  Yeh guarantee karta hai ke drones ke liye hamesha raasta milega.

- **Physical scale table:**
  | Cheez | Number | Real meaning |
  |-------|--------|--------------|
  | World size | 500 u | 500 metre × 500 metre |
  | Max speed | 5 u/s | 5 m/s — slow safe UAV |
  | Collision radius | 2 u | 2 metre separation |
  | Target radius | 5 u | 5 metre GPS accuracy margin |
  | One step | dt=0.1s | 100ms control loop |
  | Max episode | 300 steps | 30 seconds |

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
    thoda minus (jaldi karein) — **sirf mission wali cheezein**
  - `r_safety` = takkar pe bada minus + obstacle ke paas minus + "kareeb aa rahe hain"
    ka smooth minus — **sirf safety wali cheezein**
  - Final: `r = α·r_mission + (1−α)·r_safety`
  - Dono ko alag rakhna zaroori hai taaki α unke beech balance kar sake

- **Sabhi numbers (dt, v_max, d_col, etc.) ek table mein hain** — abhi "starting guess",
  P1 mein tune karenge.

- **Jo cheezein humne DA-MAPPO se hataayi (aur kyun theek hai):** 3D physics, LiDAR,
  communication model — ye sab thesis ke "assumptions" section mein likhenge.

- **Centralized Critic kahan chalta hai — CTDE ka matlab:**

  Training aur deployment mein fark hai:

  | Phase | Critic | Actor |
  |-------|--------|-------|
  | **Training** (Kaggle/server pe) | ✅ Ground station pe — saare N drones ki observations ek saath dekhta hai | ✅ Server pe |
  | **Deployment** (actual flight) | ❌ NAHI chalta — zaroorat hi nahi | ✅ Har drone apna actor khud chalaata hai |

  Yeh CTDE hai: Centralized Training, Decentralized Execution.

  Deployment mein har drone sirf **apna actor** chalaata hai — ~5,000 parameters, kisi
  bhi chhote processor pe chal sakta hai. Critic sirf training ke liye tha taake better
  learning ho sake — missions mein nahi chahiye.

  **Channel assumption:** Training ke waqt ground station ko saare drones ki info
  chahiye (clear channel assume). Deployment mein sirf thodi position broadcast (< 10
  bytes per drone) — lamba range channel nahi chahiye.

## Mushkil lafz
- **Dec-POMDP** = multi-agent + har agent ko aadhi info wali problem ka formal naam
- **Point-mass** = drone ko sirf ek chalta hua bindu maanna
- **Observation vector** = drone ko dikhne wale numbers ki list
- **Mask bit** = 0/1 flag jo batata hai "ye slot khaali hai ya asli data"
- **Termination** = episode khatam hone ki condition
- **α (alpha)** = mission vs safety ka balance knob (0 se 1)
- Baaki `handbook/glossary.md` mein
