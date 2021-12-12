#!/bin/bash
PWD=`pwd`
source "$PWD/server/venv/bin/activate" && PYTHONPATH="$PWD" python3 server/app.py
