# RUN ME FIRST — CAN Bus Laborategiaren Abiarazte Azkarra

[Gaztelaniazko bertsioa](RUN_ME_FIRST.md)

> Estimatutako denbora: **10 minutu** (Linux VM prest dagoenean eta can-utils + ICSim konpilatuta daudenean).

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

## 2. urratsa — ICSim abiarazi (aginte-panela)

1. terminala ireki:
```bash
./ICSim/builddir/icsim vcan0
```
Abiaduragailua, txandakatzaileak eta ateen egoera dituen leiho grafiko bat agertuko da.

---

## 3. urratsa — Kontrol-agintea abiarazi

2. terminala ireki:
```bash
./ICSim/builddir/controls vcan0
```
Teklatua edo gamepad-a erabili interakziorako. Lehenetsitako teklak:
- `W/S` — azeleratu / frenatu (abiadura)
- `Q/E` — ezkerreko / eskuineko txandakatzearen adierazlea
- `1/2/3/4` — ateak blokeatu/desblokeatu

---

## 4. urratsa — Bus-eko trafikoa egiaztatu

3. terminala ireki:
```bash
candump vcan0
```
Tramak fluxuan ikusten dituzula egiaztatu behar duzu. Irteera adibidea:
```
vcan0  244   [8]  00 00 00 00 00 00 00 00
vcan0  188   [8]  00 00 00 00 00 00 00 00
vcan0  19B   [8]  0F 00 00 00 00 00 00 00
```

---

## 5. urratsa — Lehen proba-injekzioa exekutatu

4. terminala ireki:
```bash
# Abiaduragailua maximora igo aginte-panelean
cansend vcan0 244#00000000FF000000
```
ICSim-en abiaduragailua igotzen ikusi.

---

## Dena funtzionatzen al du?

`cansend`-ari abiaduragailua erantzuten badio, ingurunea prest dago. Jarraitu honela:

→ **[A Praktika — Ezagutza](lab/04_Practica_A_Reconocimiento_eu.md)**

---

## Arazoen konponketa azkarra

| Sintoma | Konponbidea |
|---|---|
| `vcan0` ez da agertzen | `sudo modprobe vcan` eta setup_vcan.sh berriz exekutatu |
| ICSim-ek ez du leihoa irekitzen | `libsdl2-dev libsdl2-image-dev` instalatu |
| `candump`-ek ez du ezer erakusten | ICSim eta controls martxan daudela egiaztatu |
| `cansend`-ek socket errorea ematen du | `vcan0` UP egoera duela egiaztatu: `ip link set vcan0 up` |
| `python-can`-ek ez du inportatzen | venv aktibatu: `source .venv/bin/activate` |
