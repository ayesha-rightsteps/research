# Handbook — common/baselines_v4.py (base paper ke methods)

Asal file: `code/notebooks/v4/common/baselines_v4.py` · Tests: `test_baselines_v4.py` · Plan: `03-base-paper-baselines/PLAN.md`

## Yeh kya hai?
Phase 2 ke liye base paper (DA-MAPPO) ke comparison methods ka code. Paanch methods:

| Method | Kya alag hai | Code kahan |
|---|---|---|
| **MAPPO** | Target shuru mein ek dafa (Hungarian se) milta hai, phir nahi badalta; sab teammates ki position dikhti hai | Phase 1b wala Plain MAPPO agent hi, sirf environment ki setting alag |
| **DA-MAPPO (2D)** | Har step pe naya assignment (base paper ka method) | Wahi Plain MAPPO agent |
| **IPPO** | Critic sirf apni observation dekhta hai — team ki poori halat nahi | `BaselineAgent('ippo')` |
| **RMAPPO** | Actor aur critic mein GRU (yaad-dasht) | `BaselineAgent('rmappo')` |
| **IGAT-style** | Har drone graph attention se conflict-graph padosiyon ko dekhta hai | `BaselineAgent('igat')` |

Environment mein do naye switch (`env_v4.py`) — default wahi jo Phase 1b mein tha:
- `assignment`: har step Hungarian / shuru mein ek dafa / bina Hungarian.
- `teammates`: conflict-graph padosi / sab teammates / koi nahi.

## Tests (7/7 pass) — kya check hota hai
- "Shuru mein ek dafa" wala assignment sach mein kabhi nahi badalta.
- Teammates wale numbers haath se nikale numbers ke barabar.
- IPPO ka critic sirf apni observation leta hai.
- RMAPPO: training ke waqt GRU ko dobara chalane se bilkul wahi probabilities aati hain jo data jama karte waqt aayi thin, aur episode shuru hote hi yaad-dasht zero hoti hai.
- IGAT: jo drone graph mein juda hi nahi, us ke badalne se drone 0 ka action nahi badalta; padosi badle to badalta hai.
- Har method train, save aur load hota hai.

Teen tests ko jaan boojh kar toda hua code diya — teeno ne ghalti pakdi. Yani tests asal mein kaam karte hain.

## Ek imandar baat
RMAPPO baqi methods se ~8–10 guna dheema hai (GRU ko 16 steps peeche tak seekhna padta hai). Barabari ke liye
batch size sab ka same rakha, is liye RMAPPO ke runs lambe hain.

**Tez update (15 Oct 2026):** RMAPPO ke seekhne wale hisse (`_chunk_eval`) ko tez kiya gaya. Hisaab wahi hai,
sirf tareeqa badla:
- Jo layers yaad-dasht nahi rakhtin, wo saare 16 steps par ek saath chalti hain (pehle har step par alag).
- Actor ka GRU aur critic ka GRU ek hi "double" GRU ki tarah ek saath chalte hain.
Test: purane aur naye code ke losses bilkul same aaye, weights mein farq sirf 0.0000002 (computer ki rounding).
Update ~2.6 guna tez hua; poora run ~2 guna tez.

## Mushkil lafz
- **GRU:** network ka hissa jo pichle steps ki baat yaad rakhta hai.
- **Graph attention:** har drone apne padosiyon ko alag ahmiyat deta hai.
- **Chunk:** lagataar 16 steps ka tukda — RMAPPO in tukdon pe seekhta hai.
