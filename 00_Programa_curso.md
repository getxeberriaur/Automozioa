# Estructura del Curso: Ciberseguridad en Automoción

[Bertsioa euskaraz](00_Horario_curso_eu.md)

---

## Día 1 — Comunicaciones del vehículo y Ataques

**Objetivo:** Comprender la arquitectura electrónica y aprender a "escuchar" el vehículo.

| Horario | Bloque |
|---|---|
| 09:00 – 09:30 | **Presentación:** Contenidos y objetivos del curso |
| 09:30 – 10:30 | **Teoría: Cambio de Paradigma** |
| 10:30 – 11:30 | **Repaso de Normativa** (UNECE R155) |
| 11:30 – 12:00 | Descanso |
| 12:00 – 14:00 | **I. Práctica: Laboratorio CAN Bus — Práctica A (Reconocimiento pasivo)** |

### 09:30 – 10:30 | Teoría: Cambio de Paradigma

- **Clave:** Antes, la seguridad de un vehículo se asociaba a los frenos o los airbags. Ahora, la seguridad digital (*ciberseguridad*) es esencial para garantizar la seguridad física.
- **Conceptos:** Cada ECU (Electronic Control Unit) es un pequeño ordenador. Un vehículo moderno puede tener más de 100 ECUs comunicadas por Ethernet, CAN y LIN.
- **Ejemplo práctico:** "Jeep Hack" (2015). Cómo lograron controlar el volante y los frenos remotamente a través del sistema de entretenimiento.

### 10:30 – 11:30 | Repaso de Normativa (UNECE R155)

- Organismos reguladores y obligaciones
- Fichas técnicas
- Introducción a ISO/SAE 21434

### 12:00 – 14:00 | I. Práctica — CAN Bus: Práctica A (Reconocimiento pasivo)

> Documentación: [`CANbus_ICSim_Ciber/lab/04_Practica_A_Reconocimiento.md`](CANbus_ICSim_Ciber/lab/04_Practica_A_Reconocimiento.md)

**12:00 – 12:30 — Configurar el entorno**
- Ejecutar `setup_vcan.sh` → levantar interfaz `vcan0`
- Arrancar ICSim (`./icsim vcan0` + `./controls vcan0`)
- Primera vista con `candump vcan0`: la pantalla se llenará de datos
- Reto: ¿qué ocurre al pulsar el acelerador? (buscar el ID `0x244`)

**12:30 – 14:00 — Práctica A: Reconocimiento pasivo**
- `can_scanner.py`: listar todos los IDs con su frecuencia
- `cansniffer`: correlacionar acción ↔ cambio de byte
- Objetivo: identificar los IDs de velocidad, puertas e indicadores de giro

---

## Día 2 — Tipos de Ataque en Redes de Automoción

**Objetivo:** Realizar ataques controlados y comprender la manipulación de datos.

| Horario | Bloque |
|---|---|
| 09:00 – 10:30 | **Teoría: Técnicas de Ingeniería Inversa** |
| 10:30 – 11:30 | **II. Práctica: Laboratorio CAN Bus — Práctica B (Inyección de frames)** |
| 11:30 – 12:00 | Descanso |
| 12:00 – 13:00 | **III. Práctica: Laboratorio CAN Bus — Práctica C (Ataque Replay)** |
| 13:00 – 14:00 | **IV. Práctica: Laboratorio CAN Bus — Práctica D (Fuzzing y DoS)** |

### 09:00 – 10:30 | Teoría: Técnicas de Ingeniería Inversa

**09:00 – 09:15 — Demo proyectada: SavvyCAN (docente)**

> El docente proyecta SavvyCAN conectado a `vcan0` mientras mueve el acelerador en `controls`. Los participantes ven en tiempo real cómo los bytes del ID `0x244` dibujan una curva ascendente — el mismo dato que ayer vieron en texto con `cansniffer`, ahora graficado como lo haría un profesional.
>
> **Mensaje clave:** *"Esta es la herramienta que usan los investigadores y los OEMs. En nuestro lab usamos `cansniffer` y `can_scanner.py`, que son el equivalente por terminal sin configuración adicional."*
>
> Referencia: [SavvyCAN](https://github.com/collin80/SavvyCAN) — GUI de código abierto, soporta SocketCAN (`vcan0`) en Linux.

**09:15 – 10:30 — Ingeniería inversa: teoría y metodología**

- Cómo aislar un comando específico entre miles de tramas por segundo
- Metodología de análisis de tráfico CAN: captura → filtrado → correlación → hipotésis → verificación
- Archivos DBC: cómo la industria documenta las señales CAN (estándar Vector)
- SavvyCAN y la lectura de archivos DBC en contexto real

### 10:30 – 11:30 | II. Práctica — CAN Bus: Práctica B (Inyección de frames)

> Documentación: [`CANbus_ICSim_Ciber/lab/05_Practica_B_Inyeccion.md`](CANbus_ICSim_Ciber/lab/05_Practica_B_Inyeccion.md)

- Inyección de frames con `cansend`: manipular velocímetro, luces y puertas
- Bucle controlado: mantener estado persistente
- Conflicto de nodos: inyección vs. controles legítimos

### 12:00 – 13:00 | III. Práctica — CAN Bus: Práctica C (Ataque Replay)

> Documentación: [`CANbus_ICSim_Ciber/lab/06_Practica_C_Replay.md`](CANbus_ICSim_Ciber/lab/06_Practica_C_Replay.md)

- Grabar secuencia con `candump -l` (apertura de puertas)
- Reproducir automáticamente con `replay_attack.py`
- **Demostración teórica:** ataques en redes inalámbricas — TPMS y Keyless Entry por radiofrecuencia

### 13:00 – 14:00 | IV. Práctica — CAN Bus: Práctica D (Fuzzing y DoS)

> Documentación: [`CANbus_ICSim_Ciber/lab/07_Practica_D_Fuzzing_DoS.md`](CANbus_ICSim_Ciber/lab/07_Practica_D_Fuzzing_DoS.md)

- `fuzz_can.py`: modos random, targeted y mutate
- `can_dos.py`: bus flooding y medición del impacto con `canbusload`
- Documentar comportamientos anómalos observados

---

## Día 3 — Defensa y Aplicación al Aula

**Objetivo:** Proteger el vehículo y transmitir ese conocimiento al alumnado de FP.

| Horario | Bloque |
|---|---|
| 09:00 – 09:30 | **Puerto OBD-II y Security Gateways** |
| 09:30 – 10:15 | **Demo en vivo: Vulnerabilidades en Balizas V16 — CVE-2025-65855** |
| 10:15 – 10:30 | Debate + preguntas |
| 10:30 – 11:30 | **Ciberseguridad en el Taller de Automoción** |
| 11:30 – 12:00 | Descanso |
| 12:00 – 13:30 | **V. Práctica: CTF Automotive — UrbanFleet 2026 (Ejercicio integrador)** |
| 13:30 – 14:00 | **Conclusiones y Evaluación** |

### 09:00 – 09:30 | Puerto OBD-II y Security Gateways

- Cómo los fabricantes están implementando **Security Gateway (SGW)** para bloquear escrituras no autorizadas
- **Concepto:** El puerto OBD-II es para diagnóstico, pero también es una "puerta". Los vehículos nuevos (2020+) tienen Security Gateways que impiden que una herramienta externa escriba en el bus sin certificado digital
- **Debate:** ¿Cómo afecta esto al taller libre? ¿Necesitamos la contraseña del fabricante para cambiar pastillas de freno?

### 09:30 – 10:15 | Demo en vivo — Vulnerabilidades en Balizas V16: CVE-2025-65855

> Documentación completa: [`Automocion_V16_Ciber/lab/05_Demo_Vulnerabilidades_Help_Flash.md`](Automocion_V16_Ciber/lab/05_Demo_Vulnerabilidades_Help_Flash.md)

**09:30 – 09:40 — Arquitectura del sistema V16/DGT 3.0**
- Cómo funciona una baliza V16: GPS → NB-IoT → APN privado → servidor fabricante → DGT 3.0 → Google Maps/paneles
- Dispositivo analizado: **Help Flash IoT** (>250.000 unidades vendidas en España)

**09:40 – 09:50 — Vulnerabilidades (teoría)**
- Vulnerabilidad 1: comunicaciones UDP en claro, sin cifrado ni autenticación (IMEI, GPS, Cell ID expuestos)
- Vector avanzado: fake eNodeB con SDR — interceptar/silenciar todas las balizas en un radio de cientos de metros
- Vulnerabilidad 2: actualización OTA sin autenticación — SSID y contraseña hardcodeados e idénticos en todos los dispositivos

**09:50 – 10:10 — Demo en vivo: ataque OTA (CVE-2025-65855)**

```bash
# 1. AP WiFi falso con las credenciales de todos los dispositivos
nmcli device wifi hotspot ssid "HF-UpdateAP-5JvqFV" password "HF-UpdateAP-5JvqFV"

# 2. Servidor HTTP falso con firmware malicioso
sudo python3 Automocion_V16_Ciber/scripts/fake_ota_server.py --dns

# 3. Mantener el botón de la baliza 8 segundos → descarga automática en ~30-60 s
```

El terminal proyectado muestra en tiempo real cómo el dispositivo descarga el firmware sin verificar identidad ni firma digital.

**10:10 – 10:15 — ¿Cómo se debería hacer?**
- Checklist de lo que falta: MQTT/TLS, credenciales únicas, HTTPS, firma de firmware, Secure Boot
- Marco normativo: UNECE R155, ISO/SAE 21434, ETSI EN 303 645

### 10:15 – 10:30 | Debate y preguntas

- *¿Este dispositivo está homologado por la DGT — qué implica eso sobre el proceso de homologación?*
- *¿Qué medida de bajo coste habría eliminado el 90% del riesgo?*
- CVE-2025-65855 (MITRE) — investigación original: Luis Miranda Acebedo

### 10:30 – 11:30 | Ciberseguridad en el Taller de Automoción

- Riesgos de las herramientas de diagnóstico pirata
- Importancia de las actualizaciones de software (OTA) y gestión de certificados
- Nunca conectar una máquina de diagnóstico a redes públicas
- Cuidado con USB y pendrives en el infotainment del vehículo

### 12:00 – 13:30 | V. Práctica — CTF Automotive: UrbanFleet 2026

> Documentación: [`CTF_Automotive/lab/01_Enunciado_participantes.md`](CTF_Automotive/lab/01_Enunciado_participantes.md)

**Ejercicio integrador — 90 minutos — Individual**

Cada participante asume el rol de Red Team y ejecuta una cadena de ataque de 4 fases sobre el vehículo simulado *UrbanFleet 2026*:

| Fase | Técnica | Duración | Puntos |
|---|---|---|---|
| F1 — Infiltración | Reconocimiento pasivo | 20 min | 150 |
| F2 — Acceso | Inyección de frames | 20 min | 200 |
| F3 — Persistencia | Ataque Replay | 20 min | 150 |
| F4 — Impacto máximo | DoS + Fuzzing | 15 min | 150 |
| Bonus — Defensa | Contramedidas | 15 min | 100 |

### 13:30 – 14:00 | Conclusiones y Evaluación

- Presentación de resultados del CTF y reconocimiento del ganador
- Debate colectivo: ¿qué contramedida habría cortado cada fase del ataque?
- Repaso de normativa: UNECE R155 e ISO/SAE 21434
- Cierre del curso y encuesta de evaluación

---

## Recursos necesarios

### Hardware
- Ordenador del docente (para proyectar ICSim) + un ordenador por participante

### Software (código abierto)
- **Kali Linux** (recomendado) o Ubuntu 22.04 — VM o nativo
- `can-utils`, `python-can`, ICSim, SavvyCAN

### Características (propuesta original)
1. **En parejas recomendado:** Informático/a + Técnico/a de Automoción — mezcla de perfiles; uno ayuda con el terminal y el otro aporta el contexto mecánico del sistema *(también viable en modalidad individual)*
2. **Software:** Kali Linux, todas las herramientas son de código abierto
