# V2X praktika — Bidegurutze ezinezkoa

**Iraupena:** 90 minutu · **Taldea:** binaka · **Ingurunea:** `127.0.0.1`

## Testuingurua

`UrbanFleet` flotak inguruko ibilgailuen mezuak jasotzen ditu. Mezu baten formatua zuzena izatea ez da nahikoa: hartzaileak igorlea, freskotasuna, errepikapenak eta egoera fisikoaren plausibilitatea egiaztatu behar ditu.

Laborategiko gateway-ak bi modu ditu. Modu babestuan identitatea, HMAC laborategikoa, timestamp-a, sekuentzia, replay-a eta tasa-muga aztertzen ditu. `--insecure` moduan kontrol batzuk desaktibatuta daude. HMAC sinadura zuzenak mezua gakoarekin bat datorrela frogatzen du; ez du frogatzen koordenatuak edo abiadura egiazkoak direnik.

Trafiko guztia tokiko simulazioa da. Ez dago V2X irrati-transmisiorik, benetako ibilgailurik edo errepide-azpiegiturarik.

## Helburuak

1. CAM eta DENM mezu legitimoak behatzea.
2. Modu babestua eta babesik gabekoa alderatzea.
3. Replay-a, spoofing-a, timestamp zaharra, datu ezinezkoak eta burst-a aztertzea.
4. Emaitza bakoitza kontrol egokiarekin lotzea.

## Prestaketa

1. Egiaztatu Python 3.10 edo berriagoa instalatuta dagoela.
2. Ireki bi terminal biltegiaren erro-karpetan.
3. Lehen terminalean abiarazi gateway babestua:

```bash
python V2X_Simulacion_Ciber/scripts/v2x_gateway.py
```

4. Bigarren terminalean bidali oinarrizko mezuak:

```bash
python V2X_Simulacion_Ciber/scripts/send_v2x.py legitimo
python V2X_Simulacion_Ciber/scripts/send_v2x.py emergency
```

Saio garbi batean biek `HTTP 202` eta `accepted` itzuli behar dute. Gorde erantzuna.

## 1. fasea — Agertoki babestuak

Agertoki bakoitzaren aurretik berrabiarazi gateway-a, aurreko sekuentzia-egoerak eragina izan ez dezan. Exekutatu agertoki bana:

```bash
python V2X_Simulacion_Ciber/scripts/send_v2x.py replay
python V2X_Simulacion_Ciber/scripts/send_v2x.py spoof
python V2X_Simulacion_Ciber/scripts/send_v2x.py impossible
python V2X_Simulacion_Ciber/scripts/send_v2x.py old
python V2X_Simulacion_Ciber/scripts/send_v2x.py burst
```

Gorde HTTP kodea, `accepted`/`rejected` egoera eta baztertze-arrazoiak. `replay` agertokiak mezu bera bi aldiz bidaltzen du; bigarren bidalketak replay-aren aurkako erantzuna erakutsi behar du.

## 2. fasea — Babesik gabeko modua

Gelditu gateway-a eta berrabiarazi kontrol batzuk desaktibatuta:

```bash
python V2X_Simulacion_Ciber/scripts/v2x_gateway.py --insecure
```

Berrabiarazi gateway-a agertoki bakoitzaren aurretik eta errepikatu oinarrizko mezuak eta bost probak. Kontuan izan modu horretan ere mezu-mota, koordenatuen tartea, abiadura, norabidea eta timestamp zaharra egiaztatzen direla.

## 3. fasea — Emaitzen konparazioa

Osatu taula, eta adierazi zein kontrolak eragin duen aldea:

| Agertokia | Babesik gabe | Babestuta | Kontrola |
|---|---|---|---|
| Replay-a | | | |
| Erregistratu gabeko igorlea | | | |
| Abiadura edo kokapen ezinezkoa | | | |
| Timestamp zaharra | | | |
| Mezu-sorta azkarra | | | |

Baztertze bakoitzerako aztertu autentikotasuna, osotasuna, freskotasuna, plausibilitatea edo erabilgarritasuna.

## 4. fasea — Txostena eta amaiera

Gorde terminaleko erantzunak edo pantaila-argazkiak eta bete [txosten-txantiloia](../reports/00_Plantilla_informe.md). Azaldu hiru defentsa-neurri lehenetsi `UrbanFleet`-entzat.

Amaitzean, gelditu gateway-a `Ctrl+C` erabiliz eta egiaztatu `8090` atakan ez dela zerbitzurik geratu. Ez erabili `127.0.0.1` ez den beste ostalaririk.