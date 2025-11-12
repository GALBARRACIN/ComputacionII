# scraper/async_http.py
from typing import Tuple, Optional
import asyncio
import logging

import aiohttp
from aiohttp import ClientTimeout, TCPConnector, ClientError

logger = logging.getLogger("scraper.async_http")

DEFAULT_TIMEOUT = 30  # segundos
DEFAULT_LIMIT_PER_HOST = 5
DEFAULT_MAX_BYTES = 5 * 1024 * 1024  # 5 MB por descarga (para fetch_bytes)


# Funciones utilitarias simples
async def fetch_text(url: str, timeout: int = DEFAULT_TIMEOUT) -> Tuple[Optional[int], Optional[str]]:
    timeout_cfg = ClientTimeout(total=timeout)
    connector = TCPConnector(ssl=False, limit_per_host=DEFAULT_LIMIT_PER_HOST)
    try:
        async with aiohttp.ClientSession(timeout=timeout_cfg, connector=connector) as session:
            async with session.get(url) as resp:
                # Intentamos devolver el texto tal cual venga
                text = await resp.text()
                return resp.status, text
    except asyncio.TimeoutError:
        logger.debug("Timeout en fetch_text para %s", url)
        return None, None
    except ClientError as e:
        logger.debug("ClientError en fetch_text para %s: %s", url, e)
        return None, None
    except Exception as e:
        logger.debug("Error inesperado en fetch_text para %s: %s", url, e)
        return None, None


async def fetch_bytes(url: str, timeout: int = DEFAULT_TIMEOUT, max_bytes: int = DEFAULT_MAX_BYTES) -> Tuple[Optional[int], Optional[bytes]]:
    timeout_cfg = ClientTimeout(total=timeout)
    connector = TCPConnector(ssl=False, limit_per_host=DEFAULT_LIMIT_PER_HOST)
    try:
        async with aiohttp.ClientSession(timeout=timeout_cfg, connector=connector) as session:
            async with session.get(url) as resp:
                # Leer en chunks hasta max_bytes
                body = bytearray()
                async for chunk in resp.content.iter_chunked(8192):
                    if not chunk:
                        break
                    body.extend(chunk)
                    if len(body) > max_bytes:
                        logger.debug("fetch_bytes: contenido excede max_bytes para %s", url)
                        return None, None
                return resp.status, bytes(body)
    except asyncio.TimeoutError:
        logger.debug("Timeout en fetch_bytes para %s", url)
        return None, None
    except ClientError as e:
        logger.debug("ClientError en fetch_bytes para %s: %s", url, e)
        return None, None
    except Exception as e:
        logger.debug("Error inesperado en fetch_bytes para %s: %s", url, e)
        return None, None


# Clase para reusar sesión entre múltiples requests
class AsyncHTTPClient:
    def __init__(self, timeout: int = DEFAULT_TIMEOUT, limit_per_host: int = DEFAULT_LIMIT_PER_HOST, ssl: bool = False):
        self._timeout = ClientTimeout(total=timeout)
        self._connector = TCPConnector(limit_per_host=limit_per_host, ssl=ssl)
        self._session: Optional[aiohttp.ClientSession] = None
        self._closed = False

    async def _ensure_session(self) -> None:
        """Crea la sesión si no existe o está cerrada."""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(timeout=self._timeout, connector=self._connector)

    async def fetch_text(self, url: str) -> Tuple[Optional[int], Optional[str]]:
        """Versión reutilizable de fetch_text; mantiene la sesión abierta."""
        await self._ensure_session()
        try:
            async with self._session.get(url) as resp:
                text = await resp.text()
                return resp.status, text
        except asyncio.TimeoutError:
            logger.debug("Timeout en AsyncHTTPClient.fetch_text para %s", url)
            return None, None
        except ClientError as e:
            logger.debug("ClientError en AsyncHTTPClient.fetch_text para %s: %s", url, e)
            return None, None
        except Exception as e:
            logger.debug("Error inesperado en AsyncHTTPClient.fetch_text para %s: %s", url, e)
            return None, None

    async def fetch_bytes(self, url: str, max_bytes: int = DEFAULT_MAX_BYTES) -> Tuple[Optional[int], Optional[bytes]]:
        """Versión reutilizable de fetch_bytes con límite de tamaño."""
        await self._ensure_session()
        try:
            async with self._session.get(url) as resp:
                body = bytearray()
                async for chunk in resp.content.iter_chunked(8192):
                    if not chunk:
                        break
                    body.extend(chunk)
                    if len(body) > max_bytes:
                        logger.debug("AsyncHTTPClient.fetch_bytes: contenido excede max_bytes para %s", url)
                        return None, None
                return resp.status, bytes(body)
        except asyncio.TimeoutError:
            logger.debug("Timeout en AsyncHTTPClient.fetch_bytes para %s", url)
            return None, None
        except ClientError as e:
            logger.debug("ClientError en AsyncHTTPClient.fetch_bytes para %s: %s", url, e)
            return None, None
        except Exception as e:
            logger.debug("Error inesperado en AsyncHTTPClient.fetch_bytes para %s: %s", url, e)
            return None, None

    async def close(self) -> None:
        if self._session and not self._session.closed:
            try:
                await self._session.close()
            except Exception:
                pass
        self._closed = True

    async def __aenter__(self):
        await self._ensure_session()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()


__all__ = [
    "fetch_text",
    "fetch_bytes",
    "AsyncHTTPClient",
    "DEFAULT_TIMEOUT",
]
