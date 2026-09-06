# Samjho: docs/plans/02_experiment_protocol.md

## Yeh cheez kya hai
Experiments chalane ke pakke rules — kya measure karna hai, kitni baar, kaise compare
karna hai. Ek baar fix, phir badalna nahi.

## Iski zaroorat kyun
Agar beech mein rules badalte raho to results compare hi nahi honge, aur thesis
committee bharosa nahi karegi. "Kitne seeds?" — is sawaal ka jawab strong hona chahiye.

## Main baatein

- **Main score — Mission Success Rate (MSR):** kitne % episodes mein saare drones target
  pe pahunche bina kisi takkar ke, time se pehle.

- **Secondary scores:** inter-drone takkar, obstacle takkar, target kitni baar
  reassign hua, path kitna lamba, khatarnak-kareeb kitni der.

- **Evaluation ka tareeqa:** 200 episodes per setting. Eval ke seeds training ke seeds
  se alag aur fixed — sab methods ke liye wahi 200 episodes, taaki fair comparison ho.
  Eval mein policy deterministic (koi random exploration nahi).

- **Seeds:** har setting kam se kam **5 baar** alag seed se chalao. Result = average ±
  spread. Headline comparison (PAH vs fixed-α) ke liye 10 seeds.

- **Methods ki list (5):** B1 plain MAPPO, B2 DA-MAPPO-2D, B3 IGAT-style,
  B4 fixed-α MAPPO, M = hamara (PAH). **B4 vs M sabse important comparison hai.**

- **Grid:** {3, 5, 8 drones} × {kam, medium, zyada obstacles} — har box mein 5 seeds.

- **"PAH jeeta" ka matlab (pakka rule):** Stage 3 (8 drones) + ek aur stage pe —
  MSR(PAH) ≥ MSR(best fixed-α), aur error bars overlap na karein, aur PAH ki takkar
  rate zyada na ho. Plus: seekha hua α **constant nahi** hona chahiye — usko
  time-to-collision ke saath badalna chahiye.

- **Agar PAH nahi jeeta:** to bhi thesis hai — honestly likho, analyze karo kyun.
  Negative result bhi valid result hai.

## Mushkil lafz
- **Metric** = maapne ka paimana (jaise MSR)
- **Confidence interval (CI)** = "asli value is range mein hai" — error bar
- **t-test / p-value** = "ye difference sach hai ya sirf luck?" ka statistical check
- **Deterministic policy** = koi randomness nahi, har baar same action
- **Ablation matrix** = table jismein system ke alag-alag hisse on/off karke test karte hain
