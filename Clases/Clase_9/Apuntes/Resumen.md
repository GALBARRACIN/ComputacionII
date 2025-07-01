# 🧵 Dominando la Concurrencia en Python

## 🎯 Introducción General: La Orquesta de Procesos
- Concurrencia y paralelismo: necesarios en sistemas modernos.
- Problema central: condiciones de carrera.
- Solución: exclusión mutua con primitivas de sincronización de `multiprocessing`.

---

## 🔐 1. Lock: El Guardián de la Exclusión Mutua
- Primitiva básica: `acquire()` y `release()`.
- Garantiza acceso exclusivo a secciones críticas.
- Uso típico: protección de variables compartidas.
- Soporta el contexto `with` para evitar deadlocks.

---

## 🔁 2. RLock: Lock Reentrante
- Permite reentrancia: el mismo proceso puede adquirir el lock varias veces.
- Ideal en funciones recursivas o métodos sincronizados encadenados.
- Más costoso que un `Lock` simple.

---

## 🚦 3. Semaphore: Semáforo Contador
- Controla cuántos procesos pueden acceder simultáneamente.
- Casos: pools de conexiones, buffers limitados, control de carga.

---

## 🔒 4. BoundedSemaphore: Semáforo con Límite
- Igual que `Semaphore`, pero lanza error si se libera más de lo adquirido.
- Útil para detección de errores de sincronización.

---

## 📶 5. Condition: Variable de Condición
- Permite espera activa a condición específica.
- Combina `Lock` con `wait()` y `notify()`.
- Ideal para patrón productor-consumidor avanzado o sincronización por estado.

---

## 🚨 6. Event: Señal de Evento
- Bandera binaria compartida: `set()` y `clear()`.
- Procesos pueden esperar (`wait()`) a que un evento ocurra.
- Uso: inicio coordinado, señales de parada.

---

## 🧱 7. Barrier: Barrera de Sincronización
- Espera a que un número fijo de procesos lleguen antes de continuar.
- Uso común: sincronización por fases.

---

## 📬 8. Queue: Cola Segura de Procesos
- FIFO segura para compartir datos entre procesos.
- Uso: envío de tareas, logging, resultados.
- Subclase útil: `JoinableQueue` con `task_done()` y `join()`.

---

## 🔢 9. Value: Valor Compartido
- Para compartir un único valor simple (`int`, `float`, `bool`).
- Requiere `Lock` para operaciones compuestas.
- `.value` expone el valor actual.

---

## 📊 10. Array: Arreglo Compartido
- Similar a `Value`, pero para múltiples valores homogéneos.
- Acceso tipo lista: `arr[i]`.
- Necesita `Lock` para acceso seguro concurrente.

---

## 🎓 Conclusión General
- Cada primitiva tiene su aplicación ideal según la complejidad del problema.
- La elección apropiada mejora la escalabilidad, eficiencia y seguridad.
- Dominar estas herramientas permite construir software concurrente robusto y moderno.
