# processor/performance.py
import time
import logging
from typing import Dict, List
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger("processor.performance")

# Valores por defecto y límites razonables
DEFAULT_TIMEOUT = 15          # timeout total para la petición principal (segundos)
RESOURCE_TIMEOUT = 5         # timeout para HEAD/GET de recursos (segundos)
MAX_RESOURCES = 50           # máximo de recursos a analizar para evitar explosión de requests
MAX_RESOURCE_BYTES = 2 * 1024 * 1024  # 2 MB por recurso (lectura máxima)

# User-Agent sencillo para requests
DEFAULT_HEADERS = {"User-Agent": "TP2-Processor/1.0"}


def _gather_resource_urls(soup: BeautifulSoup, base_url: str, max_items: int) -> List[str]:
    seen = set()
    resources: List[str] = []

    def add(url: str):
        if not url:
            return
        full = urljoin(base_url, url)
        if full not in seen:
            seen.add(full)
            resources.append(full)

    # imágenes
    for tag in soup.find_all("img", src=True):
        add(tag.get("src"))

    # scripts
    for tag in soup.find_all("script", src=True):
        add(tag.get("src"))

    # hojas de estilo
    for tag in soup.find_all("link", href=True):
        rel = tag.get("rel") or []
        # normalizar rel a lista de strings en minúsculas
        if isinstance(rel, list):
            rels = [r.lower() for r in rel]
        else:
            rels = [str(rel).lower()]
        if "stylesheet" in rels or "stylesheet" in (tag.get("type") or "").lower():
            add(tag.get("href"))

    # limitar
    if len(resources) > max_items:
        return resources[:max_items]
    return resources


def _get_resource_size(session: requests.Session, url: str, timeout: int, max_bytes: int) -> int:
    try:
        # HEAD primero
        head = session.head(url, timeout=timeout, allow_redirects=True)
        head.raise_for_status()
        cl = head.headers.get("Content-Length")
        if cl:
            try:
                size = int(cl)
                if size >= 0:
                    return size
            except Exception:
                pass
        # Si no hay Content-Length o es 0, hacer GET en streaming
        resp = session.get(url, stream=True, timeout=timeout, allow_redirects=True)
        resp.raise_for_status()
        total = 0
        for chunk in resp.iter_content(chunk_size=8192):
            if not chunk:
                break
            total += len(chunk)
            if total > max_bytes:
                # cortamos si excede el límite razonable
                resp.close()
                raise ValueError("resource_too_large")
        resp.close()
        return total
    except Exception as e:
        # No queremos que un recurso falle la medición completa
        logger.debug("No se pudo obtener tamaño recurso %s: %s", url, e)
        return 0


def analyze_performance(url: str, timeout: int = DEFAULT_TIMEOUT) -> Dict:
    start = time.perf_counter()
    total_bytes = 0
    num_requests = 0

    session = requests.Session()
    session.headers.update(DEFAULT_HEADERS)

    try:
        # Petición principal (HTML)
        resp = session.get(url, timeout=timeout, allow_redirects=True)
        resp.raise_for_status()
        main_content = resp.content or b""
        main_size = len(main_content)
        total_bytes += main_size
        num_requests += 1

        # Parsear HTML para extraer recursos
        try:
            soup = BeautifulSoup(resp.text, "lxml")
        except Exception:
            soup = BeautifulSoup(resp.text, "html.parser")

        resources = _gather_resource_urls(soup, url, MAX_RESOURCES)

        # Iterar recursos y estimar tamaño
        for res_url in resources:
            # Para no exceder el número de requests, respetamos MAX_RESOURCES
            size = _get_resource_size(session, res_url, timeout=RESOURCE_TIMEOUT, max_bytes=MAX_RESOURCE_BYTES)
            if size:
                total_bytes += size
            # Contamos el intento como una request (HEAD o GET)
            num_requests += 1

        load_ms = int((time.perf_counter() - start) * 1000)
        return {
            "load_time_ms": load_ms,
            "total_size_kb": max(0, total_bytes // 1024),
            "num_requests": num_requests
        }
    except requests.RequestException as e:
        logger.debug("Error en requests para %s: %s", url, e)
        return {"error": "perf_failed", "detail": str(e)}
    except Exception as e:
        logger.exception("Error inesperado en analyze_performance: %s", e)
        return {"error": "perf_failed", "detail": str(e)}
    finally:
        try:
            session.close()
        except Exception:
            pass
