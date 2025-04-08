# El Modelo de Procesos en UNIX/Linux

## Jerarquía de Procesos

Los procesos en UNIX/Linux forman un árbol. Todo proceso es creado por otro (proceso padre).

- El proceso **init** (ahora reemplazado por `systemd` en muchas distros) es el ancestro de todos los procesos.
- Se puede ver esta jerarquía con:
  ```bash
  pstree
