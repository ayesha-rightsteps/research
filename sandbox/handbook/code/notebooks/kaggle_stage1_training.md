# Handbook — kaggle_stage1_training.ipynb

## Yeh file kia hai?
Kaggle pe seedha upload karne wali **notebook** — isme sab kuch ek jagah hai.
Koi GitHub nahi chahiye, koi alag files nahi — bas yeh ek file upload karein aur run karein.

## Kaggle pe kaise use karein?

1. kaggle.com kholo → **"Create"** → **"New Notebook"**
2. Top right → **"File"** → **"Import Notebook"** → yeh `.ipynb` file upload karein
3. Right side panel → **"Session Options"** → **"Accelerator"** → **GPU T4 x2** select karein
4. **"Run All"** dabao

Bus! Training shuru ho jayegi. 1-2 ghante lagenge.

## 6 cells mein kia kia hai?

| Cell | Kia karta hai |
|------|--------------|
| Cell 1 | Libraries install + GPU check |
| Cell 2 | Environment (2D duniya — drones, targets) |
| Cell 3 | MAPPO (Actor, Critic, training logic) |
| Cell 4 | Setup — config numbers, environment + agent banayein |
| Cell 5 | **Asli training loop** — yahan drones seekhte hain |
| Cell 6 | Results plot — success rate ka graph |

## Screen pe kia dikhega?
```
Episode | Success  | Collision | A-Loss   | Time
    100 |    5.0%  |    60.0%  | -0.0120  |  3.2m
    200 |   15.0%  |    45.0%  | -0.0080  |  6.5m
    500 |   45.0%  |    20.0%  | -0.0030  | 16.1m
   1000 |   72.0%  |     8.0%  | -0.0010  | 32.3m
   3000 |   88.0%  |     3.0%  | -0.0002  | 97.0m
```
Success upar aana chahiye, collision neeche — yeh seekhne ki nishaani.

## Results kahan save honge?
`/kaggle/working/results/` mein:
- `final_model.pt` — trained model
- `history.json` — training log
- `training_curves.png` — success rate ka graph

Kaggle pe right side mein **Output** tab mein yeh sab dikhai denge — wahan se download kar sakte hain.
