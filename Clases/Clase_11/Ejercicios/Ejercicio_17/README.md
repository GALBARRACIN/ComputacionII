## 🔄 Ejercicio 17: Simulación de Lector y Escritor con FIFO

# ✅ Objetivo:
Crear dos scripts Bash:

Uno que escribe en una FIFO cada segundo.

Otro que lee continuamente de la FIFO.

Analizar qué pasa si se inicia el lector antes o después del escritor.

# 📁 Paso 1: Crear la FIFO

mkfifo /tmp/mi_fifo

# ▶️ Cómo probar:
En una terminal, ejecutá el lector:

chmod +x lector.sh
./lector.sh

En otra terminal, ejecutá el escritor:

chmod +x escritor.sh
./escritor.sh

# 🧠 Observaciones:

Si arrancás el lector primero:
El lector queda esperando (bloqueado) hasta que el escritor escriba en la FIFO.

Si arrancás el escritor primero:
El escritor quedará bloqueado hasta que el lector abra la FIFO para lectura.

Esto demuestra cómo el FIFO sin lector o escritor activo bloquea a quien quiera escribir o leer.