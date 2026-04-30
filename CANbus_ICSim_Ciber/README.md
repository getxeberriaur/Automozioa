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
| Conectar hardware real (opcional) | `usbcan` + BluePill STM32 |

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

> **Nota hardware (opcional):** Si el laboratorio dispone de dongle USB CAN (p.ej. módulo BluePill+HW-184 del proyecto [usbcan](https://github.com/BatchDrake/usbcan)), se puede sustituir `vcan0` por la interfaz física y conectar al bus real de un vehículo de prueba o banco.

---

## Requisitos mínimos

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
│   ├── 02_Checklist_configuracion_laboratorio.md
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
