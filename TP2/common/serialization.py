# common/serialization.py

from typing import Any
import json
import base64
import binascii

# JSON helpers
def to_json(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))


def from_json(s: str) -> Any:
    try:
        return json.loads(s)
    except json.JSONDecodeError as e:
        raise ValueError(f"invalid JSON: {e}") from e


# Base64 helpers
def bytes_to_b64(b: bytes) -> str:
    if not isinstance(b, (bytes, bytearray)):
        raise TypeError("bytes_to_b64 espera bytes o bytearray")
    return base64.b64encode(bytes(b)).decode("ascii")


def b64_to_bytes(s: str) -> bytes:
    if not isinstance(s, str):
        raise TypeError("b64_to_bytes espera una cadena str")
    try:
        return base64.b64decode(s.encode("ascii"), validate=True)
    except (binascii.Error, ValueError) as e:
        # binascii.Error para Python <3.9, ValueError para validate errors en algunas versiones
        raise ValueError(f"invalid base64 string: {e}") from e


# Export público
__all__ = [
    "to_json",
    "from_json",
    "bytes_to_b64",
    "b64_to_bytes",
]
