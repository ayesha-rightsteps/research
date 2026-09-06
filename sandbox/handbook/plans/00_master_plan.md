# Samjho: docs/plans/00_master_plan.md

## Yeh cheez kya hai
Poore project ka "map" — hum kaam kaise karenge, kis order mein, aur kya rules hain.

## Iski zaroorat kyun
Research bikhri hui na ho. Sabko pata ho abhi kaunse phase mein hain, agla kadam kya
hai, aur kya galtiyan nahi karni.

## Main baatein

- **Ek line ka claim jo hum test kar rahe hain:** "α ko seekhna (PAH se) α ko fix rakhne
  se behtar coordination deta hai." Bas yehi prove/disprove karna hai. Jo kaam isse
  connected nahi, wo out of scope.

- **7 principles:**
  1. Pehle design likho (formulation), phir code
  2. Pehle purana result reproduce karo, phir naya banao
  3. Environment ko test karke pakka karo, phir RL lagao
  4. Ek baar mein ek cheez badlo, hamesha baseline ke saath compare karo
  5. Har result kam se kam 5 seeds pe (warna wo result nahi hai)
  6. Scope tight — sirf 2D, max 8 drones, koi extra feature nahi
  7. Session log mein sach likho — fail hue experiments bhi

- **7 phases:** P0 design likhna → P1 environment banana → P2 MAPPO banana →
  P3 assignment + conflict graph jodna → P4 PAH banana → P5 saare experiments +
  evaluation → P6 thesis likhna

- **MUST karna:** supervisor se P0 pe sign-off, har experiment ka config + seed + log,
  fixed-α baseline sweep, session log har din

- **MUST NOT karna:** PyBullet, single-seed result, PAH ka core idea badalna bina
  poochhe, synopsis se chupke deviate karna, fake results, git push bina poochhe

## Mushkil lafz
- **Formulation** = design ko likhit roop mein daalna (formulas ke saath), code se pehle
- **Baseline** = comparison ke liye rakha gaya purana/simple system
- **Seed** = random ka starting point; fix karo taaki experiment repeat ho sake
- **Scope** = project ki hadd; "scope creep" = chupke se kaam badhta jaana (bura)
- **Ablation** = ek hissa nikaal ke dekhna wo kitna zaroori tha
- Baaki `handbook/glossary.md` mein
