# Samjho: docs/plans/01_roadmap.md

## Yeh cheez kya hai
Har phase (P0 se P6) ke andar ke chhote-chhote kaam, kaunsa kaam kis pe depend karta
hai, aur "ye kaam done kab maana jayega".

## Iski zaroorat kyun
Master plan bada picture deta hai. Yeh doc batata hai **kal subah exactly kya karna
hai** aur "ho gaya" ka matlab kya hai.

## Main baatein

- **Synopsis ka Gantt chart (12 mahine) is roadmap se match kiya gaya hai.** Har
  synopsis task ko humne apne phases se jod diya.

- **Honest timeline warning:** Synopsis kehta hai "2D env + DA-MAPPO replication = 2
  mahine". Sach: environment ache se + tests = 3-5 hafte, minimal MAPPO = 3-4 hafte,
  Stage 1 ko actually chalana = 2-4 hafte debugging. To realistically month 2 ke end
  tak env + MAPPO chal raha hoga, poori replication month 3. Supervisor ko abhi bata
  do.

- **Har phase ke liye table hai:** kaam | kis pe depend karta hai | done kab.
  Example (P1 Environment): "collision detection" done tab hoga jab hand-banaye hue test
  cases pass ho jaayein.

- **P0 aur P1 parallel chal sakte hain** — environment banane ke liye PAH ka jawab
  nahi chahiye, to supervisor ka wait karte hue P1 shuru kar do.

- **Standing risks table** — har badi problem (PAH reward hacking, assignment
  thrashing, MAPPO na seekhna, time overrun) ke saath uska plan B likha hai.

## Mushkil lafz
- **Gantt chart** = time ke against tasks ka bar chart (synopsis mein hai)
- **Dependency** = "ye kaam pehle wale kaam ke bina nahi ho sakta"
- **Done criteria / "done when"** = wo condition jispe kaam complete maana jaye
- **Thrashing** = baar-baar aage-peeche switch hota rehna, progress na hona
- **Convergence** = training mein model ka seekhna ruk jaana (achhe level pe pahunch ke)
