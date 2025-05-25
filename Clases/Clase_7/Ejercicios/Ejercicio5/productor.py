import os
import signal
import time

# Obtener PID del consumidor desde un archivo temporal
def obtener_pid_consumidor():
    try:
        with open("consumidor_pid.txt", "r") as f:
            return int(f.read().strip())
    except FileNotFoundError:
        print("[PRODUCTOR] No se encontró el PID del consumidor.")
        return None

def generar_trabajo():
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[PRODUCTOR] Trabajo generado: {timestamp}")

    consumidor_pid = obtener_pid_consumidor()
    if consumidor_pid:
        with open("trabajos.txt", "a") as f:
            f.write(f"{timestamp}\n")

        os.kill(consumidor_pid, signal.SIGUSR1)
        print(f"[PRODUCTOR] Señal enviada a consumidor ({consumidor_pid})")

if __name__ == "__main__":
    print("[PRODUCTOR] Iniciando generación de trabajos...")
    while True:
        time.sleep(2)  # Generar trabajo cada 2 segundos
        generar_trabajo()
