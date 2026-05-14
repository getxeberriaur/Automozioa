# CAN Bus Laborategiaren Konfigurazio Checklista (irakaslea)

[Gaztelaniazko bertsioa](02_Checklist_configuracion_laboratorio.md)

---

## Linux ala Windows? — Aukeratu zure bidea

> **ICSim-ek `vcan` behar du, Linux kernel-eko modulu bat.** Docker Desktop Windowsen Microsoft kernel bat erabiltzen du, modulu hau gabe — **ezin da Windows-en Docker Desktop-ekin zuzenean erabili.**

| Parte-hartzailearen egoera | Metodo gomendatua |
|---|---|
| **Linux natiboa** (Ubuntu, Kali, Debian…) | → [A aukera — Docker Linuxen](#a-aukera--docker-linuxen-gomendatua) |
| **Windows** | → [B aukera — VirtualBox VM + OVA](#b-aukera--virtualbox-vm--ova-windowserako) |
| Internetik gabe / VMrik gabe | → [C aukera — Instalazio natiboa Linuxen](#c-aukera--instalazio-natiboa-linuxen) |

---

## A aukera — Docker Linuxen (gomendatua)

Metodorik azkarrena eta erreproduzigarriena. Ez da ICSim konpilatu behar ez SDL2 instalatu.

### Eskakizunak
- [ ] `vcan` modulu eskuragarria duen Linux (`sudo modprobe vcan` ez da errorea).
- [ ] Docker instalatuta (`docker --version` erantzuten du).
- [ ] 4 GB RAM, 2 vCPU, 5 GB disko librea.

### Abiaraztea
```bash
# vcan modulua kargatu (saio bakoitzean behin)
sudo modprobe vcan

cd CANbus_ICSim_Ciber
docker build -t icsim:local .
docker run --name icsim_run --network host --cap-add NET_ADMIN -d icsim:local
```

### Egiaztapena
- [ ] `docker logs icsim_run` → "x11vnc is listening on :5901" erakusten du.
- [ ] `http://localhost:6080/vnc_lite.html` → abiaduragailua eta agintea erakusten ditu.
- [ ] `candump vcan0` hostetik → CAN tramak erakusten ditu.
- [ ] `while true; do cansend vcan0 244#00000000FF000000; sleep 0.01; done` → abiaduragailua igotzen da.

### Arazoen konponketa azkarra

| Arazoa | Ekintza |
|---|---|
| `modprobe vcan` huts egiten du | Kernelek ez du CAN laguntzen — B aukera erabili |
| Docker-en "permission denied" errorea | `sudo usermod -aG docker $USER` + saioa itxi/ireki |
| Edukiontzia jada existitzen da | `docker rm -f icsim_run` |
| 6080 ataka okupatuta | `docker run ... -p 6081:6080 ...` eta `:6081` ireki |
| `cansend` bakar batek ez du abiaduragailua mugitzen | Espero da — ICSim-ek bere tramak bidaltzen ditu etengabe. Begizta erabili: `while true; do cansend vcan0 244#00000000FF000000; sleep 0.01; done` |
| `SIOCGIFINDEX: No such device` logeetan | `vcan0` ez dago — hostean `sudo modprobe vcan` exekutatu eta edukiontzia berrabiarazi |

---

## B aukera — VirtualBox VM + OVA (Windowserako)

> **Docker Desktop Windowsen ez du `vcan` onartzen** (Microsoft WSL2 kernelek ez dute `CONFIG_CAN_VCAN`). Windows-erako irtenbide azkarrena aurrekonfiguratutako VM bat inportatzea da.

### Irakaslearen prestaketa (behin, ikastaroa baino lehen)

1. Linux makina batean, prestaketa-scripta exekutatu:
   ```bash
   cd CANbus_ICSim_Ciber
   sudo bash scripts/setup_ova_vm.sh
   ```
2. VMa itzali: `sudo shutdown now`
3. VirtualBoxen: **Fitxategia → Zerbitzu birtuala esportatu**
   - Formatua: `OVA 2.0`
   - Izen iradokia: `CANbus_ICSim_Lab.ova`
4. OVA banatu parte-hartzaileei (USB, tokiko zerbitzaria, Google Drive…)

### Windows-eko parte-hartzailearen konfigurazioa (5 minutu)

1. **VirtualBox** instalatu [https://www.virtualbox.org](https://www.virtualbox.org)-etik.
2. `CANbus_ICSim_Lab.ova`-n klik bikoitza → Inportatu.
3. VMa abiarazi → `canlab` erabiltzailea.
4. VMn terminal ireki eta exekutatu:
   ```bash
   bash ~/Escritorio/Iniciar_ICSim_Lab.sh
   ```
5. VMko arakatzailean ireki: `http://localhost:6080/vnc_lite.html`

### Egiaztapena (VMren barrutik)
- [ ] `ip link show vcan0` → `UP` egoera erakusten du.
- [ ] `http://localhost:6080/vnc_lite.html` → abiaduragailua eta agintea erakusten ditu.
- [ ] `candump vcan0` → tramak fluxuan erakusten ditu.

---

## C aukera — Instalazio natiboa Linuxen

> Erabili Docker eskuragarri ez badago.

---

## B) Sistema menpekotasunak

```bash
sudo apt update
sudo apt install -y \
    can-utils \
    libsdl2-dev \
    libsdl2-image-dev \
    python3 python3-pip python3-venv \
    git build-essential
```

Egiaztatu:
- [ ] `candump --version` erantzuten du.
- [ ] `cansend --version` erantzuten du.
- [ ] `python3 --version` ≥ 3.10.

---

## C) ICSim konpilatu

```bash
git clone https://github.com/zombieCraig/ICSim.git
cd ICSim
sudo apt install -y meson ninja-build
meson setup builddir
cd builddir
meson compile
```

- [ ] `icsim` binarioa `builddir/`-en sortuta.
- [ ] `controls` binarioa `builddir/`-en sortuta.

> Makefile alternatiboa: `make` ICSim direktorio erroan (meson-ek huts egiten badu).

---

## D) Python ingurunea

```bash
cd CANbus_ICSim_Ciber
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

- [ ] `python -c "import can; print(can.__version__)"` ≥ 4.0 bertsioa erakusten du.

---

## E) CAN interfaze birtuala

```bash
sudo bash scripts/setup_vcan.sh
ip link show vcan0
```

- [ ] `vcan0` `UP` egoerarekin agertzen da.
- [ ] `candump vcan0` errorik gabe abiarazten da (isilik tramak itxaron dezake).

---

## F) Ingurunearen egiaztapen osoa

3 terminal irekita aldi berean:

**1. terminala — ICSim:**
```bash
./ICSim/builddir/icsim vcan0
```
- [ ] Leiho grafikoa abiaduragailua eta txandakatzaileekin agertzen da.

**2. terminala — Controls:**
```bash
./ICSim/builddir/controls vcan0
```
- [ ] Teklatuz azeleratu/frenatu daiteke eta abiaduragailua erantzuten du.

**3. terminala — Candump:**
```bash
candump vcan0
```
- [ ] `0x244`, `0x188`, `0x19B` IDak dituzten tramak ikusten dira.

---

## G) «Laborategia prest» irizpidea

- ICSim-en abiaduragailua `cansend vcan0 244#00000000FF000000`-ri erantzuten dio.
- `candump`-ek ICSim aktibo dagoen bitartean ≥ 3 ID desberdin kapturatzen ditu.
- Python scriptak `can` errorik gabe inportatzen du.
- Taldeak ICSim + `candump` pantaila-argazkiak entregatzen ditu.

---

## H) Modu aurreratua — Hardware erreala (aukerazkoa)

Zentroak USB-CAN hardware bat badu (adib. BatchDrake proiektuko usbcan/BluePill+ dongle-a):

1. USB dongle-a konektatu.
2. `usbcanbr /dev/ttyACM0 vcan0` exekutatu (usbcan erabiltzen bada).
3. Edo `slcan` konfiguratu: `slcand -o -s6 /dev/ttyUSB0 slcan0 && ip link set slcan0 up`.
4. `vcan0` `slcan0`-rekin edo dagokion interfazearekin ordezkatu komando guztietan.

> Ikus [https://github.com/BatchDrake/usbcan](https://github.com/BatchDrake/usbcan) BluePill+-ren wiring eta Arduino kodeagorako.

---

## I) Kontingentziarako plana

| Arazoa | Ekintza |
|---|---|
| ICSim ez da konpilatzen | Docker irudia erabili (`docker build -t icsim:local .`) |
| SDL2 ez dago VMn | VMren ezarpenetan grafika-azelerazioa aktibatu, edo Docker erabili |
| `vcan0` berrabiaraztean desagertzen da | `setup_ova_vm.sh` scriptak `vcan0.service` systemd zerbitzua sortzen du automatikoki |
| Paketeak internetik gabe | `can-utils`, `libsdl2-dev`, `libsdl2-image-dev`-en `.deb` USBn prestatu |
| Windows VirtualBoxik gabe | Kali Linux live USB persistence-ekin erabili |
| Docker Desktop Windowsen ez du ICSim erakusten | Espero da — B aukera erabili (OVA) |
