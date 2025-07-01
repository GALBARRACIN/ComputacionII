# 🧵 Profundizando en la Concurrencia con Python (`threading`)

## 1. Introducción a los Hilos
- **Concurrencia** permite ejecutar múltiples operaciones de forma simultánea para mejorar rendimiento y responsividad.
- **Hilo (thread):** Unidad más pequeña de ejecución dentro de un proceso. Comparte memoria con otros hilos del mismo proceso.
- **Ventajas:**
  - Mejor rendimiento en tareas CPU-bound o I/O-bound.
  - Mayor responsividad en interfaces gráficas.
  - Menor costo que los procesos.
- **Desafíos:**
  - Sincronización compleja.
  - Condiciones de carrera y deadlocks.
  - Difícil depuración y sobrecarga si se usan demasiados hilos.

## 2. Hilos vs Procesos
| Aspecto               | Hilos                            | Procesos                        |
|-----------------------|-----------------------------------|----------------------------------|
| Memoria               | Compartida                        | Aislada                          |
| Comunicación          | Directa (memoria compartida)      | IPC (más costoso)               |
| Creación              | Ligera                            | Costosa                          |
| Paralelismo CPU real  | Limitado por GIL (en CPython)     | Sí, cada proceso tiene su GIL   |
| Aislamiento            | Bajo                              | Alto                             |

## 3. Tipos de Hilos
- **User-level Threads:** Gestionados por bibliotecas del espacio de usuario, eficientes pero limitados (no paralelismo real).
- **Kernel-level Threads:** Gestionados por el SO, permiten paralelismo real. Es lo que usa `threading` en CPython.

## 4. El módulo `threading` en Python
- Clases clave: `Thread`, `Lock`, `RLock`, `Semaphore`, `Event`, `Condition`, `Barrier`.
- Métodos importantes: `start()`, `join()`, `is_alive()`, `setDaemon()`, etc.

### Ejemplos prácticos:
- 🧮 **Ejecución concurrente de funciones.**
- 🔐 **Evitar condiciones de carrera con `Lock`.**
- 🧑‍💼 **Uso de argumentos, hilos daemon.**

## 5. El Global Interpreter Lock (GIL)
- **Qué es:** Lock que impide que múltiples hilos ejecuten bytecode Python simultáneamente.
- **Afecta:** Tareas CPU-bound en multihilo (no hay paralelismo real en CPython).
- **No afecta:** Tareas I/O-bound (el GIL se libera durante esperas).
- **Alternativas para CPU-bound:** `multiprocessing`, extensiones en C que liberan el GIL.

## 6. Comparativa: Hilos, Corutinas y Procesos

| Aspecto              | `threading` (Hilos) | `asyncio` (Corutinas) | `multiprocessing` (Procesos) |
|----------------------|---------------------|------------------------|-------------------------------|
| Gestión              | Kernel              | Usuario                | Kernel                        |
| Concurrencia         | Preventiva          | Cooperativa            | Preventiva                    |
| Cambio de contexto   | Moderado            | Muy barato             | Costoso                       |
| Ideal para           | I/O-bound           | I/O-bound masivo       | CPU-bound                     |
| Afectado por GIL     | Sí                  | No                     | No                            |

## 7. Ejercicios y Proyectos
- **Web Crawler Multihilo:** Crawlea múltiples URLs y guarda resultados usando `threading` y `Lock`.
- **Procesamiento por Lotes:** Simula hilos productores, consumidores y logger con `queue.Queue`.

## 8. Conclusiones
- El multihilo sigue siendo útil para tareas concurrentes simples y compatibles con bibliotecas existentes.
- Nuevas tendencias incluyen `asyncio`, `multiprocessing`, y lenguajes como Go o Rust.
- Python avanza con iniciativas como **PEP 703 (eliminar el GIL)** para mejorar el paralelismo real.
