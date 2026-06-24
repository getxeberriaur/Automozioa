# 🚀 INICIO RÁPIDO — RF_Lab_Seguro

**Bienvenido al Laboratorio de Análisis RF Seguro.**

Este documento te guía en 5 minutos para entender qué tienes y cómo empezar.

---

## 📦 ¿Qué Tienes?

```
RF_Lab_Seguro/
├── README.md                    ← Descripción completa
├── docs/                        ← LEER PRIMERO
│   ├── 00_GUIA_MONTAJE_GENERAL.md      ← Visión general (START HERE)
│   ├── 01_GUIA_RASPBERRY.md            ← Instalar RPi+RTL-SDR
│   ├── 02_GUIA_PORTATIL.md             ← Instalar análisis
│   ├── 03_PROCEDIMIENTO_CAPTURA.md     ← Pasos prácticos
│   ├── 04_ETICA_Y_SEGURIDAD.md         ← LECTURA OBLIGATORIA
│   └── 05_INTEGRACION_HACKRF_ONE.md    ← NUEVO: Reproducción con HackRF
├── scripts/                     ← HERRAMIENTAS
│   ├── spectrum_capture.sh              ← Captura espectral en RPi
│   ├── iq_capture.sh                    ← NUEVO: Captura IQ en RPi
│   ├── analyze_spectrum.py              ← Análisis en portátil
│   └── hackrf_playback.py               ← NUEVO: Reproducción/análisis HackRF
└── templates/                   ← PLANTILLAS
    ├── INFORME_ALUMNOS.md               ← Para lab reports
    └── CHECKLIST_SEGURIDAD.md           ← Para supervisión
```

---

## ⏱️ Ruta de 5 Minutos

1. **Tú (Profesor):**
   - Abre: `docs/00_GUIA_MONTAJE_GENERAL.md`
   - Lee los primeros 10 minutos para entender hardware
   - Luego: `docs/04_ETICA_Y_SEGURIDAD.md` (CRÍTICO)

2. **Tus Alumnos:**
   - Leer: `docs/03_PROCEDIMIENTO_CAPTURA.md`
   - Seguir paso a paso
   - Completar: `templates/INFORME_ALUMNOS.md`

3. **Supervisión:**
   - Usar: `templates/CHECKLIST_SEGURIDAD.md`
   - Antes, durante y después de cada sesión

4. **Con HackRF One (Opcional):**
   - Leer: `docs/05_INTEGRACION_HACKRF_ONE.md`
   - Ejecutar captura IQ en RPi: `./scripts/iq_capture.sh`
   - Reproducir/visualizar en portátil: `python3 ./scripts/hackrf_playback.py`

---

## 🎯 Flujo Principal

```
ANTES DE CLASE
  ↓
1. Preparación (30 min)
   └─ Leer 00_GUIA_MONTAJE_GENERAL.md
   └─ Verificar hardware (docs/01 + 02)
   └─ Revisar ética (docs/04)
  ↓
2. EN CLASE (120 min)
   ├─ Explicar límites éticos (alumnos firman)
   ├─ Seguir: docs/03_PROCEDIMIENTO_CAPTURA.md
   ├─ Ejecutar: scripts/spectrum_capture.sh (RPi)     ← Opción A: CSV espectral
   │                          O
   │           scripts/iq_capture.sh (RPi)            ← Opción B: IQ para HackRF
   ├─ Analizar: scripts/analyze_spectrum.py (Portátil) ← Para Opción A
   │                     O
   │           scripts/hackrf_playback.py (Portátil)   ← Para Opción B
   └─ Generar gráficos y eventos
  ↓
3. DESPUÉS (30 min)
   ├─ Completar: templates/INFORME_ALUMNOS.md
   ├─ Verificar: templates/CHECKLIST_SEGURIDAD.md
   └─ Guardar equipo bajo llave
```

---

## 🔧 Requisitos Mínimos

| Componente | Necesario | Opcional |
|---|---|---|
| **Raspberry Pi 4/5** | Sí (2GB RAM) | - |
| **RTL-SDR Dongle** | Sí (433 MHz) | - |
| **Mando RF aislado** | Sí (433.92 MHz) | - |
| **Python 3.8+** | Sí | - |
| **Portátil** | Sí (análisis) | - |
| **HackRF One** | - | ✅ Para Opción B |

**Presupuesto:** €60-100 (sin contar portátil ni HackRF)

---

## 📚 Lectura Obligatoria (En Orden)

1. **PRIMERO:** `docs/00_GUIA_MONTAJE_GENERAL.md` (20 min)
   → Visión general de la práctica

2. **LUEGO:** `docs/04_ETICA_Y_SEGURIDAD.md` (15 min)
   → Límites legales, CRÍTICO para profesores

3. **PARA INSTALAR:**
   - `docs/01_GUIA_RASPBERRY.md` (30 min)
   - `docs/02_GUIA_PORTATIL.md` (20 min)

4. **PARA EJECUTAR:** `docs/03_PROCEDIMIENTO_CAPTURA.md` (durante clase)

5. **SI TIENES HACKRF:** `docs/05_INTEGRACION_HACKRF_ONE.md` (análisis avanzado)

---

## ⚡ Comandos Rápidos

### En Raspberry Pi

```bash
# Verificar RTL-SDR
rtl_test -t

# Capturar espectro 120 segundos
./scripts/spectrum_capture.sh 120

# Resultado: archivo CSV en ~/rf_capture/
```

### En Portátil

```bash
# Analizar CSV descargado
python3 scripts/analyze_spectrum.py data/spectrum_*.csv

# Resultado: gráficos en plots/
```

---

## 🛑 Si Algo Falla

| Problema | Solución |
|---|---|
| RTL-SDR no aparece | Ver troubleshooting en `docs/01_GUIA_RASPBERRY.md` |
| Python sin librerías | `pip install matplotlib pandas numpy scipy` |
| SSH sin acceso | Verificar IP RPi, contraseña, firewall |
| Gráficos sin datos | Verificar CSV no está vacío, aumentar duración captura |

---

## 🎓 Estructura de la Clase Recomendada

### Sesión 1 (4-5 horas)

```
30 min | Intro teórica (RF, ISM, vulnerabilidades, defensa)
30 min | Montaje hardware (RTL-SDR, antenas)
60 min | Captura pasiva (baseline + pulsaciones del mando)
60 min | Análisis (gráficos, detección de eventos)
30 min | Debate sobre mitigaciones
```

### Sesión 2 (opcional, 3 horas)

```
30 min | Repaso de resultados
60 min | Captura avanzada (con interferencia simulada)
90 min | Análisis profundo y escritura de informe
```

---

## ✅ Pre-Checklist del Profesor

Antes de la PRIMERA clase, completar esto:

- [ ] He leído `docs/00_GUIA_MONTAJE_GENERAL.md`
- [ ] He leído `docs/04_ETICA_Y_SEGURIDAD.md` completamente
- [ ] He verificado que `rtl_test -t` funciona en RPi
- [ ] He probado `spectrum_capture.sh` en RPi
- [ ] He descargado CSV y corrido `analyze_spectrum.py` en portátil
- [ ] He obtenido aprobación ética del centro
- [ ] He impreso `templates/CHECKLIST_SEGURIDAD.md`
- [ ] He impreso `templates/INFORME_ALUMNOS.md`
- [ ] He grabado mis límites éticos en un guion

---

## 📞 Preguntas Frecuentes

**P: ¿Puedo usar este material para clases online?**  
R: Sí, pero la captura práctica requiere presencia (no remota).

**P: ¿Qué pasa si un alumno intenta hacer jamming?**  
R: Parada inmediata, confiscación, reporte a dirección.

**P: ¿Puedo capturar un coche real?**  
R: No. Esto no es una práctica sobre coches reales, solo equipos de prueba aislados.

**P: ¿Está permitido por ley?**  
R: Sí, si es captura pasiva bajo supervisión en contexto académico. Consulta autoridades locales.

---

## 🔗 Estructura en GitHub

Este material está en:  
`https://github.com/getxeberriaur/Automozioa/tree/main/RF_Lab_Seguro`

Para actualizar:
```bash
cd Automozioa/
git pull origin main
cp -r RF_Lab_Seguro ~/RF_Lab_Seguro_latest/
```

---

## 🎯 Próximos Pasos

**Ahora:**
1. Lee `docs/00_GUIA_MONTAJE_GENERAL.md` (20 min)
2. Lee `docs/04_ETICA_Y_SEGURIDAD.md` (15 min)

**Semana que viene:**
1. Instala según `docs/01_GUIA_RASPBERRY.md` y `docs/02_GUIA_PORTATIL.md`
2. Prueba scripts con datos de ejemplo
3. Prepara la primera clase

**En clase:**
1. Alumnos firman declaración ética
2. Seguir `docs/03_PROCEDIMIENTO_CAPTURA.md`
3. Completan `templates/INFORME_ALUMNOS.md`

---

## 💡 Consejo Final

> **La seguridad en este laboratorio no es opcional.**  
> Tu reputación profesional y la del centro dependen de que estos límites se respeten.  
> Si tienes dudas, pregunta primero. Siempre.

---

**¿Listo? → Abre `docs/00_GUIA_MONTAJE_GENERAL.md` ahora.** 🚀

