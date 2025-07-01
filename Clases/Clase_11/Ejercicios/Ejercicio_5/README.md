## 🧵 Ejercicio 5: Pipes anónimos entre padre e hijo

# ✅ Objetivo:
Usar os.pipe() para crear un canal anónimo entre padre e hijo.

El hijo envía un mensaje al padre.

El padre lee e imprime el mensaje.

Uso de codificación binaria y cierre adecuado de descriptores.

# ▶️ Cómo ejecutar:

python3 pipe_padre_hijo.py

👀 Verás la salida:

[PADRE] Mensaje recibido del hijo: Hola padre, soy tu hijo.
Este script demuestra correctamente la comunicación entre procesos mediante pipe anónimo, con manejo explícito de los descriptores.