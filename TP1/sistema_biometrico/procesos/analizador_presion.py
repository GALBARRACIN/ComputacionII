# analizador_presion.py
import numpy as np
from collections import deque

def analizador_presion(pipe_in, queue_out):
    """
    Calcula estadísticas sobre la presión sistólica (valor alto).
    """
    ventana = deque(maxlen=30)

    for _ in range(60):
        paquete = pipe_in.recv()
        presion_sistolica = paquete["presion"][0]
        ventana.append(presion_sistolica)

        media = float(np.mean(ventana))
        desviacion = float(np.std(ventana))

        resultado = {
            "tipo": "presion",
            "timestamp": paquete["timestamp"],
            "media": media,
            "desv": desviacion
        }

        queue_out.put(resultado)
