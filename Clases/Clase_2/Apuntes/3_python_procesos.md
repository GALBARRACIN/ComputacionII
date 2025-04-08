# 3. Manipulación de procesos con Python

En esta sección abordamos cómo manipular procesos en sistemas operativos desde Python utilizando funciones del módulo `os`, que permiten interactuar directamente con el sistema, similar a cómo lo hace un programa en C.

---

## 🔧 Funciones principales en la manipulación de procesos

| Función            | Qué hace                                                                 |
|--------------------|--------------------------------------------------------------------------|
| `os.fork()`        | Duplica el proceso actual. Crea un nuevo proceso hijo.                   |
| `os.exec*()`       | Reemplaza el proceso actual por otro programa.                           |
| `os.wait()`        | Hace que el proceso padre espere a que termine uno de sus hijos.         |
| `os.waitpid()`     | Igual que `wait()`, pero permite especificar qué proceso hijo esperar.   |

---

## 🧬 `os.fork()` – Crear un proceso hijo

La función `os.fork()` **duplica el proceso actual**. Crea un nuevo proceso hijo que ejecuta exactamente el mismo código que el padre desde la línea siguiente al `fork()`.

```python
import os

pid = os.fork()

if pid == 0:
    # Este bloque lo ejecuta el proceso hijo
    print("Hola desde el hijo!")
else:
    # Este bloque lo ejecuta el proceso padre
    print(f"Hola desde el padre. PID del hijo: {pid}")
```

- El proceso hijo recibe como valor de retorno 0.

- El proceso padre recibe el PID del hijo.

--- 

## 🔁 `os.exec*()` – Reemplazar un proceso por otro
La familia os.exec*() permite reemplazar el proceso actual con otro programa. Si exec() se ejecuta correctamente, el código posterior a esa llamada no se ejecuta porque el proceso original deja de existir.

```python
import os

# Reemplaza el proceso actual con el comando 'ls -l'
os.execvp("ls", ["ls", "-l"])
execvp() busca el programa en las rutas del sistema (PATH).
```

- El proceso original se sobreescribe completamente por el nuevo.

---

## ⏳ os.wait() y os.waitpid() – Sincronización entre procesos
Estas funciones permiten que el proceso padre espere a que uno de sus procesos hijos termine. Esto es útil para evitar procesos zombis y para mantener sincronización.

```python
import os
import time

pid = os.fork()

if pid == 0:
    print("Proceso hijo haciendo algo...")
    time.sleep(2)
    print("Hijo finalizó.")
else:
    print("Padre esperando que el hijo termine...")
    pid_terminado, estado = os.wait()
    print(f"Hijo {pid_terminado} terminó con estado {estado}")
os.wait() espera a cualquier hijo.

os.waitpid(pid, 0) espera a un hijo específico.
```
---

## 🔀 Combinando fork(), exec() y wait()
Es común combinar estas tres funciones para que un proceso padre cree un hijo, el hijo reemplace su ejecución con otro programa y el padre espere a que termine.

```python
import os

pid = os.fork()

if pid == 0:
    # El hijo ejecuta otro programa
    os.execvp("ls", ["ls", "-l"])
else:
    # El padre espera que el hijo termine
    os.wait()
    print("El hijo terminó. El padre continúa.")
```
---

## 🧠 Resumen rápido
- fork(): duplica el proceso actual.

- exec(): reemplaza el código del proceso actual por otro programa.

- wait() / waitpid(): el padre espera a que su hijo termine, evitando zombis.

---

## 👀 Recomendación para probar
Mientras ejecutás los scripts de ejemplo, usá herramientas del sistema como:

- htop (en terminal, más visual)

- ps aux (para ver procesos activos)

- pstree (para ver la jerarquía de procesos)