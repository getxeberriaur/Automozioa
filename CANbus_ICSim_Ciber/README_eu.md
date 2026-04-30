# CAN Bus Zibersegurtasun Laborategia — ICSim

[Gaztelaniazko bertsioa](README.md)

> **V16 modulutik independentea.** Karpeta honek **CAN bus** protokoloaren ahuleziak ikertzen dituen laborategi autonomo bat dauka, **ICSim** (Instrument Cluster Simulator) simulagailua eta **can-utils** tresnak erabilita.

---

## Zer ikasiko duzu?

| Gaitasuna | Tresna |
|---|---|
| CAN trafiko errealean entzutea | `candump`, `cansniffer` |
| Intereseko tramak identifikatzea (alderantzizko ingeniaritza) | `cansniffer`, Python scriptak |
| Trama arbitrarioak injektatzea | `cansend`, `python-can` |
| Replay eraso bat exekutatzea | `canplayer`, Python scripta |
| CAN bus-a fuzzeatzen | `cangen`, `fuzz_can.py` |
| Bus-a saturatzen (DoS) | `can_dos.py` |
| Hardware erreala konektatzea (aukerazkoa) | `usbcan` + BluePill STM32 |

---

## Laborategiaren arkitektura

```
┌──────────────────────────────────────┐
│        Linux VM / Host               │
│                                      │
│  vcan0 (CAN interfaze birtuala)      │
│      │                               │
│      ├── ICSim (aginte-panela)       │
│      ├── controls (agintea)          │
│      ├── candump / cansniffer        │
│      └── scripts/ (erasoak)          │
└──────────────────────────────────────┘
```

> **Hardware oharra (aukerazkoa):** Laborategiak USB CAN dongle bat badu (adib. [usbcan](https://github.com/BatchDrake/usbcan) proiektuko BluePill+HW-184 modulua), `vcan0` interfaze fisikoarekin ordezkatu daiteke eta proba-ibilgailu edo banku baten bus errealera konektatu.

---

## Gutxieneko eskakizunak

- **Sistema eragilea:** Ubuntu 22.04 LTS edo Kali Linux 2024+ (VM edo bare metal).  
  *Windows-ek ez du SocketCAN onartzen. Ikus `lab/03_Setup_entorno_linux_eu.md` VM aukerak.*
- **CPU:** 2 nukleo, 4 GB RAM.
- **Menpekotasunak:** `can-utils`, `SDL2`, `SDL2_image`, `python3`, `python-can`.
- **ICSim:** [https://github.com/zombieCraig/ICSim](https://github.com/zombieCraig/ICSim)-etik konpilatuta.

---

## Karpeta egitura

```
CANbus_ICSim_Ciber/
├── README.md                          ← fitxategi hau (gaztelania)
├── README_eu.md                       ← fitxategi hau (euskara)
├── RUN_ME_FIRST.md                    ← abiarazte azkarra (10 min)
├── requirements.txt                   ← Python menpekotasunak
├── lab/
│   ├── 01_Introduccion_CANbus.md/_eu.md      ← teoria eta testuingurua
│   ├── 02_Checklist_configuracion_laboratorio.md/_eu.md
│   ├── 03_Setup_entorno_linux.md/_eu.md      ← VM/ICSim konfigurazioa
│   ├── 04_Practica_A_Reconocimiento.md/_eu.md
│   ├── 05_Practica_B_Inyeccion.md/_eu.md
│   ├── 06_Practica_C_Replay.md/_eu.md
│   └── 07_Practica_D_Fuzzing_DoS.md/_eu.md
├── scripts/
│   ├── setup_vcan.sh
│   ├── can_scanner.py
│   ├── fuzz_can.py
│   ├── replay_attack.py
│   └── can_dos.py
├── samples/
│   └── icsim_normal.log
├── logs/
└── reports/
    └── 00_Ebidentzia_txosten_txantiloia.md
```

---

## Praktikak

| Praktika | Helburua |
|---|---|
| **A — Ezagutza** | Bus-a entzun eta aktibo dauden IDak katalogatu |
| **B — Frame injekzioa** | `cansend` erabilita aginte-panelaren kontrola hartu |
| **C — Replay erasoa** | Ekintza-sekuentzia bat grabatu eta erreproduzitu |
| **D — Fuzzing eta DoS** | Trafiko aleatorio sortu eta bus-a saturatu |

---

## Ohar legal eta etikoa

Laborategi honek **ingurune birtual soilak** erabiltzen ditu (vcan0 + ICSim). Teknika hauek jabeak berariazko baimenik gabe ibilgailu errealetan erabiltzea **legez kontrakoa** da (10/1995 Lege Organikoa, delitu informatikoak, KP 264. art. eta ondorengoak). Ibilgailuen kontrol-sistemetara baimenik gabe sartzeak bide-segurtasuna arriskuan jar dezake.
