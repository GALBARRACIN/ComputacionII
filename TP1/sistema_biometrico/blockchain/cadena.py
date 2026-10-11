# cadena.py
import json
import os
from blockchain.bloque import Bloque


class CadenaDeBloques:
    """
    Maneja la cadena de bloques en memoria y en disco.
    """

    def __init__(self):
        self.archivo = os.path.join(os.path.dirname(__file__), "blockchain.json")
        self.bloques = []

        # Intentar cargar blockchain existente
        if os.path.exists(self.archivo):
            with open(self.archivo, "r") as f:
                datos = json.load(f)
                for bloque_dict in datos:
                    bloque = Bloque(
                        timestamp=bloque_dict["timestamp"],
                        datos=bloque_dict["datos"],
                        alerta=bloque_dict["alerta"],
                        prev_hash=bloque_dict["prev_hash"]
                    )
                    self.bloques.append(bloque)

    def ultimo_hash(self):
        if not self.bloques:
            return "0" * 64  # hash génesis
        return self.bloques[-1].hash

    def agregar_bloque(self, bloque):
        self.bloques.append(bloque)

    def guardar(self):
        with open(self.archivo, "w") as f:
            json.dump([b.a_dict() for b in self.bloques], f, indent=4)
