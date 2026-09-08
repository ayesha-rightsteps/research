# Handbook — pah.py (Priority Arbitration Head)

## Yeh cheez kya hai?

PAH — yani **Priority Arbitration Head** — thesis ka **novel contribution** hai.

Ek chhota sa brain jo har step pe decide karta hai: "Abhi drone ko **target dhundhna** chahiye ya **takkar bachana** chahiye?"

Yeh decision ek number se hota hai — **α (alpha)** — jo 0.1 se 0.9 ke beech hota hai.

```
α → 0.9  = "mission pe focus karein, abhi safe ho"
α → 0.1  = "rukko, takkar hone wali hai — safety pehle"

r_final = α × r_mission  +  (1 - α) × r_safety
```

## Iski zaroorat kyun?

Purane papers mein α **fix** hoti thi — hamesha 0.5.

Matlab chahe drone safe ho ya bilkul takkar ke qareeb — reward ka formula same rehta tha.

PAH yeh seekhta hai: "Jab situation aisi hai toh α aisa hona chahiye." Yeh **thesis ka main claim** hai.

## Real life se misaal

Sochiye aap car drive kar rahi hain. Normally aap apni manzil ki taraf fast jaayengi. Lekin agar saamne dusri car aa rahi hai — aap pehle brake marti hain, phir manzil ki taraf sochti hain.

PAH bhi yahi karta hai. τ_collision kam hoti hai (danger qarib hai) → α choti hoti hai → safety reward zyada matter karta hai.

## Andar kia kia hai?

### 1. `PAHNormalizer` — inputs ko ek hi range pe laana

PAH ko 3 numbers milte hain. Problem yeh thi ke yeh sab alag-alag ranges mein hote hain:
- τ_collision: 0 se 3.0 seconds
- d_target: 0 se 141 units (world diagonal)
- n_conflict: 0 se N−1 (3 drones: 0, 1, ya 2)

Agar yeh normalize nahi karein toh MLP ek input basically ignore kar deta hai (kyunki baaki bahut badi hain).

`normalize()` function teen numbers lyta hai → sab ko 0 se 1 ke beech le aata hai.

### 2. `PriorityArbitrationHead` (nn.Module) — asli PAH network

```
Input (B, 3) → Linear(3→32) → ReLU → Linear(32→1) → Sigmoid → clip [0.1, 0.9]
```

- `B` = batch size (ek saath kitne samples process ho rahe hain)
- Andar 32 hidden units hain (lightweight — sirf ~130 parameters)
- Sigmoid se output 0 se 1 ke beech aata hai
- Phir clip karte hain 0.1 se 0.9 — matlab mission ya safety kabhi bhi **bilkul** ignore nahi hogi

**`compute_prior_loss()`** — ek chhoti si "pull": alpha ko 0.5 ke qareeb rakhti hai training mein.
Agar yeh nahi hota toh PAH seekh sakta tha ke "hamesha 0.9 do" ya "hamesha 0.1 do" — yeh reward hacking hai.

### 3. `PAHWrapper` — PAH ko environment se connect karta hai

**`compute_alpha()`** — rollout mein call hota hai (bina gradient ke, fast)
- Numpy arrays leta hai
- PyTorch tensor banata hai, PAH se alpha nikalata hai
- Alpha numpy mein return karta hai
- Diagnostic log mein save karta hai (thesis plots ke liye)

**`combine_rewards()`** — alpha use karke reward combine karta hai
```
r = α × r_mission + (1-α) × r_safety
```

**`compute_alpha_gradient()`** — PPO update mein call hota hai (gradient chahiye, PAH seekhta hai)

**`get_diagnostics()`** — thesis figures banane ke liye data: α histogram, α vs τ scatter, etc.

### 4. `split_reward()` — environment se do alag rewards

Environment pehle ek combined reward deta tha. Ab:
- `r_mission` — drone target se kitna door hai (negative distance)
- `r_safety` — koi takkar hua? (-1.0) ya safe (0.0)

Yeh dono alag log hote hain toh thesis mein hum show kar sakte hain: "mission reward aisa tha, safety reward aisa tha."

## PAH kaise train hota hai?

PAH **MAPPO ke saath** train hota hai — alag nahi. Jab PPO update hota hai:
1. Old rollout mein stored `r_mission` aur `r_safety` nikaalein
2. Current PAH se alpha recompute karein (with gradients)
3. `r = α × r_mission + (1-α) × r_safety` banayein
4. GAE chalayein, PPO loss banayein, prior loss add karein
5. Ek hi optimizer mein actor + PAH dono update ho jaate hain

## Files ka connection

```
multi_uav_env.py
   ↓  r_mission, r_safety (info dict mein)
pah.py (PAHWrapper)
   ↓  compute_alpha() → alpha
   ↓  combine_rewards() → r_combined
mappo.py (MAPPO update)
   ↓  compute_alpha_gradient() → prior_loss
   → actor + PAH jointly updated
```

## Mushkil lafz

| Lafz | Matlab |
|------|--------|
| **PAH** | Priority Arbitration Head — alpha decide karne wala chhota network |
| **α (alpha)** | Mission vs safety ka balance: 0.9 = mission, 0.1 = safety |
| **Prior regularizer** | Chhoti penalty jo alpha ko extreme values se rokthi hai |
| **Normalize** | Numbers ko same range mein laana (0 se 1) |
| **Batch (B)** | Ek saath kitne examples process ho rahe hain |
| **Gradient** | Woh math jo network ko seekhne mein madad karta hai |
| **No-grad** | Rollout mein gradient nahi chahiye — sirf value chahiye |
| **Prior coef** | Alpha ke regularizer ka strength — kitni zyada pull toward 0.5 |
| **Reward hacking** | Jab PAH seekhe ke ek extreme alpha se zyada reward milta hai aur wahi karna shuru kar de |
| **Fixed-α baseline** | Comparison model jahan alpha 0.5 par fix hai — PAH ko justify karta hai |
