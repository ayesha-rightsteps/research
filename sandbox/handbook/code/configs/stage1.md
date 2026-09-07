# Handbook — stage1.yaml

## Yeh file kia hai?
Stage 1 training ki **sab settings ek jagah** — environment, MAPPO, training loop.
Koi bhi number change karna ho toh yahan aao, code mein mat jaao.

## Settings ka matlab

### env (environment settings)
| Setting | Value | Matlab |
|---------|-------|--------|
| n_drones | 3 | 3 drones (Stage 1 mein sabse kam) |
| n_obstacles | 0 | Stage 1 mein koi obstacles nahi — easy start |
| world_size | 100 | 100×100 ka map |
| max_speed | 5.0 | Drone ek step mein max 5 units move kar sakta hai |
| max_steps | 300 | 300 steps ke baad episode band — time limit |
| target_radius | 5.0 | Itne paas aao toh target "reached" |
| collision_radius | 3.0 | Itne paas aao toh collision |

### mappo (AI brain settings)
| Setting | Value | Matlab |
|---------|-------|--------|
| lr | 0.0003 | Learning rate — kitna tezi se seekhe |
| gamma | 0.99 | Future rewards ki importance (0.99 = zyada important) |
| lam | 0.95 | GAE smoothing |
| clip_eps | 0.2 | PPO clip — update zyada bada mat hone do |
| n_epochs | 10 | Ek rollout se 10 baar seekhe |
| batch_size | 64 | Ek baar mein 64 samples update karo |

### training
| Setting | Value | Matlab |
|---------|-------|--------|
| total_episodes | 3000 | Itne episodes tak train karo |
| rollout_steps | 512 | Har update se pehle itne steps collect karo |
| eval_every | 100 | Har 100 episodes mein progress check |
| eval_episodes | 20 | Evaluation mein 20 episodes chalao |
| save_every | 200 | Har 200 episodes mein checkpoint save |
| seed | 42 | Random seed — results reproducible hone ke liye |
