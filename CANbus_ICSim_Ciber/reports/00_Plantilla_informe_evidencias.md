# Plantilla de informe de evidencias — Laboratorio CAN Bus (equipo)

## 1) Datos del equipo

- Centro:
- Curso / grupo:
- Equipo nº:
- Integrantes:
- Fecha:
- Docente:

---

## 2) Objetivo de la práctica

Describir en 3-5 líneas qué se ha validado en el laboratorio (análisis de tráfico CAN, ataques de inyección, replay y fuzzing sobre ICSim).

---

## 3) Entorno utilizado

- Sistema operativo:
- Versión del kernel Linux:
- Versión de can-utils (`candump --version`):
- Versión de python-can (`python -c "import can; print(can.__version__)"`):
- ICSim compilado y operativo: Sí / No
- Interfaz `vcan0` operativa (`ip link show vcan0`): Sí / No

---

## 4) Práctica A — Reconocimiento

### 4.1 Tabla de IDs identificados

| CAN ID | Frecuencia (Hz) | DLC | Función inferida |
|---|---|---|---|
| | | | |
| | | | |
| | | | |

### 4.2 Tabla de correlación acción → bus

| Acción en controls | CAN ID | Byte | Valor antes | Valor después |
|---|---|---|---|---|
| Acelerar al máximo | | | | |
| Frenar | | | | |
| Intermitente izquierdo | | | | |
| Intermitente derecho | | | | |
| Desbloquear puerta 1 | | | | |

### 4.3 Captura de pantalla

> [Adjuntar captura de `cansniffer` mostrando bytes cambiantes]

### 4.4 Observaciones

---

## 5) Práctica B — Inyección de frames

### 5.1 Casos ejecutados

| Acción inyectada | Comando `cansend` | Resultado observado en ICSim | ¿OK? |
|---|---|---|---|
| Velocímetro al máximo | `cansend vcan0 244#00000000FF000000` | | |
| Intermitente izquierdo | `cansend vcan0 188#0100000000000000` | | |
| Luces de emergencia | `cansend vcan0 188#0300000000000000` | | |
| Desbloquear todas las puertas | `cansend vcan0 19B#0000000000000000` | | |
| Secuencia compuesta (reto B.4) | (script adjunto) | | |

### 5.2 Evidencias

> [Captura de pantalla de ICSim con velocímetro al máximo por inyección]

> [Captura de pantalla de ICSim con intermitentes activos por inyección]

### 5.3 Resultado del conflicto de nodos (B.5)

- ¿Gana la inyección o el controls legítimo? ¿Por qué?

---

## 6) Práctica C — Replay Attack

### 6.1 Secuencia grabada

- Duración de la grabación:
- Número de tramas capturadas:
- IDs presentes en el log:

### 6.2 Resultado del replay

| Intento | ¿El ICSim reprodujo la secuencia? | Observaciones |
|---|---|---|
| Replay completo | | |
| Replay solo puertas | | |
| Replay en bucle ×3 | | |

### 6.3 Evidencias

> [Captura antes del replay — puertas bloqueadas]

> [Captura durante el replay — puertas desbloqueadas]

### 6.4 Escenario parking (C.5)

- Descripción del ataque ejecutado:
- Número de tramas que provocaron el desbloqueo:

---

## 7) Práctica D — Fuzzing y DoS

### 7.1 Fuzzing

| Modo de fuzzing | Duración | Tramas enviadas | Comportamientos anómalos observados |
|---|---|---|---|
| random | | | |
| targeted (0x244) | | | |
| mutate | | | |

### 7.2 Denegación de Servicio

| Métrica | Condición normal | Durante el DoS |
|---|---|---|
| Carga del bus (%) | | |
| Respuesta del controls | Sí | |
| Velocímetro actualizable | Sí | |

### 7.3 Evidencias

> [Captura de `canbusload` durante el flooding]

> [Captura de ICSim congelado durante el DoS]

---

## 8) Análisis técnico

### 8.1 Vulnerabilidades identificadas

| Vulnerabilidad | Práctica donde se demuestra | Impacto potencial (real) |
|---|---|---|
| Sin autenticación de origen | A, B | Inyección de comandos |
| Sin anti-replay | C | Replay de desbloqueo |
| Sin control de flujo | D (DoS) | Saturación del bus |
| Broadcast total | A | Escucha pasiva indetectable |

### 8.2 ¿Cuál es el ataque más peligroso en un vehículo real? Justificación

### 8.3 Contramedidas propuestas

| Ataque | Contramedida | Factibilidad (alta/media/baja) |
|---|---|---|
| Inyección | | |
| Replay | | |
| DoS | | |

---

## 9) Conclusiones

- Conclusión principal (1-2 frases):
- Aprendizaje técnico más relevante:
- Mejora que propondrías para el laboratorio:

---

## 10) Archivos adjuntos

- [ ] `logs/secuencia_grabada.log` (Práctica C)
- [ ] `logs/scan_resultado.txt` (Práctica A)
- [ ] `logs/fuzz_session.log` (Práctica D)
- [ ] Script de secuencia compuesta (Práctica B, reto B.4)
- [ ] Capturas de pantalla (mínimo 5)
