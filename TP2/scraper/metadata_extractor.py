# scraper/metadata_extractor.py
from typing import Dict
import logging

from bs4 import BeautifulSoup

logger = logging.getLogger("scraper.metadata_extractor")


def extract_meta(soup: BeautifulSoup) -> Dict[str, str]:

    metas: Dict[str, str] = {}

    try:
        for tag in soup.find_all("meta"):
            key = None
            # Preferir name, luego property, luego itemprop
            if tag.get("name"):
                key = tag.get("name").strip().lower()
            elif tag.get("property"):
                key = tag.get("property").strip().lower()
            elif tag.get("itemprop"):
                key = tag.get("itemprop").strip().lower()

            if not key:
                continue

            # content puede venir en distintos atributos según el HTML
            content = tag.get("content") or tag.get("value") or ""
            content = content.strip()
            if not content:
                continue

            # Si ya existe la key, concatenamos evitando duplicados exactos
            if key in metas:
                if content not in metas[key].split("; "):
                    metas[key] = metas[key] + "; " + content
            else:
                metas[key] = content
    except Exception as e:
        # No queremos que un meta mal formado rompa el parser completo
        logger.debug("Error extrayendo meta tags: %s", e)

    # Normalizar salida: siempre incluir description y keywords
    normalized: Dict[str, str] = {
        "description": metas.get("description", ""),
        "keywords": metas.get("keywords", ""),
    }

    # Incluir Open Graph y Twitter cards tal cual (og:*, twitter:*)
    for k, v in metas.items():
        if k.startswith("og:") or k.startswith("twitter:"):
            normalized[k] = v

    return normalized


__all__ = ["extract_meta"]
