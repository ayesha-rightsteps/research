# Samjho: docs/research/02_assignment_and_conflict.md

## Yeh cheez kya hai
Do mechanism ka detail: (1) Hungarian algorithm — kaun sa drone kaun sa target le,
(2) Conflict graph — kaunse drones takrane wale hain.

## Iski zaroorat kyun
Ye dono har step pe chalte hain aur inka output drone ki observation aur PAH ke input
mein jaata hai. Detail galat hui to sab galat.

## Main baatein

### Hungarian (target assignment)
- **Cost matrix banao:** har drone-target jodi ki doori ka square. `C[i][j] = doori²`
- **Solve:** `scipy.optimize.linear_sum_assignment(C)` — ek line. Ye optimal matching
  deta hai (total doori sabse kam).
- **Thrashing problem:** agar do targets ek drone se lagbhag barabar door hain, to
  assignment har step flip ho sakta hai → drone confuse, aage-peeche.
- **Bachav ke options (preference order):**
  1. Pehle kuch mat karo (DA-MAPPO ne aisa hi kiya) — bas "reassignments per episode"
     count karo
  2. Switching cost — assignment badalne pe thoda penalty cost matrix mein
  3. Hysteresis — naya assignment tabhi lo jab wo margin se behtar ho
  4. Har 50 step pe assign karo (DA-MAPPO: sirf 3-5% loss)

### Conflict graph
- **Idea:** har drone ko har doosre se mat jodo. Sirf un jodiyon ko jodo jinki
  **aane wale kuch second mein takkar** ho sakti hai. Drones zyada ho to bhi graph
  chhota rehta hai.
- **CPA maths (theek se karo):** relative position `p` aur relative velocity `v` se —
  sabse kareeb aane ka time `t* = −(p·v)/(v·v)`, usko 0 se H ke beech clip karo.
  Us waqt ki doori `DCPA = |p + v·t*|`. Agar `DCPA < d_danger` aur `t*` future mein hai
  → edge banao.
- ⚠️ Guide sirf `t = H` pe doori check karta hai — wo galat hai (jo pehle kareeb aa ke
  door ho jaate hain wo miss ho jaate). Upar wala formula use karo.
- **Adjacency matrix `A`:** `A[i][j] = 1` agar edge hai. Symmetric, diagonal 0.
- **`n_conflict`** = ek drone ke kitne edges (PAH input).
- **`τ_collision`** = us drone ke edges mein sabse chhota `t*` (sabse kareeb khatra).
  Koi edge nahi → `τ = H` (safe).
- **Observation mein neighbors:** conflict neighbors ko `t*` ke order mein sort karo,
  pehle 4 lo, zero se pad karo.

## Mushkil lafz
- **Cost matrix** = table jismein har (drone, target) jodi ki "keemat" (doori)
- **Optimal matching** = sabse achhi possible jodi-banai
- **Thrashing** = baar-baar switch hota rehna, kaam na banna
- **Hysteresis** = "badalne mein sust" — chhote change pe switch mat karo
- **CPA (Closest Point of Approach)** = do drones sabse kareeb kab aur kitna aayenge
- **DCPA** = us sabse-kareeb waqt ki doori; **TCPA / t\*** = wo waqt
- **Adjacency matrix** = graph ko table (0/1) ki form mein likhna
- **Edge** = graph mein do points ke beech ka connection
