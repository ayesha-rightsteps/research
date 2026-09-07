# handbook/ — sab kuch simple Hinglish mein

Yeh folder Ayesha ke liye hai.

`docs/` aur `code/` mein jo bhi likha jaata hai — plan, design, ya code file — uska
ek **simple Hinglish explanation** yahan banta hai. Bina jargon ke, aaram se samajhne
ke liye.

## Naming rule

Handbook file ka naam = jis file ko explain kar rahe hain uska **wahi naam aur wahi
path**, bas `handbook/` ke andar.

| Asli file | Handbook file |
|-----------|---------------|
| `docs/plans/00_master_plan.md` | `handbook/plans/00_master_plan.md` |
| `docs/research/01_pah_design.md` | `handbook/research/01_pah_design.md` |
| `code/environment/multi_uav_env.py` | `handbook/code/multi_uav_env.md` |

## Har handbook file mein kya hota hai

1. **Yeh cheez kya hai** — ek line
2. **Iski zaroorat kyun** — 2-3 line
3. **Main baatein** — bullet points, simple
4. **Mushkil lafz** — jo bhi technical word aaya, uska matlab

## Alag se

- `glossary.md` — poore project ke saare technical words, ek jagah, simple explanation ke saath

## Abhi tak kya bana hai

### Glossary
| Handbook file | Kis cheez ko samjhata hai |
|---------------|---------------------------|
| `glossary.md` | Poore project ke saare technical words, simple Hinglish mein |

### Synopsis (paper/)
| Handbook file | Kis cheez ko samjhata hai |
|---------------|---------------------------|
| `paper/synopsis.md` | Ayesha ka approved synopsis — simple language mein |

### Plans (plans/)
| Handbook file | Kis cheez ko samjhata hai |
|---------------|---------------------------|
| `plans/00_master_plan.md` | Project ka map — phases, rules, kya karna hai kya nahi |
| `plans/01_roadmap.md` | Phase-by-phase kaam ki detailed list |
| `plans/02_experiment_protocol.md` | Experiments ke pakke rules — seeds, metrics, evaluation |
| `plans/03_engineering_standards.md` | Code likhne ke rules — style, configs, checkpoints |

### Research (research/)
| Handbook file | Kis cheez ko samjhata hai |
|---------------|---------------------------|
| `research/00_problem_formalization.md` | Problem maths ki bhasha mein — MDP, obs, actions, rewards |
| `research/01_pah_design.md` | PAH ka design + reward-hacking problem aur solutions |
| `research/02_assignment_and_conflict.md` | Hungarian assignment + conflict graph — math aur code |
| `research/03_baseline_specs.md` | 4 baselines + papers ke numbers |
| `research/04_open_questions_for_supervisor.md` | Supervisor se poochhne wale 14 sawaal |
| `research/05_supervisor_email_draft.md` | Sir ko bheji jane wali email ka draft |

### Code (code/)
| Handbook file | Kis cheez ko samjhata hai |
|---------------|---------------------------|
| `code/environment/multi_uav_env.md` | Main 2D environment — drones, targets, obstacles, rewards |
| `code/environment/rendering.md` | Visualization — animated window mein episode dekhna |
| `code/environment/watch.md` | Ek click script — seedha run karo aur dekho |
| `code/tests/test_env.md` | 15 unit tests — environment sahi kaam karta hai prove karte hain |
| `code/algorithms/mappo.md` | MAPPO — drones ka AI brain (Actor, Critic, training loop) |
| `code/algorithms/conflict_graph.md` | Conflict graph — kaun se drones takrarne wale hain detect karna |
| `code/algorithms/pah.md` | PAH — thesis ka novel contribution, dynamic α se mission vs safety balance |
| `code/training/train.md` | Training loop — Kaggle pe drones ko sikhane wali script |
| `code/configs/stage1.md` | Stage 1 config — sab settings ka matlab |
| `code/notebooks/kaggle_stage1_training.md` | Kaggle notebook — seedha upload karo aur run karo |

## Kaam kaun karta hai

Jab bhi Claude (Aayat) koi naya `docs/` ya `code/` file banaye ya badle, wo uska
handbook entry bhi banata/update karta hai. Ye rule `../CLAUDE.md` mein likha hai.
