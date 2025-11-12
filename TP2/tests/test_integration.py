# tests/test_integration.py
import os
import subprocess
import sys
import time
import socket
from pathlib import Path

def wait_for_port(host: str, port: int, timeout: int = 30) -> bool:
    end = time.time() + timeout
    while time.time() < end:
        try:
            with socket.create_connection((host, port), timeout=1):
                return True
        except Exception:
            time.sleep(0.2)
    return False

def test_full_flow_processor_capture(tmp_path):
    host = "127.0.0.1"
    port = 9001
    server_cmd = [sys.executable, "server_processing.py", "-i", host, "-p", str(port), "-n", "1", "-t", "300"]
    server_proc = subprocess.Popen(server_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    try:
        assert wait_for_port(host, port, timeout=30), "El servidor de procesamiento no abrió el puerto en 30s"

        out_file = tmp_path / "wikipedia_shot_from_processor.png"
        capture_cmd = [
            sys.executable, "capture_wikipedia.py",
            "--url", "https://es.wikipedia.org/wiki/Wikipedia",
            "--send-to-processor",
            "--processor-host", host,
            "--processor-port", str(port),
            "--output", str(out_file),
        ]
        # Ejecutamos con un timeout amplio (600s) para dar margen
        proc = subprocess.run(capture_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=600)
        # Imprimimos salida para diagnóstico si pytest se queja
        print(proc.stdout)

        assert out_file.exists(), "El archivo de salida del procesador no fue creado"
        assert out_file.stat().st_size > 0, "El archivo creado por el procesador está vacío"
    finally:
        # Terminamos el servidor
        try:
            server_proc.terminate()
            server_proc.wait(timeout=5)
        except Exception:
            try:
                server_proc.kill()
            except Exception:
                pass
