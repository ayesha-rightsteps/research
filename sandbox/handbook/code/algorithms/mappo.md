# Handbook — mappo.py

## Yeh file kia hai?
MAPPO — **Multi-Agent Proximal Policy Optimization** — drones ka **AI brain**.
Yeh file 4 cheezein define karti hai:

1. **Actor** — drone decide karta hai: kahan jauN?
2. **Critic** — judge karta hai: yeh situation achi thi ya buri?
3. **RolloutBuffer** — experience store karta hai
4. **MAPPO** — sab milake training karta hai

## Real life mein soch ke samjhein

Sochiye aap tennis seekh rahi hain:
- **Actor** = aapka haath jo racket marta hai (decision maker)
- **Critic** = coach jo kehta hai "yeh shot acha tha, woh bura" (evaluator)
- **RolloutBuffer** = notebook jis mein coach aapke sab shots note karta hai
- **Training loop** = coach ki notes dekh ke haath improve karna

Drones bhi yahi karte hain — baar baar play karte hain, coach evaluate karta hai, phir improve karte hain.

## Andar kia kia hai?

### Actor network
- Input: **ek drone ki observation** (10 numbers)
- 2 hidden layers (64 neurons each)
- Output: **action** — kahan jauN (vx, vy)
- Gaussian distribution use karta hai — matlab thoda randomness bhi hota hai (exploration)

### Critic network
- Input: **saare drones ki observations ek saath** (3×10 = 30 numbers)
- 2 hidden layers (64 neurons each)
- Output: **ek number** — yeh situation kitni achi hai?
- Centralized = training mein sab drones ki info dekh sakta hai

**Update (2026-09-17) — ab Stage 2+ mein DO critics hain, ek nahi:**
Stage 1 mein (PAH off) abhi bhi ek hi critic hai, pehle jaisa. Lekin Stage 2+
mein (PAH on) ab **do alag critics** hain — `critic_m` (mission ke liye) aur
`critic_s` (safety ke liye), har ek apna reward alag se seekhta hai. Pehle
dono ek hi critic share karte the — check karne pe pata chala ki ye sharing
kabhi-kabhi problem create kar rahi thi (α galat direction mein ja raha tha
kuch seeds mein, 5 mein se 2 mein). Ab dono critics independent hain, is
problem ko root se fix karne ke liye.

### RolloutBuffer
- Training ke dauran experience store karta hai
- `use_pah=True` hoga toh **extra cheezein bhi store karta hai:**
  - `r_mission` — mission reward (alag)
  - `r_safety` — safety reward (alag)
  - `pah_tau`, `pah_d`, `pah_n` — PAH ke teen inputs
- Phir **GAE** calculate karta hai:
  > GAE = "yeh action expected se kitna better/worse tha?"
  > Isko **advantage** kehte hain

### MAPPO.get_actions()
- Jab environment mein khelna ho → actor se action lo
- M3 GPU (MPS) use karta hai — fast!

### MAPPO.update()
- Buffer dekhein → advantages calculate karein → networks update karein
- **PPO clip:** update itna bada mat karein ke policy bigad jaye
- **Entropy bonus:** thodi randomness rakhein — nahi toh drone ek hi cheez karta rahega
- **Gradient clipping:** ek bada update sab kuch barbaad kar sakta hai — roko
- **PAH loss (jab PAH ON ho) — Option B, two-head critic (2026-09-17):**
  1. *Component advantages:* `A_mission` aur `A_safety` alag alag compute hote hain (GAE), **ab apna-apna critic baseline use karte hain** (`critic_m`, `critic_s` — pehle ek hi shared critic tha). PAH ka α inhe weight karta hai: `w_adv = α·A_mission + (1−α)·A_safety`. Isi weighted advantage pe PPO clip loss lagti hai. Gradient naturally α ke through jaata hai — koi hand-crafted formula nahi, seedha experience se seekhta hai.
  2. *Do value losses:* `critic_m` aur `critic_s` dono apna-apna loss compute karte hain, dono add hoke total critic loss banta hai
  3. *Prior loss:* alpha ko τ (danger ka signal) ke hisaab se target ki taraf kheenchti hai — danger mein low, safe mein high. Danger-close samples ko zyada weight milti hai (pehle sirf 0.5 ke paas kheenchta tha, jo direction nahi batata tha)

### MAPPO — PAH ke saath ya bina

```
Stage 1:  MAPPO(pah_wrapper=None)   → fixed α=0.5, sab same
Stage 2+: MAPPO(pah_wrapper=...)    → learned α, PAH bhi update hota hai
```

PAH aur actor/critic ek hi optimizer mein hain — ek saath seekhte hain.

### save() / load()
- Stage 1: file mein `actor` aur `critic` weights save hote hain
- Stage 2+ (PAH on): `critic_m`, `critic_s`, aur `pah` weights save hote hain
  (`critic` ki jagah do alag critics)
- Checkpoint keys: Stage 1 → `['actor', 'critic']`, Stage 2+ → `['actor', 'critic_m', 'critic_s', 'pah']`
- **`load_actor_only()`** — naya method, sirf actor load karta hai (warm-start
  ke liye, jaise Stage 2b se Stage 2 mein). Dono critics aur PAH hamesha fresh
  shuru hote hain — purana checkpoint ka `critic` key naye `critic_m`/`critic_s`
  pe fit nahi baithta

## Numbers (sanity test se)
- Actor: **4,996 parameters** (chota network — intentional)
- Critic: **6,209 parameters**
- PAH: **~130 parameters** (bahut chota — thesis mein "lightweight" yahi matlab)
- Device: **MPS** (aapka M3 GPU — fast training!)

## Hard words
- **PPO (Proximal Policy Optimization):** policy update ka safe tarika — chote chote steps
- **GAE (Generalized Advantage Estimation):** "yeh action kitna better tha expected se" calculate karna
- **Entropy:** randomness ka measure — zyada entropy = zyada explore karna
- **Gradient clipping:** neural network update ka size limit karna — stability ke liye
- **MPS:** Apple Silicon ka GPU — PyTorch is pe run kar sakta hai
- **Parameters:** neural network ke "knobs" jo training mein adjust hote hain
- **use_pah:** flag jo batata hai PAH ON hai ya nahi — Stage 1 mein False, Stage 2+ mein True
- **pah_wrapper:** woh object jo PAH ko environment se connect karta hai
