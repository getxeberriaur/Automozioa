# 🚀 HACKRF TRESNAK DESPLEGUEA — Urrats-urratsean Gidoa

## 📋 Edukiaren Taula

1. **Sistemaren aurretik egiaztaketa**
2. **libhackrf (oinarri liburutegia) instalatze**
3. **hackrf_transfer eta CLI tresnak instalatze**
4. **Baimenen eta udev konfigurazioa**
5. **Instalazioaren egiaztaketa**
6. **Python tresnak instalatze**
7. **Arazoak konpontzea**

---

## 1️⃣ SISTEMAREN AURRETIK EGIAZTAKETA

### 1.1 Urratsak: Zein SO duzu?

```bash
# SO ikusi
uname -s

# Posibleak emaitza:
# Linux    → Erabili apt install
# Darwin   → Erabili brew install
# MINGW64  → WSL2 Windows-tan
```

### 1.2 Urratsak: 64 bitakoa da?

```bash
uname -m
# x86_64  → 64 bitakoa ✅
# arm64   → 64 bitakoa ARM ✅
# armv7l  → 32 bitakoa ARM (ez gomendatua)
```

### 1.3 Urratsak: Sudo baimena daukazu?

```bash
sudo whoami
# root → ✅ Baimena dauzka
```

---

## 2️⃣ AUKERA A: UBUNTU/DEBIAN (Gehien gomendatua)

### Instalazio Azkarra (Lerro Batean)

```bash
sudo apt update && sudo apt install -y hackrf libhackrf-dev libhackrf0
```

**Deskribapena:**
- `apt update` → Paketteen zerrenda eguneratu
- `hackrf` → CLI tresnak (hackrf_transfer, hackrf_info, etc.)
- `libhackrf-dev` → Aplikazioak konpilatzeko entzuleak
- `libhackrf0` → Liburutegi exekuzioa

### Instalazio Urrats-urratsean

```bash
# Urratsa 1: Biltegia eguneratu
sudo apt update

# Urratsa 2: Paketeak instalatu
sudo apt install -y \
  hackrf \
  libhackrf-dev \
  libhackrf0 \
  libusb-1.0-0 \
  libusb-1.0-0-dev

# Urratsa 3: Egiaztatu
hackrf_info
```

### Zein paketea egiten du?

| Paketea | Funtzioa |
|---------|---------|
| `hackrf` | **CLI tresnak** — hackrf_transfer, hackrf_info |
| `libhackrf0` | **Exekuzio liburutegia** — Exekutatzeko beharrezkoa |
| `libhackrf-dev` | **Garapen entzuleak** — Konpilatzeko |
| `libusb-1.0-0` | **USB liburutegia** — HackRF komunikaziorako |
| `libusb-1.0-0-dev` | **USB garapen entzuleak** — Konpilatzeko |

---

## 3️⃣ AUKERA B: macOS (Homebrew-ekin)

### Instalazio Azkarra

```bash
brew install hackrf
```

### Instalazio Eskua (Homebrew-ik ez baduzu)

```bash
# Urratsa 1: Homebrew instalatu
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Urratsa 2: HackRF instalatu
brew install hackrf

# Urratsa 3: Egiaztatu
hackrf_info
```

---

## 4️⃣ AUKERA C: ITURRITIK KONPILATU

**Erabili baldin:**
- Zure distrok ez du pakete aurrez konpilatua
- Bertsioa berriagoa behar duzu
- ARM (Raspberry Pi, etc.) erabiltzaile zara

### 1. Urratsa: Dependentziak instalatu

```bash
# Linux
sudo apt install -y \
  build-essential \
  cmake \
  git \
  libusb-1.0-0 \
  libusb-1.0-0-dev

# macOS
brew install cmake libusb
```

### 2. Urratsa: Biltegia klonatu

```bash
cd ~/tmp
git clone https://github.com/greatscottgadgets/hackrf.git
cd hackrf/host
```

### 3. Urratsa: Konpilatu eta instalatu

```bash
# Konpilazioaren karpeta sortu
mkdir build
cd build

# Konpilatu
cmake ..
make -j$(nproc)

# Instalatu (sudo behar du)
sudo make install

# Liburutegi cachea eguneratu
sudo ldconfig
```

### 4. Urratsa: Egiaztatu

```bash
hackrf_info
```

---

## 5️⃣ BAIMEN KONFIGURAZIOA (GARRANTZITSUA)

### Arazoa

```bash
# Sudo gabe exekutatzean, ikusten duzu:
hackrf_info

# Arazoa:
# hackrf_open() failed: LIBUSB_ERROR_ACCESS (-3)
# Did you mean 'sudo hackrf_info'?
```

### Irtenbidea: Udev Arauak Sortu

```bash
# Udev arauak fitxategia sortu
sudo nano /etc/udev/rules.d/99-hackrf.rules

# Lerroak gehitu:
# HackRF One (r9 eta berriagoak)
SUBSYSTEM=="usb", ATTRS{idVendor}=="1d50", ATTRS{idProduct}=="604b", MODE="0666"

# HackRF One (r8 eta zaharragoak)
SUBSYSTEM=="usb", ATTRS{idVendor}=="1d50", ATTRS{idProduct}=="6045", MODE="0666"

# Gorde: Ctrl+O, Enter, Ctrl+X
```

### Arauak Aplikatu

```bash
# Aukera 1: Udev berrargaldu (deskonektatu gabe)
sudo udevadm control --reload
sudo udevadm trigger

# Aukera 2: Berrabiatu (seguruagoa)
sudo reboot
```

### Funtzionatzea Egiaztatu

```bash
# Deskonektatu eta HackRF berrkonektatu

# Sudo gabe proba
hackrf_info

# Emaitza ikusten badu, ✅ Arrakasta! 
```

---

## 6️⃣ INSTALAZIOAREN OSOA EGIAZTAKETA

### Testa 1: CLI Tresnak

```bash
# Bertsioa erakutsi
hackrf_info --version

# Gulegoen tresna detxalu
hackrf_info
hackrf_transfer --help
hackrf_sweep --help
hackrf_debug --help
```

### Testa 2: HackRF Konexioa

```bash
# **HACKRF ONE USB-RA KONEKTATU LEHENENGO**

# Xehetasun osoa erakutsi
hackrf_info

# Esperatutako emaitza:
# ╔════════════════════════════════════════════════════════════╗
# ║               HackRF One r9                               ║
# ╠════════════════════════════════════════════════════════════╣
# ║ Serial Number: 0000000000000000YYYYYYYYYY                ║
# ║ Board ID Code: 0x04 (HackRF One)                         ║
# ║ Firmware Version: 2022.09.1                               ║
# ║ Part ID Number: 0xa000c21b 0x00634d44                    ║
# ║                 0x00000000 0x00000000                     ║
# ║ USB Bus Speed: High Speed                                 ║
# ║ USB D+ Pullup: False                                      ║
# ║ Clock Source: Internal                                    ║
# ║ Baseband Filter Bandwidth Setting: 1750000 Hz             ║
# ║ LNA Gain: 0 dB (max 40 dB)                               ║
# ║ VGA Gain: 0 dB (max 62 dB)                               ║
# ║ TX VGA Gain: 47 dB (max 47 dB)                           ║
# ╚════════════════════════════════════════════════════════════╝
```

### Testa 3: Transmisioen Proba (Segurua)

```bash
# LABORATEGIAN SOILIK
# Transmisioaren lagina erakutsi

hackrf_transfer -h

# Tipikoa komandoa:
# hackrf_transfer -t fitxategia.iq8 -f 433920000 -s 2000000 -p 1 -a 1
#
# -t = transmititu (sarrerako fitxategia)
# -f = maiztasuna (433.92 MHz = 433920000 Hz)
# -s = laginaren tasa (2 MHz = 2000000)
# -p = potentzia mailak (1 = gehienez, ~20 dBm)
# -a = indargetzailea (1 = aktibatuta)
```

---

## 7️⃣ PYTHON TRESNAK INSTALATZE

Python analisien scriptaak behar dute:

### Urratsa 1: Python 3.7+

```bash
python3 --version
# Python 3.10.x ✅
# Baldin ez baduzu:
sudo apt install python3 python3-pip python3-venv
```

### Urratsa 2: Ingurune Birtuala Sortu (Gomendatua)

```bash
# Zure lanaren karpetan
cd ~/rf_analysis

# Venv sortu
python3 -m venv venv

# Aktibatu
source venv/bin/activate
# Edo Windows-tan:
# venv\Scripts\activate

# Egiaztatu (prefixu (venv) ikusi behar duzu)
which python
```

### Urratsa 3: Python Dependentziak Instalatu

```bash
# Ingurune birtualean egon ala ez egiaztatu

# Aukera A: Banaka instalatze
pip install numpy scipy matplotlib scikit-dsp-comm

# Aukera B: requirements.txt fitxategitik
cat > requirements.txt << 'EOF'
numpy>=1.21.0
scipy>=1.7.0
matplotlib>=3.4.0
scikit-dsp-comm>=0.7.0
EOF

pip install -r requirements.txt
```

### Urratsa 4: Inportazioak Egiaztatu

```bash
python3 << 'EOF'
import numpy as np
import scipy.signal
import matplotlib.pyplot as plt
print("✅ Liburutegi gulegoak inportatu egiten duen ondo")
EOF
```

---

## 8️⃣ ANALISIAREN SCRIPTAAK INSTALATZE

### Urratsa 1: Scriptaak Deskargatu

```bash
# Aukera A: GitHub-etik
cd ~/rf_analysis/scripts
git clone https://github.com/zure_erabiltzailea/RF_Lab_Seguro.git
cd RF_Lab_Seguro/scripts

# Aukera B: Eskua kopiatze
cp hackrf_interactive.py ~/rf_analysis/scripts/
cp rf_capture_comparator.py ~/rf_analysis/scripts/
```

### Urratsa 2: Scriptaak Exekutagarriak Egitu

```bash
chmod +x ~/rf_analysis/scripts/*.py
```

### Urratsa 3: Aliasak Sortu (Aukerazkoa)

```bash
# ~/.bashrc-rean gehitu
echo "alias hackrf_viz='python3 ~/rf_analysis/scripts/hackrf_interactive.py'" >> ~/.bashrc
source ~/.bashrc

# Orain erabil dezakezu:
hackrf_viz nire_kaptura.iq8
```

---

## 9️⃣ ARAZO KONPUNTZEA

### 1. Arazoa: `hackrf_info` dioiteke "Gailu ez da aurkitu"

```bash
# Kausa: HackRF ez da detektatu

# Irtenbideak:
1. USB-rean konektata dago? Egiaztatu:
   lsusb | grep HackRF

2. Udev baimena behar du? Exekutatu:
   sudo hackrf_info
   
   Sudo-rekin dabil baina ez gabe:
   sudo chown $USER:$USER /dev/bus/usb/*/

3. Firmware kaltuta? Reprograma:
   hackrf_spiflash --write hackrf_one_usb.bin

4. Beste prozesua erabiltzen du? Itxi:
   sudo lsof | grep hackrf
   kill -9 <PID>
```

### 2. Arazoa: `Permission denied` sudo ez dena

```bash
# Kausa: Udev arauak ez dira ondo aplikatuta

# Irtenbideak:
1. Erabiltzailea plugdev taldera gehitu:
   sudo usermod -a -G plugdev $USER
   
   # Saioa berrabiarazi edo:
   su - $USER

2. Hobea udev araua sortu:
   sudo nano /etc/udev/rules.d/99-hackrf.rules
   
   # Gehitu:
   SUBSYSTEM=="usb", ATTRS{idVendor}=="1d50", \
   ATTRS{idProduct}=="604b", GROUP="plugdev", MODE="0660"
   
   # Berrcargatu:
   sudo udevadm control --reload
   sudo udevadm trigger
```

### 3. Arazoa: `libusb_open() failed: LIBUSB_ERROR_ACCESS`

```bash
# Kausa: Insufiziente baimena (sudo behar duzu)

# Azkarra irtenbidea:
sudo hackrf_info          # Sudo erabiltzea behin-behinean

# Betikoa irtenbidea:
# Goiko 2. arazoa ikus
```

### 4. Arazoa: Python scriptetan `pyusb` inportazioak huts egiten du

```bash
# Kausa: USB Python liburutegia ez da instalatuta

pip install pyusb
```

### 5. Arazoa: Konpilaziaren arazoak iturritik

```bash
# CMake ez dago:
sudo apt install cmake

# libusb-1.0-0-dev ez dago:
sudo apt install libusb-1.0-0-dev

# gcc ez dago:
sudo apt install build-essential

# Berriro saia:
cd ~/tmp/hackrf/host/build
cmake ..
make -j$(nproc)
sudo make install
```

---

## 1️⃣0️⃣ AZKARRA GIDOA SISTEMAREN

### 🐧 UBUNTU/DEBIAN

```bash
# GUZTI LERRO BATEAN
sudo apt update && \
sudo apt install -y hackrf libhackrf-dev libhackrf0 && \
sudo nano /etc/udev/rules.d/99-hackrf.rules && \
# (Udev arauak gehitu) && \
sudo udevadm control --reload && \
sudo udevadm trigger && \
hackrf_info

# Denbora: 3-5 minutu
```

### 🍎 macOS

```bash
# GUZTI LERRO BATEAN
brew install hackrf && hackrf_info

# Denbora: 2-3 minutu
# Oharra: macOS-k ez du udev arauak behar
```

### 🪟 WSL2 (Windows)

```bash
# WSL2-n (Ubuntu 20.04+)
sudo apt update && \
sudo apt install -y hackrf libhackrf-dev libhackrf0

# Oharra: Baldin HackRF ez da detektatu WSL2-n:
# Erabili USBIPD Windows-tik gailu bideratu
# https://github.com/dorssel/usbipd-win
```

### 🍓 RASPBERRY PI (ARM)

```bash
# Raspberry Pi OS-n (Debian-based)
# Konpilazioak behar du (denbora gehiago)

# Aukera azkarra (baldin paketea prekonpilatua badago):
sudo apt install hackrf

# Aukera konpilazioa (20-30 min):
cd ~/tmp
git clone https://github.com/greatscottgadgets/hackrf.git
cd hackrf/host
mkdir build && cd build
cmake ..
make -j4  # (4 = CPU nukleoen zenbakia)
sudo make install
sudo ldconfig
```

---

## 1️⃣1️⃣ AZKEN ZERRENDA

### ✅ Instalazioaren Osoa Egiaztatu

```bash
# Testa 1: Instalatuta dagoela?
which hackrf_info
# Irudia: /usr/bin/hackrf_info edo antzekoa

# Testa 2: Zein bertsioa?
hackrf_info --version

# Testa 3: Hardware detektatu?
hackrf_info
# Irudia: "HackRF One r9"

# Testa 4: Sudo gabe erabil daiteke?
hackrf_info 2>&1 | grep -q "HackRF" && echo "✅ OK" || echo "❌ Baimena"

# Testa 5: Python lista?
python3 -c "import numpy, scipy, matplotlib; print('✅ Python OK')"

# Testa 6: Analisien scriptaak?
ls ~/rf_analysis/scripts/hackrf_*.py
```

### Zerrenda

- [ ] `hackrf_info` gailu agerian du
- [ ] Sudo beharra ez dut
- [ ] `hackrf_transfer --help` dabil
- [ ] Python 3.7+ instalatuta
- [ ] numpy, scipy, matplotlib instalatuta
- [ ] Scriptaak hackrf_*.py deskargatuta
- [ ] Exekuta dezaket: `python3 hackrf_interactive.py fitxategia.iq8`

---

## 1️⃣2️⃣ HURRENGO URRATSAK

Instalazioaren ondoren, ahal duzu:

1. **Bisualera proba:**
   ```bash
   python3 hackrf_interactive.py nire_kaptura.iq8
   ```

2. **Konparazio proba:**
   ```bash
   python3 rf_capture_comparator.py kap1.iq8 kap2.iq8
   ```

3. **Transmisioen proba (LABORATEGIAN):**
   ```bash
   hackrf_transfer -t nire_kaptura.iq8 -f 433920000 -s 2000000 -p 1 -a 1
   ```

4. **Praktika osoa jarraitu:**
   Ikus `07_PRAKTIKA_HACKRF_ERREPRODUKZIOA_EU.md`

---

## 📞 LAGUNTZA ETA ERREFERENTZIAK

- **Ofiziala dokumentuak:** https://github.com/greatscottgadgets/hackrf/wiki
- **Forua:** https://github.com/greatscottgadgets/hackrf/discussions
- **Issues:** https://github.com/greatscottgadgets/hackrf/issues
- **Komunitatea:** https://greatscottgadgets.com/

---

**Urratsa gulegoak amaitu? Praktikarentzat prest zaude! 🎉**
