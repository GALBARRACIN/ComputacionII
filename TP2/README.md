# README - TP2 - Sistema de Scraping y Análisis Web Distribuido

## Descripción
Este trabajo práctico implementa un flujo distribuido para capturar y procesar páginas web.  
Incluye tres componentes principales:

- **Processor**: servidor TCP que recibe tareas length‑prefixed (4 bytes big‑endian + body JSON) y ejecuta procesamiento en un pool de procesos (captura con Playwright, análisis de performance, generación de thumbnails).  
- **Scraper**: servidor HTTP que encola tareas, hace polling y consulta resultados del processor.  
- **Cliente**: script de ejemplo que captura localmente y/o envía la tarea al processor y guarda los artefactos.

El proyecto fue desarrollado y probado en **Windows** usando PowerShell.

---

## Requisitos y estructura del proyecto
**Requisitos mínimos**

- Python 3.8+ (recomendado 3.10+).  
- Virtual environment (venv).  
- Playwright y navegadores instalados: `python -m playwright install`.  
- Dependencias del proyecto en `requirements.txt`

---

## Preparación del entorno
1. **Crear y activar el entorno virtual** (ejecutar una sola vez):
```
# Crear venv
python -m venv .venv
```

# Activar venv en PowerShell
```
.\.venv\Scripts\Activate.ps1
```

# Actualizar pip e instalar dependencias si existe requirements
```
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

2. **Instalar Playwright y navegadores** (obligatorio para capturas):
```
# Dentro del venv activado ( activa el venv en cada terminal antes de ejecutar comandos Python. )
python -m pip install playwright
python -m playwright install
```

## Puesta en marcha y comandos
Abre tres terminales (A, B, C). En cada terminal activa el venv con:
```
.\.venv\Scripts\Activate.ps1
```

# Terminal A ( Processor )

## Terminal A: arrancar el servidor de procesamiento TCP
```
python server_processing.py -i 127.0.0.1 -p 9001 -n 1 -t 300
```

1. Explicación

- -i IP a escuchar.

- -p puerto.

- -n número de procesos en el pool.

- -t timeout en segundos para cada tarea del pool.

# Terminal B ( Scraper)

## Terminal B: arrancar el servidor HTTP de scraping
```
python server_scraping.py -i 127.0.0.1 -p 8000 --processor-host 127.0.0.1 --processor-port 9001
```

1. Explicación

- --processor-host y --processor-port indican dónde está el processor.

# Terminal C ( Cliente )

## Terminal C: ejecutar el cliente que captura y envía la tarea al processor
```
python capture_wikipedia.py --url "https://es.wikipedia.org/wiki/Wikipedia" --send-to-processor --processor-host 127.0.0.1 --processor-port 9001 --sock-timeout 600 --output wikipedia_shot_from_processor.png
```

1. Explicación

- --send-to-processor envía la tarea al processor.

- --sock-timeout timeout del socket en segundos.

- --output archivo donde se guarda la imagen recibida del processor.


# Tests y verificación
Comando para ejecutar todos los tests
```
# Activar venv primero
.\.venv\Scripts\Activate.ps1
```

## Ejecutar pytest para toda la suite
```
pytest -q -s
```

1. Explicación
- -q salida concisa.

- -s muestra stdout/stderr en tiempo real (útil para ver logs de servidores arrancados por fixtures).


## Ejecutar tests individuales
```
pytest tests/test_processor.py::test_processor_tcp -q -s
pytest tests/test_scraper.py::test_scraper_end_to_end -q -s
pytest tests/test_screenshot.py::test_generate_screenshot_base64_viewport_quick -q -s
```

# Resumen 
```
# .\.venv\Scripts\Activate.ps1
# pip install -r requirements.txt
# python -m playwright install
# python server_processing.py -i 127.0.0.1 -p 9001
# python server_scraping.py -i 127.0.0.1 -p 8000 --processor-host 127.0.0.1 --processor-port 9001

# Windows Comprobar
# ii wikipedia_shot.png
# i wikipedia_shot_from_processor.png
```