#!/bin/bash

# spectrum_capture.sh
# Script para captura de espectro RF con RTL-SDR en Raspberry Pi
# Uso: ./spectrum_capture.sh [duración_segundos] [ruta_salida]

set -e

# Configuración por defecto
FREQ_START="433.5M"
FREQ_STOP="434.5M"
FREQ_STEP="100k"
GAIN="40"
DURATION="${1:-120}"  # 120 segundos por defecto
OUTPUT_DIR="${2:-.}"

# Validar
if ! command -v rtl_power &> /dev/null; then
    echo "[✗] Error: rtl_power no encontrado. Instalar: sudo apt install rtl-sdr"
    exit 1
fi

# Crear salida
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT_FILE="${OUTPUT_DIR}/spectrum_${TIMESTAMP}.csv"

# Crear directorio si no existe
mkdir -p "$OUTPUT_DIR"

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  CAPTURA DE ESPECTRO RF — 433 MHz                             ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "[*] Parámetros:"
echo "    Rango:      ${FREQ_START} a ${FREQ_STOP}"
echo "    Paso:       ${FREQ_STEP}"
echo "    Ganancia:   ${GAIN}"
echo "    Duración:   ${DURATION} segundos"
echo "    Salida:     ${OUTPUT_FILE}"
echo ""
echo "[*] INSTRUCCIONES:"
echo "    • Mantener mando a ~50 cm de antena"
echo "    • Pulsar mando a los 10, 20, 30, 40, 50 segundos (aprox)"
echo "    • Esperar a que finalice automáticamente"
echo ""
read -p "[?] ¿Comenzar captura? (s/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Ss]$ ]]; then
    echo "[✗] Cancelado."
    exit 1
fi

echo ""
echo "[*] Iniciando captura..."
echo "    (Presiona CTRL+C para cancelar)"
echo ""

# Ejecutar captura
rtl_power -f "${FREQ_START}:${FREQ_STOP}:${FREQ_STEP}" \
          -g "${GAIN}" \
          -i 1 \
          -e "${DURATION}s" \
          "$OUTPUT_FILE"

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  ✓ CAPTURA COMPLETADA                                         ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "[✓] Archivo guardado: ${OUTPUT_FILE}"
echo "[*] Tamaño: $(ls -lh "$OUTPUT_FILE" | awk '{print $5}')"
echo "[*] Líneas: $(wc -l < "$OUTPUT_FILE")"
echo ""
echo "[→] Siguiente: Transferir a portátil con SCP"
echo "    scp pi@192.168.1.100:${OUTPUT_FILE} ~/rf-analysis/data/"
echo ""
