# bloque.py
import hashlib
import json


class Bloque:
    """
    Representa un bloque en la cadena.
    Contiene: timestamp, datos, flag de alerta, hash previo, y su propio hash.
    """

    def __init__(self, timestamp, datos, alerta, prev_hash):
        self.timestamp = timestamp
        self.datos = datos
        self.alerta = alerta
        self.prev_hash = prev_hash
        self.hash = self.calcular_hash()

    def calcular_hash(self):
        """
        Calcula hash SHA-256 usando los campos clave del bloque.
        """
        contenido = json.dumps({
            "timestamp": self.timestamp,
            "datos": self.datos,
            "alerta": self.alerta,
            "prev_hash": self.prev_hash
        }, sort_keys=True).encode()

        return hashlib.sha256(contenido).hexdigest()

    def a_dict(self):
        """
        Convierte el bloque a un diccionario serializable.
        """
        return {
            "timestamp": self.timestamp,
            "datos": self.datos,
            "alerta": self.alerta,
            "prev_hash": self.prev_hash,
            "hash": self.hash
        }
