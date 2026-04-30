# Checklist del docente — Game Master CTF Automotive

[Bertsioa euskaraz](02_Checklist_docente_eu.md)

> Este documento es **confidencial**. No distribuir a los participantes.

---

## A) Preparación del entorno (30 min antes)

### Sistema
- [ ] Ubuntu 22.04 / Kali Linux arrancado y actualizado
- [ ] Kernel ≥ 5.15 confirmado: `uname -r`
- [ ] can-utils instalado: `candump --version`
- [ ] python-can instalado: `python3 -c "import can; print(can.__version__)"`

### Interfaz vcan0
- [ ] `sudo modprobe can vcan can_raw`
- [ ] `sudo ip link add dev vcan0 type vcan`
- [ ] `sudo ip link set up vcan0`
- [ ] Verificar: `ip link show vcan0` → debe mostrar `UP`

### ICSim
- [ ] ICSim compilado y ejecutable (`./icsim` sin errores)
- [ ] `./icsim vcan0` → ventana del cuadro de instrumentos visible
- [ ] `./controls vcan0` → controles responden (teclas flechas mueven velocímetro)
- [ ] ICSim proyectado en pantalla o monitor visible para todos los equipos

### Scripts del lab (heredados del lab CAN)
- [ ] `can_scanner.py` ejecutable: `python3 ../CANbus_ICSim_Ciber/scripts/can_scanner.py --help`
- [ ] `replay_attack.py` ejecutable
- [ ] `fuzz_can.py` ejecutable
- [ ] `can_dos.py` ejecutable

### Tráfico señuelo (obligatorio para Fase 1 genuina)
- [ ] `scripts/decoy_traffic.py` presente: `ls scripts/decoy_traffic.py`
- [ ] python-can instalado: `python3 -c "import can"`
- [ ] Lanzado en terminal separada **antes** de que lleguen los participantes:
  ```bash
  python3 scripts/decoy_traffic.py
  ```
- [ ] Confirmar que el script muestra 6 IDs señuelo en el log de arranque
- [ ] Verificar con `candump vcan0` que se ven IDs: `0x300`, `0x4AA`, `0x1F0`, `0x3C0`, `0x520`, `0x6B0`

---

## B) Materiales a preparar (impresos)

- [ ] `01_Enunciado_participantes.md` — una copia por participante
- [ ] `03_Hoja_flags_equipo.md` — una copia por participante (para firmar y entregar)
- [ ] `04_Respuestas_master.md` — **solo docente**, no distribuir
- [ ] Hoja de puntuación en blanco (ver sección D)

---

## C) Guía de validación de flags por fase

### FASE 1 — Reconocimiento

| Flag | Respuesta correcta | Cómo validar |
|---|---|---|
| FLAG-F1A | `0x244` | El participante muestra `cansniffer` o log con 0x244 cambiando al mover el acelerador |
| FLAG-F1B | `0x19B` | El participante muestra 0x19B cambiando al abrir/cerrar puertas en controls |
| FLAG-F1C | `0x01` | El participante muestra byte 0 = 01 en ID 0x188 al activar giro izquierdo |

> **IDs señuelo activos** (inyectados por `decoy_traffic.py`) — si el participante presenta
> uno de estos como respuesta, NO validar; indicar *"sigue buscando"*:
> `0x300`, `0x4AA`, `0x1F0`, `0x3C0`, `0x520`, `0x6B0`
>
> El método correcto es correlacionar acción en `controls` con cambio en el bus:
> mover acelerador → solo `0x244` cambia al ritmo de la acción.

**Pregunta oral sugerida F1:** *"¿Cómo distinguiste los IDs reales de los señuelos? ¿Qué herramienta te ayudó a correlacionar acción con cambio de byte?"*

---

### FASE 2 — Inyección

| Flag | Criterio de validación | Evidencia esperada |
|---|---|---|
| FLAG-F2A | ICSim muestra velocímetro en zona roja (>200) | Pantallazo + `cansend vcan0 244#00000000FF000000` o equivalente |
| FLAG-F2B | Ambos indicadores de giro parpadeando | Pantallazo + `cansend vcan0 188#0300000000000000` |
| FLAG-F2C | ICSim muestra puertas abiertas (iconos verdes) | Pantallazo + `cansend vcan0 19B#0000000000000000` |
| FLAG-F2D | Terminal con bucle activo 30 s | Script con `while true; do cansend ...; sleep 0.01; done` o equivalente Python |

**Pregunta oral sugerida F2:** *"¿Qué diferencia hay entre inyectar un frame una vez y mantener el bucle? ¿Qué pasaría si paras el bucle?"*

---

### FASE 3 — Replay

| Flag | Criterio de validación | Evidencia esperada |
|---|---|---|
| FLAG-F3 | Un valor entre 3 y 10 segundos es razonable | Archivo `.log` + comando `replay_attack.py --id 19B` + capturas |

> **Nota:** no hay un único valor correcto. Aceptar cualquier tiempo que el equipo pueda justificar con su log. El valor típico con ICSim es **5 segundos** si se activa una vez.

**Pregunta oral sugerida F3:** *"¿Cómo podría el fabricante prevenir este ataque? ¿Sería suficiente con cifrar el CAN?"*

---

### FASE 4 — DoS / Fuzzing

| Flag | Criterio de validación | Rango aceptable |
|---|---|---|
| FLAG-F4 | Tasa de fps durante DoS | Entre 500 y 10.000 fps — cualquier valor demostrado con `canbusload` >80% |

**Pregunta oral sugerida F4:** *"¿Por qué el ID 0x000 es el más eficaz para un DoS en CAN? ¿Qué protocolo usa CAN para la arbitración?"*

---

### BONUS — Defensa

Aceptar si:
- [ ] El código Python funciona en el terminal sin errores
- [ ] El participante puede demostrar que detecta/filtra al menos un frame anómalo en tiempo real
- [ ] El participante explica en 2 frases la limitación de su contramedida

---

## D) Hoja de puntuación (rellenar durante el CTF)

| Participante | F1A | F1B | F1C | F2A | F2B | F2C | F2D | F3 | F4 | Bonus | Tiempo flags | TOTAL |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Participante 1 | | | | | | | | | | | | |
| Participante 2 | | | | | | | | | | | | |
| Participante 3 | | | | | | | | | | | | |
| Participante 4 | | | | | | | | | | | | |

**Puntos por flag:** F1 = 50/flag · F2 = 50/flag · F3 = 150 · F4 = 150 · Bonus = 100

**Bonus de velocidad:**
- F1 completado en <15 min desde el inicio: +50
- F2 completado en <15 min desde F1: +50
- F3 completado en <15 min desde F2: +50
- F4 completado en <10 min desde F3: +25

---

## E) Cierre del CTF

1. Anunciar los resultados y el **participante ganador**
2. Revisión colectiva de 10-15 min: el GM muestra los comandos correctos de cada fase
3. Debate: *"¿Qué contramedidas habrían impedido cada fase?"*
4. Recoger todas las hojas de flags firmadas (evidencia de participación)
5. Apagar ICSim y eliminar vcan0: `sudo ip link delete vcan0`
