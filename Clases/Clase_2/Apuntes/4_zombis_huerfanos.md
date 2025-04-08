# 4. Procesos Zombis y Huérfanos

Cuando se trabaja con procesos en sistemas operativos, es fundamental comprender el concepto de **procesos zombis** y **procesos huérfanos**, ya que pueden afectar el rendimiento del sistema si no se manejan correctamente.

---

## 🧟 Procesos zombis

Un proceso zombi es un proceso que ha terminado su ejecución, pero aún permanece en la tabla de procesos del sistema porque su padre **no leyó su estado de salida** (no hizo un `wait()`).

- No consume CPU, pero **ocupa espacio en la tabla de procesos**.
- Aparecen como `<defunct>` al usar `ps` o `htop`.

**Cómo se crean:**
```python
import os
import time

pid = os.fork()

if pid == 0:
    print("Hijo terminado")
    exit(0)
else:
    time.sleep(10)  # El padre no hace wait inmediatamente
    os.wait()
```
---

## 👻 Procesos Huérfanos
Un proceso huérfano es un proceso cuyo padre ha terminado antes que él. En este caso, el sistema operativo automáticamente reasigna al proceso huérfano al proceso init o systemd, que se convierte en su nuevo padre.

🔧 ¿Es un problema?
No necesariamente, el sistema operativo se encarga de adoptarlos. Sin embargo, se debe tener cuidado si el proceso huérfano depende de recursos liberados por su padre.
