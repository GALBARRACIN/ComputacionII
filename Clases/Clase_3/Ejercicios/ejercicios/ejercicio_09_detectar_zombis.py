import os

def ejecutar():
    # Recorre todos los directorios de procesos en /proc
    for pid in os.listdir('/proc'):
        if pid.isdigit():  # Asegura que es un PID válido
            try:
                with open(f"/proc/{pid}/status") as f:
                    lines = f.readlines()
                    estado = next((l for l in lines if l.startswith("State:")), "")
                    if "Z" in estado:  # Zombi encontrado
                        nombre = next((l for l in lines if l.startswith("Name:")), "").split()[1]
                        ppid = next((l for l in lines if l.startswith("PPid:")), "").split()[1]
                        print(f"Zombi detectado → PID: {pid}, PPID: {ppid}, Nombre: {nombre}")
            except IOError:
                continue  # Ignora procesos inaccesibles (ya terminaron o no tenés permisos)
