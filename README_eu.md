# Automozioa — Automozioaren Zibersegurtasuna

[Gaztelaniazko bertsioa](README.md)

Automozioaren **zibersegurtasunari** buruzko irakaskuntza-material eta laborategi praktikoen biltegi hau da. Karpeta bakoitzak dokumentazioa, scriptak eta ebidentzia-txantiloiak dituen praktika autonomo bat dauka.

> Eduki guztia **ingurune simulatu edo sandbox batean defentsa-prestakuntza** egiteko diseinatuta dago. Ez da baimenik gabe ibilgailu edo azpiegitura errealen gainean erabili behar.

---

## Praktika erabilgarriak

### 1 — V16 baliza konektatua (`Automocion_V16_Ciber/`)

V16 larrialdi-abisu sistema konektatuaren zibersegurtasunari buruzko laborategia. Tokiko REST API baten gainean baliza-gertaerak bidaltzen eta baliozkotzen simulatzen du.

**Gaiak:** JSON eskemaren baliozkotzea, nonce bidezko replay-aurkako babesa, denbora-leihoa, rate limiting, gertaeren trazabilitatea.  
**Ingurunea:** Python / FastAPI — Windows, Linux eta macOS-en funtzionatzen du.  
**Dokumentazioa:** [Automocion_V16_Ciber/README_eu.md](Automocion_V16_Ciber/README_eu.md)

---

### 2 — CAN Bus ICSim-ekin (`CANbus_ICSim_Ciber/`)

**CAN bus** protokoloaren ahuleziei buruzko laborategia, ICSim simulagailua (Instrument Cluster Simulator) eta `can-utils` tresnak erabilita. Ezagutza pasiboa, frame injekzioa, replay-a eta fuzzing/DoS-a biltzen ditu.

**Gaiak:** CAN 2.0 protokoloa, frame-en alderantzizko ingeniaritza, autentifikaziorik gabeko injekzioa, replay erasoa, bus flooding-a.  
**Ingurunea:** Linux (Ubuntu 22.04 / Kali) `vcan0` birtualarekin — VM batean ere erabil daiteke.  
**Dokumentazioa:** [CANbus_ICSim_Ciber/README_eu.md](CANbus_ICSim_Ciber/README_eu.md)

---

## Biltegiaren egitura

```text
Automozioa/
├── README.md                          ← indize orokorra (gaztelania)
├── README_eu.md                       ← fitxategi hau (indize orokorra, euskaraz)
│
├── Automocion_V16_Ciber/              ← 1. Praktika: V16 baliza
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
└── CANbus_ICSim_Ciber/                ← 2. Praktika: CAN Bus
    ├── README.md
    ├── README_eu.md
    ├── RUN_ME_FIRST.md
    ├── lab/
    ├── scripts/
    ├── samples/
    ├── logs/
    ├── reports/
    └── requirements.txt
```

---

## Norentzat dago zuzenduta

- LHko (Automozio, Informatika, Zibersegurtasuna) eta unibertsitateko irakasleak.
- Automozio konektatuaren segurtasun-demostrazioetan lan egin nahi duten talde teknikoak.
- Sistema txertatuetan eta CAN bus-en zibersegurtasunarekiko interesa duten ikasleak.

---

## Ohar legala

Laborategi hauetan erakutsitako teknikak baimenik gabe sistema errealen gainean erabiltzea legez kontrakoa da eta bide-segurtasuna arriskuan jar dezake. Ingurune guztiak tokiko sandbox batean edo sare guztiz isolatuan funtzionatzeko diseinatuta daude.
