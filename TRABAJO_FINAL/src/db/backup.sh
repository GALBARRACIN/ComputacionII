#!/bin/bash

# ==============================================================================
# Script de Políticas de Resguardo (Backup Lógico)
# Materia: Diseño de Bases de Datos II
# Objetivo: Automatizar el respaldo de MongoDB aislando el entorno Docker.
# ==============================================================================

# NOTA ARQUITECTURA: Al usar una arquitectura orquestada con Docker, no es 
# necesario (ni recomendado) instalar las tools de Mongo en Debian. 
# La mejor práctica es ejecutar el comando DENTRO del contenedor que ya 
# tiene los binarios nativos, y redirigir la salida a nuestro disco físico.

# 1. Variables de entorno (Evita hardcodear y permite reutilizar el script)
CONTENEDOR="c2_tactico_mongo"
BASE_DE_DATOS="c2_tactico_db"

# 2. Generación del Timestamp
# Usamos el comando 'date' de POSIX. 
# Formato: Año-Mes-Día_Hora-Minuto-Segundo (Ej: 2026-10-07_09-40-12)
# Esto garantiza que ningún backup sobrescriba a uno anterior.
FECHA=$(date +"%Y-%m-%d_%H-%M-%S")
CARPETA_DESTINO="./backups"

# 3. Preparación del directorio
# El flag '-p' (parents) es crucial: crea la carpeta si no existe, 
# pero si ya existe, no arroja error ni corta la ejecución del script.
mkdir -p $CARPETA_DESTINO

# 4. Ruta absoluta/relativa del archivo destino
ARCHIVO_SALIDA="$CARPETA_DESTINO/backup_$FECHA.gz"

echo "[INFO] Iniciando resguardo lógico de la base de datos '$BASE_DE_DATOS'..."

# ==========================================================================
# 5. EJECUCIÓN DEL MONGODUMP
# ==========================================================================
# Desglose del comando para repasar:
# - 'docker exec': Inyecta y ejecuta un comando en un contenedor corriendo.
# - 'mongodump': Utilidad oficial de MongoDB para volcar datos a BSON.
# - '--db $BASE_DE_DATOS': Aísla el dump. Ignora bases de sistema (admin/config).
# - '--archive': Escribe todo en un flujo estándar (stdout) en vez de crear carpetas.
#   Esto empaqueta también la configuración de los índices (como el 2dsphere).
# - '--gzip': Comprime el flujo al vuelo. Consume un poco de CPU extra pero 
#   reduce drásticamente el I/O y el peso en el disco SSD.
# - '> $ARCHIVO_SALIDA': Operador de redirección de Linux. Toma el flujo que 
#   escupió el contenedor y lo escribe en el archivo .gz local.
docker exec $CONTENEDOR mongodump --db $BASE_DE_DATOS --archive --gzip > $ARCHIVO_SALIDA

# 6. Validación de ejecución
# $? almacena el código de salida (exit status) del ÚLTIMO comando ejecutado.
# En Linux, un código 0 significa éxito absoluto.
if [ $? -eq 0 ]; then
    echo "[EXITO] Backup completado y comprimido en: $ARCHIVO_SALIDA"
    echo "-----------------------------------------------------------------"
    echo "IMPORTANTE: Para cumplir con el requisito de automatización, "
    echo "este script se debe registrar en el demonio Cron de Linux."
    echo "Comando: crontab -e"
    echo "Regla (Todos los días a las 3 AM):"
    echo "0 3 * * * /home/cuervo/ComputacionII/TRABAJO_FINAL/src/db/backup.sh"
    echo "-----------------------------------------------------------------"
else
    # Si el contenedor está apagado o falla el disco, $? será distinto de 0
    echo "[ERROR] Fallo crítico al intentar crear el resguardo con mongodump."
fi