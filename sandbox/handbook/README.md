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

| Handbook file | Kis cheez ko samjhata hai |
|---------------|---------------------------|
| `glossary.md` | Saare technical words |
| `paper/synopsis.md` | Ayesha ka approved synopsis |
| `plans/00_master_plan.md` | Project ka map — phases + rules |
| `plans/01_roadmap.md` | Phase-by-phase kaam ki list |
| `plans/02_experiment_protocol.md` | Experiments ke pakke rules |
| `plans/03_engineering_standards.md` | Code likhne ke rules |
| `research/00_problem_formalization.md` | Problem maths ki bhasha mein |
| `research/01_pah_design.md` | PAH ka design + reward-hacking problem |
| `research/02_assignment_and_conflict.md` | Hungarian + conflict graph |
| `research/03_baseline_specs.md` | 4 baselines + papers ke numbers |
| `research/04_open_questions_for_supervisor.md` | Supervisor se poochhne wale 14 sawaal |
| `code/...` | (abhi code nahi likha — jab likhenge tab yahan aayega) |

## Kaam kaun karta hai

Jab bhi Claude (Aayat) koi naya `docs/` ya `code/` file banaye ya badle, wo uska
handbook entry bhi banata/update karta hai. Ye rule `../CLAUDE.md` mein likha hai.
