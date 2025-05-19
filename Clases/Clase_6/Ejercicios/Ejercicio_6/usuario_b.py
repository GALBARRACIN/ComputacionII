import os

fifo_envio = "/tmp/chat_b"
fifo_recepcion = "/tmp/chat_a"

# Crear los FIFOs si no existen
for fifo in [fifo_envio, fifo_recepcion]:
    if not os.path.exists(fifo):
        os.mkfifo(fifo)

print("Chat activo. Escribe tu mensaje:")

while True:
    mensaje = input("Usuario B > ")  # Leer mensaje del usuario
    if mensaje.lower() == "/exit":
        break  # Salir del chat
    
    with open(fifo_envio, "w") as fifo:
        fifo.write(mensaje + "\n")  # Enviar mensaje
    
    # Leer respuesta de Usuario A
    with open(fifo_recepcion, "r") as fifo:
        respuesta = fifo.readline().strip()
        print(f"Usuario A: {respuesta}")
