# Handbook — v3_env.py (v3 environment ki ek pakki copy)

Asal file: `code/notebooks/v4/common/v3_env.py`

## Yeh kya hai?

v3 ke environment (drones, targets, obstacles), conflict graph, actor network aur PAH — sab ki **ek hi
copy**, ek file mein. Iska kaam sirf ek hai: v3 ke pehle se trained models ko **bilkul usi code pe**
chalana jis pe woh train huye thay.

## Kyun zaroori thi?

v3 mein yeh code har notebook mein alag se paste hota tha. v4 mein jab bhi v3 ke models check karne hon,
yahi file import hoti hai — koi naya paste nahi.

## Kaise banayi (taaki galti na ho)

- Code **haath se dobara type nahi kiya**. Program ne seedha v3 ke notebooks se nikaala:
  - Conflict graph, environment, actor → `v3/results-table` notebook se (jo pehle hi v3 ke numbers
    reproduce kar chuka tha)
  - PAH → `v3/stage3/var-alpha` notebook se (Stage 2 mein bhi bilkul same settings hain)
- Phir check kiya: is copy ne 5 models pe v3 ke **200 mein se 200 episodes bilkul wahi** nateeje diye.
- 12 Oct ko isi tareeqe se **critic** aur **RolloutBuffer** (advantage ka hisaab) bhi jode, taaki
  advantage-correlation check training ke bilkul asli code se ho. Saare 6 training notebooks ka advantage
  wala code check kiya — sab same hai.

## Naya code jo add kiya (copy ka hissa nahi)

| Function | Kya karta hai |
|---|---|
| `load_checkpoint(path)` | model file se actor aur PAH load karta hai (Fixed-weight MAPPO aur Hand-coded τ-rule MAPPO ki files mein PAH nahi hota) |
| `deterministic_action` | actor ka beech wala (mean) action — evaluation ke liye |
| `stochastic_action` | random action, bilkul training jaisa — fixed seed ke saath, taaki dobara chalane pe same aaye |
| `pah_alpha` | kisi state pe PAH kya α deta, bilkul training ke tareeqe se |
| `load_critic(path, n_drones)` | model file se critic load karta hai (input = saare drones ke observations ek line mein) |

## Zaroori usool

**Is file ki copied classes kabhi edit nahi karni.** Agar v4 mein environment badalna hua, to woh nayi
file mein hoga — taaki v3 ke models hamesha apne asli code pe check hon.
