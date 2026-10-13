#!/bin/sh
# Phase 2 main training: 5 base-paper methods x 10 seeds (42-51) x Stage 2/3 = 100 runs, 4 at a time.
# Longest jobs first (RMAPPO, then IGAT-style, Stage 3 before Stage 2) so the night ends with short jobs.
# Launch from v4/03-base-paper-baselines/:
#   nohup caffeinate -i -s ./runs/run_phase2.sh > runs/logs/launcher.out 2>&1 &
# Then check one runs/stage*/<method>/seed-*/config.json of every method.
cd "$(dirname "$0")/.."
. ../../../../venv/bin/activate
date '+start %Y-%m-%d %H:%M:%S' >> runs/logs/time.txt
cat runs/jobs.txt | xargs -P 4 -L 1 sh -c 'm=$0; st=$1; sd=$2; python3 -u train_baselines.py $m $st $sd > runs/logs/$m-stage$st-seed$sd.log 2>&1'
date '+end %Y-%m-%d %H:%M:%S' >> runs/logs/time.txt
