# scraper/__init__.py
from __future__ import annotations

import logging

from .async_http import AsyncHTTPClient, fetch_text, fetch_bytes
from .html_parser import parse_html
from .metadata_extractor import extract_meta

__all__ = ["AsyncHTTPClient", "fetch_text", "fetch_bytes", "parse_html", "extract_meta"]

__version__ = "0.1.0"

# Logger local para el paquete scraper
logger = logging.getLogger("tp2.scraper")
