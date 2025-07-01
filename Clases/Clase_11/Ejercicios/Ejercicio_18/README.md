## 🔍 Ejercicio 18: Observación de Pipes con lsof

# ✅ Objetivo:
Ejecutar un programa Python que use os.pipe() para comunicación entre procesos.

Desde Bash, usar lsof -p [pid] para observar los descriptores abiertos por el proceso.

# ▶️ Cómo ejecutar:

python3 pipe_lsof.py

Deja correr el script para que el proceso padre esté vivo.

🔎 En otra terminal, inspeccionar los descriptores con lsof:
Obtener el PID del proceso padre (aparece en la salida o con ps).

Ejecutar:

lsof -p [PID]

# 🧠 Qué verás:
Los descriptores abiertos, incluyendo los pipes (PIPE), con detalles de lectura o escritura.

Por ejemplo:

COMMAND   PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
python3  1234 user    3u  PIPE  0,12      0t0 12345 pipe
python3  1234 user    4r  PIPE  0,12      0t0 12345 pipe
...