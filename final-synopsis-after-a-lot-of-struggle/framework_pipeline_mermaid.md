# Framework Pipeline — Mermaid Diagram Code

Copy-paste this into any Mermaid renderer (e.g., mermaid.live) to get the visual diagram.

---

```mermaid
flowchart TD
    A([3D Environment\n5–8 Drones, Dynamic Targets, Obstacles]) --> B

    subgraph OBS [Step 1 — Observation Builder per Drone]
        B[Self-State\n3D position + velocity]
        C[Assignment State\nHungarian min-cost allocation\n→ target relative position]
        D[Conflict Neighborhood\nDynamic Conflict Graph\n→ collision-course drone pairs]
        E[Obstacle Proximity\n6 cardinal directions]
    end

    B --> F[Joint Observation Vector]
    C --> F
    D --> F
    E --> F

    F --> G[MAPPO Decentralized Actor\nOutputs: 3D velocity action]
    F --> H[Priority Arbitration Head\n2-layer FF, 64 neurons\nInputs: τ_collision · d_target · n_conflict\nOutput: α ∈ 0,1]

    G --> I[3D Velocity Command]
    H --> J[Dynamic Weight α\nα→1: assignment dominant\nα→0: avoidance dominant]

    I --> K["Reward Computation\nr_total = α × r_assign + 1−α × r_avoid"]
    J --> K

    K --> L[Environment Step\nNew State Observed]
    L --> A

    subgraph TRAIN [Centralized Training — MAPPO]
        M[Centralized Critic\nFull Joint State of ALL Drones] --> N[Policy Gradient Update]
        N -->|Updates jointly| G
        N -->|Updates jointly| H
    end

    style H fill:#ff9900,color:#000,font-weight:bold
    style K fill:#4CAF50,color:#fff
    style TRAIN fill:#e8f4f8,stroke:#2196F3
```

---

## What Makes This Novel

| Component | Existing Frameworks | This Framework |
|---|---|---|
| Reward weighting | Fixed constants (DA-MAPPO: fixed C_collision; IGAT-MARL: fixed P1, P2) | **Learned α — changes every timestep** |
| Assignment + avoidance | Handled by separate frameworks | **Joint observation, single policy** |
| 3D environment | DA-MAPPO: 2D; IGAT-MARL: 2D | **3D — altitude adds vertical collision courses** |
| Priority Arbitration Head | Does not exist | **First learned arbitration mechanism in multi-UAV coordination** |

---

## PAH Technical Spec (for Methodology section)

- **Architecture:** 2-layer feedforward MLP, 64 hidden neurons, ReLU activation, sigmoid output
- **Inputs (3 scalars):**
  - τ_collision — time-to-collision with nearest conflict neighbor (seconds)
  - d_target — Euclidean distance to assigned target (meters)
  - n_conflict — count of drones currently in conflict neighborhood
- **Output:** α ∈ [0,1] (single scalar per drone per timestep)
- **Training:** Jointly with MAPPO actor via same policy gradient update; no separate training loop
- **Critic:** No change to centralized critic — PAH adds zero parameters to the critic
- **At deployment:** Runs decentralized on each drone using only local observation
- **Reward formula:** r_total = α × r_assignment + (1−α) × r_avoidance
