#!/bin/bash

echo "Listado de procesos activos:"
echo "PID  | PPID | Nombre           | Estado"
echo "------------------------------------------"

declare -A estados

for pid in $(ls /proc | grep -E '^[0-9]+$'); do
    status="/proc/$pid/status"

    if [ -f "$status" ]; then
        PID=$(grep "^Pid:" "$status" | awk '{print $2}')
        PPID=$(grep "^PPid:" "$status" | awk '{print $2}')
        NAME=$(grep "^Name:" "$status" | awk '{print $2}')
        STATE_LINE=$(grep "^State:" "$status")
        STATE=$(echo "$STATE_LINE" | awk '{print $2}')
        
        printf "%-5s| %-5s| %-16s| %s\n" "$PID" "$PPID" "$NAME" "$STATE"

        # Contador por estado
        ((estados["$STATE"]++))
    fi
done

echo
echo "Resumen de estados:"
for estado in "${!estados[@]}"; do
    echo "Estado '$estado': ${estados[$estado]} procesos"
done
