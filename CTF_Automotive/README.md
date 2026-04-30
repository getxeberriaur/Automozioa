# CTF Automotive — UrbanFleet 2026

[Bertsioa euskaraz](README_eu.md)

> Ejercicio integrador de ciberseguridad en automoción: ataque/defensa sobre bus CAN simulado.  
> Duración: **90 minutos** · **Individual** · Nivel: FP Ciberseguridad / Automoción

---

## Descripción

CTF temático donde cada participante asume el rol de un **Red Team** atacando la ECU de telemetría de un vehículo de la flota ficticia *UrbanFleet 2026*.  
El entorno es completamente virtual: [ICSim](https://github.com/zombieCraig/ICSim) como simulador del cuadro de instrumentos y `vcan0` como interfaz CAN virtual. No se requiere hardware real.

## Prerequisito obligatorio

Este CTF **requiere haber completado** el laboratorio [`CANbus_ICSim_Ciber/`](../CANbus_ICSim_Ciber/README.md).  
Las herramientas y conceptos de las 4 prácticas (A, B, C, D) se combinan aquí en un escenario competitivo.

## Estructura del CTF

```
CTF_Automotive/
├── README.md                              ← este archivo
├── README_eu.md
├── RUN_ME_FIRST.md                        ← arranque rápido (Game Master)
├── RUN_ME_FIRST_eu.md
├── requirements.txt
└── lab/
    ├── 01_Enunciado_participantes.md      ← distribuir a equipos al inicio
    ├── 01_Enunciado_participantes_eu.md
    ├── 02_Checklist_docente.md            ← solo Game Master
    ├── 02_Checklist_docente_eu.md
    ├── 03_Hoja_flags_equipo.md            ← una copia por equipo
    ├── 03_Hoja_flags_equipo_eu.md
    ├── 04_Respuestas_master.md            ← ¡CONFIDENCIAL! solo docente
    └── 04_Respuestas_master_eu.md
```

## Resumen de fases

| Fase | Técnica | Duración | Flags | Puntos |
|---|---|---|---|---|
| F1 — Infiltración | Reconocimiento pasivo | 20 min | 3 | 150 |
| F2 — Acceso | Inyección de frames | 20 min | 4 | 200 |
| F3 — Persistencia | Replay attack | 20 min | 1 | 150 |
| F4 — Impacto | DoS + Fuzzing | 15 min | 1 | 150 |
| Bonus — Defensa | Contramedida implementada | 15 min | 1 | 100 |
| **Total** | | **90 min** | **10 flags** | **750 pts** |

## Flujo para el docente

1. Leer [`RUN_ME_FIRST.md`](RUN_ME_FIRST.md) y verificar el entorno (30 min antes)
2. Imprimir [`04_Respuestas_master.md`](lab/04_Respuestas_master.md) — **no compartir**
3. Distribuir [`01_Enunciado_participantes.md`](lab/01_Enunciado_participantes.md) a cada participante
4. Entregar una copia de [`03_Hoja_flags_equipo.md`](lab/03_Hoja_flags_equipo.md) a cada participante
5. Arrancar el cronómetro y actuar como Game Master

## Variantes de dificultad

| Nivel | Modificación |
|---|---|
| Básico | Se entrega la tabla parcial de IDs (solo faltan los bytes) |
| Estándar | Sin pistas — todo desde cero (recomendado) |
| Avanzado | Se añaden IDs de ruido con `cangen` para dificultar reconocimiento |
| Expert | Igual que avanzado + `cansniffer` eliminado del toolset permitido |

## Aviso legal

Este ejercicio se realiza exclusivamente sobre infraestructura virtual controlada en aula.  
Aplicar estas técnicas sobre vehículos reales sin autorización escrita es ilegal según el Código Penal español (art. 197 y 264) y la Directiva NIS2.  
El docente es responsable de velar por el uso ético de los conocimientos adquiridos.
