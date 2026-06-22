# Laboratorio RF Seguro — Análisis Espectral de Sistemas de Acceso Remoto

**Especialización:** Ciberseguridad en Automoción  
**Duración:** 4-5 horas (teórica + práctica)  
**Nivel:** Intermedio-Avanzado

---

## 📌 Descripción General

Este laboratorio pedagógico proporciona una introducción segura y legal a la captura y análisis de señales de radiofrecuencia (RF) en la banda 433 MHz, frecuencia común en sistemas de acceso remoto de vehículos.

**Objetivo educativo:**
Comprender cómo se transmiten y detectan señales RF, visualizar su espectro, registrar eventos de pulsación y analizar sus características, sin realizar replay, jamming ni interferencias activas.

---

## 🎯 Competencias Alcanzadas

Al completar este laboratorio, los alumnos podrán:

1. ✅ Identificar componentes y topología de un sistema RF de captura pasiva.
2. ✅ Configurar Raspberry Pi + RTL-SDR para análisis espectral.
3. ✅ Capturar y registrar datos de potencia en banda ISM 433 MHz.
4. ✅ Detectar automáticamente eventos de pulsación en datos RF.
5. ✅ Visualizar espectrogramas y correlacionar eventos temporal-espectrales.
6. ✅ Identificar vulnerabilidades y proponer mitigaciones en sistemas RKE/PKES.
7. ✅ Debatir defensa en profundidad en arquitectura de vehículos conectados.

---

## 📂 Estructura del Material

```
RF_Lab_Seguro/
├── README.md (este archivo)
├── docs/
│   ├── 00_GUIA_MONTAJE_GENERAL.md      ← Inicio aquí
│   ├── 01_GUIA_RASPBERRY.md             ← Instalación RPi+RTL-SDR
│   ├── 02_GUIA_PORTATIL.md              ← Análisis en portátil
│   ├── 03_PROCEDIMIENTO_CAPTURA.md      ← Paso a paso práctico
│   └── 04_ETICA_Y_SEGURIDAD.md          ← Límites legales/éticos
├── scripts/
│   ├── spectrum_capture.sh              ← Script captura en RPi
│   ├── analyze_spectrum.py              ← Análisis en portátil
│   └── event_detector.py                ← Detección automática de eventos
└── templates/
    ├── INFORME_ALUMNOS.md               ← Plantilla de laboratorio
    └── CHECKLIST_SEGURIDAD.md           ← Checklist pre/post captura
```

---

## 🚀 Inicio Rápido (5 minutos)

1. **Profesor:** Revisar [00_GUIA_MONTAJE_GENERAL.md](docs/00_GUIA_MONTAJE_GENERAL.md)
2. **Alumnos:** Seguir [03_PROCEDIMIENTO_CAPTURA.md](docs/03_PROCEDIMIENTO_CAPTURA.md)
3. **Análisis:** Usar scripts en `scripts/analyze_spectrum.py`
4. **Informe:** Completar plantilla en `templates/INFORME_ALUMNOS.md`

---

## 🔧 Material Necesario

| Cantidad | Componente | Especificación |
|---|---|---|
| 1 | Raspberry Pi | Pi 4 o 5 (2GB mín) |
| 1 | RTL-SDR Dongle | RTL2832U |
| 1 | Mando RF | 433.92 MHz, código fijo, aislado |
| 1 | Portátil | Linux/macOS/Win+WSL2 |
| 2 | Antenas dipolo | 433 MHz (improvisables) |
| 1 | Fuente 5V | Para RPi |

**Costo aproximado:** €40-60 (si no tiene RPi)

---

## 📋 Plan de Sesión (4 horas)

| Bloque | Duración | Contenido |
|---|---|---|
| 1. Intro teórica | 30 min | RF, espectro, vulnerabilidades en RKE |
| 2. Montaje HW | 30 min | Conectar RTL-SDR, verificar drivers |
| 3. Captura pasiva | 60 min | Baseline + pulsaciones del mando |
| 4. Análisis | 60 min | Gráficos, detección de eventos, debate |
| 5. Documentación | 30 min | Informe y conclusiones |

---

## ⚠️ Límites Éticos y Legales

### ✅ PERMITIDO
- Capturar espectro pasivamente (solo lectura).
- Registrar pulsaciones de emisor propio aislado.
- Medir frecuencia, duración, potencia.
- Analizar y graficar datos.
- Discutir mitigaciones defensivas.

### ❌ PROHIBIDO
- Capturar/reproducir señales de llave real.
- Intentar abrir/cerrar el receptor conectado.
- Usar jamming o interferencia activa.
- Transmitir sin licencia.
- Replicar o clonar señales.

**Responsable:** Profesor supervisa equipos, antenas y emisores.

---

## 📖 Flujo Recomendado de Lectura

### Para Profesores:
1. Este README
2. [00_GUIA_MONTAJE_GENERAL.md](docs/00_GUIA_MONTAJE_GENERAL.md) — Visión completa
3. [04_ETICA_Y_SEGURIDAD.md](docs/04_ETICA_Y_SEGURIDAD.md) — Límites críticos
4. [03_PROCEDIMIENTO_CAPTURA.md](docs/03_PROCEDIMIENTO_CAPTURA.md) — Para explicar pasos

### Para Alumnos:
1. Resumen de [00_GUIA_MONTAJE_GENERAL.md](docs/00_GUIA_MONTAJE_GENERAL.md) (primeros 10 min)
2. Seguir exactamente [03_PROCEDIMIENTO_CAPTURA.md](docs/03_PROCEDIMIENTO_CAPTURA.md)
3. Completar plantilla en [templates/INFORME_ALUMNOS.md](templates/INFORME_ALUMNOS.md)

---

## 🛠️ Requisitos Técnicos Mínimos

### Software:
- **Raspberry Pi:** Raspberry Pi OS Lite (bullseye+)
- **Portátil:** Linux (Ubuntu 20.04+), macOS 11+, o Windows 10+ con WSL2
- **Python 3.8+** con matplotlib, pandas, numpy, scipy

### Red:
- WiFi o Ethernet entre RPi y portátil
- SSH habilitado en RPi

### Espacio:
- RPi: ~200 MB (instalación + datos)
- Portátil: ~500 MB (análisis)

---

## 📊 Resultados Esperados

Tras completar el laboratorio, los alumnos obtendrán:

1. **Gráfico de espectro promedio** — Pico en ~433.92 MHz
2. **Espectrograma temporal** — Mapa de potencia vs frecuencia vs tiempo
3. **Detección automática de eventos** — ~8-10 pulsaciones marcadas
4. **Informe de análisis** — Con conclusiones pedagógicas
5. **Propuestas de mitigación** — 5+ defensas aplicables

---

## 🐛 Soporte Rápido

### ¿RTL-SDR no aparece?
```bash
# En RPi
lsusb
rtl_test -t
```

### ¿No hay señal en gráficos?
- Verificar antena (longitud ~34 cm para 433 MHz)
- Acercar mando a ~50 cm
- Aumentar ganancia en scripts

### ¿Portátil no ve RPi?
```bash
# Test de red
ping 192.168.1.100  # (sustituir IP)
ssh pi@192.168.1.100
```

---

## 📚 Referencias Adicionales

**Papers académicos** (búsqueda recomendada):
- "Rolling Code Security in Car Keyfobs" — Hoppe & Kiltz (2008)
- "Replay Attacks on Passive Keyless Entry" — García et al. (2015)
- "RF Security and SDR Fundamentals" — NIST, IEEE 802.15.4

**Herramientas complementarias:**
- GNU Radio Companion (visualización en tiempo real)
- Wireshark (protocolo de captura)
- MATLAB/Octave (análisis avanzado)

---

## 📞 Preguntas Frecuentes

**¿Puedo hacerlo con un coche real?**
No. Este laboratorio solo funciona con mandos aislados sin conexión física. Cualquier intento sobre un vehículo real es ilegal.

**¿Puedo capturar y reproducir la señal?**
No. La reproducción está prohibida. Solo captura pasiva y análisis defensivo.

**¿Es legal hacer esto en clase?**
Sí, siempre que sea captura pasiva (sin transmisión ni jamming) y bajo supervisión docente.

---

## 🔗 Conexiones con Otros Módulos

Este laboratorio es complementario a:
- **CANbus_ICSim_Ciber** — Análisis de bus interno del vehículo
- **CTF_Automotive** — Retos de seguridad en automoción

---

## ✍️ Autoría y Versión

**Versión:** 1.0  
**Fecha:** Junio 2026  
**Actualización:** RF_Lab_Seguro integrado en Automozioa  
**Licencia:** CC BY-NC-SA 4.0 (Uso educativo)

---

## 📋 Checklist de Profesor (Antes de Clase)

- [ ] Revisar guías de montaje (docs/)
- [ ] Preparar RPi y RTL-SDR (verificar con rtl_test)
- [ ] Cargar mando de prueba (pilas nuevas)
- [ ] Verificar conectividad RPi-Portátil (SSH)
- [ ] Probar script de captura (`spectrum_capture.sh`)
- [ ] Instalar dependencias Python en portátil
- [ ] Descargar plantilla de informe
- [ ] Revisar límites éticos con alumnos

---

**¿Preguntas?** Consulta las guías específicas o el troubleshooting en cada documento.

