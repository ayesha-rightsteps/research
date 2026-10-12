# Handbook — diag.py (episode chalate waqt sab kuch record karna)

Asal file: `code/notebooks/v4/00-diagnostics/diag.py`

## Yeh kya hai?

Ek function, `run_episode()`, jo ek episode chalata hai aur har step pe yeh cheezein note karta hai:

| Kya record hota hai | Matlab |
|---|---|
| Safety reward ON tha ya nahi | kya koi drone kisi doosre drone ya obstacle se 9 units ke andar tha |
| Kis wajah se ON tha | doosra drone paas tha, ya obstacle |
| Conflict graph ne conflict dikhaya ya nahi | yahi PAH ka τ input banata hai |
| α kitna tha | Fixed-weight MAPPO = hamesha 0.5, Hand-coded τ-rule MAPPO = τ wala formula, MAPPO + PAH = trained PAH |
| Loss-of-separation | kitne drone-jore 9 units se kam doori pe thay (near-miss) |
| Active edges | conflict graph mein kitne jore takraav ke raaste pe thay |
| Collision ki type | agar takkar hui: drone se ya obstacle se, aur goal ke paas ya raaste mein |

## Zaroori baat

Yeh environment ko **badalta nahi** — sirf har step ke baad environment ki halat padhta hai.

Ek andar ka check bhi hai: environment ka safety reward tab hi ON hona chahiye jab koi drone ya obstacle
9 units ke andar ho. Agar yeh hisaab kabhi na mile, to code wahin ruk jata hai — taaki galat numbers
chupke se na nikal jayein.

**"9 units" kyun?** Yeh danger radius hai = 3 × collision radius. v3 ka reward aur conflict graph dono
yahi radius use karte hain, isliye diagnostics mein bhi yahi rakha.

## Naya function (12 Oct): `advantage_batch()`

Training jaisa ek **batch** banata hai — 512 steps, random (stochastic) actions, aur success bonus 20 (bilkul
training jaisa) — phir v3 ke asli code se mission advantage aur safety advantage nikaalta hai, aur naapta hai:
- dono advantages aapas mein kitne milte hain (aur ulte to nahi),
- normalize se pehle dono kitne phaile hain,
- drone ko jo signal milta hai woh α = 0.5 wale signal se kitna alag hai (direction aur size alag-alag),
- woh signal plain MAPPO ke signal jaisa hai ya nahi.

`make_env` mein ab `success_bonus` choose kar sakte hain: purane checks ke liye 0 (nateeje pe asar nahi),
advantage check ke liye 20 (kyunki wahan reward bilkul training jaisa chahiye).
