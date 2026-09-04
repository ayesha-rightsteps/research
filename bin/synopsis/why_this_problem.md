# Why This Is a Good Research Problem

---

**1. The gap is proven by the papers themselves — not by me.**
DA-MAPPO and IGAT-MARL both wrote in their own future work sections that what the other paper does is what they could not do. I did not invent the gap. The original authors documented it. That makes it a real and acknowledged open problem in the field.

**2. There is a specific technical conflict no one has resolved.**
In 3D space, the assignment mechanism tells a drone "go here" and the collision mechanism tells it "deviate from this path" — at the same time, without knowing what the other is doing. This is not just two things being combined. It is two things that can directly contradict each other. That contradiction is the research question.

**3. The numbers are real.**
DA-MAPPO's own ablation showed mission success drops from 90% to 0% when the assignment is removed. IGAT-MARL reduced unnecessary interactions by 44%. These are not estimates — they are published experimental results. The research question builds directly on what those numbers mean.

**4. The scope is right for a Masters.**
5 to 8 drones, simulation only, free tools (PyBullet, PyTorch). It is not too small to publish and not too large to finish. There is a clear baseline to beat, a clear metric to measure, and a clear timeline.

**5. The answer is not known.**
This is the most important point. A good research problem is one where you genuinely do not know the outcome before you run the experiment. No paper has tested whether these two mechanisms work together or interfere. That is exactly what research is for.

**6. Why I chose this specific problem.**
After reading all ten papers, I noticed that Papers 9 and 91 were solving the same real-world scenario from opposite sides — one focused entirely on where drones go, the other on how they avoid each other — and neither looked at what happens when both problems occur at the same time in 3D space. That is not a coincidence or a gap I was told about. It is something I saw by reading both papers carefully and asking: why has nobody put these two together? That question is what this research is trying to answer.
