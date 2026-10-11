# 🔄 Arquitectura y Modelo de Datos Integral (Computación II y Diseño de BD II)

Este documento especifica el diseño estructural de los datos a lo largo de todo su ciclo de vida dentro del **Sistema C2 Táctico**: desde su generación y transporte concurrente en red (**Datos en Tránsito y Memoria — Computación II**) hasta su transformación, indexación espacial y persistencia (**Datos en Reposo — Diseño de Bases de Datos II**).

---

## 1. Flujo y Transformación del Dato (Pipeline End-to-End)

El dato atraviesa cinco estados arquitectónicos desde que nace en el nodo simulado hasta que se renderiza en el radar táctico:

```text
[1. Nodo Dron] ──(Trama JSON plana vía Socket TCP)──> [2. Servidor C2 (select)]
                                                            │
                    ┌──(Si batería < 20%: Flujo de bytes)───┴───(Delegación Asíncrona)──┐
                    ▼                                                                   ▼
         [3A. Canal IPC (os.pipe)]                                         [3B. Broker Redis + Celery]
        (Alerta crítica en Kernel)                                        (Transformación a GeoJSON)
                                                                                        │
                                                                                        ▼
[5. Radar UI (Streamlit/Folium)] <──(4B. Aggregation Pipeline)── [4A. MongoDB (Colección 'telemetria')]
  (Cálculo Haversine en RAM)                                       (Persistencia BSON + Índice 2dsphere)
```

---

## 2. Datos en Tránsito, IPC y Colas en Memoria (Computación II)

### 2.1. Trama de Red sobre Sockets TCP (`drone_node.py` ➔ `c2_server.py`)
Para minimizar el *overhead* de red y facilitar la lectura no bloqueante mediante multiplexación I/O (`select.select`), los clientes emiten un paquete ligero serializado en texto plano **JSON (codificación UTF-8)** de menos de 1024 bytes por ráfaga:

```json
{
  "drone_id": "D-Alpha",
  "lat": -32.890812,
  "lon": -68.827245,
  "battery": 84.0
}
```
* **Justificación de diseño:** En la capa de transporte TCP, el nodo envía una estructura plana (`lat` y `lon` separados) para reducir el tamaño del *payload* y delegar el costo de armado de estructuras complejas al backend asíncrono.

### 2.2. Estructura de Mensajes IPC mediante Tuberías (`os.pipe()`)
Cuando el servidor TCP detecta en memoria un paquete cuyo campo `battery` es inferior al umbral crítico (`< 20%`), dispara un mecanismo de **Comunicación Inter-Procesos (IPC)** nativo de Linux utilizando descriptores de archivo en memoria del kernel (`r_fd`, `w_fd`):

```text
b"ALERTA CRITICA: Dron D-Alpha con bateria al 19.0%"
```
* **Formato:** Flujo crudo de bytes (`bytes` en UTF-8) escrito mediante `os.write(w_fd, ...)` y consumido de forma inmediata mediante `os.read(r_fd, 1024)`, aislando el canal de emergencias del flujo normal de base de datos.

### 2.3. Encolado en Message Broker (Redis + Celery)
Para evitar que la escritura en disco bloquee el bucle de eventos `select` del servidor TCP, el diccionario de telemetría se inyecta en **Redis** (almacenamiento clave-valor en memoria RAM) a través del método `.delay()` de Celery.
* **Estructura en Redis:** Celery envuelve el JSON del dron en un sobre de tarea (*Task Message*) con un `task_id` único (UUID) y lo apila en una lista en memoria (`LPUSH`/`BRPOP`), garantizando velocidad de respuesta de orden sub-milisegundo hacia el socket.

---

## 3. Modelo de Datos en Reposo y Geoespacial (Diseño de Bases de Datos II)

### 3.1. Justificación del Motor Documental (MongoDB)
Para una carga de trabajo de telemetría IoT (*Write-Heavy*), se descartó el modelo relacional (SQL) en favor de **MongoDB** por tres motivos:
1. **Ingesta Masiva sin Bloqueos:** Los *workers* de Celery ejecutan operaciones `insert_one()` concurrentes sin sufrir bloqueos de tablas ni validaciones de claves foráneas.
2. **Denormalización:** Cada lectura contiene la totalidad del estado de la unidad, eliminando la necesidad de costosos `JOIN` al refrescar el radar cada 2 segundos.
3. **Soporte Geoespacial Nativo:** Cálculos sobre geometría esférica integrados en el motor en C++.

### 3.2. Transformación y Esquema BSON (Colección `telemetria`)
El *worker* de Celery (`src/tasks/worker.py`) recibe el diccionario plano desde Redis, le inyecta la marca temporal del servidor, evalúa el estado operativo y **transforma las coordenadas al estándar internacional RFC 7946 (GeoJSON)** antes de persistirlo en la base de datos `c2_tactico_db`:

```json
{
  "_id": ObjectId("6708f9b2e4b0a1c2d3e4f5a6"),
  "drone_id": "D-Alpha",
  "timestamp": "2026-10-11T12:00:05.123456",
  "battery_pct": 84.0,
  "status": "active",
  "location": {
    "type": "Point",
    "coordinates": [
      -68.827245,
      -32.890812
    ]
  }
}
```

#### Diccionario de Campos Persistidos
| Campo | Tipo BSON | Origen / Transformación | Descripción Técnica |
| :--- | :--- | :--- | :--- |
| `_id` | `ObjectId` | Generado por MongoDB | Clave primaria de 12 bytes (incluye timestamp de creación y contador único). |
| `drone_id` | `String` | Trama TCP | Identificador único del nodo emisor (`D-Alpha`, `D-Bravo`, etc.). |
| `timestamp` | `String` | Generado en Worker | Fecha y hora exacta de procesamiento en formato estándar `ISO-8601`. |
| `battery_pct` | `Double` | Trama TCP (`battery`) | Porcentaje de carga energética (`0.0` a `100.0`). |
| `status` | `String` | Calculado en Worker | `"active"` si `battery_pct >= 20`, o `"low_battery"` si es menor. |
| `location` | `Object` | Transformado en Worker | Objeto **GeoJSON** obligatorio para indexación espacial. |
| `location.type` | `String` | Constante `"Point"` | Define la primitiva geométrica espacial. |
| `location.coordinates` | `Array<Double>` | `[lon, lat]` | **Regla estricta GeoJSON:** El índice `0` es la **Longitud** (X) y el índice `1` es la **Latitud** (Y). |

---

## 4. Estrategia de Indexación (`2dsphere`) y Auditoría (`explain`)

Para resolver consultas de proximidad (ej. detectar qué drones vuelan dentro del radio de cobertura de 1000 metros del C2) sin recorrer secuencialmente toda la colección histórica, se definió un índice geoespacial esférico sobre el subdocumento `location`:

```python
coleccion.create_index([("location", GEOSPHERE)])
```

* **Validación de Rendimiento (`src/db/queries.py`):** Al auditar consultas `$nearSphere` mediante `.explain("executionStats")`, el optimizador de MongoDB descarta el escaneo completo (`COLLSCAN`, complejidad `O(N)`) y selecciona la etapa **`IXSCAN`** (*Index Scan*, complejidad `O(log N)`), leyendo únicamente las celdas geográficas (Geohashes) cercanas al centro de Mendoza.

---

## 5. Modelo de Extracción y Vista en Memoria (Aggregation + Frontend)

### 5.1. Reducción de Datos en el Motor (Aggregation Framework)
Dado que la colección `telemetria` funciona como una bitácora histórica inmutable (caja negra), el Frontend no ejecuta un `find()` convencional. En su lugar, envía un **Pipeline de Agregación** que filtra y transforma los documentos dentro del servidor de base de datos:

```python
pipeline = [
    {"$sort": {"timestamp": -1}},
    {"$group": {
        "_id": "$drone_id",
        "lat": {"$first": {"$arrayElemAt": ["$location.coordinates", 1]}},
        "lon": {"$first": {"$arrayElemAt": ["$location.coordinates", 0]}},
        "bateria": {"$first": "$battery_pct"},
        "estado": {"$first": "$status"}
    }}
]
```
* **Eficiencia de Red y RAM:** Aunque existan 50.000 registros históricos en disco, este pipeline colapsa la colección mediante `$sort` y `$group` (`$first`), transfiriendo por red hacia Streamlit únicamente **1 documento liviano por cada dron activo**.

### 5.2. Enriquecimiento en Memoria (Capa UI - Haversine)
Al recibir el cursor agregado, el Dashboard (`src/ui/dashboard.py`) mantiene el último estado conocido de todos los drones y calcula en memoria la distancia ortodrómica a la base mediante la **Fórmula de Haversine**, clasificando cada unidad en dos estados visuales sin perder su rastro en el mapa:
* **Distancia `<= 1000 m`:** Unidad `🟢 EN RANGO` (Marcador triangular verde/rojo opaco).
* **Distancia `> 1000 m`:** Unidad `⚪ SEÑAL PERDIDA` (Marcador triangular gris traslúcido en su última coordenada registrada).

---

## 6. Estructura de Resguardo Lógico (Backups)

La política de contingencia (`src/db/backup.sh`) extrae los datos en caliente desde el contenedor Docker mediante `mongodump`:
* **Formato de Salida:** Flujo binario empaquetado (`--archive`) y comprimido en tiempo real con algoritmo Lempel-Ziv (`--gzip`).
* **Artefacto Generado:** `./backups/backup_YYYY-MM-DD_HH-MM-SS.gz` (preserva tanto los documentos BSON de la colección `telemetria` como la definición estructural del índice `2dsphere` para restauraciones inmediatas con `mongorestore`).