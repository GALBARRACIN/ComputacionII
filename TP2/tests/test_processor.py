# tests/test_processor.py
import json
import socket
import tempfile
from pathlib import Path

def pack_message(body_bytes: bytes) -> bytes:
    length = len(body_bytes)
    return length.to_bytes(4, "big") + body_bytes

def recvall(sock: socket.socket, n: int) -> bytes:
    data = bytearray()
    while len(data) < n:
        chunk = sock.recv(n - len(data))
        if not chunk:
            break
        data.extend(chunk)
    return bytes(data)

def test_processor_tcp(processor_server, tmp_path):
    host = processor_server["host"]
    port = processor_server["port"]
    payload = {"url": "https://es.wikipedia.org/wiki/Wikipedia"}
    body = json.dumps(payload).encode("utf-8")
    msg = pack_message(body)

    with socket.create_connection((host, port), timeout=10) as s:
        s.settimeout(120)
        s.sendall(msg)
        # leer prefijo de 4 bytes
        header = recvall(s, 4)
        assert header and len(header) == 4, "No se recibió prefijo de respuesta"
        length = int.from_bytes(header, "big")
        resp_bytes = recvall(s, length)
        assert resp_bytes and len(resp_bytes) == length, "Respuesta incompleta del processor"
        resp = json.loads(resp_bytes.decode("utf-8"))
        # Debe contener al menos 'screenshot' y 'status' o un error claro
        assert isinstance(resp, dict)
        assert "screenshot" in resp or "error" in resp
        # Si hay screenshot con data, guardarla y comprobar tamaño
        ss = resp.get("screenshot")
        if isinstance(ss, dict) and ss.get("data"):
            out = tmp_path / "proc_shot.png"
            out.write_bytes(__import__("base64").b64decode(ss["data"]))
            assert out.stat().st_size > 0
