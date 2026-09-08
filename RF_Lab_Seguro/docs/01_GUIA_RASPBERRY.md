# Instalación: Raspberry Pi + RTL-SDR

**Tiempo estimado:** 30-45 minutos

---

## Requisitos Previos

- Raspberry Pi 4/5 con SD Card y Raspberry Pi OS Lite instalado
- Acceso SSH habilitado
- RTL-SDR dongle conectado y reconocido (`lsusb`)
- Conexión WiFi o Ethernet

---

## Paso 1: Actualizar Sistema

```bash
sudo apt update
sudo apt upgrade -y
sudo apt install -y git wget curl build-essential pkg-config
```

**Duración:** 10-15 minutos

---

## Paso 2: Instalar RTL-SDR

```bash
sudo apt install -y rtl-sdr librtlsdr0 librtlsdr-dev
```

**Verificar instalación:**
```bash
rtl_test -t
```

**Salida esperada:**
```
Found 1 device(s):
  0:  Realtek, RTL2832U, SN: 00000001

Using device 0: Realtek RTL2832U
...
[R82XX] PLL not locked!
Test passed
```

---

## Paso 3: Instalar Python y Dependencias

```bash
sudo apt install -y python3-dev python3-pip python3-numpy python3-scipy
pip3 install --upgrade pip
pip3 install matplotlib pandas scipy
```

---

## Paso 4: Crear Estructura de Carpetas

```bash
mkdir -p ~/rf_capture/data
mkdir -p ~/rf_capture/logs
cd ~/rf_capture
```

---

## Paso 5: Descargar Scripts de Captura

### Opción A: Desde GitHub (recomendado)

```bash
cd ~/rf_capture
wget https://github.com/getxeberriaur/Automozioa/raw/main/RF_Lab_Seguro/scripts/spectrum_capture.sh
wget https://github.com/getxeberriaur/Automozioa/raw/main/RF_Lab_Seguro/scripts/analyze_spectrum.py
chmod +x spectrum_capture.sh
```

### Opción B: Manual

Si descargas no funcionan, crear manualmente:

**Archivo:** `~/rf_capture/spectrum_capture.sh`
```bash
#!/bin/bash

FREQ_START=433.5M
FREQ_STOP=434.5M
FREQ_STEP=100k
DURATION=120
GAIN=40
OUTPUT="~/rf_capture/data/spectrum_$(date +%Y%m%d_%H%M%S).csv"

echo "[*] Capturando espectro 433.5-434.5 MHz durante ${DURATION}s..."

rtl_power -f ${FREQ_START}:${FREQ_STOP}:${FREQ_STEP} \
          -g ${GAIN} \
          -i 1 \
          -e ${DURATION}s \
          $OUTPUT

echo "[✓] Captura completada: $OUTPUT"
```

Hacer ejecutable:
```bash
chmod +x ~/rf_capture/spectrum_capture.sh
```

---

## Paso 6: Prueba de Captura

```bash
cd ~/rf_capture
./spectrum_capture.sh
```

**Resultado esperado:**
```
[*] Capturando espectro 433.5-434.5 MHz durante 120s...
[*] Sampling rate: 2.048e+06 [Hz]
[*] Bins: 10, Span: 1.000 MHz
[*] Elapsed time: 120.00 sec
[✓] Captura completada: /home/pi/rf_capture/data/spectrum_20260622_143021.csv
```

---

## Paso 7: Configurar SSH para Transferencia de Datos

Verificar que SSH está activo:
```bash
sudo systemctl status ssh
sudo systemctl enable ssh
sudo systemctl start ssh
```

Obtener IP:
```bash
ip a | grep "inet " | grep -v 127.0.0.1
```

Ejemplo de salida:
```
inet 192.168.1.100/24 brd 192.168.1.255 scope global wlan0
```

---

## Paso 8: Prueba de Conectividad (Desde Portátil)

```bash
# Desde portátil
ssh pi@192.168.1.100 "ls ~/rf_capture/data/"
```

**Salida esperada:**
```
spectrum_20260622_143021.csv
```

---

## 🧪 Verificación Final en RPi

```bash
#!/bin/bash
# Ejecutar en RPi para verificar todo está OK

echo "=== VERIFICACIÓN FINAL ==="
echo ""

echo "[1] RTL-SDR detectado:"
lsusb | grep Realtek || echo "  ✗ NO DETECTADO"

echo ""
echo "[2] Librerías rtl-sdr:"
which rtl_test && echo "  ✓ Instaladas" || echo "  ✗ NO INSTALADAS"

echo ""
echo "[3] Python y dependencias:"
python3 -c "import matplotlib, pandas, numpy; print('  ✓ OK')" || echo "  ✗ FALTA ALGO"

echo ""
echo "[4] Carpeta de trabajo:"
ls -la ~/rf_capture/ && echo "  ✓ Estructura OK" || echo "  ✗ NO EXISTE"

echo ""
echo "[5] Scripts:"
ls -la ~/rf_capture/*.sh ~/rf_capture/*.py 2>/dev/null && echo "  ✓ Descargados" || echo "  ✗ FALTA DESCARGAR"

echo ""
echo "=== FIN VERIFICACIÓN ==="
```

---

## 🐛 Troubleshooting

### RTL-SDR no aparece en `lsusb`
```bash
# Comprobar puerto USB
lsusb -v

# Reiniciar servicios USB
sudo systemctl restart usbmount
```

### Permiso denegado en USB
```bash
sudo usermod -a -G plugdev pi
# Luego reiniciar RPi
sudo reboot
```

### `rtl_test` falla o cuelga
```bash
# Instalar driver específico
sudo apt install -y libusb-1.0-0-dev
# Recompilar
git clone https://github.com/osmocom/rtl-sdr.git
cd rtl-sdr
mkdir build && cd build
cmake .. -DINSTALL_UDEV_RULES=ON
make
sudo make install
sudo ldconfig
```

### No hay espacio en SD
```bash
df -h
# Si lleno, eliminar logs antiguos
rm ~/rf_capture/logs/*.log
```

### SSH no responde
```bash
# Verificar servicio
sudo systemctl status ssh

# Habilitar
sudo systemctl enable ssh
sudo systemctl start ssh

# Test local
ssh pi@localhost
```

---

## 📋 Checklist Post-Instalación

- [ ] `rtl_test -t` ejecuta correctamente
- [ ] Archivo CSV creado en `~/rf_capture/data/`
- [ ] SSH conecta desde portátil
- [ ] Python importa todas las librerías
- [ ] Scripts descargados y ejecutables

---

## ⏭️ Siguiente Paso

→ Configurar portátil: **[02_GUIA_PORTATIL.md](02_GUIA_PORTATIL.md)**

