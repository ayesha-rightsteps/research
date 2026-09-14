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
- World kitni badi? (default: 100×100)
- Max speed kitni? (default: 5)
- Max steps kitne? (default: 300)

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
reward    = 0.5 × r_mission + 0.5 × r_safety   (default jab PAH nahi)
r_mission = target se distance (negative number)
r_safety  = graded proximity penalty (neeche explain hai)
```

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
