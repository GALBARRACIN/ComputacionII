# common/protocol.py
from typing import Any, Optional
import json
import struct
import asyncio
import logging
import socket

logger = logging.getLogger("common.protocol")

# Tamaño máximo por defecto para evitar lecturas/explosiones de memoria (10 MB)
DEFAULT_MAX_MESSAGE = 10 * 1024 * 1024

# Serialización / empaquetado
def pack_message(obj: Any) -> bytes:
    if isinstance(obj, (bytes, bytearray)):
        data = bytes(obj)
    else:
        try:
            # compact JSON pero legible; ensure_ascii=False para soportar UTF-8
            data = json.dumps(obj, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        except Exception:
            # Fallback: convertir a string si no es serializable
            data = str(obj).encode("utf-8")
    length_prefix = struct.pack(">I", len(data))
    return length_prefix + data


def unpack_message_bytes(b: bytes) -> Any:
    if not isinstance(b, (bytes, bytearray)):
        raise TypeError("unpack_message_bytes espera bytes")
    try:
        return json.loads(b.decode("utf-8"))
    except json.JSONDecodeError as e:
        # Propagamos un error claro para que el caller lo maneje
        raise ValueError(f"invalid JSON payload: {e}") from e


# Lectura sincrónica desde socket
def recvall(sock: socket.socket, n: int, timeout: Optional[float] = None) -> bytes:

    if n <= 0:
        return b""
    data = bytearray()
    # Guardamos el timeout original y lo restauramos al final
    orig_timeout = sock.gettimeout()
    try:
        if timeout is not None:
            sock.settimeout(timeout)
        while len(data) < n:
            try:
                chunk = sock.recv(n - len(data))
            except socket.timeout:
                raise TimeoutError("socket read timeout")
            if not chunk:
                raise ConnectionError("socket closed while reading")
            data.extend(chunk)
    finally:
        try:
            sock.settimeout(orig_timeout)
        except Exception:
            pass
    return bytes(data)


def recv_message(sock: socket.socket, max_size: int = DEFAULT_MAX_MESSAGE, timeout: Optional[float] = None) -> Any:
    header = recvall(sock, 4, timeout=timeout)
    if len(header) < 4:
        raise ConnectionError("incomplete header")
    length = int.from_bytes(header, "big")
    if length < 0 or length > max_size:
        raise ValueError(f"invalid message length: {length}")
    body = recvall(sock, length, timeout=timeout)
    return unpack_message_bytes(body)



# Helpers asíncronos para StreamReader/StreamWriter
async def async_send(writer: asyncio.StreamWriter, obj: Any) -> None:

    if isinstance(obj, (bytes, bytearray)):
        data = bytes(obj)
    else:
        try:
            data = json.dumps(obj, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        except Exception:
            data = str(obj).encode("utf-8")
    writer.write(len(data).to_bytes(4, "big") + data)
    try:
        await writer.drain()
    except ConnectionResetError:
        # El receptor cerró la conexión
        raise


async def async_recv(reader: asyncio.StreamReader, max_size: int = DEFAULT_MAX_MESSAGE) -> Any:

    # readexactly lanzará IncompleteReadError si no alcanza los bytes
    header = await reader.readexactly(4)
    length = int.from_bytes(header, "big")
    if length < 0 or length > max_size:
        raise ValueError(f"invalid message length: {length}")
    body = await reader.readexactly(length)
    try:
        return json.loads(body.decode("utf-8"))
    except json.JSONDecodeError as e:
        raise ValueError(f"invalid JSON payload: {e}") from e


# Export público
__all__ = [
    "pack_message",
    "unpack_message_bytes",
    "recvall",
    "recv_message",
    "async_send",
    "async_recv",
    "DEFAULT_MAX_MESSAGE",
]
