#!/bin/bash
# Updates hub status by calling check_hub_stat.py
# This script may be scheduled as a cronjob for auto-updation of website or README.md

cd ~/WorkInProgress/IIT-Madras-DC-Hubs
git pull 
python check_hub_status.py
bash auto_commit.sh
git push
