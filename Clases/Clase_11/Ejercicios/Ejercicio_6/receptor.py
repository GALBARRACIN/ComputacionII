# receptor.py

fifo_path = "/tmp/mi_fifo"

with open(fifo_path, 'r') as fifo:
    print("[RECEPTOR] Esperando mensajes...")
    while True:
        mensaje = fifo.readline()
        if not mensaje:
            break  # EOF
        print(f"[RECEPTOR] Recibido: {mensaje.strip()}")
