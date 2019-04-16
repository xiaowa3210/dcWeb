#!/usr/bin/env bash
git init
git remote add origin https://git.coding.net/dachuang/dcWeb.git
git pull origin release
nohup python3 run.py &