## 🧟 Ejercicio 2: Proceso Zombi

# ✅ Objetivo:
Crear un hijo que finaliza inmediatamente.

El padre no lo espera durante al menos 10 segundos.

El hijo queda en estado zombi (Z) durante ese tiempo.

Verificar desde Bash con ps o /proc/[pid]/status.

# ▶️ Cómo ejecutar:
En una terminal:

python3 zombi.py

Rápidamente, en otra terminal, mientras el padre duerme:

ps -elf | grep defunct

O directamente:

ps -o pid,ppid,stat,cmd | grep Z

También podés inspeccionar /proc:

cat /proc/[pid_del_hijo]/status
El estado "State:\tZ (zombie)" indicará que efectivamente el proceso es un zombi.