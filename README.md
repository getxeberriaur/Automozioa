# Automozioa — Ciberseguridad en Automoción

[Bertsioa euskaraz](README_eu.md)
Repositorio para participantes con prácticas de laboratorio autónomas, instrucciones de ejecución, scripts, muestras y plantillas de evidencias.

> Todo el contenido está orientado a **formación defensiva en entorno simulado o sandbox**. No debe utilizarse sobre vehículos o infraestructuras reales sin autorización explícita.

---

## Prácticas disponibles

### 1 — Baliza V16 conectada (`Automocion_V16_Ciber/`)

Laboratorio sobre ciberseguridad en el sistema de aviso de emergencia V16 conectado. Simula el envío y validación de eventos de baliza sobre una API REST local.

**Temas:** validación de esquema JSON, anti-replay por nonce, ventana temporal, rate limiting, trazabilidad de eventos.

**Entorno:** Python / FastAPI — funciona en Windows, Linux y macOS.
**Documentación:** [Automocion_V16_Ciber/README.md](Automocion_V16_Ciber/README.md)

---

### 2 — CAN Bus con ICSim (`CANbus_ICSim_Ciber/`)

Laboratorio sobre las vulnerabilidades del protocolo **CAN bus** usando el simulador ICSim (Instrument Cluster Simulator) y las herramientas `can-utils`. Cubre reconocimiento pasivo, inyección de frames, replay y fuzzing/DoS.

**Temas:** protocolo CAN 2.0, ingeniería inversa de tramas, inyección sin autenticación, replay attack, flooding del bus.

**Entorno:** Linux (Ubuntu 22.04 / Kali) con `vcan0` virtual — se puede usar en VM.
**Documentación:** [CANbus_ICSim_Ciber/README.md](CANbus_ICSim_Ciber/README.md)

---

### 3 — CTF Automotive — UrbanFleet 2026 (`CTF_Automotive/`)

Ejercicio integrador tipo **Capture The Flag** de 90 minutos que combina todas las técnicas del lab CAN bus (reconocimiento, inyección, replay, DoS/fuzzing) en un escenario competitivo por equipos.

**Temas:** Red Team en bus CAN, ataque encadenado por fases, defensa y contramedidas, presentación de evidencias.

**Prerequisito:** haber completado `CANbus_ICSim_Ciber/`.

**Entorno:** Linux con ICSim + vcan0 (mismo entorno que la práctica 2).
**Documentación:** [CTF_Automotive/README.md](CTF_Automotive/README.md)

El enunciado y la hoja de entrega están en `CTF_Automotive/lab/`.

### 4 — Análisis RF pasivo (`RF_Lab_Seguro/`)

Captura y análisis de espectro con RTL-SDR y un emisor de prueba aislado. La práctica no incluye transmisión, replay ni interferencia RF.

**Entorno:** Raspberry Pi con RTL-SDR y portátil para el análisis.
**Documentación:** [RF_Lab_Seguro/README.md](RF_Lab_Seguro/README.md)

---

### 4 — V2X Simulación (`V2X_Simulacion_Ciber/`)

Laboratorio local sobre confianza en mensajes V2V/V2I/V2P. Simula CAM, DENM y eventos de infraestructura sin utilizar radio real.

**Temas:** spoofing simulado, replay, autenticación, frescura, plausibilidad física, rate limiting y detección de mensajes anómalos.
**Entorno:** Python 3.10+ y biblioteca estándar; tráfico limitado a `127.0.0.1`.
**Documentación:** [V2X_Simulacion_Ciber/README.md](V2X_Simulacion_Ciber/README.md)

---

## Estructura del repositorio

```text
Automozioa/
├── README.md                          ← este archivo (índice general)
├── README_eu.md                       ← bertsio orokorra euskaraz
│
├── Automocion_V16_Ciber/              ← Práctica 1: Baliza V16
│   ├── README.md
│   ├── README_eu.md
│   ├── RUN_ME_FIRST.md
│   ├── backend/
│   ├── lab/
│   ├── simulator/
│   ├── samples/
│   ├── logs/
│   ├── reports/
│   └── requirements.txt
│
├── CANbus_ICSim_Ciber/                ← Práctica 2: CAN Bus
│   ├── README.md
│   ├── README_eu.md
│   ├── RUN_ME_FIRST.md
│   ├── lab/
│   ├── scripts/
│   ├── samples/
│   ├── logs/
│   ├── reports/
│   └── requirements.txt
│
├── CTF_Automotive/                    ← Práctica 3: CTF integrador
    ├── README.md
    ├── README_eu.md
    ├── lab/
    └── requirements.txt

├── RF_Lab_Seguro/                     ← Práctica 4: análisis RF pasivo
│   ├── README.md
│   ├── QUICKSTART.md
│   ├── docs/
│   ├── scripts/
│   └── templates/
└── V2X_Simulacion_Ciber/              ← Práctica 5: V2X simulado
    ├── README.md
    ├── RUN_ME_FIRST.md
    ├── lab/
    ├── reports/
    └── scripts/
```

---

## Inicio rápido

- V16: [arranque rápido](Automocion_V16_Ciber/RUN_ME_FIRST.md).
- CAN/ICSim: [arranque rápido](CANbus_ICSim_Ciber/RUN_ME_FIRST.md).
- CTF: completa primero el laboratorio CAN y sigue [CTF Automotive](CTF_Automotive/README.md).
- RF: [guía de participantes](RF_Lab_Seguro/QUICKSTART.md).
- V2X: [arranque rápido](V2X_Simulacion_Ciber/RUN_ME_FIRST.md).

---

## Aviso legal

Las prácticas CAN, V16 y V2X se limitan a simuladores o `127.0.0.1`. La práctica RF es exclusivamente de recepción pasiva con un emisor de prueba aislado. No conectes los ejercicios a vehículos, redes CAN físicas ni sistemas RF reales.
