## 🚦 Ejercicio 9: Control de concurrencia con Semaphore

# ✅ Objetivo:
Simular un entorno con puestos limitados (zona crítica con capacidad máxima).

Crear 10 procesos que intenten acceder a esa zona crítica.

Usar multiprocessing.Semaphore para permitir solo 3 accesos simultáneos.

# ▶️ Cómo ejecutar:

python3 puestos_limitados.py

Solo 3 procesos entran a la vez. Los demás esperan hasta que se libere un puesto.

# Ejemplo de salida parcial:

[P1] PID 12345 esperando un puesto...
[P1] ✅ Entró a la zona crítica.
[P2] PID 12346 esperando un puesto...
[P2] ✅ Entró a la zona crítica.
[P3] PID 12347 esperando un puesto...
[P3] ✅ Entró a la zona crítica.
[P4] PID 12348 esperando un puesto...
...
[P1] ❌ Saliendo de la zona crítica.
[P4] ✅ Entró a la zona crítica.