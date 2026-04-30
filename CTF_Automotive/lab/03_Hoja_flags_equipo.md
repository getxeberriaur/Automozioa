# CTF Automotive — UrbanFleet 2026
## Hoja de entrega de flags (individual)

[Bertsioa euskaraz](03_Hoja_flags_equipo_eu.md)

---

**Centro:** ________________________________  
**Fecha:** ________________________________  
**Nombre del participante:** ________________________________  
**Curso / grupo:** ________________________________

**Hora de inicio:** ____:____  
**Hora de entrega:** ____:____

---

## Instrucciones

- Completar esta hoja a medida que obtengáis cada flag
- Anotar el comando exacto o nombre del script usado como evidencia
- Indicar la referencia al archivo de captura o pantallazo
- Entregar esta hoja firmada al Game Master al finalizar el tiempo

---

## FASE 1 — Infiltración (Reconocimiento pasivo)

**Hora de finalización de F1:** ____:____

| Flag | Vuestra respuesta | Comando / herramienta usada | Archivo de evidencia |
|---|---|---|---|
| FLAG-F1A (ID velocidad) | `0x` | | |
| FLAG-F1B (ID puertas) | `0x` | | |
| FLAG-F1C (byte giro izq.) | `0x` | | |

**Observaciones / hallazgos adicionales de F1:**

```
(espacio libre para notas)
```

---

## FASE 2 — Acceso (Inyección de frames)

**Hora de finalización de F2:** ____:____

| Flag | Criterio | Comando exacto usado | Archivo de evidencia |
|---|---|---|---|
| FLAG-F2A (velocímetro >200) | ✓ / ✗ | | |
| FLAG-F2B (hazard lights) | ✓ / ✗ | | |
| FLAG-F2C (puertas desbloqueadas) | ✓ / ✗ | | |
| FLAG-F2D (bucle 30 s) | ✓ / ✗ | | |

**Observaciones / script empleado en F2D:**

```python
# Pegar aquí el script o bucle bash usado
```

---

## FASE 3 — Persistencia (Replay attack)

**Hora de finalización de F3:** ____:____

| Flag | Vuestra respuesta | Comando de replay usado | Archivos de log |
|---|---|---|---|
| FLAG-F3 (segundos mínimos) | __ segundos | | |

**Descripción del escenario de replay ejecutado:**

```
(describir brevemente: qué grabasteis, qué filtrasteis, qué se reprodujo)
```

---

## FASE 4 — Impacto máximo (DoS + Fuzzing)

**Hora de finalización de F4:** ____:____

| Flag | Vuestra respuesta | Comando DoS usado | Evidencia canbusload |
|---|---|---|---|
| FLAG-F4 (fps DoS) | ____ fps | | |

**Comportamientos anómalos observados durante fuzzing:**

```
ID objetivo: 0x____
Modo de fuzzing: random / targeted / mutate
Comportamientos observados en ICSim:
-
-
```

---

## FASE BONUS — Contramedidas (Defensa)

| Flag | Opción implementada | Archivo del código |
|---|---|---|
| FLAG-BONUS | A / B / C | |

**Descripción de la contramedida y su limitación:**

```
Contramedida implementada:

Limitación principal:
```

---

## Resumen de puntuación (rellenar el GM)

| Fase | Flags obtenidas | Puntos base | Bonus velocidad | Subtotal |
|---|---|---|---|---|
| F1 | /3 | | | |
| F2 | /4 | | | |
| F3 | /1 | | | |
| F4 | /1 | | | |
| Bonus | /1 | | | |
| **TOTAL** | **/10** | | | |

---

**Firma del participante:** ________________________________  
**Firma del GM:** ________________________________
