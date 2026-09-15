# Handbook — stage2.yaml

## Yeh file kia hai?
Stage 2 training ki sab settings — Stage 1 se zyada mushkil task hai: zyada drones,
moving targets, obstacles, aur conflict graph ON. PAH abhi bhi OFF hai — pehle plain
MAPPO se confirm karo ki base kaam karta hai, phir PAH wala run.

## Stage 1 se kia badla?

| Setting | Stage 1 | Stage 2 | Kyun |
|---------|---------|---------|------|
| n_drones | 3 | **5** | Thesis ka Stage 2 requirement |
| n_obstacles | 0 | **5** | Thodi mushkil — Poisson-disk se place honge |
| target_speed | — | **1.0 m/step** | Moving targets — drones ko moving cheez follow karni hai |
| max_steps | 300 | **500** | Zyada time chahiye — 5 drones + obstacles + moving targets |
| total_episodes | 5000 | **8000** | Harder task = zyada training |
| use_conflict_graph | false (obs=10) | **true (obs=30)** | Conflict graph ON — har drone ko pata hoga kaunse drones collision course pe hain |
| use_pah | false | **false** | Abhi bhi PAH OFF — base confirm karo pehle |

## Naya concept: Moving Targets

Stage 1 mein targets static the (ekdum khade). Stage 2 mein targets dheeray dheeray
hilt hain — har step 1 m/step. Agar wall se takra jaayein, bounce kar ke wapas aatein
hain (bilkul ball ki tarah). Drones ko continuously target ki taraf adjust karna padega.

## Naya concept: Conflict Graph (ON)

Stage 1 mein har drone sirf apna position, velocity, aur target dekhta tha (obs=10).
Stage 2 mein 20 extra numbers aatay hain — kaunse drones collision course pe hain,
kab takra sakte hain, kahan hain. Isi ki wajah se PAH kaam kar sakta hai (usse pata
hoga danger hai ya nahi). obs_dim: 10 → **30**.

## Settings ka matlab

### env
| Setting | Value | Matlab |
|---------|-------|--------|
| n_drones | 5 | Paanch drones |
| n_obstacles | 5 | Paanch static obstacles — Poisson-disk se place, drones/targets se door |
| world_size | 500.0 | Same 500×500m map |
| max_steps | 500 | Stage 1 se 200 steps zyada |
| target_radius | 25.0 | Same training curriculum value — baad mein tighten karenge |
| success_bonus | 20.0 | Same — zaruri hai positive signal ke liye |
| target_speed | 1.0 | Target ki speed — drone ki speed (5) ka 20% |
| use_conflict_graph | true | Conflict graph observations ON |

### mappo
Sab values Stage 1 jaisi — validated hain, change mat karo jab tak koi diagnosed
reason na ho.
| Setting | Value |
|---------|-------|
| ent_coef | 0.003 |
| lr | 0.0003 |
| clip_eps | 0.2 |

### training
| Setting | Value |
|---------|-------|
| total_episodes | 8000 |
| eval_every | 100 |
| save_every | 500 |

## Run kaise karein

Notebook: `code/notebooks/stage2/kaggle_stage2_plain.ipynb`
Output: `code/notebooks/stage2/output-stage-2-plain/`

## Agar training fail ho

Manish ka plan: pehle plain MAPPO chalao, phir PAH ON. Agar yeh run fail ho:
1. **Success 0% kaafi episodes tak** → ent_coef check karo (Stage 1 wala v3 failure same tha)
2. **Collision bahut zyada** → target_speed 0.5 kar do (aasaan karo)
3. **Converge hi na ho** → total_episodes badhao ya target_radius temporarily
   badhao (Stage 1 jitna mushkil hai to aasaan nahi hoga yeh)
