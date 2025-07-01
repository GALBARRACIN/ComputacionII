## 🌲 Ejercicio 13: Visualización de Jerarquía de Procesos

# ✅ Objetivo:
Crear un script en Python que cree dos procesos hijos.

Desde Bash, usar pstree -p y ps --forest para visualizar la genealogía de procesos.

Capturar la salida y analizar la jerarquía.

# ▶️ Cómo ejecutar:
Ejecutá el script:

python3 jerarquia_procesos.py
Rápidamente, desde otra terminal, observá la jerarquía con:

pstree:

pstree -p [PID_DEL_PADRE]
Por ejemplo:


python3(1000)─┬─python3(1001)
             └─python3(1002)
ps --forest:


ps -ejH

O bien, filtrado:

ps --forest -C python3

# 🧠 Interpretación:
El proceso padre aparece con dos hijos directos.

Visualmente, se ve la relación de jerarquía: el árbol muestra cómo los hijos dependen del padre.

PPID confirma la relación (el PPID del hijo es el PID del padre).