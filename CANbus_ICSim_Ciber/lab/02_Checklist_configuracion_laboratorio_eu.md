# CAN Bus Laborategiaren Konfigurazio Checklista (irakaslea)

[Gaztelaniazko bertsioa](02_Checklist_configuracion_laboratorio.md)

## A) Sistemaren eskakizunak (pustu bakoitzeko)

- [ ] Ubuntu 22.04 LTS edo Kali Linux 2024+ (fisikoa edo VM ≥4 GB RAM, ≥2 vCPU).
- [ ] `sudo` sarbidea.
- [ ] Menpekotasunak instalatzeko interneteko konexioa (edo USB offline paketeak).
- [ ] OpenGL laguntza duen txartel grafikoa (SDL2 / ICSim leihorako).
- [ ] Python 3.10+.

> **Windows:** Ez du SocketCAN onartzen. Erabili VM VirtualBox/VMware edo kernel pertsonalizatua duen WSL2 (konplexua — ikasgelarako ez gomendatua).

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
| ICSim ez da konpilatzen | Aurrekonpilatutako Docker irudia edo snapshot duen VM erabili |
| SDL2 ez dago VMn | VMren ezarpenetan grafika-azelerazioa aktibatu |
| `vcan0` berrabiaraztean desagertzen da | `setup_vcan.sh` `/etc/rc.local`-era edo systemd-era gehitu |
| Paketeak internetik gabe | `can-utils`, `libsdl2-dev`, `libsdl2-image-dev`-en `.deb` USBn prestatu |
| Ekipamendurik gabe VM | Kali Linux live USB persistence-ekin erabili |
