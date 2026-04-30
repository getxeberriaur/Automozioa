# Automozioa — Automozioaren Zibersegurtasuna

[Gaztelaniazko bertsioa](README.md)

> **Ikastaroaren programa osoa (3 egun):** [00_Horario_curso_eu.md](00_Horario_curso_eu.md)

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

### 3 — CTF Automotive — UrbanFleet 2026 (`CTF_Automotive/`)

90 minutuko **Capture The Flag** motako ariketa integratzailea, CAN bus laborategiko teknika guztiak (ezagutza, injekzioa, replay, DoS/fuzzing) taldeen arteko lehia-eszenatoki batean konbinatzen dituena.

**Gaiak:** CAN bus-eko Red Team-a, faseka kateatutako erasoa, defentsa eta kontraesanerako neurriak, ebidentzien aurkezpena.  
**Aurrebaldintza:** `CANbus_ICSim_Ciber/` osatu izana.  
**Ingurunea:** Linux ICSim + vcan0-rekin (2. praktikako ingurune bera).  
**Dokumentazioa:** [CTF_Automotive/README_eu.md](CTF_Automotive/README_eu.md)

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
├── CANbus_ICSim_Ciber/                ← 2. Praktika: CAN Bus
│   ├── README.md
│   ├── README_eu.md
│   ├── RUN_ME_FIRST.md
│   ├── lab/
│   ├── scripts/
│   ├── samples/
│   ├── logs/
│   ├── reports/
│   └── requirements.txt
│
└── CTF_Automotive/                    ← 3. Praktika: CTF integratzailea
    ├── README.md
    ├── README_eu.md
    ├── RUN_ME_FIRST.md
    ├── lab/
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
