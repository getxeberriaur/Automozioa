# Introducción al protocolo CAN Bus y su superficie de ataque

[Bertsioa euskaraz](01_Introduccion_CANbus_eu.md)

## 1. ¿Qué es el CAN bus?

El **Controller Area Network (CAN)** es un protocolo de comunicación en serie desarrollado por Bosch en 1983, diseñado para permitir que microcontroladores y dispositivos se comuniquen entre sí sin necesidad de un ordenador central. Desde la década de 1990 es el estándar de facto en la electrónica de automoción.

### 1.1 Características fundamentales

| Característica | Valor |
|---|---|
| Velocidad máxima | Hasta 1 Mbit/s (CAN 2.0) |
| Topología | Bus lineal con terminación en cada extremo |
| Modelo de comunicación | Broadcast — todos los nodos ven todos los mensajes |
| Longitud máxima de datos | 8 bytes por trama (CAN 2.0), 64 bytes (CAN FD) |
| Arbitraje | Por prioridad (ID más bajo = mayor prioridad) |
| Detección de errores | CRC, ACK, bit stuffing, error framing |
| Autenticación | **Ninguna** (por diseño) |
| Cifrado | **Ninguno** (por diseño) |

---

## 2. Estructura de una trama CAN 2.0A

```
┌─────┬──────────────┬─────┬─────────┬──────────────────┬─────┬─────┬─────┐
│ SOF │ Arbitration  │ RTR │ Control │ Data (0-8 bytes) │ CRC │ ACK │ EOF │
│  1b │  ID (11 bit) │  1b │   6b    │    0-64 bits     │ 16b │  2b │  7b │
└─────┴──────────────┴─────┴─────────┴──────────────────┴─────┴─────┴─────┘
```

- **SOF**: Start of Frame — bit dominante (0) que inicia la trama.
- **Arbitration ID**: Identifica el tipo de mensaje y su prioridad.
- **RTR**: Remote Transmission Request — solicitud de datos (no se usa en inyección).
- **DLC**: Data Length Code — número de bytes de datos (0-8).
- **Data**: El contenido del mensaje (hasta 8 bytes).
- **CRC**: 15 bits de comprobación de errores + delimitador.
- **ACK**: Cualquier nodo que reciba correctamente el mensaje responde con un bit ACK dominante.

---

## 3. Arquitectura de red en vehículos modernos

Los vehículos modernos pueden tener entre **40 y 100 ECUs** (Electronic Control Units) distribuidas en varios buses CAN separados por **gateways**:

```
┌─────────────────────────────────────────────────────┐
│                     GATEWAY ECU                     │
│                                                     │
│  CAN Bus Powertrain  │  CAN Bus Carrocería  │  LIN  │
│  ─────────────────   │  ─────────────────   │  ───  │
│  Motor, Transmisión  │  Luces, Puertas      │  Asientos│
│  ABS, ESC            │  Climatización       │  Espejos │
│                      │  Airbags             │         │
└─────────────────────────────────────────────────────┘
         │
   OBD-II Port (acceso diagnóstico — punto de entrada)
```

---

## 4. Superficie de ataque del protocolo CAN

### 4.1 Vulnerabilidades inherentes al diseño

El protocolo CAN fue diseñado en los años 80 pensando en **fiabilidad**, no en **seguridad**. Sus principales debilidades son:

1. **Sin autenticación:** Cualquier nodo puede enviar tramas con cualquier ID arbitrario.
2. **Sin cifrado:** Todo el tráfico es en claro y puede ser capturado por cualquier nodo.
3. **Broadcast total:** Todos los nodos reciben todos los mensajes.
4. **Sin control de origen:** No hay forma de verificar qué nodo envió un mensaje.
5. **Prioridad por ID:** Un atacante puede saturar el bus con frames de ID=0x000.

### 4.2 Vectores de acceso físico

| Vector | Descripción |
|---|---|
| Puerto OBD-II | Acceso directo al bus diagnóstico (bajo el volante) |
| Unidad de infoentretenimiento | Puede conectarse al bus principal |
| Módulo Bluetooth/Wi-Fi | Acceso remoto si hay vulnerabilidad en la pila de red |
| ECU comprometida | Un nodo comprometido puede atacar a todos los demás |
| Cable de carga / USB | Algunos vehículos EV exponen interfaces de red |

---

## 5. Tipos de ataque sobre CAN bus

### 5.1 Ataque de reconocimiento (pasivo)

Escuchar el bus con `candump` para catalogar qué IDs existen, con qué frecuencia y qué datos transportan. No requiere transmitir nada — es completamente indetectable.

### 5.2 Ingeniería inversa

Correlacionar la activación de funciones físicas (pulsar un botón, girar el volante) con los cambios en los datos de ciertas tramas. Objetivo: mapear `ID → función → byte → valor`.

### 5.3 Inyección de frames

Enviar tramas falsas con `cansend` o scripts. El bus no puede distinguir una trama legítima de una falsa. Permite:
- Activar funciones sin que el conductor lo haga (intermitentes, bloqueo de puertas...).
- Suplantar lecturas de sensores (velocidad falsa, temperatura falsa...).
- Desactivar sistemas de seguridad (frenos, airbags...) — **muy peligroso en entorno real**.

### 5.4 Ataque de replay

Grabar una secuencia de tramas con `candump` y reproducirla luego con `canplayer`. Permite reproducir acciones sin comprender los datos (por ejemplo, abrir las puertas porque se grabó el momento de desbloqueo).

### 5.5 Fuzzing

Enviar tramas con IDs y datos aleatorios (`cangen`) para provocar comportamientos inesperados en las ECUs: reinicios, congelaciones, estados de error.

### 5.6 Denegación de servicio (DoS)

Inundar el bus con tramas de prioridad máxima (ID=0x000). Las ECUs legítimas no pueden arbitrar y el bus queda saturado. En un vehículo real puede provocar que los frenos o la dirección dejen de responder.

---

## 6. Herramientas del ecosistema CAN

### 6.1 can-utils (Linux)

| Herramienta | Uso |
|---|---|
| `candump` | Captura de tráfico |
| `cansend` | Envío de una trama |
| `cangen` | Generación de tráfico aleatorio |
| `cansniffer` | Filtrado y visualización de cambios |
| `canplayer` | Reproducción de capturas |
| `canbusload` | Estadísticas de carga del bus |
| `isotpdump` | Captura de mensajes ISO-TP (diagnóstico) |

### 6.2 Python

| Librería | Uso |
|---|---|
| `python-can` | API Python para CAN (socketcan, kvaser, vector...) |
| `cantools` | Decodificación con ficheros DBC |
| `scapy` | Soporte CAN en Scapy para crafting avanzado |

### 6.3 Hardware

| Dispositivo | Conexión | Precio aprox. |
|---|---|---|
| BluePill+ STM32 + HW-184 (usbcan) | USB→vcan | ~10€ |
| USB2CAN (8devices) | USB→SocketCAN | ~80€ |
| Kvaser Leaf Light | USB→SocketCAN | ~300€ |
| CANable | USB→SocketCAN | ~30€ |
| Raspberry Pi + MCP2515 | SPI→SocketCAN | ~40€ |

---

## 7. Marco legal y ético

> **IMPORTANTE:** Las técnicas de este laboratorio se practican **exclusivamente** sobre el entorno virtual `vcan0 + ICSim`. El acceso no autorizado a sistemas CAN de vehículos reales está tipificado como delito informático en el Código Penal español (art. 264 y ss.) y puede comprometer gravemente la seguridad vial.

Un investigador de seguridad que trabaje con vehículos reales debe:
1. Obtener autorización escrita del propietario.
2. Trabajar en un entorno controlado (banco de pruebas, vehículo inmovilizado).
3. Documentar y comunicar los hallazgos de forma responsable (responsible disclosure).
4. Nunca poner en riesgo a terceros.

---

## 8. Referencias

- ISO 11898: CAN bus standard.
- "The Car Hacker's Handbook" — Craig Smith (OpenGarages), No Starch Press.
- ICSim: [https://github.com/zombieCraig/ICSim](https://github.com/zombieCraig/ICSim)
- can-utils: [https://github.com/linux-can/can-utils](https://github.com/linux-can/can-utils)
- usbcan (BatchDrake): [https://github.com/BatchDrake/usbcan](https://github.com/BatchDrake/usbcan)
- python-can: [https://python-can.readthedocs.io](https://python-can.readthedocs.io)
