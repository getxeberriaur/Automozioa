# 🎯 ¿QUÉ ES HACKRF EN TU PRÁCTICA? — Guía Conceptual

## 📺 La Analogía Más Simple

Imagina que tienes un **teatro con dos roles distintos**:

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  RTL-SDR (Receptor/Cámara)       HackRF (Transmisor/Actor) │
│  ═════════════════════════════    ════════════════════════ │
│                                                             │
│  • Solo ESCUCHA señales           • Puede GRABAR           │
│  • Como una cámara de video       • Puede REPRODUCIR lo    │
│  • Pasa lo que ve a archivo       • grabado por la cámara  │
│                                                             │
│  Función: CAPTURAR                Función: REPRODUCIR      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 El Flujo Completo de tu Práctica

```
PASO 1: CAPTURA (RTL-SDR en Raspberry Pi)
═════════════════════════════════════════════════════════════

    Tu mando RF físico
           │
           ├─→ [Emite] "433.92 MHz"
           │
           ├─→ RTL-SDR [Antena + Dongle USB]
           │   └─→ "Capto la onda"
           │
           ├─→ Archivo guardado: capture.iq8
           │   (Estos son números que representan la onda)
           │
           └─→ Transferencia al portátil (SCP/SFTP)


PASO 2: ANÁLISIS (Portátil con Python)
═════════════════════════════════════════════════════════════

    Archivo capture.iq8
           │
           ├─→ hackrf_interactive.py
           │   └─→ "Visualizo la onda capturada"
           │       ├─ Gráfico de potencia en tiempo
           │       ├─ Espectro (FFT)
           │       └─ Espectrograma
           │
           ├─→ rf_capture_comparator.py
           │   └─→ "Comparo múltiples capturas"
           │       ├─ Detecta eventos (pulsaciones)
           │       └─ Estadísticas


PASO 3: REPRODUCCIÓN (HackRF One en portátil)
═════════════════════════════════════════════════════════════

    Archivo capture.iq8
           │
           ├─→ HackRF One [Antena + Interfaz USB]
           │   └─→ "Reproduzco exactamente la onda capturada"
           │
           ├─→ La antena emite
           │   └─→ "Alguien con RTL-SDR puede recibirla"
           │
           └─→ Permitir visualizar "¿Qué se transmite exactamente?"


PASO 4: COMPARACIÓN (RTL vs HackRF)
═════════════════════════════════════════════════════════════

    Captura Original (RTL-SDR)     Reproducción (HackRF)
           │                              │
           ├──────────────────────────────┤
           │                              │
    Análisis comparativo:
    ✓ ¿Son idénticas?
    ✓ ¿Hay distorsiones?
    ✓ ¿Cuál tiene más potencia?
    ✓ ¿Se pierden detalles en la reproducción?

```

---

## 🤔 ¿POR QUÉ HACKRF ES IMPORTANTE EN LA PRÁCTICA?

### Razón 1: Reproducibilidad
```
SIN HackRF:
  "Capturé una onda. Puedo verla, pero no puedo reproducirla.
   Solo tengo una foto estática de la onda."

CON HackRF:
  "Capturé una onda. Puedo reproducirla exactamente.
   Es como tener la grabación en video y poder hacer play."
```

### Razón 2: Educación sobre Seguridad
```
Los alumnos entienden:
  1. "¿Cómo se captura una señal de verdad?" (RTL-SDR)
  2. "¿Cómo es la onda cuando se reproduce?" (HackRF)
  3. "¿Qué diferencias hay?" (Comparación)
  4. "¿Por qué es importante validar si una onda es genuina?"
     (Defensa contra replay attacks y falsificaciones)
```

### Razón 3: Análisis Práctico
```
Preguntas que tu práctica ahora puede responder:

✓ ¿Cuál es la duración exacta de un pulso?
✓ ¿Cuál es la amplitud real (en dBm)?
✓ ¿Tiene ruido? ¿Cuánto?
✓ ¿Cuál es el espectro exacto?
✓ ¿Se puede falsificar sin ser detectado?
✓ ¿Qué información revela la onda sobre el dispositivo?
```

---

## 🔧 FLUJO TÉCNICO DETALLADO

### Fase 1: Captura (RTL-SDR → archivo IQ)

```
Mando RF emite a 433.92 MHz
        ↓
RTL-SDR lo recibe (2 millones de muestras por segundo)
        ↓
Cada muestra = 2 números (I, Q — componentes de la onda)
        ↓
Archivos guardado en formato .iq8 (uint8 intercalado)
        ↓
Archivo típico: 480 MB por 2 minutos
        ↓
Transferencia a portátil
```

**Lo que obtuviste:**
```
Archivo: capture_20261031_134500.iq8
├─ Muestras IQ: 240,000,000
├─ Duración: 120 segundos
├─ Frecuencia: 433.92 MHz
└─ Tamaño: 480 MB
```

---

### Fase 2: Análisis Visual (Python)

**hackrf_interactive.py** — Herramienta Interactiva:

```
Abre el archivo .iq8
        ↓
Crea 5 gráficos simultáneos:
├─ [1] Potencia en tiempo (línea azul)
│   └─→ "¿En qué momentos hay señal?"
│
├─ [2] Espectro FFT (frecuencias)
│   └─→ "¿Cuál es el contenido frecuencial?"
│
├─ [3] Histograma de potencia
│   └─→ "¿Cuál es la distribución de potencias?"
│
├─ [4] Espectrograma (tiempo-frecuencia)
│   └─→ "¿Cómo evolucionan las frecuencias en el tiempo?"
│
└─ [5] Detecta automáticamente eventos (pulsaciones)
    └─→ "¿Cuándo pulsaste el mando?"

INTERACTIVIDAD:
  • Slider para navegar en tiempo
  • Botones Anterior/Siguiente para explorar ventanas
  • Zoom en zonas de interés
  • Todo en una sola pantalla
```

**rf_capture_comparator.py** — Comparador:

```
Cargas 2 o más archivos .iq8
        ↓
Visualiza lado a lado:
├─ Potencia superpuesta (¿son iguales?)
├─ Espectros comparados (¿mismo contenido?)
├─ Tabla de estadísticas
├─ Timeline de eventos (¿sincronizados?)
└─ Distribución de duraciones

GENERA REPORTE:
  └─→ Estadísticas detalladas (media, min, max, etc.)
```

---

### Fase 3: Reproducción (HackRF)

```
HackRF conectado al portátil
        ↓
Comando:
    hackrf_transfer -t capture.iq8 -f 433920000 -s 2000000
        ↓
HackRF lee archivo .iq8
        ↓
Convierte números (I, Q) → señal RF analógica
        ↓
Emite por la antena a 433.92 MHz
        ↓
Alguien con un RTL-SDR en el mismo rango puede recibirla
```

**Parámetros importantes:**
```
-t capture.iq8         → Transmitir este archivo
-f 433920000           → Frecuencia: 433.92 MHz
-s 2000000             → Sample rate: 2 millones/segundo
-p 1                   → Potencia máxima (~20 dBm)
-a 1                   → Amplificador activado
```

---

## 🎓 ¿QUÉ APRENDEN LOS ALUMNOS?

### Concepto 1: Captura vs Reproducción
```
"No es lo mismo GRABAR algo que REPRODUCIRLO exactamente igual.
 La fidelidad es importante en comunicaciones."
```

### Concepto 2: Autenticidad de Señales
```
"Una onda capturada contiene 'huellas dactilares':
  - Amplitud y fase exactas
  - Ruido característico del dispositivo
  - Timing preciso
  
 Si intentas falsificar sin estos detalles, se detecta."
```

### Concepto 3: Vulnerabilidad y Defensa
```
VULNERABLE:        "Una alarma o cerradura que solo valida
                    la frecuencia es fácil de falsificar."

DEFENDIDO:         "Una alarma que valida:
                    • Frecuencia
                    • Modulación
                    • Timing exacto
                    • Código rolling (cambia cada vez)
                    
                    Es mucho más segura."
```

---

## 📊 TABLA COMPARATIVA: RTL-SDR vs HackRF

| Aspecto | RTL-SDR | HackRF |
|---------|---------|--------|
| **Función** | Receptor (Solo Rx) | Transmisor/Receptor (Tx/Rx) |
| **Frecuencia** | 24 MHz - 1.7 GHz | 1 MHz - 6 GHz |
| **Precisión** | ±50-100 ppm | ±20 ppm |
| **Potencia TX** | N/A | ~20 dBm (100 mW) |
| **Uso Típico** | Captura, análisis | Reproducción, pruebas |
| **Coste** | ~€25-40 | ~€300-400 |
| **En tu práctica** | **CAPTURA en RPi** | **REPRODUCCIÓN en portátil** |

---

## 🚀 FLUJO PRÁCTICO PASO A PASO

### Día 1: Captura (Raspberry Pi con RTL-SDR)

```bash
# En el Raspberry Pi
cd ~/rf_capture

# Ejecutar script de captura
./iq_capture.sh 120 captures/

# Resultado: capture_20261031_134500.iq8 (480 MB, 2 minutos)
```

**Qué ven los alumnos:**
- Interfaz clara que muestra progreso
- Confirmación de archivo guardado
- Tamaño del archivo

---

### Día 1: Análisis (Portátil Linux/macOS/WSL2)

```bash
# Descargar archivo
scp pi@192.168.1.100:~/rf_capture/captures/capture_*.iq8 ./

# Visualización interactiva
python3 hackrf_interactive.py capture_20261031_134500.iq8

# Qué ven:
# ✓ Gráfico con potencia en tiempo real
# ✓ Barra deslizante para navegar
# ✓ 5 gráficos sincronizados
# ✓ Lista de eventos detectados (pulsaciones del mando)
```

---

### Día 2: Reproducción (Portátil con HackRF One)

```bash
# Conectar HackRF al puerto USB

# Verificar que está conectado
hackrf_info

# Reproducir archivo capturado
hackrf_transfer -t capture_20261031_134500.iq8 \
    -f 433920000 -s 2000000 -p 1 -a 1

# Qué pasa:
# ✓ HackRF emite la onda exacta que se capturó
# ✓ Un RTL-SDR cercano podría captarla de nuevo
# ✓ Alumnos comprenden la reproducibilidad
```

---

### Día 2: Comparación (Portátil)

```bash
# Comparar múltiples capturas
python3 rf_capture_comparator.py capture_1.iq8 capture_2.iq8 capture_3.iq8

# Genera visualización:
# ✓ Potencia superpuesta
# ✓ Espectros lado a lado
# ✓ Tabla de estadísticas
# ✓ Timeline de eventos
# ✓ Reporte exportado a .txt
```

---

## ⚠️ CONSIDERACIONES IMPORTANTES

### Legal (España/UE)
```
✅ PERMITIDO:
   • Capturar señales públicas (educación)
   • Analizar sin reproducir
   • Reproducir en laboratorio controlado
   • Archivos históricos de tus propios dispositivos

❌ PROHIBIDO:
   • Reproducir en 433 MHz fuera del laboratorio
   • Interferir con dispositivos de terceros
   • Falsificar mandos de otros
   • Operación sin supervisor presente
```

### Seguridad
```
PROTECCIONES EN TU PRÁCTICA:
  ✓ HackRF con antena aislada (no apunta afuera)
  ✓ Sesión limitada (<30 minutos)
  ✓ Supervisor siempre presente
  ✓ Solo archivos .iq8 pre-grabados (no en directo)
  ✓ Laboratorio cerrado
```

---

## 📚 RESUMEN: ROL DE HACKRF EN TU PRÁCTICA

```
╔═══════════════════════════════════════════════════════════╗
║  HACKRF = "Reproductor de Ondas RF"                      ║
║                                                           ║
║  OBJETIVO:                                                ║
║  ─────────                                                ║
║  • Convertir archivos IQ → señales RF reales              ║
║  • Permitir que los alumnos comprendan:                   ║
║    1. Captura (RTL-SDR)                                   ║
║    2. Reproducción (HackRF)                               ║
║    3. Validación (¿son idénticas?)                        ║
║    4. Seguridad (¿cómo se defiende?)                      ║
║                                                           ║
║  RESULTADO EDUCATIVO:                                     ║
║  ──────────────────                                       ║
║  Los alumnos NO SOLO ven datos.                           ║
║  Comprenden el flujo RF COMPLETO.                         ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

---

## 🎯 SIGUIENTES PASOS PARA TU PRÁCTICA

1. **Instalar HackRF tools en portátil:**
   ```bash
   sudo apt install hackrf libhackrf0
   ```

2. **Crear documento de prácticas con HackRF** que incluya:
   - Checklist de seguridad
   - Paso a paso de reproducción
   - Ejercicio de comparación

3. **Tus scripts nuevos (ya creados):**
   - `hackrf_interactive.py` — Visualización interactiva
   - `rf_capture_comparator.py` — Comparación de capturas

4. **Integrar en el syllabus:**
   - Sesión 1: Captura (RTL-SDR, 2h)
   - Sesión 2: Análisis (Python, 1h)
   - Sesión 3: Reproducción (HackRF, 1h)
   - Sesión 4: Comparación y conclusiones (30 min)

---

**¿Preguntas sobre algún paso específico?**
