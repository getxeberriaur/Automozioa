# F Praktika — Keyfob RF seinalearen kaptura eta relay erasoa

[Versión en castellano](09_Practica_F_RF_Keyfob.md)

**Gutxi gorabeherako iraupena:** 50 minutu  
**Zailtasuna:** Ertain-Altua  
**Tresnak:** RTL-SDR, `rtl_433`, Universal Radio Hacker (URH), `rpitx` edo bigarren SDR (relay)

---

## Helburua

Ibilgailu baten aginte-botoitik (keyfob) igorritako irrati-frekuentziako seinalea kostu txikiko SDR hargailu baten bidez kapturatu, egitura aztertu, eta ulertu zergatik den relay erasoa gaur egungo ibilgailuen lapurreta metodorik hedatuena — CAN busera edo OBD-II portura sartu gabe.

---

## Testuingurua

Gama ertain-altuko ibilgailuak lapurtzeko krimen-antolakuntzak gehien erabiltzen duen erasoa ez da CAN busa — **keyfob RF seinalearen hedapena** da. Ez du ibilgailurako sarbide fisikoa behar, ezta CAN protokoloaren ezagutzarik ere. Jabearengandik eta ibilgailutik gertu egotea nahikoa da.

### Zergatik funtzionatzen du?

Sarrera gakogabe sistemak (*keyless entry / passive entry*) honela funtzionatzen du:

```
[Autoak LF 125 kHz seinalea igortzen du] → [Keyfob-ak UHF 433/868 MHz-tan erantzuten du]
         ↑                                               ↓
   "Ba al dago keyfob bat gertu?"           "Bai, baimendutako keyfoba naiz"
         ↑                                               ↓
              [Autoak desblokeatzen du eta abiaraztea ahalbidetzen du]
```

Relay erasoak ez du kodea **deszifratzen edo klonatu** — komunikazioaren **distantzia hedatzen** du:

```
[Autoa] ←—LF—→ [Relay B autoaren ondoan] ~~~kable/RF~~~ [Relay A jabearen ondoan] ←—LF—→ [Keyfob poltsikoan]
```

Autoak uste du keyfoba 1 metrora dagoela. Errealitatean 100 metrotara edo eraikinaren beste solairuan egon daiteke.

### Rolling codes — zergatik ez duen erreproduzketa sinpleak funtzionatzen

Mando modernoak **rolling code** erabiltzen dute (KeeLoq, AUT64, Hitag2...):
- Sakada bakoitzak kode desberdina sortzen du.
- Aurreko kodea ez da baliozkoa.
- Egun batzuk geroago errepikatutako kode bat → autoak baztertzen du.

**Relay erasoak funtzionatzen du** kodea erreplikatu gabe: seinalea denbora errealean erre-transmititzen du. Keyfob-ak kode legitimoa sortzen du autoaren seinaleari erantzunez.

> ⚠️ **Abisu juridikoa:**
> - Praktika hau norberaren ibilgailuan edo baimena dugunean soilik egin.
> - Hirugarrenen komunikazioak baimenik gabe harrapatzea delitua da.
> - Helburua erasoa ulertzea da kontrakoaleak ezarri ahal izateko.
> - Ez igorri seinalerik inongo kasutan hirugarrenen ibilgailuen gainean.

---

## Beharrezko hardware-a

| Gailua | Prezioa (gutxi gora) | Funtzioa |
|---|---|---|
| **RTL-SDR v3** (edo RTL-SDR Blog v4) | ~25–35€ | SDR hargailua — keyfob seinalea kapturatu |
| 433/868 MHz antena (RTL-SDR-arekin) | — | Harrera |
| Bigarren RTL-SDR edo **HackRF One** | ~25€ / ~330€ | Erre-transmisioa (relay) — aukerazkoa |
| Linux portaila | — | USB eskuragarriarekin |

> Kaptura eta analisi demoa egiteko **RTL-SDR bakar bat** nahikoa da (~25€).  
> Relay demo osoa egiteko transmisio gaitasuna behar da: HackRF, YARD Stick One (~100€) edo Raspberry Pi bat `rpitx`-ekin.

---

## Tresnen instalazioa

```bash
# RTL-SDR driverrak
sudo apt install -y rtl-sdr librtlsdr-dev

# rtl_433 — RF protokoloen deskodetzaile automatikoa
sudo apt install -y rtl_433

# Universal Radio Hacker (URH) — RF seinaleen analisi bisualerako
pip3 install urh

# GNU Radio (aukerazkoa — analisi aurreratua)
sudo apt install -y gnuradio
```

---

## F.1 Ariketa — RTL-SDR-arekin harrera egiaztatu

### Egokigailua detektatu

```bash
rtl_test -t
# Erakutsi behar du: Found 1 device(s)
```

### 433 MHz-tan jarduera eskaneatu

```bash
# 433.92 MHz-tan entzun (keyfob-en Europako frekuentzia estandarra)
rtl_433 -f 433920000 -A
```

Autoko agintea sakatu — honelako zerbait agertu behar da:
```
time      : 2026-05-19 10:23:45
model     : Generic-Remote  id: 0xA3F2
data      : aa bb cc dd
```

> 433.92 MHz-tan ezer detektatzen ez badu, saiatu **868.35 MHz**-tan:
> ```bash
> rtl_433 -f 868350000 -A
> ```

---

## F.2 Ariketa — Kaptura eta analisia URH-rekin

### Seinale gordina kapturatu

```bash
# 433.92 MHz-ko 5 segundoko seinalea kapturatu
rtl_sdr -f 433920000 -s 250000 -n 1250000 kaptura_keyfob.cu8
```

Kaptura bitartean agintea **2-3 aldiz** sakatu.

### URH-n ireki

```bash
urh kaptura_keyfob.cu8
```

URH-n:
1. **File → Open** → `kaptura_keyfob.cu8` hautatu
2. **Sample Rate** `250000`-ra doitu
3. Pultsuak identifikatu — aginte-sakada bakoitza seinale-ráfaga bat da
4. **Analysis → Assign Labels** erabili preámburua, datuak eta CRC markatzeko
5. **Bi sakada ezberdineko** ráfagak alderatu — datuak aldatzen dira (rolling code)

### Zer behatu

| Elementua | Deskribapena |
|---|---|
| **Modulazioa** | ASK/OOK keyfob merke gehienetan; FSK moderno batzuetan |
| **Portadoraren frekuentzia** | 433.92 MHz edo 868.35 MHz |
| **Mezuaren luzera** | 32–64 bit tipikoa (KeeLoq: 66 bit) |
| **Rolling code** | Azken N bitak sakada bakoitzean aldatzen dira |
| **Preámbulo finkoa** | Lehen bitak sakada guztietan berdinak dira |

---

## F.3 Ariketa — Relay erasoaren erakustaldia (kontzeptuala)

### Erasoaren diagrama

```
Lapurreta eszenategi erreala:

  [Jabea etxean]                    [Autoa garajean / aparkalekuan]
       keyfoba poltsikoan                 keyless entry duen autoa

  [Lapurra A — jabearen ondoan]     [Lapurra B — autoaren ondoan]
       LF antena + hargailua            LF igorgailua + UHF antena

  Lapurra B-k LF seinalea aktibatzen du → keyfob-ak UHF-tan erantzuten du →
  Lapurra A-k UHF kapturatzen du → Lapurra B-ri erre-transmititzen dio →
  Lapurra B-k autoarengana bidaltzen du → Autoak desblokeatzen du eta abiaraztea ahalbidetzen du
```

### Benetako erasorako behar den denbora: < 30 segundo

### Transmisio hardware-arekin (HackRF edo YARD Stick One)

```bash
# RTL-SDR-arekin seinalea kapturatu
rtl_sdr -f 433920000 -s 250000 -n 1250000 relay_kaptura.cu8

# HackRF-rekin berehala erre-transmititu
hackrf_transfer -t relay_kaptura.cu8 -f 433920000 -s 2000000 -x 20
```

---

## F.4 Ariketa — RollJam kaptura (eraso aurreratua — demo teorikoa soilik)

> **RollJam**-ak (Samy Kamkar, DEF CON 2015) geroago erabiltzeko kode baliozkoa kapturatzen du.

### Nola funtzionatzen duen

```
1. Sakada:
  [Keyfob-ak N kodea igortzen du]
  [Erasotzaileak: seinalea blokeatzen du (jammer) + N kodea kapturatzen du]
  [Autoak ezer ez jasotze → jabeak berriro sakatzen du]

2. Sakada:
  [Keyfob-ak N+1 kodea igortzen du]
  [Erasotzaileak: N+1 seinalea blokeatu + N+1 kapturatu + N kodea ERRE-TRANSMITITU]
  [Autoak N kodea jasotzen du → desblokeatzen da]
  [Erasotzaileak N+1 kodea gordeta dauka → geroago erabiltzeko baliozkoa]
```

Erasotzaileak erabili gabeko kode baliozkoa gordetzen du. Jabeak ez du ezer nabaritzen.

---

## Kontrakoaleak — fabrikatzaileek eta jabeek zer egin dezaketen

| Kontrakoalea | Eraginkortasuna | Kostua |
|---|---|---|
| **Keyfoba Faraday poltsan gorde** | Altua — LF seinalea blokeatzen du | ~5€ |
| **Sarrera gakogabea desaktibatu** (modelo batzuetan posible) | Altua | Doan |
| **UWB (Ultra-Wideband)** — distantzia zehatza neurtu | Oso altua — relay erasoa ezinezkoa | Hardware berria |
| **PIN inmovilizatzaile** gehigarria | Altua | Aldakorra |
| **Mugimenduren sentsorea keyfob-ean** | Ertaina — geldik badago desaktibatzen da | Modelo moderno batzuk |

---

## Ibilgailuen gaineko eraso-bektore konparaketa

| Bektorea | Sarbide fisikoa behar | Martxan dagoen bitartean | Zailtasuna | Hardware-a |
|---|---|---|---|---|
| CAN injekzioa (OBD-II) | Bai — autoan | Ez | Ertaina | ~25€ |
| CAN replay (ateak) | Bai — autoan | Ez | Ertaina | ~25€ |
| RF keyfob relay | Ez | Ez (hotzeko abiaraztea) | Baxua | ~100-300€ |
| RollJam | Ez (2-5 metro) | Ez | Ertaina | ~100€ |
| OBD-II urrunekoa (Macchina A0) | Bai — OBD-II | Bai | Altua | ~50€ |

---

## Hausnarketa galderak

1. Zergatik ezin da relay erasoa rolling code konplexuagoekin soilik arindu?
2. Zer teknologia erabiltzen dute ibilgailu modernoek relay erasoaren aurka eta nola funtzionatzen du?
3. Zer desberdintasun teknikoa dago relay erasoaren eta RollJam-en artean? Zein da arriskutsuagoa?
4. Aseguru-konpainia batek sartze-indar zantzurik gabeko lapurreta patroi bat detektatzen du. Zer teknika erabiltzen ari diren lapurrak ziurrenik?
5. Zer segurtasun-neurri har dezake jabeak gaur, ia kostu gabe, relay erasoaren aurka babesteko?

---

## Ebidentziak txostenerako

- [ ] `rtl_433`-k keyfob-aren seinalea detektatzen duela erakusten duen pantaila-argazkia
- [ ] 2 sakada ezberdinetako ráfagak dituen URH-ko kaptura
- [ ] Identifikatutako portadoraren frekuentziaren eta modulazioaren anotazioa
- [ ] Bi sakaden arteko rolling code biten konparaketa
- [ ] Taldeak marraztu/dokumentatutako relay erasoaren diagrama
- [ ] Hausnarketa galderen erantzunak
