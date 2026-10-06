# Inicio rápido — Laboratorio RF pasivo

Este laboratorio analiza espectro recibido con un RTL-SDR y un emisor de prueba propio, aislado y autorizado. No incluye transmisión, replay, jamming ni conexión a receptores o vehículos.

## Requisitos

- Raspberry Pi 4/5 con RTL-SDR y antena de recepción.
- Emisor de prueba aislado de 433.92 MHz.
- Portátil con Python 3.8+ y conexión SSH a la Raspberry Pi.

## Preparación

1. Lee [Ética y seguridad](docs/04_ETICA_Y_SEGURIDAD.md).
2. Sigue la guía de [instalación de Raspberry Pi](docs/01_GUIA_RASPBERRY.md) y la [guía de análisis en portátil](docs/02_GUIA_PORTATIL.md).
3. Revisa el [procedimiento de captura](docs/03_PROCEDIMIENTO_CAPTURA.md).

## Captura y análisis

En la Raspberry Pi, desde la carpeta que contiene `spectrum_capture.sh`:

```bash
./spectrum_capture.sh 120 ~/rf_capture
```

Copia el CSV resultante al portátil y prepara las dependencias documentadas en `docs/02_GUIA_PORTATIL.md`. Después ejecuta:

```bash
python3 scripts/analyze_spectrum.py data/spectrum_<fecha>.csv
```

Completa [la plantilla de informe](templates/INFORME_ALUMNOS.md) y conserva las capturas y resultados generados.

## Límites

Usa únicamente señales de un emisor de prueba aislado, dentro del laboratorio y bajo supervisión. No captures señales de llaves, TPMS u otros equipos reales; no transmitas ni reproduzcas señales.
