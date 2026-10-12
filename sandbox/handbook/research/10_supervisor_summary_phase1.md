# Handbook — 10_supervisor_summary_phase1.md

Asal file: `docs/research/10_supervisor_summary_phase1.md`

## Yeh kya hai?

Supervisor ke liye **ek page ka summary** (English mein): ab tak kya mila, kyun design badalna chahiye, aur
kis cheez ki ijazat chahiye. Meeting mein yahi dikhana hai.

## Ismein kya hai (simple mein)

1. **Abhi ke results:** teeno methods (Fixed-weight MAPPO, Hand-coded τ-rule MAPPO, MAPPO + PAH) ~88–90%
   pe barabar; Hungarian hataane se 8 drones pe success 51.5% tak girti hai.
2. **Diagnostics ne kya dikhaya:** takkar obstacles se hoti hai; PAH obstacles nahi dekh sakta; α learning
   ko bahut kam badalta hai (is liye tie); obstacle sensing kamzor hai.
3. **Base paper se seedha comparison kyun nahi:** unka problem alag hai (3 drones, 30–50 obstacles).
4. **4 badlav jinki ijazat chahiye:** mission/safety ke alag value heads; PAH ko obstacle ka khatra;
   LiDAR jaisi sensing; asli size ke ghane obstacles.
5. **Time:** laptop pe training tez hai, ~2–3 hafte.
6. **Supervisor se 3 sawal:** kya badlav theek hain (khaas taur pe PAH ke inputs badalna, kyunki synopsis
   mein 3 inputs likhe hain); kaun se base-paper baselines chahiye; kya abhi ke results "pehla stage" ke
   taur pe report kar sakte hain.

## Dhyan rahe

Badlav number 2 (PAH ko obstacle ka khatra dena) **thesis ke core** ko chhoota hai — synopsis mein PAH ke
3 inputs fixed likhe hain. Is liye iski ijazat sab se zaroori hai.
