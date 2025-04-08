# Fundamentos de Procesos

## ¿Qué es un proceso?

Un **proceso** es un programa en ejecución. Es una unidad activa que posee su propio contexto de ejecución, incluyendo:

- **PID (Process ID)**: identificador único.
- **Estado**: listo, ejecutando, bloqueado, etc.
- **Contador de programa**: indica la siguiente instrucción a ejecutar.
- **Stack**: contiene llamadas a funciones, variables locales, etc.
- **Heap**: memoria dinámica.
- **Sección de datos**: variables globales.

## Programa vs Proceso

| Programa (código)       | Proceso (en ejecución)         |
|-------------------------|--------------------------------|
| Es pasivo               | Es activo                      |
| No usa recursos         | Usa CPU, memoria, etc.         |
| Puede generar procesos  | Es instanciado desde un programa |

## Historia

- En los primeros sistemas, solo un proceso podía ejecutarse a la vez.
- Con el tiempo, surgieron **procesos concurrentes** y **multitarea**.
- Hoy, los procesos permiten ejecución paralela, aislamiento y seguridad.

---

## 🛑 Puesta en común

- ¿Qué diferencia hay entre un proceso y un programa?
- ¿Qué atributos importantes tiene un proceso?
- ¿Qué recursos controla el sistema operativo por cada proceso?

💬 Compartí estas respuestas con tu profesor.
