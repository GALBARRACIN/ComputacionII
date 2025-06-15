# analizador_frecuencia.py
import numpy as np
from collections import deque

def analizador_frecuencia(pipe_in, queue_out):
    """
    Recibe muestras por Pipe, calcula media y desviación estándar de frecuencia
    sobre una ventana móvil de 30 elementos, y envía los resultados por Queue.
    """
    ventana = deque(maxlen=30)

    for _ in range(60):
        paquete = pipe_in.recv()
        valor = paquete["frecuencia"]
        ventana.append(valor)

        media = float(np.mean(ventana))
        desviacion = float(np.std(ventana))

        resultado = {
            "tipo": "frecuencia",
            "timestamp": paquete["timestamp"],
            "media": media,
            "desv": desviacion
        }

        queue_out.put(resultado)
