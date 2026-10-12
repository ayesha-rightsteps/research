# Handbook — mappo_v4.py (v4 ka naya agent)

Asal file: `code/notebooks/v4/common/mappo_v4.py` · Tests: `test_mappo_v4.py`

## Yeh kya hai?

v3 ka MAPPO agent, ek bade badlav ke saath: **mission aur safety ke liye alag value heads** (critic ke do
"dimaag" — ek batata hai mission kitna achha chal raha hai, doosra safety). Isse safety ka signal sach mein
safety ka hota hai, aur α ka asar padta hai. (v3 mein ek hi critic tha, is liye mixing plain MAPPO ban jaati
thi.)

Ek hi class, settings se paanch methods banti hain:

| Method | Critic | Drone ka signal |
|---|---|---|
| Plain MAPPO | ek head | normal combined advantage |
| Fixed-weight MAPPO | do heads | α = 0.5 se mix |
| Hand-coded τ-rule MAPPO | do heads | α formula se |
| MAPPO + PAH | do heads | α PAH se |
| MAPPO + PAH, Hungarian off | do heads | α PAH se, assignment fixed |

## Galti se bachne ke tests (5/5 pass)

- GAE ka hisaab haath se kiye 5-step example se milta hai.
- **Sab se zaroori:** agar naye agent ko v3 jaisa set karein (ek critic, mixing), to woh ek fixed batch pe
  v3 agent jaisa **bilkul wahi update** deta hai (saare weights same). Matlab PPO ka baaki saara code
  unchanged hai.
- Do heads wale critic ka loss same batch pe ghatta hai; har method save/load ho kar same action deta hai.

Tests ne do bugs pehle hi pakad liye (inference-only Actor, ek missing import) — dono theek.

## PAH ka fix (13 Oct 2026) — "risk-learning PAH"

Pehla PAH apna α policy ke loss se seekhta tha, aur us loss ne use **khatre mein safety ko nazarandaz** karna sikha
diya (khatre mein uski correction poori had tak mission ki taraf thi). Naya PAH:
- wahi 3 inputs aur wahi chhota network;
- seekhta hai ke **is situation mein aage kitna safety ka nuksaan aane wala hai** (asli tajurbe se);
- α = zyada khatra → kam (safety pehle), kam khatra → zyada (mission pehle);
- policy ke loss se use koi gradient nahi milta — is liye use safety ko nazarandaz karne ka koi faayda nahi.
Tests: actor loss se PAH tak zero gradient; khatre mein α kam seekhta hai; chhote run mein α khatre mein 0.13, safe mein 0.73.
