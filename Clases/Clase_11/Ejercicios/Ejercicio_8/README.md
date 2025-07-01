## ⚠️ Ejercicio 8: Condición de Carrera y su Corrección

# ✅ Objetivo:
Implementar un contador compartido entre dos procesos sin protección, evidenciando una condición de carrera.

Corregirlo usando multiprocessing.Lock.

# ▶️ Cómo probar:
Primero ejecutá la versión sin Lock:

python3 contador_sin_lock.py

Después la versión corregida:

python3 contador_con_lock.py