# verificador.py
import hashlib
import json
import os
from datetime import datetime
from blockchain.bloque import Bloque
from blockchain.cadena import CadenaDeBloques


def verificador(queue_frec, queue_pres, queue_oxi):
    """
    Proceso verificador que:
    - Agrupa resultados por timestamp.
    - Detecta alertas si hay valores fuera de rango.
    - Construye y enlaza bloques.
    - Persiste los bloques en blockchain.json.
    """

    blockchain = CadenaDeBloques()

    # Diccionario temporal de resultados por timestamp
    pendientes = {}

    # Procesa 60 muestras (una por segundo)
    for _ in range(60):
        # Obtener un resultado de cada tipo
        r_f = queue_frec.get()
        r_p = queue_pres.get()
        r_o = queue_oxi.get()

        # Asegurar que todos coincidan en timestamp
        timestamp = r_f["timestamp"]

        # Agrupar por tipo
        datos = {
            "frecuencia": {
                "media": r_f["media"],
                "desv": r_f["desv"]
            },
            "presion": {
                "media": r_p["media"],
                "desv": r_p["desv"]
            },
            "oxigeno": {
                "media": r_o["media"],
                "desv": r_o["desv"]
            }
        }

        # Verificar condiciones de alerta
        alerta = (
            r_f["media"] >= 200 or
            r_p["media"] >= 200 or
            not (90 <= r_o["media"] <= 100)
        )

        # Crear nuevo bloque
        bloque = Bloque(
            timestamp=timestamp,
            datos=datos,
            alerta=alerta,
            prev_hash=blockchain.ultimo_hash()
        )

        # Añadir bloque a la cadena y persistir
        blockchain.agregar_bloque(bloque)
        blockchain.guardar()

        print(f"🧱 Bloque #{len(blockchain.bloques)} - Hash: {bloque.hash[:12]}{' ⚠️ ALERTA' if alerta else ''}")
