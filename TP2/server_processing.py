# server_processing.py
import argparse
import json
import logging
import os
import signal
import socket
import socketserver
import sys
import time
import traceback
from concurrent.futures import ProcessPoolExecutor, TimeoutError as FutureTimeoutError
from typing import Dict, Any, List, Optional

# Intentamos importar utilidades comunes; si no existen, definimos implementaciones sencillas
try:
    from common.protocol import recvall, pack_message, unpack_message_bytes  # se asume que existen
except Exception:
    # Implementaciones fallback mínimas para que el servidor funcione sin dependencia externa.
    def recvall(conn: socket.socket, n: int) -> bytes:

        data = bytearray()
        while len(data) < n:
            chunk = conn.recv(n - len(data))
            if not chunk:
                break
            data.extend(chunk)
        return bytes(data)

    def pack_message(body_bytes: bytes) -> bytes:

        if not isinstance(body_bytes, (bytes, bytearray)):
            try:
                body_bytes = json.dumps(body_bytes, ensure_ascii=False).encode("utf-8")
            except Exception:
                body_bytes = b""
        length = len(body_bytes)
        return length.to_bytes(4, "big") + body_bytes

    def unpack_message_bytes(body: bytes):

        try:
            return json.loads(body.decode("utf-8"))
        except Exception:
            return body

# Importamos funciones de procesamiento desde el paquete processor.
# Se asume que processor.__init__ expone generate_screenshot (wrapper) y las demás funciones.
try:
    # Preferimos el wrapper si existe
    from processor import generate_screenshot  # wrapper que delega a generate_screenshot_base64
except Exception:
    # Si no existe el wrapper, intentamos importar la función base
    try:
        from processor.screenshot import generate_screenshot_base64 as _gsb

        def generate_screenshot(url: str, **kwargs):
            """Adaptador si solo existe generate_screenshot_base64"""
            return _gsb(url, **kwargs)
    except Exception:
        # Si no hay ninguna función, definimos un stub que lanza error para que quede claro en logs.
        def generate_screenshot(url: str, **kwargs):
            raise RuntimeError("generate_screenshot no disponible en el paquete processor")

try:
    from processor.performance import analyze_performance
except Exception:
    def analyze_performance(url: str) -> Dict[str, Any]:
        return {"error": "analyze_performance_not_available"}

try:
    from processor.image_processor import generate_thumbnails
except Exception:
    def generate_thumbnails(image_urls: List[str], max_images: int = 3) -> List[Dict[str, Any]]:
        return [{"error": "generate_thumbnails_not_available"}]


# Configuración básica de logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("server_processing")

# Límite razonable para payloads (10 MB)
MAX_PAYLOAD_BYTES = 10 * 1024 * 1024



# Función que corre en procesos del pool
def process_task(payload: Dict[str, Any]) -> Dict[str, Any]:

    start_total = time.time()
    try:
        url = payload.get("url", "")
        html = payload.get("html", "") or ""
        # Extraer imágenes de forma simple desde el HTML (regex rápido)
        image_urls: List[str] = []
        try:
            import re
            image_urls = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html, flags=re.IGNORECASE)
        except Exception:
            image_urls = []

        # Ejecutar tareas CPU/IO intensivas (estas funciones deben ser seguras para multiprocessing)
        screenshot_res = None
        perf = None
        thumbs = []

        # Intentamos generar screenshot; generate_screenshot puede devolver dict con 'data' o 'error'
        try:
            # Forzamos captura de viewport (no full_page) para que sea más rápida por defecto
            screenshot_res = generate_screenshot(
                url,
                timeout_ms=180_000,  # 180s para dar margen
                full_page=False,
                viewport=(1280, 900),
                headless=True
            )
        except Exception as e:
            screenshot_res = {"error": f"screenshot_failed: {str(e)}", "detail": traceback.format_exc()}

        try:
            perf = analyze_performance(url)
        except Exception as e:
            perf = {"error": f"performance_failed: {str(e)}", "detail": traceback.format_exc()}

        try:
            thumbs = generate_thumbnails(image_urls, max_images=3)
        except Exception as e:
            thumbs = [{"error": f"thumbnails_failed: {str(e)}", "detail": traceback.format_exc()}]

        total_time = round(time.time() - start_total, 2)
        return {
            "screenshot": screenshot_res,
            "performance": perf,
            "thumbnails": thumbs,
            "status": "ok",
            "processing_time_s": total_time
        }
    except Exception as e:
        # Capturamos cualquier excepción inesperada y la devolvemos como error
        return {"error": "process_task_exception", "detail": str(e), "traceback": traceback.format_exc()}


# Handler TCP por conexión
class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    pool: Optional[ProcessPoolExecutor] = None
    task_timeout_seconds: int = 180  # tiempo por defecto que esperamos por la tarea del pool

    def _send_response(self, conn: socket.socket, obj: Dict[str, Any]) -> None:
        """
        Serializa obj a JSON y lo envía con prefijo de 4 bytes.
        """
        try:
            # pack_message puede aceptar dicts o bytes; si devuelve bytes, lo usamos tal cual
            body = pack_message(obj)
            if not isinstance(body, (bytes, bytearray)):
                # Si pack_message devolvió una estructura no-bytes, serializamos nosotros
                body = json.dumps(body, ensure_ascii=False).encode("utf-8")
        except Exception:
            # Fallback: serializamos nosotros mismos
            body = json.dumps(obj, ensure_ascii=False).encode("utf-8")

        # Detectar si body ya tiene prefijo de 4 bytes correcto
        if len(body) >= 4:
            try:
                pref_len = int.from_bytes(body[:4], "big")
                if pref_len == len(body) - 4:
                    # Ya está prefijado, enviamos tal cual
                    conn.sendall(body)
                    return
            except Exception:
                # Si falla la detección, continuamos y prefijamos manualmente
                pass

        # Si no estaba prefijado, lo prefijamos aquí
        length_prefix = len(body).to_bytes(4, "big")
        conn.sendall(length_prefix + body)

    def handle(self) -> None:
        conn: socket.socket = self.request
        addr = self.client_address
        # Ponemos un timeout razonable para evitar sockets colgados indefinidamente
        # Este timeout es solo para operaciones de recv; la espera por la tarea del pool se controla aparte.
        conn.settimeout(300)
        logger.info("Conexión entrante desde %s:%s", addr[0], addr[1])

        try:
            # Leer header (4 bytes) y luego el body
            header = recvall(conn, 4)
            if not header or len(header) < 4:
                logger.warning("Header incompleto desde %s:%s", addr[0], addr[1])
                return
            length = int.from_bytes(header, "big")
            if length <= 0 or length > MAX_PAYLOAD_BYTES:
                logger.warning("Payload con longitud inválida (%d) desde %s:%s", length, addr[0], addr[1])
                # Enviar respuesta de error
                err = {"error": "invalid_payload_length", "length": length}
                self._send_response(conn, err)
                return

            body = recvall(conn, length)
            if not body or len(body) != length:
                logger.warning("Body incompleto (esperado %d, recibido %d) desde %s:%s", length, len(body or b""), addr[0], addr[1])
                err = {"error": "incomplete_body"}
                self._send_response(conn, err)
                return

            # Deserializar payload (se espera JSON o estructura manejable por unpack_message_bytes)
            try:
                payload = unpack_message_bytes(body)
                if isinstance(payload, (bytes, bytearray)):
                    # Si unpack devuelve bytes, intentamos decodificar JSON
                    payload = json.loads(payload.decode("utf-8"))
                elif not isinstance(payload, dict):
                    # Si no es dict, intentamos parsear como JSON string o convertir a dict
                    payload = json.loads(json.dumps(payload))
            except Exception as e:
                logger.exception("Error deserializando payload desde %s:%s: %s", addr[0], addr[1], e)
                err = {"error": "invalid_json_payload", "detail": str(e)}
                self._send_response(conn, err)
                return

        except socket.timeout:
            logger.warning("Timeout leyendo datos desde %s:%s", addr[0], addr[1])
            return
        except Exception as e:
            logger.exception("Error leyendo payload desde %s:%s: %s", addr[0], addr[1], e)
            return

        # Enviar la tarea al pool de procesos
        if not self.pool:
            logger.error("Pool de procesos no inicializado")
            self._send_response(conn, {"error": "server_not_ready"})
            return

        try:
            future = self.pool.submit(process_task, payload)
            # Esperamos el resultado (bloqueante en este hilo, pero el trabajo se hace en procesos)
            try:
                result = future.result(timeout=getattr(self, "task_timeout_seconds", 180))
            except FutureTimeoutError:
                # Intentamos cancelar la tarea y devolvemos un error claro
                try:
                    future.cancel()
                except Exception:
                    pass
                logger.warning("Timeout procesando tarea para URL=%s (esperado %ds)", payload.get("url"), getattr(self, "task_timeout_seconds", 180))
                result = {"error": "processor_timeout", "detail": f"task exceeded {getattr(self, 'task_timeout_seconds', 180)} seconds"}
        except Exception as e:
            logger.exception("Error ejecutando process_task: %s", e)
            result = {"error": "processing_failed", "detail": str(e)}

        # Enviar respuesta al cliente (length-prefixed)
        try:
            self._send_response(conn, result)
        except Exception as e:
            logger.exception("Error enviando respuesta a %s:%s: %s", addr[0], addr[1], e)


# Servidor TCP con hilos para aceptar conexiones
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    daemon_threads = True  # hilos hijos terminan cuando el servidor se apaga


# Entrypoint / CLI
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Servidor de Procesamiento Distribuido (Parte B)")
    parser.add_argument("-i", "--ip", default="127.0.0.1", help="Dirección de escucha (IPv4 o IPv6)")
    parser.add_argument("-p", "--port", type=int, default=9001, help="Puerto de escucha")
    parser.add_argument("-n", "--processes", type=int, default=None, help="Número de procesos en el pool (default: CPU count - 1)")
    parser.add_argument("-t", "--task-timeout", type=int, default=180, help="Timeout (s) para esperar la finalización de cada tarea del pool")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    host = args.ip
    port = args.port
    # Determinamos número de procesos por defecto: CPU count - 1 (mínimo 1)
    num_procs = args.processes or max(1, (os.cpu_count() or 2) - 1)
    task_timeout = args.task_timeout

    logger.info("Inicializando pool de procesos con %d workers", num_procs)
    pool = ProcessPoolExecutor(max_workers=num_procs)
    ThreadedTCPRequestHandler.pool = pool
    ThreadedTCPRequestHandler.task_timeout_seconds = task_timeout

    server = ThreadedTCPServer((host, port), ThreadedTCPRequestHandler)
    logger.info("Servidor de procesamiento escuchando en %s:%d", host, port)

    # Manejo de señales para apagado ordenado (Unix y Windows manejan KeyboardInterrupt)
    def _shutdown(signum=None, frame=None):
        logger.info("Señal de apagado recibida, cerrando servidor...")
        try:
            server.shutdown()
        except Exception:
            pass
        try:
            server.server_close()
        except Exception:
            pass
        try:
            pool.shutdown(wait=True)
        except Exception:
            pass
        logger.info("Servidor detenido.")
        # No forzamos sys.exit aquí para permitir limpieza en finally

    try:
        signal.signal(signal.SIGINT, _shutdown)
        # SIGTERM puede no estar disponible en Windows; lo intentamos en sistemas que lo soporten
        if hasattr(signal, "SIGTERM"):
            signal.signal(signal.SIGTERM, _shutdown)
    except Exception:
        # En algunos entornos (ej: Windows con ciertas restricciones) puede fallar; no crítico
        pass

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("Interrupción por teclado, apagando...")
    finally:
        logger.info("Apagando servidor y pool de procesos...")
        try:
            server.shutdown()
        except Exception:
            pass
        try:
            server.server_close()
        except Exception:
            pass
        try:
            pool.shutdown(wait=True)
        except Exception:
            pass
        logger.info("Servidor detenido.")


if __name__ == "__main__":
    main()

