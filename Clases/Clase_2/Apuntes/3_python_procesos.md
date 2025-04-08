# 3. Manipulación de procesos con Python

Python permite crear y controlar procesos usando el módulo `os`, que proporciona funciones del sistema operativo como `fork()`, `exec()` y `wait()`. Estas funciones están disponibles en sistemas UNIX/Linux y permiten manipular procesos a bajo nivel.

---

## 🔁 os.fork()

La función `os.fork()` crea un nuevo proceso. El proceso original se llama **padre**, y el nuevo proceso generado se llama **hijo**. Ambos procesos continúan ejecutando el código a partir del mismo punto.

- En el proceso hijo, `os.fork()` devuelve `0`.
- En el proceso padre, devuelve el PID del hijo.

**Ejemplo:**
```python
import os

pid = os.fork()

if pid == 0:
    print("Soy el hijo. PID:", os.getpid())
else:
    print("Soy el padre. PID del hijo:", pid)
