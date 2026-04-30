# Linux / VM Ingurunearen Konfigurazioa — Urrats Aurreratua

[Gaztelaniazko bertsioa](03_Setup_entorno_linux.md)

## A aukera — Makina birtuala (Windows-erako gomendatua)

### A1. VirtualBox instalatu

1. VirtualBox deskargatu [https://www.virtualbox.org](https://www.virtualbox.org)-etik.
2. Windows-en instalatu aukera lehenetsiekin.
3. **Ubuntu 22.04 LTS**-ren ISO deskargatu [https://ubuntu.com/download/desktop](https://ubuntu.com/download/desktop)-etik.

### A2. VM sortu

| Parametroa | Gomendatutako balioa |
|---|---|
| Izena | `CANlab` |
| Mota | Linux / Ubuntu 64-bit |
| RAM | 4096 MB (gutxienez 2048 MB) |
| Diskoa | 30 GB dinamikoa |
| Prozesadoreak | 2 vCPU |
| Grafikoak | VBoxSVGA, 3D azelerazioa gaitu |
| Karpeta partekatua | Hostetik scriptak dauden direktorioa |

### A3. Ubuntu instalatu

1. ISO muntatu unitate optiko birtualean.
2. VM abiarazi → "Install Ubuntu" → gutxieneko instalazioa.
3. Erabiltzailea sortu (`canlab` / ikasgelako pasahitza).
4. Berrabiarazi eta instalazio-euskarria kendu.

### A4. Guest Additions instalatu

```bash
sudo apt update
sudo apt install -y build-essential dkms linux-headers-$(uname -r)
# VirtualBox menutik: Gailuak → Guest Additions irudia txertatu
sudo mount /dev/cdrom /mnt
sudo /mnt/VBoxLinuxAdditions.run
sudo reboot
```

---

## B aukera — Kali Linux (zentroak dagoeneko erabiltzen badu gomendatua)

1. Kali Linux VM irudia deskargatu [https://www.kali.org/get-kali/#kali-virtual-machines](https://www.kali.org/get-kali/#kali-virtual-machines)-etik.
2. VirtualBox edo VMware-n inportatu.
3. Lehenetsitako kredentzialak: `kali` / `kali`.
4. Kalik dagoeneko tresna asko ditu. Bakarrik `can-utils` eta `ICSim` instalatu behar dira.

---

## C aukera — Docker (aurreratua)

> Docker Desktop Windows-en + WSL2 backend-a, edo Linux host-ean Docker behar du.

```bash
# CAN laguntza duen pribilegiatutako edukiontzia sortu
docker run -it --privileged \
  --cap-add=NET_ADMIN \
  ubuntu:22.04 bash
```

Edukiontziaren barruan:
```bash
apt update && apt install -y can-utils python3 python3-pip
modprobe vcan  # Docker kernel batzuetan huts egin dezake
ip link add dev vcan0 type vcan
ip link set up vcan0
```

> **Muga:** ICSim-ek SDL2 eta pantaila grafiko bat behar du — X11 birbidalketa edo VNC eskatzen du. Ez gomendatua ikasgelarako Docker esperientziarik gabe.

---

## Ubuntu/Kali-n instalazio osoa

### 1. urratsa — Sistema menpekotasunak

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y \
    can-utils \
    libsdl2-dev \
    libsdl2-image-dev \
    meson ninja-build \
    python3 python3-pip python3-venv \
    git build-essential \
    wireshark  # aukerazkoa — azterketa grafikoa
```

### 2. urratsa — CAN kernel moduluak

```bash
sudo modprobe can
sudo modprobe vcan
sudo modprobe can_raw
```

Iraunkorra izateko:
```bash
echo -e "can\nvcan\ncan_raw" | sudo tee /etc/modules-load.d/can.conf
```

### 3. urratsa — CAN interfaze birtuala

```bash
sudo bash scripts/setup_vcan.sh
# edo eskuz:
sudo ip link add dev vcan0 type vcan
sudo ip link set up vcan0
```

Egiaztatu:
```bash
ip -details link show vcan0
```

### 4. urratsa — ICSim konpilatu

```bash
git clone https://github.com/zombieCraig/ICSim.git
cd ICSim
meson setup builddir
cd builddir
meson compile
cd ../..
```

Egiaztatu:
```bash
ls ICSim/builddir/icsim ICSim/builddir/controls
# Bi binariak egon behar dira
```

### 5. urratsa — Python ingurunea

```bash
cd CANbus_ICSim_Ciber
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 6. urratsa — Integrazioaren proba

```bash
# 1. terminala
./ICSim/builddir/icsim vcan0 &

# 2. terminala (ICSim abiarazi arteko 2 segundo itxaron)
./ICSim/builddir/controls vcan0 &

# 3. terminala
candump vcan0

# 4. terminala — proba-injekzioa
cansend vcan0 244#00000000FF000000
# Abiaduragailua igo behar da
```

---

## CAN-erako Wireshark konfiguratzea (aukerazkoa)

1. `sudo usermod -aG wireshark $USER` eta sesioa itxi/ireki.
2. Wireshark ireki → `vcan0` interfazea aukeratu.
3. Iragazki-kaptura: `can` edo hutsik utzi.
4. CAN frame-ak ID, DLC eta datuekin aztertzen dira.

---

## Gomendatutako snapshot-a (irakaslea)

Saioa baino lehen:
1. Dena instalatuta eta funtzionatzen duenean, VMren snapshot bat egin: `VirtualBox → Makina → Snapshot hartu → "lab-prest"`.
2. VM `.ova` gisa banatu ekipamenduak desberdinak badira.
3. Parte-hartzaileek `.ova` inportatu eta `setup_vcan.sh` exekutatu besterik ez dute egin behar.
