## ⚠️ Ejercicio 19: Escritura Concurrente sin Exclusión

# ✅ Objetivo:
Ejecutar varios procesos Python que escriben simultáneamente a un mismo archivo sin usar Lock.

Observar cómo se mezclan y corrompen las escrituras.

Comparar con la versión sincronizada usando multiprocessing.Lock.

# ▶️ Cómo ejecutar y comparar:
Ejecutar versión sin Lock:

python3 escritura_sin_lock.py
cat log_concurrente_sin_lock.txt

Ejecutar versión con Lock:

python3 escritura_con_lock.py
cat log_concurrente_con_lock.txt

# 🧠 Observaciones:
Sin Lock, las líneas pueden mezclarse, perderse o solaparse.

Con Lock, la escritura es ordenada y coherente.

