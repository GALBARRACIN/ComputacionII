# Guía de Instalación y Despliegue

Este documento detalla los pasos para configurar el entorno local y desplegar la infraestructura base del Sistema C2 Táctico.

## Prerrequisitos
Asegúrese de contar con el siguiente software en su sistema Debian/Linux:
* Python 3.10 o superior.
* Docker y Docker Compose.
* Git.

## Paso 1: Clonar el Repositorio

```bash
git clone [https://github.com/GALBARRACIN/ComputacionII.git](https://github.com/GALBARRACIN/ComputacionII.git)
cd ComputacionII/TRABAJO_FINAL
```

## Paso 2: Entorno Virtual (Requisito estricto)
Se exige el uso de entornos virtuales para evitar conflictos de paquetería a nivel de sistema operativo:

```bash
python3 -m venv venv
source venv/bin/activate
```

## Paso 3: Instalación de Dependencias
Con el entorno virtual activado, instale las librerías requeridas para el ecosistema (Worker, Base de Datos, Frontend):

```bash
pip install pymongo celery redis streamlit folium streamlit-folium
```

## Paso 4: Levantar la Infraestructura Dockerizada
El sistema requiere que los contenedores de Redis (Message Broker) y MongoDB (Persistencia) estén activos antes de levantar el servidor TCP.

```bash
docker compose up -d
```

(Para verificar el estado de los servicios, puede ejecutar ```bash docker ps```).

Una vez finalizada la instalación, consulte la sección "Guía de Ejecución" en el README.md principal para encender los módulos del sistema.