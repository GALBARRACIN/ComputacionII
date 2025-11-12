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
