# 🎯 Práctica de Laboratorio: HackRF One — Reproducción y Validación RF

**Duración:** 2-2.5 horas  
**Nivel:** Intermedio-Avanzado  
**Equipo:** Raspberry Pi + RTL-SDR, Portátil + HackRF One  
**Objetivo:** Comprender captura, reproducción y validación de señales RF

---

## 📋 CHECKLIST DE SEGURIDAD PRE-PRÁCTICA

**ANTES DE COMENZAR, VERIFICAR:**

- [ ] **HackRF conectado al portátil** (puerto USB)
  - Comando: `hackrf_info`
  - Resultado esperado: "HackRF One" + versión

- [ ] **Antena HackRF conectada**
  - ⚠️ CRÍTICO: La antena debe estar **aislada** (no apuntando fuera)
  - Usar antena dipolo 433 MHz (o improvisada con cable)

- [ ] **Laboratorio cerrado**
  - Puertas cerradas
  - Sin acceso de personas no autorizadas

- [ ] **Supervisor presente**
  - Profesor o técnico disponible
  - Puede detener la práctica en cualquier momento

- [ ] **Archivos .iq8 pre-grabados**
  - ✓ NO capturar en directo (solo reproducir archivos guardados)
  - ✓ Archivos de prácticas anteriores o ejemplos

- [ ] **Duración limitada**
  - Máximo 30 minutos de reproducción
  - HackRF se calienta si transmite continuamente

- [ ] **Equipos de protección**
  - Gafas de seguridad (recomendado)
  - Zona de trabajo despejada

- [ ] **Documentación a mano**
  - Este documento impreso o en segunda pantalla
  - README_SCRIPTS.md como referencia

**FIRMADO POR:**
- Alumno: _________________________ Fecha: _______
- Supervisor: _____________________ Fecha: _______

---

## 🎓 OBJETIVOS DE APRENDIZAJE

Al completar esta práctica, serás capaz de:

1. ✓ **Reproducir archivos IQ capturados** con HackRF One
2. ✓ **Validar fidelidad de reproducción** comparando captura vs reproducción
3. ✓ **Detectar diferencias** entre ondas originales y falsificadas
4. ✓ **Entender vulnerabilidades** de validación en sistemas RF
5. ✓ **Proponer defensa en profundidad** para sistemas seguros

---

## 🔧 REQUISITOS PREVIOS

### Software (en portátil)

```bash
# Instalar HackRF tools
sudo apt install hackrf libhackrf0

# Verificar instalación
hackrf_info

# Instalar dependencias Python (si no están)
pip install numpy scipy matplotlib

# Verificar scripts disponibles
ls ~/rf_analysis/scripts/hackrf_*.py
```

### Hardware

- [ ] HackRF One (conectado USB, con antena)
- [ ] Archivo .iq8 capturado previamente (>30 segundos)
- [ ] RTL-SDR conectado a Raspberry Pi (para recapturar)
- [ ] Portátil con Linux/macOS/WSL2
- [ ] Red local para transferencia SCP

### Archivos

```
Tu carpeta de trabajo debe tener:
├─ capture_original.iq8       (archivo a reproducir)
├─ hackrf_interactive.py       (para visualizar)
├─ rf_capture_comparator.py   (para comparar)
└─ este_documento.md          (guía paso a paso)
```

---

## 📖 PARTE 1: PREPARACIÓN (15 minutos)

### Paso 1.1: Verificar HackRF

```bash
# Conectar HackRF One al puerto USB del portátil

# Verificar conexión
hackrf_info

# Salida esperada:
# ╔═══════════════════════════════════════════════════════════╗
# ║         HackRF One r9                                    ║
# ╠═══════════════════════════════════════════════════════════╣
# ║ Serial Number: 0000000000000000YYYYYYYYYY               ║
# ║ Board ID Code: 0x04 (HackRF One)                        ║
# ║ Firmware Version: 2022.09.1                              ║
# ║ Part ID Number: 0xa000c21b 0x00634d44                   ║
# ║                 0x00000000 0x00000000                    ║
# ║ USB Bus Speed: High Speed                                ║
# ║ USB D+ Pullup: False                                     ║
# ║ Clock Source: Internal                                   ║
# ║ Baseband Filter Bandwidth Setting: 1750000 Hz            ║
# ║ LNA Gain: 0 dB                                           ║
# ║ VGA Gain: 0 dB                                           ║
# ║ TX VGA Gain: 47 dB                                       ║
# ╚═══════════════════════════════════════════════════════════╝
```

**Si ves error `libusb_open() failed`:**
```bash
# Crear reglas udev
sudo nano /etc/udev/rules.d/10-hackrf.rules

# Agregar esta línea:
# SUBSYSTEM=="usb", ATTRS{idVendor}=="1d50", ATTRS{idProduct}=="604b", MODE="0666"

# Recargar
sudo udevadm control --reload
sudo udevadm trigger

# Desconectar y reconectar HackRF
```

✅ **Checkpoint:** HackRF conectado y detectado

---

### Paso 1.2: Preparar Archivo IQ

```bash
# Verificar que tienes archivo .iq8
ls -lh *.iq8

# Salida esperada:
# -rw-r--r-- 1 user group 480M Oct 31 13:45 capture_20261031_134500.iq8

# Si no tienes, descargar desde RPi:
scp pi@192.168.1.100:~/rf_capture/captures/capture_*.iq8 ./
```

**Requisitos del archivo:**
- Duración: mínimo 30 segundos, máximo 2 minutos
- Formato: .iq8 (uint8 intercalado)
- Tamaño: típicamente 240-480 MB
- Debe contener eventos (pulsaciones)

✅ **Checkpoint:** Archivo .iq8 disponible localmente

---

### Paso 1.3: Verificar Scripts

```bash
# Comprobar que los scripts existen
python3 hackrf_interactive.py --help
python3 rf_capture_comparator.py --help

# Salida esperada:
# usage: hackrf_interactive.py [-h] [--freq FREQ] [--rate RATE] ...
# usage: rf_capture_comparator.py [-h] [--freq FREQ] ...
```

✅ **Checkpoint:** Scripts listos para usar

---

## 📊 PARTE 2: ANÁLISIS DE CAPTURA ORIGINAL (30 minutos)

### Paso 2.1: Visualización Interactiva

```bash
# Abrir archivo con visualización interactiva
python3 hackrf_interactive.py capture_20261031_134500.iq8

# Se abrirá ventana interactiva con 5 gráficos sincronizados
```

**Qué observar:**

```
┌────────────────────────────────────────────────────────────┐
│ [1] POTENCIA EN TIEMPO (arriba, azul)                      │
│     ├─ Línea azul = potencia a lo largo del tiempo         │
│     ├─ Líneas rojas = eventos detectados automáticamente   │
│     └─ ¿En qué momentos hay pulsaciones?                   │
│                                                            │
│ [2] ESPECTRO FFT (abajo izq)                               │
│     ├─ Línea verde = contenido frecuencial                │
│     └─ ¿Dónde está concentrada la energía?               │
│                                                            │
│ [3] HISTOGRAMA (abajo derecha)                             │
│     ├─ Barras = distribución de potencias                 │
│     └─ ¿Es gaussiana o uniforme?                          │
│                                                            │
│ [4] ESPECTROGRAMA (medio derecha)                          │
│     ├─ Mapa de calor = potencia vs tiempo vs frecuencia   │
│     └─ ¿Cómo evolucionan las frecuencias?                 │
│                                                            │
│ [5] WATERFALL (abajo)                                      │
│     ├─ Zoom detallado del segmento actual                 │
│     └─ ¿Hay modulación? ¿Estructura fina?                 │
└────────────────────────────────────────────────────────────┘
```

### Paso 2.2: Exploración con Slider

**Usar el slider (barra abajo) para:**

1. **Localizar eventos** (pulsaciones)
   - Mueve el slider lentamente
   - Observa cuándo suben los picos rojos en el timeline

2. **Explorar primer evento**
   - Desliza hasta el primer evento
   - Observa los 5 gráficos en ese momento
   - Toma captura de pantalla (Print Screen)

3. **Analizar duración**
   - ¿Cuánto dura el evento? (30 ms? 100 ms? 1 s?)
   - Comprueba en la lista de eventos (abajo derecha)

4. **Comparar eventos**
   - Localiza el segundo evento
   - ¿Es igual al primero? ¿Duración similar?
   - Toma otra captura

### Paso 2.3: Anotaciones

**En tu cuaderno, anota:**

```
ANÁLISIS DE CAPTURA ORIGINAL
════════════════════════════

Archivo: ________________________________
Duración: ________________________________

EVENTOS DETECTADOS:
┌──────┬─────────┬──────────┬─────────────┐
│ Nº   │ Inicio  │ Duración │ Potencia    │
├──────┼─────────┼──────────┼─────────────┤
│ 1    │ 10.25 s │ 1.234 s  │ -15.3 dBm   │
│ 2    │ 20.48 s │ 1.198 s  │ -14.8 dBm   │
│ 3    │         │          │             │
└──────┴─────────┴──────────┴─────────────┘

CARACTERÍSTICAS DEL ESPECTRO:
├─ Banda principal: ________________ MHz
├─ Ancho: _________________________ kHz
├─ Potencia media: ________________ dBm
└─ Ruido de fondo: _______________ dBm

OBSERVACIONES:
_________________________________________________
_________________________________________________
_________________________________________________
```

✅ **Checkpoint:** Captura analizada y documentada

---

## 📡 PARTE 3: REPRODUCCIÓN CON HACKRF (30 minutos)

### Paso 3.1: Preparar Reproducción

**VERIFICACIÓN CRÍTICA DE SEGURIDAD:**

- [ ] ¿Antena HackRF está aislada? (no apunta fuera)
- [ ] ¿Laboratorio cerrado?
- [ ] ¿Supervisor presente?
- [ ] ¿Puerta con aviso "No entrar — Transmisión RF"?

**SI ALGUNO ES NO, DETENER AQUÍ**

---

### Paso 3.2: Reproducir Archivo

```bash
# Comando de reproducción
hackrf_transfer -t capture_20261031_134500.iq8 \
    -f 433920000 \
    -s 2000000 \
    -p 1 \
    -a 1

# Explicación de parámetros:
# -t archivo.iq8    → Transmitir este archivo
# -f 433920000      → Frecuencia: 433.92 MHz
# -s 2000000        → Sample rate: 2 millones/segundo
# -p 1              → Potencia máxima (~20 dBm)
# -a 1              → Amplificador activado
```

**Salida esperada:**

```
Transmitting, press Ctrl+C to stop
Actual frequency: 433.920000 MHz
[*] 2000000 Hz sample rate
[*] Actual TX gain: 47 dB
TX: 56.32 Mb/s  (480000000 bytes / 8.51 seconds)

[✓] TX completed successfully
```

### Paso 3.3: Observaciones Durante Transmisión

**Mientras HackRF está transmitiendo (8-10 segundos):**

- ¿Oyes algo? (es normal, no hay sonido audible a 433 MHz)
- ¿Se calienta el dispositivo? (normal, es pequeño)
- ¿Hay indicadores LED? (LED rojo/verde parpadea)

**Notas:**

```
Transmisión iniciada a: _______________
Duración esperada: 8-10 segundos
Finalización: _______________

Observaciones:
_________________________________________________
_________________________________________________
```

✅ **Checkpoint:** Archivo reproducido exitosamente

---

## 📥 PARTE 4: RECAPTURA CON RTL-SDR (20 minutos)

### Paso 4.1: Capturar la Reproducción

**EN RASPBERRY PI (o segundo portátil con RTL-SDR):**

```bash
# Conectar RTL-SDR
ssh pi@192.168.1.100
cd ~/rf_capture

# Ejecutar captura
./iq_capture.sh 120 captures/

# Responder a las preguntas:
# ¿Comenzar captura? s
# (Mientras captura, que alguien ejecute la reproducción con HackRF)

# Resultado:
# [✓] Archivo guardado: captures/capture_20261031_150000.iq8
```

**TIMING:**
- Inicia captura en RPi
- Espera 5 segundos (para estabilizar)
- Ejecuta reproducción HackRF
- Permite que la captura continúe 10 segundos más

### Paso 4.2: Descargar Captura Reproducida

```bash
# Desde portátil
scp pi@192.168.1.100:~/rf_capture/captures/capture_20261031_150000.iq8 ./

# Renombrar para distinguir
mv capture_20261031_150000.iq8 capture_reproducida.iq8
```

✅ **Checkpoint:** Tienes dos archivos:
- `capture_20261031_134500.iq8` (original)
- `capture_reproducida.iq8` (reproducida con HackRF)

---

## 🔍 PARTE 5: COMPARACIÓN (30 minutos)

### Paso 5.1: Ejecutar Comparador

```bash
# Comparar ambas capturas lado a lado
python3 rf_capture_comparator.py \
    capture_20261031_134500.iq8 \
    capture_reproducida.iq8 \
    --report comparacion_original_vs_reproducida.txt

# Salida:
# [✓] Cargada: capture_20261031_134500 (120.0s, 7 eventos)
# [✓] Cargada: capture_reproducida (120.0s, 7 eventos)
# 
# [*] Comparando 2 capturas...
# [✓] Gráfico guardado (6 paneles)
# [✓] Reporte guardado: comparacion_original_vs_reproducida.txt
```

### Paso 5.2: Interpretar Gráficos

**Se generan 6 gráficos comparativos:**

```
┌──────────────────────────────────────────────┐
│ [1] POTENCIA SUPERPUESTA                     │
│     ├─ Azul (original) vs Verde (reproducida)
│     └─ ¿Son idénticas o hay diferencias?     │
├──────────────────────────────────────────────┤
│ [2] TABLA ESTADÍSTICA                        │
│     ├─ Media, Min, Max, Duración, Eventos   │
│     └─ ¿Qué valores cambiaron?               │
├──────────────────────────────────────────────┤
│ [3-4] ESPECTROS COMPARADOS                   │
│     ├─ FFT de cada captura                   │
│     └─ ¿Hay diferencias frecuenciales?       │
├──────────────────────────────────────────────┤
│ [5] TIMELINE CON EVENTOS                     │
│     ├─ Líneas verticales = pulsaciones      │
│     └─ ¿Ocurren al mismo tiempo?             │
├──────────────────────────────────────────────┤
│ [6] HISTOGRAMA DE DURACIONES                 │
│     ├─ Distribución de duraciones            │
│     └─ ¿Son consistentes?                    │
└──────────────────────────────────────────────┘
```

### Paso 5.3: Leer Reporte Generado

```bash
# Abrir reporte
cat comparacion_original_vs_reproducida.txt

# O con editor
nano comparacion_original_vs_reproducida.txt
```

**El reporte contiene:**

```
╔════════════════════════════════════════════════════════════════╗
║           REPORTE DE COMPARACIÓN DE CAPTURAS RF                ║
╚════════════════════════════════════════════════════════════════╝

CAPTURA 1: capture_20261031_134500
  Duración:          120.00 segundos
  Total muestras:    240,000,000
  Eventos:           7
  
  ESTADÍSTICAS DE POTENCIA:
    Media:           -25.34 dBm
    Mediana:         -25.20 dBm
    Desv. Est.:      2.15 dB
    Mínima:          -45.20 dBm
    Máxima:          -8.70 dBm

CAPTURA 2: capture_reproducida
  Duración:          120.00 segundos
  Total muestras:    240,000,000
  Eventos:           7
  
  ESTADÍSTICAS DE POTENCIA:
    Media:           -24.56 dBm ← DIFERENCIA
    Mediana:         -24.15 dBm ← DIFERENCIA
    Desv. Est.:      2.34 dB
    Mínima:          -44.80 dBm
    Máxima:          -9.10 dBm

═════════════════════════════════════════════════════════════════
RESUMEN COMPARATIVO

Captura más fuerte:   capture_reproducida (-24.56 dBm vs -25.34 dBm)
Diferencia de potencia: +0.78 dB

Más eventos:          Ambas igual (7 eventos)

CONCLUSIÓN:
Los eventos se alinenan temporalmente. La potencia media es
ligeramente mayor en la captura reproducida (+0.78 dB), posiblemente
debido a amplificación de HackRF o ruido ambiental reducido.
La fidelidad de reproducción es ALTA.
```

### Paso 5.4: Análisis en Profundidad

**Preguntas a responder:**

1. **¿Son idénticas las potencias?**
   - Media original: _____ dBm
   - Media reproducida: _____ dBm
   - Diferencia: _____ dB
   - ¿Es significativa? (>1 dB = SÍ)

2. **¿Se perdió algo en la reproducción?**
   - Eventos originales: _____ 
   - Eventos reproducidos: _____
   - ¿Falta alguno?

3. **¿Hay ruido adicional?**
   - Desv. Est. original: _____ dB
   - Desv. Est. reproducida: _____ dB
   - ¿Aumentó?

4. **¿Cómo se defiende contra falsificaciones?**
   - ¿Solo con potencia?
   - ¿Necesita validar timing?
   - ¿Código rolling?

---

## 📝 PARTE 6: EJERCICIO DE COMPARACIÓN

### Ejercicio 6.1: "Detecta la Falsificación"

**Tendrás 3 capturas:**

1. `original.iq8` — Captura genuina original
2. `reproducida.iq8` — Reproducida por HackRF (esta sesión)
3. `falsificada.iq8` — Sintetizada digitalmente (ejemplo)

**Tu tarea:**
```bash
python3 rf_capture_comparator.py original.iq8 reproducida.iq8 falsificada.iq8 \
    --report analisis_falsificacion.txt

# Analiza y responde:
# ① ¿Cuál es la falsificada?
# ② ¿Qué métrica la delata? (potencia, timing, espectro)
# ③ ¿Cuánta diferencia hay? (dB, ms, etc.)
# ④ ¿Cómo la validarías automáticamente?
```

### Ejercicio 6.2: Propuesta de Defensa

**Escribe una propuesta de seguridad:**

```
PROPUESTA DE DEFENSA CONTRA FALSIFICACIONES
════════════════════════════════════════════

Mi sistema RF debe validar:

1. POTENCIA
   └─ Rango aceptable: _____ a _____ dBm
   └─ Si <MIN o >MAX → Rechazar

2. TIMING
   └─ Duración esperada: _____ ms (±10%)
   └─ Si fuera de rango → Rechazar

3. ESPECTRO
   └─ Banda esperada: _____ MHz
   └─ Si fuera → Rechazar

4. RUIDO
   └─ Desv. Est. esperada: _____ dB
   └─ Si >máximo → Rechazar

5. CÓDIGO ROLLING (BONUS)
   └─ Cada transmisión debe tener código diferente
   └─ Validar contra base de datos de códigos vistos
   └─ Si repetida → Rechazar (replay attack)

CONCLUSIÓN:
_________________________________________________
_________________________________________________
_________________________________________________
```

---

## ✅ CHECKLIST POST-PRÁCTICA

**AL TERMINAR, VERIFICAR:**

- [ ] HackRF desconectado y almacenado
- [ ] RTL-SDR desconectado y almacenado
- [ ] Todos los archivos .iq8 guardados en carpeta
- [ ] Reportes generados y guardados (.txt)
- [ ] Capturas de pantalla guardadas (PNG)
- [ ] Cuaderno completado con anotaciones
- [ ] Ejercicio de falsificación completado
- [ ] Propuesta de defensa escrita

**Archivos esperados en carpeta:**
```
├─ capture_original.iq8
├─ capture_reproducida.iq8
├─ comparacion_original_vs_reproducida.txt
├─ analisis_falsificacion.txt
├─ screenshot_evento1.png
├─ screenshot_evento2.png
├─ cuaderno_anotaciones.txt
└─ propuesta_defensa.md
```

---

## 📊 RÚBRICA DE EVALUACIÓN

| Aspecto | Excelente (5) | Bien (4) | Aceptable (3) | Insuficiente (<3) |
|---------|---------------|---------|---------------|--------------------|
| **Reproducción HackRF** | Sin errores, transmisión completa | 1 reintento | Múltiples intentos | No funciona |
| **Análisis Original** | 5+ eventos identificados, anotaciones detalladas | 3-4 eventos, anotaciones claras | 2 eventos, anotaciones básicas | <2 eventos |
| **Comparación** | Diferencias cuantificadas (dB, ms) | Diferencias identificadas | Observaciones vagas | Sin análisis |
| **Ejercicio Falsificación** | Correctamente identificada + método descrito | Correctamente identificada | Identificación dudosa | No resuelto |
| **Propuesta Defensa** | 5+ métodos, realista, implementable | 4 métodos, realista | 3 métodos, básica | <3 métodos |
| **Documentación** | Completa, limpia, con gráficos | Completa, fácil de leer | Incompleta pero legible | Falta contenido |

---

## 🤔 PREGUNTAS FRECUENTES

**P: ¿Puedo transmitir fuera del laboratorio?**
R: ❌ NO. Está prohibido. Solo en laboratorio cerrado bajo supervisión.

**P: ¿Por qué la reproducción tiene potencia diferente?**
R: HackRF suma amplificación (+47 dB TX VGA) y puede haber ruido ambiental. Normal.

**P: ¿Se puede detectar un replay attack?**
R: SÍ. Si el sistema usa código rolling o timestamp. Por eso es importante.

**P: ¿Qué pasa si me equivoco al reproducir?**
R: Presiona Ctrl+C para detener. Reinicia desde el paso 3.2.

**P: ¿Cuánto se calienta HackRF?**
R: Bastante después de 5+ minutos. Esperado. Deja enfriar 10 min entre transmisiones.

**P: ¿Necesito tomar gráficos en cada paso?**
R: Sí. Son evidencia para el reporte final.

---

## 📚 REFERENCIAS

- [06_QUE_ES_HACKRF_EXPLICACION.md](06_QUE_ES_HACKRF_EXPLICACION.md) — Conceptos
- [README_SCRIPTS.md](../scripts/README_SCRIPTS.md) — Referencia de scripts
- `hackrf_interactive.py` — Manual interactivo
- `rf_capture_comparator.py` — Manual comparador

---

## 📋 PLANTILLA DE REPORTE FINAL

**Entregar documento PDF o Word con:**

1. **Portada**
   - Nombre, grupo, fecha
   - Título: "Práctica HackRF One — Reproducción y Validación RF"

2. **Objetivos** (copia de arriba + personal)

3. **Metodología**
   - Equipos usados
   - Pasos realizados
   - Problemas encontrados

4. **Resultados**
   - Capturas de pantalla (5-10 imágenes)
   - Gráficos comparativos
   - Tabla de eventos

5. **Análisis**
   - Respuestas a las 4 preguntas (Sección 5.4)
   - Interpretación de resultados
   - Conclusiones sobre fidelidad

6. **Ejercicio Falsificación**
   - Cuál detectaste
   - Por qué
   - Método de validación

7. **Propuesta Defensa**
   - Tu diseño de seguridad
   - Métodos específicos
   - Justificación técnica

8. **Anexos**
   - Reportes .txt generados
   - Archivos .iq8 usados (tamaño, duración)
   - Cualquier script modificado

**Longitud:** 5-10 páginas  
**Fecha entrega:** 1 semana después de la sesión

---

**¡Éxito en tu práctica! 🚀**

Recuerda: La seguridad RF es sobre capas. Una onda capturada genuina tiene propiedades que una falsificada no puede replicar fácilmente.
