# tests/test_scraper.py
import json
import time
import requests
from pathlib import Path

def test_scraper_end_to_end(scraper_server, tmp_path):
    """
    Test end-to-end del scrapper:
    - POST /scrape -> acepta 200 o 202 y extrae task_id (body JSON o Location header)
    - Poll /status/{task} hasta completed/partial/failed
    - GET /result/{task} y validar contenido
    """
    base = scraper_server["base_url"]
    url = "https://es.wikipedia.org/wiki/Wikipedia"

    # Enviar la petición de scrape
    r = requests.post(f"{base}/scrape", json={"url": url}, timeout=30)

    # Aceptamos 200 (sincrónico) o 202 (aceptado, asíncrono)
    assert r.status_code in (200, 202), f"Respuesta inesperada {r.status_code}: {r.text}"

    # Intentar extraer task_id desde JSON
    task_id = None
    try:
        if r.headers.get("content-type", "").lower().startswith("application/json"):
            body = r.json()
            task_id = body.get("task_id") or body.get("id") or body.get("task")
    except Exception:
        body = None

    # Si no está en el body, intentar Location header
    if not task_id:
        loc = r.headers.get("Location") or r.headers.get("location")
        if loc:
            task_id = loc.rstrip("/").split("/")[-1]

    assert task_id, f"No se encontró task_id en body ni Location. Resp: {r.status_code} {r.text}"

    # Polling hasta estado final (con timeout total)
    deadline = time.time() + 180
    status = None
    while time.time() < deadline:
        s = requests.get(f"{base}/status/{task_id}", timeout=10)
        assert s.status_code == 200, f"/status devolvió {s.status_code}: {s.text}"
        st = s.json()
        status = st.get("status")
        if status in ("completed", "partial", "failed"):
            break
        time.sleep(1)

    assert status in ("completed", "partial"), f"Estado final inesperado: {status}"

    # Obtener resultado final
    res = requests.get(f"{base}/result/{task_id}", timeout=30)
    assert res.status_code == 200, f"/result devolvió {res.status_code}: {res.text}"
    payload = res.json()

    # El resultado puede estar en processing_data o en la raíz
    proc = payload.get("processing_data") or payload
    ss = proc.get("screenshot")
    if isinstance(ss, dict) and ss.get("data"):
        out = tmp_path / "scraper_shot.png"
        out.write_bytes(__import__("base64").b64decode(ss["data"]))
        assert out.stat().st_size > 0
