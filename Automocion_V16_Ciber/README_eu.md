# Automozioa

[Gaztelaniazko bertsioa](README.md)

Automozioaren zibersegurtasunari buruzko irakaskuntza-materialak eta laborategi praktikoa biltzen dituen laguntza-biltegia da hau, ingurune simulatuan dauden V16 balizen gertaera konektatuetan arreta jarrita.

## Helburua

Biltegi hau honetarako pentsatuta dago:

- ITS sistemetako eta automozio konektatuko zibersegurtasunari buruzko sarrera-saio didaktikoak laguntzeko;
- defentsara bideratutako laborategi kontrolatu, erreproduzigarri eta gidatu bat eskaintzeko;
- backend-a, simulagailua eta ebidentziak dituen praktika lokal bat eraikitzeko oinarri izateko.

> Garrantzitsua: eduki guztia tokiko sandbox edo sare isolatu batean defentsa-ikuspegiko prestakuntzarako diseinatuta dago. Ez da azpiegitura errealetan erabili behar.

## Praktika

Jarraitu [abiarazte azkarra](RUN_ME_FIRST.md). Karpeta honetan daude API lokala, simulagailua, proba-adibidea eta txosten-txantiloiak.

## Ibilbidea

1. Irakurri [RUN_ME_FIRST.md](RUN_ME_FIRST.md).
2. Egin agertokiak `simulator/send_event.py` erabilita.
3. Berrikusi `logs/events.log` eta entregatu [txosten-txantiloia](reports/00_Ebidentzia_txosten_txantiloia.md).

## Publikoa

Laborategia tokiko ingurunean exekutatzen da, `127.0.0.1` helbidean. Ez konektatu kanpoko zerbitzuekin edo sistema errealekin.

## Publikoa

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

## Exekuzioa

Laborategia lokalean, `127.0.0.1` helbidean, exekutatzen da. Ez konektatu kanpoko zerbitzuekin edo sistema errealekin.

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

## Osagaiak

- `backend/app.py`: balidazioa eta erabakien erregistroa dituen API lokala.
- `simulator/send_event.py`: legitimo, replay, timestamp, koordenatu, identitate eta ráfaga agertokiak.
- `samples/event_legitimo.json`: payload adibidea.
- `reports/`: gaztelaniazko eta euskarazko txantiloiak.

## Eskuragarri dagoen gutxieneko inplementazioa

Biltegiak lehen oinarri exekutagarri bat dauka jada:

- [Automocion_V16_Ciber/backend/app.py](backend/app.py): eskema-balidazioa, denbora-leihoa, anti-replay kontrola, tasa-kontrola eta logging-a dituen API lokala.
- [Automocion_V16_Ciber/simulator/send_event.py](simulator/send_event.py): `legitimo`, `replay`, `timestamp-atrasado`, `coordenadas-invalidas`, `identidad-invalida` eta `rafaga` eszenatokiak dituen simulagailua.
- [Automocion_V16_Ciber/samples/event_legitimo.json](samples/event_legitimo.json): payload adibidea.
- [Automocion_V16_Ciber/RUN_ME_FIRST.md](RUN_ME_FIRST.md): hasierako abiarazte azkarra.
- [Automocion_V16_Ciber/requirements.txt](requirements.txt): laborategiaren mendekotasunak.

## Segurtasun- eta etika-printzipioak

- Tokiko, simulatutako edo isolatutako inguruneak bakarrik.
- Material hauek sistema errealen aurka erabiltzea debekatuta dago.
- Helburua soilik hezitzailea eta defentsiboa da.
- Praktikak balidazioa, hardening-a, detekzioa eta erantzuna izan behar ditu ardatz.

## Lizentzia eta erabilera

Material hau ikastetxe batean berrerabiliko baduzu, komeni da biltegian lizentzia esplizitu bat gehitzea eta, nahi izanez gero, egiletza edo ekarpen-ohar bat eranstea.
