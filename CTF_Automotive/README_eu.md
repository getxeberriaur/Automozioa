# CTF Automotive — UrbanFleet 2026

[Gaztelaniazko bertsioa](README.md)

> Ibilgailuen zibersegurtasuneko CTF integratzailea: eraso/defentsa CAN bus simulatu baten gainean.  
> Iraupena: **90 minutu** · 2-3 pertsonako taldeak · Maila: LH Zibersegurtasuna / Automozioa

---

## Deskribapena

CTF tematikoa, non taldeek **Red Team** baten rola hartzen duten *UrbanFleet 2026* flota fiktizioko ibilgailu baten telemetria ECU bat erasotuz.  
Ingurunea guztiz birtuala da: [ICSim](https://github.com/zombieCraig/ICSim) aginte-panelaren simulagailu gisa eta `vcan0` CAN interfaze birtual gisa. Ez da hardware errealrik behar.

## Aurrebaldintzak

CTF honek [`CANbus_ICSim_Ciber/`](../CANbus_ICSim_Ciber/README_eu.md) laborategia **osatu izana eskatzen du**.  
4 praktiketan (A, B, C, D) ikasitako tresnak eta kontzeptuak lehiaketa-eszenatoki batean konbinatzen dira hemen.

## CTF-aren egitura

```
CTF_Automotive/
├── README.md                              ← gaztelaniazko bertsioa
├── README_eu.md                           ← fitxategi hau
├── RUN_ME_FIRST.md                        ← abiarazte azkarra (Game Master)
├── RUN_ME_FIRST_eu.md
├── requirements.txt
└── lab/
    ├── 01_Enunciado_participantes.md      ← taldeei banatu hasieran
    ├── 01_Enunciado_participantes_eu.md
    ├── 02_Checklist_docente.md            ← Game Master soilik
    ├── 02_Checklist_docente_eu.md
    ├── 03_Hoja_flags_equipo.md            ← kopia bat talde bakoitzeko
    ├── 03_Hoja_flags_equipo_eu.md
    ├── 04_Respuestas_master.md            ← KONFIDENTZIALA — irakaslearentzat soilik
    └── 04_Respuestas_master_eu.md
```

## Faseen laburpena

| Fasea | Teknika | Iraupena | Flagak | Puntuak |
|---|---|---|---|---|
| F1 — Infiltrazioa | Ezagutza pasiboa | 20 min | 3 | 150 |
| F2 — Sarbidea | Frame injekzioa | 20 min | 4 | 200 |
| F3 — Iraunkortasuna | Replay erasoa | 20 min | 1 | 150 |
| F4 — Inpaktu maximoa | DoS + Fuzzing | 15 min | 1 | 150 |
| Bonus — Defentsa | Kontraneurriak ezarrita | 15 min | 1 | 100 |
| **Guztira** | | **90 min** | **10 flag** | **750 puntu** |

## Irakaslearentzako fluxua

1. [`RUN_ME_FIRST_eu.md`](RUN_ME_FIRST_eu.md) irakurri eta ingurunea egiaztatu (30 minutu lehenago)
2. [`04_Respuestas_master_eu.md`](lab/04_Respuestas_master_eu.md) inprimatu — **ez partekatu**
3. [`01_Enunciado_participantes_eu.md`](lab/01_Enunciado_participantes_eu.md) banatu talde bakoitzari
4. [`03_Hoja_flags_equipo_eu.md`](lab/03_Hoja_flags_equipo_eu.md) kopia bat eman talde bakoitzari
5. Kronometroa martxan jarri eta Game Master gisa jardun

## Zailtasun aldaerak

| Maila | Aldaketa |
|---|---|
| Oinarrizkoa | ID taula partziala ematen da (byteak bakarrik falta dira) |
| Estandarra | Pista gabe — dena hutsetik (gomendatua) |
| Aurreratua | Zarata IDak gehitzen dira `cangen`-ekin ezagutza zailtze aldera |
| Aditu | Aurreratuaren berdina + `cansniffer` tresna-zerrendarik kendu |

## Ohartarazpen legala

Ariketa hau gelan kontrolatutako azpiegitura birtual baten gainean soilik egiten da.  
Teknika hauek baimenik gabe benetako ibilgailuetan aplikatzea legez kanpokoa da Espainiako Zigor Kodearen arabera (197. eta 264. art.) eta NIS2 Direktibaren arabera.  
Irakaslea eskuratutako ezagutzaren erabilera etikoa zaintzeko ardura du.
