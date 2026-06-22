# Procedimiento de Captura: Paso a Paso

**Duración total:** 90-120 minutos  
**Personas por grupo:** 3-4 alumnos  
**Supervisor:** Profesor presente en todo momento

---

## 📋 Checklist Pre-Captura (5 minutos)

ANTES de empezar, verificar:

**Hardware:**
- [ ] Raspberry Pi encendida y accesible por SSH
- [ ] RTL-SDR conectado al USB
- [ ] Antena conectada a RTL-SDR
- [ ] Mando de prueba con pilas nuevas
- [ ] Receptor RF aislado (sin cargar/conectar a nada)

**Software:**
- [ ] `rtl_test -t` ejecuta correctamente en RPi
- [ ] Portátil conectado a WiFi/Ethernet
- [ ] SSH desde portátil a RPi funciona
- [ ] Carpeta `~/rf_capture/` existe en RPi
- [ ] Script `spectrum_capture.sh` es ejecutable

**Seguridad:**
- [ ] Profesor supervisa equipo
- [ ] Mando solo será usado dentro del aula
- [ ] Receptor no conectado a instalación real
- [ ] Alumnos comprenden límites éticos

---

## FASE 1: Captura Base (Sin Emisor) — 20 minutos

### Objetivo
Registrar "ruido de fondo" para comparación posterior.

### Procedimiento

**Paso 1.1:** Abrir SSH a RPi desde portátil
```bash
ssh pi@192.168.1.100
# Ingresar contraseña

cd ~/rf_capture
```

**Paso 1.2:** Iniciar captura de 60 segundos SIN pulsar el mando
```bash
./spectrum_capture.sh
```

O manualmente:
```bash
rtl_power -f 433M:434M:50k -g 40 -i 1 -e 60s baseline_no_tx.csv
```

**¿Qué ocurre?**
- Barrido de 433-434 MHz (rango 1 MHz)
- Bins de 50 kHz cada uno (~20 bins)
- Ganancia 40 (nivel medio-alto)
- Duración 60 segundos
- Crea archivo: `baseline_no_tx.csv`

**Esperar a que termine (~60 segundos)**

**Salida esperada:**
```
[*] Sampling rate: 2.048e+06 [Hz]
[*] Antenna: Dipole
[*] Bins: 20, Span: 1.000 MHz
[*] Elapsed time: 60.00 sec
[✓] CSV creado: baseline_no_tx.csv
```

---

## FASE 2: Captura con Pulsaciones — 45 minutos

### Objetivo
Registrar eventos reales de pulsación del mando de prueba.

### Procedimiento

**Paso 2.1:** Iniciar captura larga (120 segundos)
```bash
rtl_power -f 433M:434M:50k -g 40 -i 1 -e 120s captures/mando_pulsaciones.csv
```

**Paso 2.2:** Cronograma de pulsaciones

```
Timeline durante la captura:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  0-10s   | Capturando RUIDO (sin pulsar)
 10-11s   | ⚠️ PULSA BOTÓN 1 del mando (mantener 1-2 segundos)
 11-17s   | Esperar sin hacer nada
 17-18s   | PULSA BOTÓN 1 (1-2 segundos)
 18-25s   | Esperar
 25-26s   | PULSA BOTÓN 1
 26-33s   | Esperar
 33-34s   | PULSA BOTÓN 1
 34-41s   | Esperar
 41-42s   | PULSA BOTÓN 1
 42-49s   | Esperar
 49-50s   | PULSA BOTÓN 1
 50-57s   | Esperar
 57-58s   | PULSA BOTÓN 1
 58-120s  | Captura continúa (sin pulsar más)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**IMPORTANTE:**
- Mantener mando a **~50 cm** de antena
- Pulsar con claridad (sin accidentes)
- Espaciar eventos **al menos 7 segundos**
- Total objetivo: **7-8 pulsaciones bien separadas**

**Durante la espera:** Anotar en papel la hora exacta de cada pulsación para validación posterior.

**Ejemplo de anotaciones:**
```
10:42:15 → Pulsa 1
10:42:22 → Pulsa 2
10:42:29 → Pulsa 3
...
```

---

## FASE 3: Captura Avanzada (Opcional) — 20 minutos

### Con Ruido Simulado

**Objetivo:** Comparar detección con interferencia ambiental.

**Procedimiento:**

**Paso 3.1:** Iniciar nueva captura
```bash
rtl_power -f 433M:434M:50k -g 40 -i 1 -e 120s captures/con_ruido_ambiente.csv
```

**Paso 3.2:** Mientras se captura, DURANTE 30-40 segundos, generar ruido:
- Prender microondas
- Enciende WiFi nearby (smartphone)
- Luces LED parpadeantes

**Paso 3.3:** Continuar con pulsaciones normales

**Resultado esperado:**
- Base de ruido elevada durante interferencia
- Pulsaciones aún detectables (resiliencia)
- Diferencia clara antes/después de interferencia

---

## FASE 4: Transferencia de Datos — 10 minutos

### Descargar CSVs desde RPi

**Método A: SCP desde portátil (más rápido)**
```bash
# Desde portátil
mkdir -p ~/rf-analysis/data
cd ~/rf-analysis/data

scp pi@192.168.1.100:~/rf_capture/*.csv .

# Listar archivos descargados
ls -lh
```

**Método B: SSH interactivo**
```bash
ssh pi@192.168.1.100
ls ~/rf_capture/
# Copiar manualmente cada archivo
```

**Salida esperada:**
```
-rw-r--r--  baseline_no_tx.csv
-rw-r--r--  mando_pulsaciones.csv
-rw-r--r--  con_ruido_ambiente.csv (si se hizo FASE 3)
```

---

## FASE 5: Análisis en Portátil — 30 minutos

### Instalación de Herramientas

Si aún no lo hiciste: [02_GUIA_PORTATIL.md](02_GUIA_PORTATIL.md)

### Análisis Básico

```bash
cd ~/rf-analysis
source venv/bin/activate  # Si tienes entorno virtual

# Analizar captura sin emisor
python3 scripts/analyze_spectrum.py data/baseline_no_tx.csv
```

**Salida esperada:**
```
[✓] CSV cargado: 2000 filas, 3605 columnas
[*] Rango de potencia: -90.5 a -85.2 dBm
[*] Eventos detectados: 0
[✓] Gráfico guardado: plots/spectrum_baseline_no_tx.png
```

### Análisis de Pulsaciones

```bash
python3 scripts/analyze_spectrum.py data/mando_pulsaciones.csv
```

**Salida esperada:**
```
[✓] CSV cargado: 3000 filas, 3605 columnas
[*] Rango de potencia: -90.5 a -45.2 dBm
[*] Eventos detectados: 7
    E1: t=125-135s, P_max=-47.8 dBm, dur=10s
    E2: t=245-256s, P_max=-46.5 dBm, dur=11s
    E3: t=365-375s, P_max=-48.1 dBm, dur=10s
    E4: t=485-495s, P_max=-47.5 dBm, dur=10s
    E5: t=605-615s, P_max=-48.3 dBm, dur=10s
    E6: t=725-735s, P_max=-47.9 dBm, dur=10s
    E7: t=845-855s, P_max=-48.0 dBm, dur=10s
[✓] Gráfico guardado: plots/spectrum_mando_pulsaciones.png
[✓] Gráfico de eventos: plots/events_mando_pulsaciones.png
```

---

## FASE 6: Interpretación de Gráficos

### Gráfico 1: Espectro Promedio

```
Espectro promedio de una pulsación (baseline vs con transmisión):

         Baseline (sin tx)      Mando (con tx)
Potencia   -85  ║ -45
  (dBm)         ║
                ║    ____
                ║   /    \
             ___║__/      \___
                ║433.5 433.92 434 MHz
```

**Interpretación:**
- Pico en ~433.92 MHz → **Frecuencia central del mando**
- Diferencia: ~40 dB entre baseline y pulsación
- Forma estrecha (±500 kHz) → **Transmisión ASK/OOK**

### Gráfico 2: Eventos Detectados (Timeline)

```
Potencia vs Tiempo:

     -40 dBm   ╔═╗         ╔═╗         ╔═╗
               ║ ║         ║ ║         ║ ║  ← Pulsaciones detectadas
     -50 dBm   ║ ║ ╔═╗     ║ ║         ║ ║
               ╨═╨ ║ ║ ╔═╗ ╨═╨ ╔═╗ ╔═╗ ╨═╨
     -60 dBm       ╨═╨ ║ ║     ║ ║ ║ ║
                       ╨═╨ ╔═╗ ╨═╨ ╨═╨
     -70 dBm             ║ ║
                         ╨═╨
     -80 dBm  ═════════════════════════════════
         0s       20s      40s      60s      80s
```

**Interpretación:**
- Rectángulos rojos = eventos automáticamente detectados
- Espaciado regular = patrón consistente de pulsaciones
- Duración típica = 10-15 segundos (largo para una pulsación)
  - *(Nota: cada "evento" incluye todo el tiempo de transmisión)*

### Gráfico 3: Espectrograma (Opcional)

```
Tiempo →
     0  10  20  30  40  50  60  70  80  90  100
 434┤■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
 433.92┤░░░░■■■■■■■░░░░░░░░■■■■■■■░░░░░░░░░■■■■
 433.5┤■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
↑
Frecuencia
  ■ = Potencia alta (-45 dBm)
  ░ = Potencia media (-60 dBm)
    = Potencia baja (-90 dBm)
```

**Interpretación:**
- Bandas oscuras = actividad transmitida
- Ubicación en 433.92 MHz = frecuencia central confirmada
- Patrón pulsante = eventos bien separados

---

## FASE 7: Análisis Detallado (30 minutos)

### Preguntas Clave para Responder

1. **Frecuencia central:** ¿A qué frecuencia exacta transmite el mando?
2. **Ancho de banda:** ¿Qué rango de frecuencias ocupa la transmisión?
3. **Duración:** ¿Cuántos segundos dura cada pulsación?
4. **Potencia:** ¿Cuál es la potencia máxima en dBm?
5. **Periodicidad:** ¿Hay patrón en los tiempos de pulsación?
6. **Ruido:** ¿Cambia la línea base con interferencia?
7. **Detectabilidad:** ¿Se diferencia claramente evento vs ruido?

### Tabla de Resultados

Completar durante el análisis:

| Parámetro | Valor Observado | Esperado | Notas |
|---|---|---|---|
| Frecuencia central | \_\_\_ MHz | 433.92 MHz | ±100 kHz |
| Ancho de banda | \_\_\_ kHz | ~500 kHz | Depende modulación |
| Duración evento | \_\_\_ s | 10-15 s | Por evento |
| Potencia máxima | \_\_\_ dBm | -40 a -50 dBm | A 50 cm antena |
| Eventos detectados | \_\_\_ | 7-8 | Según pulsaciones |
| SNR (Signal/Noise) | \_\_\_ dB | >20 dB | Diferencia pico/base |

---

## FASE 8: Informe (30 minutos)

### Completar Plantilla

Usar: [templates/INFORME_ALUMNOS.md](../templates/INFORME_ALUMNOS.md)

**Secciones obligatorias:**
1. Portada (grupo, fecha, profesor)
2. Objetivos (qué buscaban)
3. Metodología (qué hicieron)
4. Resultados (tabla de datos + gráficos)
5. Análisis (interpretación de gráficos)
6. Conclusiones (qué aprendieron)
7. Vulnerabilidades identificadas
8. Mitigaciones propuestas

---

## 🎯 Preguntas de Debate Posterior (20 minutos)

1. ¿Por qué se elige 433 MHz para mandos de puertas/garajes?
2. ¿Cómo se diferencia un "rolling code" de un "fixed code" en análisis RF?
3. Si alguien capturara esta señal, ¿podría reproducirla? ¿Por qué no en esta práctica?
4. ¿Qué defensa implementarían para detectar si alguien intenta capturar?
5. ¿Cómo se protegen los vehículos modernos contra replay attacks?
6. ¿Es posible hacer jamming en 433 MHz? ¿Consecuencias?
7. ¿Qué papel juega la autenticación criptográfica?

---

## ✅ Checklist Post-Captura

- [ ] Todos los CSVs descargados a portátil
- [ ] Scripts de análisis ejecutados sin errores
- [ ] Gráficos PNG generados en `plots/`
- [ ] Tabla de resultados completada
- [ ] Informe escrito y revisado
- [ ] Preguntas de debate respondidas
- [ ] Equipo devuelto en buen estado
- [ ] Profesor validó límites éticos

---

## 📞 Troubleshooting Durante Captura

| Síntoma | Causa | Solución |
|---|---|---|
| `rtl_power` cuelga | Dongle sin inicializar | `rtl_test -t` primero |
| CSV vacío (0 bytes) | Permisos o espacio disco | `df -h`, `chmod 777 ~/rf_capture` |
| Potencia -100 dBm (muy baja) | Mando lejano o antena deficiente | Acercar mando, verificar antena |
| Línea plana (sin eventos) | Mando sin pilas o no pulsando | Probar en receptor de prueba |
| Ruido muy alto (-30 dBm) | Interferencia RF ambiental | Cambiar ubicación, alejarse de WiFi |
| SCP falla | SSH sin acceso | Verificar IP, usuario, contraseña |

---

## 📈 Resultados Típicos

**Captura exitosa debería mostrar:**
- ✅ Pico espectral en 433.92 ± 0.1 MHz
- ✅ 7-10 eventos detectados automáticamente
- ✅ SNR (signal-to-noise) > 20 dB
- ✅ Duración consistente (±10% entre eventos)
- ✅ Ausencia de eventos en captura baseline
- ✅ Diferencia visible con ruido ambiental

**Si no ves esto:** Revisar troubleshooting y repetir captura.

---

## ⏭️ Siguientes Pasos

→ Completar [Informe de Alumnos](../templates/INFORME_ALUMNOS.md)  
→ Leer [Consideraciones Éticas](04_ETICA_Y_SEGURIDAD.md)  
→ Debate en clase sobre mitigaciones

