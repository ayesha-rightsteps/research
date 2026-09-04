# Implementation Guide — Ayesha's MS Research
## Multi-Agent PPO for Joint Target Assignment & Collision Avoidance in UAV Systems

> **Yeh file sirf tumhare liye likhi gayi hai — ek researcher ki taraf se jo assume karta hai tum field mein bilkul naye ho.**
> Har cheez plain language mein explain ki gayi hai. Koi jargon bina explanation ke nahi.

---

## SECTION 1: Bari Tasveer — Tum Actually Kia Bana Rahi Ho?

Soch lo tum ek **video game bana rahi ho** jis mein:
- Ek 2D map hai (top-down view, jaise chess board)
- Us map pe **3 se 8 drones** hain (players)
- Map pe **targets** hain (goals, jaise flags)
- Map pe **obstacles** bhi hain (walls ya rocks)
- Har drone ko apna target reach karna hai **bina kisi se takray**

Problem yeh hai ke drones ek dusre ko dekh ke automatically seekhein ke kab target ki taraf jao aur kab raasta badlo. Yeh koi rule-based system nahi — drones **khud seekhte hain** experience se (jaise insaan chess seekhta hai — haar ke, jeet ke).

Tumhara research ka novel part yeh hai ke tumne **ek naya brain module** design kiya hai jisko **Priority Arbitration Head (PAH)** kehte hain. Yeh module har second decide karta hai: "Abhi target ki taraf jao ya pehle collision se bacho?"

---

## SECTION 2: Tumhari Research Ke 5 Building Blocks

Tumhari puri implementation inhi 5 cheezoon se bani hai:

```
┌─────────────────────────────────────────────────────────────┐
│                    TUMHARI SYSTEM                           │
│                                                             │
│  1. ENVIRONMENT  ──►  2D world jahan drones fly karte hain  │
│         │                                                   │
│  2. HUNGARIAN    ──►  "Kaun sa drone kaun sa target lay?"   │
│     ALGORITHM                                               │
│         │                                                   │
│  3. CONFLICT     ──►  "Kaun kaun se drones ki takkar        │
│     GRAPH              honewaali hai?"                      │
│         │                                                   │
│  4. MAPPO        ──►  Main AI brain jo drones ko            │
│     (Neural Net)       movements sikhata hai                │
│         │                                                   │
│  5. PRIORITY     ──►  TUMHARA NOVEL PART — "Abhi kia        │
│     ARBITRATION        priority hai: target ya safety?"     │
│     HEAD (PAH)                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## SECTION 3: Tools aur Libraries — Kia Install Karo Gi?

### Programming Language: Python 3.10 ya 3.11
Koi aur option nahi. Poora RL research Python mein hota hai.

### Core Libraries (sab free hain):

| Library | Kia Karta Hai | Tum Isay Kyun Use Karo Gi |
|---------|--------------|--------------------------|
| **PyTorch** | Neural networks banata hai | MAPPO aur PAH ka brain yahi hai |
| **NumPy** | Math aur arrays | Har jagah use hoga |
| **SciPy** | Scientific algorithms | Hungarian algorithm yahan se milega (`scipy.optimize.linear_sum_assignment`) |
| **Gymnasium** (pehle OpenAI Gym tha) | RL environment ka standard structure | Tumhara 2D world isi structure mein banega |
| **Matplotlib** | Graphs banana | Training results plot karne ke liye |
| **Pandas** | Data tables | Results save aur analyze karne ke liye |
| **PyBullet** | Physics simulation | Synopsis mein likha tha, lekin 2D ke liye actually zarori nahi (neeche explain kiya) |

### Install kaise karo:
```bash
pip install torch numpy scipy gymnasium matplotlib pandas
```

---

## SECTION 4: PyBullet Wali Confusion — Important!

Synopsis mein **PyBullet** likha hai lekin tumhara research **2D** hai.

PyBullet ek **3D physics engine** hai — ye realistic gravity, weight, wind sab simulate karta hai. 2D research ke liye yeh overkill hai aur complex bhi.

**Recommendation:** PyBullet use MAT karo apni environment ke liye.

Iske bajaaye tum ek **custom Python environment** banao jo Gymnasium ke structure ko follow kare. Yeh much simpler hai, faster train hoga, aur 2D research ke liye bilkul theek hai.

---

## SECTION 5: DA-MAPPO aur IGAT-MARL — Code Kahan Se Milega?

Yeh important reality check hai:

### DA-MAPPO (Sheng et al., 2026)
- **Paper:** IEEE Internet of Things Journal, 2026
- **Code publicly available hai ya nahi?** Abhi tak confirmed nahi. 2026 paper hai, researchers ne GitHub link share kiya ho to paper ke PDF mein ya IEEE page pe milega.
- **Kya karna hai:**
  1. Paper ka IEEE page dhundho
  2. Authors ka email dhundho (usually paper mein hota hai), email karo: "Could you please share your implementation code for DA-MAPPO?"
  3. Researchers usually share karte hain — ye normal academic practice hai

### IGAT-MARL (Rezaee et al., 2026)
- **Paper:** Applied Soft Computing, 2026
- **Same situation** — paper dekhna hoga GitHub link ke liye
- Same email approach karo

### Agar code nahi mila toh?
Ghabrao mat. Tumhe unka exact code copy nahi karna. Tumhe unke **methodology** ko samjhna hai aur apni implementation mein use karna hai. Papers mein itni detail hoti hai ke reimplementation possible hai.

---

## SECTION 6: MAPPO Ka Code — Yahan Se Milega (Confirmed!)

MAPPO ka original implementation publicly available hai:

**GitHub Repository:** `marlbenchmark/on-policy`
- Search karo Google pe: **"MAPPO on-policy GitHub marlbenchmark"**
- Yeh Yu et al. (2022) wale paper ka official code hai
- MIT License hai — freely use kar sakti ho

Yeh repo tumhare liye starting point hai. Tumhe isko modify karna hoga apni research ke liye.

---

## SECTION 7: Platform — Kaggle, Colab, ya Local Computer?

### Tumhara Research Kitna Heavy Hai?

Suno — 2D environment, 8 drones maximum — yeh **relatively lightweight** hai MARL research mein. Yeh koi 100-drone 3D simulation nahi. 

### Option Comparison:

#### Option A: Kaggle (RECOMMENDED tumhare liye)
- **Free GPU:** NVIDIA T4 ya P100 (bilkul free)
- **Session time:** 30 hours per week free GPU
- **Internet access:** Papers download kar sakti ho, GitHub se clone kar sakti ho
- **Sharing:** Supervisor ko easily share kar sakti ho notebook link se
- **Best for:** Experiments run karna, results dekhna
- **Limitation:** Agar session band ho gayi toh state save karni hoti hai

#### Option B: Google Colab
- **Free GPU:** T4 (free tier mein limited)
- **Problem:** Session 12 hours se zyada run nahi karta free mein, training interrupt ho jaati hai
- **Better option:** Colab Pro (~$10/month) agar Kaggle se problem ho

#### Option C: Local Computer (MacBook/PC)
- **Agar GPU nahi hai:** Training bohat slow hogi (ghante ki jagah din lag sakte hain)
- **Use karo:** Code likhne ke liye, debugging ke liye — training Kaggle pe karo
- **M1/M2 Mac walo ke liye:** PyTorch MPS support hai, kuch help milegi

#### Recommendation:
> **Code likho local machine pe (VS Code use karo), training aur experiments Kaggle pe karo.**

---

## SECTION 8: GPU Ki Zarurat Hai Ya Nahi?

**Haan, GPU chahiye — lekin free GPU kaafi hai.**

Explanation:
- Neural networks (MAPPO, PAH) GPU pe **10x-50x faster** train hote hain CPU se
- Tumhara case: 2D environment, 8 drones max, relatively simple network
- **Kaggle ka free T4 GPU tumhare liye sufficient hai**
- Agar 8 drones, simple network: ek training run likely **2-6 ghante** lagega
- Tum raat ko run chhod do, subah results ready

---

## SECTION 9: Computational Cost — Konsa Part Heavy Hai?

Har step ka load yahan estimate kiya gaya hai:

| Component | Computational Cost | Kyun |
|-----------|-------------------|------|
| 2D Environment Step | Very Low | Sirf positions update hoti hain |
| Hungarian Algorithm | Low-Medium | O(n³) — 8 drones ke liye negligible |
| Conflict Graph Update | Low | O(n²) — sirf distances check |
| MAPPO Neural Network Forward Pass | Medium | GPU pe fast hai |
| MAPPO Gradient Update (training) | High | Yahan GPU zaroori hai |
| Priority Arbitration Head | Very Low | Sirf 2-layer small network |

**Bottleneck:** MAPPO training — baaki sab fast hai.

---

## SECTION 10: Step-by-Step Implementation Plan

### STEP 1: Environment Banana (Week 1-4)

Yeh sab se pehla kaam hai. Tumhara **2D world** Python class mein banana hai.

```
Environment mein yeh hoga:
- Grid ya continuous 2D space (e.g., 100x100 units)
- N drones (initially 3, baad mein 8 tak)
- M targets (N ke barabar — har drone ka ek target)
- K obstacles (static positions)
- Har step mein: drone move karta hai, collision check hoti hai,
  target reach check hota hai
```

Gymnasium ka `Env` class inherit karo:

```python
import gymnasium as gym
import numpy as np

class MultiUAVEnv(gym.Env):
    def __init__(self, n_drones=3, n_obstacles=5):
        self.n_drones = n_drones
        # ...
    
    def reset(self):
        # drones ko random positions pe rakh do
        # targets generate karo
        # return observation
        pass
    
    def step(self, actions):
        # drones ko move karo
        # collision check karo
        # reward calculate karo
        # return obs, reward, done, info
        pass
```

**Resource:** Gymnasium documentation: `gymnasium.farama.org`

---

### STEP 2: Hungarian Algorithm (Week 1-2, parallel with environment)

Yeh already implement hai SciPy mein! Tumhe likhna nahi:

```python
from scipy.optimize import linear_sum_assignment
import numpy as np

def assign_targets(drone_positions, target_positions):
    # Cost matrix: har drone ka har target se distance
    cost_matrix = np.zeros((n_drones, n_targets))
    for i, drone in enumerate(drone_positions):
        for j, target in enumerate(target_positions):
            cost_matrix[i][j] = np.linalg.norm(drone - target)
    
    # Hungarian algorithm ek line mein:
    drone_indices, target_indices = linear_sum_assignment(cost_matrix)
    
    return target_indices  # drone i ka target = target_indices[i]
```

Yeh har step pe call hoga — jaise drone move karta hai, reassignment check hoti hai.

---

### STEP 3: Conflict Graph (Week 3-4)

Yeh graph batata hai: "Kaun se drones collision course pe hain?"

```python
def build_conflict_graph(drone_positions, drone_velocities, 
                          time_horizon=2.0, danger_threshold=5.0):
    """
    Agar drone A aur drone B agle 'time_horizon' seconds mein
    'danger_threshold' distance se closer aajayein, toh unke
    beech edge draw karo.
    """
    n = len(drone_positions)
    edges = []
    
    for i in range(n):
        for j in range(i+1, n):
            # Future position predict karo (linear extrapolation)
            future_pos_i = drone_positions[i] + drone_velocities[i] * time_horizon
            future_pos_j = drone_positions[j] + drone_velocities[j] * time_horizon
            
            future_dist = np.linalg.norm(future_pos_i - future_pos_j)
            
            if future_dist < danger_threshold:
                edges.append((i, j))
    
    return edges  # conflict mein hain ye pairs
```

---

### STEP 4: MAPPO Implementation (Week 5-8)

Yeh tumhara main AI brain hai. Yahan do options hain:

**Option A (Recommended):** GitHub se MAPPO code clone karo aur apni environment ke liye modify karo.
```
git clone https://github.com/marlbenchmark/on-policy
```

**Option B:** Scratch se likhna — zyada seekhoge lekin time zyada lagega.

MAPPO mein kia hota hai (simple explanation):
```
Har drone ka apna "Actor" network hota hai:
  Input: drone ki observation (position, target, neighbors, obstacles)
  Output: action (kahan move karna hai — 2D velocity)

Ek shared "Critic" network hota hai (training ke waqt sirf):
  Input: sabhi drones ki combined state
  Output: "Yeh situation kitni achi hai?" (value estimate)

Training loop:
  1. Sab drones environment mein play karo (experience collect karo)
  2. Critic se estimate karo: kia hona chahiye tha
  3. Actor ko update karo: achi actions probability badhao, buri kam karo
  4. PPO clipping: update zyada bada mat hone do (stability ke liye)
  5. Repeat
```

---

### STEP 5: Priority Arbitration Head — TUMHARA NOVEL PART (Week 9-10)

Yeh tumhara original contribution hai. Yeh ek chota sa neural network hai jo Actor ke saath train hota hai.

```
PAH ka kaam:
  INPUT (3 numbers):
    1. τ_collision: kitne waqt mein collision hogi (time-to-collision)
       → Agar yeh number chhota hai = danger close!
    2. d_target: target kitna door hai
       → Agar yeh bada hai = abhi target door hai
    3. n_conflict: kitne drones conflict graph mein mere neighbors hain
       → Agar yeh zyada hai = bheed mein hoon

  OUTPUT (1 number):
    α ∈ [0, 1]  ← yeh dynamic weight hai
    
  MEANING OF α:
    α = 0.9 → "90% target pe focus karo, 10% collision pe"
    α = 0.1 → "10% target, 90% collision avoidance pe focus karo"
```

```python
import torch
import torch.nn as nn

class PriorityArbitrationHead(nn.Module):
    def __init__(self):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(3, 32),   # 3 inputs: tau, d_target, n_conflict
            nn.ReLU(),
            nn.Linear(32, 1),   # 1 output: alpha
            nn.Sigmoid()        # output 0 to 1 ke beech
        )
    
    def forward(self, tau_collision, d_target, n_conflict):
        inputs = torch.tensor([tau_collision, d_target, n_conflict], 
                               dtype=torch.float32)
        alpha = self.network(inputs)
        return alpha  # 0 to 1
```

Yeh alpha phir reward calculation mein use hota hai:

```python
def compute_reward(mission_reward, safety_reward, alpha):
    # alpha = assignment priority weight (PAH output)
    # (1 - alpha) = collision avoidance priority weight
    total_reward = alpha * mission_reward + (1 - alpha) * safety_reward
    return total_reward
```

Yeh isiliye novel hai kyunki **sab existing papers mein alpha fixed hota hai** (jaise 0.5 hamesha). Tumhara PAH yeh **situation dekh ke decide karta hai.**

---

### STEP 6: Curriculum Learning (Week 11-14)

Pehle easy se seekho, phir mushkil:

```
Stage 1: 3 drones, static targets, no obstacles
         → Ye DA-MAPPO replicate karna hai (baseline)
         
Stage 2: 5 drones, moving targets, few obstacles
         → Mushkil ho raha hai

Stage 3: 8 drones, dynamic targets, many obstacles
         → Full complexity
         
Stage 4: Unseen swarm sizes (test generalization)
         → Kia seekha hua policy naye scenarios mein kaam karti hai?
```

---

## SECTION 11: Observation Vector — Har Drone Ko Kia Dikhta Hai?

Har drone ko yeh information milti hai (observation):

```
Observation of drone i = [
    pos_x, pos_y,           # apni position (2 numbers)
    vel_x, vel_y,           # apni velocity (2 numbers)
    target_rel_x, target_rel_y,  # target kahan hai relative to me (2 numbers)
    neighbor_1_pos_x, neighbor_1_pos_y, neighbor_1_vel_x, neighbor_1_vel_y,  # conflict neighbor 1
    neighbor_2_pos_x, ...   # conflict neighbor 2 (agar hai)
    obs_north, obs_east, obs_south, obs_west  # obstacles kitni door hain 4 directions mein
]
```

Total size depends on max neighbors. Agar max 3 conflict neighbors: ~18-20 numbers per drone.

---

## SECTION 12: Evaluation — Results Kaise Measure Karo Gi?

### Primary Metric:
**Mission Success Rate** = kitne episodes mein SARE drones ne apne targets reach kiye bina collision ke

```python
def compute_mission_success(episode_results):
    successful = sum(1 for ep in episode_results if ep['all_targets_reached'] 
                     and ep['zero_collisions'])
    return successful / len(episode_results)  # 0 to 1, higher is better
```

### Secondary Metrics:
- Inter-drone collisions per episode
- Obstacle collisions per episode
- Target reassignments per episode
- Average trajectory length per drone

### Baselines (comparisons):

| Baseline | Description |
|----------|-------------|
| Standard MAPPO | MAPPO without assignment or conflict graph |
| DA-MAPPO (your reimplementation) | With Hungarian assignment, WITHOUT conflict graph |
| IGAT-MARL (your reimplementation) | With conflict graph, WITHOUT real-time assignment |
| Fixed-weight MAPPO | Like your method BUT alpha is fixed (e.g., 0.5 always) |

Last baseline sabse important hai — yeh directly prove karta hai ke tumhara PAH (learned alpha) fixed alpha se better hai.

---

## SECTION 13: Project Folder Structure (Recommended)

```
your_project/
│
├── environment/
│   ├── multi_uav_env.py      # 2D environment
│   └── rendering.py          # visualization (optional)
│
├── algorithms/
│   ├── hungarian.py          # target assignment
│   ├── conflict_graph.py     # conflict detection
│   ├── mappo.py              # MAPPO actor-critic
│   └── pah.py                # Priority Arbitration Head
│
├── training/
│   ├── train.py              # main training loop
│   └── curriculum.py         # curriculum stages
│
├── evaluation/
│   └── evaluate.py           # test trained models
│
├── configs/
│   └── config.yaml           # hyperparameters (learning rate, etc.)
│
├── results/
│   ├── models/               # saved trained weights
│   └── plots/                # graphs
│
└── notebooks/
    └── experiments.ipynb     # Kaggle notebook
```

---

## SECTION 14: Kaggle Pe Kaise Kaam Karo?

1. **Account banao:** kaggle.com
2. **New Notebook:** "+ Create" → "New Notebook"
3. **GPU enable karo:** Settings → Accelerator → GPU T4 x2
4. **GitHub se code import karo:**
   ```python
   !git clone https://github.com/your-username/your-project.git
   ```
5. **Libraries install karo:**
   ```python
   !pip install torch gymnasium scipy matplotlib
   ```
6. **Training run karo aur model save karo:**
   ```python
   import torch
   torch.save(model.state_dict(), '/kaggle/working/trained_model.pth')
   ```
7. **Download karo:** Output section se model download kar sakte ho

**Tip:** Har few hours mein model save karo — session expire hoti hai.

---

## SECTION 15: Realistic Timeline

| Month | Kia Karogi |
|-------|------------|
| Month 1 | Python basics agarchi kaafi nahi aata, Gymnasium sikho, simple 2D environment banao |
| Month 2 | Hungarian algorithm integrate karo, conflict graph banao, simple testing |
| Month 3 | MAPPO code samjho (existing GitHub code), apni environment se connect karo |
| Month 4 | Stage 1 curriculum: 3 drones, baseline DA-MAPPO replicate |
| Month 5-6 | PAH design karo aur MAPPO mein integrate karo |
| Month 7 | Stage 2-3 curriculum training |
| Month 8-9 | Evaluation vs. all 4 baselines, ablation studies |
| Month 10-11 | Results analyze karo, failure cases dhundho |
| Month 12 | Thesis writing |

---

## SECTION 16: Pehle Pehle Kia Seekho?

Agar tum bilkul noob ho, yeh order follow karo:

1. **Python basics** (agar weak hai): Variables, loops, functions, classes — 1 week
2. **NumPy** (arrays aur math): 3-4 din
3. **Basic RL concepts** (sirf theory): Spinning Up in Deep RL (OpenAI ki free tutorial) — 1 week
4. **Gymnasium hello world**: Cartpole environment mein ek simple agent chalao — 2-3 din
5. **PyTorch basics**: Simple neural network banao — 1 week
6. **Phir apna environment banana shuru karo**

---

## SECTION 17: Kahan Dhundho (Resources)

| Cheez | Kahan |
|-------|-------|
| MAPPO code | GitHub: `marlbenchmark/on-policy` |
| RL theory (free) | Spinning Up in Deep RL — openai.com (Google karo) |
| Gymnasium docs | gymnasium.farama.org |
| PyTorch tutorials | pytorch.org/tutorials |
| Hungarian algorithm | `scipy.optimize.linear_sum_assignment` — SciPy docs |
| DA-MAPPO paper | IEEE Internet of Things Journal — authors ko email karo code ke liye |
| IGAT-MARL paper | Applied Soft Computing — same, authors ko email karo |
| Free GPU training | kaggle.com (Notebooks) |

---

## SECTION 18: Ek Aur Important Baat — Kia Tum Ye Kar Sakti Ho?

Haan. Yeh research technically doable hai, especially kyunki:

- 2D hai, 3D nahi — environment simple hai
- 8 drones max — manageable scale
- PyTorch mein MAPPO implementations available hain
- PAH novel but small hai — 2-layer network
- Free GPUs (Kaggle) is research ke liye sufficient hain

**Sabse mushkil part:** Environment banana aur MAPPO ko apni environment se sahi tarah connect karna. Yeh 2-3 months ka kaam hai lekin doable hai.

---

*Yeh guide tumhare supervisor ke saath bhi share kar sakti ho planning ke liye.*
*Agar koi bhi point clear nahi hua toh poochho — har step pe help milegi.*
