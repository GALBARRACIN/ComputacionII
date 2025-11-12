# processor/image_processor.py
from typing import List, Tuple
from urllib.parse import urlparse
import io
import base64
import logging

import requests
from PIL import Image, ImageFile

# Permitir cargar imágenes truncadas en casos razonables
ImageFile.LOAD_TRUNCATED_IMAGES = True

logger = logging.getLogger("processor.image_processor")


# Helpers
def _b64(data: bytes) -> str:
    return base64.b64encode(data).decode("ascii")


# Función principal
def generate_thumbnails(
    image_urls: List[str],
    max_images: int = 3,
    size: Tuple[int, int] = (128, 128),
    max_bytes: int = 2 * 1024 * 1024,
    timeout: int = 10,
) -> List[str]:

    thumbs: List[str] = []
    if not image_urls:
        return thumbs

    headers = {"User-Agent": "TP2-Processor/1.0"}
    # Usamos Session para reusar conexiones
    with requests.Session() as session:
        session.headers.update(headers)

        for raw_url in image_urls[:max_images]:
            url = raw_url.strip()
            if not url:
                continue

            # Normalizar protocol-relative URLs y URLs sin esquema
            if url.startswith("//"):
                url = "http:" + url
            parsed = urlparse(url)
            if not parsed.scheme:
                url = "http://" + url

            try:
                # Petición en streaming para controlar el tamaño descargado
                resp = session.get(url, stream=True, timeout=(5, timeout))
                resp.raise_for_status()

                # Verificar content-type básico
                content_type = resp.headers.get("Content-Type", "").lower()
                if not content_type.startswith("image/"):
                    logger.debug("Omitiendo URL (no es imagen): %s (Content-Type=%s)", url, content_type)
                    resp.close()
                    continue

                # Si el servidor informa Content-Length y es demasiado grande, saltar
                cl = resp.headers.get("Content-Length")
                if cl:
                    try:
                        if int(cl) > max_bytes:
                            logger.debug("Omitiendo URL (Content-Length > max_bytes): %s (%s bytes)", url, cl)
                            resp.close()
                            continue
                    except Exception:
                        pass

                # Leer en chunks hasta max_bytes
                buf = io.BytesIO()
                total = 0
                for chunk in resp.iter_content(chunk_size=8192):
                    if not chunk:
                        break
                    total += len(chunk)
                    if total > max_bytes:
                        raise ValueError("image_too_large")
                    buf.write(chunk)
                resp.close()

                if buf.tell() == 0:
                    raise ValueError("empty_image")

                buf.seek(0)
                # Abrir imagen con PIL y generar thumbnail
                with Image.open(buf) as img:
                    img = img.convert("RGB")
                    img.thumbnail(size)
                    out = io.BytesIO()
                    img.save(out, format="PNG", optimize=True)
                    thumbs.append(_b64(out.getvalue()))

            except Exception as e:
                # No fallamos todo por una imagen; registramos y seguimos
                logger.debug("No se pudo procesar imagen %s: %s", url, e)
                continue

    return thumbs


__all__ = ["generate_thumbnails"]
