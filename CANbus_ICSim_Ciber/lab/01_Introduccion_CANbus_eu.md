# CAN Bus Protokoloaren eta Eraso-Azaleraren Sarrera

[Gaztelaniazko bertsioa](01_Introduccion_CANbus.md)

## 1. Zer da CAN bus-a?

**Controller Area Network (CAN)** Bosch-ek 1983an garatutako serie-komunikazio protokoloa da, mikrokontrolagailuek eta gailuek ordenagailu zentral baten beharrik gabe elkarrekin komunikatu ahal izateko diseinatua. 1990eko hamarkadatik autogintzako elektronikaren de facto estandarra da.

### 1.1 Oinarrizko ezaugarriak

| Ezaugarria | Balioa |
|---|---|
| Gehieneko abiadura | 1 Mbit/s-era arte (CAN 2.0) |
| Topologia | Mutur bakoitzean amaiera duen bus lineala |
| Komunikazio eredua | Broadcast — nodo guztiek mezu guztiak ikusten dituzte |
| Gehieneko datu-luzera | 8 byte trama bakoitzeko (CAN 2.0), 64 byte (CAN FD) |
| Arbitrajea | Lehentasunaren arabera (ID baxuena = lehentasun handiena) |
| Errore-detekzioa | CRC, ACK, bit stuffing, error framing |
| Autentifikazioa | **Bat ere ez** (diseinuz) |
| Enkriptazioa | **Bat ere ez** (diseinuz) |

---

## 2. CAN 2.0A trama baten egitura

```
┌─────┬──────────────┬─────┬─────────┬──────────────────┬─────┬─────┬─────┐
│ SOF │ Arbitration  │ RTR │ Control │ Data (0-8 byte)  │ CRC │ ACK │ EOF │
│  1b │  ID (11 bit) │  1b │   6b    │    0-64 bit      │ 16b │  2b │  7b │
└─────┴──────────────┴─────┴─────────┴──────────────────┴─────┴─────┴─────┘
```

- **SOF**: Frame-aren Hasiera — tramaberria hasten duen bit dominante (0).
- **Arbitration ID**: Mezuaren mota eta lehentasuna identifikatzen du.
- **RTR**: Urruneko Transmisio Eskaera — datuen eskaera (injekzioan ez da erabiltzen).
- **DLC**: Datu Luzera Kodea — datu-byteen kopurua (0-8).
- **Data**: Mezuaren edukia (gehienez 8 byte).
- **CRC**: 15 errore-egiaztapen bit + mugatzailea.
- **ACK**: Mezua zuzen jasotzen duen edozein nodok ACK bit dominante batekin erantzuten du.

---

## 3. Ibilgailu modernoen sareko arkitektura

Ibilgailu modernoek **40 eta 100 ECU (Electronic Control Unit)** bitartean izan ditzakete **gateway**-en bidez bereizitako hainbat CAN bus-etan:

```
┌─────────────────────────────────────────────────────┐
│                   GATEWAY ECU                       │
│                                                     │
│  CAN Bus Motorra    │  CAN Bus Karozeria  │  LIN    │
│  ───────────────    │  ─────────────────  │  ───    │
│  Motorra, Transm.   │  Argiak, Ateak      │  Eserlekuak │
│  ABS, ESC           │  Klimatizazioa      │  Ispilua    │
│                     │  Airbag-ak          │         │
└─────────────────────────────────────────────────────┘
         │
   OBD-II Ataka (diagnostiko sarbidea — sarrera-puntua)
```

---

## 4. CAN protokoloaren eraso-azalera

### 4.1 Diseinuak berezko ahuleziak

CAN protokoloa 80ko hamarkadan **fidagarritasuna** kontuan hartuta diseinatu zen, ez **segurtasuna**. Ahulezia nagusiak hauek dira:

1. **Autentifikaziorik gabe:** Edozein nodok ID arbitrarioa duten tramak bidal ditzake.
2. **Enkriptaziorik gabe:** Trafiko osoa argi dago eta edozein nodok kaptura dezake.
3. **Broadcast osoa:** Nodo guztiek mezu guztiak jasotzen dituzte.
4. **Jatorriari buruzko kontrolik gabe:** Ezin da egiaztatu zein nodok bidali duen mezu bat.
5. **ID-aren araberako lehentasuna:** Erasotzaile batek bus-a ID=0x000 frame-ekin ase dezake.

### 4.2 Sarbide fisikoko bektoreak

| Bektorea | Deskribapena |
|---|---|
| OBD-II ataka | Diagnostiko bus-era zuzeneko sarbidea (volantepean) |
| Infoentretenamenduko unitatea | Bus nagusira konektatu daiteke |
| Bluetooth/Wi-Fi modulua | Urruneko sarbidea sare-pilan ahultasunik badago |
| Konprometitutako ECU | Konprometitutako nodo batek gainerako guztiak eraso ditzake |
| Karga-kablea / USB | EV ibilgailu batzuek sare-interfazeak agerian uzten dituzte |

---

## 5. CAN bus-eko eraso motak

### 5.1 Ezagutza erasoa (pasiboa)

`candump`-ekin bus-a entzutea, dauden IDak, haien maiztasuna eta eramaten dituzten datuak katalogatzeko. Ez du ezer transmititzea eskatzen — erabat detektaezina da.

### 5.2 Alderantzizko ingeniaritza

Funtzio fisikoen aktibazioaren (botoi bat sakatzen, bolantea biratzen) eta trama jakin batzuetako datuen aldaketen arteko korrelaziotzea. Helburua: `ID → funtzio → byte → balioa` mapatzea.

### 5.3 Frame injekzioa

`cansend` edo scriptrekin trama faltsuak bidaltzea. Bus-ak ezin du trama legitimo bat faltsu batetatik bereizi. Honek aukera ematen du:
- Gidaria egin gabe funtzioak aktibatzea (txandakatzaileak, ateen blokeoa...).
- Sentsore-irakurketak ordeztu (abiadura faltsua, tenperatura faltsua...).
- Segurtasun-sistemak desaktibatu (balaztak, airbag-ak...) — **oso arriskutsua benetako ingurunean**.

### 5.4 Replay erasoa

`candump`-ekin trama-sekuentzia bat grabatu eta `canplayer`-ekin geroago erreproduzitzea. Datuak ulertu gabe ekintzak erreproduzitzeko aukera ematen du (adibidez, desblokeoaren momentua grabatuz ateak irekitzea).

### 5.5 Fuzzing

ID eta datu aleatorioetako tramak bidaltzea (`cangen`) ECU-etan ustekabeko portaerak eragiteko: berrabiarazi, izozteak, errore-egoerak.

### 5.6 Zerbitzu-ukapena (DoS)

Bus-a lehentasun maximoko tramaz gainezka egitea (ID=0x000). ECU legitimoek ezin dute arbitratu eta bus-a saturatuta geratzen da. Benetako ibilgailu batean balaztek edo norabideak erantzuteari utzi diezaiokete.

---

## 6. CAN ekosistemaren tresnak

### 6.1 can-utils (Linux)

| Tresna | Erabilera |
|---|---|
| `candump` | Trafiko-kaptura |
| `cansend` | Trama bat bidaltzea |
| `cangen` | Trafiko aleatorio sortzea |
| `cansniffer` | Aldaketen iragazketa eta bistaratzea |
| `canplayer` | Kaptura-erreprodukzioa |
| `canbusload` | Bus-karga estatistikak |
| `isotpdump` | ISO-TP mezuen kaptura (diagnostikoa) |

### 6.2 Python

| Liburutegia | Erabilera |
|---|---|
| `python-can` | Python CAN APIa (socketcan, kvaser, vector...) |
| `cantools` | DBC fitxategiekin deskodetzen |
| `scapy` | Scapy-n CAN laguntza crafting aurreratuarako |

### 6.3 Hardware

| Gailua | Konexioa | Gutxi gorabeherako prezioa |
|---|---|---|
| BluePill+ STM32 + HW-184 (usbcan) | USB→vcan | ~10€ |
| USB2CAN (8devices) | USB→SocketCAN | ~80€ |
| Kvaser Leaf Light | USB→SocketCAN | ~300€ |
| CANable | USB→SocketCAN | ~30€ |
| Raspberry Pi + MCP2515 | SPI→SocketCAN | ~40€ |

---

## 7. Esparru legala eta etikoa

> **GARRANTZITSUA:** Laborategi honetako teknikak **soilik** `vcan0 + ICSim` birtualeko ingurunean praktikatu daitezke. Baimenik gabe ibilgailuen benetako CAN sistemetara sartzea Espainiako Zigor Kodean delitu informatiko gisa tipifikatuta dago (264. art. eta ondorengoak) eta bide-segurtasuna larriki arriskuan jar dezake.

Benetako ibilgailuekin lan egiten duen segurtasun-ikertzaile batek:
1. Jabearen baimena idatziz lortu behar du.
2. Ingurune kontrolatu batean lan egin behar du (proba-bankua, gelditutako ibilgailua).
3. Aurkikuntzak modu arduratsuan komunikatu behar ditu (responsible disclosure).
4. Sekula ez du hirugarrenak arriskuan jarri behar.

---

## 8. Erreferentziak

- ISO 11898: CAN bus estandarra.
- "The Car Hacker's Handbook" — Craig Smith (OpenGarages), No Starch Press.
- ICSim: [https://github.com/zombieCraig/ICSim](https://github.com/zombieCraig/ICSim)
- can-utils: [https://github.com/linux-can/can-utils](https://github.com/linux-can/can-utils)
- usbcan (BatchDrake): [https://github.com/BatchDrake/usbcan](https://github.com/BatchDrake/usbcan)
- python-can: [https://python-can.readthedocs.io](https://python-can.readthedocs.io)
