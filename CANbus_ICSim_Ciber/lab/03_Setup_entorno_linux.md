# Setup del entorno Linux / VM — Paso a paso

## Opción A — Máquina virtual (recomendada para Windows)

### A1. Instalar VirtualBox

1. Descargar VirtualBox desde [https://www.virtualbox.org](https://www.virtualbox.org).
2. Instalar en Windows con opciones por defecto.
3. Descargar la ISO de **Ubuntu 22.04 LTS** (Desktop) desde [https://ubuntu.com/download/desktop](https://ubuntu.com/download/desktop).

### A2. Crear la VM

| Parámetro | Valor recomendado |
|---|---|
| Nombre | `CANlab` |
| Tipo | Linux / Ubuntu 64-bit |
| RAM | 4096 MB (mínimo 2048 MB) |
| Disco | 30 GB dinámico |
| Procesadores | 2 vCPU |
| Gráficos | VBoxSVGA, habilitar aceleración 3D |
| Carpeta compartida | Directorio del host con los scripts del lab |

### A3. Instalar Ubuntu

1. Montar la ISO en la unidad óptica virtual.
2. Iniciar VM → "Install Ubuntu" → instalación mínima.
3. Crear usuario (`canlab` / contraseña de aula).
4. Reiniciar y eliminar medio de instalación.

### A4. Instalar Guest Additions

```bash
sudo apt update
sudo apt install -y build-essential dkms linux-headers-$(uname -r)
# Desde el menú de VirtualBox: Dispositivos → Insertar imagen de Guest Additions
sudo mount /dev/cdrom /mnt
sudo /mnt/VBoxLinuxAdditions.run
sudo reboot
```

---

## Opción B — Kali Linux (recomendada si el centro ya la usa)

1. Descargar imagen VM de Kali Linux desde [https://www.kali.org/get-kali/#kali-virtual-machines](https://www.kali.org/get-kali/#kali-virtual-machines).
2. Importar en VirtualBox o VMware.
3. Credenciales por defecto: `kali` / `kali`.
4. Kali ya incluye muchas herramientas útiles. Solo falta instalar `can-utils` e `ICSim`.

---

## Opción C — Docker (avanzado)

> Requiere Docker Desktop en Windows + WSL2 backend, o Docker en Linux host.

```bash
# Crear contenedor privilegiado con soporte CAN
docker run -it --privileged \
  --cap-add=NET_ADMIN \
  ubuntu:22.04 bash
```

Dentro del contenedor:
```bash
apt update && apt install -y can-utils python3 python3-pip
modprobe vcan  # puede fallar en algunos kernels Docker
ip link add dev vcan0 type vcan
ip link set up vcan0
```

> **Limitación:** ICSim necesita SDL2 y pantalla gráfica — requiere X11 forwarding o VNC. No recomendado para aula sin experiencia en Docker.

---

## Instalación completa en Ubuntu/Kali

### Paso 1 — Dependencias de sistema

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y \
    can-utils \
    libsdl2-dev \
    libsdl2-image-dev \
    meson ninja-build \
    python3 python3-pip python3-venv \
    git build-essential \
    wireshark  # opcional — análisis gráfico
```

### Paso 2 — Módulos del kernel CAN

```bash
sudo modprobe can
sudo modprobe vcan
sudo modprobe can_raw
```

Para que sean persistentes:
```bash
echo -e "can\nvcan\ncan_raw" | sudo tee /etc/modules-load.d/can.conf
```

### Paso 3 — Interfaz CAN virtual

```bash
sudo bash scripts/setup_vcan.sh
# o manualmente:
sudo ip link add dev vcan0 type vcan
sudo ip link set up vcan0
```

Verificar:
```bash
ip -details link show vcan0
```

### Paso 4 — Compilar ICSim

```bash
git clone https://github.com/zombieCraig/ICSim.git
cd ICSim
meson setup builddir
cd builddir
meson compile
cd ../..
```

Verificar:
```bash
ls ICSim/builddir/icsim ICSim/builddir/controls
# Ambos binarios deben existir
```

### Paso 5 — Entorno Python

```bash
cd CANbus_ICSim_Ciber
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Paso 6 — Test de integración

```bash
# Terminal 1
./ICSim/builddir/icsim vcan0 &

# Terminal 2 (esperar 2 seg a que ICSim arranque)
./ICSim/builddir/controls vcan0 &

# Terminal 3
candump vcan0

# Terminal 4 — inyección de prueba
cansend vcan0 244#00000000FF000000
# El velocímetro debe subir
```

---

## Configuración de Wireshark para CAN (opcional)

1. `sudo usermod -aG wireshark $USER` y cerrar sesión / volver a abrir.
2. Abrir Wireshark → seleccionar interfaz `vcan0`.
3. Filtro de captura: `can` o dejar vacío.
4. Los frames CAN aparecen con disector integrado (ID, DLC, datos en hex y ASCII).

---

## Snapshot recomendado (docente)

Antes de la sesión:
1. Con todo instalado y funcionando, hacer snapshot de la VM: `VirtualBox → Máquina → Tomar Snapshot → "lab-listo"`.
2. Distribuir la VM como `.ova` exportada si los equipos son distintos.
3. Los participantes solo tienen que importar la `.ova` y ejecutar `setup_vcan.sh`.
