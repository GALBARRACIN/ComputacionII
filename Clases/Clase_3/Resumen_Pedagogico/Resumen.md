# 🧠 Ejercicios sobre Procesos en Sistemas Operativos

Este proyecto contiene una serie de ejercicios prácticos implementados en Python para reforzar el estudio del concepto de **procesos** en Sistemas Operativos. Cada ejercicio aborda un aspecto puntual del comportamiento de los procesos, su creación, gestión y particularidades como zombis o huérfanos.

---

## 🎯 Objetivo Pedagógico

El propósito de este proyecto es consolidar la comprensión de cómo funcionan los procesos a nivel del sistema operativo, utilizando Python como herramienta para observar y experimentar los siguientes conceptos:

- Creación y jerarquía de procesos (padres e hijos)
- Bifurcación múltiple y paralelismo
- Sustitución del espacio de ejecución con `exec`
- Estados especiales: procesos zombis y huérfanos
- Sincronización con `wait`
- Análisis del sistema de archivos `/proc` para detección de procesos
- Riesgos de seguridad relacionados a la ejecución de comandos por procesos no controlados

---

## 🧩 Estructura del Proyecto

proyecto_procesos/ 
│ ├── main.py # Menú principal interactivo 
└── ejercicios/ 
├── init.py # Archivo necesario para tratar la carpeta como paquete 
├── ejercicio_01_padre_hijo.py 
├── ejercicio_02_doble_bifurcacion.py 
├── ejercicio_03_exec.py 
├── ejercicio_04_secuencia_controlada.py 
├── ejercicio_05_zombi_temporal.py 
├── ejercicio_06_huerfano_init.py 
├── ejercicio_07_multiproceso_paralelo.py 
├── ejercicio_08_servidor_multiproceso.py 
├── ejercicio_09_detectar_zombis.py 
└── ejercicio_10_inyeccion_comandos.py


Cada archivo de ejercicio implementa una función pública `ejecutar()` que es invocada desde el `main.py` al elegir la opción correspondiente del menú.

---

## ⚙️ Requisitos

- Python 3.x
- Sistema operativo compatible con llamadas `os.fork()` y manipulación de `/proc` (por ejemplo, GNU/Linux)

---

## 🚀 Uso

Desde consola, dentro de la carpeta del proyecto:

```bash
python3 main.py
