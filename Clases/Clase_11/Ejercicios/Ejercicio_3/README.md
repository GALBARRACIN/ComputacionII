## 👤 Ejercicio 3: Proceso Huérfano

# ✅ Objetivo:
Crear un proceso hijo que siga vivo después de que el padre finalice.

El hijo debe seguir ejecutándose (por ejemplo, durmiendo).

Verificar que su nuevo PPID sea 1 (init o systemd) usando ps o /proc.

# ▶️ Cómo ejecutar y verificar:
Ejecutá el script:

python3 huerfano.py

Rápidamente, abrí otra terminal y corré:

ps -o pid,ppid,cmd | grep python

Buscá el PPID del proceso hijo. Si es 1 (en sistemas modernos puede ser systemd), es un huérfano correctamente adoptado por el sistema.

También podés verificar:

cat /proc/[pid_del_hijo]/status | grep PPid