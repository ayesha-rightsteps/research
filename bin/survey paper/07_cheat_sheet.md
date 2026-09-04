```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📄 PAPER CHEAT SHEET
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TITLE:   A Survey on Deep Reinforcement Learning Applications
         in Autonomous Systems: Applications, Open
         Challenges, and Future Directions

AUTHORS: Shruti Govinda, Bouziane Brik (Sr. Member, IEEE),
         Saad Harous (Sr. Member, IEEE)

VENUE:   IEEE Transactions on Intelligent Transportation
         Systems, Vol. 26, No. 7   |   YEAR: July 2025

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
THE CORE STORY (memorize this)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PROBLEM:    Traditional control methods can't handle the
            unpredictability of the real world. DRL can —
            but no one had mapped the whole field.

SOLUTION:   A systematic review of DRL across 4 domains:
            autonomous cars, robots, drones, and ADAS —
            with structured comparison tables.

KEY RESULT: VILDS: 98.2% lane detection + 96.5% departure
            warning accuracy. SIFRCNN: 23% miss rate
            improvement. SAC: 100% safety in robot planning.

SO WHAT:    DRL is already in Tesla, Waymo, Boston Dynamics,
            Amazon drones & DJI — but Sim-to-Real gap and
            safety certification remain unsolved challenges.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
5 TERMS TO KNOW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⭐ DRL:   AI that learns by trial-and-error using neural nets
⭐ DDPG:  Best algorithm for continuous control (steering, speed)
⭐ SAC:   Safest algorithm; achieved 100% safety in robot tasks
⭐ DQN:   Best for discrete decisions (turn left/right/go straight)
   ADAS:  Car safety systems (lane warning, cruise control)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
4 DOMAINS COVERED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚗 Autonomous Cars   → lane following, parking, urban navigation,
                        obstacle avoidance, braking
🤖 Autonomous Robots → swarm behavior, collision avoidance,
                        trajectory planning
🚁 Autonomous Drones → security, pollution monitoring,
                        stability, collision avoidance
🛡️ ADAS              → lane departure warning, pedestrian
                        detection, adaptive cruise control

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WHAT MAKES THIS PAPER UNIQUE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• First survey to cover ALL 4 autonomous system domains together
• Structured comparison tables (Tables III–VI) — not just a list
• Includes real industry case studies: Tesla, Waymo, Amazon,
  Boston Dynamics, DJI, Mobileye, Nvidia
• Forward-looking: discusses LLM and Transformer integration
  as the next frontier for autonomous AI

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY NUMBERS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

98.2%   → VILDS lane detection accuracy (ADAS)
96.5%   → VILDS departure warning accuracy (ADAS)
23%     → SIFRCNN miss rate improvement in nighttime
           pedestrian detection (KAIST, CityPerson, Caltech)
100%    → SAC safety rate in robot trajectory planning
           (6,000 simulation episodes)
2018–24 → Publication period of papers reviewed
7       → Academic databases searched

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
QUICK Q&A
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

If asked about limitations:
→ "The key limitation is the Sim-to-Real gap — systems
  trained in simulation show performance drops in the
  real world. Safety certification is also unresolved."

If asked what you'd change:
→ "I'd add a quantitative meta-analysis and propose a
  standardized benchmarking protocol, so results from
  different research groups could be directly compared."

If asked about future work:
→ "The authors suggest integrating Large Language Models
  for reasoning, transformer architectures for efficiency,
  and developing international safety and ethical
  regulatory frameworks for autonomous systems."

If asked why DRL over traditional methods:
→ "Traditional rule-based methods break down in dynamic
  or unpredictable situations. DRL learns from experience
  and adapts — making it far more robust in real-world
  conditions."

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ALGORITHM QUICK REFERENCE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DDPG  → Continuous control (steering, speed) — most used
DQN   → Discrete decisions (routing, braking events)
PPO   → Safe incremental learning (swarm robots, racing)
SAC   → Safest; adds exploration bonus (manipulation)
D2QN  → Improved DQN; less overestimation (VRU avoidance)
D3QN  → Even better; dual architecture (drones)
TD3   → Twin critics; multi-drone coordination
MARL  → Multiple agents coordinating (drone fleets)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
