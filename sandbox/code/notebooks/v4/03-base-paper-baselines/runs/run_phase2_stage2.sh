#!/bin/sh
# Phase 2, part 1b: Stage 2 only (IGAT-style, IPPO, MAPPO, DA-MAPPO (2D) x 10 seeds = 40 runs), 6 at a time.
# Ayesha 2026-10-14: Stage 3 pehle, Stage 2 baad mein jab woh kahen. Launch from v4/03-base-paper-baselines/:
#   nohup caffeinate -i -s ./runs/run_phase2_stage2.sh > runs/logs/launcher_stage2.out 2>&1 &
cd "$(dirname "$0")/.."
. ../../../../venv/bin/activate
date '+start %Y-%m-%d %H:%M:%S' >> runs/logs/time_stage2.txt
cat runs/jobs_stage2.txt | xargs -P 6 -L 1 sh -c 'm=$0; st=$1; sd=$2; python3 -u train_baselines.py $m $st $sd > runs/logs/$m-stage$st-seed$sd.log 2>&1'
date '+end %Y-%m-%d %H:%M:%S' >> runs/logs/time_stage2.txt
