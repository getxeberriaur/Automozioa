#!/bin/bash

# iq_capture.sh
# Script para captura de datos IQ (complejos) con RTL-SDR en Raspberry Pi
# Uso: ./iq_capture.sh [duracion_segundos] [ruta_salida] [frecuencia] [sample_rate]
# Salida: archivo .iq8 compatible con HackRF One

set -e

# Configuración
FREQ="${3:-433.92M}"     # Frecuencia central (ej: 433.92M, 315M, 868.3M)
SAMPLE_RATE="${4:-2000000}"  # 2 MHz por defecto
GAIN="40"
DURATION="${1:-120}"     # 120 segundos por defecto
OUTPUT_DIR="${2:-.}"

# Validar
if ! command -v rtl_sdr &> /dev/null; then
    echo "[✗] Error: rtl_sdr no encontrado. Instalar: sudo apt install rtl-sdr"
    exit 1
fi

# Crear salida
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT_FILE="${OUTPUT_DIR}/capture_${TIMESTAMP}.iq8"

# Crear directorio si no existe
mkdir -p "$OUTPUT_DIR"

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  CAPTURA DE DATOS IQ — RTL-SDR (Para HackRF One)              ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "[*] Parámetros:"
echo "    Frecuencia:     ${FREQ}"
echo "    Sample Rate:    ${SAMPLE_RATE} Hz (2 MHz)"
echo "    Ganancia:       ${GAIN}"
echo "    Duración:       ${DURATION} segundos"
echo "    Salida:         ${OUTPUT_FILE}"
echo ""
echo "[*] INSTRUCCIONES:"
echo "    • Colocar mando a ~50 cm de antena"
echo "    • Pulsar mando en tiempos: 10s, 20s, 30s, 40s, 50s (aprox)"
echo "    • Esperar a que finalice automáticamente"
echo ""
read -p "[?] ¿Comenzar captura? (s/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Ss]$ ]]; then
    echo "[✗] Cancelado."
    exit 1
fi

echo ""
echo "[*] Iniciando captura IQ..."
echo "    (Presiona CTRL+C para cancelar)"
echo ""

# Calcular tamaño aproximado
SIZE_MB=$(echo "scale=1; $SAMPLE_RATE * 2 * $DURATION / 1024 / 1024" | bc)
echo "[*] Tamaño estimado: ${SIZE_MB} MB"
echo ""

# Capturar datos IQ en formato int8
# rtl_sdr -f <frecuencia> -s <sample_rate> -g <ganancia> <archivo_salida>
rtl_sdr -f "$FREQ" \
        -s "$SAMPLE_RATE" \
        -g "$GAIN" \
        -n $((SAMPLE_RATE * DURATION)) \
        "$OUTPUT_FILE"

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  ✓ CAPTURA COMPLETADA                                         ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "[✓] Archivo guardado: ${OUTPUT_FILE}"
echo "[*] Tamaño real: $(ls -lh "$OUTPUT_FILE" | awk '{print $5}')"
echo "[*] Muestras IQ: $((SAMPLE_RATE * DURATION))"
echo ""
echo "[→] Siguiente: Transferir a portátil con SCP"
echo "    scp pi@192.168.1.100:${OUTPUT_FILE} ~/rf-analysis/captures/"
echo ""
echo "[→] En portátil: Reproducir con HackRF One"
echo "    hackrf_transfer -t ${OUTPUT_FILE} -f 433920000 -s 2000000"
echo ""
