# manejador_senal.py

import signal
import os
import time

def recibir_senal(signum, frame):
    print(f"[{os.getpid()}] Señal recibida: {signum} (SIGUSR1)")

def main():
    print(f"[PROCESO] PID {os.getpid()} esperando señal SIGUSR1...")
    signal.signal(signal.SIGUSR1, recibir_senal)

    # Espera pasiva
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
