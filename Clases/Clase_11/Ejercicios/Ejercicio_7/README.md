## 🧠 Ejercicio 7: Procesos Concurrentes con multiprocessing

# ✅ Objetivo:
Crear 4 procesos con multiprocessing.Process.

Cada proceso escribe su PID y una marca de tiempo en un mismo archivo de log.

Usar multiprocessing.Lock para evitar colisiones en escritura concurrente.

# Salida esperada en log_concurrente.txt

[2025-07-01 10:30:02] PID 12345 (Proceso 1) escribiendo en el log.
[2025-07-01 10:30:02] PID 12346 (Proceso 2) escribiendo en el log.
...

# ▶️ Cómo ejecutar:

python3 multiprocesos_log.py

Luego podés revisar:

cat log_concurrente.txt