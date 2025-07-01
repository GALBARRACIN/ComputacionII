## 📶 Ejercicio 11: Manejo de Señales

# ✅ Objetivo:
Crear un script que instale un manejador para la señal SIGUSR1.

El proceso queda esperando pasivamente (con pause() o bucle infinito).

Al recibir SIGUSR1, el proceso debe reaccionar e imprimir un mensaje.

# ▶️ Cómo ejecutar y probar:
En una terminal, ejecutá el proceso:

python3 manejador_senal.py

En otra terminal, enviá la señal:

kill -SIGUSR1 [PID]

Podés obtener el PID directamente desde la salida del script, o con:

ps aux | grep manejador_senal.py

# 🧠 Cuando la señal se recibe, el proceso imprime:

[12345] Señal recibida: 10 (SIGUSR1)