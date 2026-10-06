# Automozioa — Automozioaren zibersegurtasuna

Parte-hartzaileentzako biltegia: laborategi praktikoak, exekuzio-gidak, scriptak, laginak eta ebidentzia-txantiloiak.

> Praktikak simulagailuetan, sandbox-ean edo jasotze pasiboan soilik egiteko dira. Ez erabili ibilgailu, CAN bus fisiko edo RF sistema errealetan.

## Praktikak

### V16 baliza konektatua
Tokiko API batek simulatutako V16 abisuak baliozkotzen ditu. Eskema, denbora-leihoa, nonce bidezko replay-aren aurkako babesa, tasa-muga eta trazabilitatea lantzen dira.

- [Laborategiaren gida](Automocion_V16_Ciber/README.md)
- [Abiarazte azkarra](Automocion_V16_Ciber/RUN_ME_FIRST.md)

### CAN bus ICSim-ekin
`vcan0` birtualean ezagutza pasiboa, frame-injekzioa, replay-a eta fuzzing/DoS simulatuak.

- [Laborategiaren gida](CANbus_ICSim_Ciber/README.md)
- [Linux/VM konfigurazioa](CANbus_ICSim_Ciber/lab/03_Setup_entorno_linux_eu.md)
- [Abiarazte azkarra](CANbus_ICSim_Ciber/RUN_ME_FIRST.md)

### CTF Automotive
CAN laborategia osatu ondoren egiteko talde-ariketa integratzailea.

- [CTF gida](CTF_Automotive/README.md)
- [Parte-hartzaileen enuntziatua](CTF_Automotive/lab/01_Enunciado_participantes_eu.md)

### RF analisi pasiboa
RTL-SDR bidezko espektro-kaptura eta analisia, isolatutako proba-igorle batekin. Ez dago transmisiorik, replay-rik edo interferentziarik.

- [Laborategiaren gida](RF_Lab_Seguro/README.md)
- [Abiarazte azkarra](RF_Lab_Seguro/QUICKSTART.md)

### V2X simulazioa
V2V/V2I/V2P mezuen konfiantza, autentikazioa, freskotasuna, plausibilitatea eta replay-a `127.0.0.1`-en simulatzen dira.

- [Laborategiaren gida](V2X_Simulacion_Ciber/README.md)
- [Praktika](V2X_Simulacion_Ciber/lab/01_Practica_V2X.md)
- [Abiarazte azkarra](V2X_Simulacion_Ciber/RUN_ME_FIRST.md)

## Erabilera segurua

CAN laborategia `vcan0` + ICSim-en exekutatu. V16 eta V2X praktiketan erabili `127.0.0.1`. RF laborategian erabili RTL-SDR hargailua eta isolatutako proba-igorlea soilik; ez harrapatu benetako giltzen edo ibilgailuen seinalerik.
