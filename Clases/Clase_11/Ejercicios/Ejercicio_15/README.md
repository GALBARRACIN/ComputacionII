## 🧾 Ejercicio 15: Análisis de Procesos Activos

# ✅ Objetivo:
Crear un script Bash que recorra /proc y:

Liste los procesos activos.

Para cada uno, muestre: PID, PPID, Nombre del ejecutable, Estado.

Al final, generar un resumen de los estados encontrados (ej: cuántos en R, S, Z, etc.).

# ▶️ Cómo ejecutar:
Dar permisos al archivo:

chmod +x analizar_procesos.sh

Ejecutarlo:

./analizar_procesos.sh
🧠 Qué vas a ver:
Un listado tipo:

PID  | PPID | Nombre           | Estado
------------------------------------------
1    | 0    | systemd          | S
2453 | 1    | bash             | S
2480 | 2453 | python3          | R
...
Y al final, algo como:


Resumen de estados:
Estado 'S': 103 procesos
Estado 'R': 4 procesos
Estado 'Z': 1 procesos

# 🧠 Estado comunes:

R: running

S: sleeping

D: waiting

Z: zombie

T: stopped