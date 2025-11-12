# server_scraping.py
import argparse
import asyncio
import json
import logging
import uuid
from collections import deque
from datetime import datetime, timezone
from typing import Any, Dict, Optional, Tuple
from urllib.parse import urlparse

from aiohttp import web

from scraper.async_http import AsyncHTTPClient
from scraper.html_parser import parse_html
from common.protocol import async_send, async_recv  # utilidades para enviar/recibir mensajes length-prefixed

# Configuración básica
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("server_scraping")

# Valores por defecto
DEFAULT_TIMEOUT = 30
DEFAULT_WORKERS = 4
DEFAULT_CACHE_TTL = 3600  # 1 hora
DEFAULT_RATE_LIMIT = 30   # requests por minuto por dominio

# Límite de tamaño de payload/resultados en cache (evita consumir memoria indefinidamente)
MAX_CACHE_ITEM_BYTES = 5 * 1024 * 1024  # 5 MB (estimado)

# Stores en memoria (no persistentes). Protegidos por locks asíncronos.
_tasks: Dict[str, Dict[str, Any]] = {}
_tasks_lock = asyncio.Lock()

_cache: Dict[str, Tuple[float, Dict[str, Any]]] = {}
_cache_lock = asyncio.Lock()

_rate_buckets: Dict[str, deque] = {}
_rate_lock = asyncio.Lock()


# Comunicación con servidor de procesamiento (Parte B)
async def ask_processor(host: str, port: int, payload: dict, timeout: int = DEFAULT_TIMEOUT) -> dict:
    try:
        reader, writer = await asyncio.open_connection(host, port)
    except Exception as e:
        logger.error("No se pudo conectar al servidor de procesamiento %s:%s -> %s", host, port, e)
        return {"error": "processor_unreachable", "detail": str(e)}

    try:
        # Enviar y recibir con timeouts razonables
        await asyncio.wait_for(async_send(writer, payload), timeout=10)
        resp = await asyncio.wait_for(async_recv(reader), timeout=timeout)
        # Cerrar conexión ordenadamente
        try:
            writer.close()
            await writer.wait_closed()
        except Exception:
            pass
        # Aseguramos que la respuesta sea dict
        if isinstance(resp, dict):
            return resp
        # Si viene como JSON string/bytes, intentar parsear
        if isinstance(resp, (bytes, bytearray)):
            try:
                return json.loads(resp.decode("utf-8"))
            except Exception:
                return {"error": "invalid_processor_response", "raw": resp.decode("utf-8", errors="ignore")}
        try:
            return dict(resp)
        except Exception:
            return {"error": "invalid_processor_response", "detail": str(resp)}
    except asyncio.TimeoutError:
        logger.warning("Timeout esperando respuesta del procesador %s:%s", host, port)
        try:
            writer.close()
            await writer.wait_closed()
        except Exception:
            pass
        return {"error": "processor_timeout"}
    except Exception as e:
        logger.exception("Error en comunicación con procesador: %s", e)
        try:
            writer.close()
            await writer.wait_closed()
        except Exception:
            pass
        return {"error": "processor_error", "detail": str(e)}


# Cache y rate limiting simples
async def _increment_rate(domain: str, limit: int) -> bool:
    now = asyncio.get_event_loop().time()
    async with _rate_lock:
        dq = _rate_buckets.get(domain)
        if dq is None:
            dq = deque()
            _rate_buckets[domain] = dq
        # limpiar timestamps viejos (>60s)
        while dq and now - dq[0] > 60:
            dq.popleft()
        if len(dq) >= limit:
            return False
        dq.append(now)
        return True


async def _get_cached(url: str, ttl: int) -> Optional[Dict[str, Any]]:
    """Devuelve resultado cacheado si existe y no expiró, sino None."""
    async with _cache_lock:
        entry = _cache.get(url)
        if not entry:
            return None
        ts, result = entry
        now = asyncio.get_event_loop().time()
        if now - ts > ttl:
            # expiró
            try:
                del _cache[url]
            except KeyError:
                pass
            return None
        return result


async def _set_cache(url: str, result: Dict[str, Any]) -> None:
    """Guarda resultado en cache con timestamp actual. No cachea objetos demasiado grandes."""
    try:
        # Intentamos estimar tamaño en bytes de la representación JSON
        size = len(json.dumps(result, ensure_ascii=False).encode("utf-8"))
        if size > MAX_CACHE_ITEM_BYTES:
            logger.info("Resultado demasiado grande para cachear (%d bytes) url=%s", size, url)
            return
    except Exception:
        # Si falla la estimación, seguimos y guardamos de todos modos
        pass
    async with _cache_lock:
        _cache[url] = (asyncio.get_event_loop().time(), result)


# -------------------------
# Worker: toma tareas de la cola y procesa
# -------------------------
async def worker_loop(queue: asyncio.Queue, processor_host: str, processor_port: int, cache_ttl: int):
    """
    Loop de worker que:
    - obtiene tarea (task_id, url)
    - hace fetch asíncrono del HTML
    - parsea HTML
    - pide procesamiento al servidor B
    - consolida resultado, cachea y actualiza estado de la tarea
    """
    client = AsyncHTTPClient(timeout=DEFAULT_TIMEOUT)
    while True:
        task = await queue.get()
        if task is None:
            # Señal de terminación
            queue.task_done()
            break

        task_id = task.get("task_id")
        url = task.get("url")
        logger.info("Worker: procesando task %s url=%s", task_id, url)

        # Marcar scraping en progreso
        async with _tasks_lock:
            if task_id in _tasks:
                _tasks[task_id]["status"] = "scraping"
                _tasks[task_id]["updated_at"] = datetime.now(timezone.utc).isoformat()

        # Fetch HTML (manejo de errores)
        try:
            status_code, html = await client.fetch_text(url)
        except Exception as e:
            logger.exception("Error fetch_text para %s: %s", url, e)
            status_code, html = None, None

        if status_code is None or html is None:
            async with _tasks_lock:
                if task_id in _tasks:
                    _tasks[task_id]["status"] = "failed"
                    _tasks[task_id]["error"] = "fetch_error"
                    _tasks[task_id]["updated_at"] = datetime.now(timezone.utc).isoformat()
            queue.task_done()
            continue

        # Parse HTML (title, links, meta, structure, images_count)
        try:
            scraping_data = parse_html(html, url)
        except Exception as e:
            logger.exception("Error parseando HTML de %s: %s", url, e)
            scraping_data = {
                "title": "",
                "links": [],
                "meta_tags": {},
                "structure": {},
                "images_count": 0
            }

        # Enviar a servidor de procesamiento (Parte B)
        payload = {"url": url, "html": html, "timestamp": datetime.now(timezone.utc).isoformat()}
        processing_data = await ask_processor(processor_host, processor_port, payload)

        # Consolidar resultado final
        consolidated = {
            "url": url,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "scraping_data": {
                "title": scraping_data.get("title", ""),
                "links": scraping_data.get("links", []),
                "meta_tags": scraping_data.get("meta_tags", {}),
                "structure": scraping_data.get("structure", {}),
                "images_count": scraping_data.get("images_count", 0)
            },
            "processing_data": processing_data,
            "status": "success" if "error" not in processing_data else "partial"
        }

        # Guardar en cache y actualizar tarea
        try:
            await _set_cache(url, consolidated)
        except Exception:
            logger.exception("Error guardando en cache para %s", url)

        async with _tasks_lock:
            if task_id in _tasks:
                _tasks[task_id]["status"] = "completed" if "error" not in processing_data else "completed"
                _tasks[task_id]["result"] = consolidated
                _tasks[task_id]["updated_at"] = datetime.now(timezone.utc).isoformat()

        queue.task_done()


# Creación de tarea (rate limit, cache check, encolar)
async def create_task(queue: asyncio.Queue, url: str, rate_limit: int, cache_ttl: int) -> str:
    """
    Crea una tarea y la encola si no está cacheada.
    Devuelve task_id.
    Lanza web.HTTPTooManyRequests si se excede rate limit.
    """
    # Normalizar URL: si falta esquema, asumimos http
    parsed = urlparse(url)
    if not parsed.scheme:
        url = "http://" + url
        parsed = urlparse(url)

    domain = parsed.netloc.lower()
    allowed = await _increment_rate(domain, rate_limit)
    if not allowed:
        raise web.HTTPTooManyRequests(text=json.dumps({"error": "rate_limited", "domain": domain}), content_type="application/json")

    # Revisar cache
    cached = await _get_cached(url, cache_ttl)

    task_id = uuid.uuid4().hex
    now = datetime.now(timezone.utc).isoformat()
    async with _tasks_lock:
        _tasks[task_id] = {
            "task_id": task_id,
            "url": url,
            "status": "pending",
            "created_at": now,
            "updated_at": now,
            "result": None,
            "error": None
        }

    if cached:
        # Completar inmediatamente con cache
        async with _tasks_lock:
            _tasks[task_id]["status"] = "completed"
            _tasks[task_id]["result"] = cached
            _tasks[task_id]["updated_at"] = datetime.now(timezone.utc).isoformat()
        return task_id

    # Encolar para procesamiento por workers
    await queue.put({"task_id": task_id, "url": url})
    return task_id


# Handlers HTTP
async def handle_scrape(request: web.Request):
    """
    Soporta GET /scrape?url=... y POST /scrape with JSON {"url": "...", "wait": bool, "timeout": int}
    Si wait=true, espera hasta timeout (por defecto DEFAULT_TIMEOUT) y devuelve resultado final o 202 si no está listo.
    """
    # Obtener parámetros desde GET o POST JSON
    params = {}
    if request.method == "GET":
        params = dict(request.query)
    else:
        try:
            params = await request.json()
            if not isinstance(params, dict):
                params = dict(request.query)
        except Exception:
            params = dict(request.query)

    url = params.get("url")
    if not url:
        raise web.HTTPBadRequest(text=json.dumps({"error": "missing url"}), content_type="application/json")

    # Normalizar URL si falta esquema
    parsed = urlparse(url)
    if not parsed.scheme:
        url = "http://" + url

    wait = str(params.get("wait", "false")).lower() in ("1", "true", "yes")
    try:
        wait_timeout = int(params.get("timeout", DEFAULT_TIMEOUT))
    except Exception:
        wait_timeout = DEFAULT_TIMEOUT

    app = request.app
    queue: asyncio.Queue = app["queue"]
    rate_limit = int(app.get("rate_limit", DEFAULT_RATE_LIMIT))
    cache_ttl = int(app.get("cache_ttl", DEFAULT_CACHE_TTL))

    # Crear tarea (puede lanzar HTTPTooManyRequests)
    try:
        task_id = await create_task(queue, url, rate_limit, cache_ttl)
    except web.HTTPTooManyRequests:
        raise
    except Exception as e:
        logger.exception("Error creando tarea para %s: %s", url, e)
        raise web.HTTPInternalServerError(text=json.dumps({"error": "task_creation_failed", "detail": str(e)}), content_type="application/json")

    response = {"task_id": task_id, "status": "pending"}

    if wait:
        # Esperar hasta que la tarea esté completa o timeout
        start = asyncio.get_event_loop().time()
        while True:
            async with _tasks_lock:
                t = _tasks.get(task_id)
                if t and t.get("status") == "completed" and t.get("result") is not None:
                    return web.json_response(t["result"])
                if t and t.get("status") == "failed":
                    return web.json_response({"task_id": task_id, "status": "failed", "error": t.get("error")}, status=500)
            if asyncio.get_event_loop().time() - start > wait_timeout:
                break
            await asyncio.sleep(0.5)
        # Timeout esperando resultado
        response["status"] = "pending"
        return web.json_response(response, status=202)

    # Respuesta inmediata con task_id
    return web.json_response(response, status=202)


async def handle_status(request: web.Request):
    """Devuelve estado básico de la tarea."""
    task_id = request.match_info.get("task_id")
    async with _tasks_lock:
        t = _tasks.get(task_id)
        if not t:
            raise web.HTTPNotFound(text=json.dumps({"error": "task_not_found"}), content_type="application/json")
        return web.json_response({
            "task_id": task_id,
            "status": t["status"],
            "created_at": t["created_at"],
            "updated_at": t["updated_at"]
        })


async def handle_result(request: web.Request):
    """Devuelve resultado final si está completo, sino 202 con estado actual."""
    task_id = request.match_info.get("task_id")
    async with _tasks_lock:
        t = _tasks.get(task_id)
        if not t:
            raise web.HTTPNotFound(text=json.dumps({"error": "task_not_found"}), content_type="application/json")
        if t["status"] != "completed":
            return web.json_response({"task_id": task_id, "status": t["status"]}, status=202)
        return web.json_response(t["result"])


# Entrypoint / CLI
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Servidor de Scraping Web Asíncrono (con cola y cache)")
    parser.add_argument("-i", "--ip", required=True, help="Dirección de escucha (IPv4/IPv6)")
    parser.add_argument("-p", "--port", type=int, required=True, help="Puerto de escucha")
    parser.add_argument("-w", "--workers", type=int, default=DEFAULT_WORKERS, help="Número de workers de la cola")
    parser.add_argument("--processor-host", default="127.0.0.1", help="Host del servidor de procesamiento")
    parser.add_argument("--processor-port", type=int, default=9001, help="Puerto del servidor de procesamiento")
    parser.add_argument("--cache-ttl", type=int, default=DEFAULT_CACHE_TTL, help="TTL de cache en segundos")
    parser.add_argument("--rate-limit", type=int, default=DEFAULT_RATE_LIMIT, help="Rate limit por dominio (requests/min)")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    # Validaciones simples de argumentos
    if args.workers < 1:
        logger.warning("Workers < 1, ajustando a 1")
        args.workers = 1
    if args.cache_ttl < 0:
        args.cache_ttl = DEFAULT_CACHE_TTL
    if args.rate_limit < 1:
        args.rate_limit = DEFAULT_RATE_LIMIT

    app = web.Application()
    app["queue"] = asyncio.Queue()
    app["processor_host"] = args.processor_host
    app["processor_port"] = args.processor_port
    app["cache_ttl"] = args.cache_ttl
    app["rate_limit"] = args.rate_limit

    # Rutas
    app.router.add_route("GET", "/scrape", handle_scrape)
    app.router.add_route("POST", "/scrape", handle_scrape)
    app.router.add_get("/status/{task_id}", handle_status)
    app.router.add_get("/result/{task_id}", handle_result)

    # Startup: lanzar workers
    async def on_startup(app):
        workers = []
        for _ in range(args.workers):
            w = asyncio.create_task(worker_loop(app["queue"], app["processor_host"], app["processor_port"], app["cache_ttl"]))
            workers.append(w)
        app["workers_tasks"] = workers
        logger.info("Workers iniciados: %d", args.workers)
        logger.info("Procesador configurado en %s:%d", app["processor_host"], app["processor_port"])

    # Cleanup: señalizar a workers para terminar y esperar
    async def on_cleanup(app):
        logger.info("Señalando workers para terminar...")
        for _ in range(args.workers):
            await app["queue"].put(None)
        for w in app.get("workers_tasks", []):
            try:
                await w
            except Exception:
                pass
        logger.info("Workers finalizados")

    app.on_startup.append(on_startup)
    app.on_cleanup.append(on_cleanup)

    logger.info("Iniciando servidor de scraping en %s:%d", args.ip, args.port)
    # web.run_app maneja señales y soporta IPv4/IPv6 según el host pasado
    web.run_app(app, host=args.ip, port=args.port)


if __name__ == "__main__":
    main()
