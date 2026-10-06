# Guía Completa de Montaje: Laboratorio RF Seguro

## 📌 Resumen Ejecutivo

Este laboratorio permite capturar y analizar señales de radiofrecuencia (RF) en 433 MHz de forma pasiva y segura. No se realiza jamming, replay, ni interferencia activa.

**Tiempo de preparación:** 30-60 minutos  
**Tiempo de práctica:** 2-3 horas  
**Equipos recomendados:** Grupos de 3-4 alumnos

---

## 🎯 Topología del Laboratorio

```
┌──────────────────────────────────────┐
│  AULA CERRADA Y CONTROLADA           │
├──────────────────────────────────────┤
│                                      │
│  [Mando RF 433 MHz]                  │
│       │ Emisor aislado               │
│       ↓ Pulsación manual             │
│                                      │
│  [Raspberry Pi 4/5]                  │
│  ├─ RTL-SDR USB                      │
│  ├─ Python 3.9+                      │
│  └─ Scripts de captura               │
│       │                              │
│       │ Datos CSV/IQ                 │
│       │ (Wifi/Ethernet)              │
│       ↓                              │
│  [Portátil]                          │
│  ├─ Python + Matplotlib              │
│  ├─ GNU Radio (opcional)             │
│  └─ Jupyter Notebook                 │
│                                      │
└──────────────────────────────────────┘
```

---

## 🔧 Material Necesario

| Componente | Especificación | Cantidad | Precio aprox |
|---|---|---|---|
| **Raspberry Pi** | Pi 4B (2GB) o Pi 5 | 1 | €30-50 |
| **RTL-SDR Dongle** | RTL2832U genérico | 1 | €20-30 |
| **Mando RF** | 433.92 MHz, código fijo | 1 | €10-20 |
| **Receptor RF** | Relé 10A (sin cargar) | 1 (ref) | €5-15 |
| **Antenas** | Dipolo 433 MHz | 2 | €2-5 (improvisables) |
| **Cables/USB** | Micro-USB, Ethernet | - | €5-10 |
| **Fuente 5V** | Para RPi | 1 | Disponible |

**Total:** €60-130 (sin contar portátil)

---

## 📋 Bloque 1: Introducción Teórica (30 minutos)

### Conceptos Clave

**1. Radiofrecuencia (RF)**
- Onda electromagnética en rango 3 kHz - 300 GHz
- Usada en comunicaciones inalámbricas

**2. Banda ISM 433 MHz**
- Industria, Científico, Médico
- Europa: 433.05-434.79 MHz
- Libre para uso con potencia <10 dBm
- Común en: mandos, puertas, persianas, garageras

**3. Modulación ASK/OOK**
- Amplitude Shift Keying
- On-Off Keying
- Alternar presencia/ausencia de señal para codificar bits

**4. Rolling Code vs Fixed Code**
- **Fixed:** Mismo código cada pulsación (vulnerable a replay)
- **Rolling:** Código diferente cada vez (más seguro)

### Vulnerabilidades Conocidas

**RollJam / Lock Relay:** 
- Bloquear (jam) pulsación real
- Capturar siguiente código
- Reproducir primer código capturado
- ⚠️ Esta práctica NO implementa esto (pedagogía defensiva)

---

## 🛠️ Bloque 2: Montaje Hardware (30 minutos)

### Paso 2.1: Verificar Componentes

Checklist:
- [ ] Raspberry Pi con alimentación 5V
- [ ] Tarjeta microSD con Raspberry Pi OS Lite instalado
- [ ] RTL-SDR dongle sin daños físicos
- [ ] Mando RF con pilas nuevas
- [ ] Antenas/cables de conexión
- [ ] Cable Ethernet o WiFi configurada

### Paso 2.2: Conectar RTL-SDR a Raspberry Pi

1. Insertar dongle RTL-SDR en puerto USB de RPi
2. Conectar antena dipolo al conector SMA del dongle
   - Longitud recomendada para 433 MHz: **34 cm** (λ/4)
   - O improvisada: cable de ~34 cm conectado a pin central

3. Verificar detección:
   ```bash
   lsusb | grep Realtek
   ```
   Resultado esperado:
   ```
   Bus 001 Device 005: ID 0bda:2832 Realtek Semiconductor Corp. RTL2832U
   ```

### Paso 2.3: Test de Hardware

```bash
rtl_test -t
```

Salida esperada:
```
Found 1 device(s):
  0:  Realtek, RTL2832U, SN: 00000001

Using device 0: Realtek RTL2832U
...
[R82XX] PLL not locked!
Test passed
```

---

## 📚 Bloque 3: Instalación de Software (30 minutos)

### En Raspberry Pi

**3.1: Actualizar sistema**
```bash
sudo apt update && sudo apt upgrade -y
```

**3.2: Instalar rtl-sdr y herramientas**
```bash
sudo apt install -y rtl-sdr librtlsdr0 librtlsdr-dev build-essential pkg-config
```

**3.3: Instalar Python y dependencias**
```bash
sudo apt install -y python3-pip python3-numpy python3-scipy
pip3 install --upgrade pip
pip3 install matplotlib pandas scipy
```

**3.4: Crear carpeta de trabajo**
```bash
mkdir -p ~/rf_capture
cd ~/rf_capture
```

**3.5: Copiar scripts** (descargar desde repo)
```bash
wget https://github.com/getxeberriaur/Automozioa/raw/main/RF_Lab_Seguro/scripts/spectrum_capture.sh
chmod +x spectrum_capture.sh
```

### En Portátil (Linux/macOS)

**Python y librerías:**
```bash
python3 -m venv rf-env
source rf-env/bin/activate
pip install matplotlib pandas numpy scipy jupyter
```

**Para Windows (WSL2):**
```bash
# En terminal WSL2
sudo apt update && sudo apt install -y python3-pip
pip3 install matplotlib pandas numpy scipy
```

---

## 🧪 Bloque 4: Verificación Pre-Práctica (10 minutos)

### En Raspberry Pi

```bash
# Test 1: Dongle conectado
lsusb | grep Realtek && echo "✓ RTL-SDR detectado"

# Test 2: librtlsdr funcional
rtl_test -t && echo "✓ Hardware OK"

# Test 3: Captura básica (5 segundos)
rtl_fm -f 433.92M -g 40 -s 200k - | head -c 1000000 > /dev/null && echo "✓ Captura OK"

# Test 4: Acceso SSH
hostname -I && echo "✓ IP disponible para SSH"
```

---

## 🔐 Bloque 5: Consideraciones de Seguridad (CRÍTICO)

### ✅ Permitido
- Capturar espectro pasivamente (solo lectura)
- Registrar pulsaciones de emisor propio aislado
- Medir frecuencia, duración, potencia
- Analizar datos estadísticamente
- Discutir mitigaciones defensivas

### ❌ Prohibido Explícitamente
- Capturar y reproducir (replay) una señal real
- Intentar activar el receptor conectado
- Transmitir sin licencia en 433 MHz
- Usar jamming o interferencia deliberada
- Trabajar fuera de la aula

### Responsabilidades
- **Profesor:** Supervisar equipos, antenas, emisor. Revisar límites éticos
- **Alumnos:** Firmar declaración de compromisos antes de empezar
- **Centro:** Asegurar seguridad física, almacenamiento de equipos

---

## 📋 Bloque 6: Checklist Pre-Sesión del Profesor

**Una semana antes:**
- [ ] Leer documentación completa
- [ ] Revisar límites éticos con dirección
- [ ] Recibir aprobación institucional

**Un día antes:**
- [ ] Verificar RPi + RTL-SDR con `rtl_test -t`
- [ ] Comprobar mando de prueba (pilas nuevas)
- [ ] Probar captura: `./spectrum_capture.sh`
- [ ] Verificar SSH entre RPi y portátil
- [ ] Instalar Python/dependencias en portátil

**Al comenzar la clase:**
- [ ] Alumnos leen y firman declaración de ética
- [ ] Explicar topología y límites
- [ ] Distribuir guía paso a paso (03_PROCEDIMIENTO_CAPTURA.md)
- [ ] Asignar grupos (3-4 alumnos/grupo)

---

## 🎓 Objetivos Pedagógicos Alcanzables

Al completar este montaje, los alumnos comprenderán:

1. ✅ Componentes de un sistema de análisis RF
2. ✅ Diferencia entre captura pasiva y activa (transmisión)
3. ✅ Limitaciones legales en frecuencias ISM
4. ✅ Fundamentos de modulación digital en banda ISM
5. ✅ Importancia de la autenticación vs captura/replay

---

## 📞 Troubleshooting Inicial

| Problema | Causa | Solución |
|---|---|---|
| `lsusb` no muestra RTL-SDR | USB no conectado o defectuoso | Probar otro puerto, reiniciar RPi |
| `rtl_test` cuelga | Permiso de USB | `sudo usermod -a -G plugdev pi` y reiniciar |
| No hay red RPi-Portátil | Wifi no configurada | Configurar SSID/contraseña en RPi |
| SSH rechaza conexión | SSH no habilitado | `sudo systemctl enable ssh && sudo systemctl start ssh` |

---

## 🚀 Siguiente Paso

Una vez verificado todo, pasar a:
→ **[03_PROCEDIMIENTO_CAPTURA.md](03_PROCEDIMIENTO_CAPTURA.md)** (Ejecución práctica)

