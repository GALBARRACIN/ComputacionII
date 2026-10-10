# Sistema C2 Táctico - Enjambre FPV

Este repositorio contiene el proyecto final integrador para las materias **Computación II** y **Diseño de Bases de Datos II**. Consiste en un radar visual de Comando y Control (C2) que rastrea coordenadas GIS de un enjambre de drones simulado en tiempo real.

## Arquitectura del Sistema
*   **Computación II:** Servidor TCP concurrente usando multiplexación I/O (`select`), comunicación inter-procesos (Pipes) para alertas críticas, y delegación de tareas asíncronas con Celery + Redis.
*   **Diseño de BD II:** Motor MongoDB denormalizado, índices geoespaciales (`2dsphere`), agregaciones complejas (Aggregation Framework) para renderizado eficiente, medición de rendimiento (`explain`), y políticas de resguardo lógicas automatizadas.
*   **Frontend:** Interfaz web interactiva construida con Streamlit y mapas de OpenStreetMap (vía Folium).

---

## Guía de Ejecución (Simulación del Sistema)

Para levantar el sistema completo y simular el enjambre, es necesario contar con la infraestructura de Docker encendida (`docker compose up -d`) y abrir múltiples terminales. 

**⚠️ Importante:** En *todas* las terminales es obligatorio estar posicionado en la raíz del proyecto y activar el entorno virtual antes de ejecutar cualquier comando:

```bash
cd ~/ComputacionII/TRABAJO_FINAL
source venv/bin/activate
```

### Paso 1: Levantar el Worker (Cola de Tareas)

Esta terminal procesa los mensajes en segundo plano y los guarda en MongoDB sin bloquear el servidor.

```bash
celery -A src.tasks.worker worker --loglevel=info
```

### Paso 2: Levantar el Servidor C2 Táctico

Este es el núcleo de red. Escucha múltiples conexiones TCP de manera concurrente.

```bash
python src/server/c2_server.py
```

### Paso 3: Levantar el Radar Visual (Frontend)

Inicia la interfaz gráfica. Se abrirá automáticamente una pestaña en el navegador web.

```bash
streamlit run src/ui/dashboard.py
```

### Paso 4: Desplegar el Enjambre (Drones)

Para simular concurrencia real, abrí nuevas terminales (recordá activar el venv en cada una) y copiá y pegá estos comandos para ir sumando drones al mapa. Podés abrir tantas como quieras:

## Dron 1 (D-Alpha):

```bash
cd ~/ComputacionII/TRABAJO_FINAL
source venv/bin/activate
python src/client/drone_node.py --id D-Alpha
```

## Dron 2 (D-Bravo):

```bash
cd ~/ComputacionII/TRABAJO_FINAL
source venv/bin/activate
python src/client/drone_node.py --id D-Bravo
```

## Dron 3 (D-Charlie):

```bash
cd ~/ComputacionII/TRABAJO_FINAL
source venv/bin/activate
python src/client/drone_node.py --id D-Charlie
```

## Dron 4 (D-Delta):

```bash
cd ~/ComputacionII/TRABAJO_FINAL
source venv/bin/activate
python src/client/drone_node.py --id D-Delta
```
(Una vez encendidos los drones, presioná el botón "Actualizar Radar" en la web para verlos moverse en el mapa y observar cómo cambian a estado de alerta cuando su batería baja).

# Políticas de Resguardo (Backups)
Para cumplir con las normativas de integridad de datos, el sistema cuenta con un script de Bash que ejecuta un respaldo lógico (mongodump) aislado dentro del contenedor de la base de datos y lo comprime.

Para ejecutar un backup manual, abrí una terminal y ejecutá:

Bash
# Le damos permisos de ejecución (solo la primera vez)
chmod +x src/db/backup.sh

# Ejecutamos el resguardo

```bash
./src/db/backup.sh
```
Los archivos comprimidos se guardarán automáticamente en la carpeta ./backups/ con un timestamp único (ej. backup_2026-10-07_09-57-16.gz).

# Automatización (Crontab):
Para programar este script de forma automática todos los días a las 3:00 AM, se debe registrar en el demonio Cron del sistema Linux (crontab -e) con la siguiente regla:

```bash
0 3 * * * /ruta/absoluta/al/proyecto/src/db/backup.sh
```