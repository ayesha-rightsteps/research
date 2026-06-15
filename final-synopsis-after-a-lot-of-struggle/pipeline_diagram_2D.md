# Framework Pipeline Diagram — 2D Version

Paste the code below into **mermaid.live** → diagram tayyar.

---

```mermaid
flowchart TD
    A([2D Environment\n5 to 8 Drones · Dynamic Targets · Obstacles]) --> OBS

    subgraph OBS [STEP 1 — Observation Builder · per drone · per timestep]
        B[Self-State\n2D position + velocity]
        C[Assignment State\nHungarian min-cost allocation\nTarget relative position]
        D[Conflict Neighborhood\nDynamic Conflict Graph\nCollision-course drone pairs only]
        E[Obstacle Proximity\n4 cardinal directions]
    end

    B --> F[Joint Observation Vector]
    C --> F
    D --> F
    E --> F

    subgraph PROC [STEP 2 — Parallel Processing]
        G[MAPPO Decentralized Actor\nOutput: 2D velocity action]
        H[Priority Arbitration Head\n2-layer MLP · 64 neurons\nInput: τ_collision · d_target · n_conflict\nOutput: α ∈ 0 to 1]
    end

    F --> G
    F --> H

    G --> K
    H --> K

    K["STEP 3 — Reward Computation\nr_total = α × r_assignment + 1−α × r_avoidance\nα learned · not fixed"]

    K --> L[STEP 4 — Environment Step\nNew state observed]
    L --> A

    subgraph TRAIN [STEP 5 — Centralized Training · MAPPO]
        M[Centralized Critic\nFull joint state of ALL drones]
        N[Policy Gradient Update\nUpdates Actor + PAH jointly]
        M --> N
        N --> G
        N --> H
    end

    style H fill:#ff9900,color:#000
    style K fill:#2e7d32,color:#fff
    style TRAIN fill:#e3f2fd,stroke:#1565c0
    style OBS fill:#fafafa,stroke:#999
    style PROC fill:#fff8e1,stroke:#f9a825
```

---

## Reading the Diagram

| Box | Kya hai |
|---|---|
| **2D Environment** | Simulation — 5 to 8 drones, dynamic targets, obstacles |
| **Observation Builder** | Har drone 4 cheezein observe karta hai (self, target, neighbors, obstacles) |
| **MAPPO Actor** | Action decide karta hai — 2D velocity |
| **Priority Arbitration Head (orange)** | α decide karta hai — assignment kitna, avoidance kitna |
| **Reward Computation (green)** | r = α × r_assign + (1−α) × r_avoid — α fixed nahi, learned hai |
| **Centralized Critic (blue)** | Training mein sab drones ka poora state dekhta hai |
| **Policy Gradient Update** | MAPPO Actor aur PAH dono ko SAATH update karta hai |

---

## PAH — Priority Arbitration Head (Main Contribution)

```
Inputs (3 numbers, per timestep):
  τ_collision  →  kitne seconds mein collision hoga
  d_target     →  assigned target kitna door hai
  n_conflict   →  conflict neighborhood mein kitne drones hain

Output (1 number):
  α ∈ [0, 1]
    α → 1  :  assignment dominant  (target ki taraf jao)
    α → 0  :  avoidance dominant   (collision se bacho)

Formula:
  r_total = α × r_assignment + (1−α) × r_avoidance

Training:
  MAPPO actor ke saath jointly — koi alag training loop nahi
  Centralized critic mein koi change nahi
```

**Yeh kyun novel hai:**
DA-MAPPO aur IGAT-MARL dono mein α fixed constant hai — training se pehle manually set hota hai, kabhi nahi badlta.
PAH mein α **seekhta hai** — har timestep pe situation dekh ke decide karta hai. Kisi bhi existing framework mein yeh nahi hai.
