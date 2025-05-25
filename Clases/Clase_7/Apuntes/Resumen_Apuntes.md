# **Resumen Teórico sobre Señales en Sistemas Operativos UNIX/POSIX**

## **1. Introducción a las Señales**
Las señales son un mecanismo de comunicación **asíncrono** entre procesos en sistemas operativos UNIX/POSIX. Su propósito es **notificar** a un proceso sobre un evento sin que este deba estar esperando activamente. Se usan para:
- Manejo de excepciones como división por cero (`SIGFPE`).
- Terminación controlada (`SIGTERM`).
- Interrupción por teclado (`SIGINT` con Ctrl+C).
- Comunicación entre procesos (`SIGUSR1`, `SIGUSR2`).

## **2. Funcionamiento Interno**
Cada proceso tiene:
- **Una tabla de señales pendientes** que almacena señales recibidas.
- **Una máscara de señales bloqueadas** que evita interrupciones en secciones críticas.

El flujo de una señal es:
1. Se envía una señal al proceso.
2. El kernel verifica si está bloqueada.
3. Si no está bloqueada, se ejecuta su **manejador** (`signal handler`).
4. Si no hay manejador, se aplica la acción por defecto.

## **3. Tipos de Señales**
| Tipo | Descripción |
|------|------------|
| **Síncronas** | Generadas por el propio proceso (`SIGFPE`, `SIGSEGV`). |
| **Asíncronas** | Enviadas desde otro proceso o el kernel (`SIGUSR1`, `SIGINT`). |
| **Reales (POSIX RT)** | Permiten colas múltiples y envío de datos (`sigqueue`). |

## **4. Envío de Señales**
Las señales pueden enviarse de varias maneras:
```c
kill(pid, SIGUSR1);       // Desde otro proceso
raise(SIGTERM);           // Desde el mismo proceso
pthread_kill(tid, SIGUSR1); // A un hilo específico
sigqueue(pid, SIGUSR1, value); // Con datos adicionales
```

## **5. Manejo de Señales**
Los procesos pueden capturar señales con un manejador:
```c
#include <signal.h>

void handler(int sig) {
    write(1, "Señal capturada\n", 17);
}

int main() {
    struct sigaction sa = {0};
    sa.sa_handler = handler;
    sigaction(SIGUSR1, &sa, NULL);

    while (1) pause(); // Espera señales
}
```
El uso de **`sigaction()`** es preferible sobre `signal()` debido a su mayor control sobre las señales.

## **6. Bloqueo y Máscaras de Señales**
Se puede evitar que un proceso reciba señales en momentos críticos:
```c
sigset_t mask;
sigemptyset(&mask);
sigaddset(&mask, SIGINT);
pthread_sigmask(SIG_BLOCK, &mask, NULL);
```
Esto es útil para proteger **secciones críticas**.

## **7. Señales en Programas Multihilo**
Las señales en procesos con múltiples hilos requieren cuidados especiales:
- Las señales dirigidas a un **proceso** pueden ser captadas por cualquier hilo.
- Se recomienda que **un único hilo** gestione las señales:
```c
sigwait(&mask, &sig);
```

## **8. Señales Reales (POSIX RT)**
POSIX introduce señales **con información adjunta** (`sigqueue`):
```c
sigqueue(pid, SIGRTMIN, (union sigval){.sival_int = 42});
```
Esto permite enviar datos junto con la señal.

## **9. Comparación de IPC (Comunicación entre Procesos)**
Las señales son **rápidas** y útiles, pero tienen limitaciones en el transporte de datos.

| Mecanismo   | Asíncrono | Bidireccional | Capacidad de Datos | Hilos Seguros |
|------------|-----------|--------------|------------------|--------------|
| **Señales** | ✅ | ❌ | Limitada | Parcial |
| **Pipes** | ❌ | ✅ | Ilimitada | ✅ |
| **Sockets** | ❌ | ✅ | Ilimitada | ✅ |
| **Shared Memory** | ❌ | ✅ | Ilimitada | ✅ (con locks) |

## **10. Ejemplo de Sincronización con Señales**
```python
import os, signal, time

def handler(signum, frame):
    print("[PADRE] Señal recibida, procediendo...")

signal.signal(signal.SIGUSR1, handler)

pid = os.fork()
if pid == 0:
    time.sleep(2)
    os.kill(os.getppid(), signal.SIGUSR1)
    sys.exit(0)
else:
    print("[PADRE] Esperando señal...")
    while True:
        time.sleep(1)
```

## **11. Consideraciones Finales**
- **Evitar `SIGKILL` (`kill -9`)**, ya que impide la liberación de recursos.
- Usar **`sigaction()`** en lugar de `signal()` por mejor control.
- En programas multihilo, **centralizar el manejo de señales** en un solo hilo.

# **Resumen Completo: Señales en Sistemas Operativos y Ejercicios en Python**

## **1. Conceptos Fundamentales sobre Señales en Sistemas Operativos**
Las **señales** son un mecanismo asíncrono en sistemas UNIX/POSIX para la comunicación entre procesos. Permiten notificar eventos sin que un proceso deba estar esperando activamente.

### **Características Principales**
- Son interrupciones software enviadas a procesos.
- Pueden generarse por eventos internos o externos.
- Su manejo debe ser **async-signal-safe** para evitar errores en entornos concurrentes.

### **Tipos de Señales**
- **Síncronas**: Generadas por el propio proceso (ej. `SIGSEGV`, `SIGFPE`).
- **Asíncronas**: Enviadas por el kernel o otro proceso (`SIGUSR1`, `SIGINT`).
- **POSIX Real-Time**: Pueden transportar datos (`sigqueue`).

### **Envío y Manejo de Señales**
Las señales pueden enviarse y manejarse con:
```c
kill(pid, SIGUSR1);     // Desde otro proceso
raise(SIGTERM);         // Desde sí mismo
sigaction(SIGINT, ...); // Instalación de un manejador
```

En Python:
```python
import signal

def handler(signum, frame):
    print(f"Señal recibida: {signum}")

signal.signal(signal.SIGUSR1, handler)
```

## **2. Uso del Comando `kill`**
El comando `kill` permite enviar señales a procesos, no solo para terminarlos, sino también para detenerlos, reiniciarlos o notificarlos.

### **Ejemplos de uso**
```bash
kill -TERM <pid>  # Terminación ordenada
kill -STOP <pid>  # Pausar un proceso
kill -CONT <pid>  # Reanudar un proceso
kill -USR1 <pid>  # Señal personalizada
```
También existen herramientas como `pkill` para matar procesos por nombre.

---

## **3. Ejercicios en Python sobre Señales**
Estos ejercicios han permitido comprender y aplicar el uso de señales en programación con Python.

### **Ejercicio 1: Manejo básico con `SIGTERM`**
- El proceso espera la señal `SIGTERM`.
- Al recibirla, limpia recursos con `atexit` y finaliza.
- Se prueba enviando `kill -TERM <pid>`.

**Código esencial:**
```python
import signal, sys

def handle_sigterm(signum, frame):
    print("SIGTERM recibido, finalizando...")
    sys.exit(0)

signal.signal(signal.SIGTERM, handle_sigterm)
while True:
    pass
```

---

### **Ejercicio 2: Diferenciar señales según su origen**
- Se crean tres procesos hijos.
- Cada hijo envía `SIGUSR1`, `SIGUSR2` o `SIGTERM` al padre.
- El padre identifica quién envió qué señal.

**Código esencial:**
```python
import os, signal

def handler(signum, frame):
    print(f"Señal {signum} recibida de proceso {os.getpid()}")

signal.signal(signal.SIGUSR1, handler)
signal.signal(signal.SIGUSR2, handler)
signal.signal(signal.SIGTERM, handler)
```

---

### **Ejercicio 3: Ignorar señales temporalmente**
- `SIGINT` (Ctrl+C) es ignorado por 5 segundos.
- Luego, el comportamiento se restaura.
- Se prueba ejecutando y presionando Ctrl+C.

**Código esencial:**
```python
import signal, time

def ignore_sigint(signum, frame):
    print("SIGINT ignorado temporalmente.")

signal.signal(signal.SIGINT, ignore_sigint)
time.sleep(5)
signal.signal(signal.SIGINT, signal.default_int_handler)
```

---

### **Ejercicio 4: Control multihilo con señales externas**
- Un hilo cuenta regresivamente desde 30.
- `SIGUSR1` pausa la cuenta, `SIGUSR2` la reanuda.
- Se protege la variable compartida con `threading.Lock()`.

**Código esencial:**
```python
import signal, threading

def pause(signum, frame):
    global contador_activo
    contador_activo = False

signal.signal(signal.SIGUSR1, pause)
```

---

### **Ejercicio 5: Simulación de cola de trabajos**
- Un **productor** genera tareas y envía `SIGUSR1` al **consumidor**.
- El **consumidor** recibe la señal y procesa los trabajos.
- Se almacena y consulta la cola de trabajos en un archivo temporal.

**Código esencial (`productor.py`):**
```python
import os, signal

os.kill(consumidor_pid, signal.SIGUSR1)
```

**Código esencial (`consumidor.py`):**
```python
import signal

def procesar_trabajo(signum, frame):
    print("Procesando trabajo recibido.")

signal.signal(signal.SIGUSR1, procesar_trabajo)
```

---

## **Conclusiones**
- Las señales son una herramienta poderosa para **gestión de procesos y sistemas reactivos**.
- Su uso requiere **sincronización cuidadosa**, especialmente en entornos **multihilo y multiproceso**.
- Python proporciona **soporte básico** para señales en procesos principales, pero no en hilos secundarios.
- Dominar señales es clave para **programación de sistemas y administración UNIX**.
