# Laboratorio de Ciberseguridad CAN Bus — ICSim

> **Práctica independiente** del módulo V16. Esta carpeta contiene un laboratorio autónomo centrado en las vulnerabilidades del protocolo **CAN bus** usando el simulador **ICSim** (Instrument Cluster Simulator) y las herramientas **can-utils**.

---

## ¿Qué aprenderás?

| Competencia | Herramienta |
|---|---|
| Escuchar tráfico CAN en tiempo real | `candump`, `cansniffer` |
| Identificar tramas de interés (ingeniería inversa) | `cansniffer`, scripts Python |
| Inyectar tramas arbitrarias | `cansend`, `python-can` |
| Ejecutar un ataque de replay | `canplayer`, script Python |
| Hacer fuzzing al bus CAN | `cangen`, `fuzz_can.py` |
| Saturar el bus (DoS) | `can_dos.py` |

---

## Arquitectura del laboratorio

```
┌──────────────────────────────────────┐
│          Linux VM / Host             │
│                                      │
│  vcan0 (interfaz CAN virtual)        │
│      │                               │
│      ├── ICSim (cuadro de mandos)    │
│      ├── controls (mando)            │
│      ├── candump / cansniffer        │
│      └── scripts/ (ataques)          │
└──────────────────────────────────────┘
```

> **Alcance:** todas las prácticas de esta rama usan exclusivamente `vcan0` e ICSim. No conectes interfaces CAN físicas.

---

## Requisitos mínimos

### Opción A — Docker (recomendada, sin instalar dependencias)
- **Docker Engine** instalado en Linux. En Windows, ejecuta el laboratorio dentro de una VM Linux.
- **CPU:** 2 núcleos, 4 GB RAM.
- El contenedor incluye ICSim, can-utils, Xvfb, openbox, tint2 y noVNC.

### Opción B — Instalación nativa en Linux
- **Sistema operativo:** Ubuntu 22.04 LTS o Kali Linux 2024+ (VM o bare metal).  
  *Windows no soporta SocketCAN de forma nativa. Ver `lab/03_Setup_entorno_linux.md` para opciones de VM.*
- **CPU:** 2 núcleos, 4 GB RAM.
- **Dependencias:** `can-utils`, `SDL2`, `SDL2_image`, `python3`, `python-can`.
- **ICSim:** compilado desde [https://github.com/zombieCraig/ICSim](https://github.com/zombieCraig/ICSim).

---

## Estructura de carpetas

```
CANbus_ICSim_Ciber/
├── README.md                          ← este archivo
├── RUN_ME_FIRST.md                    ← arranque rápido (10 min)
├── requirements.txt                   ← dependencias Python
├── lab/
│   ├── 01_Introduccion_CANbus.md      ← teoría y contexto
│   ├── 03_Setup_entorno_linux.md      ← setup VM/ICSim paso a paso
│   ├── 04_Practica_A_Reconocimiento.md
│   ├── 05_Practica_B_Inyeccion.md
│   ├── 06_Practica_C_Replay.md
│   └── 07_Practica_D_Fuzzing_DoS.md
├── scripts/
│   ├── setup_vcan.sh                  ← levanta vcan0
│   ├── can_scanner.py                 ← escaneo y log de IDs activos
│   ├── fuzz_can.py                    ← fuzzer de frames CAN
│   ├── replay_attack.py               ← ataque de replay
│   └── can_dos.py                     ← flooding / DoS
├── samples/
│   └── icsim_normal.log               ← captura de tráfico de referencia
├── logs/
│   └── .gitkeep
└── reports/
    └── 00_Plantilla_informe_evidencias.md
```

---

## Prácticas incluidas

| Práctica | Objetivo |
|---|---|
| **A — Reconocimiento** | Escuchar el bus y catalogar IDs y bytes activos |
| **B — Inyección de frames** | Tomar control del cuadro de mandos con `cansend` |
| **C — Replay Attack** | Grabar y reproducir una secuencia de acción |
| **D — Fuzzing y DoS** | Generar tráfico aleatorio y saturar el bus |

---

## Aviso legal y ético

Este laboratorio usa **exclusivamente entornos virtuales** (vcan0 + ICSim). Cualquier uso de estas técnicas sobre vehículos reales sin autorización explícita del propietario es **ilegal** (Ley Orgánica 10/1995, delitos informáticos, art. 264 y ss. CP). El acceso no autorizado a sistemas de control de vehículos puede comprometer la seguridad vial.
