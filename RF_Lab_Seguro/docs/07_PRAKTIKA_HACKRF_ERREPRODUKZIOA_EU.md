# 🎯 Laborategiaren Praktika: HackRF One — RF Erreprodukzioa eta Balidazioa

**Iraupena:** 2-2.5 orduak  
**Maila:** Ertaina-Aurreratua  
**Ekipamendua:** Raspberry Pi + RTL-SDR, Laptopa + HackRF One  
**Helburua:** Seinalen kaptura, erreprodukzioa eta balidazioa ulertu

---

## 📋 SEGURTASUNAREN ZERRENDA PRE-PRAKTIKA

**HASI AURRETIK, EGIAZTATU:**

- [ ] **HackRF laptopara konektata** (USB ataka)
  - Komandoa: `hackrf_info`
  - Esperatutako emaitza: "HackRF One" + bertsioa

- [ ] **HackRF antenaren konektata**
  - ⚠️ KRITIKOA: Antenak **isolatuta** egon behar du (ez kanpora)
  - Erabili 433 MHz dipolo antena (edo kablearekin egina)

- [ ] **Laborategia itxita**
  - Atzak itxita
  - Baimendua ez duten pertsonak sartu ezin

- [ ] **Enplegurik (Supervisor) hor dagoen**
  - Irakasleak edo teknikariak hor
  - Praktikaari gelak gelditu ahal du aldean

- [ ] **Aurrez grabatutako .iq8 fitxategiak**
  - ✓ EZ zuzenean kapturatu (biltegitako fitxategiak bakarrik erreproduzitu)
  - ✓ Aurretiko praktiken fitxategiak edo adibideak

- [ ] **Mugatutako iraupena**
  - Gehienez 30 minutu erreprodukzioaren
  - HackRF berotzea batzuk transmititzen badu jarraian

- [ ] **Protekzioaren ekipamendua**
  - Segurtasunaren betaurrekoak (gomendatua)
  - Lanaren eremuaren garbita

- [ ] **Dokumentazioa eskura**
  - Dokumentu hau inprimatuta edo bigarren pantailan
  - README_SCRIPTS.md erreferentzia gisaz

**SINATUTA :**
- Ikaslea: _________________________ Data: _______
- Enplegurik (Supervisor): _____________________ Data: _______

---

## 🎓 IKASKUNTZA HELBURUAK

Praktika hau amaitzean, gauza hauek egiten ahal izango dituzu:

1. ✓ **HackRF One-rekin kapturatutako IQ fitxategiak erreproduzitu**
2. ✓ **Erreproduzzioan fidelitatea balidatu** kaptura vs erreprodukzioa konparatzean
3. ✓ **Desberdintasunak detektatu** jatorrizko eta faltsutako uhinen artean
4. ✓ **Balidazioaren zaurgarritasunak ulertu** RF sistemetan
5. ✓ **Babesa proposatu sakonean** sistema seguruetarako

---

## 🔧 AURRETIK BEHARREZKOAK

### Software-a (laptopan)

```bash
# HackRF tresnak instalatu
sudo apt install hackrf libhackrf0

# Instalazioaren egiaztatu
hackrf_info

# Python dependentziak instalatu (baldin ez badira)
pip install numpy scipy matplotlib

# Scripts dagoela egiaztatu
ls ~/rf_analysis/scripts/hackrf_*.py
```

### Hardware-a

- [ ] HackRF One (USB konektata, antenarekin)
- [ ] .iq8 fitxategia aurrez kapturatua (>30 segundu)
- [ ] RTL-SDR Raspberry Pi-rean konektata (berrekapturatzeko)
- [ ] Laptopa Linux/macOS/WSL2-rekin
- [ ] Sareko tokia SCP transferentziarako

### Fitxategiak

```
Zure lanaren karpeta du:
├─ capture_original.iq8       (fitxategia erreproduzitu)
├─ hackrf_interactive.py       (bisualera)
├─ rf_capture_comparator.py   (konparatu)
└─ dokumentu_hau.md           (urrats-urratsean gidoa)
```

---

## 📖 1. ZATIA: PRESTAKETA (15 minutu)

### 1.1 Urratsak: HackRF egiaztatu

```bash
# HackRF One USB ataka laptopera konektatu

# Konexioa egiaztatu
hackrf_info

# Esperatutako emaitza:
# ╔═══════════════════════════════════════════════════════════╗
# ║         HackRF One r9                                    ║
# ╠═══════════════════════════════════════════════════════════╣
# ║ Serial Number: 0000000000000000YYYYYYYYYY               ║
# ║ Board ID Code: 0x04 (HackRF One)                        ║
# ║ Firmware Version: 2022.09.1                              ║
# ║ Part ID Number: 0xa000c21b 0x00634d44                   ║
# ║                 0x00000000 0x00000000                    ║
# ║ USB Bus Speed: High Speed                                ║
# ║ USB D+ Pullup: False                                     ║
# ║ Clock Source: Internal                                   ║
# ║ Baseband Filter Bandwidth Setting: 1750000 Hz            ║
# ║ LNA Gain: 0 dB                                           ║
# ║ VGA Gain: 0 dB                                           ║
# ║ TX VGA Gain: 47 dB                                       ║
# ╚═══════════════════════════════════════════════════════════╝
```

**Baldin `libusb_open() failed` errorea ikusten badu:**
```bash
# Udev arauak sortu
sudo nano /etc/udev/rules.d/10-hackrf.rules

# Lerroa gehitu:
# SUBSYSTEM=="usb", ATTRS{idVendor}=="1d50", ATTRS{idProduct}=="604b", MODE="0666"

# Berrcargatu
sudo udevadm control --reload
sudo udevadm trigger

# HackRF deskonektatu eta berkonektatu
```

✅ **Kontrolpuntua:** HackRF konektata eta detektata

---

### 1.2 Urratsak: IQ fitxategia prestatu

```bash
# .iq8 fitxategia dagoela egiaztatu
ls -lh *.iq8

# Esperatutako emaitza:
# -rw-r--r-- 1 user group 480M urr 31 13:45 capture_20261031_134500.iq8

# Baldin ez baduzu, Raspberry Pi-tik deskargatu:
scp pi@192.168.1.100:~/rf_capture/captures/capture_*.iq8 ./
```

**Fitxateguaren baldintzak:**
- Iraupena: gutxienez 30 segundu, gehienez 2 minutu
- Formatua: .iq8 (uint8 interlaced)
- Tamaina: tipikoki 240-480 MB
- Gertaerak (pulsazioak) ditu

✅ **Kontrolpuntua:** .iq8 fitxategia lokal dagoela

---

### 1.3 Urratsak: Skriptaak egiaztatu

```bash
# Scriptaak daudela ikusi
python3 hackrf_interactive.py --help
python3 rf_capture_comparator.py --help

# Esperatutako emaitza:
# usage: hackrf_interactive.py [-h] [--freq FREQ] [--rate RATE] ...
# usage: rf_capture_comparator.py [-h] [--freq FREQ] ...
```

✅ **Kontrolpuntua:** Skriptaak erabiltzeko prest

---

## 📊 2. ZATIA: JATORRIAREN KAPTURAREN ANALISIA (30 minutu)

### 2.1 Urratsak: Interaktiboa bisualera

```bash
# Fitxategia abri interaktiboa bisualerarekin
python3 hackrf_interactive.py capture_20261031_134500.iq8

# Interaktiboa leihoa irekiko da 5 grafika sinkronizatua
```

**Zer behatzearen:**

```
┌────────────────────────────────────────────────────────────┐
│ [1] POTENTZIA DENBORAN (goian, urdina)                     │
│     ├─ Urdina lerroa = potentzia denboran zehar             │
│     ├─ Gorri lerroak = automatikoki detektaturiko gertaerak │
│     └─ Noiz daude pulsazioak?                              │
│                                                            │
│ [2] ESPEKTRO FFT (behean ezkerretik)                       │
│     ├─ Berdea lerroa = maiztasun edukia                     │
│     └─ Nondik biltzen da energiaren gehiena?              │
│                                                            │
│ [3] HISTOGRAMA (behean eskuinetik)                         │
│     ├─ Barrak = potentziaren banaketa                      │
│     └─ Gaussiarra edo uniformea da?                        │
│                                                            │
│ [4] ESPEKTROGRAMA (erdian eskuinetik)                      │
│     ├─ Bero-mapa = potentzia vs denbora vs maiztasuna     │
│     └─ Nola bihurtzen diren maiztasunak?                   │
│                                                            │
│ [5] WATERFALL (behean)                                     │
│     ├─ Xeheagoa zoom uneko segmentuaren                    │
│     └─ Modulazioa daude? Estruktura fina?                  │
└────────────────────────────────────────────────────────────┘
```

### 2.2 Urratsak: Lekualdatzailearekin arakatzea

**Lekualdatzailea erabiltzea (barra behean):**

1. **Gertaerak lokalizatu** (pulsazioak)
   - Lekualdatzailea astiro mugitu
   - Behatu noiz igotzen diren gorri pikoak

2. **Lehenengo gertaera arakatu**
   - Lekualdatzailea lehenengo gertaerera desplazatu
   - 5 grafikak behatu momentu horretan
   - Pantaila-argazkia hartu (Print Screen)

3. **Iraupenaren analisia**
   - Zenbat du gertaerak irauten? (30 ms? 100 ms? 1 s?)
   - Gertaeren zerrendan egiaztatu (behean eskuinetik)

4. **Gertaerak konparatu**
   - Bigarren gertaerarik lokalizatu
   - Berdina al da lehenengoaren? Antzeko iraupena?
   - Beste argazkia hartu

### 2.3 Urratsak: Anotazioak

**Zure koadernoan, idatzi:**

```
JATORRIAREN KAPTURAREN ANALISIA
════════════════════════════════════

Fitxategia: ________________________________
Iraupena: ________________________________

DETEKTATURIKO GERTAERAK:
┌──────┬─────────┬──────────┬─────────────┐
│ Zk   │ Hasiera │ Iraupena │ Potentzia   │
├──────┼─────────┼──────────┼─────────────┤
│ 1    │ 10.25 s │ 1.234 s  │ -15.3 dBm   │
│ 2    │ 20.48 s │ 1.198 s  │ -14.8 dBm   │
│ 3    │         │          │             │
└──────┴─────────┴──────────┴─────────────┘

ESPEKTROAREN EZAUGARRIAK:
├─ Banda nagusia: ________________ MHz
├─ Zabalera: _________________________ kHz
├─ Potentzia media: ________________ dBm
└─ Fontoaren zarata: _______________ dBm

BEHAKARIAK:
_________________________________________________
_________________________________________________
_________________________________________________
```

✅ **Kontrolpuntua:** Kaptura analizatua eta dokumentatua

---

## 📡 3. ZATIA: HACKRF-REKIN ERREPRODUKZIOA (30 minutu)

### 3.1 Urratsak: Erreprodukzioan prestatu

**SEGURTASUNAREN KRITIKOA EGIAZTAKETA:**

- [ ] HackRF antenak isolatuta daude? (ez kanpora dagoena)
- [ ] Laborategia itxita?
- [ ] Enplegurik hor dago?
- [ ] Atzak abisuarekin "Ez sartu — RF Transmisio"?

**BALDIN BATEK EZ BADU, GELDI HEMEN**

---

### 3.2 Urratsak: Fitxategia erreproduzitu

```bash
# Erreproduzziaren komandoa
hackrf_transfer -t capture_20261031_134500.iq8 \
    -f 433920000 \
    -s 2000000 \
    -p 1 \
    -a 1

# Parametren azalpena:
# -t fitxategia.iq8  → Fitxategia hau transmititu
# -f 433920000       → Maiztasuna: 433.92 MHz
# -s 2000000         → Laginaren tasa: 2 milioi/segundu
# -p 1               → Potentzia maximoa (~20 dBm)
# -a 1               → Indargetzailea aktibatuta
```

**Esperatutako emaitza:**

```
Transmitting, press Ctrl+C to stop
Actual frequency: 433.920000 MHz
[*] 2000000 Hz sample rate
[*] Actual TX gain: 47 dB
TX: 56.32 Mb/s  (480000000 bytes / 8.51 seconds)

[✓] TX completed successfully
```

### 3.3 Urratsak: Transmisioan behakariak

**HackRF transmititzen duen bitartean (8-10 segundu):**

- Entzuten duzu zerbait? (normalean, ez dago audible soinua 433 MHz-tan)
- Berotzea gailua? (normalean, txikia da)
- LED adierazleak daude? (gorria/berdea parpadeak)

**Anotazioak:**

```
Transmisio hasita: _______________
Esperatutako iraupena: 8-10 segundu
Amaitzea: _______________

Behakariak:
_________________________________________________
_________________________________________________
```

✅ **Kontrolpuntua:** Fitxategia ondo erreproduzitua

---

## 📥 4. ZATIA: RTL-SDR-REKIN BERREKAPTUA (20 minutu)

### 4.1 Urratsak: Erreprodukzioa kapturatu

**RASPBERRY PI-N (edo RTL-SDR duen bigarren laptopan):**

```bash
# RTL-SDR konektatu
ssh pi@192.168.1.100
cd ~/rf_capture

# Kaptura exekutatu
./iq_capture.sh 120 captures/

# Galderak erantzun:
# Kapturatzea hasi? s
# (Kaptura bitartean, nor nahi batek HackRF-ari erreprodukzioa exekutatu)

# Emaitza:
# [✓] Fitxategia gordeta: captures/capture_20261031_150000.iq8
```

**DENBORA:**
- Kaptura Raspberry Pi-n hasi
- 5 segundu itxaron (egonkortzeko)
- Erreprodukzioa HackRF-an exekutatu
- Kaptura 10 segundu gehiago jarraitu

### 4.2 Urratsak: Erreproduzitako kaptura deskargatu

```bash
# Laptopetik
scp pi@192.168.1.100:~/rf_capture/captures/capture_20261031_150000.iq8 ./

# Berrizenegin desberdintasun egiteko
mv capture_20261031_150000.iq8 capture_erreproduzitua.iq8
```

✅ **Kontrolpuntua:** Bi fitxategiak dituzela:
- `capture_20261031_134500.iq8` (jatorrizkoa)
- `capture_erreproduzitua.iq8` (HackRF-ekin erreproduzitua)

---

## 🔍 5. ZATIA: KONPARAZIOA (30 minutu)

### 5.1 Urratsak: Konparatzaile exekutatu

```bash
# Bi kapturak albo-aldean konparatu
python3 rf_capture_comparator.py \
    capture_20261031_134500.iq8 \
    capture_erreproduzitua.iq8 \
    --report konparazio_jatorrizkoa_vs_erreproduzitua.txt

# Emaitza:
# [✓] Kargata: capture_20261031_134500 (120.0s, 7 gertaerak)
# [✓] Kargata: capture_erreproduzitua (120.0s, 7 gertaerak)
# 
# [*] 2 kapturak konparatzen...
# [✓] Grafikoa gordeta (6 panelak)
# [✓] Txostena gordeta: konparazio_jatorrizkoa_vs_erreproduzitua.txt
```

### 5.2 Urratsak: Grafikoak interpretatu

**6 konparatzaile grafikak sortzen diren:**

```
┌──────────────────────────────────────────────┐
│ [1] POTENTZIA GAINJARRITA                     │
│     ├─ Urdina (jatorrizkoa) vs Berdea        │
│     └─ Berdinak edo desberdintasunak daude?  │
├──────────────────────────────────────────────┤
│ [2] ESTATISTIKEN TAULA                        │
│     ├─ Media, Min, Max, Iraupena, Gertaerak  │
│     └─ Zein balioak aldatu egin diren?       │
├──────────────────────────────────────────────┤
│ [3-4] ESPEKTROAK KONPARATUA                   │
│     ├─ FFT bakoitza kaptura                  │
│     └─ Maiztasun desberdintasunak daude?     │
├──────────────────────────────────────────────┤
│ [5] DENBORA-LERROA GERTAEREKIN                │
│     ├─ Lerro bertikalak = pulsazioak         │
│     └─ Aldean gertatzen diren?                │
├──────────────────────────────────────────────┤
│ [6] IRAUPENAREN HISTOGRAMA                    │
│     ├─ Iraupenaren banaketa                   │
│     └─ Koherenteak dira?                      │
└──────────────────────────────────────────────┘
```

### 5.3 Urratsak: Sortutakoa txostena irakurri

```bash
# Txostena abri
cat konparazio_jatorrizkoa_vs_erreproduzitua.txt

# Editorean edo
nano konparazio_jatorrizkoa_vs_erreproduzitua.txt
```

**Txostenean daude:**

```
╔════════════════════════════════════════════════════════════════╗
║        KAPUREN KONPARATZAILE TXOSTENA RF-TIK                   ║
╚════════════════════════════════════════════════════════════════╝

KAPURA 1: capture_20261031_134500
  Iraupena:         120.00 segundu
  Gulegoen laguneak:    240,000,000
  Gertaerak:           7
  
  POTENTZIAREN ESTATISTIKAK:
    Media:           -25.34 dBm
    Erdikoa:         -25.20 dBm
    Desv. Est.:      2.15 dB
    Minimoa:         -45.20 dBm
    Maximoa:         -8.70 dBm

KAPURA 2: capture_erreproduzitua
  Iraupena:         120.00 segundu
  Gulegoen laguneak:    240,000,000
  Gertaerak:           7
  
  POTENTZIAREN ESTATISTIKAK:
    Media:           -24.56 dBm ← DESBERDINTASUNA
    Erdikoa:         -24.15 dBm ← DESBERDINTASUNA
    Desv. Est.:      2.34 dB
    Minimoa:         -44.80 dBm
    Maximoa:         -9.10 dBm

═════════════════════════════════════════════════════════════════
KONPARATZAILE LABURPENA

Kapura indartsuena:   capture_erreproduzitua (-24.56 dBm vs -25.34 dBm)
Potentziaren desberdintasuna: +0.78 dB

Gertaerak gehien:     Biak berdina (7 gertaerak)

ONDORIOA:
Gertaerak denboran lerrotzen diren. Potentzia media
erreproduzitako kapuran apur bat da handiagoa (+0.78 dB), ipia dela
HackRF-ren indargetzea edo inguruaren zarata gutxiago.
Erreproduzziaren fidelitatea ALTUA da.
```

### 5.4 Urratsak: Sakontzearen analisia

**Erantzun beharko lioke galderak:**

1. **Potentziaren berdina al daude?**
   - Media jatorrizkoa: _____ dBm
   - Media erreproduzitua: _____ dBm
   - Desberdintasuna: _____ dB
   - Axola duen? (>1 dB = BAI)

2. **Zerbait galtzen bada erreproduzzioan?**
   - Jatorrizko gertaerak: _____
   - Erreproduzitako gertaerak: _____
   - Nolabait falta diren?

3. **Zarata gehiagoren daude?**
   - Desv. Est. jatorrizkoa: _____ dB
   - Desv. Est. erreproduzitua: _____ dB
   - Areagotua?

4. **Nola defenditu faltsuen aurka?**
   - Potentzia baikarrik?
   - Denbora balidatu behar du?
   - Lekualdatze kodea?

---

## 📝 6. ZATIA: KONPARATZAILE ARIKETA

### Ariketa 6.1: "Faltsua Detektatu"

**Hiru kaputak izango dituzu:**

1. `jatorrzizkoa.iq8` — Jatorrizko benetako kapura
2. `erreproduzitua.iq8` — HackRF-ekin erreproduzitua (saioa hau)
3. `falsutua.iq8` — Digitalar sintetizatua (adibidea)

**Zure zeregina:**
```bash
python3 rf_capture_comparator.py jatorrizkoa.iq8 erreproduzitua.iq8 falsutua.iq8 \
    --report analisia_falsuen.txt

# Analyza eta erantzun:
# ① Zein da falsutua?
# ② Zein metrika delata? (potentzia, denbora, espektroa)
# ③ Zenbat da desberdintasuna? (dB, ms, etc.)
# ④ Nola balidatuko duzu automatikoki?
```

### Ariketa 6.2: Babesa Proposatu

**Segurtasunaren proposatu idatzi:**

```
FALTSUEN AURKA BABESA PROPOSATU
════════════════════════════════════

Nire RF sistema balidatu behar du:

1. POTENTZIA
   └─ Onargarri barrutia: _____ tik _____ dBm
   └─ Baldin <MIN edo >MAX → Baztertu

2. DENBORA
   └─ Esperatutako iraupena: _____ ms (±10%)
   └─ Barrutitik kanpo baldin → Baztertu

3. ESPEKTROA
   └─ Esperatutako banda: _____ MHz
   └─ Kanpo baldin → Baztertu

4. ZARATA
   └─ Esperatutako Desv. Est.: _____ dB
   └─ >maximoa baldin → Baztertu

5. LEKUALDATZE KODEA (OSAGARRIA)
   └─ Transmisio bakoitza kodea desberdina egon behar du
   └─ Ikusitako kodeen datu-baseari aurka balidatu
   └─ Errepikatua baldin → Baztertu (replay atakea)

ONDORIOA:
_________________________________________________
_________________________________________________
_________________________________________________
```

---

## ✅ POST-PRAKTIKA ZERRENDA

**AMAITZEAN, EGIAZTATU:**

- [ ] HackRF deskonektata eta bildetakoa
- [ ] RTL-SDR deskonektata eta bildetakoa
- [ ] Gulegoen .iq8 fitxategiak bildetakoa
- [ ] Txostena sortuta eta bildetakoa (.txt)
- [ ] Pantaila-argazkiak bildetakoa (PNG)
- [ ] Koaderna anotazioekin osamendutakoa
- [ ] Faltsuen ariketa osamendutakoa
- [ ] Babesa proposatu idatzia

**Karpetan esperatutako fitxategiak:**
```
├─ capture_jatorrizkoa.iq8
├─ capture_erreproduzitua.iq8
├─ konparazio_jatorrizkoa_vs_erreproduzitua.txt
├─ analisia_faltsuen.txt
├─ screenshot_gertaera1.png
├─ screenshot_gertaera2.png
├─ koaderna_anotazioak.txt
└─ babesa_proposatu.md
```

---

## 📊 EBALUAZIOAREN RÚBRIKA

| Alderdia | Ezin hobea (5) | Ona (4) | Onargarria (3) | Nahikoa ez (<3) |
|----------|---------------|--------|---|---|
| **Erreprodukzioa** | Akatsik ez, transmisio osoa | 1 berrsaio | Berrsaio anizkoiak | Ez da dabil |
| **Jatorriaren Analisia** | 5+ gertaerak identifikatuta, oharrak xehetasunduak | 3-4 gertaerak, oharrak argiak | 2 gertaerak, oharrak oinarrikoak | <2 gertaerak |
| **Konparazioa** | Desberdintasunak kuantifikatuta (dB, ms) | Desberdintasunak identifikatuta | Behakariak kezkoak | Analisirik ez |
| **Faltsuen Ariketa** | Behar ez dena identifikatuta + metodoa deskribatuta | Behar ez dena identifikatuta | Identifikazioa zalantza | Ebatzigabea |
| **Babesa Proposatu** | 5+ metodoak, errealistikoa, inplementagarria | 4 metodoak, errealistikoa | 3 metodoak, oinarrikoa | <3 metodoak |
| **Dokumentazioa** | Osoa, garbita, grafikoekin | Osoa, irakurtzekoa erraza | Osamendua ez baina irakurgarria | Edukia falta |

---

## 🤔 MAIZ EGITEN DIREN GALDERAK

**G: Nondik laborategitik kanpo erreproduzitu ahal dut?**
A: ❌ EZ. Debekatuta dago. Bakarrik laborategian itxita begiraparakoan.

**G: Zergatik erreproduzzioak potentzia desberdina du?**
A: HackRF indargetzea (+47 dB TX VGA) gehitzen du eta inguruko zarata izan daitekeen. Normalean.

**G: Replay atakea detektatu daiteke?**
A: BAI. Sistemak lekualdatze kodea edo denbora-marka erabiltzen badu. Horregatik garrantzitsua dena.

**G: Zer gertatzen da erreproduzzioan akatsaren egin nahi badu?**
A: Ctrl+C sakatu geldia. Berriro hasi 3.2 urratsatik.

**G: Zenbat berotzea HackRF?**
A: Asko 5+ minutu ondoren. Itxarote 10 min bigarrena ondoren.

**G: Behar dituzu grafikoak urrats bakoitzean hartu?**
A: Bai. Azken txostenaren ebidentzia diren.

---

## 📚 ERREFERENTZIAK

- [06_ZER_DA_HACKRF_AZALPENA_EU.md](06_ZER_DA_HACKRF_AZALPENA_EU.md) — Kontzeptua
- [README_SCRIPTS.md](../scripts/README_SCRIPTS.md) — Scriptaren erreferentzia
- `hackrf_interactive.py` — Manualaren interaktiboa
- `rf_capture_comparator.py` — Konparatzailearen manualak

---

## 📋 AZKEN TXOSTENAREN PLANTILLA

**PDF edo Word dokumentuarekin entregatu:**

1. **Aurreko orrialdia**
   - Izena, taldea, data
   - Izenburua: "Praktika HackRF One — RF Erreprodukzioa eta Balidazioa"

2. **Helburuak** (goian kopiatua + pertsonala)

3. **Metodologia**
   - Ekipamendua erabilia
   - Urratsa exekutatuta
   - Arazo aurkituta

4. **Emaitzak**
   - Pantaila-argazkiak (5-10 irudiak)
   - Konparatzaile grafikoak
   - Gertaeren taula

5. **Analisia**
   - 4 galderei erantzunak (5.4 zatia)
   - Emaitzaren interpretazioa
   - Ondoriotzak fidelitateaz

6. **Faltsuen Ariketa**
   - Zein detektatu duzu
   - Zergatik
   - Balidazioaren metodoa

7. **Babesa Proposatu**
   - Zure segurtasunaren diseinua
   - Espezifiko metodoak
   - Tekniko justifikazioa

8. **Eranskinak**
   - Sortutako .txt txostena
   - .iq8 fitxategiak erabilia (tamaina, iraupena)
   - Edozein eraldatutako skripta

**Luzera:** 5-10 orrialda  
**Entregaren data:** Astea ondoren saioaren

---

**Zorte zure praktikan! 🚀**

Gogoratzen: RF segurtasuna kapei buruz. Kapturatutako benetako uhinak propietateak ditu faltsua batek ezin errazki ordezka.
