# 🛠️ Scripts de Análisis RF — Guía Rápida

Esta carpeta contiene herramientas Python para capturar, visualizar, reproducir y comparar archivos de radiofrecuencia (RF).

---

## 📦 Scripts Disponibles

### 1. **hackrf_interactive.py** — Visualización Interactiva 🎯

**¿Qué hace?**
- Abre un archivo IQ capturado con RTL-SDR
- Muestra 5 gráficos sincronizados simultáneamente
- Permite navegar por el archivo con slider de tiempo
- Detecta automáticamente eventos (pulsaciones del mando)

**Salida Visual:**
```
┌─────────────────────────────────────────────────────────┐
│ [1] Potencia en tiempo     [2] Espectro FFT            │
│     (línea azul)               (frecuencias)            │
├─────────────────────────────────────────────────────────┤
│ [3] Espectrograma       [4] Waterfall Zoomed           │
│     (tiempo-frecuencia)      (zoom ventana actual)     │
├─────────────────────────────────────────────────────────┤
│ [5] Lista de Eventos Detectados (pulsaciones)          │
├─────────────────────────────────────────────────────────┤
│  ◀ Anterior    ┌──────────────────┐    Siguiente ▶    │
│                │ Slider de Tiempo │                    │
└─────────────────────────────────────────────────────────┘
```

**Uso:**

```bash
# Forma básica
python3 hackrf_interactive.py capture.iq8

# Con parámetros personalizados
python3 hackrf_interactive.py capture.iq8 \
    --freq 433920000 \
    --rate 2000000 \
    --threshold 5
```

**Parámetros:**
- `--freq` (Hz): Frecuencia central capturada [def: 433.92 MHz]
- `--rate` (Hz): Sample rate de captura [def: 2 MHz]
- `--threshold` (dB): Umbral para detectar eventos [def: 5 dB]

**Ejemplo de sesión:**
```bash
$ python3 hackrf_interactive.py capture_20261031_134500.iq8

[✓] Archivo cargado: capture_20261031_134500.iq8
    Muestras IQ: 240,000,000
    Duración: 120.00 segundos
    Frecuencia: 433.920 MHz
    Sample Rate: 2.00 MHz

[*] Eventos detectados: 7
    E1: 10.25s - 11.49s (duracion 1.234s, potencia máx -15.3 dBm)
    E2: 20.48s - 21.68s (duracion 1.198s, potencia máx -14.8 dBm)
    ...
    
[*] Abriendo interfaz interactiva...
```

**Dentro de la interfaz:**
- Use **slider** abajo para navegar en tiempo
- Clicke **◀ Anterior** o **Siguiente ▶** para saltar
- Observe cómo se actualizan los 5 gráficos
- Los eventos detectados están resaltados en rojo en el timeline

---

### 2. **rf_capture_comparator.py** — Comparador de Capturas 🔄

**¿Qué hace?**
- Carga 2 o más archivos IQ capturados
- Compara potencia, espectros y eventos
- Genera visualización lado a lado
- Exporta reporte detallado con estadísticas

**Salida Visual:**
```
┌────────────────────────────────────────────────────┐
│ [1] Potencia Superpuesta (todas las capturas)      │
├────────────────────────────────────────────────────┤
│ [2] Tabla de Estadísticas (Media, Min, Max, etc)  │
├────────────────────────────────────────────────────┤
│ [3] Espectro Captura 1   [4] Espectro Captura 2   │
├────────────────────────────────────────────────────┤
│ [5] Timeline de Eventos (marcas punteadas)        │
├────────────────────────────────────────────────────┤
│ [6] Distribución de Duraciones de Eventos         │
└────────────────────────────────────────────────────┘

REPORTE:
========
Captura 1 / Captura 2 / Captura 3
├─ Duración
├─ Número de eventos
├─ Potencia media/min/max
└─ Detalle de cada evento
```

**Uso:**

```bash
# Comparar 2 archivos
python3 rf_capture_comparator.py capture1.iq8 capture2.iq8

# Comparar 3+ archivos
python3 rf_capture_comparator.py *.iq8

# Guardar reporte en archivo
python3 rf_capture_comparator.py capture1.iq8 capture2.iq8 \
    --report comparacion.txt

# Con parámetros personalizados
python3 rf_capture_comparator.py *.iq8 \
    --freq 433920000 \
    --rate 2000000 \
    --report reporte_completo.txt
```

**Parámetros:**
- `--freq` (Hz): Frecuencia central [def: 433.92 MHz]
- `--rate` (Hz): Sample rate [def: 2 MHz]
- `--report` (path): Guardar reporte en archivo

**Ejemplo de sesión:**
```bash
$ python3 rf_capture_comparator.py capture_*.iq8 --report reporte.txt

[✓] Cargada: capture_1 (120.0s, 7 eventos)
[✓] Cargada: capture_2 (120.0s, 8 eventos)
[✓] Cargada: capture_3 (120.0s, 7 eventos)

[*] Comparando 3 capturas...

╔════════════════════════════════════════════════════════════════╗
║           REPORTE DE COMPARACIÓN DE CAPTURAS RF                ║
╚════════════════════════════════════════════════════════════════╝

[*] Total de capturas analizadas: 3

─────────────────────────────────────────────────────────────────
CAPTURA 1: capture_1
─────────────────────────────────────────────────────────────────
  Archivo:           capture_20261031_134500.iq8
  Duración:          120.00 segundos
  Total muestras:    240,000,000
  Frecuencia:        433.920 MHz
  Sample rate:       2.00 MHz

  ESTADÍSTICAS DE POTENCIA:
    Media:           -25.34 dBm
    Mediana:         -25.20 dBm
    Desv. Est.:      2.15 dB
    Mínima:          -45.20 dBm
    Máxima:          -8.70 dBm
    Rango:           36.50 dB

  EVENTOS DETECTADOS: 7
  ...

═════════════════════════════════════════════════════════════════
RESUMEN COMPARATIVO
═════════════════════════════════════════════════════════════════

Captura más corta:  capture_1 (120.00s)
Captura más larga:  capture_3 (120.00s)
Señal más fuerte:   capture_2 (-24.56 dBm media)
Señal más débil:    capture_1 (-25.34 dBm media)
Más eventos:        capture_2 (8 eventos)

[✓] Reporte guardado: reporte.txt
```

---

### 3. **analyze_spectrum.py** — Análisis de Espectro 📊

**¿Qué hace?**
- Carga CSV de rtl_power (captura pasiva)
- Detecta eventos de potencia
- Genera gráficos de espectro
- Genera espectrograma waterfall

**Uso:**
```bash
python3 analyze_spectrum.py capture.csv
```

**Salida:**
- `plots/spectrum_YYYYMMDD_HHMMSS.png` — Espectro + espectrograma
- `plots/reporte_YYYYMMDD_HHMMSS.txt` — Eventos detectados

---

### 4. **hackrf_playback.py** — Reproductor IQ 📡

**¿Qué hace?**
- Carga archivo IQ capturado
- Genera reportes de análisis
- Crea gráficos de potencia/espectrograma

**Uso:**
```bash
# Ver reporte
python3 hackrf_playback.py capture.iq8 --report

# Generar gráficos
python3 hackrf_playback.py capture.iq8 \
    --plot-all plots \
    --plot-start-s 0 \
    --plot-duration-s 20
```

---

## 🚀 Flujo Típico de Uso (Laboratorio)

### Día 1: Captura + Análisis

```bash
# 1. En Raspberry Pi: Capturar
ssh pi@192.168.1.100
cd ~/rf_capture
./iq_capture.sh 120 captures/

# 2. En portátil: Descargar
scp pi@192.168.1.100:~/rf_capture/captures/*.iq8 ./

# 3. Visualización interactiva
python3 hackrf_interactive.py capture_20261031_134500.iq8

# 4. Análisis de evento específico
# (Usar slider para explorar zona de interés)
```

### Día 2: Reproducción + Comparación

```bash
# 1. Reproducir con HackRF
hackrf_transfer -t capture_20261031_134500.iq8 \
    -f 433920000 -s 2000000 -p 1 -a 1

# 2. Capturar de nuevo con RTL-SDR mientras HackRF emite
./iq_capture.sh 120 captures/

# 3. Comparar captura original vs reproducida
python3 rf_capture_comparator.py \
    capture_original.iq8 capture_reproducida.iq8 \
    --report comparacion_original_vs_reproducida.txt
```

---

## 📋 Requisitos e Instalación

### Dependencias Python
```bash
pip install numpy scipy matplotlib
```

### Herramientas Externas
```bash
# Para HackRF (reproducción)
sudo apt install hackrf libhackrf0

# Verificar instalación
hackrf_info
```

---

## 🐛 Solución de Problemas

### Error: `ModuleNotFoundError: No module named 'numpy'`
```bash
pip install numpy scipy matplotlib
```

### Error: `No se encontraron columnas de potencia`
- Asegúrate que el CSV tiene encabezados o está en formato rtl_power

### Error: `No X11 forwarding display available`
- Usar `--plot-all plots/` para guardar a archivo en lugar de mostrar ventana

### HackRF no conecta
```bash
# Verificar permisos
lsusb | grep HackRF
sudo hackrf_info

# Crear reglas udev si falta
sudo nano /etc/udev/rules.d/10-hackrf.rules
# Agregar:
# SUBSYSTEM=="usb", ATTRS{idVendor}=="1d50", ATTRS{idProduct}=="604b", MODE="0666"

sudo udevadm control --reload
sudo udevadm trigger
```

---

## 📚 Referencia Rápida de Comandos

| Tarea | Comando |
|-------|---------|
| Visualización interactiva | `python3 hackrf_interactive.py file.iq8` |
| Comparar capturas | `python3 rf_capture_comparator.py *.iq8` |
| Generar reporte | `... --report output.txt` |
| Reproducir con HackRF | `hackrf_transfer -t file.iq8 -f 433920000 -s 2000000` |
| Verificar HackRF | `hackrf_info` |
| Analizar espectro CSV | `python3 analyze_spectrum.py file.csv` |

---

## 🎓 Ejemplos de Prácticas

### Práctica 1: "¿Cuál es la verdadera forma de la onda?"
```
Objetivo: Usar hackrf_interactive.py para explorar estructura de eventos
Entregable: Reporte con gráficos de 3 eventos diferentes
```

### Práctica 2: "¿Son iguales dos capturas?"
```
Objetivo: Comparar 2+ capturas con rf_capture_comparator.py
Entregable: Reporte de comparación + análisis de diferencias
```

### Práctica 3: "¿Puedo reproducir exactamente una captura?"
```
Objetivo: Capturar → Reproducir con HackRF → Recapturar → Comparar
Entregable: Análisis de fidelidad de reproducción
```

---

## 📞 Soporte

Si encuentras errores:
1. Verifica que los archivos .iq8 existen
2. Comprueba que Python 3.7+ está instalado
3. Instala dependencias: `pip install numpy scipy matplotlib`
4. Lee el mensaje de error completo (scroll arriba)

---

**Última actualización:** 2026-10-31  
**Versión de scripts:** 1.2
