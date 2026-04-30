# Automozioa — Ciberseguridad en Automoción

[Bertsioa euskaraz](README_eu.md)
> **Programa completo del curso (3 días):** [00_Programa_curso.md](00_Programa_curso.md)
Repositorio de materiales docentes y laboratorios prácticos sobre **ciberseguridad en automoción**. Cada carpeta contiene una práctica autónoma con documentación, scripts y plantillas de evidencias.

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
└── CTF_Automotive/                    ← Práctica 3: CTF integrador
    ├── README.md
    ├── README_eu.md
    ├── RUN_ME_FIRST.md
    ├── lab/
    └── requirements.txt
```

---

## Público objetivo

- Profesorado de FP (Automoción, Informática, Ciberseguridad) y universidad.
- Equipos técnicos que quieran montar demostraciones de seguridad en automoción conectada.
- Estudiantes con interés en ciberseguridad aplicada a sistemas embebidos y CAN bus.

---

## Aviso legal

El uso de las técnicas demostradas en estos laboratorios sobre sistemas reales sin autorización expresa es ilegal y puede comprometer la seguridad vial. Todos los entornos están diseñados para funcionar en sandbox local o red completamente aislada.
