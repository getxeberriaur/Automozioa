# CTF Automotive — UrbanFleet 2026

90 minutuko ariketa integratzailea CAN bus simulatuaren gainean. Aurretik [CAN/ICSim laborategia](../CANbus_ICSim_Ciber/README.md) eta A-D praktikak osatu behar dira.

## Ingurunea

- Linux ICSim eta `vcan0`-rekin.
- `can-utils` eta Python 3, `CANbus_ICSim_Ciber/requirements.txt` mendekotasunekin.
- Ariketa osoa `vcan0`-ra mugatzen da; ez konektatu CAN interfaze fisikorik edo ibilgailurik.

## Ibilbidea

1. Prestatu ingurunea [CAN laborategiaren abiarazte-gida](../CANbus_ICSim_Ciber/RUN_ME_FIRST.md) jarraituz.
2. Ireki [parte-hartzaileen enuntziatua](lab/01_Enunciado_participantes_eu.md).
3. Egin faseak ICSim-en, tokiko bus birtualean soilik.
4. Erregistratu komandoak eta ebidentziak [entrega-orrian](lab/03_Hoja_flags_equipo_eu.md).

CTF-ak ezagutza, injekzioa, replay-a eta fuzzing/DoS-a lantzen ditu simulazioan. Jarraitu enuntziatuko segurtasun-arauak eta gelditu prozesuak amaitzean.
