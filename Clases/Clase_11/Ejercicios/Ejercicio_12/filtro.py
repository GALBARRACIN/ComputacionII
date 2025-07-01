# filtro.py

import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description="Filtro de números mayores a un umbral.")
    parser.add_argument("--min", type=int, required=True, help="Mínimo valor permitido")
    args = parser.parse_args()

    for linea in sys.stdin:
        try:
            num = int(linea.strip())
            if num > args.min:
                print(num)
        except ValueError:
            continue  # Ignorar líneas no numéricas

if __name__ == "__main__":
    main()
