#!/bin/sh
# Phase 1b Step 4: 100 runs, 4 at a time (MacBook Air, fanless), settings frozen in PLAN.md Section 10.
cd "$(dirname "$0")/.."
. ../../../../venv/bin/activate
date '+start %Y-%m-%d %H:%M:%S' > runs/logs/time.txt
cat runs/jobs.txt | xargs -P 4 -L 1 sh -c 'm=$0; st=$1; sd=$2; d=$3; python3 -u train.py $m $st $sd --obstacles $d --danger 20 --collision-penalty 10 > runs/logs/$m-stage$st-seed$sd.log 2>&1'
date '+end %Y-%m-%d %H:%M:%S' >> runs/logs/time.txt
