# RUN ME FIRST — CAN Bus Laborategiaren Abiarazte Azkarra

[Gaztelaniazko bertsioa](RUN_ME_FIRST.md)

> Estimatutako denbora: **5 minutu** Docker-ekin Linuxen / **15 minutu** Windowsen VM batetik.

---

## Linux ala Windows?

> **ICSim-ek `vcan` behar du, Linux kernel-eko modulu bat.**
> Docker Desktop Windowsen Microsoft kernel bat erabiltzen du, modulu hau gabe — **Windowsen zuzenean ez du funtzionatzen.**

| Sistema | Metodoa |
|---|---|
| **Linux natiboa** (Ubuntu, Kali…) | Jarraitu beheko urratsak |
| **Windows** | Lehenik [konfiguratu Linux VM bat](lab/02_Checklist_configuracion_laboratorio_eu.md#b-aukera--virtualbox-vm--ova-windowserako), gero jarraitu urrats hauek VMren barrutik |

---

## 1. urratsa — CAN interfaze birtuala abiarazi

```bash
sudo bash scripts/setup_vcan.sh
```

Egiaztatu:
```bash
ip link show vcan0
# Erakutsi behar du: vcan0: <NOARP,UP,LOWER_UP> ...
```

---

## 2. urratsa — Docker irudia eraiki

```bash
cd CANbus_ICSim_Ciber
docker build -t icsim:local .
```

> Lehen aldiz soilik beharrezkoa da, edo `Dockerfile` aldatzen denean.

---

## 3. urratsa — Edukiontzia abiarazi

```bash
docker run --name icsim_run --network host --cap-add NET_ADMIN -d icsim:local
```

> `--network host` beharrezkoa da Linuxen, edukiontziak host-eko `vcan0` ikus dezan.

Edukiontziak automatikoki abiarazten ditu:
- ICSim (abiaduragailua) eta controls (agintea)
- VNC + noVNC zerbitzaria `6080` atakan

---

## 4. urratsa — Interfaze grafikoa ireki

Arakatzailean ireki:
```
http://localhost:6080/vnc_lite.html
```

Bi leiho ikusiko dituzu:
- **Abiaduragailua** (icsim) — goian
- **Kontrol-agintea** (controls) — behean

Interakzionatu aginte-panelarekin teklatua erabiliz (geziak = azeleratu/frenatu, Q/E = txandakatzaileak).

---

## 5. urratsa — Bus-eko trafikoa egiaztatu

Hostetik terminalean (ez edukiontziaren barruan):

```bash
candump vcan0
```

Tramak fluxuan ikusi behar dituzu:
```
vcan0  244   [8]  00 00 00 00 1A 00 00 00
vcan0  188   [8]  00 00 00 00 00 00 00 00
vcan0  19B   [8]  0F 00 00 00 00 00 00 00
```

---

## 6. urratsa — Lehen proba-injekzioa

```bash
# Frame bakarra (efektua aldi batekoa da)
cansend vcan0 244#00000000FF000000

# Etengabeko efekturako (begizta jarraitua)
while true; do cansend vcan0 244#00000000FF000000; sleep 0.01; done
```

ICSim-en abiaduragailua igotzen ikusi arakatzailean.

> **Oharra:** ICSim-ek etengabe bere tramak sortzen ditu. `cansend` bakar batek haiekin lehiatzen du eta agian ez da nabarituko. Begiztak injekzioak bus-a menderatzen duela bermatzen du.

---

## Dena funtzionatzen al du?

`cansend` begiztari abiaduragailua erantzuten badio, ingurunea prest dago. Jarraitu honela:

→ **[A Praktika — Ezagutza](lab/04_Practica_A_Reconocimiento_eu.md)**

---

## Edukiontziaren komando erabilgarriak

```bash
# Edukiontziaren logak ikusi
docker logs -f icsim_run

# Shell ireki edukiontziaren barruan
docker exec -it icsim_run bash

# Edukiontzia gelditu
docker stop icsim_run

# Edukiontzia ezabatu (berrabiarazteko)
docker rm -f icsim_run
```

---

## Arazoen konponketa azkarra

| Sintoma | Konponbidea |
|---|---|
| `vcan0` ez da agertzen | `sudo modprobe vcan` eta `setup_vcan.sh` berriz exekutatu |
| Edukiontziak berehala irteten du | `docker logs icsim_run` — entrypoint erroreak bilatu |
| `candump`-ek ez du ezer erakusten | ICSim martxan dagoela egiaztatu: `docker logs icsim_run` |
| `cansend`-ek ez du abiaduragailua mugitzen | Begizta erabili: `while true; do cansend vcan0 244#00000000FF000000; sleep 0.01; done` |
| `cansend`-ek socket errorea ematen du | `vcan0` UP dagoela egiaztatu: `ip link show vcan0` |
| Windowsen Docker-ek ez du funtzionatzen | Docker Desktop-ek ez du `vcan` onartzen — Linux VM erabili (ikus checklist) |
| `python-can`-ek ez du inportatzen | venv aktibatu: `source .venv/bin/activate` |
