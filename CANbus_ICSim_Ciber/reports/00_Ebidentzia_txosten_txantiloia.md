# Ebidentzia-txosten txantiloia — CAN Bus Laborategia (taldea)

[Gaztelaniazko bertsioa](00_Plantilla_informe_evidencias.md)

## 1) Taldearen datuak

- Zentroa:
- Ikasturtea / taldea:
- Talde zk.:
- Kideak:
- Data:
- Irakaslea:

---

## 2) Praktikaren helburua

Laborategian zer balioztatu den deskribatu 3-5 lerrotan (CAN trafiko azterketa, injekzio erasoak, replay-a eta fuzzing-a ICSim-en gainean).

---

## 3) Erabilitako ingurunea

- Sistema eragilea:
- Linux kernel bertsioa:
- can-utils bertsioa (`candump --version`):
- python-can bertsioa (`python -c "import can; print(can.__version__)"`):
- ICSim konpilatuta eta operatibo: Bai / Ez
- `vcan0` interfazea operatibo (`ip link show vcan0`): Bai / Ez

---

## 4) A Praktika — Ezagutza

### 4.1 Identifikatutako IDen taula

| CAN ID | Maiztasuna (Hz) | DLC | Inferitutako funtzioa |
|---|---|---|---|
| | | | |
| | | | |
| | | | |

### 4.2 Ekintza → bus erlaziotze-taula

| Ekintza controls-en | CAN ID | Bytea | Aurretiazko balioa | Osteko balioa |
|---|---|---|---|---|
| Maximora azeleratu | | | | |
| Frenatu | | | | |
| Ezkerreko txandakatzearen adierazlea | | | | |
| Eskuineko txandakatzearen adierazlea | | | | |
| 1. atea desblokeatu | | | | |

### 4.3 Pantaila-argazkia

> [Byte aldakorrak erakusten dituen `cansniffer`-en argazkia erantsi]

### 4.4 Behaketak

---

## 5) B Praktika — Frame injekzioa

### 5.1 Exekutatutako kasuak

| Injektatutako ekintza | `cansend` komandoa | ICSim-en behatutako emaitza | OK? |
|---|---|---|---|
| Abiaduragailua maximoan | `cansend vcan0 244#00000000FF000000` | | |
| Ezkerreko txandakatzearen adierazlea | `cansend vcan0 188#0100000000000000` | | |
| Larrialdiko argiak | `cansend vcan0 188#0300000000000000` | | |
| Ate guztiak desblokeatu | `cansend vcan0 19B#0000000000000000` | | |
| Ekintza konposatua (B.4 erronka) | (scripta erantsirik) | | |

### 5.2 Ebidentziak

> [ICSim-en pantaila-argazkia injekzioak eragindako abiaduragailua maximoan]

> [ICSim-en pantaila-argazkia injekzioak eragindako txandakatzaileak aktibo]

### 5.3 Nodo gatazkaren emaitza (B.5)

- Injekzioak edo controls legitimoak irabazten du? Zergatik?

---

## 6) C Praktika — Replay Erasoa

### 6.1 Grabatutako sekuentzia

- Grabaketaren iraupena:
- Kapturatutako trama kopurua:
- Logean dauden IDak:

### 6.2 Replay-aren emaitza

| Saiakera | ICSim-ek sekuentzia erreproduzitu al du? | Behaketak |
|---|---|---|
| Replay osoa | | |
| Ate-replay soilik | | |
| Replay 3 aldiz begiztan | | |

### 6.3 Ebidentziak

> [Replay baino lehen argazkia — ateak blokeatuta]

> [Replay bitartean argazkia — ateak desblokeatuta]

### 6.4 Parkingeko eszenatokia (C.5)

- Exekutatutako erasoaren deskribapena:
- Desblokeatze eragin duten trama kopurua:

---

## 7) D Praktika — Fuzzing eta DoS

### 7.1 Fuzzing-a

| Fuzzing modua | Iraupena | Bidalitako tramak | Behatutako portaera anomaloak |
|---|---|---|---|
| random | | | |
| targeted (0x244) | | | |
| mutate | | | |

### 7.2 Zerbitzu-Ukapena

| Metrika | Baldintza normala | DoS bitartean |
|---|---|---|
| Bus-karga (%) | | |
| Controls-en erantzuna | Bai | |
| Abiaduragailua eguneragarria | Bai | |

### 7.3 Ebidentziak

> [Flooding bitarteko `canbusload`-en kaptura]

> [DoS bitartean izoztutako ICSim-en kaptura]

---

## 8) Azterketa teknikoa

### 8.1 Identifikatutako ahuleziak

| Ahultasuna | Frogatzen den praktika | Balizko inpaktua (benetakoa) |
|---|---|---|
| Jatorriaren autentifikaziorik gabe | A, B | Komandoen injekzioa |
| Replay-rik gabe | C | Desblokeoaren replay-a |
| Fluxu-kontrolik gabe | D (DoS) | Bus-aren saturazioa |
| Broadcast osoa | A | Entzuketa pasiboa detektaezina |

### 8.2 Zein eraso da arriskutsuena benetako ibilgailu batean? Justifikazioa

### 8.3 Proposatutako kontraesanerako neurriak

| Erasoa | Kontraneurriak | Bideragarritasuna (altua/ertaina/baxua) |
|---|---|---|
| Injekzioa | | |
| Replay-a | | |
| DoS-a | | |

---

## 9) Ondorioak

- Ondorio nagusia (1-2 esaldi):
- Ikaskuntza tekniko garrantzitsuena:
- Laborategiarentzat proposatuko zenukeen hobekuntza:

---

## 10) Erantsitako fitxategiak

- [ ] `logs/sekuentzia_grabatua.log` (C Praktika)
- [ ] `logs/scan_emaitza.txt` (A Praktika)
- [ ] `logs/fuzz_saioa.log` (D Praktika)
- [ ] Ekintza konposatuen scripta (B Praktika, B.4 erronka)
- [ ] Pantaila-argazkiak (gutxienez 5)
