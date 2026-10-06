# CTF Automotive — UrbanFleet 2026

[Gaztelaniazko bertsioa](README.md)

> Ibilgailuen zibersegurtasuneko CTF integratzailea: eraso/defentsa CAN bus simulatu baten gainean.  
> Iraupena: **90 minutu** · **Banakakoa** · Maila: LH Zibersegurtasuna / Automozioa

---

## Deskribapena

CTF tematikoa, non parte-hartzaile bakoitzak **Red Team** baten rola hartzen duen *UrbanFleet 2026* flota fiktizioko ibilgailu baten telemetria ECU bat erasotuz.  
Ingurunea guztiz birtuala da: [ICSim](https://github.com/zombieCraig/ICSim) aginte-panelaren simulagailu gisa eta `vcan0` CAN interfaze birtual gisa. Ez da hardware errealrik behar.

# CTF Automotive — UrbanFleet 2026

[Gaztelaniazko bertsioa](README.md)

90 minutuko ariketa integratzailea CAN simulatuaren gainean. Aurretik [CAN/ICSim laborategia](../CANbus_ICSim_Ciber/README_eu.md) eta A-D praktikak osatu behar dira.

## Ingurunea

- Linux ICSim eta `vcan0`-rekin.
- `can-utils` eta Python 3, `CANbus_ICSim_Ciber/requirements.txt` fitxategiko mendekotasunekin.
- Ariketa osoa `vcan0`-ra mugatzen da; ez konektatu CAN interfaze fisikorik edo ibilgailurik.

## Ibilbidea

1. Prestatu ingurunea [CANbus_ICSim_Ciber/RUN_ME_FIRST_eu.md](../CANbus_ICSim_Ciber/RUN_ME_FIRST_eu.md) jarraituz.
2. Ireki [enuntziatua](lab/01_Enunciado_participantes_eu.md).
3. Egin faseak ICSim-en soilik, tokiko bus birtualean.
4. Erregistratu komandoak eta ebidentziak [entrega-orrian](lab/03_Hoja_flags_equipo_eu.md).

CTF-ak ezagutza, injekzioa, replay-a eta fuzzing/DoS-a konbinatzen ditu tokiko simulazio batean. Errespetatu enuntziatuko arauak eta gelditu prozesuak amaitzean.
    ├── 03_Hoja_flags_equipo_eu.md
