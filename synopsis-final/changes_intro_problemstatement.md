# Changes: Introduction + Problem Statement + Tentative Schedule
*Ayesha in document mein yeh replace karein*

---

## 1. Introduction
*(No "Background" heading — seedha text se shuru)*

Unmanned aerial vehicles (UAVs) have transitioned from specialized military tools to widely used platforms across civilian and industrial domains. Their deployment in disaster response, search and rescue, precision agriculture, infrastructure inspection, and emergency communications has grown steadily, driven by advances in onboard computing, sensor miniaturization, and wireless communication. In most real-world missions of practical value, a single drone is insufficient. The scale of the task, the need for redundancy, or the requirement to cover large areas simultaneously demands teams of drones operating together. This shift from single-UAV operations to coordinated multi-UAV systems has introduced a new class of challenges that hardware improvements alone cannot resolve.

Coordinating multiple drones in shared airspace requires each drone to make decisions that are individually rational but collectively effective. Classical approaches to this problem rely on centralized planners that compute globally optimal solutions before deployment. These methods work in controlled, static settings but break down when the environment changes — when targets move, obstacles appear, or drones fail mid-mission. The planner cannot anticipate every contingency, and recomputing a global solution in real time is computationally intractable for large teams. This limitation has led researchers toward learning-based methods, where drones acquire navigation policies through experience rather than through preprogrammed rules.

Deep reinforcement learning (DRL) has become the dominant paradigm for this purpose. A DRL agent interacts with a simulated environment, receives reward signals, and gradually improves its policy without requiring an explicit model of the world. Extended to multiple agents through multi-agent deep reinforcement learning (MARL), this approach allows teams of drones to develop cooperative behaviors, each drone learning to account for the actions of its teammates. Several MARL frameworks have been proposed for this setting, including centralized-training decentralized-execution architectures that train agents with access to global information but allow them to act independently during deployment.

Progress in this field, however, has followed a fragmented pattern. Researchers who studied how to assign targets to drones in real time developed their methods without building in collision avoidance between teammates. Researchers who studied how drones detect and avoid each other during flight developed their methods without incorporating any goal structure — their drones had no targets to reach, only teammates to avoid. Work that operated in large environments did so in two dimensions only. The result is a collection of capable but partial solutions, each addressing one aspect of the coordination problem while assuming the others are either trivial or solved elsewhere.

This research addresses one specific and well-documented instance of this fragmentation. The two most relevant recent contributions — one to target assignment and one to collision avoidance — each explicitly identify the other's problem as their own next step, confirming that no existing work has brought both mechanisms together. The present work proposes a unified MAPPO-based framework that integrates real-time target assignment and conflict-aware collision avoidance in a single policy, operating in a three-dimensional environment with five to eight drones. The goal is to determine empirically whether these two mechanisms, when placed in the same policy in 3D space, reinforce each other or produce competing navigation signals that degrade overall performance.

---

## 3. Problem Statement
*(2-3 lines, no paper mentions)*

Existing approaches to multi-UAV coordination treat dynamic target assignment and collision avoidance as separate problems, each developed and validated independently in two-dimensional environments. When both mechanisms operate simultaneously in three-dimensional space, they generate competing navigation signals — the assignment directs each drone toward its target without awareness of active collision conflicts, while the collision avoidance module forces course corrections without awareness of current assignments, a tension that becomes structurally significant when vertical flight paths are introduced. The result is a fundamental tension in three-dimensional multi-UAV deployment: goal-directed navigation and inter-agent collision avoidance pull each drone in opposing directions, and whether a unified policy can hold both objectives in balance — or whether one systematically undermines the other — has not been established.

---

## Tentative Schedule
*(12 months)*

| Tasks | M 1–2 | M 3–4 | M 5–7 | M 8–9 | M 10–11 | M 12 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| Task-I: 3D environment setup + baseline replication | ● | | | | | |
| Task-II: Assignment obs + conflict graph integration | | ● | | | | |
| Task-III: Curriculum training (3 → 5 → 8 drones) | | | ● | | | |
| Task-IV: Evaluation vs. 4 baselines | | | | ● | | |
| Task-V: Ablation experiments + failure analysis | | | | | ● | |
| Task-VI: Thesis writing + revision + submission | | | | | | ● |
