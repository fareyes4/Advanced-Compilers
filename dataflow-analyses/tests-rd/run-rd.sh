#!/usr/bin/env bash
set -euo pipefail
file=$(ls *.bril)
# run the analysis
/home/fareyes4/.local/bin/bril2json < "$file" | /bin/python3 /home/fareyes4/bril/examples/reaching.py
