# Handbook — multi_uav_env.py

## Yeh file kia hai?
Tumhara **2D duniya** — jahan drones fly karte hain, targets hain, obstacles hain.
Yeh poori research ki neenv hai. Iske bina kuch nahi.

## Real life mein soch ke samjho
Soch lo ek top-down game — jaise GTA ka map upar se dekho. Us map pe:
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
Phir **Hungarian algorithm** chalao: decide karo kaun sa drone kaun sa target lay.

### `step(actions)` — Ek time step aagay badhata hai
- Drones ko move karo (actions apply karo)
- Check karo: koi takraya? koi target pahuncha?
- Reward calculate karo
- Observation return karo

### `_get_obs()` — Har drone ko information deta hai
Har drone ko **10 numbers** milte hain:

| Number | Matlab |
|--------|--------|
| 1, 2 | Apni position (x, y) |
| 3, 4 | Apni speed (vx, vy) |
| 5, 6 | Target kitna door hai aur kahan (relative) |
| 7, 8, 9, 10 | North/South/East/West mein obstacle kitna door hai |

### `_hungarian_assignment()` — Targets assign karta hai
"Kaun sa drone kaun sa target lay?" — yeh math se optimal decide hota hai.
SciPy library ka `linear_sum_assignment` use hota hai — ek line ka code!

### `_compute_rewards()` — Reward calculate karta hai
Yeh function **teen cheezein return karta hai** (pehle sirf ek thi):

```
reward    = 0.5 × r_mission + 0.5 × r_safety   (default jab PAH nahi)
r_mission = target se distance (negative number)
r_safety  = collision hua? -1, nahi toh 0
```

Dono components alag kyun? Kyunki **PAH ko dono alag chahiye** taake woh apna α apply kare. Train ke waqt PAH ek alag formula use karta hai:
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
