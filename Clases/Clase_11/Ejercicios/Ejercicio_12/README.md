## 🔗 Ejercicio 12: Ejecución Encadenada con argparse y Pipes

# ✅ Objetivo:
Crear dos scripts:

generador.py: genera una cantidad de números aleatorios (parámetro --n) y los imprime por stdout.

filtro.py: recibe números por stdin y muestra solo los mayores a un umbral (--min).

Desde Bash, encadenar ambos con un pipe:

python3 generador.py --n 100 | python3 filtro.py --min 50

# ▶️ Cómo ejecutar desde Bash:

python3 generador.py --n 20 | python3 filtro.py --min 50

Esto generará 20 números aleatorios entre 0 y 100, y solo mostrará los mayores a 50.