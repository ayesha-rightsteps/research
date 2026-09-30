# Handbook — 08_literature_comparison_artifact.md

## Yeh cheez kya hai?

Ek presentation page (link ke through khulta hai, koi file nahi) jo
`07_literature_comparison.md` ka hi content hai, lekin visual charts ke
saath — Manish ne supervisor ko dikhane ke liye banwaya tha.

**Link:** https://claude.ai/artifact/GQTD3VBaacCbfNuvEh3cB6

## Isme kya hai

- Headline numbers (Stage 2 91%, Stage 3 74.8%, DA-MAPPO ka ablation 0%)
- Ek sorted bar chart — saare methods (paper ke aur hamare) ek hi scale pe
- Ek "effect size" chart — DA-MAPPO ka 99-point drop vs hamara sirf
  0.2-point fark, side by side, taaki fark seedha dikhe
- Teacher ko bolne ke liye ready script

## Kyun banaya

Manish ne kaha tha table-only comparison "dull" lag raha tha presentation
ke liye. Charts se fark seedha dikh jaata hai, calculation karni nahi
padti.

## Ek zaroori sawal jo poocha gaya tha: DA-MAPPO hi kyun compare kiya?

Sirf topic same hone ki wajah se nahi — 5 concrete wajah:
1. Same problem (assignment + collision avoidance dono saath)
2. Same algorithm family (MAPPO)
3. Same assignment mechanism (Hungarian algorithm)
4. Same metric (success/collision rate)
5. **DA-MAPPO hi hamare apne experiment protocol ka B2 baseline hai** —
   `docs/plans/02_experiment_protocol.md` mein already likha hua tha

Matlab ye koi bahar ka reference nahi, hamara apna planned baseline hai.
