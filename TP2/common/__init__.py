# common/__init__.py
from __future__ import annotations

import logging

# Re-exportar funciones útiles desde submódulos
from .protocol import (
    pack_message,
    unpack_message_bytes,
    recvall,
    recv_message,
    async_send,
    async_recv,
    DEFAULT_MAX_MESSAGE,
)
from .serialization import (
    to_json,
    from_json,
    bytes_to_b64,
    b64_to_bytes,
)

# Versión del paquete (útil para debugging)
__version__ = "0.1.0"

# Logger local para el paquete
logger = logging.getLogger("tp2.common")

# Qué se exporta cuando se hace `from common import *`
__all__ = [
    "pack_message",
    "unpack_message_bytes",
    "recvall",
    "recv_message",
    "async_send",
    "async_recv",
    "DEFAULT_MAX_MESSAGE",
    "to_json",
    "from_json",
    "bytes_to_b64",
    "b64_to_bytes",
    "__version__",
    "logger",
]
