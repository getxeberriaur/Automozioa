# Checklist de configuración del laboratorio CAN Bus (docente)

[Bertsioa euskaraz](02_Checklist_configuracion_laboratorio_eu.md)

---

## Opción recomendada — Docker ✅

Método más rápido y reproducible. No requiere compilar ICSim ni instalar SDL2.

### Requisitos
- [ ] Docker instalado (`docker --version` responde).
- [ ] 4 GB RAM, 2 vCPU, 5 GB disco libre.
- [ ] Linux con módulo `vcan` disponible (`modprobe vcan` no da error).

### Arranque
```bash
cd CANbus_ICSim_Ciber
docker build -t icsim:local .
docker run --name icsim_run --network host --cap-add NET_ADMIN -d icsim:local
```

### Verificación
- [ ] `docker logs icsim_run` muestra "x11vnc is listening on :5901".
- [ ] `http://localhost:6080/vnc_lite.html` muestra velocímetro y mando.
- [ ] `docker exec -it icsim_run candump vcan0` muestra tramas CAN.
- [ ] `docker exec -it icsim_run cansend vcan0 244#00000000FF000000` mueve el velocímetro.

### Solución rápida de problemas Docker

| Problema | Acción |
|---|---|
| Error "permission denied" en docker | `sudo usermod -aG docker $USER` + cerrar/abrir sesión |
| Contenedor ya existe | `docker rm -f icsim_run` |
| Puerto 6080 ocupado | `docker run ... -p 6081:6080 ...` y abrir `:6081` |
| X server no arranca | `docker logs icsim_run` → buscar `/tmp/xvfb.log` |

---

## Opción alternativa — Instalación nativa en Linux

> Usar solo si Docker no está disponible en el aula.

## A) Requisitos del sistema (por puesto)

- [ ] Ubuntu 22.04 LTS o Kali Linux 2024+ (física o VM con ≥4 GB RAM, ≥2 vCPU).
- [ ] Acceso a `sudo`.
- [ ] Conexión a internet para instalar dependencias (o paquetes en USB offline).
- [ ] Tarjeta gráfica con soporte OpenGL (para SDL2 / ventana ICSim).
- [ ] Python 3.10+.

> **Windows:** No soporta SocketCAN. Usar VM VirtualBox/VMware o WSL2 con kernel personalizado (complejo — no recomendado para aula).

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
| `vcan0` desaparece al reiniciar | Añadir `setup_vcan.sh` a `/etc/rc.local` o systemd |
| Paquetes sin internet | Preparar USB con `.deb` de `can-utils`, `libsdl2-dev`, `libsdl2-image-dev` |
| Equipo sin VM | Usar live USB Kali Linux con persistence, o Docker en Windows con WSL2 |
