# Práctica C — Ataque de Replay

[Bertsioa euskaraz](06_Practica_C_Replay_eu.md)

**Duración estimada:** 40 minutos  
**Dificultad:** Media  
**Herramientas:** `candump`, `canplayer`, `scripts/replay_attack.py`

---

## Objetivo

Grabar una secuencia de acciones legítimas sobre el bus CAN y reproducirla posteriormente para causar el mismo efecto, sin conocer el significado de las tramas. Demostrar que la ausencia de mecanismos anti-replay en CAN bus permite reutilizar capturas.

---

## Contexto

Un **ataque de replay** consiste en:
1. Capturar (grabando) una comunicación legítima.
2. Reproducirla en el mismo o en otro bus compatible.

En CAN bus, este ataque es trivial porque:
- No hay timestamps en el protocolo.
- No hay números de secuencia.
- No hay challenge-response.
- No hay firma de mensaje.

**Casos reales documentados:**
- Replay de secuencia de desbloqueo de puertas (grabada en el parking).
- Replay de secuencia de arranque del motor en vehículos sin inmovilizador correctamente implementado.
- Replay de comandos de infoentretenimiento para escalar privilegios al bus de control.

---

## Prerrequisitos

- `vcan0` activa.
- ICSim y controls corriendo.

---

## Ejercicio C.1 — Grabar una secuencia de acción

### Pasos

1. Iniciar la grabación en un terminal:
```bash
candump -l vcan0
# El archivo se crea como: candump-YYYYMMDD-HHMMSS.log
```

2. Ir a la ventana de `controls` y realizar las siguientes acciones **en orden**:
   - Acelerar al máximo (mantener 3 segundos).
   - Activar intermitente derecho (2 segundos).
   - Desbloquear todas las puertas.
   - Frenar hasta 0.

3. Parar la grabación:
```bash
Ctrl+C
```

4. Renombrar el archivo para facilitar el trabajo:
```bash
mv candump-*.log logs/secuencia_grabada.log
```

5. Inspeccionar las primeras líneas del log:
```bash
head -20 logs/secuencia_grabada.log
```

Formato de cada línea del log de candump:
```
(1635000000.000000) vcan0 244#0000000050000000
(1635000000.016700) vcan0 188#0000000000000000
(1635000000.033400) vcan0 19B#0F00000000000000
```

---

## Ejercicio C.2 — Reproducir el replay con `canplayer`

### Pasos

1. Detener `controls` (para evitar interferencias con el replay).

2. Reproducir la grabación:
```bash
canplayer -I logs/secuencia_grabada.log
```

Opciones útiles:
```bash
# Reproducir en bucle
canplayer -l 3 -I logs/secuencia_grabada.log

# Reproducir a velocidad doble
canplayer -g 50 -I logs/secuencia_grabada.log
# -g N: gap entre tramas en porcentaje del original (50 = doble velocidad)
```

3. Observar en ICSim que la secuencia se reproduce fielmente: velocímetro sube, intermitente se activa, puertas cambian de estado.

### Preguntas

- ¿El cuadro de mandos puede distinguir entre la acción original y el replay?
- ¿Cuántas veces puedes reproducir el replay con el mismo efecto?
- ¿Qué pasaría si este log fuera de un vehículo real y lo reprodujeras en otro del mismo modelo?

---

## Ejercicio C.3 — Replay selectivo (solo un subconjunto de tramas)

En lugar de reproducir toda la secuencia, filtrar solo las tramas de un ID específico.

```bash
# Extraer solo tramas de puertas (ID 0x19B) del log
grep "19B" logs/secuencia_grabada.log > logs/solo_puertas.log

# Reproducir solo la apertura de puertas
canplayer -I logs/solo_puertas.log
```

O filtrar durante la reproducción:
```bash
canplayer -I logs/secuencia_grabada.log vcan0=vcan0,19B:7FF
```

---

## Ejercicio C.4 — Replay con Python (`replay_attack.py`)

El script `scripts/replay_attack.py` ofrece más control sobre el replay:
- Filtrado por ID.
- Ajuste de timing.
- Opción de loop.
- Logging de tramas enviadas.

```bash
source .venv/bin/activate

# Replay completo
python scripts/replay_attack.py \
    --file logs/secuencia_grabada.log \
    --interface vcan0

# Replay solo ID 0x19B (puertas), 3 veces
python scripts/replay_attack.py \
    --file logs/secuencia_grabada.log \
    --interface vcan0 \
    --filter-id 0x19B \
    --loops 3 \
    --speed 1.5
```

---

## Ejercicio C.5 — Reto: Replay de desbloqueo de puertas en parking

**Escenario simulado:**
> Un atacante observa a la víctima desbloquear su vehículo con el teléfono (app de fabricante via Bluetooth → gateway → CAN bus). Con un dongle conectado al OBD-II del vehículo, graba los 5 segundos anteriores al desbloqueo. Más tarde, reproduce esa captura.

Simular el escenario:
1. Con `controls`, desbloquear las puertas manualmente (simulación de app legítima).
2. Capturar con `candump -l`.
3. Volver a bloquear todas las puertas.
4. Reproducir el log capturado → las puertas se desbloquean solas.

Documentar el ataque en el informe con:
- Captura antes del replay (puertas bloqueadas en ICSim).
- Captura durante el replay (puertas desbloqueadas en ICSim).
- Número de líneas del log que causaron el efecto.

---

## Entregables de la Práctica C

1. Archivo `logs/secuencia_grabada.log` (evidencia de la grabación).
2. Captura de pantalla de ICSim antes y después del replay.
3. Respuestas a las preguntas del Ejercicio C.2.
4. Evidencia del Ejercicio C.5 (escenario parking).

---

## Contramedidas conocidas

| Contramedida | Descripción | Limitación |
|---|---|---|
| Timestamps en capa aplicación | ECU valida que el mensaje no es demasiado antiguo | Requiere sincronización de tiempo segura |
| Números de secuencia (counters) | Cada mensaje lleva un contador incrementado | El atacante puede capturar y manipular el contador |
| MACs (Message Authentication Codes) | Firma HMAC-SHA256 en el payload CAN | Reduce los bytes de datos disponibles (8 bytes es poco) |
| AUTOSAR SecOC | Estándar de autenticación de mensajes CAN | Solo disponible en ECUs AUTOSAR, coste elevado |
| CAN FD + SecOC | Mayor payload (64 bytes) facilita MACs | Requiere hardware CAN FD |

---

## Reflexión final

- ¿Por qué es difícil implementar protección anti-replay en CAN bus?
- Si tuvieras 8 bytes de payload, ¿cuántos bytes dedicarías al MAC y cuántos a los datos?
- ¿Qué información necesita el receptor para verificar un MAC? ¿Cómo se distribuye la clave?
