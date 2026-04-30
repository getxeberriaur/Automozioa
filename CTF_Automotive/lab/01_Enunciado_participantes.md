# CTF Automotive — UrbanFleet 2026
## Enunciado para participantes

[Bertsioa euskaraz](01_Enunciado_participantes_eu.md)

---

## Escenario

> **[COMUNICADO INTERNO — RED TEAM AUTORIZADO]**
>
> La empresa de car-sharing **UrbanFleet 2026** ha desplegado 200 vehículos conectados en el área metropolitana. Su ECU de telemetría central fue instalada con la configuración por defecto de fábrica y nunca fue auditada.
>
> Se ha detectado actividad sospechosa en el parking subterráneo del edificio corporativo. El departamento de seguridad ha contratado a vuestro equipo para realizar un **ejercicio de Red Team autorizado** y demostrar el impacto real de un atacante con acceso físico al conector OBD-II del vehículo.
>
> Disponéis de **90 minutos**. El vehículo objetivo está simulado mediante ICSim en `vcan0`.

---

## Normas

1. Solo podéis interactuar con la interfaz `vcan0` — nunca con interfaces físicas reales
2. Está prohibido atacar sistemas ajenos al entorno de laboratorio
3. Cada flag debe entregarse al Game Master (GM) con evidencia (comando + captura)
4. El GM puede pedir explicación oral de cualquier flag antes de validarla
5. En caso de empate en puntos, gana el equipo con menor tiempo total

---

## Herramientas disponibles

```
candump       cansend       cansniffer    cangen        canplayer
canbusload    can_scanner.py             replay_attack.py
fuzz_can.py   can_dos.py    python3       wireshark (opcional)
```

Todas las herramientas están en `PATH` o en `../CANbus_ICSim_Ciber/scripts/`.

---

## FASE 1 — Infiltración (Reconocimiento pasivo) · 20 min · 150 pts

**Contexto:** *El atacante conecta un sniffer silencioso. No debe emitir ningún frame.*

**Objetivos:**
1. Capturar tráfico del bus durante al menos 60 segundos sin emitir frames
2. Calcular la frecuencia (Hz) de cada ID presente en el bus
3. Identificar qué ID controla la velocidad del vehículo
4. Identificar qué ID controla las puertas
5. Identificar qué valor del byte 0 activa el indicador de giro izquierdo

**Flags de esta fase:**
- `FLAG-F1A`: El ID (en hex) que controla la velocidad
- `FLAG-F1B`: El ID (en hex) que controla las puertas
- `FLAG-F1C`: El valor hex del byte 0 que activa el giro izquierdo en el ID de señales

**Evidencias requeridas:**
- Captura del log de `candump`
- Tabla de IDs con frecuencia en Hz (usar `can_scanner.py`)
- Pantallazos de `cansniffer` correlacionando acciones con cambios de byte

---

## FASE 2 — Acceso (Inyección de frames) · 20 min · 200 pts

**Contexto:** *El vehículo está aparcado. El atacante ha conectado un dispositivo al OBD-II.*

**Objetivos:**
1. Subir el velocímetro a más de 200 km/h mediante inyección
2. Activar las luces de emergencia (hazard lights)
3. Desbloquear todas las puertas del vehículo
4. Mantener el estado de control activo durante 30 segundos consecutivos (script en bucle)

**Flags de esta fase:**
- `FLAG-F2A`: Captura de ICSim con velocímetro >200 km/h + el comando exacto usado
- `FLAG-F2B`: Captura de ICSim con luces de emergencia activas + comando
- `FLAG-F2C`: Captura de ICSim con puertas desbloqueadas + comando
- `FLAG-F2D`: Script de bucle funcionando 30 s + captura del terminal con el bucle activo

**Evidencias requeridas:**
- Pantallazos del ICSim para cada estado
- Comandos exactos o script empleado

---

## FASE 3 — Persistencia (Replay attack) · 20 min · 150 pts

**Contexto:** *El atacante grabó una secuencia legítima durante la ronda del vigilante. Horas después la reproduce sin estar presente.*

**Objetivos:**
1. Grabar al menos 30 segundos de tráfico mientras se usa `controls` normalmente (incluye abrir puertas)
2. Filtrar del log solo los frames de puertas y reproducirlos
3. Medir cuántos segundos de grabación bastan para capturar un evento de desbloqueo completo

**Flag de esta fase:**
- `FLAG-F3`: Número entero de segundos mínimos de grabación que garantizan capturar el evento de desbloqueo (formato: `FLAG-F3: Xs`)

**Evidencias requeridas:**
- Archivo `.log` de la grabación
- Comando de `replay_attack.py` usado
- Capturas de ICSim antes y después del replay

---

## FASE 4 — Impacto máximo (DoS + Fuzzing) · 15 min · 150 pts

**Contexto:** *Como distracción mientras se roba el vehículo, el atacante satura el bus para inutilizar el cuadro de instrumentos.*

**Objetivos:**
1. Medir la carga base del bus en condiciones normales (`canbusload`)
2. Lanzar un ataque DoS y demostrar que la carga supera el 80%
3. Verificar que el ICSim deja de responder durante el DoS
4. Ejecutar fuzzing dirigido sobre el ID de velocidad y documentar comportamientos anómalos

**Flag de esta fase:**
- `FLAG-F4`: Tasa de frames/segundo alcanzada durante el DoS (formato: `FLAG-F4: XXXXfps`)

**Evidencias requeridas:**
- Captura de `canbusload` en condiciones normales vs DoS
- Pantallazos del ICSim congelado durante el ataque
- Log del fuzzing con al menos un comportamiento anómalo documentado

---

## FASE BONUS — Contramedidas (Defensa) · 15 min · 100 pts

**Contexto:** *El equipo de Blue Team propone e implementa una contramedida técnica real.*

Implementar **al menos una** de las siguientes opciones en Python usando `python-can`:

**Opción A — Detector de anomalías por frecuencia:**  
Si un ID supera 2× su frecuencia basal → imprimir alerta por consola

**Opción B — Whitelist de IDs:**  
Leer el bus y descartar silenciosamente cualquier frame cuyo ID no esté en una lista blanca predefinida (0x244, 0x188, 0x19B)

**Opción C — Rate limiter por ID:**  
Máximo N frames/segundo por ID; los frames que superen el límite se descartan y se registran en log

**Flag de esta fase:**
- `FLAG-BONUS`: Demo en vivo de la contramedida funcionando + código fuente

---

## Puntuación y bonificaciones

| Fase | Puntos base | Bonus velocidad |
|---|---|---|
| F1 — Reconocimiento | 150 (50 por flag) | +50 si todas las F1 en <15 min |
| F2 — Inyección | 200 (50 por flag) | +50 si todas las F2 en <15 min |
| F3 — Replay | 150 | +50 si en <15 min |
| F4 — DoS/Fuzzing | 150 | +25 si en <10 min |
| Bonus — Defensa | 100 | — |
| **Máximo posible** | **750 pts** | **+175 pts** |

---

## Entregables finales

Al terminar el tiempo, entregar al GM la hoja `03_Hoja_flags_equipo.md` completada con:
- Todos los flags obtenidos
- Referencias a evidencias (nombre de archivo de captura/script)
- Respuesta oral a las preguntas de validación del GM
