# RUN ME FIRST — Arranque rápido del laboratorio CAN Bus

[Bertsioa euskaraz](RUN_ME_FIRST_eu.md)

> Tiempo estimado: **5 minutos** con Docker (método recomendado).

---

## Método recomendado — Docker

### Paso 1 — Construir la imagen

```bash
cd CANbus_ICSim_Ciber
docker build -t icsim:local .
```

> Solo es necesario la primera vez o cuando se modifique el `Dockerfile`.

### Paso 2 — Arrancar el contenedor

```bash
docker run --name icsim_run --network host --cap-add NET_ADMIN -d icsim:local
```

El contenedor levanta automáticamente:
- Interfaz CAN virtual `vcan0`
- ICSim (velocímetro) y controls (mando)
- Servidor VNC + noVNC en puerto `6080`

### Paso 3 — Abrir la interfaz gráfica

Abre en el navegador:
```
http://localhost:6080/vnc_lite.html
```

Verás dos ventanas con barra de título (openbox) y una barra de tareas (tint2):
- **Velocímetro** (icsim) — arriba
- **Mando de control** (controls) — abajo

### Paso 4 — Verificar tráfico en bus

Desde tu terminal (host), conéctate al bus virtual dentro del contenedor:

```bash
docker exec -it icsim_run candump vcan0
```

Debes ver tramas fluyendo. Ejemplo:
```
vcan0  244   [8]  00 00 00 00 00 00 00 00
vcan0  188   [8]  00 00 00 00 00 00 00 00
vcan0  19B   [8]  0F 00 00 00 00 00 00 00
```

### Paso 5 — Ejecutar la primera inyección de prueba

```bash
docker exec -it icsim_run cansend vcan0 244#00000000FF000000
```

Observar el velocímetro de ICSim subir en el navegador.

---

## ¿Todo funcionando?

Si el velocímetro responde a `cansend`, el entorno está listo. Continúa con:

→ **[Práctica A — Reconocimiento](lab/04_Practica_A_Reconocimiento.md)**

---

## Comandos útiles del contenedor

```bash
# Ver logs del contenedor
docker logs -f icsim_run

# Abrir shell dentro del contenedor
docker exec -it icsim_run bash

# Parar el contenedor
docker stop icsim_run

# Eliminar el contenedor (para empezar de nuevo)
docker rm -f icsim_run
```

---

## Método alternativo — Instalación nativa en Linux

> Solo si no puedes usar Docker. Ver [`lab/02_Checklist_configuracion_laboratorio.md`](lab/02_Checklist_configuracion_laboratorio.md) y [`lab/03_Setup_entorno_linux.md`](lab/03_Setup_entorno_linux.md).

```bash
# Levantar vcan0
sudo bash scripts/setup_vcan.sh

# Iniciar ICSim (terminal 1)
./ICSim/builddir/icsim vcan0

# Iniciar controls (terminal 2)
./ICSim/builddir/controls vcan0

# Verificar tráfico (terminal 3)
candump vcan0
```

---

## Solución rápida de problemas

| Síntoma | Solución |
|---|---|
| `vcan0` no aparece | `sudo modprobe vcan` y repetir setup_vcan.sh |
| ICSim no abre ventana | Instalar `libsdl2-dev libsdl2-image-dev` |
| `candump` no muestra nada | Verificar que ICSim y controls están corriendo |
| `cansend` da error de socket | Verificar que `vcan0` está UP: `ip link set vcan0 up` |
| `python-can` no importa | Activar venv: `source .venv/bin/activate` |
