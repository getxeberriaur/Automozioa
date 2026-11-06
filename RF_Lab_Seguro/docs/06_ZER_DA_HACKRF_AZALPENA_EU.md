# 🎯 ZER DA HACKRF ZURE LANEAN? — Kontzeptualaren Gidoa

## 📺 Analogia Sinpleena

Irudika ezazu **antzoki bat bi rol desberdinekin**:

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  RTL-SDR (Hartzailea/Kamera)    HackRF (Bidalkaria/Aktorea)│
│  ════════════════════════════    ════════════════════════ │
│                                                             │
│  • Seinaleak ENTZUTEN ditu       • GRABATU dezake          │
│  • Bideo kamera moduan           • Grabatutakoa ERREPRODUZITU │
│  • Ikusten duena fitxategin biltzen du                     │
│                                                             │
│  Funtzioa: KAPTURATU            Funtzioa: ERREPRODUZITU   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 Zure Lanaren Fluxu Osoa

```
URRATSA 1: KAPTURA (RTL-SDR Raspberry Pi-n)
═════════════════════════════════════════════════════════════

    Zure RF agintea emititzen du
           │
           ├─→ [Emititzen du] "433.92 MHz"
           │
           ├─→ RTL-SDR [Antena + Dongle USB]
           │   └─→ "Uhinaren hartzea"
           │
           ├─→ Fitxategia gordeta: capture.iq8
           │   (Hauek uhinaren adierazten duten zenbakiak dira)
           │
           └─→ Transferentzia laptopera (SCP/SFTP)


URRATSA 2: ANALISIA (Laptopa Python-ekin)
═════════════════════════════════════════════════════════════

    Fitxategia capture.iq8
           │
           ├─→ hackrf_interactive.py
           │   └─→ "Kapturatutako uhina ikusten dut"
           │       ├─ Potentziaren grafika denboran
           │       ├─ Espektroa (FFT)
           │       └─ Espektrograma
           │
           ├─→ rf_capture_comparator.py
           │   └─→ "Kaptura anitzak konparatzen ditut"
           │       ├─ Gertaerak detektatu (sakatzeaz)
           │       └─ Estatistikak


URRATSA 3: ERREPRODUKZIOA (HackRF One laptopan)
═════════════════════════════════════════════════════════════

    Fitxategia capture.iq8
           │
           ├─→ HackRF One [Antena + USB interfazea]
           │   └─→ "Kapturatutako uhina zehatz-mehatz erreproduzitzen dut"
           │
           ├─→ Antena emititzen du
           │   └─→ "RTL-SDR duten pertsona batek jaso dezake"
           │
           └─→ "Zer transmititzen den jakin"


URRATSA 4: KONPARAZIOA (RTL vs HackRF)
═════════════════════════════════════════════════════════════

    Jatorrizko Kaptura (RTL-SDR)   Erreprodukzioa (HackRF)
           │                              │
           ├──────────────────────────────┤
           │                              │
    Konparatzaile analisia:
    ✓ Berdinak dira?
    ✓ Deformazioak daude?
    ✓ Zeinek dute potentzia gehiago?
    ✓ Xehetasunak galtzen dira erreproduzzioan?

```

---

## 🤔 ZERGATIK DA HACKRF GARRANTZITSUA LANEAN?

### Arrazoia 1: Erreproduktibilitasun
```
HACKRF-RIK GABE:
  "Uhina hartu nuen. Ikusi dezaket, baina erreproduzitu ezin dut.
   Uhinaren argazki estatiko bat baino ez dut."

HACKRF-REKIN:
  "Uhina hartu nuen. Zehatza erreproduzitu dezaket.
   Bideoa dut grabatua eta playback egin dezaket."
```

### Arrazoia 2: Segurtasunaren Heziketa
```
Ikasleek ulertzen dute:
  1. "Nola hartzen da benetako seinalea?" (RTL-SDR)
  2. "Nola da uhina erreproduzitzean?" (HackRF)
  3. "Zer desberdintasun dago?" (Konparazioa)
  4. "Zergatik da garrantzitsua benetako nahiz faltsua baieztatzea?"
     (Replay atakaeen eta falsifikazioen aurka defentsa)
```

### Arrazoia 3: Praktikoa Analisia
```
Zure lanaren galderei erantzun dezakete:

✓ Zein da pultso baten zehatzeko iraupena?
✓ Zein da benetako anplitudea (dBm-tan)?
✓ Zarata du? Zenbat?
✓ Zein da espektro zehatzena?
✓ Faltsua egitea detektatu daitekeen gabe?
✓ Zer informazio eztabaidatzen du uhinak gailuari buruz?
```

---

## 🔧 TEKNIKO FLUXU ZEHATZA

### 1. Fasea: Kaptura (RTL-SDR → fitxategi IQ)

```
RF agintea 433.92 MHz-tan emititzen du
        ↓
RTL-SDR hori hartzen du (2 milioien lagina segunduko)
        ↓
Lagin bakoitza = 2 zenbaki (I, Q — uhinaren osagaiak)
        ↓
Fitxategia .iq8 formatuan gordeta (uint8 interlaced)
        ↓
Tipikoa fitxategia: 480 MB 2 minutuan
        ↓
Laptopera transferentzia
```

**Zer lortu duzu:**
```
Fitxategia: capture_20261031_134500.iq8
├─ IQ laginak: 240,000,000
├─ Iraupena: 120 segundu
├─ Maiztasuna: 433.92 MHz
└─ Tamaina: 480 MB
```

---

### 2. Fasea: Bisualaren Analisia (Python)

**hackrf_interactive.py** — Tresna Interaktiboa:

```
.iq8 fitxategia irekitzen du
        ↓
5 grafika sortu aldi berean:
├─ [1] Potentzia denboran (urdina lerroa)
│   └─→ "Noiz dagoen seinalea?"
│
├─ [2] Espektro FFT (maiztasunak)
│   └─→ "Zein da maiztasun edukia?"
│
├─ [3] Potentziaren histograma
│   └─→ "Zein da potentzia banaketaren?"
│
├─ [4] Espektrograma (denbora-maiztasuna)
│   └─→ "Nola bihurtzen diren maiztasunak denboran?"
│
└─ [5] Automatikoki gertaerak detektatu (sakatzeaz)
    └─→ "Noiz sakatu duzu agintea?"

INTERAKTIBOTASUNA:
  • Lekualdatzailea denboran nabigatzeko
  • Aurretik/Ondoren botoiak 10 segunduko leihoetan
  • Zoom intereseko zonetan
  • Dena pantaila bakarrean
```

**rf_capture_comparator.py** — Konparatzailea:

```
2 edo gehiago .iq8 fitxategiak kargatzen ditu
        ↓
Albo-aldean ikusten ditu:
├─ Potentzia gainjarrita (berdinak dira?)
├─ Espektroak konparatuta (eduki berdina?)
├─ Estatistiken taula
├─ Gertaeren denbora-lerroa (sinkronizatuta?)
└─ Iraupenaren banaketa

SORTZEN DITU TXOSTENA:
  └─→ Xehetasunez estatistikak (media, min, max, etab.)
```

---

### 3. Fasea: Erreprodukzioa (HackRF)

```
HackRF laptopera konektata
        ↓
Komandoa:
    hackrf_transfer -t capture.iq8 -f 433920000 -s 2000000
        ↓
HackRF .iq8 fitxategia irakurtzen du
        ↓
Zenbakiak (I, Q) → RF seinale analogikoa bihurtzen du
        ↓
Antenaz emititzen du 433.92 MHz-tan
        ↓
RTL-SDR duten besteek jaso dezakete barruti berean
```

**Parametro garrantzitsua:**
```
-t capture.iq8         → Fitxategi hau transmititu
-f 433920000           → Maiztasuna: 433.92 MHz
-s 2000000             → Laginaren tasa: 2 milioi/segundu
-p 1                   → Potentzia maximoa (~20 dBm)
-a 1                   → Indargetzailea aktibatuta
```

---

## 🎓 ZER IKASLEEK IKASTEN DUTE?

### Kontzeptua 1: Kaptura vs Erreprodukzioa
```
"Ez da berdina zerbait GRABATZEA berdina ERREPRODUZITZEA.
 Fidelitatea garrantzitsua da komunikazioetan."
```

### Kontzeptua 2: Seinalen Autentikotasuna
```
"Kapturatutako uhina 'atzamar marken' ditu:
  - Amplitudea eta fase zehatza
  - Gailuaren ezaugarriko zarata
  - Denbora zehatza
  
 Faltsua egiten saiatzen bada xehetasun horik gabe, detektatu egiten da."
```

### Kontzeptua 3: Zaurgarritasuna eta Defentsa
```
ZAURGARRIA:        "Alarma edo blokea baten frekuentziaren balidazioaren
                    arabera errazak dira faltsua egitea."

DEFENTSA:          "Alarma balidatzen duena:
                    • Maiztasuna
                    • Modulazioa
                    • Denbora zehatza
                    • Lekualdatze kodea (sakatze bakoitzean aldatzen da)
                    
                    Askoz seguruagoa da."
```

---

## 📊 TAULA KONPARATIBO: RTL-SDR vs HackRF

| Aspektua | RTL-SDR | HackRF |
|----------|---------|--------|
| **Funtzioa** | Hartzailea (Soilik Rx) | Bidalkaria/Hartzailea (Tx/Rx) |
| **Maiztasuna** | 24 MHz - 1.7 GHz | 1 MHz - 6 GHz |
| **Zehatzak** | ±50-100 ppm | ±20 ppm |
| **Potentzia TX** | N/A | ~20 dBm (100 mW) |
| **Erabilera Tipikoa** | Kaptura, analisia | Erreprodukzioa, froga |
| **Kostua** | ~€25-40 | ~€300-400 |
| **Zure lanean** | **KAPTURA RPi-n** | **ERREPRODUKZIOA laptopan** |

---

## 🚀 PRAKTIKOA URRATS-URRATSEAN FLUXUA

### Asteagunea 1: Kaptura (Raspberry Pi RTL-SDR-rekin)

```bash
# Raspberry Pi-n
cd ~/rf_capture

# Kaptura-skriptua exekutatu
./iq_capture.sh 120 captures/

# Emaitza: capture_20261031_134500.iq8 (480 MB, 2 minutu)
```

**Zer ikusten dute ikasleek:**
- Argitasunaren interfazea
- Aurrerapenaren erakustea
- Gordeta dagoen fitxategiren berrespena
- Fitxategia tamaina

---

### Asteagunea 1: Analisia (Laptopa Linux/macOS/WSL2)

```bash
# Fitxategia deskargatu
scp pi@192.168.1.100:~/rf_capture/captures/capture_*.iq8 ./

# Interaktiboa bisualera
python3 hackrf_interactive.py capture_20261031_134500.iq8

# Zer ikusten dute:
# ✓ Benetako denboran potentziaren grafika
# ✓ Nabigazioko barra-lekualdatzailea
# ✓ 5 grafika sinkronizatuta
# ✓ Detektaturiko gertaeren zerrenda (aginte-sakatzeaz)
```

---

### Asteagunea 2: Erreprodukzioa (Laptopa HackRF One-rekin)

```bash
# HackRF laptoprako USB-ean konektatu

# Konektatuta dagoela egiaztatu
hackrf_info

# Kapturatutako fitxategia erreproduzitu
hackrf_transfer -t capture_20261031_134500.iq8 \
    -f 433920000 -s 2000000 -p 1 -a 1

# Zer gertatzen da:
# ✓ HackRF kapturatutako uhina zehatza emititzen du
# ✓ RTL-SDR gertua berriro jaso dezake
# ✓ Ikasleek erreproduktibilitasuna ulertzen dute
```

---

### Asteagunea 2: Konparazioa (Laptopa)

```bash
# Kaptura anitzak konparatu
python3 rf_capture_comparator.py capture_1.iq8 capture_2.iq8 capture_3.iq8

# Sortzen du bisualera:
# ✓ Potentzia gainjarrita
# ✓ Espektroak albo-aldean
# ✓ Estatistiken taula
# ✓ Gertaeren denbora-lerroa
# ✓ Iraupenaren banaketa
# ✓ Txostena .txt-a exportatua
```

---

## ⚠️ GARRANTZITSUA KONTUAN HARTZEA

### Legearen ikuspuntutik (Espainia/UE)
```
✅ BAIMENA:
   • Seinaleak kapturatzea hezkuntza-helburuarena
   • Analisirik gabe erreproduziturik
   • Laboratori kontrolatuan erreproduzitzea
   • Zure gailuaren historiaren fitxategiak

❌ DEBEKATUTA:
   • 433 MHz-tan laboratoriotik kanpo erreproduzitzea
   • Hirugarrenen gailuekin interferitura
   • Beste batzuen aginteak faltsua egitea
   • Enplegurik gabe zegoena zezenak
```

### Segurtasuna
```
ZU LANEAN PROTEKZIOAK:
  ✓ HackRF isolatutako antenarekin (ez kanpora dagoena)
  ✓ Saioa mugatua (<30 minutu)
  ✓ Enplegurik gabe beti hor
  ✓ Aurrez grabatutako .iq8 fitxategiak bakarrik (zuzen ez)
  ✓ Laboratorioaren itxita
```

---

## 📚 LABURPENA: HACKRF-REN ROLA ZURE LANEAN

```
╔═══════════════════════════════════════════════════════════╗
║  HACKRF = "RF Uhinen Erreproduktzailea"                  ║
║                                                           ║
║  HELBURUA:                                                ║
║  ─────────                                                ║
║  • IQ fitxategiak → benetako RF seinaleak bihurtu         ║
║  • Ikasleek ulertaraztea:                                 ║
║    1. Kaptura (RTL-SDR)                                   ║
║    2. Erreprodukzioa (HackRF)                             ║
║    3. Balidazioa (berdinak dira?)                         ║
║    4. Segurtasuna (nola defenditu?)                       ║
║                                                           ║
║  HEZKUNTZA-EMAITZA:                                       ║
║  ──────────────────                                       ║
║  Ikasleek ez DUTE SOILIK datuak ikusi.                    ║
║  RF FLUXU OSOA ulertzen dute.                             ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

---

## 🎯 ZURE LANAREN HURRENGO URRATSAK

1. **Laptopa HackRF tresnak instalatuak:**
   ```bash
   sudo apt install hackrf libhackrf0
   ```

2. **HackRF-rekin lana duten dokumentua sortu** zein duten:
   - Segurtasunaren zerrenda
   - Erreproduzziaren urratsez urratsa
   - Konparatzailearen ariketa

3. **Zure skriptak berriak (dagoeneko sortuta):**
   - `hackrf_interactive.py` — Interaktiboa bisualera
   - `rf_capture_comparator.py` — Kapuren konparazioa

4. **Silaboan integratu:**
   - Saioa 1: Kaptura (RTL-SDR, 2h)
   - Saioa 2: Analisia (Python, 1h)
   - Saioa 3: Erreprodukzioa (HackRF, 1h)
   - Saioa 4: Konparazioa eta ondoriotzak (30 min)

---

**Nola ere, galdera zureagunera edozein urrats?**
