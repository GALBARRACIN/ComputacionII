## ⏱️ Ejercicio 14: Ejecución Diferida y Sincronización con sleep

# ✅ Objetivo:
Crear un script Bash que ejecute en segundo plano un script Python que duerme 10 segundos.

Desde otra terminal, verificar su ejecución con ps.

Enviarle una señal SIGTERM para terminarlo prematuramente.

# ▶️ Cómo ejecutar y probar:
Dar permisos y ejecutar el lanzador:

chmod +x lanzador.sh
./lanzador.sh
Desde otra terminal, mientras el proceso duerme:

ps -p [PID] -o pid,ppid,etime,cmd
Luego, matarlo prematuramente:

kill -SIGTERM [PID]
Confirmar que no llegó al mensaje final de "Desperté y terminé."

# 🧠 Resultado:
Si no matás el proceso, imprimirá el mensaje de finalización.

Si lo terminás con SIGTERM, el mensaje final no aparecerá.

dormilon.py puede manejar esa señal también

