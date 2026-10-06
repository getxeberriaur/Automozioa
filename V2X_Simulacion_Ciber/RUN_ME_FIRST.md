# Arranque rápido — Laboratorio V2X

## Requisitos

- Python 3.10 o posterior.
- Dos terminales en la carpeta raíz del repositorio.
- No se necesitan dependencias externas: se usa únicamente la biblioteca estándar de Python.

## 1. Arrancar el gateway protegido

En la primera terminal:

```bash
python V2X_Simulacion_Ciber/scripts/v2x_gateway.py
```

Debe aparecer:

```text
Gateway V2X escuchando en http://127.0.0.1:8090 (protegido)
```

## 2. Enviar un mensaje legítimo

En la segunda terminal:

```bash
python V2X_Simulacion_Ciber/scripts/send_v2x.py legitimo
```

El resultado esperado es `HTTP 202` y `"status": "accepted"`.

## 3. Ejecutar escenarios

```bash
python V2X_Simulacion_Ciber/scripts/send_v2x.py replay
python V2X_Simulacion_Ciber/scripts/send_v2x.py spoof
python V2X_Simulacion_Ciber/scripts/send_v2x.py impossible
python V2X_Simulacion_Ciber/scripts/send_v2x.py old
python V2X_Simulacion_Ciber/scripts/send_v2x.py burst
```

Para observar el comportamiento vulnerable, detener el gateway y arrancarlo con:

```bash
python V2X_Simulacion_Ciber/scripts/v2x_gateway.py --insecure
```

En este modo se desactivan los controles de seguridad del gateway. El objetivo es comparar evidencias, no dejar este modo como configuración válida.

## Detener

Pulsa `Ctrl+C` en la terminal del gateway.