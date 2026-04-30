# RUN ME FIRST — Arranque rápido del laboratorio CAN Bus

[Bertsioa euskaraz](RUN_ME_FIRST_eu.md)

> Tiempo estimado: **10 minutos** (asumiendo que la VM Linux ya está lista y can-utils + ICSim compilados).

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

## Paso 2 — Iniciar ICSim (cuadro de mandos)

Abrir terminal 1:
```bash
./ICSim/icsim vcan0
```
Aparecerá una ventana gráfica con velocímetro, intermitentes y estado de puertas.

---

## Paso 3 — Iniciar el mando de control

Abrir terminal 2:
```bash
./ICSim/controls vcan0
```
Usar teclado o gamepad para interactuar. Las teclas por defecto:
- `W/S` — acelerar / frenar (velocidad)
- `Q/E` — intermitente izquierda / derecha
- `1/2/3/4` — bloquear/desbloquear puertas

---

## Paso 4 — Verificar tráfico en bus

Abrir terminal 3:
```bash
candump vcan0
```
Debes ver tramas fluyendo. Ejemplo de salida:
```
vcan0  244   [8]  00 00 00 00 00 00 00 00
vcan0  188   [8]  00 00 00 00 00 00 00 00
vcan0  19B   [8]  0F 00 00 00 00 00 00 00
```

---

## Paso 5 — Ejecutar la primera inyección de prueba

Abrir terminal 4:
```bash
# Subir velocidad al máximo en el cuadro de mandos
cansend vcan0 244#00000000FF000000
```
Observar el velocímetro de ICSim subir.

---

## ¿Todo funcionando?

Si el velocímetro responde a `cansend`, el entorno está listo. Continúa con:

→ **[Práctica A — Reconocimiento](lab/04_Practica_A_Reconocimiento.md)**

---

## Solución rápida de problemas

| Síntoma | Solución |
|---|---|
| `vcan0` no aparece | `sudo modprobe vcan` y repetir setup_vcan.sh |
| ICSim no abre ventana | Instalar `libsdl2-dev libsdl2-image-dev` |
| `candump` no muestra nada | Verificar que ICSim y controls están corriendo |
| `cansend` da error de socket | Verificar que `vcan0` está UP: `ip link set vcan0 up` |
| `python-can` no importa | Activar venv: `source .venv/bin/activate` |
