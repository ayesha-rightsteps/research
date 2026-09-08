# Handbook — train.py

## Yeh file kia hai?
**Main training loop** — yeh file drones ko actually sikhati hai.
Yahan sab kuch ek saath aata hai: environment + MAPPO + config.

## Real life mein soch ke samjhein
Sochiye ek student 3000 exam papers practice karta hai:
- Har 512 questions ke baad teacher check karta hai (rollout → update)
- Har 100 papers ke baad progress test hota hai (evaluation)
- Har 200 papers ke baad progress save hoti hai (checkpoint)
- End mein final result aata hai

Drones ke saath bilkul yahi hota hai.

## Andar kia kia hai?

### `load_config()` — settings load karta hai
`stage1.yaml` ya `stage2.yaml` se sab numbers padhta hai — kitne drones, PAH ON/OFF, etc.

### `make_pah_wrapper()` — PAH banata hai (agar config mein ON ho)

Config mein `pah.enabled: true` likha ho toh PAH automatically ban jaata hai.
Agar `pah.enabled: false` ya pah section nahi hai → PAH nahi banta (Stage 1 waala behavior).

```yaml
# Stage 2 config mein yeh hoga:
pah:
  enabled: true
  hidden_dim: 32
  prior_coef: 0.01
```

### `collect_rollout()` — experience collect karta hai
512 steps environment mein play karein. Jo kuch hua — actions, rewards — sab buffer mein store karein.

**Jab PAH ON ho:**
- Har step pe environment se `pah_inputs` milte hain (tau, d_target, n_conflict)
- PAH se alpha compute hota hai (bina gradient ke — fast)
- `r_combined = alpha × r_mission + (1-alpha) × r_safety` → yeh reward store hoti hai
- r_mission, r_safety, pah_inputs bhi alag store hote hain (training ke liye zaroor)

### `evaluate()` — progress check karta hai
20 fresh episodes chalayein (bina training ke) aur dekhein:
- Kitne episodes mein sare drones target tak pahunche? → **Success Rate**
- Kitne episodes mein collision hua? → **Collision Rate**

### `train()` — main loop
```
Repeat jab tak episodes poore na ho jayein:
  1. 512 steps khelein (collect_rollout) — PAH bhi use hota hai agar ON ho
  2. MAPPO update karein — actor + critic + PAH (ek saath)
  3. Har 100 episodes: evaluate + print karein
  4. Har 200 episodes: model save karein (checkpoint — PAH weights bhi!)
End mein: final model save karein
```

### Kia track hota hai training mein?
```
episode        → kitna hua
success_rate   → main metric
collision_rate → collision rate
actor_loss     → actor ka loss
critic_loss    → critic ka loss
entropy        → kitni exploration ho rahi hai
pah_loss       → PAH ka loss (sirf Stage 2+ mein — warna empty)
alpha_mean     → average alpha us rollout mein (sirf Stage 2+ mein)
```

`alpha_mean` track karna important hai thesis ke liye — agar alpha hamesha 0.9 ya 0.1 par ho, matlab PAH kuch sikh nahi raha (reward hacking).

### Screen pe kia dikhega training ke waqt?
```
Ep  100/3000 | Success: 12.5% | Collision: 45.0% | ALoss: -0.012 | ...
Ep  200/3000 | Success: 28.0% | Collision: 30.0% | ALoss: -0.008 | ...
...
Ep 3000/3000 | Success: 85.0% | Collision:  5.0% | ALoss: -0.002 | ...
```
Success rate upar aani chahiye, collision rate neeche — yeh seekhne ki nishaani hai.

## Config file kia hoti hai?
Sab settings wahan hain — yahan kuch hardcode nahi:

| Config | Use |
|--------|-----|
| `stage1.yaml` | 3 drones, koi obstacles nahi, PAH off — Stage 1 |
| `stage2.yaml` | 5 drones, obstacles hain, PAH on — Stage 2 (abhi banana hai) |

## Kaggle pe kaise chalayein?
Kaggle notebook (`kaggle_stage1_training.ipynb`) mein sab instructions hain — copy paste karke cells run karein.

## Hard words
- **Rollout:** ek baar environment mein khelna — experience collect karna
- **Checkpoint:** training ka snapshot — agar kuch ho jaye toh yahan se restart kar sako
- **Hyperparameter:** settings jo training se pehle set karte hain (learning rate, etc.)
- **Success Rate:** kitne % episodes mein sare drones target pahunche — main metric
- **Collision Rate:** kitne % episodes mein koi takkar hui
