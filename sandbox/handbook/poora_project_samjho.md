# Poora Project — Shuru Se Abhi Tak
### Ayesha ke liye: ek dum simple, ek dum detail mein

---

> **Yeh file kya hai?**
> Is file mein poora project start se end tak explain kiya gaya hai.
> Har cheez ka matlab, har cheez ka kisi doosri cheez se kya connection hai.
> Isko parhne ke baad tumhe poori picture mil jaayegi.

---

## SECTION 1 — Pehle yeh samjho: Hum kya bana rahe hain?

### Problem kya hai?

Soch lo teen drones hain. Inhe teen jagahon pe pahunchna hai — bina aapas mein takraye, bina obstacles se takraye.

Yeh simple lagta hai, lekin mushkil yeh hai:
- **Kaun sa drone kaun si jagah le?** (Target Assignment problem)
- **Raaste mein ek doosre se kaise bachein?** (Collision Avoidance problem)

Purane papers yeh dono alag alag solve karte the. Result? Dono parts conflict karte the — ek system drone ko target ki taraf bhejta tha, doosra system brakes lagata tha. Overlap aur slow mission.

**Hum kya kar rahe hain:** Dono problems ek saath solve karo, ek hi AI brain se.

---

### Hamara solution kya hai?

```
┌─────────────────────────────────────────────────────────────┐
│                      HAMARA SYSTEM                          │
│                                                             │
│   Drone ki situation dekho                                  │
│         ↓                                                   │
│   PAH decide karta hai: "Abhi mission important hai        │
│   ya safety?" → Alpha (α) number                           │
│         ↓                                                   │
│   MAPPO (AI brain) decide karta hai: Kahan jauN?           │
│         ↓                                                   │
│   Hungarian Algorithm: Kaun sa drone kaun sa target le?    │
│         ↓                                                   │
│   Conflict Graph: Koi takkar hone wali hai?                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

### Thesis ka main claim (novel contribution)

Purane papers mein α (alpha) hamesha **fixed** hota tha — jaise 0.5.

Matlab: chahe drone bilkul safe ho ya takkar ke ek second pahle — formula same:
```
reward = 0.5 × mission_reward + 0.5 × safety_reward
```

**Hamara claim:** Alpha ko situation dekh ke automatically adjust hona chahiye.

```
Drone safe hai, target door hai  →  α = 0.8  →  mission pe focus
Drone takkar ke qareeb hai        →  α = 0.2  →  safety pe focus
```

Yeh kaam karta hai **PAH** — Priority Arbitration Head. Yahi thesis ka novel contribution hai.

---

## SECTION 2 — Building Block 1: Environment (Duniya banana)

**File:** `code/environment/multi_uav_env.py`

### Yeh kya hai?

Drones ko sikhane ke liye pehle ek "duniya" chahiye jahan woh khelein.

Soch lo ek video game map — upar se dekho:
- Drones upar se dikhte hain (top-down view)
- World 100×100 units ka square hai
- Drones move karte hain, targets hain, obstacles hain

Yeh duniya Python mein bani hai — real physics nahi (simple 2D), lekin thesis ke liye kaafi hai.

### Environment kaise kaam karta hai?

Har "step" mein yeh hota hai:

```
1. Hum drone ko action dete hain: (vx, vy) — x aur y direction mein speed
2. Drone move karta hai
3. Environment check karta hai:
   - Koi takraya? → Reward -1
   - Koi target pahuncha? → Reward positive
4. Environment observation return karta hai
5. AI observation dekh ke agle action decide karta hai
6. Repeat...
```

### Observation kya hoti hai?

Har drone ko 10 numbers milte hain (Stage 1 mein):

```
[x, y, vx, vy, rel_tx, rel_ty, clear_N, clear_S, clear_E, clear_W]
 ↑   ↑   ↑    ↑    ↑      ↑       ↑         ↑        ↑       ↑
 apni     apni   target  target  North    South    East    West
position  speed   ka      ka     mein     mein     mein    mein
          (vel)   x       y     door     door     door    door
                 diff    diff
```

Stage 2 mein 20 aur numbers add hote hain (conflict neighbors ke baare mein).

### Reward kya hoti hai?

Reward = drone ko "feedback" — acha kiya ya bura?

```python
r_mission = -distance_to_target / world_size   # jitna door, utna negative
r_safety  = -1.0  agar collision hua, warna 0.0

# Combine (PAH ke bina):
reward = 0.5 × r_mission + 0.5 × r_safety

# Combine (PAH ke saath):
reward = α × r_mission + (1-α) × r_safety
```

### Hungarian Assignment kya hai? (Environment ke andar hota hai)

Yeh decide karta hai: **Kaun sa drone kaun sa target le?**

```
3 drones hain: D1, D2, D3
3 targets hain: T1, T2, T3

Cost matrix (distances):
        T1    T2    T3
D1  [  20,   80,   60  ]
D2  [  70,   30,   50  ]
D3  [  40,   60,   10  ]

Hungarian Algorithm: minimize karo total distance
Result: D1→T1, D2→T2, D3→T3  (total = 20+30+10 = 60)
```

Yeh har step pe run hota hai — targets reassign hote hain dynamically.

---

## SECTION 3 — Building Block 2: MAPPO (AI Brain)

**File:** `code/algorithms/mappo.py`

### Yeh kya hai?

MAPPO = Multi-Agent Proximal Policy Optimization.

Yeh woh algorithm hai jo drones ko actually sikhata hai — kahan jaana chahiye, kaise bachna chahiye.

### Reinforcement Learning (RL) kya hota hai?

Pehle RL samjho — poori thesis isi pe based hai.

```
Soch lo tum ek nayi game seekh rahi ho:
  - Tum kuch karo (action)
  - Game tumhe points de (reward)
  - Tum seekhti ho: woh action acha tha ya bura
  - Agli baar better action karo
  - Baar baar practice karo → expert ban jao
```

Yahi AI ke saath hota hai:
- AI ek action karta hai (drone ko kahan bhejo)
- Environment reward deta hai
- AI seekhta hai: woh action acha tha ya bura
- Update karo → better ho jao
- 3000 episodes practice → skilled drone!

### MAPPO ke 3 main parts

#### Part A: Actor Network

```
Actor = "Drone ka brain" — decide karta hai: kahan jauN?

Input:  Drone ki observation (10 ya 30 numbers)
           ↓
    Layer 1: 64 neurons, Tanh activation
           ↓
    Layer 2: 64 neurons, Tanh activation
           ↓
    Output: (vx, vy) — x aur y mein speed
```

**Shared weights:** Teeno drones ka ek hi actor hota hai. D1, D2, D3 — sab ek hi brain se action lete hain. Matlab: agar ek drone kuch seekhta hai, sab seekhte hain!

#### Part B: Critic Network

```
Critic = "Coach" — evaluate karta hai: situation achi thi ya buri?

Input:  SAARI drones ki observations ek saath (3×10 = 30 numbers)
           ↓
    Layer 1: 64 neurons, Tanh activation
           ↓
    Layer 2: 64 neurons, Tanh activation
           ↓
    Output: ek number (Value) — "yeh situation X points wali thi"
```

**Centralized critic:** Actor sirf apni observation dekhta hai (realistic — real drone bhi sirf apna sensor data dekhta hai). Lekin Critic training mein sab kuch dekh sakta hai — isse better evaluation milti hai.

#### Part C: RolloutBuffer

```
RolloutBuffer = "Coach ki notebook"

Har step pe store hota hai:
  - Observation (drone ne kya dekha)
  - Action (drone ne kya kiya)
  - Reward (kitna mila)
  - Value (critic ne kitna estimate kiya)
  - Log probability (is action ke chances kitne the)
  - Done (episode khatam hua ya nahi)

  + Jab PAH ON ho:
  - r_mission (sirf mission reward)
  - r_safety  (sirf safety reward)
  - pah_tau   (collision time)
  - pah_d     (target distance)
  - pah_n     (conflict neighbors count)
```

512 steps store hote hain — phir ek update hota hai.

### GAE (Generalized Advantage Estimation) — Advantage kya hota hai?

Yeh samajhna zaroor hai:

```
"Advantage" = "Yeh action expected se kitna BETTER ya WORSE tha?"

Positive advantage → yeh action expected se better tha → is action ki probability badhao
Negative advantage → yeh action expected se worse tha  → is action ki probability ghatao
```

GAE formula:
```
delta(t) = reward(t) + γ × Value(t+1) - Value(t)
              ↑                ↑              ↑
        jo mila      future kitna    ab kitna
                      worth hai      estimate tha

Advantage(t) = delta(t) + γλ × delta(t+1) + (γλ)² × delta(t+2) + ...
```

γ (gamma) = 0.99 — future rewards ka weight
λ (lambda) = 0.95 — advantage estimate ka smoothing

### PPO Update — Network kaise seekhta hai?

```
Purana policy (rollout ke waqt): π_old
Naya policy (update ke waqt):    π_new

Ratio = π_new(action) / π_old(action)
      = "Naye network ne is action ki kitni probability di
         vs. purane network ne"

PPO Loss = -min(ratio × advantage,
                clip(ratio, 0.8, 1.2) × advantage)
```

**Clip kyun?** Agar ratio bahut bada ho jaaye (matlab policy bahut badal gayi), training unstable ho jaati hai. Clip = "ek step mein itna hi badlo."

### Complete Update Step

```
1. GAE calculate karo (advantages, returns)
2. Mini-batches banao (64 samples each)
3. Har mini-batch ke liye:
   a. Actor se naye log_probs lo
   b. PPO clipped loss calculate karo
   c. Critic loss (value prediction kitni galat)
   d. Entropy bonus (randomness encourage karo)
   e. PAH loss (agar PAH ON ho)
   f. Total loss = actor + critic + entropy + pah
   g. Gradient calculate karo
   h. Gradient clip karo (max 0.5)
   i. Optimizer step (Adam) — weights update!
4. Buffer clear karo
```

---

## SECTION 4 — Building Block 3: Conflict Graph

**File:** `code/algorithms/conflict_graph.py`

### Yeh kya hai?

Conflict Graph detect karta hai: **Kaun se drones aapas mein takrarne wale hain?**

### CPA Math (Closest Point of Approach)

Do drones move kar rahe hain. Kabhi takraayenge?

```
Drone A position: pA, velocity: vA
Drone B position: pB, velocity: vB

Relative position: p = pA - pB
Relative velocity: v = vA - vB

t* = -(p · v) / (v · v)    ← yeh woh waqt hai jab dono sabse paas honge

DCPA = || p + v × t*_clamped ||   ← us waqt unke beech ki distance

Agar DCPA < danger_threshold  AND  0 ≤ t* ≤ horizon:
    → Yeh dono takraa sakte hain! → Edge add karo graph mein
```

### Graph kya hota hai?

```
3 drones: D1, D2, D3

Suppose D1 aur D2 collision course pe hain:

    D1 ——— D2      D3

Is graph mein ek edge hai D1-D2 ke beech.
D3 safe hai — koi edge nahi.

D1 ke liye: n_conflict = 1 (ek neighbor)
D2 ke liye: n_conflict = 1 (ek neighbor)
D3 ke liye: n_conflict = 0 (koi neighbor nahi)
```

### PAH ko kya milta hai conflict graph se?

```
tau_collision(i) = drone i ke liye: sabse pehli takkar kab hogi?
                   Agar safe hai → horizon (3.0) return karo = "bohat waqt hai"
                   Agar danger hai → woh time return karo = "jaldi aao"

n_conflict(i)    = drone i ke kitne "danger neighbors" hain
```

### Observation mein kya add hota hai?

```
Stage 1:  obs = 10 numbers (base only)
Stage 2+: obs = 10 + 4×5 = 30 numbers

4 conflict-neighbor slots, har slot mein:
  [rel_x, rel_y, rel_vx, rel_vy, mask]
   ↑       ↑      ↑        ↑      ↑
   relative position    relative velocity   1=real, 0=empty

Agar 4 se kam neighbors hain → baaki slots mein zeros (padding)
```

---

## SECTION 5 — Building Block 4: PAH (Thesis ka Novel Contribution)

**File:** `code/algorithms/pah.py`

### Yeh kya hai?

PAH = Priority Arbitration Head.

Yeh ek chota sa neural network hai jo sirf ek kaam karta hai:
> "Abhi is drone ke liye mission important hai ya safety?" → α (alpha) number output

### PAH ke 3 inputs

```
┌─────────────────────────────────────────────────────┐
│  Input 1: τ_collision (tau)                         │
│           Takkar kab hogi? (seconds mein)           │
│           0 = abhi hogi!, 3.0 = bahut safe          │
│                                                     │
│  Input 2: d_target                                  │
│           Target kitna door hai? (units mein)       │
│           0 = already wahan, 141 = max door         │
│                                                     │
│  Input 3: n_conflict                                │
│           Kitne drones danger zone mein hain?       │
│           0 = koi nahi, 2 = dono drones danger mein │
└─────────────────────────────────────────────────────┘
```

### PAH ka architecture

```
Input [τ_norm, d_norm, n_norm]  ← pehle normalize karo (sab 0 se 1 mein)
         ↓
   Linear(3 → 32)    ← 3 inputs, 32 hidden neurons
         ↓
       ReLU          ← negative values zero kar do
         ↓
   Linear(32 → 1)    ← 32 se ek number
         ↓
      Sigmoid        ← 0 se 1 ke beech laao
         ↓
   Clip [0.1, 0.9]  ← kabhi bilkul 0 ya 1 mat hone do
         ↓
       α (alpha)     ← final output!
```

**Total parameters: ~130** — yeh ek bohat chota network hai (intentionally!)

### Normalization kyun zaroor hai?

```
Problem bina normalization ke:
  τ_collision:  0 se 3.0
  d_target:     0 se 141.4
  n_conflict:   0 se 2

d_target bohat badi range mein hai → network sirf use dekhega, baaki ignore

Fix — normalize karo:
  τ_norm    = τ / horizon          → 0 se 1
  d_norm    = d / world_diagonal   → 0 se 1
  n_norm    = n / (N-1)            → 0 se 1

Ab teeno same range mein hain → network sab consider karta hai
```

### Alpha ka matlab kya hota hai?

```
α = 0.9  →  reward = 0.9 × r_mission + 0.1 × r_safety
            Matlab: "Mission pe 90% dhyan, safety pe 10%"
            Kab: Drone safe hai, sirf target door hai

α = 0.5  →  reward = 0.5 × r_mission + 0.5 × r_safety
            Matlab: "Dono equally important"
            Kab: Normal situation

α = 0.1  →  reward = 0.1 × r_mission + 0.9 × r_safety
            Matlab: "Safety pe 90% dhyan, mission pe 10%"
            Kab: Takkar hone wali hai!
```

### PAH Prior Loss kya hai?

Ek chhoti si "pull" — alpha ko 0.5 ke paas rakhti hai.

```
prior_loss = 0.01 × (α - 0.5)²

Agar α → 0.9 → prior_loss bada hota hai → training mein penalty
Agar α ≈ 0.5 → prior_loss = 0        → koi penalty nahi
```

Yeh kyun? Reward hacking rokne ke liye. PAH seekh sakta tha ke "hamesha 0.9 do" — mission reward zyada hoti toh PAH exploitative behavior seekhta. Prior loss use rokta hai.

### PAH ko gradient kaise milta hai?

PAH seekhta hai in do losses se:

**1. Policy Gradient Loss:**
```
pah_loss = -(r_mission - r_safety) × α

Matlab:
  Agar r_mission > r_safety:
    → Mission better hai → alpha badhao → drone target pe focus kare
  
  Agar r_safety > r_mission (ya r_safety sirf penalty hai):
    → Safety zyada urgent → alpha ghatao → drone collision bachaye
```

**2. Prior Loss:**
```
prior_loss = 0.01 × (α - 0.5)²
```

Total PAH loss = policy_gradient + prior_loss

---

## SECTION 6 — Building Block 5: Training Script

**File:** `code/training/train.py`

### Yeh kya karta hai?

Sab pieces ko ek saath jodhta hai aur actually training karta hai.

```
┌──────────────────────────────────────────────────────────┐
│                      train.py                            │
│                                                          │
│  1. Config load karo (stage1.yaml ya stage2.yaml)        │
│  2. Environment banao                                    │
│  3. PAH banao (agar config mein ON ho)                   │
│  4. MAPPO banao (PAH ke saath ya bina)                   │
│  5. RolloutBuffer banao                                  │
│                                                          │
│  Loop (jab tak episodes poore na hon):                   │
│    ├─ collect_rollout (512 steps)                        │
│    ├─ MAPPO.update (actor + critic + PAH seekhte hain)  │
│    ├─ Evaluate (har 100 episodes)                        │
│    └─ Checkpoint save (har 200 episodes)                 │
│                                                          │
│  6. Final results save karo                              │
└──────────────────────────────────────────────────────────┘
```

### collect_rollout kya karta hai (detail mein)?

```python
Har step mein:

1. MAPPO.get_actions(obs) → actions, log_probs, value

2. env.step(actions) → next_obs, rewards, terminated, info
   info mein milta hai:
   - r_mission (mission reward)
   - r_safety  (safety reward)
   - pah_inputs (tau, d_target, n_conflict) — Stage 2 mein

3. Agar PAH ON hai:
   alpha = pah_wrapper.compute_alpha(tau, d_target, n_conflict)
   rewards = alpha × r_mission + (1-alpha) × r_safety

4. buffer.add(obs, actions, rewards, value, log_probs, done,
              r_mission, r_safety, pah_inputs)

5. Agla obs → repeat
```

---

## SECTION 7 — Sab Cheezein Ek Saath (Connection Map)

Yeh poora map samjho — kaun si cheez kaun si cheez ko call karti hai:

```
┌─────────────────────────────────────────────────────────────────┐
│                    TRAINING LOOP (train.py)                     │
│                                                                 │
│   ┌─────────────┐    actions    ┌──────────────────────────┐   │
│   │             │ ←──────────── │                          │   │
│   │   MAPPO     │               │   MultiUAVEnv            │   │
│   │   (mappo.py)│ ──────────→   │   (multi_uav_env.py)    │   │
│   │             │  observations │                          │   │
│   │  ┌────────┐ │               │  ┌──────────────────┐   │   │
│   │  │ Actor  │ │               │  │ Hungarian        │   │   │
│   │  └────────┘ │               │  │ Assignment       │   │   │
│   │  ┌────────┐ │               │  └──────────────────┘   │   │
│   │  │ Critic │ │               │  ┌──────────────────┐   │   │
│   │  └────────┘ │               │  │ ConflictGraph    │   │   │
│   └─────────────┘               │  │ (conflict_graph) │   │   │
│          ↑                      │  └──────────────────┘   │   │
│          │ update()             └──────────────────────────┘   │
│          │                              ↓                       │
│   ┌──────────────┐            r_mission, r_safety,             │
│   │ RolloutBuffer│ ←──────── pah_inputs (tau, d, n)           │
│   │              │                      ↓                       │
│   │ obs, actions,│            ┌──────────────────┐             │
│   │ rewards,     │            │   PAHWrapper     │             │
│   │ r_mission,   │ ←────────  │   (pah.py)       │             │
│   │ r_safety,    │  alpha,    │                  │             │
│   │ pah_inputs   │  combined  │  ┌────────────┐  │             │
│   └──────────────┘  rewards   │  │PAHNormalizer│ │             │
│                               │  └────────────┘  │             │
│                               │  ┌────────────┐  │             │
│                               │  │ PAH Network │  │             │
│                               │  │ (nn.Module) │  │             │
│                               │  └────────────┘  │             │
│                               └──────────────────┘             │
└─────────────────────────────────────────────────────────────────┘
```

### Flow ek step mein:

```
1. env.reset() → obs (30 numbers per drone)
                      ↓
2. MAPPO.get_actions(obs) → actions (vx, vy per drone)
                      ↓
3. env.step(actions) → obs, r_mission, r_safety, pah_inputs
                      ↓
4. PAHWrapper.compute_alpha(tau, d, n) → alpha (per drone)
                      ↓
5. r_combined = alpha × r_mission + (1-alpha) × r_safety
                      ↓
6. buffer.add(obs, actions, r_combined, ..., r_mission, r_safety, pah_inputs)
                      ↓
7. [512 steps ke baad] MAPPO.update(buffer)
   - GAE compute
   - PPO loss
   - Critic loss
   - PAH loss (policy gradient + prior)
   - Sab mila ke → optimizer.step()
                      ↓
8. Sab networks improve ho jaate hain → agle rollout mein better!
```

---

## SECTION 8 — Stages (Curriculum Learning)

Drones ko seedha mushkil situation mein nahi daala — phased approach:

```
Stage 1 (DONE ✅):
  - 3 drones, 3 targets
  - Koi obstacles nahi
  - Conflict graph: OFF
  - PAH: OFF (fixed α=0.5)
  - Goal: kya MAPPO kuch seekh sakta hai?
  - Result: 100% success from episode 300!

Stage 2 (NEXT):
  - 5 drones, 5 targets
  - Obstacles hain
  - Conflict graph: ON (obs = 30 numbers)
  - PAH: ON (learned alpha)
  - Goal: PAH useful hai?

Stage 3 (baad mein):
  - 8 drones
  - Dense obstacles
  - Same PAH

Stage 4 (generalization):
  - Unseen sizes (4 drones, 6 drones, etc.)
  - Kya model generalize kar sakta hai?
```

---

## SECTION 9 — Files ka Map

```
sandbox/
│
├── code/
│   ├── environment/
│   │   └── multi_uav_env.py     ← DUNIYA — drones, targets, obstacles
│   │
│   ├── algorithms/
│   │   ├── conflict_graph.py    ← SENSOR — kaun takraane wala hai?
│   │   ├── mappo.py             ← BRAIN — Actor + Critic + Buffer + Update
│   │   └── pah.py               ← NOVEL CONTRIBUTION — dynamic alpha
│   │
│   ├── training/
│   │   └── train.py             ← MAIN SCRIPT — sab ek saath
│   │
│   ├── configs/
│   │   ├── stage1.yaml          ← Stage 1 settings
│   │   └── stage2.yaml          ← Stage 2 settings (banana hai)
│   │
│   ├── notebooks/
│   │   ├── kaggle_stage1_training.ipynb   ← Kaggle pe chalane wala
│   │   └── output/v0/                     ← Stage 1 results
│   │
│   └── results/
│       └── stage1_seed42/        ← Final trained model + graphs
│
├── docs/
│   └── research/
│       ├── 01_pah_design.md     ← PAH ka technical design
│       └── 02_assignment_and_conflict.md  ← Math details
│
└── handbook/                    ← YEH FOLDER — sab simple mein
    └── poora_project_samjho.md  ← YEH FILE
```

---

## SECTION 10 — Abhi Tak Kya Ho Gaya (Status)

```
✅  Environment bana (multi_uav_env.py)
    → Drones move karte hain, targets assign hote hain, rewards milti hain

✅  MAPPO bana (mappo.py)
    → Actor + Critic + RolloutBuffer + PPO update
    → MPS (M3 GPU) support

✅  Stage 1 Training (Kaggle T4 GPU pe run hua)
    → 3000 episodes, 3 drones, no obstacles
    → Result: 100% success from episode 300!
    → Checkpoints: ep500 se ep3000 tak, final_model.pt

✅  Conflict Graph bana (conflict_graph.py)
    → CPA math se collision pairs detect karta hai
    → tau_collision, n_conflict, neighbor_obs deta hai

✅  Environment update hua
    → use_conflict_graph=True → obs 10 se 30 ho jaati hai
    → pah_inputs info dict mein aate hain

✅  PAH bana (pah.py)
    → PAHNormalizer + PriorityArbitrationHead + PAHWrapper
    → Alpha 0.1 se 0.9 ke beech
    → Prior loss reward hacking rokta hai
    → Tests pass!

✅  MAPPO + train.py mein PAH integrate hua
    → RolloutBuffer r_mission/r_safety store karta hai
    → update() mein PAH loss add hua
    → save/load mein PAH weights hain
    → Integration tests pass!

⏳  Stage 2 config (stage2.yaml) — banana hai
⏳  Stage 2 Kaggle notebook — banana hai
⏳  Stage 2 Training — Kaggle pe run karna hai
⏳  4 Baselines implement karna hai
⏳  Evaluation + thesis figures
```

---

## SECTION 11 — Mushkil Alfaz (Glossary)

| Lafz | Simple Matlab |
|------|---------------|
| **RL (Reinforcement Learning)** | AI ko reward/penalty de ke sikhana |
| **PPO** | Policy update ka safe tarika — chote steps mein |
| **MAPPO** | Multi-agent ke liye PPO |
| **Actor** | Decision maker — drone kahan jaye |
| **Critic** | Judge — situation kitni achi thi |
| **GAE** | "Yeh action kitna better tha expected se" calculate karna |
| **Advantage** | Expected se better/worse ka measure |
| **Rollout** | Training data collect karna — environment mein khelna |
| **Episode** | Ek game — reset se done tak |
| **Observation** | Drone ko jo information milti hai — aankhein |
| **Action** | Drone kya kare — yahan (vx, vy) |
| **Reward** | Feedback — kitna mila is step mein |
| **Hungarian** | Optimal target assignment math |
| **Conflict Graph** | Sparse graph — sirf dangerous drone pairs |
| **CPA** | Closest Point of Approach — minimum future distance |
| **PAH** | Priority Arbitration Head — dynamic alpha |
| **α (alpha)** | 0.1 to 0.9 — mission vs safety ka balance |
| **Prior loss** | Alpha ko 0.5 ke paas rakhne ki pull |
| **Reward hacking** | AI galat shortcut dhundhta hai — prior loss rokta hai |
| **Normalize** | Numbers ko same range mein laana (0 se 1) |
| **Gradient** | Direction jis mein network improve karna chahiye |
| **Gradient clipping** | Update ka size limit — stability ke liye |
| **Entropy** | Randomness — exploration encourage karta hai |
| **MPS** | Apple M3 GPU backend PyTorch mein |
| **Checkpoint** | Model ka snapshot — crash ke baad yahan se restart |
| **Dec-POMDP** | Formal math framework — multi-agent partial info |
| **Curriculum learning** | Pehle simple, phir mushkil — staged approach |
| **Baseline** | Comparison model — "PAH ke bina kya hota?" |
| **Fixed-α baseline** | Sab same lekin alpha=0.5 — PAH ko justify karta hai |
| **Seed** | Random number starting point — reproducibility ke liye |
| **Config (yaml)** | Settings file — numbers code mein hard-code nahi |
| **Batch size** | Ek saath kitne samples process hote hain |
| **Learning rate** | Network kitna fast seekhta hai (3e-4 = 0.0003) |

---

## SECTION 12 — Ek Sentence Mein Poora Project

> Multi-UAV missions mein drones ko target assignment aur collision avoidance dono ek saath karna hota hai. Hum MAPPO (multi-agent AI) use karte hain jisme PAH (ek chota network) dynamically decide karta hai ke abhi mission important hai ya safety — aur yeh thesis ka novel contribution hai.

---

*Yeh file Aayat ne Ayesha ke liye likhi — taake kabhi bhi confuse ho toh yahan aao.*
