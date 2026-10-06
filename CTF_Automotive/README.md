# CTF Automotive — UrbanFleet 2026

[Bertsioa euskaraz](README_eu.md)

Ejercicio integrador de 90 minutos sobre CAN simulado. Requiere completar antes el [laboratorio CAN/ICSim](../CANbus_ICSim_Ciber/README.md) y sus prácticas A-D.

## Entorno

- Linux con ICSim y `vcan0`.
- `can-utils` y Python 3 con las dependencias de `CANbus_ICSim_Ciber/requirements.txt`.
- Todo el ejercicio se limita a `vcan0`; no conectes interfaces CAN físicas ni vehículos.

## Recorrido

1. Prepara el entorno siguiendo [CANbus_ICSim_Ciber/RUN_ME_FIRST.md](../CANbus_ICSim_Ciber/RUN_ME_FIRST.md).
2. Abre el [enunciado](lab/01_Enunciado_participantes.md).
3. Ejecuta las fases únicamente contra ICSim en tu bus virtual local.
4. Registra comandos y evidencias en la [hoja de entrega](lab/03_Hoja_flags_equipo.md).

El CTF combina reconocimiento, inyección, replay y fuzzing/DoS en una simulación local. Respeta en todo momento las normas del enunciado y detén los procesos al terminar.
