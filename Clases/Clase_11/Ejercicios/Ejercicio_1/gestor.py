# gestor.py

import argparse
import os
import time
import random
import subprocess
import sys

def main():
    parser = argparse.ArgumentParser(description="Gestor de procesos hijos.")
    parser.add_argument('--num', type=int, required=True, help='Cantidad de procesos hijos a crear')
    parser.add_argument('--verbose', action='store_true', help='Activar salida detallada')
    args = parser.parse_args()

    hijos = []

    if args.verbose:
        print(f"[PADRE] PID: {os.getpid()} - Creando {args.num} hijos...")

    for i in range(args.num):
        pid = os.fork()
        if pid == 0:
            # Proceso hijo
            duracion = random.randint(1, 5)
            if args.verbose:
                print(f"[HIJO {os.getpid()}] Durmiendo {duracion} segundos.")
            time.sleep(duracion)
            if args.verbose:
                print(f"[HIJO {os.getpid()}] Finalizando.")
            os._exit(0)
        else:
            hijos.append(pid)

    # Solo el padre llega acá
    if args.verbose:
        print(f"[PADRE] Todos los hijos creados. PID: {os.getpid()}")

    # Mostrar jerarquía de procesos
    print("\nJerarquía de procesos (pstree -p):")
    subprocess.run(['pstree', '-p', str(os.getpid())])

    # Esperar a los hijos
    for pid in hijos:
        os.waitpid(pid, 0)

    if args.verbose:
        print("[PADRE] Todos los hijos han finalizado.")

if __name__ == "__main__":
    main()
