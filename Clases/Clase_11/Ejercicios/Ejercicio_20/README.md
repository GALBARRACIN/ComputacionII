## ⚙️ Ejercicio 20: Interacción entre Procesos con Señales Personalizadas

# ✅ Objetivo:
Implementar dos scripts:

Receptor: espera indefinidamente con pause() y maneja señales SIGUSR1 y SIGUSR2, reaccionando de forma distinta.

Emisor: envía señales SIGUSR1 y SIGUSR2 cada cierto tiempo al receptor.

# ▶️ Cómo ejecutar:
Abrir una terminal y ejecutar el receptor:

python3 receptor.py

En otra terminal, ejecutar el emisor pasando el PID del receptor:

python3 emisor.py [PID_receptor]

Podés obtener el PID del receptor con:

ps aux | grep receptor.py

# 🧠 Resultado:
El receptor imprimirá mensajes alternados según la señal recibida (SIGUSR1 o SIGUSR2).

El emisor enviará señales cada 2 segundos hasta interrumpirse con Ctrl+C.