# generador.py

import argparse
import random

def main():
    parser = argparse.ArgumentParser(description="Generador de números aleatorios.")
    parser.add_argument("--n", type=int, required=True, help="Cantidad de números a generar")
    args = parser.parse_args()

    for _ in range(args.n):
        print(random.randint(0, 100))  # Se imprime a stdout

if __name__ == "__main__":
    main()
