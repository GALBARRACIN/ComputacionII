## Ejercicio 1: Creación de Procesos con Argumentos

# ✅ Objetivo:
Crear N procesos hijos.

Cada hijo duerme entre 1 y 5 segundos.

El proceso padre imprime su PID y muestra la jerarquía de procesos con pstree -p.

Si se pasa --verbose, se muestran mensajes detallados.

# ▶️ Cómo ejecutar:

python3 gestor.py --num 3 --verbose

Esto creará 3 hijos que duermen entre 1 y 5 segundos cada uno, y se mostrará el árbol de procesos actual. Podés observar el estado con:

ps -ef | grep gestor.py

O explorando /proc/[pid].