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
| world_size | **500** | 500×500 ka map (500m×500m, 1 unit=1m) — pehle 100 tha |
| max_speed | 5.0 | Drone ek step mein max 5 units move kar sakta hai |
| max_steps | 300 | 300 steps ke baad episode band — time limit |
| target_radius | **25.0** | Itne paas aao toh target "reached" — training curriculum value (5% of world); final evaluation ke liye 5.0 tak tighten karna hai baad mein |
| collision_radius | 3.0 | Itne paas aao toh collision |
| **success_bonus** | **20.0** | Target pe pahunchne pe ek baar ka bada +reward — iske bina Stage 1 3000+ episodes tak 0% success raha (2026-09-15 add) |
| **use_hungarian** | **true** | Ablation switch — `false` karke test karo ki assignment mechanism zaroori hai ya nahi |

### mappo (AI brain settings)
| Setting | Value | Matlab |
|---------|-------|--------|
| lr | 0.0003 | Learning rate — kitna tezi se seekhe |
| gamma | 0.99 | Future rewards ki importance (0.99 = zyada important) |
| lam | 0.95 | GAE smoothing |
| clip_eps | 0.2 | PPO clip — update zyada bada mat hone do |
| ent_coef | **0.003** | Exploration bonus — 0.01 se shuru hui, 0.02 try ki (bahut zyada nikli, entropy badhne lagi), 0.003 pe settle hui |
| n_epochs | 10 | Ek rollout se 10 baar seekhe |
| batch_size | 64 | Ek baar mein 64 samples update karein |

### training
| Setting | Value | Matlab |
|---------|-------|--------|
| total_episodes | **5000** | Itne episodes tak train karein — pehle 3000 tha |
| rollout_steps | 512 | Har update se pehle itne steps collect karein |
| eval_every | 100 | Har 100 episodes mein progress check |
| eval_episodes | 20 | Evaluation mein 20 episodes chalayein |
| save_every | **500** | Har 500 episodes mein checkpoint save — pehle 200 tha |
| seed | 42 | Random seed — results reproducible hone ke liye |

**Yeh saari values validated hain** — `code/notebooks/v3/v3-output/history.json`
mein isi config se 100% success, 0% collision, 5000 episodes tak, mila hai.
Lekin dekho `sessions/2026-09-15.md` Part 4/6 — itna perfect result khud ek
sawaal khada karta hai (task bahut aasaan to nahi?), ablation check pending hai.
