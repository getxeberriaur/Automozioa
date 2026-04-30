# C Praktika — Replay Erasoa

[Gaztelaniazko bertsioa](06_Practica_C_Replay.md)

**Estimatutako iraupena:** 40 minutu  
**Zailtasuna:** Ertaina  
**Tresnak:** `candump`, `canplayer`, `scripts/replay_attack.py`

---

## Helburua

CAN bus-ean egindako ekintza legitimo baten sekuentzia grabatu eta gero erreproduzitzea, tramen esanahia ulertu gabe efektu bera eragiteko. CAN bus-ean replay aurkako mekanismorik ez izateak kapturak berriro erabiltzeko aukera ematen duela frogatzea.

---

## Testuingurua

**Replay eraso** bat honetan datza:
1. Komunikazio legitimo bat kapturatzea (grabatuz).
2. Bus berean edo bateragarri batean erreproduzitzea.

CAN bus-ean, eraso hau hutsala da hauengatik:
- Ez dago protokoloan denbora-zigilurik.
- Ez dago sekuentzia-zenbakirik.
- Ez dago challenge-response mekanismorik.
- Ez dago mezu sinaturik.

**Dokumentatutako benetako kasuak:**
- Ate-desblokeatzeko sekuentziaren replay-a (parkingean grabatua).
- Motor abiarazi sekuentziaren replay-a inmobolizatzaile ongi inplementaturik gabeko ibilgailuetan.
- Infoentretenamenduko komandoen replay-a kontrol bus-era pribilegiorik igotzeko.

---

## Aurrebaldintzak

- `vcan0` aktibo.
- ICSim eta controls martxan.

---

## C.1 Ariketa — Ekintza-sekuentzia grabatu

### Urratsak

1. Terminal batean grabaketa hasi:
```bash
candump -l vcan0
# Fitxategia: candump-YYYYMMDD-HHMMSS.log gisa sortzen da
```

2. `controls`-en leihoan, ekintza hauek **hurrenez hurren** egin:
   - Maximora azeleratu (3 segundo mantendu).
   - Eskuineko txandakatzearen adierazlea aktibatu (2 segundo).
   - Ate guztiak desblokeatu.
   - Abiadura 0-ra frenatu.

3. Grabaketa gelditu:
```bash
Ctrl+C
```

4. Fitxategia berrizendatu errazago lan egiteko:
```bash
mv candump-*.log logs/sekuentzia_grabatua.log
```

5. Logaren lehen lerroak ikuskatu:
```bash
head -20 logs/sekuentzia_grabatua.log
```

---

## C.2 Ariketa — `canplayer`-ekin replay erreproduzitu

### Urratsak

1. `controls` gelditu (replay-arekin interferentziak saihesteko).

2. Grabaketa erreproduzitu:
```bash
canplayer -I logs/sekuentzia_grabatua.log
```

Aukera erabilgarriak:
```bash
# 3 aldiz erreproduzitu
canplayer -l 3 -I logs/sekuentzia_grabatua.log

# Bikoitz abiaduran erreproduzitu
canplayer -g 50 -I logs/sekuentzia_grabatua.log
```

3. ICSim-en behatu sekuentzia fidelki erreproduzitzen dela.

### Galderak

- Aginte-panelak jatorrizko ekintza eta replay-a bereiz ditzake?
- Zenbat aldiz erreproduzitu dezakezu replay-a efektu berarekin?
- Log hau benetako ibilgailu batena balitz eta modelo bereko beste batean erreproduzituko bazenu, zer gertatuko litzateke?

---

## C.3 Ariketa — Replay selektiboa (trama-azpimultzo bat soilik)

Sekuentzia osoa erreproduzitu beharrean, ID zehatz baten tramak soilik iragaztea.

```bash
# Logotik ate-tramak soilik erauzi (ID 0x19B)
grep "19B" logs/sekuentzia_grabatua.log > logs/ate_soilik.log

# Ate-irekiera soilik erreproduzitu
canplayer -I logs/ate_soilik.log
```

---

## C.4 Ariketa — Python-ekin replay-a (`replay_attack.py`)

`scripts/replay_attack.py` scriptak replay-aren gaineko kontrol gehiago eskaintzen du:
- ID-ren araberako iragazketa.
- Timing doikuntza.
- Loop aukera.
- Bidalitako tramen logging-a.

```bash
source .venv/bin/activate

# Replay osoa
python scripts/replay_attack.py \
    --file logs/sekuentzia_grabatua.log \
    --interface vcan0

# 0x19B ID-ren (ateak) replay-a soilik, 3 aldiz
python scripts/replay_attack.py \
    --file logs/sekuentzia_grabatua.log \
    --interface vcan0 \
    --filter-id 0x19B \
    --loops 3 \
    --speed 1.5
```

---

## C.5 Ariketa — Erronka: parkingeko ate-desblokeatzeko replay-a

**Simulatutako eszenatokia:**
> Erasotzaile batek biktima telefonoz (fabrikatzailearen app via Bluetooth → gateway → CAN bus) ibilgailua desblokeatzean behatzen du. OBD-II bidez konektatutako dongle batekin, desblokeoa baino lehen 5 segundoak grabatzen ditu. Geroago, kaptura hori erreproduzitzen du.

Eszenatokia simulatu:
1. `controls`-ekin ateak eskuz desblokeatu (app legitimoaren simulazioa).
2. `candump -l`-ekin kapturatu.
3. Ate guztiak berriz blokeatu.
4. Logaren kaptura erreproduzitu → ateak bakarren bakarrik desblokeatzen dira.

Txostenean erasoa dokumentatu:
- Replay baino lehen ICSim-en argazkia (ateak blokeatuta).
- Replay bitartean ICSim-en argazkia (ateak desblokeatuta).
- Efektua eragin duten log-lerroen kopurua.

---

## C Praktikaren entregagaiak

1. `logs/sekuentzia_grabatua.log` fitxategia (grabazioaren ebidentzia).
2. ICSim-en pantaila-argazkia replay baino lehen eta ostean.
3. C.2 ariketako galderen erantzunak.
4. C.5 ariketako ebidentzia (parkingeko eszenatokia).

---

## Ezagutzen diren kontraesanerako neurriak

| Kontraneurriak | Deskribapena | Muga |
|---|---|---|
| Aplikazio-geruzako denbora-zigiluak | ECU-ak mezua ez dela zaharo egiaztatu | Denbora sinkronizazio segurua behar du |
| Sekuentzia-zenbakiak (kontadoreak) | Mezu bakoitzak gero eta handiagoa den kontadore bat darama | Erasotzaileak kontadorea kapturatu eta manipula dezake |
| MAC-ak (Mezu Autentifikazio Kodeak) | HMAC-SHA256 sinadura CAN payload-ean | Erabilgarri diren datuen byte-ak murrizten ditu (8 byte gutxi da) |
| AUTOSAR SecOC | CAN mezu autentifikazioaren estandarra | AUTOSAR ECU-etan soilik, kostu altua |
| CAN FD + SecOC | Payload handiagoak (64 byte) MAC-ak errazten ditu | CAN FD hardware-a behar du |

---

## Azken gogoeta

- Zergatik da zaila CAN bus-ean replay babesaren inplementazioa?
- 8 byte-ko payload izango bazenu, zenbat byte eskainiko zenioke MAC-ari eta zenbat datuei?
- Zer informazio behar du hartzaileak MAC bat egiaztatzeko? Nola banatzen da gakoa?
