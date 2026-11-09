# 📋 Irakaslearen Gida Praktikoa — RF Lab Euskarara

**Dokumentu hau:** Praktika antolatu eta gidatutzeko irakaslerako

---

## 🎯 Zertarako Aurkezpenak?

Laborategia praktikaburua osoa, ikasleek RF teknologia segurena ikasteko:
- **Kontzeptuala:** Zer da RF teknologia eta nola funtzionatzen duen automozioan
- **Teknikoa:** Nola kaptura, analisia eta emaitzak neurtu
- **Etikoa:** Arriskuak, legeak eta segurtasun protokoloak

**Aurkezpenak 2 eta saioen sekuentzialazioa:**

| Aurkezpena | Helburua | Erabilerak | Nondik |
|---|---|---|---|
| **RF_Teknologia_Sarrera_EU.html** | Kontzeptu + Segurtasun | 30-45 min klasean | Lehenbiziko saioa |
| **RF_Praktika_Teknikoa_EU.html** | Urrats-urratsa teknikoa | 90 min x 2 saio + 45 min | Laborategian |
| **README_EU.md** | Gida osoa irakasle/ikasleentzat | Erreferentzia | GitHub-en |

---

## 📅 Praktika Plana (Gomendatua)

### **Lehenbiziko Astea - Klasean (45 min)**

#### Lehenbiziko Emaitza: RF_Teknologia_Sarrera_EU.html

```
GARAIAK:
├─ 0-10 min: Aurkezpenaren sarrera
│            "Gaurko astean RF teknologia aztertuko dugu..."
│
├─ 10-40 min: Aurkezpena proiektadorean
│            (Slides 1-14, baina kontzentzian:)
│            • RF kontzeptuak (10 min)
│            • Automozioen arazoak (15 min)
│            • Segurtasun protokoloak (10 min)
│            • Praktika planaren zehaztasuna (5 min)
│
├─ 40-45 min: Deklarazioa Etikoa
│            ✅ DEBEKATUTA: Amaitu gabe, sinatzea aitzindari!
│            (Ikasle guztiak sinaturiko papera)
│
└─ 45+ min:   Arazoak amaitzea
            "Laborategian ez da zaila. Hurrengo astean!"
```

**Nola Erabili Aurkezpena:**
```bash
# Irakaslearen ordenagailuan
firefox --fullscreen RF_Teknologia_Sarrera_EU.html

# Nabigazioa:
# - Mouse: Botoi "→ Hurrengoa" / "← Aurrekoa"
# - Gezia: Teklatu geziak (← →)
# - F11: Pantaila osoa (irtetzeko: F11 berria)
```

**Deittuak:**
- ✅ **Slide 7-8 GARRANTZITSUA:** Segurtasun protokoloak eta legeak
  - Ez etxean erabiltzea
  - Ez benetako autoak
  - Ez jamming/erreprodukzioa
  - Laborategian bakarrik + irakaslea behean
  
- ✅ **Deklarazioa Etikoa:** Papera astean-aurretik inprimatzea

---

### **Bigarren Astea - Laborategian (90 min)**

#### Bigarren Emaitza: RF_Praktika_Teknikoa_EU.html - SAIO 1

**Baimena Öncesi:**
```
✅ Hardware osoa laboran prest
   ├─ Raspberry Pi 4/5 x 3-4 (RTL-SDR + konektak)
   ├─ Antena dipolo konektatua
   ├─ Mando proba aislatu (baterik betea)
   ├─ Kableak + USB hub
   └─ Potentzia iturria

✅ Softwareak instalatuta
   ├─ Raspberry Pi OS + RTL-SDR drivers
   ├─ rtl_fm + sox komandoak
   ├─ SSH akzesioa (Wi-Fi konfigurazioa)
   └─ Python 3 + numpy, scipy, matplotlib (laptopean)

✅ Sarea
   ├─ Raspberry Pi-ak WiFi bidez konektatuta
   ├─ SCP funtzionamendua frogatua
   └─ Laptop-etik SSH konexioa osoa
```

**Laborategian Sekuentzia (90 min):**

```
LEHENBIZIKO 10 MIN:
├─ Irekita: RF_Praktika_Teknikoa_EU.html (Slides 1-3, gidea)
├─ Arazoak: Deklarazioa sinaturik? (Aitzindari!)
├─ Gidea: Urrats osoa azaltzea (diagramak Slide 4)
└─ Askatzea: "Hasi!", talde txikiak

HARDWARE SETUPA (15 min):
├─ Slides 4-5: Gidea ikusi
├─ Taldeak: RTL-SDR + Antena konektatzea
├─ Froga: Pirrima bota (restart)
└─ Baliogitzea: "Ondo badago"

SEINALEA PROBA (10 min):
├─ Slides 5: SSH komandoak
├─ SSH: pi@raspberrypi.local konektatzea
├─ Froga: rtl_test -t (IQ samples)
└─ Emaitza: "Sartzen dute!"

BASELINE KAPTURA (5 min):
├─ Slide 6: Komandoa kopiatzea
├─ Exekuzioa: ~30 segundo, seinalerik gabe
└─ Emaitza: baseline.iq8 fitxategia

MANDO SEINALEA (30 min):
├─ Slide 7: Komandoa kopiatzea (timeout 4 segundo)
├─ Sakatuak: 5 aldiz mandoa (sakatzea + 4 segundo)
│            capture_001.iq8, capture_002.iq8, ...
├─ Taldeak: Taldearen mandoa bana
└─ Emaitza: 5 fitxategi .iq8

TRANSFERENTZIA (20 min):
├─ Slide 7: SCP komandoa kopiatzea
├─ Transfer: Laptop-era deskargatzea
│            scp pi@rpi:*.iq8 ~/captures/
├─ Baieztazioa: ls -lh *.iq8 (fitxategiak aditzen direla)
└─ Emaitza: Kaptura osoa laptopean prest
```

**Irakaslearen Ardura:**
- ✅ Monitoring: Talde guztiak ondo joaten duten
- ✅ Arazoak: SSH konexioa, komandoak
- ✅ Segurean: Mando bakarrik sakatzen duten, ez beste
- ✅ Denboraz: Kronometro ikusita, atentzio-bilerak

**Laborategian DEBEKATUTA:**
- ❌ Benetako autoak
- ❌ Jamming edo erreprodukzioa
- ❌ Ekipoa etxea eraman

---

### **Hirugarren Astea - Laborategian (90 min)**

#### Hirugarren Emaitza: RF_Praktika_Teknikoa_EU.html - SAIO 2

**Aurrealdiak:**
```
✅ Fitxategiak transferituak (capture_*.iq8 laptopean)
✅ Python instalatuta (numpy, scipy, matplotlib)
✅ IDE-a prest (VSCode, Jupyter, ipython)
```

**Laborategian Sekuentzia (90 min):**

```
LEHENBIZIKO 10 MIN:
├─ Irekita: RF_Praktika_Teknikoa_EU.html (Slides 8-12, gidea)
├─ Askarrean: Python kode-a inprimatzea edo screenean
└─ Desbidea: "Gaurko astean grafikak sortzuko dugu"

PYTHON SETUP (10 min):
├─ Slides 8-9: Kode-a eta liburu-ak
├─ Taldeak: Kode-a fitxategi Python batean kopiatzen
├─ Froga: python3 script.py (errorerik ez?)
└─ Emaitza: Script osoa prest

POTENTZIA GRAFIKAK (20 min):
├─ Slides 8-9: Kode-a deskribatzen (zer egiten duen)
├─ Exekuzioa: python3 script.py
├─ Emaitza: analisis.pdf grafika bietan
├─ Kontrol: Potentzia denboraz eta espektroa?
└─ Errore-ikusgaia: matplotlib arazoak (pip reinstall)

ESPEKTROA + ESPEKTROGRAMA (20 min):
├─ Slides 9-10: Kode-a gehitzea (FFT)
├─ Exekuzioa: python3 script.py (berria)
├─ Emaitza: 3 grafikak (potentzia, espektroa, espektrograma)
└─ Ikusi: Seinaleak ondo aditzen diren?

GERTAERA DETEKTATZEA (20 min):
├─ Slides 10-11: Detektazioa-kode-a
├─ Exekuzioa: python3 script.py (events.json sortzea)
├─ Emaitza: Sakatze momentua neurtzea (hasiera, amaiera, iraupena)
└─ Baieztatzea: events.json irekita emaitzak

KONPARAZIOA CAPTURES ARTEAN (15 min):
├─ Slides 11-12: Konparatzaile-kode-a (5 capture)
├─ Exekuzioa: python3 script.py
├─ Emaitza: konparazioa.pdf (5 grafikak bata bestearen azpian)
└─ Analisia: Forma berdinak? Potentzia berdinak? Zeinek dute zehatzago?

TXOSTEN HASIERA (15 min):
├─ Markdown: Fitxategi baten hasitzea (INFORME_ALUMNOS.md txantiloia)
├─ Sekzioak: Sarrera, Hardware, Prozedura, Emaitza (grafikak inpegatzea)
└─ Ondorengo astean: Analisia osoa eta ondorioak

LEHENBIZIKO TXOSTEN EMAITZA:
├─ Beltza: Potentzia grafikak (2)
├─ Beltza: Espektroa grafika (1)
├─ Beltza: Espektrograma (1)
├─ Beltza: Konparazioa (5 capture anitzen grafikak 1 paperean)
└─ Beltza: Gertaeren JSON emaitzak
```

**Irakaslearen Ardura:**
- ✅ Monitoring: Python arazoak (llibre instalazio, sintaxia)
- ✅ Arazoak: Memory errors, matplotlib pantaila ez irekitzen
- ✅ Laguntza: Kode-aren logika (zer egiten duten FFT, gertaera detection)
- ✅ Motibatzea: "Grafikak polita! Behemoka gai handiak hartzea..."

**Kodea Konpontzea (Arazoak):**
- **Memory Error:** Fitxategiak chunketan irakurri (250000 sample = 10 seg)
- **Matplotlib ez kargatu:** `pip install matplotlib --upgrade`
- **FFT arazoak:** Zenbakia bati "1e-10" gehitzea (division zero ez)

---

### **Laugarren Astea - Laborategian (45 min)**

#### Laugarren Emaitza: RF_Praktika_Teknikoa_EU.html - SAIO 3

**Aurrealdiak:**
```
✅ Txosten gutxienez sarrera + grafikak dutenak
✅ Python analisia amaituak
✅ Taldeak aurkeztu prest (5 min < 5 min)
```

**Laborategian Sekuentzia (45 min):**

```
LEHENBIZIKO 5 MIN:
├─ Irekita: RF_Praktika_Teknikoa_EU.html (Slides 13, gidea)
└─ Arazoak: "Aurkezpenaren egitura nola?"

TXOSTEN AMAITZEA (20 min):
├─ Analisia osoa idatzitzea (zer ikusten dugu grafiketan)
├─ Ondorioak: Zer ikasi dugu? Eta defentsak?
├─ Ebidentziak: Argazkiak laborategia (hardware, emaitzak)
└─ PDF: Fitxategi osoa inprimatzea/gordetzea

AURKEZPENA TALDEAN (15 min):
├─ Taldea 1: 5 minutu presentazioa
├─ Irakaslea: Galdera 2-3 (zer jarduera?)
├─ Gainerakoa: Entzutea eta balorazioa
│
├─ Taldea 2: 5 minutu presentazioa
├─ Irakaslea: Galdera 2-3
├─ Gainerakoa: Entzutea eta balorazioa
│
└─ ...

SINATZEA + KALIFIKAZIOA (5 min):
├─ Deklarazioa sinatura (amaiera, hasiera)
├─ Rubrika betetzea (1-5 puntua)
│  ├─ Hardware setupa + Prozedura
│  ├─ Emaitzak (grafikak kalitatea)
│  ├─ Analisia (interpretazioa)
│  ├─ Txosten dokumentua
│  └─ Aurkezpena + Debate
│
└─ Emaitza: Kalifikazioa ordenagailuan
```

**Aurkezpenean Entzuteak:**

Irakaslea astebada galdera:
- ❓ Zer da garrantzitsuena grafiketan?
- ❓ Sakatze 5 berdinak? Zenek aldaerak?
- ❓ Zarata badu seinalea? Nola neurtu?
- ❓ Replay atakea detektatu ahal genuke?
- ❓ Zer defentsa hobea? (Rolling codes? Encryption?)

---

## 🛠️ Irakaslearen Zerren Zerrenda (Lehenbiziko Astea)

### Astea Aurretik:

```bash
☐ Fitxategi guztiak deskargatzea GitHub-etik
☐ README_EU.md irakurrita (Gida osoa)
☐ RF_Teknologia_Sarrera_EU.html testatzea (browser)
☐ RF_Praktika_Teknikoa_EU.html testatzea (browser)

☐ Hardware froga
  ☐ RTL-SDR + RPi konexioa osoa
  ☐ Drivers instalatuta (rtl_fm, sox)
  ☐ SSH akzesioa funtzionamendua frogatua
  ☐ Antena konektatua (433 MHz dipoloa)
  ☐ Proba mandoa aislatu (baterik betea)

☐ Laborategian sarea
  ☐ RPi-ak WiFi konektatuta
  ☐ Laptop-ak SSH akzesioa
  ☐ SCP transferentzia frogatua

☐ Python-a laptopean
  ☐ Python 3 instalatuta
  ☐ pip install numpy scipy matplotlib
  ☐ Python script-ak frogatuta (kodea)

☐ Dokumentazioa
  ☐ Deklarazioa Etikoa inprimatzea (kopiak)
  ☐ INFORME_ALUMNOS.md txantiloia kopiatzea
  ☐ Rubrika kalifikazioa osoa
  
☐ Ikasleak beren aldetik
  ☐ Irabili: README_EU.md + 04_ETICA_Y_SEGURIDAD.md irakurtzea
  ☐ Prest: Deklarazioa sinatzea lehenbiziko klasean
```

### Lehenbiziko Klasean (45 min):

```bash
☐ Laborategian aurkezpena proiektadorean (30 min)
  ☐ Firefox ireki, full screen, aurkezpena
  ☐ Slide 1-14 erakustea, azaltzen RF kontzeptuak
  ☐ PAUSE Slides 7-8: Segurtasun protokoloak, arauak
  
☐ Deklarazioa Etikoa (10 min)
  ☐ Papera banatzea guztiei
  ☐ Irakurketa: Sekzioa garrantzitsuak
  ☐ Sinatzea: Guztiek sinaturik (aitzindari!)
  ☐ Irakaslearen sinadura (datarekin)
  
☐ Laborategi sarea froga (5 min)
  ☐ RTL-SDR ukusi, konekta (ez informatika agatik)
  ☐ "Laborategian hau guztia egiten dugu"
  ☐ Denborak: "Hurrengo astean hasten dugu!"
```

### Bigarren Astea - Laborategian:

```bash
☐ Aurretik (24 orduak aurretik)
  ☐ Hardware osoa prest, frogaturik (RTL-SDR + RPi)
  ☐ WiFi sarea funtzionamendua
  ☐ Python libururak Laptop-an
  ☐ Aurkezpena zabalita: RF_Praktika_Teknikoa_EU.html
  
☐ Laborategian astea
  ☐ Talde txikiak (3-4 ikasle/taldea)
  ☐ RPi-akta banatzea (1 taldean 1)
  ☐ SSH konexioa frogatua
  ☐ Komandoak kopiatzea (edo bash script)
  ☐ Mando saka irudia (baseline + 5 saka)
  ☐ Fitxategiak transferitzea
  
☐ Amaitzean astea
  ☐ Kapturaren estatusa: Denbora nahikoa? Fitxategiak eskura?
  ☐ Denborak: "Hurrengo astean grafikak egingo ditugu"
```

### Hirugarren Astea - Laborategian:

```bash
☐ Aurretik (24 orduak aurretik)
  ☐ Python script-ak prest (Slides 8-12-en kodea)
  ☐ Aurkezpena zabalita: RF_Praktika_Teknikoa_EU.html
  ☐ Ikasleak fitxategiak laptopean (capture_*.iq8)
  
☐ Laborategian astea
  ☐ Python kodea taldeak:
    ☐ Potentzia grafikak
    ☐ Espektroa + Espektrograma
    ☐ Gertaera detektatzea
    ☐ Konparazioa (5 sakat anitzak)
  ☐ Txosten hasiera (Markdown)
  ☐ Emaitza: Grafikak + JSON + Markdown beteko
  
☐ Amaitzean astea
  ☐ Python analisia: Ondo joaten du?
  ☐ Arazoak: Memory, matplotlib, numpy
  ☐ Denborak: "Aurkezpena astean osoa!"
```

### Laugarren Astea - Laborategian:

```bash
☐ Aurretik (24 orduak aurretik)
  ☐ Aurkezpena zabalita: RF_Praktika_Teknikoa_EU.html (Slide 13)
  ☐ Taldeen aurkezpena programatua (6 min x taldeak)
  ☐ Rubrika kalifikazioa prest (kopiak)
  
☐ Laborategian astea
  ☐ Talde txikiak sortuta (aurkezpena ordena)
  ☐ Txosten amaitzea (analisia + ondorioak)
  ☐ Aurkezpena (talde 1, 2, 3...)
  ☐ Irakaslearen galderak
  ☐ Kalifikazioa betetzea
  
☐ Amaitzean astea
  ☐ Balioak irakasle-sistemari argitu
  ☐ Ebidentziak gordetzea (PDF, argazkiak)
  ☐ Feedback ikasleak: "Zer ikasi duzu?"
```

---

## ❓ Irakaslearen FAQ

**P: Zer egiten du ez bada sinaturik deklarazioa etikoa?**
R: Ez. Amatetik ez. Balioak 0/5 balioan. Astean beste talde bat egitea iradokitzen.

**P: Laborategian arazoa: RTL-SDR ez detektatua?**
R: 
```bash
# Laborategian amaitzea
lsusb  # RTL-SDR aurkitzen du?
sudo apt update
sudo apt install rtl-sdr
rtl_test -t  # Berria froga
```

**P: Seinalea oso ahula, zarata asko?**
R: 
- Antena urrunago edukitzea (-g 49.6 gain gehitu)
- Laborategian RF zarata minimoa?
- Bateria mandoan betea?
- Sakatu mando laborategian gutxiago perturbazio

**P: Python memory error?**
R: Fitxategiak chunketan irakurri (250k sample x 10 seg, ez osoa)

**P: Taldea astean osoa ez lortzen (denbora gutxi)?**
R: OK. Urratsa txikian kalifikatzea:
- Kaptura osoa? (+3 puntu)
- Python partziala? (+1-2 puntu)
- Txosten gutxia? (+1 puntu)
- Aurkezpena ez? (0 puntu aurkezpena)

**P: Laborategian praktika nola otsaita daitezke (pandemia, online)?**
R: Simulazio-fitxategiak erabiltzea (lab-scripts/ adina capture*.iq8 adibide)

**P: Emaitzak publikatzea ahal dugu?**
R: ❌ Ez. Irudia kaleko ekipoak detektazioa. Beti pribatua kodea.

---

## 📚 Erreferentzia Dokumentazioa

Irakaslearen erreferentziatzat:

### Segurtasunean:
- `RF_Lab_Seguro/docs/04_ETICA_Y_SEGURIDAD.md` — Legea, deklarazioa, kasoak

### Kontzeptuala:
- `RF_Lab_Seguro/docs/06_ZER_DA_HACKRF_AZALPENA_EU.md` — RF kontzeptuak, diagrama
- `RF_Lab_Seguro/docs/06_QUE_ES_HACKRF_EXPLICACION.md` — Originalean espaniolla

### Teknikoa:
- `RF_Lab_Seguro/docs/07_PRAKTIKA_HACKRF_ERREPRODUKZIOA_EU.md` — Laborategian urratsak
- `RF_Lab_Seguro/docs/03_PROCEDIMIENTO_CAPTURA.md` — RTL-SDR komandoak zehatza
- `RF_Lab_Seguro/docs/08_DESPLEGUEA_HACKRF_TRESNAK_EU.md` — Hardware instalazioa

### Skripteak:
- `RF_Lab_Seguro/scripts/spectrum_capture.sh` — RTL-SDR kaptura bash
- `RF_Lab_Seguro/scripts/analyze_spectrum.py` — Analisia Python
- `RF_Lab_Seguro/scripts/event_detector.py` — Gertaera detektatzea

### Txantiloia:
- `RF_Lab_Seguro/templates/INFORME_ALUMNOS.md` — Txosten moldea
- `RF_Lab_Seguro/templates/CHECKLIST_SEGURIDAD.md` — Segurtasun zerrenda

---

## 🎓 Laborategian Moralak

**Ikasleak utzi nahi dituzu sesioan:**

1. ✅ **Teknologia ulertzea:** "RF nola funtzionatzen du benetakoan"
2. ✅ **Arriskuak eta defentsa:** "Atakaak zer? Nola defendatzen dituzten?"
3. ✅ **Etikaaren garrantzia:** "Benetako arriskua. Arauak ez dira baliogabeak."
4. ✅ **Pentsamendu kritikoa:** "Beste defentsa ahal genuke? Nola?"
5. ✅ **Dokumentazio eta analisia:** "Lana erakundean honelakoa da."

**Berriki frasa irudia:**
> "Laborategia ez da joko, benetako segurtasun ariketak dituzten. Etxean etxean erabiltzeak delitua da — ez da balioba. Baina laborategian, segurean eta etzanda, ulertu dezakete atakaak eta defentsa. Horrek dira gaitasuna duten siberosasun karreran!"

---

## 📞 Kontaktuak Laguntza

**Arazoak bada:**
- 📧 Irakasle-kideari kontua egitea (RF lab mentoria)
- 📋 GitHub Issues: Aurkezpenen hobetzeak proposatzea
- 💻 Python arazoak: Stack Overflow + matplotlib dokumentazioa

---

**Gaurko dokumentazioa irakurrita? Praktika prest labora!** 🚀

Laborategian oso-osoa, segurtasun eta etika beti lehena! ⚠️
