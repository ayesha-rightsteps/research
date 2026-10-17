# Handbook — 04-base-paper-experiments/compare_papers.py (base papers ke saath comparison graphs)

Asal file: `code/notebooks/v4/04-base-paper-experiments/compare_papers.py` (17 Oct 2026). Chalane ke liye: `python compare_papers.py`.

Ye hamare Phase 3 natije base papers ke **apne table numbers** ke saath dikhata hai. Ye numbers PDF se khud padh kar
code mein likhe gaye hain:
- DA-MAPPO paper: Table IV (static), Table V (dynamic), Table IX (noise)
- IGAT-MARL paper: Table 1 (edges, 3 se 10 drones)

| Graph | Kya milaya |
|---|---|
| p3_cmp1_density | Obstacles 30/40/50 par success: paper vs hamara Stage 3. Dono mein sab girte hain |
| p3_cmp2_static_dynamic | Chalte minus ruke targets: paper mein manfi, hamare yahan musbat. Wajah: "dynamic" ka matlab alag hai |
| p3_cmp3_edges | Drones barhne par edges: dono mein barhte hain (scale alag hai) |
| p3_cmp4_noise | Noise se kitna gira: dono mein thoda sa |

**Dhyaan rakhein:** papers ke numbers ke saath koi CI nahi hai (unhon ne di hi nahi). Simulator aur drones ki tadaad
alag hain, is liye sirf rukh (trend) milaiye, seedha number nahi.

Aasaan report (graphs ke saath): `output/phase3_report.html`.
