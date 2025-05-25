import os
import signal
import time
import random
import sys

# Diccionario para registrar señales recibidas
signal_log = {}

def signal_handler(signum, frame):
    pid = os.getpid()
    signal_name = {signal.SIGUSR1: "SIGUSR1", signal.SIGUSR2: "SIGUSR2", signal.SIGTERM: "SIGTERM"}.get(signum, "UNKNOWN")
    signal_log[pid] = signal_name
    print(f"[PADRE] Señal recibida: {signal_name} desde proceso {pid}")

# Configurar manejadores para las señales
signal.signal(signal.SIGUSR1, signal_handler)
signal.signal(signal.SIGUSR2, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def create_child():
    pid = os.fork()
    if pid == 0:
        time.sleep(random.uniform(1, 3))  # Espera aleatoria antes de enviar la señal
        parent_pid = os.getppid()
        signal_to_send = random.choice([signal.SIGUSR1, signal.SIGUSR2, signal.SIGTERM])
        os.kill(parent_pid, signal_to_send)
        print(f"[HIJO {os.getpid()}] Enviado {signal_to_send} al padre ({parent_pid})")
        sys.exit(0)

if __name__ == "__main__":
    print("[PADRE] Iniciando y esperando señales de los hijos...")
    
    # Crear tres procesos hijos
    for _ in range(3):
        create_child()
    
    # Mantener el proceso padre en espera de señales
    while len(signal_log) < 3:
        time.sleep(1)
    
    print("[PADRE] Señales registradas:", signal_log)
    print("[PADRE] Finalizando...")
