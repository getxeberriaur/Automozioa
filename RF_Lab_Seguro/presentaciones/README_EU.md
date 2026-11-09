# 🛰️ RF Laborategia Euskarara - Aurkezpenak

Laborategian praktika RF-a egiteko dokumentazioa **euskaraz** doa guztia.

---

## 📊 Aurkezpenak (2 Fitxategi)

### 1️⃣ **RF_Teknologia_Sarrera_EU.html**
**Helburua:** Ikasleek RF teknologia, arriskuak eta protokoloak ulertzea

- 🎯 14 slide-ko aurkezpena
- ⏱️ 30 minutu klasearen sarreran
- 👥 Taldearen gulegoa (ikasle + irakaslea)

**Edukia:**
- Zer da RF? (eta analogia)
- Automozioan RF sistemak (RKE/PKES)
- Atakaak eta belburrean (Replay, Relay, Jamming, Spoofing)
- Segurtasun protokoloak eta arauak
- Praktika plana eta materiala
- Ebaluazioa eta FAQ-ak

**Nola erabiltzea:**
```bash
# Ireki browser-an
firefox RF_Teknologia_Sarrera_EU.html

# Botoiak:
← Aurrekoa / Hurrengoa →
# Edo: Teklatu ezker/eskuin geziak
```

**Nondik deskargatua:**
- GitHub: `RF_Lab_Seguro/presentaciones/RF_Teknologia_Sarrera_EU.html`
- Direkta: Irakaslea erakutsiko du projektorean

---

### 2️⃣ **RF_Praktika_Teknikoa_EU.html**
**Helburua:** Praktika laborategian urrats-urratsean egitea

- 🎯 15 slide-ko gida teknikoa
- ⏱️ Laborategian ordenatu (4-5 orduak, 3 saioan)
- 👥 Taldeen lan praktikoa

**Edukia:**
- Aurrekondaketa (hardware, software)
- Saio 1: Hardware setupa + Kaptura (90 min)
- Saio 2: Analisia Python-ekin (90 min)
- Saio 3: Dokumentua + Aurkezpena (45 min)
- Arazoak konpontzea (FAQ teknikoa)
- Kalifikazioa eta rubrika

**Komandoak eta Kodea:**
- SSH konexioa Raspberry Pi-ra
- RTL-SDR kaptura komandoak
- Python skripteak (grafika, analisia)
- JSON exportazioa emaitzen

**Nola erabiltzea:**
```bash
# Laborategian ordenatu
# Irakaslea: Proiekadorean bistaratu
# Ikasleak: Laptopan irekita, urrats segitzea
```

**Nondik deskargatua:**
- GitHub: `RF_Lab_Seguro/presentaciones/RF_Praktika_Teknikoa_EU.html`
- Direkta: Irakaslea emango du link-a praktikan

---

## 📁 Fitxategien Antolatze

```
RF_Lab_Seguro/
├── presentaciones/
│   ├── RF_Teknologia_Sarrera_EU.html     ← LEHENBIZIKO saioan
│   ├── RF_Praktika_Teknikoa_EU.html      ← LABORATEGIAN
│   ├── (Spanish originals...)
│   └── README_EU.md                       ← HI (gaur)
│
├── docs/
│   ├── 06_ZER_DA_HACKRF_AZALPENA_EU.md
│   ├── 07_PRAKTIKA_HACKRF_ERREPRODUKZIOA_EU.md
│   ├── 08_DESPLEGUEA_HACKRF_TRESNAK_EU.md
│   ├── 04_ETICA_Y_SEGURIDAD.md            ← Sinatzea AITZINDARI!
│   └── (English/Spanish originals...)
│
├── scripts/
│   ├── spectrum_capture.sh               ← RTL-SDR kaptura
│   ├── analyze_spectrum.py               ← Python analisia
│   └── event_detector.py                 ← Gertaeak detektatzea
│
└── templates/
    ├── INFORME_ALUMNOS.md                ← Txosten txantiloia
    └── CHECKLIST_SEGURIDAD.md            ← Segurtasun zerrenda
```

---

## 🚀 Praktika Saioen Kronograma

### **Lehenbiziko saioa (30-45 min)**
1. Aurkezpena: `RF_Teknologia_Sarrera_EU.html` (projektorean)
2. Sinatzea: Ikasle guztiak deklarazioa etikoa
3. Laborategia: Hardware aurkezpena eta funtzionamendua

### **Bigarren saioa (90 min - Kaptura)**
1. Gidea: `RF_Praktika_Teknikoa_EU.html` (saio 1. zatia)
2. Lanean: Raspberry Pi + RTL-SDR kaptura
3. Transferentzia: Fitxategiak laptopera

### **Hirugarren saioa (90 min - Analisia)**
1. Gidea: `RF_Praktika_Teknikoa_EU.html` (saio 2. zatia)
2. Lanean: Python analisia, grafikak
3. Dokumentua: Txostena hasitzea

### **Laugarren saioa (45 min - Dokumentu+Aurkezpena)**
1. Gidea: `RF_Praktika_Teknikoa_EU.html` (saio 3. zatia)
2. Lanean: Txostena amaitzea
3. Aurkezpena: Taldeak 5 min aurkezten, beste galderak

---

## ⚠️ Garrantzitsua: Dokumentazioa Irakurtzea AURRENA

**Praktika haskeran, DEBEKATUTA:**
1. **04_ETICA_Y_SEGURIDAD.md** irakurrita (30 min)
2. Deklarazioa etikoa **sinaturik** aurrean
3. Irakaslearekin sinadura egitea (fisikoa edo digitala)

**Batzuetan:**
- Ez bada sinaturik, ez zaude sartuko laborategian
- Deklarazioa: Benetako kontratu legala, ez baliatzea
- Kalifikazioa: 0/5 ez bada sinaturik

---

## 🛠️ Hardware Laborategian

```
Eskaratua / Taldeako:
├─ Raspberry Pi 4/5 (2GB RAM min)
├─ RTL-SDR Dongle (RTL2832U)
├─ Antena Dipolo 433 MHz
├─ Kableak USB + Antena
├─ Mando Proba 433 MHz (isolatua)
└─ Laptop (Linux/macOS/Win+WSL2)

Softwarea:
├─ Linux (Raspberry Pi OS)
├─ Python 3 + numpy, scipy, matplotlib
├─ rtl_fm + sox (captura)
└─ SSH (konexioa)
```

---

## 📖 Nola Erabiltzea Aurkezpenak

### Konputadore/Taula-ean:
```bash
# 1. Deskargatu fitxategia
wget https://raw.githubusercontent.com/getxeberriaur/Automozioa/main/RF_Lab_Seguro/presentaciones/RF_Teknologia_Sarrera_EU.html

# 2. Irekita browser-ean
firefox RF_Teknologia_Sarrera_EU.html
# Edo: chromium, safari, explorer...

# 3. Nabigazioa:
# - Botoi "→ Hurrengoa" / "← Aurrekoa"
# - Teklatu: Geziak (← →)
# - Puntu eta: Slide zenbakia hautatu
```

### Gela-projektor-ean:
```bash
# Irakaslea ordinaroa
firefox --fullscreen RF_Teknologia_Sarrera_EU.html

# Altxoren botoiak bera (mouse + gezia)
# Notak-ko txikia pantailan: F11 (full screen)
```

---

## 🎯 Aurkezpenak Nola Egitea (Irakasleentzat)

### **Lehenbiziko aurkezpena (RF_Teknologia_Sarrera_EU.html)**
- Denbora: 30-45 min
- Etapa: Lehenbiziko klasean, praktika aurretik
- Helburua: Ikasleen entusiasmo + segurtasun egitea

**Ahalmenak argitua:**
- Slide 1-5: Kontzeptua (zer da RF, espektroa)
- Slide 6-8: Arrisku-atakaak
- Slide 9-11: Segurtasun protokoloak
- Slide 12-14: Praktika plana + FAQ

**Eduki interesa:**
- Kasuak errealak (RollJam, Relay atakak)
- Diagramak bisuala (kaptura fluxua)
- Segurtasun deklarazioa (legez-oharra)

### **Bigarren aurkezpena (RF_Praktika_Teknikoa_EU.html)**
- Denbora: 90 min (3 saioan banatuta)
- Etapa: Laborategian praktikan
- Helburua: Urrats-urratsa gidea kodetik

**Adabakiak:**
- Slide 1-3: Aurrekondaketa eta diagrama
- Slide 4-7: Saio 1 (Hardware + Kaptura)
- Slide 8-12: Saio 2 (Analisia + Python)
- Slide 13-15: Saio 3 (Dokumentu + Presentazioa)

**Taktika:**
- Irakaslea: Slide bistaratu
- Ikasleak: Urrats segitzea (ordenagailuan txikian)
- Ardura: Komandoak buruan, Python kode-a kopiaketa

---

## ❓ FAQ - Aurkezpenei Buruz

**P: Offline-an erabiltzea ahal duzu?**
R: Bai! Fitxategi HTML autonomoa da (internet gabe). Deskargatua eta ireki batera.

**P: Diapositibak inprimatuak?**
R: Nahi bada, browser-an: Ctrl+P → PDF → Inprimatu. 15-20 orrialde.

**P: Presentazioak aldatu ahal duzuen?**
R: Bai, HTML editorean (VSCode, gedit). Dagoen CSS/HTML batzea.

**P: Zer baldintza erabil ditzaketen aurkezpenakIrakasle besteen?**
R: Libreki! Lizentzia: CC-BY-SA (egile + URL agertuak). Aiten!

**P: Arazoa: Aurkezpenak karga motel?**
R: Grafika asko. Azkara-internet laga 2-3 segundu. Ireki HTML irekita.

**P: Euskara ikasle gulegoan?**
R: Aurkezpenak 100% euskaraz. Komandoak orijinalean (Linux = englesko). Baina arazoa ez da.

---

## 🌐 Linkak eta Baliabideak

### Dokumentazioa (Euskaraz):
- ✅ `06_ZER_DA_HACKRF_AZALPENA_EU.md` — Kontzeptuala
- ✅ `07_PRAKTIKA_HACKRF_ERREPRODUKZIOA_EU.md` — Laborategian gidoa
- ✅ `08_DESPLEGUEA_HACKRF_TRESNAK_EU.md` — Instalazio gidoa

### Dokumentazioa (Espaniarra):
- `04_ETICA_Y_SEGURIDAD.md` — Segurtasun deklarazioa
- `03_PROCEDIMIENTO_CAPTURA.md` — Kaptura prosedura
- Besteak: (dokumentazio osoa, GitHub-en sarean)

### Softwareak eta Tresnak:
- **RTL-SDR:** https://osmocom.org/projects/rtl-sdr/wiki
- **GQRX:** https://gqrx.dk/
- **Python:** https://www.python.org/
- **Raspberry Pi OS:** https://www.raspberrypi.com/software/

---

## 📝 Sinatzea Deklarazioa Segurtasunean

**AITZINDARI dokumentua praktika aurretik:**

```markdown
DEKLARAZIOA ÉTICA ETA SEGURTASUN

Ni, _________________ (izena),

AITORTU dut:
1. Irakurrita RF laborategian dokumentu osoa
2. Ulertzen dut arriskuak eta legeak
3. Konfiantzatzen gaude segun gutsean:
   ✓ Ekipoa laborategian bakarrik
   ✓ Proba mandoa isolatua bakarrik
   ✓ Ez jamming, ez erreprodukzioa, ez etxean
   ✓ Ez benetako autoaren seinalea
4. Aitortu expultsioa eta kriminal karguak batzea

Sinadura: ____________________   Data: ______________

Irakaslearen sinadura: ____________________
```

**Praktika: Papera sinaturik aurrena! (Digitala: formario online).**

---

## 🎓 Laborategian Ondo Oso

```
LEHENBIZIAN:
✅ Aurkezpena: RF_Teknologia_Sarrera_EU.html
✅ Sinatzea: Deklarazioa etikoa
✅ Irakurketa: 04_ETICA_Y_SEGURIDAD.md

LABORATEGIAN:
✅ Gidea: RF_Praktika_Teknikoa_EU.html
✅ Kaptura: Saio 1
✅ Analisia: Saio 2
✅ Dokumentua: Saio 3

AMAIERA:
✅ Txosten osoa + Grafikak
✅ Python kodearen
✅ Aurkezpena taldean
✅ Sinadura eta kalifikazioa

ETXEAN:
❌ Ez erabiltzea aparatuak (DEBEKATUTA!)
❌ Ez benetako autoak (DEBEKATUTA!)
❌ Ez internet-en publikatzea (DEBEKATUTA!)
```

---

## 📞 Arazoak bada?

**Laborategian:** Irakasleari galdera zuzenean

**Aurretik:** Emaila irakasleari
- ❓ Hardware zailtasunak
- ❓ Software instalazioaren
- ❓ Deklarazioa etikoan
- ❓ Python kodea arazoak

**GitHub Issues:** (irakasleentzat)
- Aurkezpenak aldaketa proposatu
- Dokumentazioa hobetzea
- Hobekuntza ideiak

---

## 🎉 Buka!

**Laborategian oso ongi! Segurtasun eta etika beti lehena!**

Gaurko dokumentazioa irakurrita? Prest?

👉 Jarraitu gida: `RF_Praktika_Teknikoa_EU.html`
