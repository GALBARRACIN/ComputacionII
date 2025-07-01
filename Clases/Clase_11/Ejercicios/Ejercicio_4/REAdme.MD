## 🔁 Ejercicio 4: Reemplazo con exec()

# ✅ Objetivo:
Crear un proceso hijo usando fork().

El hijo debe reemplazar su imagen de ejecución por el comando ls -l usando exec().

Verificar desde Bash que el proceso efectivamente cambió su nombre.

# ▶️ Cómo ejecutar:

python3 exec_reemplazo.py

🔍 En la salida verás que el hijo imprime su PID y luego aparece directamente la salida del comando ls -l.

Podés inspeccionar en otra terminal mientras corre (si pausás el hijo antes de exec) con:

ps -ef | grep ls

Una vez ejecutado exec, el proceso ya no es Python, sino ls, y eso es lo que se verá en ps.