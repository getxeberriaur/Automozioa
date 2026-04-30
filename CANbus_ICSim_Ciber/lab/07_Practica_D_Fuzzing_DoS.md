# Práctica D — Fuzzing y Denegación de Servicio (DoS)

**Duración estimada:** 45 minutos  
**Dificultad:** Media-Alta  
**Herramientas:** `cangen`, `scripts/fuzz_can.py`, `scripts/can_dos.py`

---

## Objetivo

Comprender cómo el fuzzing y la saturación del bus pueden provocar comportamientos inesperados o denegar el servicio a nodos legítimos. En un entorno real, estas técnicas pueden afectar a sistemas críticos de seguridad vial.

---

## Contexto

### ¿Qué es el fuzzing en CAN?

El **fuzzing** consiste en enviar tramas con contenido aleatorio o semi-dirigido para descubrir:
- IDs desconocidos que afectan a funciones del vehículo.
- Valores de datos que provocan estados de error en ECUs.
- Vulnerabilidades en el procesamiento de mensajes de diagnóstico (UDS, OBD).

### ¿Qué es el DoS en CAN?

El bus CAN usa **arbitraje por colisión** basado en prioridad: el ID más bajo (dominante) gana el bus. Un atacante puede:
1. Enviar tramas de ID=0x000 (máxima prioridad) continuamente.
2. El árbitro del bus siempre cede a esta prioridad.
3. Los nodos legítimos (ID > 0x000) nunca pueden transmitir.
4. El bus queda **saturado** → todas las funciones de control pierden comunicación.

> **En un vehículo real:** esto puede desactivar frenos, dirección asistida, airbags. Es un ataque **potencialmente letal** en entorno real.

---

## Prerrequisitos

- `vcan0` activa.
- ICSim corriendo.
- `controls` parado (para observar efectos más claramente).

---

## Ejercicio D.1 — Fuzzing básico con `cangen`

`cangen` genera tráfico CAN aleatorio.

```bash
# Fuzzing de todos los IDs con datos aleatorios — 100 tramas/seg
cangen -g 10 -I r -L r vcan0

# Parámetros:
# -g 10    → gap de 10 ms entre tramas (~100 Hz)
# -I r     → IDs aleatorios (r = random)
# -L r     → DLC aleatorio (0-8 bytes)
```

Ejecutar durante 30 segundos y observar ICSim. Anotar si aparecen comportamientos inesperados.

### Fuzzing semi-dirigido (solo IDs conocidos)

```bash
# Fuzzing solo del rango de IDs 0x100-0x300, datos aleatorios
cangen -g 5 -I 0x100 -n 1000 vcan0
```

---

## Ejercicio D.2 — Fuzzing dirigido con `fuzz_can.py`

El script `scripts/fuzz_can.py` implementa estrategias de fuzzing más inteligentes:
- **Random puro:** IDs y datos completamente aleatorios.
- **Por ID:** fuzzing de datos en un ID específico.
- **Mutación:** partir de una trama conocida y mutar bytes uno a uno.

```bash
source .venv/bin/activate

# Fuzzing aleatorio durante 60 segundos
python scripts/fuzz_can.py \
    --interface vcan0 \
    --mode random \
    --duration 60 \
    --rate 50 \
    --log logs/fuzz_session.log

# Fuzzing dirigido al ID de velocidad (0x244), mutando byte a byte
python scripts/fuzz_can.py \
    --interface vcan0 \
    --mode mutate \
    --target-id 0x244 \
    --base-data 0000000000000000 \
    --duration 30
```

### ¿Qué observar?

- ¿Cambia el velocímetro de forma anómala?
- ¿Se congela o reinicia ICSim?
- ¿Aparecen lecturas fuera de rango?

Anotar en el log cualquier comportamiento inesperado con el valor exacto de la trama que lo provocó.

---

## Ejercicio D.3 — Denegación de Servicio (bus flooding)

### Paso 1 — Medir la carga de bus en condiciones normales

Con ICSim y controls corriendo:
```bash
canbusload vcan0@500000 -b -c -t
```

Anotar el porcentaje de carga del bus. Ejemplo esperado: `~15-20%`.

### Paso 2 — Lanzar el ataque DoS

```bash
# En un segundo terminal, ejecutar el flooding
python scripts/can_dos.py \
    --interface vcan0 \
    --priority-id 0x000 \
    --rate 10000 \
    --duration 30
```

O con `cangen`:
```bash
# Flooding masivo con ID de máxima prioridad
cangen -g 0 -I 0 vcan0
# -g 0: sin gap (máxima velocidad posible)
# -I 0: ID=0x000 (prioridad máxima)
```

### Paso 3 — Medir la carga de bus durante el ataque

En un tercer terminal:
```bash
canbusload vcan0@500000 -b -c -t
```

### Paso 4 — Observar el efecto en ICSim

Con el flooding activo:
- ¿Sigue respondiendo el velocímetro a los controles?
- ¿Se congelan los datos del cuadro de mandos?

### Preguntas

- ¿Qué carga de bus se alcanza durante el DoS?
- ¿En qué porcentaje el bus deja de responder a controles legítimos?
- ¿Por qué las tramas de ID=0x000 tienen prioridad máxima?

---

## Ejercicio D.4 — DoS selectivo (suprimir un nodo específico)

En lugar de saturar todo el bus, un atacante sofisticado puede silenciar un nodo específico enviando **Error Frames** o IDs del mismo nodo con datos incorrectos que fuercen a la ECU víctima a entrar en **Bus-Off mode**.

> **Nota:** Esta técnica (ECU silencing) es compleja de demostrar en vcan0 (el driver virtual no modela error counters de la misma forma que el hardware real). Se incluye como concepto teórico.

**Concepto:**
1. El CAN tiene un contador de errores por nodo (TEC/REC).
2. Si una ECU acumula suficientes errores de transmisión, entra en **Bus-Off**: deja de transmitir.
3. Un atacante puede provocar esto enviando tramas que generen ACK errors en el nodo víctima.
4. El nodo víctima "desaparece" del bus sin que nadie más lo sepa.

---

## Ejercicio D.5 — Reto: Ataque combinado

Diseñar y ejecutar un ataque en tres fases usando ICSim:

**Fase 1 (Reconocimiento):** Capturar 10 segundos de tráfico normal.
```bash
candump -l vcan0  # guardar como logs/pre_ataque.log
```

**Fase 2 (Inyección + DoS simultáneo):**
- Terminal A: flooding de ID=0x000.
- Terminal B: inyección de velocidad máxima en ID=0x244.

**Fase 3 (Análisis):** Capturar tráfico durante el ataque.
```bash
candump -l vcan0  # guardar como logs/durante_ataque.log
```

Comparar los dos logs:
```bash
# Contar tramas por ID en el log pre-ataque
awk '{print $3}' logs/pre_ataque.log | sort | uniq -c | sort -rn

# Contar tramas por ID en el log durante el ataque
awk '{print $3}' logs/durante_ataque.log | sort | uniq -c | sort -rn
```

---

## Entregables de la Práctica D

1. Log de la sesión de fuzzing (`logs/fuzz_session.log`).
2. Medición de carga del bus antes y durante el DoS.
3. Capturas de pantalla de ICSim durante el flooding.
4. Comparación de logs (Ejercicio D.5) con análisis de 3-5 líneas.
5. Respuestas a las preguntas de los ejercicios.

---

## Contramedidas conocidas

| Ataque | Contramedida |
|---|---|
| Fuzzing de IDs | Filtrado de IDs en gateway (whitelist de IDs válidos) |
| Fuzzing de datos | Validación de rango en capa aplicación ECU |
| Bus flooding | Hardware con límite de prioridad configurable; CAN XL con VCID |
| ECU silencing | Monitorización de contadores de error; redundancia |
| Todos | Segmentación de buses + gateway con filtrado estricto |

---

## Reflexión final

- ¿Cuál de los tres ataques (inyección, replay, DoS) te parece más peligroso en un vehículo real? ¿Por qué?
- ¿Qué sistemas de seguridad activa (frenos, airbags, ESP) usarías para proteger primero con autenticación CAN?
- ¿Conoces diferencias entre CAN 2.0, CAN FD y CAN XL en términos de seguridad?
