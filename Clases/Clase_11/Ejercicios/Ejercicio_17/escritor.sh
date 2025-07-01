#!/bin/bash

fifo="/tmp/mi_fifo"

for i in {1..10}; do
    echo "Mensaje $i" > "$fifo"
    echo "[ESCRITOR] Enviado: Mensaje $i"
    sleep 1
done
