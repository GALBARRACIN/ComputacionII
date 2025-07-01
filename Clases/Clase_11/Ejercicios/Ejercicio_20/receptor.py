# receptor.py

import signal
import os
import time

def manejador_usr1(signum, frame):
    print(f"[{os.getpid()}] Recibió SIGUSR1: acción 1")

def manejador_usr2(signum, frame):
    print(f"[{os.getpid()}] Recibió SIGUSR2: acción 2")

def main():
    print(f"[RECEPTOR] PID {os.getpid()} esperando señales SIGUSR1 y SIGUSR2...")
    signal.signal(signal.SIGUSR1, manejador_usr1)
    signal.signal(signal.SIGUSR2, manejador_usr2)

    while True:
        signal.pause()  # Espera pasiva

if __name__ == "__main__":
    main()
