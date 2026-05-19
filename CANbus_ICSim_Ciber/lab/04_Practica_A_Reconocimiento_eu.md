# A Praktika — CAN Bus-eko Ezagutza

[Gaztelaniazko bertsioa](04_Practica_A_Reconocimiento.md)

**Estimatutako iraupena:** 45 minutu  
**Zailtasuna:** Oinarrizkoa  
**Tresnak:** `candump`, `cansniffer`, `scripts/can_scanner.py`

---

## Helburua

ICSim simulagailuaren CAN bus-a modu pasiboan entzutea, aktibo dauden Arbitration IDak identifikatzea eta datuen aldaketak kontrol-agintean egindako ekintza fisikoekin erlazionatzea. Amaieran, taldeak `ID → funtzio` oinarrizko mapa bat egin ahal izan behar du.

---

## Testuingurua

Ibilgailu baten benetako auditoria batean, lehenengo urratsa beti **ezagutza pasiboa** da: bus-era konektatu (adibidez, OBD-II bidez) eta ezer transmititu gabe entzun. CAN bus-ak ez du mota honetako entzuketa detektatzeko mekanismorik.

Protokoloak EZ du:
- Nodoen autentifikaziorik
- Trafikoaren enkriptaziorik
- Baimenik gabeko nodoen detekziorik

Hori dela eta, sarbide fisikoa duen erasotzaile batek trafiko osoa erabat isiltasunez entzun dezake.

---

## Aurrebaldintzak

- `vcan0` aktibo (`sudo bash scripts/setup_vcan.sh` exekutatu).
- ICSim martxan (`./ICSim/builddir/icsim vcan0`).
- Controls martxan (`./ICSim/builddir/controls vcan0`).

---

## A.1 Ariketa — Hasierako kaptura `candump`-ekin

### Urratsak

1. Terminal bat ireki eta exekutatu:
```bash
candump vcan0
```

2. `controls`-en leihoan, teklatua erabili simulagailuarekin interaktuatzeko (azeleratu, txandakatzaileak aktibatu, ateak blokeatu).

3. `candump`-en irteera behatu. Espero den irteera adibidea:
```
  vcan0  244   [8]  00 00 00 00 1A 00 00 00
  vcan0  188   [8]  00 00 00 00 00 00 00 00
  vcan0  19B   [8]  0F 00 00 00 00 00 00 00
  vcan0  244   [8]  00 00 00 00 2C 00 00 00
  vcan0  188   [8]  01 00 00 00 00 00 00 00
```

4. Kaptura fitxategi batera gorde:
```bash
candump -l vcan0
# candump-YYYYMMDD-HHMMSS.log fitxategia sortzen da
```

### Galdutako galderak

- ICSim aktibo dagoen bitartean zenbat ID desberdin agertzen dira?
- Azeleratzailea sakatzen duzunean datuak aldatzen dituen IDrik al dago?
- Ezkerreko txandakatzearen adierazlea aktibatzean aldatzen den IDrik al dago?

---

## A.2 Ariketa — Iragazketa `cansniffer`-ekin

`cansniffer`-ek denbora errealean **aldatzen** diren byteak soilik erakusten ditu — alderantzizko ingeniariatzarako ezin hobea.

### Urratsak

1. Exekutatu:
```bash
cansniffer -c vcan0
```

2. `cansniffer` aktibo duen bitartean, `controls`-en **bana-bana** egiteko ekintza hauek:

| Ekintza | Zein ID aldatzen da? | Zein byte? | Aurretiazko balioa | Osteko balioa |
|---|---|---|---|---|
| Poliki azeleratu | | | | |
| Maximora azeleratu | | | | |
| Frenatu | | | | |
| Ezkerreko txandakatzailea | | | | |
| Eskuineko txandakatzailea | | | | |
| 1. atea blokeatu | | | | |
| 1. atea desblokeatu | | | | |

Taula txosten-txantiloian bete.

---

## A.3 Ariketa — Eskaneatze automatikoa `can_scanner.py`-rekin

`scripts/can_scanner.py` scriptak 30 segundo trafikoa kapturatzen du eta aktibo dauden IDen laburpen estatistikoa sortzen du.

```bash
source .venv/bin/activate
python scripts/can_scanner.py --interface vcan0 --duration 30 --output logs/scan_emaitza.txt
```

Espero den irteera (adibidea):
```
=== CAN Bus Scan — vcan0 ===
Iraupena: 30.0 s | Trama guztiak: 3621

ID       Tramak    Freq(Hz)   Min_DLC  Max_DLC   Byte aldakorrak
------   ------    --------   -------  -------   ----------------
0x188      1204      40.1       8        8        [0]
0x19B       602      20.1       8        8        [0]
0x244      1815      60.5       8        8        [3, 4]
```

### Gidatutako galderak

- Zein da maiztasun handieneko IDa?
- Zein IDk byte aldakorrena du?
- Zein maiztasunekin (Hz) bidaltzen da abiadura-IDa?

---

## A.4 Ariketa — ID-ren arabera bideratutako kaptura

Intereseko IDak identifikatu ondoren, trafiko hori soilik iragaztea:

```bash
# 0x244 IDa soilik erakutsi
candump vcan0,244:7FF

# 0x188 eta 0x19B IDak soilik erakutsi
candump vcan0,188:7FF vcan0,19B:7FF
```

Iragazitako kapturak gorde:
```bash
candump -l vcan0,244:7FF
```

---

## A Praktikaren entregagaiak

Ebidentzia-txantiloian bete (`reports/00_Ebidentzia_txosten_txantiloia.md`):

1. **Identifikatutako IDen taula** maiztasunarekin, DLC-arekin eta inferitutako funtzioarekin.
2. **Erlaziotze-taula** ekintza → ID → byte → balioa (A.2 ariketatik).
3. **Pantaila-argazkia** byte aldakorrak erakusten dituen `cansniffer`-ekin.
4. **Log fitxategia** `can_scanner.py`-k sortuta.

---

## Erreferentziazko mapa (ICSim modu ez-aleatorio)

> Praktikaren amaieran soilik erakutsi, parte-hartzaileek beraiek aurkitu dezaten.

| CAN ID | Funtzioa | Bytea | Deskribapena |
|---|---|---|---|
| `0x244` | Abiadura | 3. byte | 0x00=0 km/h, 0xFF=maximoa |
| `0x188` | Txandakatzaileak | 0. byte | `0x01`=ezkerra, `0x02`=eskuina, `0x03`=biak |
| `0x19B` | Ateak | 0. byte | 0-3 bitak = 1-4 ateak (1=irekita/desblokeatuta) |

---

## Azken gogoeta

- Zergatik da arriskutsua CAN bus-ak autentifikaziorik ez izatea?
- Nola erabil lezake erasotzaile batek informazio hori benetako ibilgailu batean?
- Zeintzuk dira ibilgailu modernoetan mapeatze hau zailtzen dituzten neurriak?

---

## A.5 Praktika — SavvyCAN: bistaratze grafikoa eta alderantzizko ingeniaritza

> **Maila:** ertaina · **Gutxi gorabeherako denbora:** 35 minutu (10 min hizlariaren erakustaldia + 25 min praktika)
> Aurreko ariketetan ikusi dituzun datu berdinak ikertzaile profesionalek eta OEM fabrikatzaileek erabiltzen duten tresnarekin aztertuko dituzu.

> ⚠️ **Exekuzio ingurunea — garrantzitsua:**
> SavvyCAN **host makinan** exekutatzen da, ez Docker edukiontziaren barruan.
> Edukiontziak `--network host` eta `--cap-add NET_ADMIN` aukerarekin exekutatzen denez, `vcan0` interfazea host-aren kernelean zuzenean ikusgai geratzen da.
> Fluxua: `[ICSim + controls (Docker)] → vcan0 (host kernela) ← [SavvyCAN (host-a)]`

### Zer ekartzen du SavvyCAN-ek `cansniffer`-en aldean?

| `cansniffer` (terminala) | SavvyCAN (GUI) |
|---|---|
| Aldatzen diren byteak kolore bidez erakusten ditu | Byte bakoitzaren balioa denboran zehar grafikatzen du |
| Instalaziorik gabe, beti funtzionatzen du | AppImage + FUSE behar du |
| Korrelazioa azkar egiteko egokia | Alderantzizko ingeniaritza xehaturako egokia |
| Historial bisualik gabe | Historial osoa zoom-arekin |
| Ez ditu DBC fitxategiak irakurtzen | DBC fitxategiak irakurtzen ditu (industria estandarra) |

### 1. urratsa — Instalazioa (oraindik instalatu ez bada)

```bash
curl -Lo SavvyCAN.AppImage \
  $(curl -s https://api.github.com/repos/collin80/SavvyCAN/releases/latest \
    | grep -o '"browser_download_url":"[^"]*AppImage[^"]*"' \
    | cut -d'"' -f4)
chmod +x SavvyCAN.AppImage
sudo apt install -y libfuse2   # FUSE errorea bada soilik
./SavvyCAN.AppImage
```

---

### 2. urratsa — `vcan0`-ra konektatu

1. Edukiontziak exekutatzen ari direla egiaztatu: `docker ps` → `icsim_run` agertu behar da
2. SavvyCAN-en: **Connection → Open Connection Manager**
3. Egin klik **Add new device bus** → mota **SocketCAN** ('d' gabe)
4. Interfaze-eremuan idatzi: `vcan0`
5. Egin klik **Connect** — beheko barrak tramak zenbatzen hasi behar du

> ⚠️ Barrak ez badu zenbatzen, exekutatu terminalean: `cansend vcan0 123#DEADBEEF`
> SavvyCAN-ek oraindik ezer erakusten ez badu, berrabiarazi: `sudo ./SavvyCAN.AppImage`

---

### Hizlariaren erakustaldia — 10 minutu

> Hizlariak sekuentzia hau egiten du proiektatutako pantailan, parte-hartzaileek euren kabuz egin aurretik.

| Denbora | Ekintza | Mezu nagusia |
|---|---|---|
| 0–2 min | Trafiko gordina duen leiho nagusia erakutsi | *"Autobusa etengabe hitz egiten ari da. Autentifikaziorik gabe. Sarbidea duenak dena irakur dezake."* |
| 2–5 min | Signal Graph ireki + azeleragailua mugitu | *"3 minututan identifikatu dugu zein tramak kontrolatzen duen abiadura, dokumentaziorik gabe. Hori da CAN alderantzizko ingeniaritza."* |
| 5–7 min | `0x188`-ra iragazi + txandakatze-adierazlea aktibatu | *"Oszilatu egiten den bit hori replay eraso baterako kapturatuko genukeena da."* |
| 7–10 min | Kaptura gorde → fitxategia ireki | *"`.csv` fitxategi honek da erasotzaile batek portaera erreproduzitzeko behar duen guztia."* |

---

### Ariketa gidatua — parte-hartzaileak

#### A.5.1 Ariketa — Zuzeneko kaptura eta iragazketa

1. SavvyCAN `vcan0`-ra konektatuta eta ICSim exekutatzen ari dela, begiratu leiho nagusia
2. Mugitu azeleragailua noVNC-n (`localhost:6080`) — zein IDk aldatzen dute beren balioa?
3. Aktibatu **Connection → Filters** → ezkutatu `0x244` eta `0x188` ez diren ID guztiak
4. Zer desberdintasun nabari duzu pantailan iragazkiarekin?

#### A.5.2 Ariketa — Seinalearen bistaratze grafikoa

1. Zerrenda nagusian, egin **klik bikoitza** `0x244` IDaren gainean — **Frame Info** leihoa irekitzen da
2. Frame Info-n, egin klik **3. bytearen** gaineko grafikaren ikonoan
3. **Graphing** leihoa irekitzen da 3. bytearen kurba denboran zehar erakutsiz
4. Mugitu azeleragailua poliki 0-tik maximora — ikusi kurba nola igotzen den
5. Askatu azeleragailua — ikusi kurba nola jaisten den
6. Errepikatu `0x188` 0. bytearekin — aktibatu/desaktibatu txandakatze-adierazlea eta behatu pultsua

> Grafikaren ikonoa agertzen ez bada Frame Info-n, saiatu: **klik eskuinarekin bytearen gainean → "Graph this signal"**

#### A.5.3 Ariketa — Kaptura eta lineaz kanpoko analisia

1. Azeleragailua maximoan 5 segundoz edukita, kaptura gorde:
   **File → Save Frames** → izena: `kaptura_azeleragailua.csv`
2. Trafiko gelditu: **Connection → Disconnect**
3. Gordeta duen fitxategia kargatu: **File → Load Frames**
4. Azeleragailua maximora iritsi zen une zehatza identifika al dezakezu?
5. Grafikaren pantaila-argazki bat gorde ebidentzia-txostenerako

---

### Hausnarketa galderak

1. Zer abantaila du SavvyCAN-ek `cansniffer`-en aldean analisi luze baterako?
2. Gorde duzun `.csv` fitxategiak, zer erabilera izango luke replay eraso bat egiteko?
3. Zer informazio gehigarri beharko zenuke `0x244`-ren 3. bytetik abiadura benetako balioa (km/h-tan) deskodetzeko?
