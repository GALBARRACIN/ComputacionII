# scraper/html_parser.py
from typing import Dict, List, Any, Set, Tuple
from urllib.parse import urljoin, urldefrag
from bs4 import BeautifulSoup

from .metadata_extractor import extract_meta  # función que extrae meta tags desde el soup


def _is_valid_href(href: str) -> bool:
    # Filtra hrefs no útiles (mailto, tel, javascript, vacíos, fragments puros).
    if not href:
        return False
    href = href.strip()
    if not href:
        return False
    low = href.lower()
    if low.startswith(("mailto:", "tel:", "javascript:")):
        return False
    # fragmentos puros como "#section" no son útiles como enlaces externos
    if href.startswith("#"):
        return False
    return True


def _normalize_and_defragment(href: str, base: str) -> str:

    try:
        abs_url = urljoin(base, href)
        # urldefrag devuelve (url_sin_fragmento, fragmento)
        clean, _ = urldefrag(abs_url)
        return clean
    except Exception:
        return href


def _dedupe_preserve_order(items: List[str]) -> List[str]:
    # Elimina duplicados
    seen: Set[str] = set()
    out: List[str] = []
    for it in items:
        if it not in seen:
            seen.add(it)
            out.append(it)
    return out


def parse_html(html: str, base_url: str) -> Dict[str, Any]:

    # Intentamos usar lxml y caemos a html.parser si no está disponible
    try:
        soup = BeautifulSoup(html, "lxml")
    except Exception:
        soup = BeautifulSoup(html, "html.parser")

    # Título (robusto ante ausencia)
    title = ""
    try:
        if soup.title and soup.title.string:
            title = soup.title.string.strip()
    except Exception:
        title = ""

    # Enlaces: filtrar, normalizar y deduplicar
    raw_links: List[str] = []
    try:
        for a in soup.find_all("a", href=True):
            try:
                href = a.get("href")
                if not _is_valid_href(href):
                    continue
                abs_href = _normalize_and_defragment(href, base_url)
                raw_links.append(abs_href)
            except Exception:
                # ignoramos enlaces problemáticos
                continue
    except Exception:
        raw_links = []

    links = _dedupe_preserve_order(raw_links)

    # Meta tags: delegamos en metadata_extractor (debe manejar soup)
    try:
        meta_tags = extract_meta(soup)
    except Exception:
        meta_tags = {}

    # Imágenes: obtener src, normalizar y deduplicar; ignorar data: URIs
    raw_images: List[str] = []
    try:
        for img in soup.find_all("img", src=True):
            try:
                src = img.get("src")
                if not src:
                    continue
                src = src.strip()
                if src.lower().startswith("data:"):
                    # ignorar imágenes embebidas en base64
                    continue
                abs_src = _normalize_and_defragment(src, base_url)
                raw_images.append(abs_src)
            except Exception:
                continue
    except Exception:
        raw_images = []

    images = _dedupe_preserve_order(raw_images)
    images_count = len(images)

    # Estructura: conteo de headers H1..H6
    structure = {}
    try:
        for i in range(1, 7):
            structure[f"h{i}"] = len(soup.find_all(f"h{i}"))
    except Exception:
        # en caso de error, devolver 0s
        structure = {f"h{i}": 0 for i in range(1, 7)}

    return {
        "title": title,
        "links": links,
        "meta_tags": meta_tags,
        "structure": structure,
        "images_count": images_count,
        "images": images,
    }
