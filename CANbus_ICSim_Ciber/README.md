# CAN bus laborategia — ICSim

[Abiarazte azkarra](RUN_ME_FIRST.md)

ICSim simulagailuarekin eta `vcan0` interfaze birtualarekin egiten den CAN bus laborategia. Jarduerak simulagailuan soilik egin; ez konektatu CAN interfaze fisikorik edo ibilgailurik.

## Praktikak

1. [Sarrera eta testuingurua](lab/01_Introduccion_CANbus_eu.md)
2. [Linux edo makina birtualaren konfigurazioa](lab/03_Setup_entorno_linux_eu.md)
3. [A — Bus-aren ezagutza pasiboa](lab/04_Practica_A_Reconocimiento_eu.md)
4. [B — Frame-injekzioa](lab/05_Practica_B_Inyeccion_eu.md)
5. [C — Replay-a](lab/06_Practica_C_Replay_eu.md)
6. [D — Fuzzing-a eta DoS-a](lab/07_Practica_D_Fuzzing_DoS_eu.md)

## Baldintzak

- Linux (Ubuntu edo Kali) edo Linux makina birtual bat.
- `vcan0`, ICSim eta `can-utils`.
- Python 3 eta `requirements.txt` fitxategiko mendekotasunak.

Windowsen, erabili Linux VM bat; Docker Desktop Windows-en ez da `vcan0` laborategi honetarako egokia. Xehetasunak konfigurazio-gidan daude.

## Ebidentziak

Gorde komandoak, behaketak eta pantaila-argazkiak euskarazko [txosten-txantiloian](reports/00_Ebidentzia_txosten_txantiloia.md). Praktika guztiak `vcan0` + ICSim-en soilik egin behar dira.
