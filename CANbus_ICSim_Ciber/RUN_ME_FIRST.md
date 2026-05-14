# RUN ME FIRST — Arranque rápido del laboratorio CAN Bus

[Bertsioa euskaraz](RUN_ME_FIRST_eu.md)

> Tiempo estimado: **5 minutos** con Docker en Linux / **15 minutos** desde VM en Windows.

---

## ¿Linux o Windows?

> **ICSim necesita `vcan`, un módulo del kernel Linux.**
> Docker Desktop en Windows usa un kernel Microsoft sin este módulo — **no funciona en Windows directamente.**

| Sistema | Método |
|---|---|
| **Linux nativo** (Ubuntu, Kali…) | Sigue los pasos de abajo |
| **Windows** | Primero [configura una VM Linux](lab/02_Checklist_configuracion_laboratorio.md#opción-b--vm-virtualbox-ova-para-windows), luego sigue estos pasos desde dentro de la VM |

---

## Paso 1 — Levantar la interfaz CAN virtual

```bash
sudo bash scripts/setup_vcan.sh
```

Verificar:
```bash
ip link show vcan0
# Debe mostrar: vcan0: <NOARP,UP,LOWER_UP> ...
```

---

## Paso 2 — Construir la imagen Docker

```bash
cd CANbus_ICSim_Ciber
docker build -t icsim:local .
```

> Solo es necesario la primera vez o cuando se modifique el `Dockerfile`.

---

## Paso 3 — Arrancar el contenedor

```bash
docker run --name icsim_run --network host --cap-add NET_ADMIN -d icsim:local
```

> `--network host` es necesario en Linux para que el contenedor vea el `vcan0` del host.

El contenedor levanta automáticamente:
- ICSim (velocímetro) y controls (mando)
- Servidor VNC + noVNC en puerto `6080`

---

## Paso 4 — Abrir la interfaz gráfica

Abre en el navegador:
```
http://localhost:6080/vnc_lite.html
```

Verás dos ventanas:
- **Velocímetro** (icsim) — arriba
- **Mando de control** (controls) — abajo

Interactúa con el mando usando el teclado (flechas = acelerar/frenar, Q/E = intermitentes).

---

## Paso 5 — Verificar tráfico en el bus

Desde la terminal del host (no dentro del contenedor):

```bash
candump vcan0
```

Debes ver tramas fluyendo:
```
vcan0  244   [8]  00 00 00 00 1A 00 00 00
vcan0  188   [8]  00 00 00 00 00 00 00 00
vcan0  19B   [8]  0F 00 00 00 00 00 00 00
```

---

## Paso 6 — Primera inyección de prueba

```bash
# Un solo frame puntual
cansend vcan0 244#00000000FF000000

# Para que el efecto sea sostenido (bucle continuo)
while true; do cansend vcan0 244#00000000FF000000; sleep 0.01; done
```

Observar el velocímetro de ICSim subir en el navegador.

> **Nota:** ICSim genera sus propias tramas continuamente. Un solo `cansend` compite con ellas y puede no verse. El bucle garantiza que la inyección domina el bus.

---

## ¿Todo funcionando?

Si el velocímetro responde al bucle de `cansend`, el entorno está listo. Continúa con:

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

## Solución rápida de problemas

| Síntoma | Solución |
|---|---|
| `vcan0` no aparece | `sudo modprobe vcan` y repetir `setup_vcan.sh` |
| Contenedor sale inmediatamente | `docker logs icsim_run` — buscar errores de entrypoint |
| `candump` no muestra nada | Verificar que ICSim está corriendo: `docker logs icsim_run` |
| `cansend` no mueve el velocímetro | Usar bucle: `while true; do cansend vcan0 244#00000000FF000000; sleep 0.01; done` |
| `cansend` da error de socket | Verificar que `vcan0` está UP: `ip link show vcan0` |
| En Windows no funciona Docker | Docker Desktop no soporta `vcan` — usar VM Linux (ver checklist) |
| `python-can` no importa | Activar venv: `source .venv/bin/activate` |
