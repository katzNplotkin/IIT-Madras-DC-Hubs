#!/bin/bash
# Updates hub status by calling check_hub_stat.py
# This script may be scheduled as a cronjob for auto-updation of website or README.md

cd ~/WorkInProgress/IIT-Madras-DC-Hubs
git pull 
python check_hub_status.py
if [[ $1 == '-t' ]]; then    # -t flag for testing without commits
  cat hubstat.txt
else
  git add hubstat.txt docs/README.md
  git commit -m 'Hub status auto-update'
  git push
fi
