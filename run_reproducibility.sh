#!/usr/bin/env bash
set -euo pipefail
python -m unittest discover -v
python instrumented_rdkit.py
python representation_sensitivity.py
python multitask_audit.py
python novelty_gate.py
