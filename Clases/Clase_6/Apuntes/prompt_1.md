# CLASE FIFOs Unix/Linux

## Pasos

#### 1- Concepto y contexto

- Explicación teórica sobre FIFOs.

- Diferencias con pipes anónimos.

- Su importancia en la comunicación entre procesos.

#### 2- reación de FIFOs en Linux

- Uso del comando mkfifo.

- Configuración de permisos y validación.

#### 3- Lectura y escritura en FIFOs con Python

- Ejemplos de código detallados.

- Manejando descriptores de archivo.

#### 4- Ejemplo con múltiples procesos

- Demostración de cómo el cursor no es compartido.

- Código en Python con procesos independientes.

#### 5- Ejercicio práctico

- Implementación de un sistema de log o chat basado en FIFOs.

- Desafío adicional para reforzar el aprendizaje.

#### 6- Pausa y preguntas de comprensión

- Te haré 2 o 3 preguntas para verificar que comprendiste bien.

- Te recordaré compartir avances con tus compañeros o profesor.

## Paso 1: Concepto y contexto de FIFOs.

Los FIFOs (First In, First Out) en Unix/Linux son una forma de pipe nombrado, lo que significa que persisten en el sistema de archivos y pueden ser utilizados por procesos independientes, en lugar de estar limitados a procesos padre-hijo. Se crean con mkfifo y permiten una comunicación estructurada.

A diferencia de los pipes anónimos, un FIFO:

- No depende de la relación padre-hijo, por lo que cualquier proceso con permisos adecuados puede leer y escribir en él.

- Tiene un nombre en el sistema de archivos, facilitando la sincronización.

- Preserva la naturaleza de acceso secuencial, lo que puede influir en el control de concurrencia.



## Paso 2: Creación de FIFOs en Linux

### Creando un FIFO en Linux
Para crear un FIFO, usamos el comando mkfifo en la terminal:

- mkfifo mi_fifo


Esto genera un archivo especial llamado mi_fifo, que se puede leer y escribir como un archivo común. Sin embargo, a diferencia de los archivos normales, el contenido no se almacena en el disco, sino que se transmite entre procesos.

Para verificar que se ha creado correctamente, usa:

- ls -l mi_fifo

Verás una salida similar a esta:

- prw-r--r-- 1 usuario usuario 0 May 19 12:30 mi_fifo


El prefijo p indica que es un pipe nombrado (FIFO).

### Configuración de permisos
Si necesitas modificar los permisos para que otros usuarios puedan interactuar con el FIFO, usa:

- chmod 666 mi_fifo

Esto permite lectura y escritura a cualquier usuario en el sistema. Antes de seguir, confirma que el FIFO se creó correctamente con ls -l.

## Paso 3: Lectura y escritura en FIFOs con Python

### Escritura en un FIFO
Podemos abrir el FIFO como si fuera un archivo normal y escribir en él:

- codigo python:

import os

fifo_path = "mi_fifo"

// Abrimos el FIFO en modo escritura
with open(fifo_path, "w") as fifo:
    fifo.write("¡Hola desde el proceso escritor!\n")
    print("Mensaje enviado al FIFO.")
// Fin


Este script abre mi_fifo en modo escritura y envía un mensaje. IMPORTANTE: Si no hay un proceso leyendo el FIFO, el programa se quedará bloqueado esperando un lector.

### Lectura desde un FIFO
Ahora, ejecuta el siguiente código en otro proceso o terminal para leer los datos:

- Codigo python:

fifo_path = "mi_fifo"

// Abrimos el FIFO en modo lectura
with open(fifo_path, "r") as fifo:
    mensaje = fifo.read()
    print("Mensaje recibido:", mensaje)
//Fin


Este proceso abrirá mi_fifo en modo lectura y mostrará el mensaje enviado por el otro proceso.


## Paso 3: Lectura y escritura en FIFOs con Python

Ahora usaremos Python para interactuar con el FIFO. Primero, probemos la escritura y lectura.

### 1. Escritura en un FIFO
Ejecuta este script en una terminal para escribir en mi_fifo:

- Codigo python:

import os

fifo_path = "mi_fifo"

// Abrir el FIFO en modo escritura
with open(fifo_path, "w") as fifo:
    fifo.write("Hola desde el proceso escritor\n")
    print("Mensaje enviado al FIFO")
// Fin

Este código abrirá el FIFO y escribirá un mensaje en él. Nota: Si no hay ningún proceso leyendo, la ejecución quedará bloqueada hasta que alguien lo haga.

### 2. Lectura desde un FIFO
En otra terminal, ejecuta este código:

- Codigo python:
fifo_path = "mi_fifo"

// Abrir el FIFO en modo lectura
with open(fifo_path, "r") as fifo:
    mensaje = fifo.read()
    print(f"Mensaje recibido: {mensaje}")
Esto abrirá el FIFO y leerá los datos que se escribieron en él.
// FIn


## Paso 4: Ejemplo con múltiples procesos

Ahora vamos a demostrar cómo dos procesos distintos pueden leer el mismo FIFO sin compartir la posición del cursor. Esto es importante porque en FIFOs, cada proceso que lee obtiene su propia vista del flujo de datos.

### Código con dos procesos lectores
Ejecuta este código en Python para simular dos lectores independientes:

- Codigo python:
import os
import multiprocessing

fifo_path = "mi_fifo"

def lector_1():
    with open(fifo_path, "r") as fifo:
        print("Lector 1 recibe:", fifo.read())

def lector_2():
    with open(fifo_path, "r") as fifo:
        print("Lector 2 recibe:", fifo.read())

// Primero escribimos datos en el FIFO
with open(fifo_path, "w") as fifo:
    fifo.write("Mensaje compartido en FIFO\n")

// Lanzamos ambos procesos lectores
p1 = multiprocessing.Process(target=lector_1)
p2 = multiprocessing.Process(target=lector_2)

p1.start()
p2.start()

p1.join()
p2.join()
// Fin

### Explicación del comportamiento

Cuando ejecutas este script, notarás que solo uno de los lectores recibe el mensaje, porque el FIFO no comparte la posición del cursor entre procesos. Esto significa que el primer lector que acceda al FIFO consumirá el mensaje, y el segundo proceso encontrará el FIFO vacío.


## Paso 4: Ejemplo con múltiples procesos y manejo del cursor

En este ejercicio, vamos a demostrar que dos procesos que leen un mismo FIFO no comparten la posición del cursor, lo que significa que cada proceso leerá los datos desde el inicio si abre el FIFO nuevamente.

### Código en Python:

Ejecuta primero este código en una terminal para escribir en el FIFO:

codigo python:
import os
import time

fifo_path = "mi_fifo"

// Abrir el FIFO en modo escritura
with open(fifo_path, "w") as fifo:
    fifo.write("Mensaje compartido para los lectores\n")
    print("Mensaje enviado al FIFO")
Ahora, en dos terminales diferentes, abre el FIFO para leer:

codigo python:
fifo_path = "mi_fifo"

// Abrir el FIFO en modo lectura
with open(fifo_path, "r") as fifo:
    mensaje = fifo.read()
    print(f"Proceso 1 recibió: {mensaje}")

Ejecuta el mismo código en otra terminal. Ambos procesos leerán el mismo mensaje, aunque el FIFO sea el mismo, porque cada uno abre el FIFO por separado.

Este comportamiento es diferente al de los pipes anónimos, donde el contenido se consume y no queda disponible para futuras lecturas.

## Paso 5: Ejercicio práctico – Sistema de log o canal de chat basado en FIFOs

Ahora aplicarás lo aprendido implementando un pequeño sistema de log o un canal de chat usando FIFOs.

### Opción 1: Sistema de Log
Aquí un ejemplo donde un proceso escribe eventos en un FIFO, y otro proceso los guarda en un archivo de log:

#### Proceso Escritor (en una terminal)

codigo python:
import os
import time

fifo_path = "mi_fifo"

while True:
    with open(fifo_path, "w") as fifo:
        mensaje = f"Evento registrado: {time.ctime()}\n"
        fifo.write(mensaje)
        print("Evento enviado al FIFO")
    time.sleep(2)  # Simular eventos periódicos

#### Proceso Lector (en otra terminal)

codigo python:
fifo_path = "mi_fifo"
log_path = "registro.log"

with open(fifo_path, "r") as fifo, open(log_path, "a") as log_file:
    while True:
        mensaje = fifo.readline()
        if mensaje:
            log_file.write(mensaje)
            print(f"Guardado en log: {mensaje.strip()}")

Este código crea un registro de eventos en tiempo real usando FIFOs.

### Opción 2: Chat Básico
En este caso, dos procesos pueden enviar y recibir mensajes a través de FIFOs.

#### Proceso de Envío de Mensajes

codigo python:

fifo_path = "chat_fifo"

while True:
    mensaje = input("Escribe tu mensaje: ")
    with open(fifo_path, "w") as fifo:
        fifo.write(mensaje + "\n")

#### Proceso de Recepción de Mensajes

codigo python:
fifo_path = "chat_fifo"

while True:
    with open(fifo_path, "r") as fifo:
        mensaje = fifo.readline()
        if mensaje:
            print(f"Mensaje recibido: {mensaje.strip()}")

Este ejemplo permite la comunicación entre dos terminales, simulando un chat básico.


## Paso 5: Ejercicio práctico – Sistema de log basado en FIFOs

Para reforzar el concepto, implementaremos un sistema de log en el que diferentes procesos envían mensajes a un FIFO, y un proceso central los almacena en un archivo.

### Código en Python
1. Creación del FIFO Ejecuta en la terminal:

- mkfifo log_fifo

2. Proceso escritor – Envía eventos al FIFO Este script simula eventos del sistema que deben registrarse en un archivo de log.

codigo python:

import os
import time

fifo_path = "log_fifo"

// Simular múltiples eventos de log
eventos = ["Inicio del sistema", "Conexión de usuario", "Error en servicio", "Finalización de sesión"]

for evento in eventos:
    with open(fifo_path, "w") as fifo:
        fifo.write(evento + "\n")
        print(f"Evento registrado: {evento}")
    time.sleep(1)

Cada evento se envía al FIFO, donde otro proceso los recolectará.

3. Proceso lector – Guarda los eventos en un archivo de log Ejecuta este script en otra terminal para recibir y almacenar los eventos en un archivo:

codigo python:

fifo_path = "log_fifo"
log_file = "system_log.txt"

with open(fifo_path, "r") as fifo, open(log_file, "a") as log:
    while True:
        linea = fifo.readline().strip()
        if not linea:
            break
        log.write(linea + "\n")
        print(f"Evento guardado: {linea}")

Este proceso lee continuamente desde el FIFO y registra los eventos en system_log.txt.

### Prueba y validación
Ejecuta ambos scripts en terminales diferentes. Luego, verifica system_log.txt para confirmar que todos los eventos fueron almacenados correctamente.