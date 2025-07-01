## 🧩 Ejercicio 16: Recolección Manual de Estado de Hijos

# ✅ Objetivo:
Crear 3 procesos hijos que terminen en distinto orden.

El padre recolecta el estado con os.waitpid manualmente.

Registrar el orden en que terminan los hijos.

# ▶️ Cómo ejecutar:

python3 recoleccion_manual.py

# 🧠 Explicación:
Cada hijo duerme un tiempo aleatorio y termina.

El padre espera a cualquier hijo que termine con os.waitpid(-1, 0).

Registra el orden en que los hijos finalizan.

Así se observa que los procesos no necesariamente terminan en orden de creación.

