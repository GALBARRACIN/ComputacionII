#!/bin/bash

fifo="/tmp/mi_fifo"

echo "[LECTOR] Esperando mensajes..."

while true; do
    if read linea < "$fifo"; then
        echo "[LECTOR] Recibido: $linea"
    else
        sleep 1
    fi
done
