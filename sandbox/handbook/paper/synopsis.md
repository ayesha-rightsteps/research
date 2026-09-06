# Samjho: Ayesha ka Synopsis (docs/paper/)

## Yeh cheez kya hai
Approved thesis proposal. Isme likha hai kya research karni hai — yeh **source of
truth** hai, sab kuch isi se aata hai.

## Thesis ka title
"Multi-Agent Proximal Policy Optimization for Joint Dynamic Target Assignment and
Collision Avoidance in UAV Systems"

Seedha matlab: **ek hi AI system jo ek saath (a) drones ko targets baante aur
(b) unhe takrane se bachaye — 2D duniya mein, 3 se 8 drones.**

## Problem kya hai
- Multi-drone missions (search & rescue, surveillance) mein do cheezein chahiye:
  target assignment + collision avoidance
- Purani research inhe **alag-alag** solve karti hai → conflicting decisions,
  raaste overlap, mission slow/incomplete
- Jab drone target pe focus kare to takkar ka risk; jab takkar se bache to target
  chhoot jaaye — ye dono jude hue hain

## Solution kya propose kiya
- **Unified MAPPO framework** — har drone ki observation mein dono cheezein encode:
  - Hungarian algorithm se assigned target (har step update)
  - Conflict graph se kaunse drones kareeb/khatarnak
- **Priority Arbitration Head (PAH)** — naya chhota network jo har step `α` deta hai
  (mission vs safety ka balance). Purane papers `α` fix rakhte hain; PAH seekhta hai.

## Kaise test karenge
- 2D simulation, curriculum learning (aasaan → mushkil): 3 static → 5 moving →
  8 dynamic → unseen sizes
- 4 baselines se compare — sabse important: **fixed-α vs learned-α (PAH)**
- Main score: mission success rate (sab target pe + zero takkar + time limit)
- Ablation: har hissa (conflict graph, Hungarian, PAH) nikaal ke dekho kitna zaroori

## Supervisory committee
- Dr. Faisal Rehman (Supervisor), Mr. Ehzaz Mustafa (Co-supervisor),
  Dr. Sardar Khaliq uz Zaman, Dr. Nuhman ul Haq

## Ek baat dhyaan se
Synopsis "PyBullet simulation" kehta hai. Hum custom 2D env use karenge (PyBullet 3D
ke liye hai, hamari research 2D). Ye change supervisor se **likhit mein OK** karana hai
— dekho `research/04_open_questions_for_supervisor.md`.

## Mushkil lafz
- **UAV** = Unmanned Aerial Vehicle = drone
- **MAPPO** = Multi-Agent PPO, hamara main AI algorithm
- **Target assignment** = kaun sa drone kaunsa target le
- **Collision avoidance** = takkar se bachna
- **Curriculum learning** = aasaan se mushkil ki taraf training
- **Ablation** = ek hissa nikaal ke dekhna wo kitna zaroori tha
- **α (alpha)** = mission vs safety balance knob (PAH ka output)
- Baaki `handbook/glossary.md` mein
