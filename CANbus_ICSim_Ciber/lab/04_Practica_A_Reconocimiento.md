# Práctica A — Reconocimiento del bus CAN

[Bertsioa euskaraz](04_Practica_A_Reconocimiento_eu.md)

**Duración estimada:** 45 minutos  
**Dificultad:** Básica  
**Herramientas:** `candump`, `cansniffer`, `scripts/can_scanner.py`

---

## Objetivo

Escuchar el bus CAN del simulador ICSim en modo pasivo, identificar los Arbitration IDs activos y correlacionar cambios en los datos con acciones físicas sobre el mando de control. Al finalizar, el equipo debe ser capaz de elaborar un mapa básico `ID → función`.

---

## Contexto

En una auditoría real de un vehículo, el primer paso siempre es el **reconocimiento pasivo**: conectar al bus (por ejemplo, vía OBD-II) y escuchar sin transmitir. El bus CAN no tiene ningún mecanismo para detectar este tipo de escucha.

El protocolo NO tiene:
- Autenticación de nodos
- Cifrado del tráfico
- Detección de nodos no autorizados

Por eso un atacante con acceso físico puede escuchar todo el tráfico de forma completamente silenciosa.

---

## Prerrequisitos

- `vcan0` activa (ejecutar `sudo bash scripts/setup_vcan.sh`).
- ICSim corriendo (`./ICSim/builddir/icsim vcan0`).
- Controls corriendo (`./ICSim/builddir/controls vcan0`).

---

## Ejercicio A.1 — Captura inicial con `candump`

### Pasos

1. Abrir un terminal y ejecutar:
```bash
candump vcan0
```

2. En la ventana de `controls`, usar el teclado para interactuar con el simulador (acelerar, activar intermitentes, bloquear puertas).

3. Observar la salida de `candump`. Ejemplo de salida esperada:
```
  vcan0  244   [8]  00 00 00 00 1A 00 00 00
  vcan0  188   [8]  00 00 00 00 00 00 00 00
  vcan0  19B   [8]  0F 00 00 00 00 00 00 00
  vcan0  244   [8]  00 00 00 00 2C 00 00 00
  vcan0  188   [8]  01 00 00 00 00 00 00 00
```

4. Guardar la captura a un archivo:
```bash
candump -l vcan0
# Genera archivo candump-YYYYMMDD-HHMMSS.log
```

### Preguntas guiadas

- ¿Cuántos IDs distintos aparecen mientras ICSim está activo?
- ¿Algún ID cambia sus datos cuando pulsas el acelerador?
- ¿Algún ID cambia cuando activas el intermitente izquierdo?

---

## Ejercicio A.2 — Filtrado con `cansniffer`

`cansniffer` muestra solo los bytes que **cambian** en tiempo real — ideal para ingeniería inversa.

### Pasos

1. Ejecutar:
```bash
cansniffer -c vcan0
```

Pantalla de referencia:
```
 delta   ID  data ...
 0.010  244  00 00 00 00 1A 00 00 00
 0.020  188  00 00 00 00 00 00 00 00
 0.010  19B  0F 00 00 00 00 00 00 00
```

Los bytes que cambian se resaltan en **negrita** o con color.

2. Con `cansniffer` activo, hacer las siguientes acciones **de una en una** en `controls`:

| Acción | ¿Qué ID cambia? | ¿Qué byte cambia? | Valor antes | Valor después |
|---|---|---|---|---|
| Acelerar lentamente | | | | |
| Acelerar al máximo | | | | |
| Frenar | | | | |
| Intermitente izquierdo | | | | |
| Intermitente derecho | | | | |
| Bloquear puerta 1 | | | | |
| Desbloquear puerta 1 | | | | |

Completar la tabla en el informe.

---

## Ejercicio A.3 — Escaneo automático con `can_scanner.py`

El script `scripts/can_scanner.py` captura tráfico durante 30 segundos y genera un resumen estadístico de los IDs activos.

```bash
source .venv/bin/activate
python scripts/can_scanner.py --interface vcan0 --duration 30 --output logs/scan_resultado.txt
```

Salida esperada (ejemplo):
```
=== CAN Bus Scan — vcan0 ===
Duración: 30.0 s | Tramas totales: 3621

ID       Tramas    Freq(Hz)   Min_DLC  Max_DLC   Bytes cambiantes
------   ------    --------   -------  -------   ----------------
0x188      1204      40.1       8        8        [0]
0x19B       602      20.1       8        8        [0]
0x244      1815      60.5       8        8        [3, 4]
```

### Preguntas guiadas

- ¿Cuál es el ID con mayor frecuencia de envío?
- ¿Qué ID tiene el byte más variable?
- ¿Con qué frecuencia (Hz) se envía el ID de velocidad?

---

## Ejercicio A.4 — Captura dirigida por ID

Una vez identificados los IDs de interés, filtrar solo ese tráfico:

```bash
# Solo mostrar ID 0x244
candump vcan0,244:7FF

# Solo mostrar IDs 0x188 y 0x19B
candump vcan0,188:7FF vcan0,19B:7FF
```

Guardar capturas filtradas:
```bash
candump -l vcan0,244:7FF
```

---

## Entregables de la Práctica A

Completar en el informe de evidencias (`reports/00_Plantilla_informe_evidencias.md`):

1. **Tabla de IDs identificados** con frecuencia, DLC y función inferida.
2. **Tabla de correlación** acción → ID → byte → valor (del Ejercicio A.2).
3. **Captura de pantalla** de `cansniffer` mostrando bytes cambiantes.
4. **Archivo de log** generado por `can_scanner.py`.

---

## Mapa de referencia (ICSim modo no aleatorio)

> Desvelar solo al final de la práctica, para que los participantes lo descubran por sí mismos.

| CAN ID | Función | Byte | Descripción |
|---|---|---|---|
| `0x244` | Velocidad | Byte 3 | 0x00=0 km/h, 0xFF=máximo |
| `0x188` | Intermitentes | Byte 0 | `0x01`=izquierda, `0x02`=derecha, `0x03`=ambos |
| `0x19B` | Puertas | Byte 0 | bits 0-3 = puertas 1-4 (1=abierta/desbloqueada) |

---

## Reflexión final

- ¿Por qué es peligroso que el CAN bus no tenga autenticación?
- ¿Cómo podría un atacante usar esta información en un vehículo real?
- ¿Qué mitigaciones existen en los vehículos modernos para dificultar este mapeo?
