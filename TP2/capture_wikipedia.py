# capture_wikipedia.py
import os
import sys

_here = os.path.abspath(os.path.dirname(__file__))
_parent = os.path.abspath(os.path.join(_here, ".."))
if _here not in sys.path:
    sys.path.insert(0, _here)
if _parent not in sys.path:
    sys.path.insert(0, _parent)

import argparse
import json
import logging
import socket
import struct
import time
from typing import Dict, Any, Optional

from processor.screenshot import generate_screenshot_base64, save_base64_to_file

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("capture_wikipedia")


def parse_clip(s: Optional[str]) -> Optional[Dict[str, int]]:
    if not s:
        return None
    parts = [int(x) for x in s.split(",")]
    if len(parts) != 4:
        raise ValueError("Clip debe tener 4 valores: x,y,width,height")
    x, y, w, h = parts
    return {"x": x, "y": y, "width": w, "height": h}


def send_task_to_processor(host: str, port: int, payload: Dict[str, Any], sock_timeout: int = 300) -> Dict[str, Any]:

    data = json.dumps(payload).encode("utf-8")
    msg = struct.pack("!I", len(data)) + data
    logger.info("Connecting to processor %s:%d (socket timeout %ds)", host, port, sock_timeout)
    with socket.create_connection((host, port), timeout=10) as s:
        s.settimeout(sock_timeout)
        s.sendall(msg)
        # lee 4-byte length prefix
        raw = s.recv(4)
        if len(raw) < 4:
            raise RuntimeError("No se recibió prefijo de respuesta del procesador")
        length = struct.unpack("!I", raw)[0]
        logger.info("Esperando %d bytes de respuesta del procesador", length)
        resp = b""
        while len(resp) < length:
            chunk = s.recv(length - len(resp))
            if not chunk:
                break
            resp += chunk
        try:
            return json.loads(resp.decode("utf-8"))
        except Exception:
            return {"raw": resp.decode("utf-8")}


def main():
    parser = argparse.ArgumentParser(description="Capture Wikipedia locally and optionally send to processor")
    parser.add_argument("--url", default="https://es.wikipedia.org/wiki/Wikipedia", help="URL to capture")
    parser.add_argument("--output", default="wikipedia_shot.png", help="Output PNG file")
    parser.add_argument("--timeout-ms", type=int, default=120_000, help="Playwright timeout in ms")
    parser.add_argument("--full-page", action="store_true", help="Capture full page (off by default)")
    parser.add_argument("--clip", type=str, default=None, help="Clip region x,y,width,height (overrides full_page)")
    parser.add_argument("--headed", action="store_true", help="Open browser visible (headed)")

    # processor opciones 
    parser.add_argument("--send-to-processor", action="store_true", help="Send task to processing server")
    parser.add_argument("--processor-host", default="127.0.0.1", help="Processing server host")
    parser.add_argument("--processor-port", type=int, default=9001, help="Processing server port")
    parser.add_argument("--sock-timeout", type=int, default=300, help="Socket timeout seconds for processor response")
    args = parser.parse_args()

    clip = None
    if args.clip:
        try:
            clip = parse_clip(args.clip)
        except Exception as e:
            logger.error("Clip inválido: %s", e)
            sys.exit(2)

    logger.info("Starting local screenshot for %s", args.url)
    start = time.time()
    res = generate_screenshot_base64(
        args.url,
        timeout_ms=args.timeout_ms,
        full_page=args.full_page,
        viewport=(1280, 900),
        clip=clip,
        headless=not args.headed,
    )
    elapsed = time.time() - start
    logger.info("Local screenshot attempt finished in %.2f s", elapsed)

    if "data" in res:
        logger.info("Screenshot generated locally, saving to %s", args.output)
        try:
            save_base64_to_file(res["data"], args.output)
            logger.info("Saved: %s", args.output)
        except Exception as e:
            logger.exception("Failed to save local screenshot: %s", e)
    else:
        logger.warning("Local screenshot not generated: %s", res)

    if args.send_to_processor:
        payload = {"url": args.url}
        logger.info("Sending task to processor %s:%d", args.processor_host, args.processor_port)
        try:
            resp = send_task_to_processor(args.processor_host, args.processor_port, payload, sock_timeout=args.sock_timeout)
            logger.info("Processor response:\n%s", json.dumps(resp, indent=2, ensure_ascii=False))
            # Si processor regresa screenshot en base64, se guarda jeje :P
            ss = resp.get("screenshot")
            if isinstance(ss, dict) and ss.get("data"):
                out = args.output.replace(".png", "_from_processor.png")
                save_base64_to_file(ss["data"], out)
                logger.info("Saved processor screenshot to %s", out)
            elif isinstance(ss, str) and ss.strip():
                out = args.output.replace(".png", "_from_processor.png")
                save_base64_to_file(ss, out)
                logger.info("Saved processor screenshot to %s", out)
            else:
                logger.info("Processor did not return a screenshot field or it was empty")
        except Exception as e:
            logger.exception("Error sending task to processor: %s", e)
            sys.exit(3)


if __name__ == "__main__":
    main()
