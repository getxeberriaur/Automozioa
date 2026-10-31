# 🚀 DESPLIEGUE DE HERRAMIENTAS HACKRF — Guía Paso a Paso

## 📋 Tabla de Contenidos

1. **Verificación previa del sistema**
2. **Instalación de libhackrf (librería base)**
3. **Instalación de hackrf_transfer y herramientas CLI**
4. **Configuración de permisos y udev**
5. **Verificación de la instalación**
6. **Instalación de Python tools**
7. **Troubleshooting**

---

## 1️⃣ VERIFICACIÓN PREVIA DEL SISTEMA

### Paso 1.1: ¿Qué sistema operativo tienes?

```bash
# Ver tu SO
uname -s

# Salidas posibles:
# Linux    → Usa apt install
# Darwin   → Usa brew install
# MINGW64  → WSL2 en Windows
```

### Paso 1.2: ¿Es de 64 bits?

```bash
uname -m
# x86_64  → 64 bits ✅
# arm64   → 64 bits ARM ✅
# armv7l  → 32 bits ARM (no recomendado)
```

### Paso 1.3: ¿Tienes permisos sudo?

```bash
sudo whoami
# root → ✅ Tienes permisos
```

---

## 2️⃣ OPCIÓN A: UBUNTU/DEBIAN (La Más Recomendada)

### Instalación Rápida (Una Línea)

```bash
sudo apt update && sudo apt install -y hackrf libhackrf-dev libhackrf0
```

**Desglose:**
- `apt update` → Actualiza lista de paquetes
- `hackrf` → Herramientas CLI (hackrf_transfer, hackrf_info, etc.)
- `libhackrf-dev` → Headers para compilar aplicaciones
- `libhackrf0` → Librería runtime

### Instalación Paso a Paso

```bash
# Paso 1: Actualizar repositorios
sudo apt update

# Paso 2: Instalar paquetes
sudo apt install -y \
  hackrf \
  libhackrf-dev \
  libhackrf0 \
  libusb-1.0-0 \
  libusb-1.0-0-dev

# Paso 3: Verificar
hackrf_info
```

### ¿Qué cada paquete?

| Paquete | Función |
|---------|---------|
| `hackrf` | **CLI tools** — hackrf_transfer, hackrf_info |
| `libhackrf0` | **Runtime library** — Necesaria para ejecutar |
| `libhackrf-dev` | **Development headers** — Para compilar |
| `libusb-1.0-0` | **USB library** — Comunicación con HackRF |
| `libusb-1.0-0-dev` | **USB dev headers** — Para compilar |

---

## 3️⃣ OPCIÓN B: macOS (con Homebrew)

### Instalación Rápida

```bash
brew install hackrf
```

### Instalación Manual (si no tienes Homebrew)

```bash
# Paso 1: Instalar Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Paso 2: Instalar HackRF
brew install hackrf

# Paso 3: Verificar
hackrf_info
```

---

## 4️⃣ OPCIÓN C: DESDE FUENTE (Compilación)

**Usa esto si:**
- Tu distro no tiene paquete precompilado
- Necesitas una versión más reciente
- Estás en ARM (Raspberry Pi, etc.)

### Paso 1: Instalar dependencias

```bash
# Linux
sudo apt install -y \
  build-essential \
  cmake \
  git \
  libusb-1.0-0 \
  libusb-1.0-0-dev

# macOS
brew install cmake libusb
```

### Paso 2: Clonar repositorio

```bash
cd ~/tmp
git clone https://github.com/greatscottgadgets/hackrf.git
cd hackrf/host
```

### Paso 3: Compilar e instalar

```bash
# Crear directorio de compilación
mkdir build
cd build

# Compilar
cmake ..
make -j$(nproc)

# Instalar (requiere sudo)
sudo make install

# Actualizar librería cache
sudo ldconfig
```

### Paso 4: Verificar

```bash
hackrf_info
```

---

## 5️⃣ CONFIGURACIÓN DE PERMISOS (IMPORTANTE)

### Problema

```bash
# Si ejecutas sin sudo, ves:
hackrf_info

# Error:
# hackrf_open() failed: LIBUSB_ERROR_ACCESS (-3)
# Did you mean 'sudo hackrf_info'?
```

### Solución: Crear Reglas udev

```bash
# Crear archivo de reglas
sudo nano /etc/udev/rules.d/99-hackrf.rules

# Agregar estas líneas:
# HackRF One (r9 and later)
SUBSYSTEM=="usb", ATTRS{idVendor}=="1d50", ATTRS{idProduct}=="604b", MODE="0666"

# HackRF One (r8 and earlier)
SUBSYSTEM=="usb", ATTRS{idVendor}=="1d50", ATTRS{idProduct}=="6045", MODE="0666"

# Guardar: Ctrl+O, Enter, Ctrl+X
```

### Aplicar Reglas

```bash
# Opción 1: Recargar udev (sin desconectar)
sudo udevadm control --reload
sudo udevadm trigger

# Opción 2: Reiniciar (más seguro)
sudo reboot
```

### Verificar que Funciona

```bash
# Desconecta y reconecta HackRF

# Prueba SIN sudo
hackrf_info

# Si ves el output, ¡éxito! ✅
```

---

## 6️⃣ VERIFICACIÓN COMPLETA DE LA INSTALACIÓN

### Test 1: Herramientas CLI

```bash
# Mostrar versión
hackrf_info --version

# Listar todos los comandos disponibles
hackrf_info
hackrf_transfer --help
hackrf_sweep --help
hackrf_debug --help
hackrf_spiflash --help
```

### Test 2: Conexión HackRF

```bash
# **CONECTA HackRF ONE AL USB PRIMERO**

# Mostrar información detallada
hackrf_info

# Salida esperada:
# ╔════════════════════════════════════════════════════════════╗
# ║               HackRF One r9                               ║
# ╠════════════════════════════════════════════════════════════╣
# ║ Serial Number: 0000000000000000YYYYYYYYYY                ║
# ║ Board ID Code: 0x04 (HackRF One)                         ║
# ║ Firmware Version: 2022.09.1                               ║
# ║ Part ID Number: 0xa000c21b 0x00634d44                    ║
# ║                 0x00000000 0x00000000                     ║
# ║ USB Bus Speed: High Speed                                 ║
# ║ USB D+ Pullup: False                                      ║
# ║ Clock Source: Internal                                    ║
# ║ Baseband Filter Bandwidth Setting: 1750000 Hz             ║
# ║ LNA Gain: 0 dB (max 40 dB)                               ║
# ║ VGA Gain: 0 dB (max 62 dB)                               ║
# ║ TX VGA Gain: 47 dB (max 47 dB)                           ║
# ╚════════════════════════════════════════════════════════════╝
```

### Test 3: Prueba de Transmisión (Segura)

```bash
# SOLO EN LABORATORIO CONTROLADO
# Crear archivo de prueba silencioso (sin transmitir realmente)

# Mostrar ayuda de hackrf_transfer
hackrf_transfer -h

# Comando típico:
# hackrf_transfer -t archivo.iq8 -f 433920000 -s 2000000 -p 1 -a 1
#
# -t = transmitir (archivo de entrada)
# -f = frecuencia (433.92 MHz = 433920000 Hz)
# -s = sample rate (2 MHz = 2000000)
# -p = power level (1 = máximo, ~20 dBm)
# -a = amplificador (1 = activado)
```

---

## 7️⃣ INSTALACIÓN DE PYTHON TOOLS

Los scripts de análisis requieren Python + librerías:

### Paso 1: Python 3.7+

```bash
python3 --version
# Python 3.10.x ✅
# Si no lo tienes:
sudo apt install python3 python3-pip python3-venv
```

### Paso 2: Crear Entorno Virtual (Recomendado)

```bash
# En tu carpeta de trabajo
cd ~/rf_analysis

# Crear venv
python3 -m venv venv

# Activar
source venv/bin/activate
# O en Windows:
# venv\Scripts\activate

# Verificar (ves prefijo `(venv)`)
which python
```

### Paso 3: Instalar Dependencias Python

```bash
# Asegurate de estar en el venv

# Opción A: Instalación individual
pip install numpy scipy matplotlib scikit-dsp-comm

# Opción B: Desde archivo requirements.txt
cat > requirements.txt << 'EOF'
numpy>=1.21.0
scipy>=1.7.0
matplotlib>=3.4.0
scikit-dsp-comm>=0.7.0
EOF

pip install -r requirements.txt
```

### Paso 4: Verificar Imports

```bash
python3 << 'EOF'
import numpy as np
import scipy.signal
import matplotlib.pyplot as plt
print("✅ Todas las librerías importan correctamente")
EOF
```

---

## 8️⃣ INSTALACIÓN DE SCRIPTS DE ANÁLISIS

### Paso 1: Descargar Scripts

```bash
# Opción A: Desde GitHub
cd ~/rf_analysis/scripts
git clone https://github.com/tu_usuario/RF_Lab_Seguro.git
cd RF_Lab_Seguro/scripts

# Opción B: Copiar manualmente
cp hackrf_interactive.py ~/rf_analysis/scripts/
cp rf_capture_comparator.py ~/rf_analysis/scripts/
```

### Paso 2: Hacer Scripts Ejecutables

```bash
chmod +x ~/rf_analysis/scripts/*.py
```

### Paso 3: Crear Alias (Opcional)

```bash
# Agregar a ~/.bashrc
echo "alias hackrf_viz='python3 ~/rf_analysis/scripts/hackrf_interactive.py'" >> ~/.bashrc
source ~/.bashrc

# Ahora puedes usar:
hackrf_viz mi_captura.iq8
```

---

## 9️⃣ TROUBLESHOOTING

### Problema 1: `hackrf_info` dice "No device found"

```bash
# Causa: HackRF no detectado

# Soluciones:
1. ¿Está conectado al USB? Verifica con:
   lsusb | grep HackRF

2. ¿Necesita permisos udev? Ejecuta:
   sudo hackrf_info
   
   Si funciona con sudo pero no sin sudo:
   sudo chown $USER:$USER /dev/bus/usb/*/

3. ¿Firmware corrupto? Reprograma:
   hackrf_spiflash --write hackrf_one_usb.bin

4. ¿Otro proceso lo usa? Cierra:
   sudo lsof | grep hackrf
   kill -9 <PID>
```

### Problema 2: `Permission denied` sin ser root

```bash
# Causa: Reglas udev no aplicadas correctamente

# Soluciones:
1. Agregar usuario a grupo `plugdev`:
   sudo usermod -a -G plugdev $USER
   
   # Reinicia sesión o usa:
   su - $USER

2. Crear mejor regla udev:
   sudo nano /etc/udev/rules.d/99-hackrf.rules
   
   # Agregar:
   SUBSYSTEM=="usb", ATTRS{idVendor}=="1d50", \
   ATTRS{idProduct}=="604b", GROUP="plugdev", MODE="0660"
   
   # Recargar:
   sudo udevadm control --reload
   sudo udevadm trigger
```

### Problema 3: `libusb_open() failed: LIBUSB_ERROR_ACCESS`

```bash
# Causa: Permisos insuficientes (necesitas sudo)

# Soluciones rápidas:
sudo hackrf_info          # Usa sudo temporalmente

# Solución permanente:
# Ver Problema 2 arriba
```

### Problema 4: Importar `pyusb` falla en scripts Python

```bash
# Causa: Librería Python USB no instalada

pip install pyusb
```

### Problema 5: Errores de compilación desde fuente

```bash
# Si ves "CMake not found":
sudo apt install cmake

# Si ves "libusb-1.0-0-dev not found":
sudo apt install libusb-1.0-0-dev

# Si ves "gcc: command not found":
sudo apt install build-essential

# Luego reintenta:
cd ~/tmp/hackrf/host/build
cmake ..
make -j$(nproc)
sudo make install
```

---

## 🔟 GUÍA RÁPIDA POR SISTEMA

### 🐧 UBUNTU/DEBIAN

```bash
# TODO EN UNA LÍNEA
sudo apt update && \
sudo apt install -y hackrf libhackrf-dev libhackrf0 && \
sudo nano /etc/udev/rules.d/99-hackrf.rules && \
# (Agrega las reglas udev) && \
sudo udevadm control --reload && \
sudo udevadm trigger && \
hackrf_info

# Tiempo: 3-5 minutos
```

### 🍎 macOS

```bash
# TODO EN UNA LÍNEA
brew install hackrf && hackrf_info

# Tiempo: 2-3 minutos
# Nota: macOS no necesita reglas udev
```

### 🪟 WSL2 (Windows Subsystem for Linux)

```bash
# En WSL2 (Ubuntu 20.04+)
sudo apt update && \
sudo apt install -y hackrf libhackrf-dev libhackrf0

# Nota: Si HackRF no se detecta en WSL2:
# Usa USBIPD para pasar dispositivo desde Windows
# https://github.com/dorssel/usbipd-win
```

### 🍓 RASPBERRY PI (ARM)

```bash
# En Raspberry Pi OS (Debian-based)
# Requiere compilación desde fuente (tarda más)

# Opción rápida (si hay paquete precompilado):
sudo apt install hackrf

# Opción compilación manual (tarda 20-30 min):
cd ~/tmp
git clone https://github.com/greatscottgadgets/hackrf.git
cd hackrf/host
mkdir build && cd build
cmake ..
make -j4  # (4 = número de núcleos)
sudo make install
sudo ldconfig
```

---

## 1️⃣1️⃣ CHECKLIST FINAL

### ✅ Verificar Instalación Completa

```bash
# Test 1: ¿Está instalado?
which hackrf_info
# Debe mostrar: /usr/bin/hackrf_info o similar

# Test 2: ¿Qué versión?
hackrf_info --version

# Test 3: ¿Se detecta el hardware?
hackrf_info
# Debe mostrar: "HackRF One r9"

# Test 4: ¿Puedo usar sin sudo?
hackrf_info 2>&1 | grep -q "HackRF" && echo "✅ OK" || echo "❌ Permisos"

# Test 5: ¿Python está listo?
python3 -c "import numpy, scipy, matplotlib; print('✅ Python OK')"

# Test 6: ¿Scripts de análisis están?
ls ~/rf_analysis/scripts/hackrf_*.py
```

### Checklist

- [ ] `hackrf_info` muestra dispositivo
- [ ] No necesito `sudo` para ejecutar
- [ ] `hackrf_transfer --help` funciona
- [ ] Python 3.7+ instalado
- [ ] numpy, scipy, matplotlib instalados
- [ ] Scripts hackrf_*.py descargados
- [ ] Puedo ejecutar: `python3 hackrf_interactive.py archivo.iq8`

---

## 1️⃣2️⃣ PRÓXIMOS PASOS

Una vez desplegado, puedes:

1. **Probar visualización:**
   ```bash
   python3 hackrf_interactive.py tu_captura.iq8
   ```

2. **Probar comparación:**
   ```bash
   python3 rf_capture_comparator.py cap1.iq8 cap2.iq8
   ```

3. **Probar reproducción (EN LABORATORIO):**
   ```bash
   hackrf_transfer -t tu_captura.iq8 -f 433920000 -s 2000000 -p 1 -a 1
   ```

4. **Seguir la práctica completa:**
   Consulta `07_PRACTICA_HACKRF_REPRODUCCION.md`

---

## 📞 SOPORTE Y REFERENCIAS

- **Documentación oficial:** https://github.com/greatscottgadgets/hackrf/wiki
- **Foro:** https://github.com/greatscottgadgets/hackrf/discussions
- **Issues:** https://github.com/greatscottgadgets/hackrf/issues
- **Comunidad:** https://greatscottgadgets.com/

---

**¿Completaste todos los pasos? ¡Ahora estás listo para la Práctica HackRF!** 🎉
