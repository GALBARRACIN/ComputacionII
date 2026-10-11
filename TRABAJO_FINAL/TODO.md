#  Registro de Evolución (Changelog) y Hoja de Ruta (To-Do)

Este documento registra el historial cronológico de implementación del **Sistema C2 Táctico** a través de sus *commits* (tareas completadas) y define las proyecciones de escalabilidad futura.

---

## ✅ Tareas Completadas (Historial de Commits)

### 11 de Octubre, 2026 — Precisión Geoespacial y Correcciones UI
- [x] **`fix(ui): corregir referencia de variable en tabla de telemetría y añadir cálculo Haversine`**
  * **Modificación:** Se corrigió un `NameError` en el bucle de renderizado de la tabla de estado en `src/ui/dashboard.py`.
  * **Agregado:** Se implementó la fórmula trigonométrica de Haversine (`math`) para calcular en tiempo real la distancia en metros desde cada dron hasta la base en Mendoza, diferenciando visualmente las unidades **En Rango** ($\le 1000\text{ m}$, verde/rojo) de aquellas con **Señal Perdida** ($> 1000\text{ m}$, gris traslúcido).

###  10 de Octubre, 2026 — Documentación Técnica y Operativa
- [x] **`docs: agregar guías de instalación (install.md) y proyecciones futuras (todo.md)`**
  * **Agregado:** Se crearon los archivos `install.md` (requisitos de entorno virtual `venv`, dependencias y levantado de contenedores con Docker Compose) y la primera versión de `todo.md`.
- [x] **`docs: crear README.md con arquitectura, instrucciones de ejecución y políticas de resguardo`**
  * **Agregado:** Se redactó el manual principal del repositorio detallando la integración entre Computación II y Diseño de Bases de Datos II, el paso a paso multi-terminal para simular el enjambre y el uso de `crontab` para backups.

###  9 de Octubre, 2026 — Tiempo Real (Polling) y Rediseño Táctico
- [x] **`feat(ui): implementar Polling para auto-rastreo en tiempo real del enjambre`**
  * **Agregado:** Se incorporó un control interactivo (`st.checkbox`) junto con `time.sleep(2)` y `st.rerun()` para actualizar automáticamente la posición de los drones cada 2 segundos sin intervención manual.
- [x] **`style(ui): centrar elementos visuales, regresar a OpenStreetMap y agregar botón para limpiar base de datos`**
  * **Modificación:** Se maquetó la interfaz usando columnas de Streamlit e inyección HTML para centrar títulos, mapa y tablas, restableciendo las capas de `OpenStreetMap`.
  * **Agregado:** Se programó la función `limpiar_base_datos()` (`delete_many({})`) vinculada a un botón en la UI para purgar registros residuales antes de una demostración en vivo.
- [x] **`feat(ui): rediseñar radar con estilo táctico (marcadores triangulares y mapa dark_matter custom)`**
  * **Modificación:** Se reemplazaron los marcadores clásicos por polígonos vectoriales triangulares (`RegularPolygonMarker` de 3 lados rotados a 30°) estilo radar UAV, y se añadió el círculo de cobertura operativa de 1 km (`folium.Circle`).

###  7 de Octubre, 2026 — Frontend GIS y Políticas de Resguardo (Backups)
- [x] **`fix(ui): migrar proveedor de mapas a OpenStreetMap para resolver bloqueo por API Key`**
  * **Modificación:** Se reemplazó el proveedor base de mapas `CartoDB` por `OpenStreetMap` en `dashboard.py` para solucionar el bloqueo de renderizado por exigencia de API Key paga.
- [x] **`feat(ui): implementar dashboard GIS con Streamlit y Folium (con documentación técnica)`**
  * **Agregado:** Creación del módulo visual `src/ui/dashboard.py` conectado a MongoDB para graficar las coordenadas de la flota y su estado de batería en una tabla interactiva.
- [x] **`feat(db): implementar script de backup automatizable con mongodump y compresión gzip`**
  * **Agregado:** Creación del script en Bash `src/db/backup.sh` que ejecuta `mongodump` dentro del contenedor Docker, empaquetando y comprimiendo (`--gzip --archive`) la base de datos con marca de tiempo en `./backups/`.

###  5 de Octubre, 2026 — Consultas Geoespaciales y Rendimiento NoSQL
- [x] **`docs(db): restaurar comentarios exhaustivos de queries.py para la defensa oral`**
  * **Modificación:** Se documentó línea por línea el archivo `src/db/queries.py` detallando el funcionamiento interno de los operadores de agregación y los índices espaciales.
- [x] **`feat(db): implementar Aggregation Framework y script de performance geoespacial con explain`**
  * **Agregado:** Se programaron los pipelines de agregación (`$sort` y `$group` con `$first`) para obtener la última posición por dron, junto con consultas `$nearSphere` auditadas mediante `.explain("executionStats")` para comprobar el uso del índice `2dsphere` (`IXSCAN` vs `COLLSCAN`).

###  3 de Octubre, 2026 — Núcleo Concurrente, Colas Asíncronas e Infraestructura Base
- [x] **`fix(server): resolver ModuleNotFoundError e integrar Celery/Pipes manteniendo comentarios`**
  * **Modificación:** Se inyectó la ruta raíz en `sys.path` (`PYTHONPATH`) para corregir las importaciones entre paquetes y se conectó el servidor TCP con el worker de Celery y un Pipe del sistema operativo (`os.pipe()`) para alertas IPC de batería crítica.
- [x] **`feat(tasks): implementar worker de Celery y Redis para inserción asíncrona en MongoDB`**
  * **Agregado:** Se desarrolló `src/tasks/worker.py` utilizando Redis como *Message Broker* para desacoplar la recepción de red de la escritura en disco (MongoDB), transformando las coordenadas al estándar `GeoJSON`.
- [x] **`feat(network): implementar cliente TCP para simular telemetría GIS de drones en formato JSON`**
  * **Agregado:** Se creó `src/client/drone_node.py` con soporte de argumentos CLI (`argparse`) para simular el movimiento aleatorio de múltiples drones, descarga gradual de batería y envío de tramas JSON por sockets.
- [x] **`feat(network): implementar servidor TCP concurrente no bloqueante con select y argparse`**
  * **Agregado:** Se implementó `src/server/c2_server.py` aplicando multiplexación de Entrada/Salida (`select.select`) en un único hilo para atender múltiples conexiones simultáneas de drones sin bloquear el proceso.
- [x] **`build(deps): definir librerias para concurrencia, base de datos y UI en requirements.txt`**
  * **Agregado:** Definición de dependencias del proyecto (`pymongo`, `celery`, `redis`, `streamlit`, `folium`, `streamlit-folium`) y configuración de contenedores en `docker-compose.yml`.
- [x] **`build(core): creacion dede estructura de directorios y archivos base para Sistema C2`**
  * **Agregado:** Inicialización del repositorio y armado de la arquitectura modular de paquetes (`src/server`, `src/client`, `src/tasks`, `src/db`, `src/ui`, `backups`).

---

##  Tareas Pendientes (Roadmap y Mejoras Futuras)

- [ ] **WebSockets en Frontend:** Reemplazar el mecanismo de *Polling* en Streamlit por WebSockets bidireccionales para actualizaciones orientadas a eventos (*Event-Driven*).
- [ ] **Suite de Tests Automatizados:** Añadir pruebas unitarias y de integración con `pytest` para validar el parseo de paquetes TCP y la estructura GeoJSON.
- [ ] **Autenticación de Operadores:** Integrar un módulo de login con tokens JWT para restringir el acceso al panel de Comando y Control.
- [ ] **Trazado de Trayectorias Históricas:** Añadir una vista en el mapa con `folium.PolyLine` que dibuje el recorrido completo de un dron seleccionado.