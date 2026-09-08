# Práctica TPMS: Resumen Ejecutivo

## 1. QUÉ ES TPMS Y POR QUÉ ES VULNERABLE

### Sistema TPMS (Tire Pressure Monitoring System)
- **Función:** Monitorizar presión de neumáticos en tiempo real
- **Componentes:** Sensor de presión en cada rueda + receptor en vehículo
- **Comunicación:** RF inalámbrica (radiofrecuencia) — **sin cifrado en modelos antiguos**
- **Frecuencias:** 
  - 315 MHz (USA, Japón)
  - 433 MHz (Europa, algunos modelos)
  - 868 MHz (algunos modelos específicos)

### Vulnerabilidades conocidas
| CVE/Referencia | Ataque | Impacto |
|---|---|---|
| CVE-2021-24148 | Replay de mensaje TPMS | Falsificar presión de neumático |
| Research Palo Alto (2013) | Captura + inyección | Hacer creer al vehículo que hay pinchazo |
| General Motors (2014) | Rolling ID débil | Reproducir mensajes sin sincronización |

**Impacto real:** Un conductor que confía en TPMS ignora neumáticos desinflados → accidente

---

## 2. ESTRUCTURA DE LA PRÁCTICA (Día 3, bloque de 1.5-2 horas)

### FASE 1: Teoría + Captura (30 min)

**Teoría (10 min):**
- Cómo funciona sensor TPMS (batería, frecuencia, mensaje)
- Estructura de trama TPMS: [ID_sensor][Presión_PSI][Temperatura][Checksum]
- Por qué no hay cifrado: histórico (2006+), bajo coste, batería limitada
- Estándares: ISO 13849, SAE J2951

**Demostración (20 min):**
```bash
# En terminal proyectado, el docente:

# 1. Enchufar RTL-SDR al ordenador
# 2. Abrir inspectrum (herramienta visualización espectro)
# 3. Sintonizar frecuencia 315/433 MHz (según región)
# 4. Presionar sensor TPMS en mano
#    → Observar pulso de RF en pantalla

# Terminal esperado:
$ rtl_fm -M wbfm -f 315M -s 200000 | xxd
# (Se ven bytes crudos transmitidos por sensor)
```

**Objetivo:** "Vimos la transmisión real de un sensor"

---

### FASE 2: Captura y Análisis (40 min)

**Captura de mensajes reales:**

```bash
# Script: capturar varios mensajes TPMS

# 1. Escuchar con RTL-SDR durante 60 segundos
rtl_433 -f 315M -f 433M -X "n:TPMS:questionable" 2>/dev/null > tpms_capture.log

# Salida esperada (JSON):
{
  "time": "2026-09-08T10:15:23Z",
  "model": "TPMS-Generic",
  "id": "a1b2c3d4",
  "pressure_kpa": 215,
  "temperature": 22,
  "signal": -60
}
```

**Análisis de estructura:**

```python
# Script Python: parse_tpms.py
import json

with open('tpms_capture.log') as f:
    for line in f:
        try:
            msg = json.loads(line)
            sensor_id = msg['id']
            pressure = msg['pressure_kpa']
            
            print(f"Sensor {sensor_id}:")
            print(f"  Presión: {pressure} kPa (~{pressure*0.145:.1f} PSI)")
            print(f"  Señal: {msg['signal']} dBm (fuerza de RF)")
        except: pass
```

**Resultados observados:**
- Identificar IDs de los 4 sensores del vehículo
- Ver cómo cambia presión si se aprieta/calienta sensor
- Observar fuerza de señal (RSSI)

**Objetivo:** "Entendemos la estructura del mensaje, sin cifrado visible"

---

### FASE 3: Ataque Replay (30 min)

**Grabación de mensaje válido:**

```bash
# Capturar UN ÚNICO mensaje limpio (sin ruido)
# Opción A: Con RTL-SDR + GNU Radio Companion (visual)
# Opción B: Con script rtl_fm + demodulación

# Resultado: fichero binario "tpms_sensor_id_a1b2c3d4.bin" (50-100 bytes)
```

**Inyección de mensaje (replay attack):**

```python
# Script: tpms_replay.py
# Usando HackRF o USRP (si tienes)

import sys
from gnuradio import gr, blocks, analog, filter
from osmosdr import source, sink

# 1. Leer fichero guardado
with open('tpms_sensor_id_a1b2c3d4.bin', 'rb') as f:
    captured_signal = f.read()

# 2. Modular en frecuencia 315 MHz
# 3. Inyectar por aire (transmitir)

# Pseudocódigo:
tx = sink(device="hackrf=0", freq=315e6, gain=47, samp_rate=2e6)
tx.work(captured_signal)
# → Se escucha beep en sensor si está en rango (5-10m)
```

**Variantes de ataque:**

| Ataque | Técnica | Observación |
|---|---|---|
| **Replay puro** | Repetir mensaje capturado cada 30s | Vehículo ve presión congelada |
| **Modificación presión** | Cambiar 1-2 bytes del mensaje | Posible si no hay checksum fuerte |
| **Rolling ID** | Algunos TPMS usan ID que cambia cada transmisión | Imposible repetir exactamente |
| **Jamming** | Inyectar ruido en 315/433 MHz | Vehículo ve "no data" en ese sensor |

**Resultado en vehículo:**
- Testigo TPMS se enciende (falsa alarma)
- O presión queda "congelada" en lecturas anteriores
- O desaparece ese sensor del panel

**Objetivo:** "Logramos engañar al sistema de seguridad del vehículo"

---

### FASE 4: Contramedidas y Cierre (10 min)

**¿Por qué falla el ataque en vehículos modernos?**

```
Modelo antiguo (pre-2015):       Modelo moderno (2020+):
├─ Sin cifrado                   ├─ Cifrado AES-128
├─ Checksum débil (CRC simple)   ├─ MAC (Message Authentication Code)
├─ Sin rolling ID                ├─ Rolling ID + contador
├─ Acceso libre a sensor         └─ Sensor con PIN físico
└─ → VULNERABLE                     → DEFENDIDO
```

**Estándares de seguridad:**
- NHTSA (USA): exigió cifrado en 2015+
- ISO 26262 (seguridad funcional): requiere autenticación
- UNECE R155: exige "protección contra inyección de datos"

**Conexión con Día 3 completo:**
- TPMS → Ejemplo real de por qué R155 es necesario
- Security Gateway → Mecanismo similar al cifrado TPMS
- CTF → Podrían tener reto de "descifrar un TPMS moderno"

---

## 3. EQUIPAMIENTO REQUERIDO

### A. Hardware (CRÍTICO)

#### Opción A1: RTL-SDR solo (captura pasiva)
```
Dispositivo: RTL-SDR v3 (RTL2832U)
├─ Costo: 20-30€
├─ Proveedor: AliExpress, Amazon, eBay
├─ Especificaciones:
│  ├─ Rango: 24 MHz - 1.7 GHz
│  ├─ Temperatura: ±25ppm
│  ├─ Conexión: USB 2.0
│  └─ Incluye antenas para 433 MHz / 315 MHz
├─ Cantidad: 1 (para docente + demostración)
└─ Funcionalidad: CAPTURA y ANÁLISIS (NO inyección)

Accesorios:
├─ Cable USB 2.0 (si no incluye)
├─ Antena dipolo para 315/433 MHz (si no incluye, costo +5€)
└─ Filtro LNA (opcional, mejora señal débil, +20€)
```

**VENTAJA:** Barato, suficiente para captura
**DESVENTAJA:** No pueden hacer inyección (ataque Fase 3)

---

#### Opción A2: HackRF One (captura + inyección) ⭐
```
Dispositivo: HackRF One
├─ Costo: 300€
├─ Proveedor: Great Scott Gadgets, Mouser
├─ Especificaciones:
│  ├─ Rango: 1 MHz - 6 GHz
│  ├─ TX + RX simultáneo (full duplex)
│  ├─ Conexión: USB
│  └─ Potencia TX: ~20 dBm (seguro, bajo riesgo legal)
├─ Cantidad: 1 (compartida en clase o por docente)
└─ Funcionalidad: CAPTURA + INYECCIÓN completa

Accesorios:
├─ Cable USB 2.0 + ferrita
├─ Antena SMA (TPMS 315 MHz)
└─ Software: GQRX, inspectrum, GNU Radio (gratis)
```

**VENTAJA:** Profesional, full funcionalidad, reutilizable
**DESVENTAJA:** Caro, requiere expertise RF

---

#### Opción A3: USRP B210 (investigación seria)
```
Dispositivo: USRP B210
├─ Costo: 1000-1200€
├─ Funcionalidad: Investigación profesional
└─ OVERKILL para curso FP/profesor
```

**NO RECOMENDADO** (presupuesto prohibitivo)

---

### B. Software (TODO GRATUITO)

| Software | Función | Instalación | SO |
|---|---|---|---|
| **rtl-sdr** | Driver + CLI tools | `apt install rtl-sdr` | Linux/Mac |
| **rtl_433** | Decodificador TPMS automático | `apt install rtl-433` | Linux |
| **inspectrum** | Visualización espectro RF | `apt install inspectrum` | Linux |
| **GQRX** | Receptor RTL-SDR GUI | Descarga sourceforge | Linux/Mac/Win |
| **GNU Radio** | Inyección + procesamiento señales | `apt install gnuradio` | Linux |
| **Python** | Scripts análisis (capture, decode) | Preinstalado | Todos |
| **Wireshark** | Análisis de tráfico RF | `apt install wireshark` | Todos |

**Setup inicial:** ~30 min (instalación + prueba RTL-SDR)

---

### C. Sensor TPMS Real (opcional pero recomendado)

| Opción | Costo | Fuente |
|---|---|---|
| Sensor TPMS usado (eBay) | 10-20€ c/u | eBay / mercado segunda mano |
| 4 sensores (juego completo) | 40-80€ | Amazon, repuestos coche |
| Activador sensor (herramienta) | 15-30€ | Amazon, tienda automoción |

**¿Por qué?** Poder demostrar en vivo que el sensor responde a cambios de presión/temperatura

**Alternativa sin sensor real:**
- Simular sensor con GNU Radio (genera onda correcta)
- O capturar vídeo de demostración previa
- Menos impactante pero funciona

---

## 4. DESGLOSE DE COSTOS

### Escenario Mínimo (RTL-SDR, sin inyección)
```
RTL-SDR v3 dongle                 €25
Antena 315/433 MHz (si falta)      €5
Sensor TPMS usado (1)              €15
─────────────────────────────────────
TOTAL:                             €45
Confiabilidad captura:             95%
Confiabilidad ataque:              30% (sin transmisión)
```

### Escenario Recomendado (HackRF)
```
HackRF One                        €300
Antenas SMA (2x)                   €20
Sensor TPMS usado (1)              €15
─────────────────────────────────────
TOTAL:                            €335
Confiabilidad captura:            99%
Confiabilidad ataque:             90%
Funcionalidad extra:              ✅ (reutilizable para RF)
```

---

## 5. TIMELINE REALISTA EN CLASE

| Tiempo | Actividad | Formato | Notas |
|---|---|---|---|
| 09:30–10:00 | Teoría TPMS + normativa | Exposición | Diapositivas |
| 10:00–10:20 | Demo captura en vivo | Proyectado | Docente + RTL-SDR |
| 10:20–11:00 | Análisis de mensajes | Hands-on | Grupos pequeños (2-3 personas) |
| 11:00–11:30 | Ataque Replay (si HackRF) | Demostrativo | Observan vehículo/sensor responder |
| 11:30–12:00 | Contramedidas + debate | Expositivo | Cómo se defiende en vehículos modernos |

**Tiempo total: 1.5 horas** ✅ Encaja en Día 3

---

## 6. RIESGOS Y MITIGACIÓN

| Riesgo | Probabilidad | Mitigación |
|---|---|---|
| RTL-SDR no captura señal | 🟡 MEDIA | Prueba 1 semana antes, ajusta ganancia (-10 a 40) |
| Interferencias RF en aula | 🟡 MEDIA | Cierra puertas, apaga WiFi cercano, usa atenuador |
| Sensor TPMS no responde | 🟡 MEDIA | Compra 2 sensores baratos, uno como backup |
| HackRF no inyecta correctamente | 🟠 BAJO | GNU Radio precalibrado, prueba antes |
| Problemas de driver en Windows | 🟠 BAJO | Usa Linux (VM VirtualBox si es necesario) |

**Preparación obligatoria:**
```
[ ] 1 semana antes: Probar RTL-SDR + capturar TPMS real
[ ] 3 días antes: Calibrar GNU Radio (si HackRF)
[ ] 1 día antes: Ensayo completo de la sesión
[ ] Día de: Tener backup (sensor extra, cable USB, antena)
```

---

## 7. ALTERNATIVA SIN HARDWARE (si falla todo)

Si el día anterior algo no funciona:

**Plan B — Análisis Forense:**
```
Opción 1: Usar logs capturados en sesión anterior
├─ Mostrar análisis Python de mensajes TPMS
├─ Identificar patrones sin hacer inyección
└─ Tiempo: 45 min, 100% confiabilidad

Opción 2: Vídeo + análisis
├─ Reproducir vídeo de demo previa
├─ Estudiantes analizan y responden preguntas
└─ Tiempo: 60 min, 100% confiabilidad
```

---

## 8. COMPARATIVA RÁPIDA: TPMS vs OTRAS OPCIONES

| Factor | TPMS | OBD-II | V2X Simulación |
|---|---|---|---|
| **Equipamiento simple** | ✅ (€45-335) | 🟡 (€10-50) | ✅ (software solo) |
| **Impacto real/visible** | ✅ Sensor responde | 🟡 Depende gateway | ✅ Vehículo simulado reacciona |
| **Confiabilidad Día 3** | 80-90% | 60-70% | 99% |
| **Prerequisitos** | RTL-SDR, antena | ELM327, puerto OBD | VEINS instalado |
| **Educación ciberseguridad** | ✅ Alto | ✅✅ Muy alto | ✅ Alto |
| **Aplicabilidad a talleres** | 🟡 Medio | ✅✅ Muy alto | 🟡 Teórico |
| **Novedad/interés profesor** | ✅ Alto | ✅ Alto | ✅✅ Muy alto (futuro) |
| **Facilidad replicar fuera curso** | ✅ Fácil | ✅ Fácil | 🟡 Medio (necesita VM) |

---

## 9. RECOMENDACIÓN FINAL

**Si tienes presupuesto (~€50-100):**
→ **TPMS con RTL-SDR** (captura + análisis)
- Factible, educativo, bajo coste
- Demo impactante (sensor responde en vivo)
- Confiabilidad 80-90%

**Si tienes presupuesto (~€350):**
→ **TPMS con HackRF** (captura + inyección completa)
- Profesional, full funcionalidad
- Ataque real (replay injection)
- Confiabilidad 95%+
- Herramienta reutilizable para otros módulos RF

**Si no tienes presupuesto:**
→ **Ir a Análisis Forense OBD o V2X Simulación**
- Software libre, 100% confiable
- Sin riesgos de hardware
