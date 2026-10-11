# analizador_oxigeno.py
import numpy as np
from collections import deque

def analizador_oxigeno(pipe_in, queue_out):
    """
    Analiza el porcentaje de oxígeno en sangre.
    """
    ventana = deque(maxlen=30)

    for _ in range(60):
        paquete = pipe_in.recv()
        oxigeno = paquete["oxigeno"]
        ventana.append(oxigeno)

        media = float(np.mean(ventana))
        desviacion = float(np.std(ventana))

        resultado = {
            "tipo": "oxigeno",
            "timestamp": paquete["timestamp"],
            "media": media,
            "desv": desviacion
        }

        queue_out.put(resultado)
