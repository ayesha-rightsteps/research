# Future Work Table

---

## Future Work from Each Paper

| Paper | What the authors said | What is actually missing (honest gap) |
|---|---|---|
| **Paper 1** Improved D3QN | Test in more complex dynamic environments with more obstacles | Extend to multi-drone coordination — single drone is the biggest limitation |
| | Reduce computational cost of training | Add continuous action space — 8 discrete directions is not realistic flight |
| | Test with real UAV hardware | Test at larger map scales, not just a small grid |
| **Paper 2** TANet-TD3 | Scale to more than 5 UAVs | No mechanism exists to scale — needs a fundamentally new approach (like mean field) |
| | Test with dynamic targets, not just dynamic obstacles | 2D only — needs 3D extension for real deployment |
| | Improve communication between drones | No inter-drone communication is modeled at all |
| **Paper 3** Dynamic Reward DQN | Parallelize DQN training to cut the 456-second compute time | Add ablation study — test DQN with sparse reward to isolate what the dynamic reward actually contributes |
| | Extend to multi-agent drone systems | Dynamic obstacles — the entire paper uses static obstacles only |
| | | Compare against modern DRL baselines (PPO, DDPG) not just Q-learning and PSO |
| **Paper 4** PO-WMFDDPG | Extend to 3D environments | Train from the start with moving NFZs, not just test on them after static training |
| | Handle heterogeneous swarms (mixed drone types) | Add target assignment — targets are pre-assigned, no allocation logic exists |
| | Test with constrained communication (latency, packet loss) | Hardware validation — not even a partial physical test is done |

---

## Combined Future Work — What Your Research Can Build On

| Research Gap | Which Papers It Combines | Difficulty | Impact |
|---|---|---|---|
| Take Paper 4's swarm framework into 3D space | Paper 4 + Paper 3 | Medium | High — no swarm paper works in 3D |
| Add dynamic obstacles to Paper 4's 80-drone swarm | Paper 4 + Paper 1 | Medium | High — Paper 4's moving NFZ test is weak |
| Replace Paper 4's reward with Paper 3's d3/(d1+d2) formula | Paper 4 + Paper 3 | Low | Medium — could improve convergence speed |
| Add target assignment to a swarm (Paper 2's TANet inside Paper 4) | Paper 4 + Paper 2 | High | Very High — no paper does both swarm + assignment |
| Multi-UAV path planning in 3D with dynamic obstacles (10–20 drones) | Paper 1 + Paper 3 | Medium | High — fills the exact gap between Papers 1 and 3 |
| Scale Paper 2's TANet-TD3 from 5 to 20+ drones using mean field | Paper 2 + Paper 4 | High | Very High — most complete real-world scenario |

---

## Recommended Research Direction

**Most achievable for a Masters project:**

> Extend PO-WMFDDPG (Paper 4) to a 3D environment with dynamic obstacles, replacing the reward function with Paper 3's d3/(d1+d2) design.

- Start from Paper 4's proven codebase and framework
- Add altitude (z-axis) to the state and action space
- Replace static NFZs with moving ones during training (not just testing)
- Use Paper 3's dense reward formula instead of the manual r_task

This is one clear thesis: **"Does the mean-field + attention approach still scale when we move from 2D to 3D and add dynamic threats?"**

**Most impactful but harder:**

> Add Paper 2's target assignment mechanism into Paper 4's swarm, creating a system that simultaneously assigns targets to 20+ drones and plans their paths in a shared environment.

This has never been done at scale and would be a genuinely new contribution.
