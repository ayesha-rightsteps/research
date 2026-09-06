# Samjho: docs/research/03_baseline_specs.md

## Yeh cheez kya hai
4 baselines (comparison ke liye systems) ka exact detail, aur DA-MAPPO + IGAT-MARL
papers se nikaale hue saare numbers/settings.

## Iski zaroorat kyun
Tumhara PAH kitna achha hai — ye tabhi pata chalega jab sahi cheezon se compare karo.
Aur DA-MAPPO/IGAT ko reproduce karne ke liye unki settings chahiye.

## Main baatein

### 4 baselines + hamara method

| Naam | Assignment on? | Conflict graph on? | α |
|------|:-:|:-:|---|
| B1 plain MAPPO | ✗ | ✗ | ek hi reward |
| B2 DA-MAPPO-2D | ✓ | ✗ | fixed |
| B3 IGAT-style | ✗ | ✓ | fixed |
| B4 fixed-α MAPPO | ✓ | ✓ | **fixed** (0.3, 0.5, 0.7 try karo) |
| **M hamara** | ✓ | ✓ | **PAH se seekha hua** |

- **M vs B4** = "α seekhna vs α fix karna" — thesis ka sawaal
- **B4 vs B2/B3** = "dono mechanism saath mein > akele"
- **B2/B3 vs B1** = "har mechanism kuch fayda deta hai ya nahi"

### DA-MAPPO se nikale numbers (hamare starting points)
- N = 3 drones, episode 600 steps, γ = 0.99
- Network: MLP 3 layers × 256, learning rate 1e-5, PPO clip 0.2, entropy 0.1,
  10 PPO epochs, total 3 million steps
- Reward: progress + arrival bonus + hover + graded obstacle penalty + step penalty
- Curriculum: obstacles dheere badhao (0→40)
- **Unka key result:** augmented observation hatao → success 0% (Table VI). Ye hamara
  "stack sahi hai ya nahi" ka test hai.

### IGAT-MARL se nikale numbers
- DQN (PPO nahi!), discrete actions (±15° turn), fixed-wing aircraft
- Conflict graph DCPA/TCPA se, GAT network (4 heads, hidden 128)
- Curriculum 3→10 drones with weight transfer
- Result: +17.56% reward, −10.52% dangerous time, −44% edges vs benchmark

### Zaroori baat B3 ke baare mein
IGAT-MARL DQN hai, hum MAPPO. To hamara "B3 IGAT-style" = MAPPO + conflict-graph
neighbors (assignment ke bina). Hum unka **idea** le rahe hain, algorithm nahi.
Ye thesis mein clearly likhna hai. Supervisor se poochhа hai (Q12).

### Zaroori warning
DA-MAPPO/IGAT ke numbers **unke** simulator mein hain. "DA-MAPPO 90%, hamara X%" —
ye fair comparison **nahi** hai. Fair comparison = hamara B2 vs hamara M, same env mein.

## Mushkil lafz
- **Baseline** = comparison ke liye rakha system
- **MLP** = simple neural network (layers ek ke baad ek)
- **Learning rate** = model kitni tezi se seekhta hai (chhota = dheere par stable)
- **PPO epochs** = ek data batch pe kitni baar training pass
- **Weight transfer** = purane (chhote) model ke seekhe weights se naya (bada) shuru karna
- **GAT (Graph Attention Network)** = graph pe chalne wala network jo "kis neighbor pe
  kitna dhyaan dena" khud seekhta hai
- **DQN** = ek purana RL algorithm (value-based, off-policy)
