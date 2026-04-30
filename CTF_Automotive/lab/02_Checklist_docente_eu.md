# Irakaslearen Checklist — Game Master CTF Automotive

[Gaztelaniazko bertsioa](02_Checklist_docente.md)

> Dokumentu hau **konfidentziala** da. Ez banatu parte-hartzaileei.

---

## A) Ingurune-prestaketa (30 minutu lehenago)

### Sistema
- [ ] Ubuntu 22.04 / Kali Linux abiarazia eta eguneratuta
- [ ] Kernel ≥ 5.15 baieztatuta: `uname -r`
- [ ] can-utils instalatuta: `candump --version`
- [ ] python-can instalatuta: `python3 -c "import can; print(can.__version__)"`

### vcan0 interfazea
- [ ] `sudo modprobe can vcan can_raw`
- [ ] `sudo ip link add dev vcan0 type vcan`
- [ ] `sudo ip link set up vcan0`
- [ ] Egiaztatu: `ip link show vcan0` → `UP` erakutsi behar du

### ICSim
- [ ] ICSim konpilatuta eta exekutagarria (`./icsim` errorik gabe)
- [ ] `./icsim vcan0` → aginte-panelaren leihoa ikusgai
- [ ] `./controls vcan0` → kontrolak erantzuten dute (geziek abiadura-adierazlea mugitzen dute)
- [ ] ICSim talde guztientzat ikusgarri den pantailan edo monitorean proiektatu

### Lab-eko scriptak (CANbus lab-etik heredatuta)
- [ ] `can_scanner.py` exekutagarria: `python3 ../CANbus_ICSim_Ciber/scripts/can_scanner.py --help`
- [ ] `replay_attack.py` exekutagarria
- [ ] `fuzz_can.py` exekutagarria
- [ ] `can_dos.py` exekutagarria

### Trafiko señueloa (derrigorrezkoa 1. Fase benetakoa izateko)
- [ ] `scripts/decoy_traffic.py` badago: `ls scripts/decoy_traffic.py`
- [ ] python-can instalatuta: `python3 -c "import can"`
- [ ] Terminal bereizi batean abiarazita **parte-hartzaileak iritsi baino lehen**:
  ```bash
  python3 scripts/decoy_traffic.py
  ```
- [ ] Scriptak abioan 6 señuelo ID erakusten dituela egiaztatu
- [ ] `candump vcan0`-rekin egiaztatu: `0x300`, `0x4AA`, `0x1F0`, `0x3C0`, `0x520`, `0x6B0` IDak agertzen direla

---

## B) Prestatu beharreko materialak (inprimatuta)

- [ ] `01_Enunciado_participantes_eu.md` — kopia bat talde bakoitzeko
- [ ] `03_Hoja_flags_equipo_eu.md` — kopia bat talde bakoitzeko (sinatu eta entregatzeko)
- [ ] `04_Respuestas_master_eu.md` — **irakaslearentzat soilik**, ez banatu
- [ ] Puntuazio-orri hutsa (D sekzioa ikusi)

---

## C) Faseka flag-en balioztapen gida

### 1. FASEA — Ezagutza

| Flaga | Erantzun zuzena | Nola balioztatu |
|---|---|---|
| FLAG-F1A | `0x244` | Parte-hartzaileak 0x244 aldatzen dela erakusten du azeleratzailea mugitzean |
| FLAG-F1B | `0x19B` | Parte-hartzaileak 0x19B aldatzen dela erakusten du ateak irekitzerakoan |
| FLAG-F1C | `0x01` | Parte-hartzaileak 0x188-ko byte 0 = 01 erakusten du ezkerreko txandakatzearekin |

> **Señuelo IDak aktibo** (`decoy_traffic.py`-k injektatuta) — parte-hartzaileak hauetako bat
> aurkezten badu, ez balioztatu; esan *"jarraitu bilatzen"*:
> `0x300`, `0x4AA`, `0x1F0`, `0x3C0`, `0x520`, `0x6B0`
>
> Metodo zuzena: `controls`-eko ekintza eta bus-eko aldaketa erlazionatzea.
> Azeleragailua mugitu → `0x244` soilik aldatzen da ekintza horren erritmoan.

**F1 iradokitako ahozko galdera:** *"Nola bereizi dituzu benetako IDak señueloenetatik? Zein tresnarekin erlazionatu duzu ekintza byte-aldaketarekin?"*

---

### 2. FASEA — Injekzioa

| Flaga | Balioztapen-irizpidea | Espero den ebidentzia |
|---|---|---|
| FLAG-F2A | ICSim-ek >200 km/h abiadura-adierazlea erakusten du | Argazkia + `cansend vcan0 244#00000000FF000000` edo baliokidea |
| FLAG-F2B | Bi txandakatzaile-adierazleak dardarka | Argazkia + `cansend vcan0 188#0300000000000000` |
| FLAG-F2C | ICSim-ek ateak irekita erakusten ditu (ikono berdeak) | Argazkia + `cansend vcan0 19B#0000000000000000` |
| FLAG-F2D | 30 s-z begizta aktibo duen terminala | `while true; do cansend ...; sleep 0.01; done` edo Python baliokidea |

**F2 iradokitako ahozko galdera:** *"Zer desberdintasun dago frame bat behin injektatu eta begizta mantentzearen artean? Zer gertatuko litzateke begizta geldiaraziz gero?"*

---

### 3. FASEA — Replay-a

| Flaga | Balioztapen-irizpidea | Espero den ebidentzia |
|---|---|---|
| FLAG-F3 | 3 eta 10 segundoren arteko edozein balio arrazoizkoa da | `.log` fitxategia + `replay_attack.py --id 19B` komandoa + argazkiak |

> **Oharra:** ez dago balio zuzena bakarra. ICSim-arekin balio tipikoa **5 segundo** da behin aktibatu bada.

**F3 iradokitako ahozko galdera:** *"Nola saihestu zezakeen fabrikatzaileak eraso hau? Nahikoa izango al litzateke CAN-a zifratzea?"*

---

### 4. FASEA — DoS / Fuzzing

| Flaga | Balioztapen-irizpidea | Onartutako tartea |
|---|---|---|
| FLAG-F4 | DoS bitarteko fps tasa | 500 eta 10.000 fps artean — `canbusload` >%80 frogatuta |

**F4 iradokitako ahozko galdera:** *"Zergatik da 0x000 IDa DoS-erako eraginkorrena CAN-en? Zein protokolo erabiltzen du CAN-ak arbitrazioan?"*

---

### BONUS — Defentsa

Onartu baldin eta:
- [ ] Python kodea terminalean errorik gabe funtzionatzen badu
- [ ] Parte-hartzaileak denbora errealean frame anomaloa detektatu/filtratzen duela frogatu dezakeen
- [ ] Parte-hartzaileak 2 esalditan bere kontraneurriak duen mugapena azaltzen badu

---

## D) Puntuazio-orria (CTF bitartean bete)

| Parte-hartzailea | F1A | F1B | F1C | F2A | F2B | F2C | F2D | F3 | F4 | Bonus | Flag denbora | TOTALA |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1. Parte-hartzailea | | | | | | | | | | | | |
| 2. Parte-hartzailea | | | | | | | | | | | | |
| 3. Parte-hartzailea | | | | | | | | | | | | |
| 4. Parte-hartzailea | | | | | | | | | | | | |

**Flag bakoitzeko puntuak:** F1 = 50/flag · F2 = 50/flag · F3 = 150 · F4 = 150 · Bonus = 100

**Abiadura bonuak:**
- F1 <15 min hasieratik: +50
- F2 <15 min F1-etik: +50
- F3 <15 min F2-tik: +50
- F4 <10 min F3-tik: +25

---

## E) CTF-aren itxiera

1. Emaitzak eta **irabazle parte-hartzailea** iragarri
2. 10-15 minutuko berrikuspena kolektiboa: GM-ak fase bakoitzeko komando zuzenak erakusten ditu
3. Eztabaida: *"Zein kontraesanerako neurrik saihestu zezakeen fase bakoitza?"*
4. Sinatu flag-orri guztiak bildu (partaidetza-ebidentzia)
5. ICSim itzali eta vcan0 ezabatu: `sudo ip link delete vcan0`
