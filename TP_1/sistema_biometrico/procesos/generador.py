# generador.py
import random
import time
from datetime import datetime

def generador(pipe_frec, pipe_pres, pipe_oxi):
    """
    Genera 60 muestras biométricas, una por segundo, y las envía por Pipe a cada analizador.
    """
    for _ in range(60):
        # Crear paquete de datos biométricos
        muestra = {
            "timestamp": datetime.now().isoformat(),
            "frecuencia": random.randint(60, 180),
            "presion": [random.randint(110, 180), random.randint(70, 110)],
            "oxigeno": random.randint(90, 100)
        }

        # Enviar la misma muestra a los tres analizadores por pipe
        pipe_frec.send(muestra)
        pipe_pres.send(muestra)
        pipe_oxi.send(muestra)

        time.sleep(1)  # Esperar 1 segundo antes de la siguiente muestra
