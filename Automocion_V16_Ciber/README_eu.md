# Automozioa

[Gaztelaniazko bertsioa](README.md)

Automozioaren zibersegurtasunari buruzko irakaskuntza-materialak eta laborategi praktikoa biltzen dituen laguntza-biltegia da hau, ingurune simulatuan dauden V16 balizen gertaera konektatuetan arreta jarrita.

## Helburua

Biltegi hau honetarako pentsatuta dago:

- ITS sistemetako eta automozio konektatuko zibersegurtasunari buruzko sarrera-saio didaktikoak laguntzeko;
- defentsara bideratutako laborategi kontrolatu, erreproduzigarri eta gidatu bat eskaintzeko;
- backend-a, simulagailua eta ebidentziak dituen praktika lokal bat eraikitzeko oinarri izateko.

> Garrantzitsua: eduki guztia tokiko sandbox edo sare isolatu batean defentsa-ikuspegiko prestakuntzarako diseinatuta dago. Ez da azpiegitura errealetan erabili behar.

## Uneko edukia

Lehen bertsio honetan, biltegiak irakaskuntza-saio bat eta 2 orduko laborategi bat prestatzeko oinarrizko dokumentazioa dauka:

- [Automocion_V16_Ciber/materiales/00_Guion_intro_30min_eu.md](Automocion_V16_Ciber/materiales/00_Guion_intro_30min_eu.md): 30 minutuko sarrera-gidoia.
- [Automocion_V16_Ciber/materiales/01_Laboratorio_2h_eu.md](Automocion_V16_Ciber/materiales/01_Laboratorio_2h_eu.md): laborategi praktikoaren diseinua.
- [Automocion_V16_Ciber/lab/02_Checklist_configuracion_laboratorio_eu.md](Automocion_V16_Ciber/lab/02_Checklist_configuracion_laboratorio_eu.md): irakaslearentzako prestaketa-checklista.
- [Automocion_V16_Ciber/lab/03_Setup_rapido_windows_eu.md](Automocion_V16_Ciber/lab/03_Setup_rapido_windows_eu.md): Windows-erako erreferentziazko konfigurazio azkarra.

## Dokumentazioaren aurkibidea

### Dokumentazioa euskaraz

- [Automocion_V16_Ciber/RUN_ME_FIRST.md](Automocion_V16_Ciber/RUN_ME_FIRST.md)
- [README_eu.md](README_eu.md)
- [Automocion_V16_Ciber/materiales/00_Guion_intro_30min_eu.md](Automocion_V16_Ciber/materiales/00_Guion_intro_30min_eu.md)
- [Automocion_V16_Ciber/materiales/01_Laboratorio_2h_eu.md](Automocion_V16_Ciber/materiales/01_Laboratorio_2h_eu.md)
- [Automocion_V16_Ciber/lab/02_Checklist_configuracion_laboratorio_eu.md](Automocion_V16_Ciber/lab/02_Checklist_configuracion_laboratorio_eu.md)
- [Automocion_V16_Ciber/lab/03_Setup_rapido_windows_eu.md](Automocion_V16_Ciber/lab/03_Setup_rapido_windows_eu.md)
- [Automocion_V16_Ciber/lab/05_Demo_Ahultasunak_Help_Flash_eu.md](Automocion_V16_Ciber/lab/05_Demo_Ahultasunak_Help_Flash_eu.md) — Demo CVE-2025-65855 (irakasleak)

### Gaztelaniazko dokumentazioa

- [README.md](README.md)
- [Automocion_V16_Ciber/materiales/00_Guion_intro_30min.md](Automocion_V16_Ciber/materiales/00_Guion_intro_30min.md)
- [Automocion_V16_Ciber/materiales/01_Laboratorio_2h.md](Automocion_V16_Ciber/materiales/01_Laboratorio_2h.md)
- [Automocion_V16_Ciber/lab/02_Checklist_configuracion_laboratorio.md](Automocion_V16_Ciber/lab/02_Checklist_configuracion_laboratorio.md)
- [Automocion_V16_Ciber/lab/03_Setup_rapido_windows.md](Automocion_V16_Ciber/lab/03_Setup_rapido_windows.md)

## Biltegiaren egitura

```text
Automozioa/
├─ README_eu.md
├─ README.md
└─ Automocion_V16_Ciber/
   ├─ backend/
   │  └─ app.py
   ├─ lab/
   │  ├─ 02_Checklist_configuracion_laboratorio.md
   │  ├─ 02_Checklist_configuracion_laboratorio_eu.md
   │  ├─ 03_Setup_rapido_windows.md
   │  └─ 03_Setup_rapido_windows_eu.md
   ├─ logs/
   │  └─ .gitkeep
   └─ materiales/
      ├─ 00_Guion_intro_30min.md
      ├─ 00_Guion_intro_30min_eu.md
      ├─ 01_Laboratorio_2h.md
      └─ 01_Laboratorio_2h_eu.md
   ├─ reports/
   │  └─ .gitkeep
   ├─ samples/
   │  └─ event_legitimo.json
   ├─ simulator/
   │  └─ send_event.py
   ├─ requirements.txt
   └─ RUN_ME_FIRST.md
```

## Norentzat dago zuzenduta

Bereziki erabilgarria da honako hauentzat:

- LHko, unibertsitateko edo prestakuntza teknikoko irakasleak;
- automozio konektatuko segurtasunaren tokiko erakustaldi bat muntatu nahi duten taldeak;
- gertaeren balidazioa, trazabilitatea eta oinarrizko hardening-a lantzeko sentsibilizazio-jarduerak.

## Ikuspegi pedagogikoa

Proposatutako laborategiak bi egoera alderatzen ditu:

1. balidazio eskasak dituen backend bat;
2. defentsa-kontrolak aktibatuta dituen backend bera.

Dokumentazioan lantzen diren kontrolen artean daude:

- JSON eskemaren balidazio zorrotza;
- koordenatuen balidazioa;
- `timestamp` eremurako denbora-leihoa;
- `nonce` bidezko replay erasoen prebentzioa;
- identitate bakoitzeko rate limiting-a;
- onarpen edo ukapen arrazoia jasotzen duen log-a.

## Nola erabili biltegi hau

### 1. aukera: irakaskuntza-material gisa bakarrik

Klaseko euskarri gisa bakarrik erabili nahi baduzu:

1. berrikusi sarrera-gidoia [Automocion_V16_Ciber/materiales/00_Guion_intro_30min_eu.md](Automocion_V16_Ciber/materiales/00_Guion_intro_30min_eu.md) fitxategian;
2. egokitu saio praktikoa [Automocion_V16_Ciber/materiales/01_Laboratorio_2h_eu.md](Automocion_V16_Ciber/materiales/01_Laboratorio_2h_eu.md) dokumentuarekin;
3. erabili [Automocion_V16_Ciber/lab/02_Checklist_configuracion_laboratorio_eu.md](Automocion_V16_Ciber/lab/02_Checklist_configuracion_laboratorio_eu.md) fitxategiko checklista saioa eman aurretik.

### 2. aukera: laborategi exekutagarri bihurtzea

Biltegiaren hurrengo bilakaera gomendatua:

- `backend/` sortzea ingestio-API lokalerako;
- `simulator/` sortzea gertaera legitimoak eta probakoak sortzeko;
- `logs/` sortzea trazabilitaterako;
- `reports/` sortzea talde bakoitzaren ebidentzietarako;
- `requirements.txt` eta payload adibideak gehitzea.

## Aurreikusitako laborategi-fluxua

Helburuzko fluxua honako hau da:

1. simulagailuak gertaera bat sortzen du;
2. backend-ak formatua, denbora, identitatea eta politika balidatzen ditu;
3. backend-ak `accepted` edo `rejected` erabakitzen du;
4. erabakia log-etan erregistratzen da;
5. taldeak ebidentziak eta ondorioak dokumentatzen ditu.

## Espero diren ikaskuntza-emaitzak

Material hau erabilita, parte-hartzaileek honako hauek egiteko gaitasuna izan beharko lukete:

- automozio konektatuko sistema bateko aktibo kritikoak identifikatzea;
- spoofing-a, replay-a eta datu baliogabeen injekzioa bereiztea;
- oinarrizko balidazio- eta trazabilitate-kontrolak aplikatzea;
- log-ak ebidentzia tekniko gisa interpretatzea;
- mitigazioak eta hondar-arriskua justifikatzea.

## Biltegiaren egoera

Uneko egoera:

- irakaskuntza-dokumentazioa: erabilgarri;
- laborategiaren gidoia: erabilgarri;
- backend minimo erreferentziala: erabilgarri;
- proba-simulagailua: erabilgarri;
- ebidentzien txantiloiak: egiteko.

## Eskuragarri dagoen gutxieneko inplementazioa

Biltegiak lehen oinarri exekutagarri bat dauka jada:

- [Automocion_V16_Ciber/backend/app.py](Automocion_V16_Ciber/backend/app.py): eskema-balidazioa, denbora-leihoa, anti-replay kontrola, tasa-kontrola eta logging-a dituen API lokala.
- [Automocion_V16_Ciber/simulator/send_event.py](Automocion_V16_Ciber/simulator/send_event.py): `legitimo`, `replay`, `timestamp-atrasado`, `coordenadas-invalidas`, `identidad-invalida` eta `rafaga` eszenatokiak dituen simulagailua.
- [Automocion_V16_Ciber/samples/event_legitimo.json](Automocion_V16_Ciber/samples/event_legitimo.json): payload adibidea.
- [Automocion_V16_Ciber/RUN_ME_FIRST.md](Automocion_V16_Ciber/RUN_ME_FIRST.md): hasierako abiarazte azkarra.
- [Automocion_V16_Ciber/requirements.txt](Automocion_V16_Ciber/requirements.txt): laborategiaren mendekotasunak.

## Gomendatutako hurrengo urratsak

1. Python-en gutxieneko inplementazioa osatzea;
2. gertaera baliozkoen eta baliogabeen adibideak gehitzea;
3. `reports/` karpetarako txosten-txantiloi bat prestatzea;
4. talde bakoitzarentzako abiarazte azkarreko jarraibideak gehitzea;
5. laborategia Windows ingurune erreal batean balidatzea, saioa eman aurretik.

## Segurtasun- eta etika-printzipioak

- Tokiko, simulatutako edo isolatutako inguruneak bakarrik.
- Material hauek sistema errealen aurka erabiltzea debekatuta dago.
- Helburua soilik hezitzailea eta defentsiboa da.
- Praktikak balidazioa, hardening-a, detekzioa eta erantzuna izan behar ditu ardatz.

## Lizentzia eta erabilera

Material hau ikastetxe batean berrerabiliko baduzu, komeni da biltegian lizentzia esplizitu bat gehitzea eta, nahi izanez gero, egiletza edo ekarpen-ohar bat eranstea.
