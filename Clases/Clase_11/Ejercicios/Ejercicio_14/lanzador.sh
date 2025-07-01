#!/bin/bash

echo "[LANZADOR] Ejecutando dormilon.py en segundo plano..."
python3 dormilon.py &
PID=$!
echo "[LANZADOR] PID del dormilón: $PID"
