# Samjho: docs/plans/03_engineering_standards.md

## Yeh cheez kya hai
Code likhne ke rules — kaise organize karna, kaise test karna, kaise save karna, taaki
har experiment dobara chalaya ja sake aur code readable rahe.

## Iski zaroorat kyun
Research code aksar messy ho jaata hai. Phir 3 mahine baad yaad nahi rehta kaunsa
result kis setting se aaya. Ye rules usse bachate hain.

## Main baatein

- **Python 3.10 ya 3.11.** Ek virtualenv. `requirements.txt` mein exact versions
  (`torch==2.x.x`, sirf `torch` nahi).

- **Config files (YAML):** har experiment ki saari settings ek `.yaml` file mein.
  Code ke andar koi number hardcode nahi. Seed bhi config mein.

- **Determinism:** same seed → same result. Python, numpy, torch — sabke seed set karo.
  Environment bhi seedable ho (test se pakka karo).

- **Testing (pytest):** environment ke liye zaroori tests — position update, collision
  detection, target-reached, reward ka sign (progress → +, takkar → bada −), same seed →
  same episode. Har training run se pehle tests green hone chahiye.

- **Logging (TensorBoard):** reward, episode length, losses, entropy — sab log karo.
  Full model ke liye α ka histogram bhi. Har run ke saath `meta.json` — git commit,
  config, seed, package versions.

- **Checkpointing:** har ~30 min training save karo (Kaggle session expire hoti hai).
  Training resume ho sakni chahiye checkpoint se.

- **Code style:** `black` se format, `ruff` se lint. Har function pe docstring
  (kya karta hai, input/output shapes). Comments "kyun" batayein "kya" nahi. Simple
  code — Ayesha ko har line samajh aani chahiye.

- **Git:** `results/` folder git mein nahi (bade files). Model weights git mein nahi —
  Kaggle/Drive pe, index file mein location. **Koi commit/push bina Manish ke kahe.**

- **Kaggle:** code GitHub se clone karo notebook mein, GPU on karo, train karo,
  `/kaggle/working/` mein checkpoint, phir download.

## Mushkil lafz
- **Virtualenv** = project ka apna alag Python + libraries ka dabba
- **YAML** = settings likhne ka simple text format
- **Determinism** = "har baar same input → same output"
- **pytest** = Python ka testing tool
- **Linting** = code mein galtiyan/bad style automatically dhoondhna
- **Checkpoint** = training ke beech model ko save karna
- **meta.json** = ek run ki poori "birth certificate" (commit, seed, versions)
- **Entropy (training mein)** = policy kitni "random/exploring" hai; dheere kam hoti hai
