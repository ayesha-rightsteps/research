# Framework Pipeline — Mermaid Diagram Code

Copy-paste this into any Mermaid renderer (e.g., mermaid.live) to get the visual diagram.

---

```mermaid
flowchart TD
    A([2D Simulation Environment\n3 to 8 Drones · Dynamic Targets · Obstacles])

    A --> B["Observation Builder\n1 Self-State — 2D position + velocity\n2 Assignment State — Hungarian allocation\n3 Conflict Graph — collision-course pairs\n4 Obstacle Proximity"]

    B --> C[Joint Observation Vector]

    C --> D["MAPPO Decentralized Actor\n2D velocity action"]
    C --> E["Priority Arbitration Head\ntime-to-collision · target distance · conflict count\nlearned weight  α ∈ 0, 1"]

    D --> F["Blended Reward\nr = α · r_assign + 1−α · r_avoid"]
    E --> F

    F --> G[Environment Step — New State]
    G --> A

    H["Centralized Critic\nfull joint state — training only"] -.->|trains| D
    H -.->|trains| E

    style A fill:#1a237e,color:#fff,font-weight:bold
    style E fill:#e65100,color:#fff,font-weight:bold
    style F fill:#2e7d32,color:#fff,font-weight:bold
    style H fill:#1565c0,color:#fff
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
