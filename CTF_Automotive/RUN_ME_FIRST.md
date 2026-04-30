# RUN ME FIRST — Arranque del CTF Automotive (Game Master)

[Bertsioa euskaraz](RUN_ME_FIRST_eu.md)

> Tiempo estimado de preparación: **30 minutos** antes de que lleguen los participantes.

---

## Paso 1 — Verificar el entorno base

```bash
# 1.1 Comprobar que vcan0 está activo
ip link show vcan0
# Debe mostrar: vcan0: ... UP ...

# Si no está activo, ejecutar:
sudo bash ../CANbus_ICSim_Ciber/scripts/setup_vcan.sh

# 1.2 Verificar can-utils
candump --version
cansend --version
cansniffer --help | head -1

# 1.3 Verificar python-can
python3 -c "import can; print('python-can', can.__version__)"

# 1.4 Verificar scripts del CTF (se usan los del lab CAN)
ls ../CANbus_ICSim_Ciber/scripts/
# Debe listar: can_scanner.py, replay_attack.py, fuzz_can.py, can_dos.py
```

---

## Paso 2 — Lanzar ICSim

```bash
# Terminal 1 — simulador visual
cd /ruta/a/ICSim
./icsim vcan0

# Terminal 2 — controles (mantener abierto durante todo el CTF)
./controls vcan0
```

> Asegúrate de que el cuadro de instrumentos es visible en pantalla para todos los equipos o proyectado en la pizarra.

---

## Paso 3 — Ajuste de dificultad (opcional)

### Nivel Avanzado — añadir ruido al bus

```bash
# Terminal 3 (solo nivel Avanzado/Expert) — IDs de ruido
cangen vcan0 -I r -L 8 -D r -g 50 &
# Genera frames aleatorios cada ~50ms para dificultar reconocimiento
```

### Nivel Básico — entregar tabla de ayuda

Imprimir y entregar a los equipos antes de empezar:

| CAN ID | Función aproximada |
|---|---|
| 0x244 | Relacionado con dinámica del vehículo |
| 0x188 | Relacionado con señalización |
| 0x19B | Relacionado con acceso al vehículo |

---

## Paso 4 — Materiales a distribuir

- [ ] Una copia de `lab/01_Enunciado_participantes.md` por equipo (o en pantalla)
- [ ] Una copia de `lab/03_Hoja_flags_equipo.md` por equipo (impresa para firmar)
- [ ] Hoja de normas (incluida en el enunciado)
- [ ] Acceso al terminal Linux con herramientas disponibles

**Tú conservas (no compartir):**
- [ ] `lab/04_Respuestas_master.md` — respuestas + scoring

---

## Paso 5 — Arrancar el CTF

```
[GM dice en voz alta]
"El escenario comienza ahora. Tienen 90 minutos.
Cualquier duda técnica sobre las herramientas la resuelvo yo.
Las preguntas sobre qué atacar o cómo hacerlo son parte del reto.
¡Suerte!"
```

Anotar hora de inicio: `___:___`  
Hora de fin: inicio + 90 min = `___:___`

---

## Paso 6 — Durante el CTF (rol de GM)

- Validar flags cuando un equipo las presente (ver `04_Respuestas_master.md`)
- Registrar timestamp de cada flag validada para calcular bonus de velocidad
- **Pistas permitidas** (sin revelar respuestas):
  - F1: *"¿Qué herramienta muestra solo los bytes que cambian?"*
  - F2: *"¿Cuántos bytes tiene un frame de 0x244? ¿Cuál es el que varía con el acelerador?"*
  - F3: *"Comprueba el flag `--id` de replay_attack.py"*
  - F4: *"¿Qué ID tiene mayor prioridad en CAN?"*

---

## Resolución de problemas

| Problema | Solución |
|---|---|
| `vcan0` no aparece | `sudo modprobe vcan; sudo ip link add dev vcan0 type vcan; sudo ip link set up vcan0` |
| ICSim no arranca | Verificar que las dependencias SDL2 están instaladas: `sudo apt install libsdl2-dev libsdl2-image-dev` |
| ICSim no responde a inyecciones | Confirmar que está escuchando en `vcan0`, no en `can0` |
| Equipos bloqueados en F1 >15 min | Dar pista de `cansniffer` o entregar tabla de IDs (solo nivel básico) |
