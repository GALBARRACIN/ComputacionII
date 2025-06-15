# 🧬 Sistema Concurrente de Análisis Biométrico con Cadena de Bloques

> Trabajo práctico para la materia de Computación II – Simulación y persistencia de señales biomédicas en sistema concurrente con blockchain local.

---

## 📌 Objetivo

Simular en tiempo real un sistema distribuido que:

- Genera datos biométricos simulados de una prueba de esfuerzo (frecuencia, presión, oxígeno).
- Los procesa concurrentemente en tres procesos distintos, uno por señal.
- Valida y almacena los resultados en una cadena de bloques local (`blockchain.json`), asegurando integridad mediante hash SHA‑256.

---

## 🧱 Arquitectura General



Generador
   │
   ├─▶ Analizador de Frecuencia ─┐
   ├─▶ Analizador de Presión ───▶│
   └─▶ Analizador de Oxígeno ───▶│
                                 ▼
                          Proceso Verificador
                                 ▼
                          Cadena de Bloques



---

## ⚙️ Tecnologías y Requisitos

- Python 3.9 o superior
- Librerías estándar: `multiprocessing`, `queue`, `datetime`, `json`, `hashlib`, `random`, `os`
- Librería externa: `numpy`
- No se usa red ni librerías de aprendizaje automático

---

## 📁 Estructura del Proyecto

```
sistema_biometrico/
├── main.py
├── procesos/
│   ├── generador.py
│   ├── analizador_frecuencia.py
│   ├── analizador_presion.py
│   ├── analizador_oxigeno.py
│   └── verificador.py
├── blockchain/
│   ├── bloque.py
│   ├── cadena.py
│   └── blockchain.json
├── verificacion/
│   ├── verificar_cadena.py
│   └── reporte.txt
├── utils/
│   ├── ipc.py               # (reservado para futuras mejoras)
│   └── helpers.py           # (no utilizado en esta versión)
└── README.md
```

## 🚀 Ejecución

1. **Clonar el repositorio (si aplica)**:

   ```bash
   git clone https://github.com/tu-usuario/sistema_biometrico.git
   cd sistema_biometrico
   ```

2. **Crear un entorno virtual (recomendado)**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instalar dependencias**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar el sistema principal (Tarea 1 + Tarea 2)**:

   ```bash
   python3 main.py
   ```

   Verás que se van imprimiendo bloques uno por uno a medida que se construyen. Ejemplo:

   ```
   🧱 Bloque #1 - Hash: 22fa4d648555
   🧱 Bloque #2 - Hash: 93fbf0b6a74a ⚠️ ALERTA
   ```

5. **Verificar integridad de la cadena (Tarea 3)**:

   ```bash
   python3 verificacion/verificar_cadena.py
   ```

6. **Consultar el reporte generado**:

   ```bash
   cat verificacion/reporte.txt
   ```

   Deberías ver algo como:

   ```
   Total de bloques: 60
   Bloques con alerta: 3
   Bloques corruptos: 0
   Promedio frecuencia: 122.4
   ...
   ```

> Si querés resetear y volver a correr el sistema desde cero, podés borrar `blockchain/blockchain.json` y `verificacion/reporte.txt` antes de reiniciar `main.py`.

## 📊 ¿Qué hace cada módulo?

| Módulo                           | Descripción                                                                 |
|----------------------------------|-----------------------------------------------------------------------------|
| `main.py`                        | Orquesta toda la ejecución del sistema. Lanza los procesos del generador, analizadores y verificador. |
| `generador.py`                   | Simula 60 muestras biométricas por segundo (frecuencia, presión, oxígeno) y las distribuye a los analizadores. |
| `analizador_frecuencia.py`       | Calcula media y desviación de la frecuencia cardíaca sobre una ventana móvil de 30 elementos. |
| `analizador_presion.py`          | Extrae la presión sistólica y analiza sus estadísticas móviles.             |
| `analizador_oxigeno.py`          | Analiza el nivel de oxígeno en sangre y calcula estadísticas en tiempo real. |
| `verificador.py`                 | Agrupa las estadísticas por timestamp, detecta alertas, genera bloques con hash y los enlaza en cadena. |
| `bloque.py`                      | Define la clase `Bloque`, con lógica de hashing SHA‑256 y estructura serializable. |
| `cadena.py`                      | Administra la lista enlazada de bloques y su persistencia en `blockchain.json`. |
| `verificar_cadena.py`            | Revisa la integridad de la blockchain comparando hashes y `prev_hash`, y genera el reporte final. |
| `reporte.txt`                    | Archivo de salida con métricas clave: cantidad de bloques, alertas y promedios. |
| `ipc.py`                         | (Actualmente sin uso) Espacio reservado para encapsular lógica de comunicación entre procesos. |
| `helpers.py`                     | (No implementado) Puede alojar funciones utilitarias como manejo de tiempo o validaciones. |


## 📌 Salida Esperada

Durante la ejecución del sistema, se espera lo siguiente:

1. **En consola**, mientras corre `main.py`, se imprimen los bloques generados:

   ```
   🧱 Bloque #1 - Hash: 22fa4d648555
   🧱 Bloque #2 - Hash: 93fbf0b6a74a ⚠️ ALERTA
   ...
   🧱 Bloque #60 - Hash: aadf15fd3e0a
   ```

   Si un bloque contiene un valor fuera de rango (ej. frecuencia > 200), se marca como `⚠️ ALERTA`.

2. **Archivo `blockchain/blockchain.json`**:

   Guarda los bloques en orden cronológico con esta estructura por bloque:

   ```json
   {
       "timestamp": "2025-06-15T17:35:42.000001",
       "datos": {
           "frecuencia": {"media": 122.3, "desv": 12.1},
           "presion": {"media": 146.7, "desv": 11.5},
           "oxigeno": {"media": 94.2, "desv": 2.3}
       },
       "alerta": false,
       "prev_hash": "000000000000...",
       "hash": "a1b2c3d4e5f6..."
   }
   ```

3. **Archivo `verificacion/reporte.txt`** generado al correr `verificar_cadena.py`:

   ```
   Total de bloques: 60
   Bloques con alerta: 4
   Bloques corruptos: 0
   Promedio frecuencia: 123.45
   Promedio presion: 147.12
   Promedio oxigeno: 94.88
   ```

Esto confirma que el sistema generó datos válidos, los verificó correctamente, y produjo una cadena íntegra de bloques junto con métricas resumidas.


## 💡 Estado del Proyecto

✅ Tarea 1: Generación y análisis concurrente completados  
✅ Tarea 2: Verificador, validación de alertas y cadena de bloques funcional  
✅ Tarea 3: Verificación de integridad y generación de reporte final  
✅ Cumplimiento de restricciones del enunciado (sin redes ni ML)  
☑️ Modularidad: estructura limpia, extensible y lista para mejoras  
☑️ Documentación: `README.md`, reporte y código comentado incluidos  
☑️ Bonus: uso profesional de entorno virtual, `requirements.txt`, e IPC bien organizado
