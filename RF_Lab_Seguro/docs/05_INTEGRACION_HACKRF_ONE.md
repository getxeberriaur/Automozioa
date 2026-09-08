# Integración HackRF One: Reproducción de Capturas RTL-SDR

**Opción B: Reproducción de Archivos Capturados**

---

## 📋 Resumen

Este documento describe cómo:
1. Capturar datos IQ (complejos) desde RTL-SDR en Raspberry Pi
2. Transferir archivos al portátil
3. Reproducir en HackRF One (portátil) con visualización

```
┌──────────────────────────────────┐
│  Raspberry Pi + RTL-SDR           │
│  ├─ Captura: iq_capture.sh        │
│  └─ Salida: capture_*.iq8         │
│          ↓ SCP                    │
│  ┌──────────────────────────────┐ │
│  │  Portátil (Linux/macOS)      │ │
│  ├─ Recibe: capture_*.iq8        │ │
│  ├─ HackRF One (conectado USB)   │ │
│  ├─ Reproducción: hackrf_transfer │ │
│  ├─ Análisis: hackrf_playback.py │ │
│  └─ Visualización: matplotlib    │ │
│                                  │ │
│  [Espectrograma/Potencia en vivo] │
└──────────────────────────────────┘
```

---

## 🔧 Requisitos: Portátil

### Software

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install -y hackrf libhackrf0 libhackrf-dev python3-pip

pip3 install numpy scipy matplotlib
```

**macOS:**
```bash
brew install hackrf

pip3 install numpy scipy matplotlib
```

**Verificar instalación:**
```bash
hackrf_info
```

Salida esperada:
```
HackRF One
...
```

### Hardware

- **HackRF One** conectado a puerto USB del portátil
- **Antena dipolo 433 MHz** conectada al puerto SMA de HackRF

---

## 📤 Paso 1: Captura en Raspberry Pi

### En RPi (SSH desde portátil):

```bash
ssh pi@192.168.1.100
cd ~/rf_capture

# Ejecutar script de captura IQ
./iq_capture.sh 120 captures/

# Salida:
# ╔════════════════════════════════════════════════════════════════╗
# ║  CAPTURA DE DATOS IQ — RTL-SDR (Para HackRF One)              ║
# ╚════════════════════════════════════════════════════════════════╝
# 
# [*] Parámetros:
#     Frecuencia:     433.92M
#     Sample Rate:    2000000 Hz (2 MHz)
#     ...
# [?] ¿Comenzar captura? (s/n): s
```

**Cronología durante captura (120s):**
```
0-10s    | Ruido de fondo
10-11s   | Pulsar mando (Evento 1)
11-20s   | Ruido de fondo
20-21s   | Pulsar mando (Evento 2)
...
50-60s   | Última pulsación
60-120s  | Grabación continúa
```

**Resultado:**
```
[✓] Archivo guardado: captures/capture_20260624_123456.iq8
[*] Tamaño real: 480 MB
[*] Muestras IQ: 240000000
```

---

## 📥 Paso 2: Transferencia al Portátil

**En portátil:**

```bash
# Crear carpeta si no existe
mkdir -p ~/rf-analysis/captures

# Descargar archivo desde RPi (sftp o scp)
scp pi@192.168.1.100:~/rf_capture/captures/capture_*.iq8 ~/rf-analysis/captures/

# Verificar
ls -lh ~/rf-analysis/captures/
```

Salida esperada:
```
-rw-r--r-- 1 user group 480M Jun 24 12:35 capture_20260624_123456.iq8
```

---

## 🎯 Paso 3: Análisis en Portátil

### 3A: Análisis Rápido (Python)

**Ver estadísticas y eventos detectados:**

```bash
cd ~/rf-analysis

python3 ../RF_Lab_Seguro/scripts/hackrf_playback.py \
    captures/capture_20260624_123456.iq8 \
    --report
```

**Salida:**
```
[✓] Archivo cargado: captures/capture_20260624_123456.iq8
    Muestras IQ: 240,000,000
    Duración: 120.00 segundos
    Frecuencia: 433.920 MHz
    Sample Rate: 2.00 MHz

======================================================================
ANÁLISIS DE ARCHIVO IQ
======================================================================

[*] Eventos detectados: 7

    Evento | Tiempo Inicio | Duración | Potencia Máx | Baseline
    ────────────────────────────────────────────────────────────────
        1  |  10.25s       |  1.234s  |  +15.3 dBm   |  +2.1 dBm
        2  |  20.48s       |  1.198s  |  +14.8 dBm   |  +2.1 dBm
        3  |  30.71s       |  1.256s  |  +15.1 dBm   |  +2.1 dBm
        ...

[*] Estadísticas de Potencia:
    Media:     +2.3 dBm
    Mediana:   +2.1 dBm
    Desv. Est: +1.5 dB
    Mínima:    -45.2 dBm
    Máxima:    +18.7 dBm
======================================================================
```

### 3B: Generar Gráficos

**Opción recomendada (un solo comando, robusto para archivos grandes):**

```bash
python3 ../RF_Lab_Seguro/scripts/hackrf_playback.py \
    captures/capture_20260624_123456.iq8 \
    --report \
    --plot-all plots \
    --plot-start-s 0 \
    --plot-duration-s 20 \
    --max-plot-points 200000
```

Genera automáticamente:
- `plots/capture_20260624_123456_power.png`
- `plots/capture_20260624_123456_spectrogram.png`

**Comandos separados (si prefieres control manual):**

**Gráfico de potencia en tiempo:**

```bash
python3 ../RF_Lab_Seguro/scripts/hackrf_playback.py \
    captures/capture_20260624_123456.iq8 \
    --plot-power plots/potencia.png \
    --plot-start-s 0 \
    --plot-duration-s 20 \
    --max-plot-points 200000
```

**Espectrograma (tiempo-frecuencia):**

```bash
python3 ../RF_Lab_Seguro/scripts/hackrf_playback.py \
    captures/capture_20260624_123456.iq8 \
    --plot-spectrogram plots/espectrograma.png \
    --plot-start-s 0 \
    --plot-duration-s 20
```

**Si aparece error de memoria o el gráfico tarda demasiado:**

```bash
python3 ../RF_Lab_Seguro/scripts/hackrf_playback.py \
    captures/capture_20260624_123456.iq8 \
    --plot-all plots \
    --plot-start-s 0 \
    --plot-duration-s 8 \
    --max-plot-points 80000
```

Salida esperada:
```
[✓] Archivo cargado: ...
    Muestras IQ: 240,000,000
    ...
[✓] Gráfico guardado: plots/potencia.png
[✓] Espectrograma guardado: plots/espectrograma.png
```

### 3C: Errores Típicos de Visualización

**`ModuleNotFoundError: No module named 'numpy'`**
```bash
python3 -m pip install numpy scipy matplotlib
```

**No aparece ventana gráfica (entorno sin GUI):**
- Usar siempre salida a archivo con `--plot-all` o `--plot-power/--plot-spectrogram`.

**Archivo muy grande (120s o más):**
- Limitar ventana temporal con `--plot-duration-s`.
- Reducir puntos con `--max-plot-points`.

---

## 📡 Paso 4: Reproducción con HackRF One

### 4A: Reproducción en Tiempo Real

**Transmitir archivo IQ a través de HackRF (⚠️ SOLO EN LABORATORIO CERRADO):**

```bash
# Sintaxis:
hackrf_transfer -t <archivo.iq8> -f <frecuencia_hz> -s <sample_rate> -p 1 -a 1

# Ejemplo con archivo capturado:
cd ~/rf-analysis/captures

hackrf_transfer -t capture_20260624_123456.iq8 \
    -f 433920000 \
    -s 2000000 \
    -p 1 \
    -a 1
```

**Parámetros:**
- `-t`: Transmitir archivo
- `-f 433920000`: Frecuencia central (433.92 MHz)
- `-s 2000000`: Sample rate (2 MHz)
- `-p 1`: Antenna power (0-1, donde 1 = potencia máxima ~20 dBm)
- `-a 1`: Amplificador (0 o 1)

**Salida esperada:**
```
Transmitting, press Ctrl+C to stop
Actual frequency: 433.920000 MHz
[*] 2000000 Hz sample rate
[*] Actual TX gain: 0 dB
TX: 0.00 Mb/s  (0 bytes / 0.00 seconds)
...
Exiting...
[✓] TX finished
```

### 4B: Reproducción Continua

**Reproducir repetidamente (loop):**

```bash
# Bash script para reproducir archivo múltiples veces
for i in {1..3}; do
    echo "Iteración $i..."
    hackrf_transfer -t capture_20260624_123456.iq8 \
        -f 433920000 -s 2000000 -p 1 -a 1
    sleep 2
done
```

---

## 👁️ Paso 5: Visualización en Vivo

### Opción A: Con GNU Radio (Avanzado)

**Instalación:**
```bash
sudo apt install gnuradio gnuradio-dev
sudo apt install gr-osmosdr libosmocom0
```

**Flujo en GNU Radio:**
1. Source: `osmocom Source` (RTL-SDR o HackRF)
2. Block: `FFT Sink` (visualización espectral)
3. Block: `Time Sink` (potencia en tiempo)

### Opción B: Con Python + Matplotlib (Recomendado)

**Script en tiempo real (streaming desde HackRF):**

```python
import subprocess
import numpy as np
import matplotlib.pyplot as plt
import struct
from scipy import signal

# Iniciar captura desde HackRF
proc = subprocess.Popen(
    ['hackrf_transfer', '-r', '-', '-f', '433920000', '-s', '2000000'],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

for iteration in range(100):  # 100 bloques
    # Leer 4096 muestras IQ
    raw_data = proc.stdout.read(4096 * 2)  # 2 bytes por muestra
    
    if len(raw_data) < 8192:
        break
    
    # Convertir a complejos
    iq_bytes = np.frombuffer(raw_data, dtype=np.int8)
    iq = iq_bytes[0::2].astype(np.float32) + 1j * iq_bytes[1::2].astype(np.float32)
    
    # FFT
    fft_result = np.fft.fft(iq)
    magnitude = np.abs(fft_result)
    magnitude_db = 10 * np.log10(magnitude + 1e-10)
    
    # Potencia
    power = np.abs(iq) ** 2
    
    # Graficar
    ax1.clear()
    ax1.plot(magnitude_db)
    ax1.set_title('FFT (Espectro)')
    
    ax2.clear()
    ax2.plot(power)
    ax2.set_title('Potencia en el Tiempo')
    
    plt.pause(0.01)

proc.terminate()
plt.close()
```

---

## ⚠️ Notas de Seguridad y Cumplimiento

### ✅ PERMITIDO
- Reproducir archivos capturados en laboratorio controlado
- Visualizar espectro en pantalla
- Analizar archivos capturados sin retransmisión

### ❌ PROHIBIDO
- Transmitir en 433 MHz fuera del laboratorio
- Retransmitir señales de mandos reales
- Interferencia activa (jamming)
- Operación sin supervisor presente

**Verificación previa a cada uso:**
- [ ] Supervisor presente
- [ ] Laboratorio cerrado
- [ ] Solo archivo IQ reproducido (sin señales reales)
- [ ] HackRF con antena aislada del equipo externo
- [ ] Duración limitada (<30 minutos)

---

## 🔧 Troubleshooting

### Problema: `hackrf_info: command not found`
**Solución:**
```bash
sudo apt install hackrf libhackrf0
```

### Problema: `libusb_open() failed with LIBUSB_ERROR_ACCESS`
**Solución (agregar permisos USB):**
```bash
# Crear archivo de reglas
sudo nano /etc/udev/rules.d/10-hackrf.rules

# Agregar:
SUBSYSTEM=="usb", ATTRS{idVendor}=="1d50", ATTRS{idProduct}=="604b", MODE="0666"

# Recargar reglas
sudo udevadm control --reload
sudo udevadm trigger

# Desconectar y reconectar HackRF
```

### Problema: Archivo muy grande (>500 MB)
**Solución - Limitar duración:**
```bash
# Capturar solo 30 segundos
./iq_capture.sh 30 captures/

# Resultado: ~60 MB
```

---

## 📚 Referencia de Comandos

| Comando | Propósito |
|---------|-----------|
| `hackrf_info` | Verificar conexión HackRF |
| `hackrf_transfer -r` | Recibir datos |
| `hackrf_transfer -t` | Transmitir datos |
| `rtl_sdr` | Capturar con RTL-SDR |
| `python3 hackrf_playback.py file.iq8 --report` | Análisis detallado |
| `python3 hackrf_playback.py file.iq8 --plot-*` | Generar gráficos |

---

## 🎓 Próximos Pasos

1. **Comparar eventos:** Detectar diferencias entre múltiples capturas
2. **Frecuencias alternativas:** Capturar a otros 433 MHz (ej: 433.05 MHz)
3. **Análisis de modulación:** Identificar tipo de código (rolling vs fixed)
4. **Detección de patrones:** Machine Learning sobre eventos

