# tests/conftest.py
import os
import signal
import socket
import subprocess
import sys
import time
from pathlib import Path
import pytest

HOST = "127.0.0.1"

def wait_for_port(host: str, port: int, timeout: int = 30) -> bool:
    end = time.time() + timeout
    while time.time() < end:
        try:
            with socket.create_connection((host, port), timeout=1):
                return True
        except Exception:
            time.sleep(0.2)
    return False

def _start_process(cmd, cwd=None, env=None, stdout=None):
    return subprocess.Popen(
        cmd,
        cwd=cwd,
        env=env,
        stdout=stdout or subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

@pytest.fixture(scope="session")
def processor_server(tmp_path_factory):
    tmpdir = tmp_path_factory.mktemp("processor_logs")
    log_file = tmpdir / "processor.log"
    port = 9001
    cmd = [sys.executable, "server_processing.py", "-i", HOST, "-p", str(port), "-n", "1", "-t", "300"]
    with open(log_file, "w", encoding="utf-8") as lf:
        proc = _start_process(cmd, stdout=lf)
    try:
        assert wait_for_port(HOST, port, timeout=30), f"processor no abrió puerto {port}"
        yield {"host": HOST, "port": port, "proc": proc, "log": str(log_file)}
    finally:
        try:
            proc.terminate()
            proc.wait(timeout=5)
        except Exception:
            try:
                proc.kill()
            except Exception:
                pass

@pytest.fixture(scope="session")
def scraper_server(processor_server, tmp_path_factory):
    tmpdir = tmp_path_factory.mktemp("scraper_logs")
    log_file = tmpdir / "scraper.log"
    port = 8000
    proc_host = processor_server["host"]
    proc_port = processor_server["port"]
    cmd = [
        sys.executable, "server_scraping.py",
        "-i", HOST, "-p", str(port),
        "--processor-host", str(proc_host), "--processor-port", str(proc_port)
    ]
    with open(log_file, "w", encoding="utf-8") as lf:
        proc = _start_process(cmd, stdout=lf)
    try:
        assert wait_for_port(HOST, port, timeout=30), f"scraper no abrió puerto {port}"
        yield {"base_url": f"http://{HOST}:{port}", "proc": proc, "log": str(log_file)}
    finally:
        try:
            proc.terminate()
            proc.wait(timeout=5)
        except Exception:
            try:
                proc.kill()
            except Exception:
                pass
