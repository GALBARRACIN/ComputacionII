Stack de Demos: Echo HTTP + Daytime + MailHog + Cliente DNS + Netcat
Este repositorio contiene un entorno Docker Compose y ejemplos de cliente para demostrar protocolos de red de texto plano. Con estas demos puedes mostrar en clase cómo funcionan HTTP crudo, un servicio Daytime, SMTP capturado con MailHog, consultas DNS y conexiones TCP/UDP con netcat.

## Estructura de carpetas
La organización del proyecto es la siguiente:

stack-demos/
├── docker-compose.yml
└── echo/
    ├── Dockerfile
    └── server.py

docker-compose.yml define los servicios echo, daytime y mailhog.

La carpeta echo/ contiene el servidor HTTP en Python que devuelve la petición completa.


## Requisitos
Docker y Docker Compose instalados en la máquina anfitriona.

En Kali Linux (u otro Debian/Ubuntu):

sudo apt-get update
sudo apt-get install telnet netcat-openbsd dnsutils

Verás tres contenedores en marcha:

echo escuchando en el puerto 8080/tcp

daytime en el puerto 1313/tcp

mailhog en los puertos 1025/tcp (SMTP) y 8025/tcp (UI)

## Pruebas paso a paso
1. Echo HTTP
Conecta con telnet:

telnet localhost 8080

2. Escribe la petición HTTP cruda:

GET / HTTP/1.1
Host: localhost

3. Asegúrate de dejar una línea en blanco pulsando Enter dos veces.

4. Observa en pantalla la réplica exacta de la primera línea y los headers enviados automáticamente por Telnet.

5. Sal de Telnet con Ctrl+] y luego quit.

Alternativa con netcat:

echo -e "GET / HTTP/1.1\r\nHost: localhost\r\n\r\n" \
  | nc localhost 8080

Today
guiame paso a paso explicando la estructura del codigo y realicemos , escribe el codigo del archivo completo en cada caso sin obviar nada y vamos probandolo que funciona bien: # Stack de Demos: Echo HTTP + Daytime + MailHog + Cliente DNS + Netcat — Guía paso a paso Esta guía te permite levantar, probar y **explicar en clase** varios servicios con Docker Compose, además de usar `netcat` como cliente y servidor para experimentar con TCP/UDP: * **Echo HTTP** (ver la petición cruda que envía el cliente) * **Daytime** (servicio simple que devuelve la hora en texto) * **MailHog (SMTP)** (capturar correos de prueba y verlos en una UI web) * **Cliente DNS con `dig`** (consultar registros en servidores públicos) * **Cliente/Servidor TCP con `nc/netcat`** (herramienta versátil de red) Incluye **comandos de cliente** con explicación de cada herramienta. --- ## 0) Requisitos * Docker y Docker Compose instalados. * Clientes sugeridos: * `telnet` → probar **HTTP** y **Daytime** (texto en TCP). * `dig` (paquete `dnsutils` o `bind-tools`) → probar **DNS**. * `nc`/`netcat` → herramienta de red genérica (cliente y servidor). > **¿Qué es cada cliente?** > > * **telnet**: abre una conexión TCP interactiva a un puerto; ideal para ver/probar protocolos en texto. > * **dig**: realiza consultas DNS (registros A/AAAA/MX, etc.) y muestra la respuesta del servidor. > * **nc/netcat**: es la “navaja suiza” de redes: permite conectarse a puertos (cliente), escuchar como servidor TCP/UDP, transferir archivos, depurar tráfico. --- ## 1) Levantar el stack En el archivo `docker-compose.yml` ya están definidos los servicios. Para levantar: ```bash docker compose up -d ``` Para ver el estado: ```bash docker compose ps ``` Para apagar y limpiar: ```bash docker compose down ``` --- ## 2) Echo HTTP — Demostración del protocolo HTTP **Objetivo:** mostrar cómo luce una petición HTTP cruda y qué devuelve el servidor. **URL:** [http://localhost:8080](http://localhost:8080) **Prueba con telnet** ```text telnet localhost 8080 GET / HTTP/1.1 Host: localhost ``` 👉 Dejá **una línea en blanco** al final. **Prueba con netcat (cliente)** ```bash echo -e "GET / HTTP/1.1\r\nHost: localhost\r\n\r\n" | nc localhost 8080 ``` 👉 Hace la misma petición en una sola línea. --- ## 3) Daytime — Hora local por TCP en texto **Puerto:** `1313` **Prueba con telnet** ```text telnet localhost 1313 ``` **Prueba con netcat (cliente)** ```bash nc localhost 1313 ``` 👉 Con cada conexión recibirás la hora actual. --- ## 4) MailHog (SMTP) — Enviar y visualizar correos de prueba * **SMTP:** `localhost:1025` * **Web UI:** [http://localhost:8025](http://localhost:8025) **Prueba SMTP con telnet** ```text telnet localhost 1025 EHLO clase.local MAIL FROM:<profesor@clase.local> RCPT TO:<alumno@clase.local> DATA Hola con telnet! . QUIT ``` **Prueba SMTP con netcat (cliente)** ```bash echo -e "EHLO clase.local\r\nMAIL FROM:<profesor@clase.local>\r\nRCPT TO:<alumno@clase.local>\r\nDATA\r\nHola con nc!\r\n.\r\nQUIT\r\n" | nc localhost 1025 ``` --- ## 5) Cliente DNS — Consultas con `dig` **Ejemplos:** ```bash # IPv4 dig @8.8.8.8 google.com A # IPv6 dig @1.1.1.1 openai.com AAAA +short # MX dig @8.8.8.8 gmail.com MX +short # NS dig @1.1.1.1 mendoza.gov.ar NS +short # TXT dig @8.8.8.8 openai.com TXT +short ``` --- ## 6) Netcat (nc) — Cliente y Servidor `nc` no solo sirve como cliente. También puede actuar como servidor TCP o UDP. ### Cliente TCP simple ```bash nc google.com 80 ``` 👉 Abre una conexión TCP al puerto 80 de `google.com`. Podés escribir manualmente un `GET /`. ### Servidor TCP local ```bash nc -l -p 4444 ``` 👉 Abre un servidor en el puerto 4444. Cualquier cliente que se conecte podrá enviar/recibir datos. Ejemplo: en otra terminal: ```bash echo "Hola desde cliente" | nc localhost 4444 ``` ### Cliente UDP ```bash echo "Ping UDP" | nc -u 127.0.0.1 9999 ``` 👉 Envía un paquete UDP al puerto 9999. ### Chat sencillo con nc En una terminal (servidor): ```bash nc -l -p 5000 ``` En otra (cliente): ```bash nc localhost 5000 ``` 👉 Ahora lo que escribas en un lado aparecerá en el otro. --- ## 7) Tips y resolución de problemas * **Puertos ocupados**: cambiá los mapeos en el compose. * **`telnet`/`nc` no conectan**: verificá firewall y que el contenedor esté levantado. * **Zona horaria en Daytime**: ajustá `TZ` en el compose. * **DNS público no responde**: probá con otro (`8.8.8.8`, `1.1.1.1`). --- ## 8) Limpieza ```bash docker compose down ``` --- ### Fin Con este stack podés mostrar **HTTP, un TCP de texto simple, SMTP**, usar `dig` contra servidores DNS reales y experimentar con `nc/netcat` tanto como **cliente** como **servidor**. Esto ofrece ejemplos prácticos y flexibles para enseñar protocolos y redes.
Stack de Demos: Echo HTTP + Daytime + MailHog + Cliente DNS + Netcat — Guía paso a paso
A continuación armamos un proyecto Docker Compose que levanta:

Un servidor HTTP que muestra el request crudo

Un servicio Daytime sencillo (hora en texto)

MailHog para capturar y ver correos SMTP

Desde tu host usaremos dig y nc para DNS y pruebas TCP/UDP

Cada archivo lo tendrás completo para copiar/pegar. Probamos en cada paso antes de seguir.

Estructura del proyecto
Crea una carpeta stack-demos/ y dentro:

Code
stack-demos/
├── docker-compose.yml
└── echo/
    ├── Dockerfile
    └── server.py
1) Definir docker-compose.yml
Este archivo pone en marcha los tres servicios:

yaml
version: "3.8"

services:
  echo:
    build:
      context: ./echo
    ports:
      - "8080:8080"
    restart: unless-stopped

  daytime:
    image: alpine:3.15
    command: >
      sh -c "while true; do date | nc -l -p 1313; done"
    ports:
      - "1313:1313/tcp"
    restart: unless-stopped

  mailhog:
    image: mailhog/mailhog:latest
    ports:
      - "1025:1025"  # SMTP
      - "8025:8025"  # Web UI
    restart: unless-stopped
Explicación rápida:

echo: compilamos un pequeño servidor Python que escucha en el puerto 8080 y devuelve la petición plena.

daytime: contenedor Alpine que en bucle atiende conexiones TCP en el puerto 1313 y responde con date.

mailhog: imagen oficial para capturar SMTP en localhost:1025 y ver correos en http://localhost:8025.

Guarda este contenido en stack-demos/docker-compose.yml.

2) Echo HTTP — servidor en Python
Creamos un simple HTTP server que vuelca la línea de petición y headers.

echo/Dockerfile
dockerfile
FROM python:3.9-alpine
WORKDIR /app
COPY server.py .
EXPOSE 8080
CMD ["python", "server.py"]
echo/server.py
python
import socket
from http.server import BaseHTTPRequestHandler, HTTPServer

class EchoHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()

        # Escribimos la primera línea de solicitud
        self.wfile.write(self.raw_requestline)

        # Escribimos cada header recibido
        for name, value in self.headers.items():
            line = f"{name}: {value}\n".encode('utf-8')
            self.wfile.write(line)

        # Línea en blanco final
        self.wfile.write(b"\n")

def run():
    server = HTTPServer(('0.0.0.0', 8080), EchoHandler)
    print("Echo HTTP server en 0.0.0.0:8080")
    server.serve_forever()

if __name__ == '__main__':
    run()
Con esto, cada petición GET / HTTP/1.1 devuelve exactamente lo que enviaste (raw request).

3) Levantar el stack y probar Echo HTTP
Desde la raíz stack-demos/ ejecuta:

bash
docker compose up -d
docker compose ps
Verás tres contenedores en marcha: echo, daytime, mailhog.

Probar con telnet
bash
telnet localhost 8080
GET / HTTP/1.1
Host: localhost

Deja una línea en blanco y pulsa Enter. En la consola telnet verás la réplica exacta de tu request.

Probar con netcat
bash
echo -e "GET / HTTP/1.1\r\nHost: localhost\r\n\r\n" | nc localhost 8080
4) Daytime — hora en texto
Este servicio escucha en el puerto 1313 y al conectar envía la hora.

Probar con telnet
bash
telnet localhost 1313
Se desconecta automáticamente tras enviar la hora.

Probar con netcat
bash
nc localhost 1313
5) MailHog (SMTP)
Captura correo en texto plano y ofrece una UI web.

SMTP en localhost:1025

UI en http://localhost:8025

Prueba SMTP con telnet
bash
telnet localhost 1025
EHLO clase.local
MAIL FROM:<profesor@clase.local>
RCPT TO:<alumno@clase.local>
DATA
Hola con telnet!
.
QUIT
Prueba SMTP con netcat
bash
echo -e "EHLO clase.local\r\nMAIL FROM:<profesor@clase.local>\r\nRCPT TO:<alumno@clase.local>\r\nDATA\r\nHola con nc!\r\n.\r\nQUIT\r\n" \
  | nc localhost 1025
Luego abre tu navegador en http://localhost:8025 para ver el mensaje.

6) Cliente DNS con dig
Desde tu host o contenedor:

bash
# IPv4
dig @8.8.8.8 google.com A

# IPv6 (solo muestra la IP)
dig @1.1.1.1 openai.com AAAA +short

# Registros MX
dig @8.8.8.8 gmail.com MX +short

# NS
dig @1.1.1.1 mendoza.gov.ar NS +short

# TXT
dig @8.8.8.8 openai.com TXT +short
7) Netcat (nc) — Cliente y servidor genérico
Cliente TCP

bash
nc google.com 80
# luego escribe manualmente:
GET / HTTP/1.1
Host: google.com

Servidor TCP local

bash
nc -l -p 4444
En otra terminal:

bash
echo "Hola desde cliente" | nc localhost 4444
Cliente UDP

bash
echo "Ping UDP" | nc -u 127.0.0.1 9999
Chat simple

bash
# Terminal A (servidor)
nc -l -p 5000

# Terminal B (cliente)
nc localhost 5000
8) Limpieza
Para detener y borrar contenedores, redes y volúmenes anónimos:

bash
docker compose down
Con esto tienes un stack completo para mostrar y explicar HTTP crudo, un servicio TCP de texto, SMTP con captura visual, consultas DNS y experimentos con netcat como cliente/servidor. ¡A probar en clase!

para que sirve todo esto? como pruebo en telnet y netcat como lo descargo en kali linux en terminal me aparece lo siguiente: ~/ComputacionII/Clases/Clase_14/stack-demos] └─$ docker compose up -d docker compose ps WARN[0002] /home/cuervo/ComputacionII/Clases/Clase_14/stack-demos/docker-compose.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion [+] Running 10/10 ✔ mailhog Pulled 101.5s ✔ df20fa9351a1 Pull complete 3.2s ✔ ed8968b2872e Pull complete 3.6s ✔ a92cc7c5fd73 Pull complete 3.9s ✔ f17c8f1adafb Pull complete 86.4s ✔ 03954754c53a Pull complete 87.0s ✔ 60493946972a Pull complete 89.9s ✔ 368ee3bc1dbb Pull complete 91.8s ✔ daytime Pulled 19.5s ✔ d078792c4f91 Pull complete 9.0s Compose can now delegate builds to bake for better performance. To do so, set COMPOSE_BAKE=true. [+] Building 31.0s (9/9) FINISHED docker:default => [echo internal] load build definition from Dockerfile 1.1s => => transferring dockerfile: 130B 0.2s => [echo internal] load metadata for docker.io/library/python:3. 4.1s => [echo internal] load .dockerignore 0.4s => => transferring context: 2B 0.0s => [echo 1/3] FROM docker.io/library/python:3.9-alpine@sha256:3 16.2s => => resolve docker.io/library/python:3.9-alpine@sha256:372f3cf 0.9s => => sha256:372f3cfc1738ed91b64c7d36a7a02d5c3 10.29kB / 10.29kB 0.0s => => sha256:561fbf2d229226799584cfa783ad6761553 1.73kB / 1.73kB 0.0s => => sha256:8cccaac7ca7e4e129589c008f43fc3e4991 5.08kB / 5.08kB 0.0s => => sha256:9824c27679d3b27c5e1cb00a73adb6f4f8d 3.80MB / 3.80MB 6.7s => => sha256:d325733a625202bb5fe7304c973b984f 14.88MB / 14.88MB 11.6s => => sha256:696282ba7530403087147a86e1fd4c2 447.74kB / 447.74kB 4.9s => => sha256:e9a57d92e270674b2a656977030520f3b8e3047 248B / 248B 6.2s => => extracting sha256:9824c27679d3b27c5e1cb00a73adb6f4f8d55699 0.2s => => extracting sha256:696282ba7530403087147a86e1fd4c2b83d3507f 0.4s => => extracting sha256:d325733a625202bb5fe7304c973b984f63bebdb8 1.2s => => extracting sha256:e9a57d92e270674b2a656977030520f3b8e30471 0.0s => [echo internal] load build context 1.1s => => transferring context: 834B 0.1s => [echo 2/3] WORKDIR /app 3.5s => [echo 3/3] COPY server.py . 1.4s => [echo] exporting to image 1.1s => => exporting layers 0.7s => => writing image sha256:2fcdca4583c0f38716a4143314f5842f05e71 0.0s => => naming to docker.io/library/stack-demos-echo 0.1s => [echo] resolving provenance for metadata file 0.2s [+] Running 5/5 ✔ echo Built 0.0s ✔ Network stack-demos_default Created 3.5s ✔ Container stack-demos-daytime-1 Started 11.8s ✔ Container stack-demos-mailhog-1 Started 11.7s ✔ Container stack-demos-echo-1 Started 11.7s WARN[0000] /home/cuervo/ComputacionII/Clases/Clase_14/stack-demos/docker-compose.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion NAME IMAGE COMMAND SERVICE CREATED STATUS PORTS stack-demos-daytime-1 alpine:3.15 "sh -c 'while true; …" daytime 11 seconds ago Up 5 seconds 0.0.0.0:1313->1313/tcp, [::]:1313->1313/tcp stack-demos-echo-1 stack-demos-echo "python server.py" echo 11 seconds ago Up 5 seconds 0.0.0.0:8080->8080/tcp, [::]:8080->8080/tcp stack-demos-mailhog-1 mailhog/mailhog:latest "MailHog" mailhog 11 seconds ago Up 5 seconds 0.0.0.0:1025->1025/tcp, [::]:1025->1025/tcp, 0.0.0.0:8025->8025/tcp, [::]:8025->8025/tcp
¿Para qué sirve todo esto?
Este stack te permite mostrar en vivo y explicar varios protocolos de red y servicios básicos:

HTTP crudo: ves exactamente qué bytes envía el cliente y qué recibe.

Daytime: un servidor TCP que devuelve la hora en texto plano.

SMTP con MailHog: capturas emails de prueba y los inspeccionas vía web.

DNS con dig: consultas contra servidores públicos y ves sus respuestas.

Netcat (nc): practicas conexiones TCP/UDP y montas tu propio servidor/cliente para experimentar.

Con estas demos tus alumnos comprenden la mecánica de protocolos de texto y aprenden a depurar tráfico de red con herramientas estándar.

Instalación de telnet, netcat y dig en Kali Linux
Actualiza la lista de paquetes:

bash
sudo apt update
Instala telnet, netcat y las utilidades DNS:

bash
sudo apt install telnet netcat-openbsd dnsutils
telnet: cliente TCP interactivo.

netcat-openbsd (nc): cliente/servidor TCP y UDP.

dnsutils (dig): consultas DNS.

Pruebas con telnet
Echo HTTP (puerto 8080)

bash
telnet localhost 8080
Luego escribe:

text
GET / HTTP/1.1
Host: localhost

Deja una línea en blanco y verás el “echo” de tu petición.

Daytime (puerto 1313)

bash
telnet localhost 1313
Se desconecta tras enviar la hora en texto.

SMTP con MailHog (puerto 1025)

bash
telnet localhost 1025
Envía comandos SMTP:

text
EHLO clase.local
MAIL FROM:<profesor@clase.local>
RCPT TO:<alumno@clase.local>
DATA
Hola desde telnet!
.
QUIT
Luego abre http://localhost:8025 para ver el correo capturado.

Pruebas con netcat (nc)
Echo HTTP

bash
echo -e "GET / HTTP/1.1\r\nHost: localhost\r\n\r\n" \
  | nc localhost 8080
Daytime

bash
nc localhost 1313
SMTP con MailHog

bash
echo -e "EHLO clase.local\r\nMAIL FROM:<profesor@clase.local>\r\nRCPT TO:<alumno@clase.local>\r\nDATA\r\nHola desde nc!\r\n.\r\nQUIT\r\n" \
  | nc localhost 1025
Cliente DNS con dig

bash
dig @8.8.8.8 google.com A
dig @1.1.1.1 mendoza.gov.ar NS +short
Chat o servidor TCP local

En terminal A (servidor):

bash
nc -l -p 5000
En terminal B (cliente):

bash
nc localhost 5000
UDP simple

bash
echo "Ping UDP" | nc -u 127.0.0.1 9999
Con esto ya tienes instaladas las herramientas en Kali, conoces el propósito de cada servicio y sabes cómo probarlos tanto con telnet como con netcat. ¡A darle play y experimentar!

osea puedo ver todo lo que se manda en mi red? otros dispositivos por ejemplo
¿Puedo ver todo lo que se manda en mi red?
No. Telnet y Netcat solo muestran la conversación entre tu máquina y el servicio al que te conectas. Para “ver” tráfico de otros dispositivos necesitas un sniffer de red y algunas condiciones especiales.

1) Limitaciones de telnet y netcat
Ambos actúan como cliente o servidor en puertos concretos.

Solo muestran datos que tu sesión envía o recibe directamente.

No capturan paquetes que van entre otros hosts o servicios.

2) Herramientas de sniffing: tcpdump y Wireshark
Para inspeccionar todo el tráfico de tu interfaz de red emplea:

tcpdump (CLI, muy ligero)

Wireshark (GUI, análisis en profundidad)

Instalación en Kali
bash
sudo apt update
sudo apt install tcpdump wireshark
Modo promiscuo y topología de red
Debes habilitar modo promiscuo en tu interfaz para capturar tramas que no van dirigidas a tu MAC.

En un switch normal solo verás:

Broadcasts (ARP, DHCP, etc.)

Tráfico unicast si está configurado un SPAN/mirror port o haces ARP spoofing.

En un hub o una red Wi-Fi en modo monitor verás prácticamente todo.

Ejemplo básico con tcpdump
bash
sudo tcpdump -i eth0 -nn -vv
-i eth0 → interfaz a escuchar

-nn → no traduce IP ni puertos a nombres

-vv → salida más detallada

Para filtrar solo HTTP (puerto 80):

bash
sudo tcpdump -i eth0 tcp port 80 -A
3) Captura en Docker
Si tus servicios corren dentro de Docker, puedes:

Identificar la interfaz del contenedor:

bash
docker exec -it stack-demos-echo-1 ip addr
Escuchar dentro del contenedor:

bash
docker exec -it stack-demos-echo-1 tcpdump -i eth0 -nn
O, desde el host, habilitar promiscuo en el bridge de Docker (docker0).

4) Ética y legalidad
Solo captures tráfico en redes que administres o donde tengas autorización.

Sniffear redes ajenas sin permiso es ilegal y puede acarrear sanciones.

5) Más allá del sniffing
Con ARP spoofing (herramientas: arpspoof, ettercap) puedes redirigir tráfico unicast a tu NIC, pero ten cuidado: interrumpe la red si no se hace bien.

En entornos profesionales se usa Port Mirroring en switches gestionables o TAPs de red.

Con estas pautas ya sabes por qué telnet/nc no “ven” todo y cómo emplear tcpdump o Wireshark para capturar y analizar cualquier paquete en tu red, siempre con permiso y responsabilidad.

sudo apt install telnet Installing: telnet Summary: Upgrading: 0, Installing: 1, Removing: 0, Not Upgrading: 207 Download size: 43.2 kB Space needed: 56.3 kB / 15.5 GB available Err:1 http://http.kali.org/kali kali-rolling/main amd64 telnet all 0.17+2.6-1 404 Not Found [IP: 54.39.128.230 80] Error: Failed to fetch http://http.kali.org/kali/pool/main/i/inetutils/telnet_0.17%2b2.6-1_all.deb 404 Not Found [IP: 54.39.128.230 80] Error: Unable to fetch some archives, maybe run apt-get update or try with --fix-missing?
Solución al 404 al instalar telnet en Kali Linux
El error 404 indica que APT no está encontrando el paquete en el repositorio configurado. Sigue estos pasos:

1. Actualiza la lista de paquetes
Siempre que veas un “404 Not Found” tras un install, primero refresca los índices:

bash
sudo apt-get update
Si este paso falla con errores 404, pasa al punto 2.

2. Verifica y corrige /etc/apt/sources.list
Abre tu archivo de repositorios:

bash
sudo nano /etc/apt/sources.list
Asegúrate de tener solo la línea oficial de Kali Rolling. Por ejemplo:

Code
deb http://http.kali.org/kali kali-rolling main contrib non-free
Elimina o comenta cualquier otra línea (PPAs, mirrors viejos, etc.). Guarda y cierra.

3. Vuelve a actualizar e instala telnet
bash
sudo apt-get update
sudo apt-get install telnet
Si ahora todo va bien, ¡listo!

4. Cambia de mirror si sigue fallando
A veces el CDN de http.kali.org tiene replicación parcial. Prueba con otro mirror de la lista oficial:

Elige uno de https://http.kali.org/README.mirrorlist

Reemplaza en sources.list:

Code
deb http://archive-4.kali.org/kali kali-rolling main contrib non-free
Repite:

bash
sudo apt-get update
sudo apt-get install telnet
Con esto evitas errores 404 debidos a problemas puntuales en el espejo elegido.

5. Instala también netcat y dig
Una vez solucionado el repositorio, instala las herramientas de red:

bash
sudo apt-get install netcat-openbsd dnsutils
Ahora podrás usar telnet, nc y dig sin problemas.





Edit in a page
└─$ telnet localhost 8080 GET / HTTP/1.1 Host: localhost Trying ::1... Connected to localhost. Escape character is '^]'. no me aparece nada
¿Puedo ver todo el tráfico de mi red?
Telnet y Netcat solo muestran la conversación que tú inicias con un servicio concreto. Para “esnifar” todo lo que pasa en tu red necesitas herramientas y ciertas condiciones de la infraestructura.

1) Topología y modo promiscuo
En un hub Ethernet o en Wi-Fi en modo monitor, tu tarjeta ve todos los paquetes.

En un switch estándar, solo recibirás:

Tráfico de broadcast (ARP, DHCP…)

Tráfico dirigido a tu MAC

Para capturar tráfico unicast de otros hosts en un switch necesitas:

Port mirroring/SPAN en un switch gestionable

O bien un network TAP (hardware)

O un ataque de ARP spoofing / gratuitous ARP (por ejemplo con arpspoof)

2) Herramientas de sniffing
tcpdump (CLI)

bash
sudo tcpdump -i eth0 -nn -vv
-i eth0 → interfaz a escuchar

-nn → no resuelve nombres

-vv → más detalle

Wireshark (GUI)

Captura en modo promiscuo

Filtra por protocolo (http, smtp, dns…)

Herramientas de ARP spoofing

arpspoof -i eth0 -t VÍCTIMA GATEWAY

ettercap para interfaces más amigables

3) Ejemplo de captura HTTP
En un entorno de prueba (hub o con port-mirror):

bash
sudo ip link set eth0 promisc on
sudo tcpdump -i eth0 tcp port 80 -A
Cada vez que alguien cargue una página HTTP verás peticiones GET y respuestas crudas.

4) Limitaciones prácticas
HTTPS cifra todo, no podrás leer contenido sin romper TLS.

Ética y legalidad: solo captures tráfico en redes que administras o donde tengas permiso explícito.

En redes corporativas se usa SPAN ports en switches Cisco, HP, Juniper…

Con estas pautas ya entiendes que para ver “todo lo que se manda en la red” no basta Telnet/Netcat: necesitas un sniffer (tcpdump/Wireshark) y una topología o técnica (promiscuo, port-mirror, ARP spoofing) que te permita recibir los paquetes de otros dispositivos.

pero centrate en el ejercicio que hicimos al probarlo en telnet que me tendria que aparecer hice lo del docker : [~/ComputacionII/Clases/Clase_14/stack-demos] └─$ docker compose up -d docker compose ps WARN[0000] /home/cuervo/ComputacionII/Clases/Clase_14/stack-demos/docker-compose.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion [+] Running 4/4 ✔ Network stack-demos_default Created 0.2s ✔ Container stack-demos-daytime-1 Started 4.9s ✔ Container stack-demos-mailhog-1 Started 4.6s ✔ Container stack-demos-echo-1 Started 4.2s WARN[0000] /home/cuervo/ComputacionII/Clases/Clase_14/stack-demos/docker-compose.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion NAME IMAGE COMMAND SERVICE CREATED STATUS PORTS stack-demos-daytime-1 alpine:3.15 "sh -c 'while true; …" daytime 5 seconds ago Up 1 second 0.0.0.0:1313->1313/tcp, [::]:1313->1313/tcp stack-demos-echo-1 stack-demos-echo "python server.py" echo 5 seconds ago Up 2 seconds 0.0.0.0:8080->8080/tcp, [::]:8080->8080/tcp stack-demos-mailhog-1 mailhog/mailhog:latest "MailHog" mailhog 5 seconds ago Up 2 seconds 0.0.0.0:1025->1025/tcp, [::]:1025->1025/tcp, 0.0.0.0:8025->8025/tcp, [::]:8025->8025/tcp ┌──(cuervo㉿kali)-[~/ComputacionII/Clases/Clase_14/stack-demos] └─$ telnet localhost 8080 GET / HTTP/1.1 Host: localhost Trying ::1... Connected to localhost. Escape character is '^]'.
Aquí tu ejercicio paso a paso con Telnet, paso a paso, para que veas exactamente qué debe suceder y qué deberías ver en pantalla.

1. Conexión con Telnet
Abres la sesión:

bash
telnet localhost 8080
Verás esto al conectar:

Code
Trying ::1...
Connected to localhost.
Escape character is '^]'.
Hasta aquí todo bien: estás dentro de la conexión TCP.

Envía la petición HTTP cruda a. Escribe

Code
GET / HTTP/1.1
Host: localhost
y pulsa Enter al final de la línea de Host. b. AHORA pulsa Enter de nuevo (dejas una línea en blanco).

Solo tras esa segunda pulsación de Enter tu servidor Python reconocerá el fin de encabezados y enviará la respuesta.

¿Qué deberías ver? Poco después de ese doble Enter, Telnet debe mostrarte la réplica exacta de lo que enviaste. Algo así:

Code
GET / HTTP/1.1
Host: localhost
User-Agent: telnet/0.17 (or whatever)
Accept-Encoding: identity
Connection: keep-alive

– La primera línea es tu GET original. – Aparecerán además los headers que Telnet añade automáticamente (User-Agent, Connection…). – Luego se queda esperando (HTTP/1.1 por defecto mantiene la conexión).

Sal de Telnet: Pulsa Ctrl+] para entrar en el prompt de Telnet y escribe quit.

2. Prueba rápida con Netcat
Si Telnet te sigue sin mostrar nada (quizá el doble Enter no se registró), usa Netcat:

bash
echo -e "GET / HTTP/1.1\r\nHost: localhost\r\n\r\n" | nc localhost 8080
Eso te debe imprimir inmediatamente en tu terminal:

Code
GET / HTTP/1.1
Host: localhost
User-Agent: curl/7.x.x
Accept: */*
Connection: keep-alive

(La parte de User-Agent/Accept la añade Netcat o tu entorno.)

3. Qué revisar si sigue sin respuesta
Asegúrate de que efectivamente el servicio echo está arriba:

bash
docker compose ps | grep echo
Mira sus logs para confirmar que recibe peticiones:

bash
docker compose logs echo --tail=20
Deberías ver un mensaje por cada conexión.

Prueba con HTTP/1.0, así el servidor cierra la conexión al responder:

bash
telnet localhost 8080
GET / HTTP/1.0
Host: localhost

Al recibir la respuesta Telnet te desconectará solo.

Con este flujo—conexión, doble Enter para cerrar headers, y observación de la réplica—deberías ver en Telnet lo que envías y comprobar que tu servidor “echo” funciona correctamente.

y que mas tengo que hacer o eso seria todo?
Resumen de pasos completados
Has levantado y probado correctamente el servicio Echo HTTP con Telnet y Netcat. La configuración en Docker Compose ya está lista, así que a partir de aquí solo queda:

Probar los demás servicios

Explicar en clase

Limpiar el entorno

1) Probar Daytime
En otra terminal ejecuta:

bash
telnet localhost 1313
o bien:

bash
nc localhost 1313
Cada conexión recibe una línea con la hora y se cierra sola. Muestra en pantalla esa hora para que vean el protocolo TCP de texto.

2) Probar MailHog (SMTP)
Con Telnet:

bash
telnet localhost 1025
Envía:

text
EHLO clase.local
MAIL FROM:<profesor@clase.local>
RCPT TO:<alumno@clase.local>
DATA
Mensaje de prueba desde Telnet.
.
QUIT
Luego abre en el navegador: http://localhost:8025

Para que inspeccionen el correo capturado en la UI web de MailHog.

3) Probar DNS con dig
En tu Kali, ejecuta por ejemplo:

bash
dig @8.8.8.8 google.com A
dig @1.1.1.1 mendoza.gov.ar NS +short
dig @8.8.8.8 openai.com TXT +short
Muestra la respuesta cruda de los servidores públicos y explica qué es cada registro (A, NS, TXT, MX…).

4) Probar Netcat como cliente y servidor
Cliente TCP

bash
nc google.com 80
GET / HTTP/1.1
Host: google.com

Servidor TCP local Terminal A:

bash
nc -l -p 4444
Terminal B:

bash
echo "¡Hola desde el cliente!" | nc localhost 4444
Chat en vivo Terminal A:

bash
nc -l -p 5000
Terminal B:

bash
nc localhost 5000
UDP simple

bash
echo "Ping UDP" | nc -u 127.0.0.1 9999
Permite demostrar conexión persistente, bidireccional y diferencias TCP vs UDP.

5) Explicación en clase
Para cada demostración:

Muestra el comando completo.

Señala qué bytes/paquetes viajan (“raw request”, headers, payload).

Compara Telnet vs Netcat.

Resalta cuándo el servicio cierra la conexión (HTTP/1.0 vs 1.1, Daytime, SMTP).

6) Limpieza final
Al terminar la sesión de laboratorio:

bash
docker compose down
Borra contenedores, redes y vuelve a tu host limpio.

Con esto ya está todo listo: pruebas de HTTP, TCP de texto, SMTP, DNS y Netcat. ¡Buena clase!

crea un readme en formato markdown en donde expliques todo lo que hicimos paso a paso, su funcionamiento y resumen general
Stack de Demos: Echo HTTP + Daytime + MailHog + Cliente DNS + Netcat
Este repositorio contiene un entorno Docker Compose y ejemplos de cliente para demostrar protocolos de red de texto plano. Con estas demos puedes mostrar en clase cómo funcionan HTTP crudo, un servicio Daytime, SMTP capturado con MailHog, consultas DNS y conexiones TCP/UDP con netcat.

Estructura de carpetas
La organización del proyecto es la siguiente:

Code
stack-demos/
├── docker-compose.yml
└── echo/
    ├── Dockerfile
    └── server.py
docker-compose.yml define los servicios echo, daytime y mailhog.

La carpeta echo/ contiene el servidor HTTP en Python que devuelve la petición completa.

Requisitos
Docker y Docker Compose instalados en la máquina anfitriona.

En Kali Linux (u otro Debian/Ubuntu):

bash
sudo apt-get update
sudo apt-get install telnet netcat-openbsd dnsutils
Levantar el stack
Desde la raíz del proyecto:

bash
docker compose up -d
docker compose ps
Verás tres contenedores en marcha:

echo escuchando en el puerto 8080/tcp

daytime en el puerto 1313/tcp

mailhog en los puertos 1025/tcp (SMTP) y 8025/tcp (UI)

Pruebas paso a paso
1. Echo HTTP
1- Conecta con telnet:

telnet localhost 8080

2- Escribe la petición HTTP cruda:

GET / HTTP/1.1
Host: localhost

3- Asegúrate de dejar una línea en blanco pulsando Enter dos veces.

4- Observa en pantalla la réplica exacta de la primera línea y los headers enviados automáticamente por Telnet.

5- Sal de Telnet con Ctrl+] y luego quit.

Alternativa con netcat:

echo -e "GET / HTTP/1.1\r\nHost: localhost\r\n\r\n" \
  | nc localhost 8080

2. Daytime
1- Con telnet:

telnet localhost 1313

2-  Con netcat:
nc localhost 1313

Cada conexión recibe una línea con la hora local y luego cierra la conexión.

3. MailHog (SMTP)

1- Con telnet:

telnet localhost 1025

2- Envía una conversación SMTP:

EHLO clase.local
MAIL FROM:<profesor@clase.local>
RCPT TO:<alumno@clase.local>
DATA
Mensaje de prueba desde Telnet.
.
QUIT

3- Abre en el navegador:

http://localhost:8025

4- Inspecciona el correo capturado en la interfaz web de MailHog.

Alternativa con netcat:

echo -e "EHLO clase.local\r\nMAIL FROM:<profesor@clase.local>\r\nRCPT TO:<alumno@clase.local>\r\nDATA\r\nCorreo desde nc!\r\n.\r\nQUIT\r\n" \
  | nc localhost 1025


4. Cliente DNS con dig

Ejemplos de consultas DNS:

dig @8.8.8.8 google.com A
dig @1.1.1.1 openai.com AAAA +short
dig @8.8.8.8 gmail.com MX +short
dig @1.1.1.1 mendoza.gov.ar NS +short
dig @8.8.8.8 openai.com TXT +short

Explain cada tipo de registro (A, AAAA, MX, NS, TXT) mostrando la respuesta cruda.

Today
guiame paso a paso explicando la estructura del codigo y realicemos , escribe el codigo del archivo completo en cada caso sin obviar nada y vamos probandolo que funciona bien: # Stack de Demos: Echo HTTP + Daytime + MailHog + Cliente DNS + Netcat — Guía paso a paso Esta guía te permite levantar, probar y **explicar en clase** varios servicios con Docker Compose, además de usar `netcat` como cliente y servidor para experimentar con TCP/UDP: * **Echo HTTP** (ver la petición cruda que envía el cliente) * **Daytime** (servicio simple que devuelve la hora en texto) * **MailHog (SMTP)** (capturar correos de prueba y verlos en una UI web) * **Cliente DNS con `dig`** (consultar registros en servidores públicos) * **Cliente/Servidor TCP con `nc/netcat`** (herramienta versátil de red) Incluye **comandos de cliente** con explicación de cada herramienta. --- ## 0) Requisitos * Docker y Docker Compose instalados. * Clientes sugeridos: * `telnet` → probar **HTTP** y **Daytime** (texto en TCP). * `dig` (paquete `dnsutils` o `bind-tools`) → probar **DNS**. * `nc`/`netcat` → herramienta de red genérica (cliente y servidor). > **¿Qué es cada cliente?** > > * **telnet**: abre una conexión TCP interactiva a un puerto; ideal para ver/probar protocolos en texto. > * **dig**: realiza consultas DNS (registros A/AAAA/MX, etc.) y muestra la respuesta del servidor. > * **nc/netcat**: es la “navaja suiza” de redes: permite conectarse a puertos (cliente), escuchar como servidor TCP/UDP, transferir archivos, depurar tráfico. --- ## 1) Levantar el stack En el archivo `docker-compose.yml` ya están definidos los servicios. Para levantar: ```bash docker compose up -d ``` Para ver el estado: ```bash docker compose ps ``` Para apagar y limpiar: ```bash docker compose down ``` --- ## 2) Echo HTTP — Demostración del protocolo HTTP **Objetivo:** mostrar cómo luce una petición HTTP cruda y qué devuelve el servidor. **URL:** [http://localhost:8080](http://localhost:8080) **Prueba con telnet** ```text telnet localhost 8080 GET / HTTP/1.1 Host: localhost ``` 👉 Dejá **una línea en blanco** al final. **Prueba con netcat (cliente)** ```bash echo -e "GET / HTTP/1.1\r\nHost: localhost\r\n\r\n" | nc localhost 8080 ``` 👉 Hace la misma petición en una sola línea. --- ## 3) Daytime — Hora local por TCP en texto **Puerto:** `1313` **Prueba con telnet** ```text telnet localhost 1313 ``` **Prueba con netcat (cliente)** ```bash nc localhost 1313 ``` 👉 Con cada conexión recibirás la hora actual. --- ## 4) MailHog (SMTP) — Enviar y visualizar correos de prueba * **SMTP:** `localhost:1025` * **Web UI:** [http://localhost:8025](http://localhost:8025) **Prueba SMTP con telnet** ```text telnet localhost 1025 EHLO clase.local MAIL FROM:<profesor@clase.local> RCPT TO:<alumno@clase.local> DATA Hola con telnet! . QUIT ``` **Prueba SMTP con netcat (cliente)** ```bash echo -e "EHLO clase.local\r\nMAIL FROM:<profesor@clase.local>\r\nRCPT TO:<alumno@clase.local>\r\nDATA\r\nHola con nc!\r\n.\r\nQUIT\r\n" | nc localhost 1025 ``` --- ## 5) Cliente DNS — Consultas con `dig` **Ejemplos:** ```bash # IPv4 dig @8.8.8.8 google.com A # IPv6 dig @1.1.1.1 openai.com AAAA +short # MX dig @8.8.8.8 gmail.com MX +short # NS dig @1.1.1.1 mendoza.gov.ar NS +short # TXT dig @8.8.8.8 openai.com TXT +short ``` --- ## 6) Netcat (nc) — Cliente y Servidor `nc` no solo sirve como cliente. También puede actuar como servidor TCP o UDP. ### Cliente TCP simple ```bash nc google.com 80 ``` 👉 Abre una conexión TCP al puerto 80 de `google.com`. Podés escribir manualmente un `GET /`. ### Servidor TCP local ```bash nc -l -p 4444 ``` 👉 Abre un servidor en el puerto 4444. Cualquier cliente que se conecte podrá enviar/recibir datos. Ejemplo: en otra terminal: ```bash echo "Hola desde cliente" | nc localhost 4444 ``` ### Cliente UDP ```bash echo "Ping UDP" | nc -u 127.0.0.1 9999 ``` 👉 Envía un paquete UDP al puerto 9999. ### Chat sencillo con nc En una terminal (servidor): ```bash nc -l -p 5000 ``` En otra (cliente): ```bash nc localhost 5000 ``` 👉 Ahora lo que escribas en un lado aparecerá en el otro. --- ## 7) Tips y resolución de problemas * **Puertos ocupados**: cambiá los mapeos en el compose. * **`telnet`/`nc` no conectan**: verificá firewall y que el contenedor esté levantado. * **Zona horaria en Daytime**: ajustá `TZ` en el compose. * **DNS público no responde**: probá con otro (`8.8.8.8`, `1.1.1.1`). --- ## 8) Limpieza ```bash docker compose down ``` --- ### Fin Con este stack podés mostrar **HTTP, un TCP de texto simple, SMTP**, usar `dig` contra servidores DNS reales y experimentar con `nc/netcat` tanto como **cliente** como **servidor**. Esto ofrece ejemplos prácticos y flexibles para enseñar protocolos y redes.
Stack de Demos: Echo HTTP + Daytime + MailHog + Cliente DNS + Netcat — Guía paso a paso
A continuación armamos un proyecto Docker Compose que levanta:

Un servidor HTTP que muestra el request crudo

Un servicio Daytime sencillo (hora en texto)

MailHog para capturar y ver correos SMTP

Desde tu host usaremos dig y nc para DNS y pruebas TCP/UDP

Cada archivo lo tendrás completo para copiar/pegar. Probamos en cada paso antes de seguir.

Estructura del proyecto
Crea una carpeta stack-demos/ y dentro:

Code
stack-demos/
├── docker-compose.yml
└── echo/
    ├── Dockerfile
    └── server.py
1) Definir docker-compose.yml
Este archivo pone en marcha los tres servicios:

yaml
version: "3.8"

services:
  echo:
    build:
      context: ./echo
    ports:
      - "8080:8080"
    restart: unless-stopped

  daytime:
    image: alpine:3.15
    command: >
      sh -c "while true; do date | nc -l -p 1313; done"
    ports:
      - "1313:1313/tcp"
    restart: unless-stopped

  mailhog:
    image: mailhog/mailhog:latest
    ports:
      - "1025:1025"  # SMTP
      - "8025:8025"  # Web UI
    restart: unless-stopped
Explicación rápida:

echo: compilamos un pequeño servidor Python que escucha en el puerto 8080 y devuelve la petición plena.

daytime: contenedor Alpine que en bucle atiende conexiones TCP en el puerto 1313 y responde con date.

mailhog: imagen oficial para capturar SMTP en localhost:1025 y ver correos en http://localhost:8025.

Guarda este contenido en stack-demos/docker-compose.yml.

2) Echo HTTP — servidor en Python
Creamos un simple HTTP server que vuelca la línea de petición y headers.

echo/Dockerfile
dockerfile
FROM python:3.9-alpine
WORKDIR /app
COPY server.py .
EXPOSE 8080
CMD ["python", "server.py"]
echo/server.py
python
import socket
from http.server import BaseHTTPRequestHandler, HTTPServer

class EchoHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()

        # Escribimos la primera línea de solicitud
        self.wfile.write(self.raw_requestline)

        # Escribimos cada header recibido
        for name, value in self.headers.items():
            line = f"{name}: {value}\n".encode('utf-8')
            self.wfile.write(line)

        # Línea en blanco final
        self.wfile.write(b"\n")

def run():
    server = HTTPServer(('0.0.0.0', 8080), EchoHandler)
    print("Echo HTTP server en 0.0.0.0:8080")
    server.serve_forever()

if __name__ == '__main__':
    run()
Con esto, cada petición GET / HTTP/1.1 devuelve exactamente lo que enviaste (raw request).

3) Levantar el stack y probar Echo HTTP
Desde la raíz stack-demos/ ejecuta:

bash
docker compose up -d
docker compose ps
Verás tres contenedores en marcha: echo, daytime, mailhog.

Probar con telnet
bash
telnet localhost 8080
GET / HTTP/1.1
Host: localhost

Deja una línea en blanco y pulsa Enter. En la consola telnet verás la réplica exacta de tu request.

Probar con netcat
bash
echo -e "GET / HTTP/1.1\r\nHost: localhost\r\n\r\n" | nc localhost 8080
4) Daytime — hora en texto
Este servicio escucha en el puerto 1313 y al conectar envía la hora.

Probar con telnet
bash
telnet localhost 1313
Se desconecta automáticamente tras enviar la hora.

Probar con netcat
bash
nc localhost 1313
5) MailHog (SMTP)
Captura correo en texto plano y ofrece una UI web.

SMTP en localhost:1025

UI en http://localhost:8025

Prueba SMTP con telnet
bash
telnet localhost 1025
EHLO clase.local
MAIL FROM:<profesor@clase.local>
RCPT TO:<alumno@clase.local>
DATA
Hola con telnet!
.
QUIT
Prueba SMTP con netcat
bash
echo -e "EHLO clase.local\r\nMAIL FROM:<profesor@clase.local>\r\nRCPT TO:<alumno@clase.local>\r\nDATA\r\nHola con nc!\r\n.\r\nQUIT\r\n" \
  | nc localhost 1025
Luego abre tu navegador en http://localhost:8025 para ver el mensaje.

6) Cliente DNS con dig
Desde tu host o contenedor:

bash
# IPv4
dig @8.8.8.8 google.com A

# IPv6 (solo muestra la IP)
dig @1.1.1.1 openai.com AAAA +short

# Registros MX
dig @8.8.8.8 gmail.com MX +short

# NS
dig @1.1.1.1 mendoza.gov.ar NS +short

# TXT
dig @8.8.8.8 openai.com TXT +short
7) Netcat (nc) — Cliente y servidor genérico
Cliente TCP

bash
nc google.com 80
# luego escribe manualmente:
GET / HTTP/1.1
Host: google.com

Servidor TCP local

bash
nc -l -p 4444
En otra terminal:

bash
echo "Hola desde cliente" | nc localhost 4444
Cliente UDP

bash
echo "Ping UDP" | nc -u 127.0.0.1 9999
Chat simple

bash
# Terminal A (servidor)
nc -l -p 5000

# Terminal B (cliente)
nc localhost 5000
8) Limpieza
Para detener y borrar contenedores, redes y volúmenes anónimos:

bash
docker compose down
Con esto tienes un stack completo para mostrar y explicar HTTP crudo, un servicio TCP de texto, SMTP con captura visual, consultas DNS y experimentos con netcat como cliente/servidor. ¡A probar en clase!

para que sirve todo esto? como pruebo en telnet y netcat como lo descargo en kali linux en terminal me aparece lo siguiente: ~/ComputacionII/Clases/Clase_14/stack-demos] └─$ docker compose up -d docker compose ps WARN[0002] /home/cuervo/ComputacionII/Clases/Clase_14/stack-demos/docker-compose.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion [+] Running 10/10 ✔ mailhog Pulled 101.5s ✔ df20fa9351a1 Pull complete 3.2s ✔ ed8968b2872e Pull complete 3.6s ✔ a92cc7c5fd73 Pull complete 3.9s ✔ f17c8f1adafb Pull complete 86.4s ✔ 03954754c53a Pull complete 87.0s ✔ 60493946972a Pull complete 89.9s ✔ 368ee3bc1dbb Pull complete 91.8s ✔ daytime Pulled 19.5s ✔ d078792c4f91 Pull complete 9.0s Compose can now delegate builds to bake for better performance. To do so, set COMPOSE_BAKE=true. [+] Building 31.0s (9/9) FINISHED docker:default => [echo internal] load build definition from Dockerfile 1.1s => => transferring dockerfile: 130B 0.2s => [echo internal] load metadata for docker.io/library/python:3. 4.1s => [echo internal] load .dockerignore 0.4s => => transferring context: 2B 0.0s => [echo 1/3] FROM docker.io/library/python:3.9-alpine@sha256:3 16.2s => => resolve docker.io/library/python:3.9-alpine@sha256:372f3cf 0.9s => => sha256:372f3cfc1738ed91b64c7d36a7a02d5c3 10.29kB / 10.29kB 0.0s => => sha256:561fbf2d229226799584cfa783ad6761553 1.73kB / 1.73kB 0.0s => => sha256:8cccaac7ca7e4e129589c008f43fc3e4991 5.08kB / 5.08kB 0.0s => => sha256:9824c27679d3b27c5e1cb00a73adb6f4f8d 3.80MB / 3.80MB 6.7s => => sha256:d325733a625202bb5fe7304c973b984f 14.88MB / 14.88MB 11.6s => => sha256:696282ba7530403087147a86e1fd4c2 447.74kB / 447.74kB 4.9s => => sha256:e9a57d92e270674b2a656977030520f3b8e3047 248B / 248B 6.2s => => extracting sha256:9824c27679d3b27c5e1cb00a73adb6f4f8d55699 0.2s => => extracting sha256:696282ba7530403087147a86e1fd4c2b83d3507f 0.4s => => extracting sha256:d325733a625202bb5fe7304c973b984f63bebdb8 1.2s => => extracting sha256:e9a57d92e270674b2a656977030520f3b8e30471 0.0s => [echo internal] load build context 1.1s => => transferring context: 834B 0.1s => [echo 2/3] WORKDIR /app 3.5s => [echo 3/3] COPY server.py . 1.4s => [echo] exporting to image 1.1s => => exporting layers 0.7s => => writing image sha256:2fcdca4583c0f38716a4143314f5842f05e71 0.0s => => naming to docker.io/library/stack-demos-echo 0.1s => [echo] resolving provenance for metadata file 0.2s [+] Running 5/5 ✔ echo Built 0.0s ✔ Network stack-demos_default Created 3.5s ✔ Container stack-demos-daytime-1 Started 11.8s ✔ Container stack-demos-mailhog-1 Started 11.7s ✔ Container stack-demos-echo-1 Started 11.7s WARN[0000] /home/cuervo/ComputacionII/Clases/Clase_14/stack-demos/docker-compose.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion NAME IMAGE COMMAND SERVICE CREATED STATUS PORTS stack-demos-daytime-1 alpine:3.15 "sh -c 'while true; …" daytime 11 seconds ago Up 5 seconds 0.0.0.0:1313->1313/tcp, [::]:1313->1313/tcp stack-demos-echo-1 stack-demos-echo "python server.py" echo 11 seconds ago Up 5 seconds 0.0.0.0:8080->8080/tcp, [::]:8080->8080/tcp stack-demos-mailhog-1 mailhog/mailhog:latest "MailHog" mailhog 11 seconds ago Up 5 seconds 0.0.0.0:1025->1025/tcp, [::]:1025->1025/tcp, 0.0.0.0:8025->8025/tcp, [::]:8025->8025/tcp
¿Para qué sirve todo esto?
Este stack te permite mostrar en vivo y explicar varios protocolos de red y servicios básicos:

HTTP crudo: ves exactamente qué bytes envía el cliente y qué recibe.

Daytime: un servidor TCP que devuelve la hora en texto plano.

SMTP con MailHog: capturas emails de prueba y los inspeccionas vía web.

DNS con dig: consultas contra servidores públicos y ves sus respuestas.

Netcat (nc): practicas conexiones TCP/UDP y montas tu propio servidor/cliente para experimentar.

Con estas demos tus alumnos comprenden la mecánica de protocolos de texto y aprenden a depurar tráfico de red con herramientas estándar.

Instalación de telnet, netcat y dig en Kali Linux
Actualiza la lista de paquetes:

bash
sudo apt update
Instala telnet, netcat y las utilidades DNS:

bash
sudo apt install telnet netcat-openbsd dnsutils
telnet: cliente TCP interactivo.

netcat-openbsd (nc): cliente/servidor TCP y UDP.

dnsutils (dig): consultas DNS.

Pruebas con telnet
Echo HTTP (puerto 8080)

bash
telnet localhost 8080
Luego escribe:

text
GET / HTTP/1.1
Host: localhost

Deja una línea en blanco y verás el “echo” de tu petición.

Daytime (puerto 1313)

bash
telnet localhost 1313
Se desconecta tras enviar la hora en texto.

SMTP con MailHog (puerto 1025)

bash
telnet localhost 1025
Envía comandos SMTP:

text
EHLO clase.local
MAIL FROM:<profesor@clase.local>
RCPT TO:<alumno@clase.local>
DATA
Hola desde telnet!
.
QUIT
Luego abre http://localhost:8025 para ver el correo capturado.

Pruebas con netcat (nc)
Echo HTTP

bash
echo -e "GET / HTTP/1.1\r\nHost: localhost\r\n\r\n" \
  | nc localhost 8080
Daytime

bash
nc localhost 1313
SMTP con MailHog

bash
echo -e "EHLO clase.local\r\nMAIL FROM:<profesor@clase.local>\r\nRCPT TO:<alumno@clase.local>\r\nDATA\r\nHola desde nc!\r\n.\r\nQUIT\r\n" \
  | nc localhost 1025
Cliente DNS con dig

bash
dig @8.8.8.8 google.com A
dig @1.1.1.1 mendoza.gov.ar NS +short
Chat o servidor TCP local

En terminal A (servidor):

bash
nc -l -p 5000
En terminal B (cliente):

bash
nc localhost 5000
UDP simple

bash
echo "Ping UDP" | nc -u 127.0.0.1 9999
Con esto ya tienes instaladas las herramientas en Kali, conoces el propósito de cada servicio y sabes cómo probarlos tanto con telnet como con netcat. ¡A darle play y experimentar!

osea puedo ver todo lo que se manda en mi red? otros dispositivos por ejemplo
¿Puedo ver todo lo que se manda en mi red?
No. Telnet y Netcat solo muestran la conversación entre tu máquina y el servicio al que te conectas. Para “ver” tráfico de otros dispositivos necesitas un sniffer de red y algunas condiciones especiales.

1) Limitaciones de telnet y netcat
Ambos actúan como cliente o servidor en puertos concretos.

Solo muestran datos que tu sesión envía o recibe directamente.

No capturan paquetes que van entre otros hosts o servicios.

2) Herramientas de sniffing: tcpdump y Wireshark
Para inspeccionar todo el tráfico de tu interfaz de red emplea:

tcpdump (CLI, muy ligero)

Wireshark (GUI, análisis en profundidad)

Instalación en Kali
bash
sudo apt update
sudo apt install tcpdump wireshark
Modo promiscuo y topología de red
Debes habilitar modo promiscuo en tu interfaz para capturar tramas que no van dirigidas a tu MAC.

En un switch normal solo verás:

Broadcasts (ARP, DHCP, etc.)

Tráfico unicast si está configurado un SPAN/mirror port o haces ARP spoofing.

En un hub o una red Wi-Fi en modo monitor verás prácticamente todo.

Ejemplo básico con tcpdump
bash
sudo tcpdump -i eth0 -nn -vv
-i eth0 → interfaz a escuchar

-nn → no traduce IP ni puertos a nombres

-vv → salida más detallada

Para filtrar solo HTTP (puerto 80):

bash
sudo tcpdump -i eth0 tcp port 80 -A
3) Captura en Docker
Si tus servicios corren dentro de Docker, puedes:

Identificar la interfaz del contenedor:

bash
docker exec -it stack-demos-echo-1 ip addr
Escuchar dentro del contenedor:

bash
docker exec -it stack-demos-echo-1 tcpdump -i eth0 -nn
O, desde el host, habilitar promiscuo en el bridge de Docker (docker0).

4) Ética y legalidad
Solo captures tráfico en redes que administres o donde tengas autorización.

Sniffear redes ajenas sin permiso es ilegal y puede acarrear sanciones.

5) Más allá del sniffing
Con ARP spoofing (herramientas: arpspoof, ettercap) puedes redirigir tráfico unicast a tu NIC, pero ten cuidado: interrumpe la red si no se hace bien.

En entornos profesionales se usa Port Mirroring en switches gestionables o TAPs de red.

Con estas pautas ya sabes por qué telnet/nc no “ven” todo y cómo emplear tcpdump o Wireshark para capturar y analizar cualquier paquete en tu red, siempre con permiso y responsabilidad.

sudo apt install telnet Installing: telnet Summary: Upgrading: 0, Installing: 1, Removing: 0, Not Upgrading: 207 Download size: 43.2 kB Space needed: 56.3 kB / 15.5 GB available Err:1 http://http.kali.org/kali kali-rolling/main amd64 telnet all 0.17+2.6-1 404 Not Found [IP: 54.39.128.230 80] Error: Failed to fetch http://http.kali.org/kali/pool/main/i/inetutils/telnet_0.17%2b2.6-1_all.deb 404 Not Found [IP: 54.39.128.230 80] Error: Unable to fetch some archives, maybe run apt-get update or try with --fix-missing?
Solución al 404 al instalar telnet en Kali Linux
El error 404 indica que APT no está encontrando el paquete en el repositorio configurado. Sigue estos pasos:

1. Actualiza la lista de paquetes
Siempre que veas un “404 Not Found” tras un install, primero refresca los índices:

bash
sudo apt-get update
Si este paso falla con errores 404, pasa al punto 2.

2. Verifica y corrige /etc/apt/sources.list
Abre tu archivo de repositorios:

bash
sudo nano /etc/apt/sources.list
Asegúrate de tener solo la línea oficial de Kali Rolling. Por ejemplo:

Code
deb http://http.kali.org/kali kali-rolling main contrib non-free
Elimina o comenta cualquier otra línea (PPAs, mirrors viejos, etc.). Guarda y cierra.

3. Vuelve a actualizar e instala telnet
bash
sudo apt-get update
sudo apt-get install telnet
Si ahora todo va bien, ¡listo!

4. Cambia de mirror si sigue fallando
A veces el CDN de http.kali.org tiene replicación parcial. Prueba con otro mirror de la lista oficial:

Elige uno de https://http.kali.org/README.mirrorlist

Reemplaza en sources.list:

Code
deb http://archive-4.kali.org/kali kali-rolling main contrib non-free
Repite:

bash
sudo apt-get update
sudo apt-get install telnet
Con esto evitas errores 404 debidos a problemas puntuales en el espejo elegido.

5. Instala también netcat y dig
Una vez solucionado el repositorio, instala las herramientas de red:

bash
sudo apt-get install netcat-openbsd dnsutils
Ahora podrás usar telnet, nc y dig sin problemas.





Edit in a page
└─$ telnet localhost 8080 GET / HTTP/1.1 Host: localhost Trying ::1... Connected to localhost. Escape character is '^]'. no me aparece nada
¿Puedo ver todo el tráfico de mi red?
Telnet y Netcat solo muestran la conversación que tú inicias con un servicio concreto. Para “esnifar” todo lo que pasa en tu red necesitas herramientas y ciertas condiciones de la infraestructura.

1) Topología y modo promiscuo
En un hub Ethernet o en Wi-Fi en modo monitor, tu tarjeta ve todos los paquetes.

En un switch estándar, solo recibirás:

Tráfico de broadcast (ARP, DHCP…)

Tráfico dirigido a tu MAC

Para capturar tráfico unicast de otros hosts en un switch necesitas:

Port mirroring/SPAN en un switch gestionable

O bien un network TAP (hardware)

O un ataque de ARP spoofing / gratuitous ARP (por ejemplo con arpspoof)

2) Herramientas de sniffing
tcpdump (CLI)

bash
sudo tcpdump -i eth0 -nn -vv
-i eth0 → interfaz a escuchar

-nn → no resuelve nombres

-vv → más detalle

Wireshark (GUI)

Captura en modo promiscuo

Filtra por protocolo (http, smtp, dns…)

Herramientas de ARP spoofing

arpspoof -i eth0 -t VÍCTIMA GATEWAY

ettercap para interfaces más amigables

3) Ejemplo de captura HTTP
En un entorno de prueba (hub o con port-mirror):

bash
sudo ip link set eth0 promisc on
sudo tcpdump -i eth0 tcp port 80 -A
Cada vez que alguien cargue una página HTTP verás peticiones GET y respuestas crudas.

4) Limitaciones prácticas
HTTPS cifra todo, no podrás leer contenido sin romper TLS.

Ética y legalidad: solo captures tráfico en redes que administras o donde tengas permiso explícito.

En redes corporativas se usa SPAN ports en switches Cisco, HP, Juniper…

Con estas pautas ya entiendes que para ver “todo lo que se manda en la red” no basta Telnet/Netcat: necesitas un sniffer (tcpdump/Wireshark) y una topología o técnica (promiscuo, port-mirror, ARP spoofing) que te permita recibir los paquetes de otros dispositivos.

pero centrate en el ejercicio que hicimos al probarlo en telnet que me tendria que aparecer hice lo del docker : [~/ComputacionII/Clases/Clase_14/stack-demos] └─$ docker compose up -d docker compose ps WARN[0000] /home/cuervo/ComputacionII/Clases/Clase_14/stack-demos/docker-compose.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion [+] Running 4/4 ✔ Network stack-demos_default Created 0.2s ✔ Container stack-demos-daytime-1 Started 4.9s ✔ Container stack-demos-mailhog-1 Started 4.6s ✔ Container stack-demos-echo-1 Started 4.2s WARN[0000] /home/cuervo/ComputacionII/Clases/Clase_14/stack-demos/docker-compose.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion NAME IMAGE COMMAND SERVICE CREATED STATUS PORTS stack-demos-daytime-1 alpine:3.15 "sh -c 'while true; …" daytime 5 seconds ago Up 1 second 0.0.0.0:1313->1313/tcp, [::]:1313->1313/tcp stack-demos-echo-1 stack-demos-echo "python server.py" echo 5 seconds ago Up 2 seconds 0.0.0.0:8080->8080/tcp, [::]:8080->8080/tcp stack-demos-mailhog-1 mailhog/mailhog:latest "MailHog" mailhog 5 seconds ago Up 2 seconds 0.0.0.0:1025->1025/tcp, [::]:1025->1025/tcp, 0.0.0.0:8025->8025/tcp, [::]:8025->8025/tcp ┌──(cuervo㉿kali)-[~/ComputacionII/Clases/Clase_14/stack-demos] └─$ telnet localhost 8080 GET / HTTP/1.1 Host: localhost Trying ::1... Connected to localhost. Escape character is '^]'.
Aquí tu ejercicio paso a paso con Telnet, paso a paso, para que veas exactamente qué debe suceder y qué deberías ver en pantalla.

1. Conexión con Telnet
Abres la sesión:

bash
telnet localhost 8080
Verás esto al conectar:

Code
Trying ::1...
Connected to localhost.
Escape character is '^]'.
Hasta aquí todo bien: estás dentro de la conexión TCP.

Envía la petición HTTP cruda a. Escribe

Code
GET / HTTP/1.1
Host: localhost
y pulsa Enter al final de la línea de Host. b. AHORA pulsa Enter de nuevo (dejas una línea en blanco).

Solo tras esa segunda pulsación de Enter tu servidor Python reconocerá el fin de encabezados y enviará la respuesta.

¿Qué deberías ver? Poco después de ese doble Enter, Telnet debe mostrarte la réplica exacta de lo que enviaste. Algo así:

Code
GET / HTTP/1.1
Host: localhost
User-Agent: telnet/0.17 (or whatever)
Accept-Encoding: identity
Connection: keep-alive

– La primera línea es tu GET original. – Aparecerán además los headers que Telnet añade automáticamente (User-Agent, Connection…). – Luego se queda esperando (HTTP/1.1 por defecto mantiene la conexión).

Sal de Telnet: Pulsa Ctrl+] para entrar en el prompt de Telnet y escribe quit.

2. Prueba rápida con Netcat
Si Telnet te sigue sin mostrar nada (quizá el doble Enter no se registró), usa Netcat:

bash
echo -e "GET / HTTP/1.1\r\nHost: localhost\r\n\r\n" | nc localhost 8080
Eso te debe imprimir inmediatamente en tu terminal:

Code
GET / HTTP/1.1
Host: localhost
User-Agent: curl/7.x.x
Accept: */*
Connection: keep-alive

(La parte de User-Agent/Accept la añade Netcat o tu entorno.)

3. Qué revisar si sigue sin respuesta
Asegúrate de que efectivamente el servicio echo está arriba:

bash
docker compose ps | grep echo
Mira sus logs para confirmar que recibe peticiones:

bash
docker compose logs echo --tail=20
Deberías ver un mensaje por cada conexión.

Prueba con HTTP/1.0, así el servidor cierra la conexión al responder:

bash
telnet localhost 8080
GET / HTTP/1.0
Host: localhost

Al recibir la respuesta Telnet te desconectará solo.

Con este flujo—conexión, doble Enter para cerrar headers, y observación de la réplica—deberías ver en Telnet lo que envías y comprobar que tu servidor “echo” funciona correctamente.

y que mas tengo que hacer o eso seria todo?
Resumen de pasos completados
Has levantado y probado correctamente el servicio Echo HTTP con Telnet y Netcat. La configuración en Docker Compose ya está lista, así que a partir de aquí solo queda:

Probar los demás servicios

Explicar en clase

Limpiar el entorno

1) Probar Daytime
En otra terminal ejecuta:

bash
telnet localhost 1313
o bien:

bash
nc localhost 1313
Cada conexión recibe una línea con la hora y se cierra sola. Muestra en pantalla esa hora para que vean el protocolo TCP de texto.

2) Probar MailHog (SMTP)
Con Telnet:

bash
telnet localhost 1025
Envía:

text
EHLO clase.local
MAIL FROM:<profesor@clase.local>
RCPT TO:<alumno@clase.local>
DATA
Mensaje de prueba desde Telnet.
.
QUIT
Luego abre en el navegador: http://localhost:8025

Para que inspeccionen el correo capturado en la UI web de MailHog.

3) Probar DNS con dig
En tu Kali, ejecuta por ejemplo:

bash
dig @8.8.8.8 google.com A
dig @1.1.1.1 mendoza.gov.ar NS +short
dig @8.8.8.8 openai.com TXT +short
Muestra la respuesta cruda de los servidores públicos y explica qué es cada registro (A, NS, TXT, MX…).

4) Probar Netcat como cliente y servidor
Cliente TCP

bash
nc google.com 80
GET / HTTP/1.1
Host: google.com

Servidor TCP local Terminal A:

bash
nc -l -p 4444
Terminal B:

bash
echo "¡Hola desde el cliente!" | nc localhost 4444
Chat en vivo Terminal A:

bash
nc -l -p 5000
Terminal B:

bash
nc localhost 5000
UDP simple

bash
echo "Ping UDP" | nc -u 127.0.0.1 9999
Permite demostrar conexión persistente, bidireccional y diferencias TCP vs UDP.

5) Explicación en clase
Para cada demostración:

Muestra el comando completo.

Señala qué bytes/paquetes viajan (“raw request”, headers, payload).

Compara Telnet vs Netcat.

Resalta cuándo el servicio cierra la conexión (HTTP/1.0 vs 1.1, Daytime, SMTP).

6) Limpieza final
Al terminar la sesión de laboratorio:

bash
docker compose down
Borra contenedores, redes y vuelve a tu host limpio.

Con esto ya está todo listo: pruebas de HTTP, TCP de texto, SMTP, DNS y Netcat. ¡Buena clase!

crea un readme en formato markdown en donde expliques todo lo que hicimos paso a paso, su funcionamiento y resumen general
Stack de Demos: Echo HTTP + Daytime + MailHog + Cliente DNS + Netcat
Este repositorio contiene un entorno Docker Compose y ejemplos de cliente para demostrar protocolos de red de texto plano. Con estas demos puedes mostrar en clase cómo funcionan HTTP crudo, un servicio Daytime, SMTP capturado con MailHog, consultas DNS y conexiones TCP/UDP con netcat.

Estructura de carpetas
La organización del proyecto es la siguiente:

Code
stack-demos/
├── docker-compose.yml
└── echo/
    ├── Dockerfile
    └── server.py
docker-compose.yml define los servicios echo, daytime y mailhog.

La carpeta echo/ contiene el servidor HTTP en Python que devuelve la petición completa.

Requisitos
Docker y Docker Compose instalados en la máquina anfitriona.

En Kali Linux (u otro Debian/Ubuntu):

bash
sudo apt-get update
sudo apt-get install telnet netcat-openbsd dnsutils
Levantar el stack
Desde la raíz del proyecto:

bash
docker compose up -d
docker compose ps
Verás tres contenedores en marcha:

echo escuchando en el puerto 8080/tcp

daytime en el puerto 1313/tcp

mailhog en los puertos 1025/tcp (SMTP) y 8025/tcp (UI)

Pruebas paso a paso
1. Echo HTTP
Conecta con telnet:

bash
telnet localhost 8080
Escribe la petición HTTP cruda:

Code
GET / HTTP/1.1
Host: localhost

Asegúrate de dejar una línea en blanco pulsando Enter dos veces.

Observa en pantalla la réplica exacta de la primera línea y los headers enviados automáticamente por Telnet.

Sal de Telnet con Ctrl+] y luego quit.

Alternativa con netcat:

bash
echo -e "GET / HTTP/1.1\r\nHost: localhost\r\n\r\n" \
  | nc localhost 8080
2. Daytime
Con telnet:

bash
telnet localhost 1313
Con netcat:

bash
nc localhost 1313
Cada conexión recibe una línea con la hora local y luego cierra la conexión.

3. MailHog (SMTP)
Con telnet:

bash
telnet localhost 1025
Envía una conversación SMTP:

Code
EHLO clase.local
MAIL FROM:<profesor@clase.local>
RCPT TO:<alumno@clase.local>
DATA
Mensaje de prueba desde Telnet.
.
QUIT
Abre en el navegador:

Code
http://localhost:8025
Inspecciona el correo capturado en la interfaz web de MailHog.

Alternativa con netcat:

echo -e "EHLO clase.local\r\nMAIL FROM:<profesor@clase.local>\r\nRCPT TO:<alumno@clase.local>\r\nDATA\r\nCorreo desde nc!\r\n.\r\nQUIT\r\n" \
  | nc localhost 1025

4. Cliente DNS con dig
Ejemplos de consultas DNS:

bash
dig @8.8.8.8 google.com A
dig @1.1.1.1 openai.com AAAA +short
dig @8.8.8.8 gmail.com MX +short
dig @1.1.1.1 mendoza.gov.ar NS +short
dig @8.8.8.8 openai.com TXT +short
Explain cada tipo de registro (A, AAAA, MX, NS, TXT) mostrando la respuesta cruda.

5. Netcat (nc) como cliente y servidor

Cliente TCP:

nc google.com 80
GET / HTTP/1.1
Host: google.com

Servidor TCP local: 
Terminal A:

nc -l -p 4444

Terminal B:
echo "Hola desde cliente" | nc localhost 4444

Chat simple: 
Terminal A:

nc -l -p 5000

Terminal B:
nc localhost 5000

Cliente UDP:
echo "Ping UDP" | nc -u 127.0.0.1 9999

Estas demostraciones ilustran conexiones bidireccionales, persistentes y la diferencia entre TCP y UDP.


Limpieza
Cuando termines la sesión de laboratorio, detén y borra todo:

docker compose down
Esto elimina contenedores, redes y volúmenes anónimos creados.

## Resumen general
Con este proyecto has visto:

Cómo montar un servidor HTTP minimalista que refleja peticiones crudas.

Un servicio Daytime simple que responde con la hora vía TCP.

Uso de MailHog para capturar y visualizar SMTP en una UI web.

Consultas DNS con dig y explicación de distintos registros.

Uso de netcat como cliente y servidor TCP/UDP para experimentar con protocolos de texto plano.

Estas prácticas permiten a los alumnos comprender en detalle el flujo de bytes en protocolos de red y dominar herramientas de diagnóstico como telnet, netcat, dig y herramientas de sniffing como tcpdump o Wireshark fuera de este entorno.