# Checklist de configuración del laboratorio CAN Bus (docente)

[Bertsioa euskaraz](02_Checklist_configuracion_laboratorio_eu.md)

---

## ¿Linux o Windows? — Elige tu camino

> **ICSim requiere `vcan`, un módulo del kernel Linux.** Docker Desktop en Windows usa un kernel Microsoft sin este módulo, por lo que **no es posible ejecutar el lab directamente en Windows con Docker Desktop.**

| Situación del participante | Método recomendado |
|---|---|
| **Linux nativo** (Ubuntu, Kali, Debian…) | → [Opción A — Docker en Linux](#opción-a--docker-en-linux-recomendada) |
| **Windows** | → [Opción B — VM VirtualBox con OVA](#opción-b--vm-virtualbox-ova-para-windows) |
| Sin internet / sin VM | → [Opción C — Instalación nativa Linux](#opción-c--instalación-nativa-en-linux) |

---

## Opción A — Docker en Linux (recomendada)

Método más rápido y reproducible. No requiere compilar ICSim ni instalar SDL2.

### Requisitos
- [ ] Linux con módulo `vcan` disponible (`sudo modprobe vcan` no da error).
- [ ] Docker instalado (`docker --version` responde).
- [ ] 4 GB RAM, 2 vCPU, 5 GB disco libre.

### Arranque
```bash
# Cargar módulo vcan (solo la primera vez por sesión)
sudo modprobe vcan

cd CANbus_ICSim_Ciber
docker build -t icsim:local .
docker run --name icsim_run -p 5901:5901 -p 6080:6080 --cap-add NET_ADMIN -d icsim:local
```

### Verificación
- [ ] `docker logs icsim_run` muestra "x11vnc is listening on :5901".
- [ ] `http://localhost:6080/vnc_lite.html` muestra velocímetro y mando.
- [ ] `docker exec -it icsim_run candump vcan0` muestra tramas CAN.
- [ ] `docker exec -it icsim_run cansend vcan0 244#00000000FF000000` mueve el velocímetro.

### Solución rápida de problemas Docker

| Problema | Acción |
|---|---|
| `modprobe vcan` falla | El kernel no tiene soporte CAN — usar Opción B o instalar kernel genérico |
| Error "permission denied" en docker | `sudo usermod -aG docker $USER` + cerrar/abrir sesión |
| Contenedor ya existe | `docker rm -f icsim_run` |
| Puerto 6080 ocupado | `docker run ... -p 6081:6080 ...` y abrir `:6081` |
| X server no arranca | `docker logs icsim_run` → buscar `/tmp/xvfb.log` |
| `SIOCGIFINDEX: No such device` en logs | `vcan0` no existe — ejecutar `sudo modprobe vcan` en el host |

### Demo SavvyCAN del Día 2 (solo docente)

> SavvyCAN se ejecuta **en el host**, no dentro del contenedor. El contenedor crea `vcan0` en el kernel del host (gracias a `--cap-add NET_ADMIN`), por lo que SavvyCAN puede conectarse a él directamente desde el escritorio.

```bash
# Descargar AppImage en el host (una vez, antes del curso)
# El nombre incluye hash del commit en cada release — curl lo resuelve automáticamente
curl -Lo SavvyCAN.AppImage \
  $(curl -s https://api.github.com/repos/collin80/SavvyCAN/releases/latest \
    | grep -o '"browser_download_url":"[^"]*AppImage[^"]*"' \
    | cut -d'"' -f4)
chmod +x SavvyCAN.AppImage
sudo apt install -y libfuse2   # solo si da error al ejecutar

# Verificar que vcan0 es visible desde el host (con el contenedor corriendo)
ip link show vcan0   # debe mostrar la interfaz

# Lanzar SavvyCAN
./SavvyCAN.AppImage
```

- [ ] SavvyCAN abre sin errores en el escritorio del host.
- [ ] En SavvyCAN: **Connection → Open Connection Manager → SocketCAN → `vcan0` → Connect**.
- [ ] Al mover el acelerador en noVNC (`localhost:6080`), aparecen tramas en SavvyCAN.

---

## Opción B — VM VirtualBox + OVA (para Windows)

> **Docker Desktop en Windows no soporta `vcan`** (el kernel Microsoft WSL2 no incluye `CONFIG_CAN_VCAN`). La solución más rápida para Windows es importar una VM preconfigurada.

### Preparación del docente (una vez, antes del curso)

1. En una máquina Linux, ejecutar el script de preparación:
   ```bash
   cd CANbus_ICSim_Ciber
   sudo bash scripts/setup_ova_vm.sh
   ```
2. Apagar la VM: `sudo shutdown now`
3. En VirtualBox: **Archivo → Exportar servicio virtualizado**
   - Formato: `OVA 2.0`
   - Nombre sugerido: `CANbus_ICSim_Lab.ova`
4. Distribuir la OVA a los participantes (USB, servidor local, Google Drive…)

### Setup del participante Windows (5 min)

1. Instalar **VirtualBox** desde [https://www.virtualbox.org](https://www.virtualbox.org).
2. Doble clic en `CANbus_ICSim_Lab.ova` → Importar.
3. Iniciar la VM → usuario `canlab`.
4. Abrir terminal en la VM y ejecutar:
   ```bash
   bash ~/Escritorio/Iniciar_ICSim_Lab.sh
   ```
5. Abrir en el navegador de la VM: `http://localhost:6080/vnc_lite.html`

### Verificación (desde dentro de la VM)
- [ ] `ip link show vcan0` muestra estado `UP`.
- [ ] `http://localhost:6080/vnc_lite.html` muestra velocímetro y mando.
- [ ] `candump vcan0` muestra tramas fluyendo.

---

## Opción C — Instalación nativa en Linux

> Usar solo si Docker no está disponible en el aula.

## A) Requisitos del sistema (por puesto)

- [ ] Ubuntu 22.04 LTS o Kali Linux 2024+ (física o VM con ≥4 GB RAM, ≥2 vCPU).
- [ ] Acceso a `sudo`.
- [ ] Conexión a internet para instalar dependencias (o paquetes en USB offline).
- [ ] Tarjeta gráfica con soporte OpenGL (para SDL2 / ventana ICSim).
- [ ] Python 3.10+.

> **Windows:** Docker Desktop no soporta `vcan` (kernel Microsoft sin `CONFIG_CAN_VCAN`). Ver [Opción B — VM VirtualBox + OVA](#opción-b--vm-virtualbox-ova-para-windows).

---

## B) Dependencias de sistema

```bash
sudo apt update
sudo apt install -y \
    can-utils \
    libsdl2-dev \
    libsdl2-image-dev \
    python3 python3-pip python3-venv \
    git build-essential
```

Verificar:
- [ ] `candump --version` responde.
- [ ] `cansend --version` responde.
- [ ] `python3 --version` ≥ 3.10.

---

## C) Compilar ICSim

```bash
git clone https://github.com/zombieCraig/ICSim.git
cd ICSim
sudo apt install -y meson ninja-build
meson setup builddir
cd builddir
meson compile
```

- [ ] Binario `icsim` generado en `builddir/`.
- [ ] Binario `controls` generado en `builddir/`.

> Alternativa con Makefile clásico: `make` en el directorio raíz de ICSim (si meson falla).

---

## D) Entorno Python

```bash
cd CANbus_ICSim_Ciber
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

- [ ] `python -c "import can; print(can.__version__)"` muestra versión ≥ 4.0.

---

## E) Interfaz CAN virtual

```bash
sudo bash scripts/setup_vcan.sh
ip link show vcan0
```

- [ ] `vcan0` aparece con estado `UP`.
- [ ] `candump vcan0` arranca sin errores (puede esperar tramas en silencio).

---

## F) Verificación completa del entorno

Abrir 3 terminales simultáneas:

**Terminal 1 — ICSim:**
```bash
./ICSim/builddir/icsim vcan0
```
- [ ] Aparece ventana gráfica con velocímetro e intermitentes.

**Terminal 2 — Controls:**
```bash
./ICSim/builddir/controls vcan0
```
- [ ] Se puede acelerar/frenar con teclado y el velocímetro responde.

**Terminal 3 — Candump:**
```bash
candump vcan0
```
- [ ] Se ven tramas con IDs `0x244`, `0x188`, `0x19B` (o similares si se usa modo `-r`).

---

## G) Criterio de «laboratorio listo»

- Velocímetro de ICSim responde a `cansend vcan0 244#00000000FF000000`.
- `candump` captura ≥ 3 IDs distintos mientras ICSim está activo.
- Scripts Python importan `can` sin error.
- Equipo entrega capturas de pantalla de ICSim + `candump`.

---

## H) Modo avanzado — Hardware real (opcional)

Si el centro dispone de hardware USB-CAN (p.ej. dongle usbcan/BluePill+ del proyecto BatchDrake):

1. Conectar el dongle USB.
2. Ejecutar `usbcanbr /dev/ttyACM0 vcan0` (si se usa usbcan).
3. O configurar `slcan`: `slcand -o -s6 /dev/ttyUSB0 slcan0 && ip link set slcan0 up`.
4. Sustituir `vcan0` por `slcan0` o la interfaz correspondiente en todos los comandos.

> Consultar [https://github.com/BatchDrake/usbcan](https://github.com/BatchDrake/usbcan) para wiring y código Arduino del BluePill+.

---

## I) Plan de contingencia

| Problema | Acción |
|---|---|
| ICSim no compila | Usar imagen Docker (`docker build -t icsim:local .`) |
| SDL2 no disponible en VM | Activar aceleración gráfica en settings de VM, o usar Docker |
| `vcan0` desaparece al reiniciar | El servicio `vcan0.service` del script `setup_ova_vm.sh` lo hace persistente |
| Paquetes sin internet | Preparar USB con `.deb` de `can-utils`, `libsdl2-dev`, `libsdl2-image-dev` |
| Windows sin VirtualBox | Usar live USB Kali Linux con persistence |
| Docker Desktop en Windows no muestra ICSim | Esperado — usar Opción B (OVA) |
