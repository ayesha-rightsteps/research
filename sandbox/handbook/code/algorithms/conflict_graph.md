# Handbook — conflict_graph.py

## Yeh file kia hai?
Conflict graph — yeh detect karta hai ke **kaun se drones aapas mein takrarne wale hain.**

Har drone ko har doosre drone se connect nahi karte (woh costly aur noisy hota) — sirf
**khatarnak pairs** ko connect karte hain. Isliye "sparse" graph kehte hain.

## Real life mein soch ke samjhein
Sochiye highway pe gaadiyan chal rahi hain. Traffic police sirf unhi gaadiyon ko watch
karti hai jo ek dusre ki taraf ja rahi hain — baaki sab ignore. Yahi conflict graph karta hai.

## Andar kia kia hai?

### CPA Math — "Kab aur kitna paas aayenge?"

Do drones ke liye:
- **t*** = woh waqt jab dono sabse zyada paas honge
- **DCPA** = us waqt unke beech ki distance

```
Agar DCPA < danger_threshold  AND  0 ≤ t* ≤ H (future mein)
    → Edge add karein (yeh dono khatarnak hain!)
```

### ConflictGraph class

**`update(drone_pos, drone_vel)`** — har step pe call hota hai
- Saare drone pairs check karein
- Graph rebuild karein

**`n_conflict(i)`** — drone i ke kitne conflict neighbors hain → PAH input 3

**`tau_collision(i)`** — drone i ki sabse jaldi aane wali takkar kab hai → PAH input 1
- Agar koi danger nahi: horizon (3.0) return karta hai = "safe"

**`neighbor_obs(i, ...)`** — drone i ke liye fixed-size observation banata hai
- K_NBR = 4 slots (fixed hamesha)
- Har slot: [rel_pos_x, rel_pos_y, rel_vel_x, rel_vel_y, mask]
- Agar kam neighbors hain: baaki slots zeros se pad

## Observation mein kia add hota hai?

```
Pehle (Stage 1):  obs = 10 numbers per drone
Ab (Stage 2+):    obs = 10 + 4×5 = 30 numbers per drone
                        ↑        ↑
                     base    4 conflict neighbor slots
```

## Parameters
| Parameter | Value | Matlab |
|-----------|-------|--------|
| horizon H | 3.0 | 3 steps aage dekhein |
| d_danger | collision_radius × 3 | itni distance pe "danger" |
| K_NBR | 4 | max 4 neighbors observation mein |

## Hard words
- **CPA (Closest Point of Approach):** do moving objects ke beech minimum future distance
- **Sparse graph:** sirf zaroori connections — density kam, efficiency zyada
- **t* (t-star):** time of closest approach — kab sabse zyada paas honge
- **DCPA:** distance at closest point of approach — kitna paas aayenge
- **Mask:** 1 = yeh slot mein actual neighbor hai, 0 = empty/padded slot
- **PAH input:** Priority Arbitration Head ko yeh numbers milte hain alpha decide karne ke liye
