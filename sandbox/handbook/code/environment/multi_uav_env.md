# Handbook — multi_uav_env.py

## Yeh file kia hai?
Aapka **2D duniya** — jahan drones fly karte hain, targets hain, obstacles hain.
Yeh poori research ki neenv hai. Iske bina kuch nahi.

## Real life mein soch ke samjhein
Sochiye ek top-down game — jaise GTA ka map upar se dekhein. Us map pe:
- 🚁 **Drones** hain jo move kar rahe hain
- ⭐ **Targets** hain jahan drones ko pahunchna hai
- ⬛ **Obstacles** hain jo raaste mein hain

Drones ko seekhna hai — bina kisi se takray — apne apne target tak pahunchna.

## Andar kia kia hai?

### `__init__` — Environment banata hai
Sab settings yahan set hoti hain:
- Kitne drones? (default: 3)
- Kitne obstacles? (default: 3)
- World kitni badi? (default: 100×100 — Stage 1 config mein 500×500 use hota hai)
- Max speed kitni? (default: 5)
- Max steps kitne? (default: 300)
- `success_bonus` (default 0.0) — target pe pahunchne pe ek baar ka bada +reward (2026-09-15 add)
- `use_hungarian` (default True) — False karo to target assignment reset pe fix ho jaata hai, kabhi badalta nahi (ablation ke liye, dekho `code/notebooks/v3/ablation/`)

### `reset()` — Naya episode shuru karta hai
Jab bhi naya game shuru ho — drones, targets, obstacles sab random jagah rakh do.
Phir **Hungarian algorithm** chalayein: decide karein kaun sa drone kaun sa target lay.

### `step(actions)` — Ek time step aagay badhata hai
- Drones ko move karein (actions apply karein)
- Check karein: koi takraya? koi target pahuncha?
- Reward calculate karein
- Observation return karein

### `_get_obs()` — Har drone ko information deta hai
Har drone ko **10 numbers** milte hain — sab **normalize** hain (0 se 1 ke beech):

| Number | Matlab | Range |
|--------|--------|-------|
| 1, 2 | Apni position (x, y) — world size se divide | [0, 1] |
| 3, 4 | Apni speed (vx, vy) — max speed se divide | [-1, 1] |
| 5, 6 | Target kahan hai (relative) — world size se divide | [-1, 1] |
| 7, 8, 9, 10 | North/South/East/West mein obstacle kitna door | [0, 1] |

**Normalize kyun?** Taake world 100m ho ya 500m ya 1km — numbers hamesha same range mein rahein. Neural network chhote numbers pe zyada achay seekhta hai, aur world size change karne pe dobara train nahi karni padegi.

### `_hungarian_assignment()` — Targets assign karta hai
"Kaun sa drone kaun sa target lay?" — yeh math se optimal decide hota hai.
SciPy library ka `linear_sum_assignment` use hota hai — ek line ka code!

### `_compute_rewards()` — Reward calculate karta hai
Yeh function **teen cheezein return karta hai** (pehle sirf ek thi):

```
r_progress = velocity target ki taraf hai kitna (-1 se +1)   [2026-09-15 add]
r_dist     = -distance/world_size (negative number)
r_mission  = 0.4 × r_progress + 0.3 × r_dist
r_safety   = graded proximity penalty (neeche explain hai)

reward = r_mission + 0.3 × r_safety                     (default jab PAH nahi)
reward += success_bonus  jab sab drones target pe pahunch jaayein
```

**`r_progress` aur `success_bonus` kyun add kiye?** Pehle sirf `r_dist` tha —
Stage 1 3000+ episodes tak 0% success raha, kyunki policy ko sirf "kitna door
hoon" pata chalta tha, "sahi direction mein ja raha hoon" ka koi seedha signal
nahi tha. Details: `sessions/2026-09-15.md` Parts 1-2.

**r_safety graded kyun hai?**
Pehle sirf collision pe -1 milta tha — lekin tab tak bohot der ho jaati hai.
Ab drone ke paas aate hi signal milna shuru ho jaata hai:

| Distance | r_safety |
|----------|----------|
| < 3m (collision!) | -1.0 (hard) |
| 3m se 9m ke beech (danger zone) | -0.33 se -1.0 (graded) |
| > 9m (clear) | 0.0 |

Yeh PAH ko pehle se signal deta hai — collision se pehle hi α adjust ho jaata hai.

PAH train ke waqt:
```
reward = α × r_mission + (1-α) × r_safety
```
Jahan α PAH ka seekha hua number hota hai (0.1 se 0.9 ke beech).

### `step()` — ab info dict mein zyada cheezein hain

Har step ke baad environment yeh extra information deta hai:

| Key | Kya hai |
|-----|---------|
| `r_mission` | Sirf mission ka reward (array, har drone ke liye alag) |
| `r_safety` | Sirf safety ka reward (array, har drone ke liye alag) |
| `pah_inputs` | PAH ke teen inputs — sirf tab jab conflict graph ON ho |

`pah_inputs` ke andar:

| Key | Matlab |
|-----|--------|
| `tau` | Har drone ke liye: takkar kab hogi? (seconds mein) |
| `d_target` | Har drone ke liye: target se distance (units) |
| `n_conflict` | Har drone ke liye: kitne drones se danger hai |

### Collision checks
- **Drone vs Drone:** do drones 3 units se paas aayein toh collision
- **Drone vs Obstacle:** drone obstacle ke 3 units mein aaye toh collision
- **Boundary:** drone world ke bahar nahi ja sakta (clip hota hai)

### `_place_obstacles_poisson()` — Obstacles kahan rakhein (2026-09-15 add)
Pehle obstacles bilkul random jagah rakhe jaate the — kabhi-kabhi do obstacle
itne paas aa jaate ki beech mein se koi drone nikal hi nahi sakta tha. Ab
**Poisson disk sampling** use hota hai: har obstacle doosre obstacles se kam se
kam `2 × collision_radius` door, aur drones/targets se kam se kam
`collision_radius` door. 1000 baar try karta hai; agar jagah na mile to kam
obstacles rakh deta hai (crash nahi karta). Stage 1 mein `n_obstacles=0` hai to
abhi iska koi effect nahi — Stage 2+ ke liye zaroori hoga.
Detail: `docs/research/00_problem_formalization.md` Section 2.2.

## Hard words (Glossary mein bhi hain)
- **Gymnasium:** Python mein RL environment banane ka standard tarika — jaise ek blueprint
- **Observation:** jo information drone ko milti hai — uski "aankhein"
- **Action:** drone kia kare — yahan `(vx, vy)` matlab x aur y direction mein speed
- **Reward:** drone ko kitna mila is step mein — positive = acha, negative = bura
- **Episode:** ek complete game — reset se lekar done tak
- **Hungarian algorithm:** targets assign karne ka optimal mathematical method
- **α (alpha):** weight — kitna mission important, kitna safety important

## Is file ko kab touch karein?
- Agar observation mein kuch add karna ho (jaise conflict neighbors — P3 mein)
- Agar reward formula badalna ho
- Agar environment ki koi setting badalni ho
