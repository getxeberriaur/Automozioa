# RUN ME FIRST — CTF Automotive abiaraztea (Game Master)

[Gaztelaniazko bertsioa](RUN_ME_FIRST.md)

> Prestaketa denbora: **30 minutu** parte-hartzaileak iritsi baino lehen.

---

## 1. urratsa — Oinarrizko ingurunea egiaztatu

```bash
# 1.1 vcan0 aktibo dagoela egiaztatu
ip link show vcan0
# Erakutsi behar du: vcan0: ... UP ...

# Aktibo ez badago:
sudo bash ../CANbus_ICSim_Ciber/scripts/setup_vcan.sh

# 1.2 can-utils egiaztatu
candump --version
cansend --version

# 1.3 python-can egiaztatu
python3 -c "import can; print('python-can', can.__version__)"

# 1.4 Scriptak egiaztatu
ls ../CANbus_ICSim_Ciber/scripts/
# Ikusi behar da: can_scanner.py, replay_attack.py, fuzz_can.py, can_dos.py
```

---

## 2. urratsa — ICSim abiarazi

```bash
# 1. terminala — pantaila bisuala
cd /ICSim/karpeta
./icsim vcan0

# 2. terminala — kontrolak (CTF osoan irekita mantendu)
./controls vcan0
```

> Aginte-panelaren leihoa ikusgai egon behar da talde guztientzat (proiektatu arbelean).

---

## 3. urratsa — Seinale-trafiko gezurrezkoa abiarazi

> **Derrigorrezko urratsa** CTFeko 1. Fasea benetako ezagutza-lan bat izan dadin.
> Urrats hau egiten ez bada, ICSim-en IDak berehala ageri dira eta parte-hartzaileek
> F1 flagak komandorik exekutatu gabe bete ditzakete.

```bash
# 3. terminala — señuelo injektatzailea (CTF osoan aktibo mantendu)
python3 scripts/decoy_traffic.py
```

Scriptak 6 ID gezurrezko gehigarri injektatzen ditu `vcan0`-n:

| ID señuelo | Deskripzio faltsua | Portaera |
|---|---|---|
| `0x300` | "Motor RPM" | ~50ms-an behin aldatzen da, kurba senoidal motela |
| `0x4AA` | "Motor tenperatura" | 2 s-an behin aldatzen da, pixkanaka igotzen/jaisten |
| `0x1F0` | "Pneumatiko presioa" | 4 s-an behin aldatzen da, 4 byte |
| `0x3C0` | "12V bateria" | Ia estatikoa, 10 s-an behin aldatzen |
| `0x520` | "Euri/argi sentsorea" | Ausazko pultsu irregularrak |
| `0x6B0` | "ECU timestamp" | Etengabeko kontagailu inkrementala |

**Funtsezko ideia:** señueloek beren erritmoa dute, ez dute simulagailuaren
ekintzei erantzuten. "Azeleragailua mugitu → zer ID aldatzen da?" koerlazioaren
bidezko metodoa oraindik zuzena da.

### Maila oinarrizkoa — laguntza taula eman

Taldeak zailtasunak baditu, taula hau eman **soilik** F1 denbora gainditzen bada:

| CAN ID | Gutxi gorabeherako funtzioa |
|---|---|
| 0x244 | Ibilgailuaren dinamikarekin lotua |
| 0x188 | Seinaleekin lotua |
| 0x19B | Ibilgailurako sarbidearekin lotua |

### Aditu maila — zarata gehigarria

```bash
# Señueloaren gainean: erabat ausazko frameak gehitu
cangen vcan0 -I r -L 8 -D r -g 30 &
```

---

## 4. urratsa — Banatu materialak

- [ ] `lab/01_Enunciado_participantes_eu.md` kopia bat parte-hartzaile bakoitzeko
- [ ] `lab/03_Hoja_flags_equipo_eu.md` kopia bat parte-hartzaile bakoitzeko (inprimatuta)
- [ ] Linux terminalerako sarbidea tresnakinsart

**Zuk gorde (ez partekatu):**
- [ ] `lab/04_Respuestas_master_eu.md` — erantzunak + puntuazioa

---

## 5. urratsa — CTF abiarazi

```
[GM-k ozen esan]
"Eszenatokia orain hasten da. 90 minutu dituzte.
Tresnei buruzko zalantzak teknikoak baleude, nik erantzungo dut.
Zer erasotu eta nola egin galderak erronkaren parte dira.
Zorte on!"
```

Hasiera ordua: `___:___`  
Amaiera ordua: hasiera + 90 min = `___:___`

---

## 6. urratsa — CTF bitartean (GM rola)

- Flagak baliozkotzea **parte-hartzaile** batek aurkezten duenean (`04_Respuestas_master_eu.md` ikusi)
- Balioztatutako flag bakoitzaren ordua erregistratu abiadura-bonus kalkulatzeko
- **Onartutako pistak** (erantzunak eman gabe):
  - F1: *"Zein tresnak erakusten ditu aldatzen diren byteak soilik?"*
  - F2: *"Zenbat byte ditu 0x244 frame batek? Zein da azeleratzailearekin aldatzen dena?"*
  - F3: *"Egiaztatu replay_attack.py-ren `--id` aukera"*
  - F4: *"Zein IDk du lehentasun handiena CAN-en?"*

---

## Arazo arrunten konponbidea

| Arazoa | Konponbidea |
|---|---|
| `vcan0` ez da agertzen | `sudo modprobe vcan; sudo ip link add dev vcan0 type vcan; sudo ip link set up vcan0` |
| ICSim ez da abiarazten | SDL2 dependentziak egiaztatu: `sudo apt install libsdl2-dev libsdl2-image-dev` |
| ICSim-ek ez du injekziorik onartzen | `vcan0`-n entzuten ari dela egiaztatu, ez `can0`-n |
| Parte-hartzaileak F1-en blokeatuta >15 min | `cansniffer` pista eman edo ID taula eman (oinarrizko mailan soilik) |
