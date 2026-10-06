# D Praktika — Fuzzing eta Zerbitzu-Ukapena (DoS)

[Gaztelaniazko bertsioa](07_Practica_D_Fuzzing_DoS.md)

**Estimatutako iraupena:** 45 minutu  
**Zailtasuna:** Ertaina-Aurreratua  
**Tresnak:** `cangen`, `scripts/fuzz_can.py`, `scripts/can_dos.py`

---

## Helburua

Fuzzing-ak eta bus-aren saturazioak nola eragin diezazkiokeen portaera ustekabeko edo nodo legitimoei zerbitzu-ukapena ulertzea. Benetako ingurunean, teknika hauek bide-segurtasunarekin lotutako sistema kritikoei eragin diezaiekete.

---

## Testuingurua

### Zer da CAN-eko fuzzing-a?

**Fuzzing**-ak eduki aleatorioa edo erdi-zuzendutako tramak bidaltzean datza, ondorengoak aurkitzeko:
- Ibilgailuaren funtzioak eragiten dituzten ID ezezagunak.
- ECU-etan errore-egoerak eragiten dituzten datu-balioak.
- Diagnostiko-mezu prozesatzeko ahuleziak (UDS, OBD).

### Zer da CAN-eko DoS-a?

CAN bus-ak lehentasunean oinarritutako **talka-arbitrajea** erabiltzen du: ID baxuenak (dominanteak) bus-a irabazten du. Erasotzaile batek:
1. ID=0x000 (lehentasun maximoa) tramak etengabe bidali ditzake.
2. Bus-aren arbitroak beti lehentasun honi uzten dio.
3. ECU legitimoek (ID > 0x000) ezin dute inoiz transmititu.
4. Bus-a **saturatuta** geratzen da → kontrol-funtzio guztiek komunikazioa galtzen dute.

> **Benetako ibilgailu batean:** honek balaztak, norabide-laguntzailea, airbag-ak desaktibatu ditzake. **Potentziala oso arriskutsua** da benetako ingurunean.

---

## Aurrebaldintzak

- `vcan0` aktibo.
- ICSim martxan.
- `controls` gelditu (efektuak argiago ikusteko).

---

## D.1 Ariketa — `cangen`-ekin oinarrizko fuzzing-a

`cangen`-ek CAN trafiko aleatorio sortzen du.

```bash
# ID guztien fuzzing-a datu aleatorioetarekin — 100 trama/segundo
cangen -g 10 -I r -L r vcan0

# Parametroak:
# -g 10    → trama arteko 10 ms-ko tartea (~100 Hz)
# -I r     → ID aleatoriak (r = random)
# -L r     → DLC aleatorio (0-8 byte)
```

30 segundo exekutatu eta ICSim behatu. Portaera ustekabe bat agertzen bada apuntatu.

### Erdi-zuzendutako fuzzing-a (ID ezagunak soilik)

```bash
# 0x100-0x300 ID tarteko fuzzing-a soilik, datu aleatorioetarekin
cangen -g 5 -I 0x100 -n 1000 vcan0
```

---

## D.2 Ariketa — `fuzz_can.py`-rekin bideratutako fuzzing-a

`scripts/fuzz_can.py` scriptak estrategia adimentsuagoak inplementatzen ditu:
- **Ausazko purua:** ID eta datu guztiz aleatoriak.
- **ID-ren arabera:** datu-fuzzing ID zehatz batean.
- **Mutazioa:** trama ezaguna abiapuntu gisa hartu eta byteak banan-banan mutatu.

```bash
source .venv/bin/activate

# Fuzzing aleatorio 60 segundoz
python scripts/fuzz_can.py \
    --interface vcan0 \
    --mode random \
    --duration 60 \
    --rate 50 \
    --log logs/fuzz_saioa.log

# Bideratutako fuzzing abiadura IDra (0x244), byte-z byte mutatuz
python scripts/fuzz_can.py \
    --interface vcan0 \
    --mode mutate \
    --target-id 0x244 \
    --base-data 0000000000000000 \
    --duration 30
```

### Zer behatu?

- Abiaduragailua era anormalean aldatzen al da?
- ICSim izoztu edo berrabiarazi egiten al da?
- Tarteko erregistrotik kanpoko irakurketak agertzen al dira?

Logean edozein portaera ustekabe apuntatu hori eragin zuen tramaren balio zehatzekin.

---

## D.3 Ariketa — Zerbitzu-Ukapena (bus flooding)

### 1. urratsa — Bus-karga neurtu baldintza normaletan

ICSim eta controls martxan daudenean:
```bash
canbusload vcan0@500000 -b -c -t
```

Bus-aren karga ehunekoa apuntatu. Espero den adibidea: `~15-20%`.

### 2. urratsa — DoS erasoa abiarazi

```bash
# Bigarren terminal batean, flooding-a exekutatu
python scripts/can_dos.py \
    --interface vcan0 \
    --priority-id 0x000 \
    --rate 10000 \
    --duration 30
```

Edo `cangen`-ekin:
```bash
# Lehentasun maximoko ID-rekin flooding masiboa
cangen -g 0 -I 0 vcan0
```

### 3. urratsa — Eraso bitartean bus-karga neurtu

Hirugarren terminal batean:
```bash
canbusload vcan0@500000 -b -c -t
```

### 4. urratsa — ICSim-en efektua behatu

Flooding aktibo dena bitartean:
- Abiaduragailua kontrolei erantzuten jarraitzen al du?
- Aginte-paneleko datuak izoztu egiten al dira?

### Galderak

- Zein bus-karga lortzen da DoS bitartean?
- Zein ehunekoan uzten dio bus-ak kontrol legitimoei erantzuteari?
- Zergatik dute ID=0x000 tramen lehentasun maximoa?

---

## D.4 Ariketa — DoS selektiboa (nodo zehatz bat isilarazi)

Bus osoa saturatu beharrean, erasotzaile sofistikatu batek **Error Frame**-ak bidaliz nodo zehatz bat isilarazi dezake edo ECU biktimak **Bus-Off moduan** sarraraziko dituzten datu okerrak dituzten ID bereko tramak.

> **Oharra:** Teknika hau (ECU silencing) `vcan0`-n frogatzea konplexua da (driver birtualak errore-kontadoreak hardware errealak bezala modelizatzen ez dituelako). Kontzeptu teoriko gisa barne hartzen da.

**Kontzeptua:**
1. CAN-ek nodo bakoitzeko errore-kontadorea du (TEC/REC).
2. ECU batek transmisio-errore nahikoa pilatzen baditu, **Bus-Off** egoeran sartzen da: transmititu gabe geratzen da.
3. Erasotzaile batek ACK errore-ak eragin ditzake biktima nodoan.
4. Biktima nodoa bus-etik "desagertu" egiten da inork jakin gabe.

---

## D.5 Ariketa — Erronka: eraso konbinatua

Hiru fasetan ICSim-ekin eraso bat diseinatu eta exekutatu:

**1. fasea (Ezagutza):** 10 segundoko trafiko normala kapturatu.
```bash
candump -l vcan0  # logs/eraso_aurretik.log gisa gorde
```

**2. fasea (Injekzioa + DoS aldi berean):**
- A terminala: ID=0x000-ren flooding-a.
- B terminala: abiadura maximoaren injekzioa ID=0x244-n.

**3. fasea (Azterketa):** Eraso bitartean trafikoa kapturatu.
```bash
candump -l vcan0  # logs/eraso_bitartean.log gisa gorde
```

Bi logak konparatu:
```bash
# Eraso aurreko logean ID-ren arabera tramak zenbatu
awk '{print $3}' logs/eraso_aurretik.log | sort | uniq -c | sort -rn

# Eraso bitartean logean ID-ren arabera tramak zenbatu
awk '{print $3}' logs/eraso_bitartean.log | sort | uniq -c | sort -rn
```

---

## D Praktikaren entregagaiak

1. Fuzzing saioaren loga (`logs/fuzz_saioa.log`).
2. Bus-karga DoS baino lehen eta bitartean.
3. Flooding bitarteko ICSim-en pantaila-argazkiak.
4. Logen konparaketa (D.5 ariketa) 3-5 lerroko azterketa.
5. Ariketen galderen erantzunak.

---

## Ezagutzen diren kontraesanerako neurriak

| Erasoa | Kontraneurriak |
|---|---|
| ID-ren fuzzing-a | Gateway-etan ID iragazketa (ID baliodun zurien zerrenda) |
| Datu-fuzzing-a | Tarteko balioztatze aplikazio-geruzako ECU-an |
| Bus flooding | Konfiguratutako lehentasun mugatua duen hardware-a; VCID duen CAN XL |
| ECU isilaraztea | Errore-kontadoreen monitorizazioa; erredundantzia |
| Guztiak | Bus-segmentazioa + iragazketa zorrotzeko gateway-a |

---

## Azken gogoeta

- Zein eraso (injekzioa, replay-a, DoS-a) iruditzen zaizu arriskutsuena benetako ibilgailu batean? Zergatik?
- Zein segurtasun-sistema aktibo (balaztak, airbag-ak, ESP) babestuko zenuke lehenik CAN autentifikazioarekin?
- Ezagutzen al dituzu CAN 2.0, CAN FD eta CAN XL arteko desberdintasunak segurtasun aldetik?
