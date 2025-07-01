# emisor.py

import os
import signal
import time
import sys

def main():
    if len(sys.argv) != 2:
        print(f"Uso: python3 emisor.py [PID_receptor]")
        sys.exit(1)

    pid_receptor = int(sys.argv[1])
    señales = [signal.SIGUSR1, signal.SIGUSR2]
    i = 0

    print(f"[EMISOR] Enviando señales a PID {pid_receptor}")

    try:
        while True:
            señal = señales[i % 2]
            os.kill(pid_receptor, señal)
            print(f"[EMISOR] Enviada señal {señal.name}")
            i += 1
            time.sleep(2)
    except KeyboardInterrupt:
        print("[EMISOR] Interrumpido y finalizando.")

if __name__ == "__main__":
    main()
