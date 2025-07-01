## 🚰 Ejercicio 6: FIFO (named pipe) entre dos scripts

# ✅ Objetivo:
Crear un FIFO (named pipe) en /tmp/mi_fifo.

Escribir dos scripts:

emisor.py: escribe mensajes en el FIFO.

receptor.py: lee mensajes desde el FIFO e imprime.

# Crear el FIFO desde Bash
Antes de ejecutar los scripts, creamos el FIFO:

mkfifo /tmp/mi_fifo

# 🔁 Si ya existe, podés borrarlo antes con:

rm -f /tmp/mi_fifo && mkfifo /tmp/mi_fifo

# ▶️ Cómo ejecutar:
En una terminal, ejecutá el receptor:

python3 receptor.py
En otra terminal, ejecutá el emisor:

python3 emisor.py
Verás cómo el receptor imprime los mensajes que el emisor va enviando uno por segundo.

🧠 Si corrés primero el emisor sin tener el receptor escuchando, el emisor quedará bloqueado hasta que alguien abra el FIFO en modo lectura.