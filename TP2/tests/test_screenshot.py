# tests/test_screenshot.py
import os
import tempfile
from processor.screenshot import generate_screenshot_base64, save_base64_to_file

def test_generate_screenshot_base64_viewport_quick():

    url = "https://es.wikipedia.org/wiki/Wikipedia"
    res = generate_screenshot_base64(
        url,
        timeout_ms=120_000,
        full_page=False,
        viewport=(1280, 900),
        headless=True,
    )
    assert isinstance(res, dict), "La respuesta debe ser un dict"
    assert "data" in res, f"No se obtuvo 'data' en la respuesta: {res}"
    # Guardar temporalmente y comprobar tamaño
    tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    try:
        save_base64_to_file(res["data"], tmp.name)
        tmp.flush()
        assert os.path.getsize(tmp.name) > 0, "El archivo PNG guardado está vacío"
    finally:
        tmp.close()
        try:
            os.unlink(tmp.name)
        except Exception:
            pass
