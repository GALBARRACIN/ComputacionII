# verificar_cadena.py
import json
import hashlib

def calcular_hash_bloque(bloque):
    contenido = {
        "timestamp": bloque["timestamp"],
        "datos": bloque["datos"],
        "alerta": bloque["alerta"],
        "prev_hash": bloque["prev_hash"]
    }
    return hashlib.sha256(
        json.dumps(contenido, sort_keys=True).encode()
    ).hexdigest()


def verificar_integridad(ruta):
    with open(ruta, "r") as f:
        cadena = json.load(f)

    bloques_corruptos = []
    alertas = 0
    suma_frecuencia = 0
    suma_presion = 0
    suma_oxigeno = 0

    for i, bloque in enumerate(cadena):
        hash_calculado = calcular_hash_bloque(bloque)
        if bloque["hash"] != hash_calculado:
            bloques_corruptos.append(i + 1)

        if bloque["alerta"]:
            alertas += 1

        suma_frecuencia += bloque["datos"]["frecuencia"]["media"]
        suma_presion += bloque["datos"]["presion"]["media"]
        suma_oxigeno += bloque["datos"]["oxigeno"]["media"]

        if i > 0:
            prev = cadena[i - 1]["hash"]
            if bloque["prev_hash"] != prev:
                bloques_corruptos.append(i + 1)

    total = len(cadena)
    promedio_frec = suma_frecuencia / total
    promedio_pres = suma_presion / total
    promedio_oxi = suma_oxigeno / total

    # Guardar reporte
    with open("verificacion/reporte.txt", "w") as r:
        r.write(f"Total de bloques: {total}\n")
        r.write(f"Bloques con alerta: {alertas}\n")
        r.write(f"Bloques corruptos: {len(set(bloques_corruptos))}\n")
        r.write(f"Promedio frecuencia: {promedio_frec:.2f}\n")
        r.write(f"Promedio presion: {promedio_pres:.2f}\n")
        r.write(f"Promedio oxigeno: {promedio_oxi:.2f}\n")

    print("🔍 Verificación completada.")
    if bloques_corruptos:
        print(f"❌ Bloques corruptos: {sorted(set(bloques_corruptos))}")
    else:
        print("✅ Cadena íntegra. Todos los hashes son válidos.")


if __name__ == "__main__":
    verificar_integridad("blockchain/blockchain.json")
