# CTF Automotive — UrbanFleet 2026
## Parte-hartzaileentzako enuntziatua

[Gaztelaniazko bertsioa](01_Enunciado_participantes.md)

---

## Eszenatokia

> **[BARNE KOMUNIKATUA — RED TEAM BAIMENDUA]**
>
> **UrbanFleet 2026** car-sharing enpresak 200 ibilgailu konektatuak zabaldu ditu metropoli-eremuan. Telemetria ECU nagusia fabrikako konfigurazioaren arabera instalatu zen eta inoiz ez da auditatu.
>
> Jardunbide susmagarria detektatu da enpresaren eraikinen sotoko aparkalekuan. Segurtasun sailak zuen taldea kontratatu du **baimendutako Red Team ariketa** bat egiteko, eta ibilgailuaren OBD-II konektoreraen sarbide fisikoa duen erasotzaile baten eragina frogatzeko.
>
> **90 minutu** dituzu. Helburu ibilgailua ICSim bidez simulatzen da `vcan0`-n.

---

## Arauak

1. `vcan0` interfazearekin soilik jardun dezakezue — inoiz ez hardware fisikoarekin
2. Debekatuta dago laborategiko ingurunetik kanpoko sistemak erasotzea
3. Flag bakoitza Game Master-ari (GM) eman behar zaio ebidentziarekin (komandoa + kaptura)
4. GM-ak edozein flag-en ahozko azalpena eskatu dezake balioztatu aurretik
5. Berdinketan, denbora gutxien erabili duen parte-hartzaileak irabazten du

---

## Erabilgarri dauden tresnak

```
candump       cansend       cansniffer    cangen        canplayer
canbusload    can_scanner.py             replay_attack.py
fuzz_can.py   can_dos.py    python3       wireshark (aukerazkoa)
```

Tresna guztiak `PATH`-en daude edo `../CANbus_ICSim_Ciber/scripts/`-en.

---

## 1. FASEA — Infiltrazioa (Ezagutza pasiboa) · 20 min · 150 puntu

**Testuingurua:** *Erasotzaileak snifferr isil bat konektatzen du. Ez du frame bakarra ere bidali behar.*

**Helburuak:**
1. Bus trafikoa harrapatu gutxienez 60 segundoz frame bakar bat bidali gabe
2. Busean dauden ID bakoitzaren maiztasuna (Hz) kalkulatu
3. Zein IDk kontrolatzen duen ibilgailuaren abiadura identifikatu
4. Zein IDk kontrolatzen dituen ateak identifikatu
5. Ezkerreko txandakatzearen adierazlea aktibatzen duen 0. bytearen balioa identifikatu

**Fase honetako flagak:**
- `FLAG-F1A`: Abiadura kontrolatzen duen IDa (hex formatuan)
- `FLAG-F1B`: Ateak kontrolatzen duen IDa (hex formatuan)
- `FLAG-F1C`: Ezkerreko txandakatzearen adierazlearen IDaren 0. bytearen hex balioa

**Beharrezkoak diren ebidentziak:**
- `candump` log-aren kaptura
- Hz-ko maiztasunarekin IDen taula (`can_scanner.py` erabili)
- `cansniffer`-en pantaila-argazkiak ekintzak byte-aldaketekin korrelatuz

---

## 2. FASEA — Sarbidea (Frame injekzioa) · 20 min · 200 puntu

**Testuingurua:** *Ibilgailua aparkatuta dago. Erasotzaileak gailu bat konektatu du OBD-II-ra.*

**Helburuak:**
1. Abiadura-adierazlea 200 km/h-tik gora igo injekzio bidez
2. Larrialdiko argiak (hazard lights) aktibatu
3. Ibilgailuko ate guztiak desblokeatu
4. 30 segunduz jarraian kontrola aktibo mantendu (begizta-scripta)

**Fase honetako flagak:**
- `FLAG-F2A`: ICSim-en kaptura abiadura-adierazlea >200 km/h + erabilitako komando zehatza
- `FLAG-F2B`: ICSim-en kaptura larrialdiko argiak aktibo + komandoa
- `FLAG-F2C`: ICSim-en kaptura ateak desblokeatuta + komandoa
- `FLAG-F2D`: 30 s-z funtzionatu duen begizta-scripta + begizta aktibo duen terminalaren kaptura

**Beharrezkoak diren ebidentziak:**
- ICSim-en pantaila-argazkiak egoera bakoitzerako
- Erabilitako komando zehatzak edo scripta

---

## 3. FASEA — Iraunkortasuna (Replay erasoa) · 20 min · 150 puntu

**Testuingurua:** *Erasotzaileak zaindariaren rondaren bitartean sekuentzia legitimoa grabatu zuen. Ordu batzuk geroago presentzia fisikoa gabe errepikatzen du.*

**Helburuak:**
1. Gutxienez 30 segundo grabatu `controls`-a normalean erabiltzen den bitartean (ateak irekitzea barne)
2. Log-etik ate-frameak soilik filtratu eta errepikatu
3. Desblokeo osoko gertaera bat harrapatzeko behar den grabaketa-denbora minimoa neurtu

**Fase honetako flaga:**
- `FLAG-F3`: Desblokeo gertaera bat bermatzeko behar diren segundo kopurua (formatua: `FLAG-F3: Xs`)

**Beharrezkoak diren ebidentziak:**
- Grabazio `.log` fitxategia
- Erabilitako `replay_attack.py` komandoa
- ICSim-en pantaila-argazkiak replay aurretik eta ondoren

---

## 4. FASEA — Inpaktu maximoa (DoS + Fuzzing) · 15 min · 150 puntu

**Testuingurua:** *Ibilgailua lapurtzen den bitarteko distrakzio gisa, erasotzaileak busa saturatzen du aginte-panela ezgaitzeko.*

**Helburuak:**
1. Bus-karga oinarrizko baldintzetan neurtu (`canbusload`)
2. DoS eraso bat abiarazi eta karga %80 gainditzen duela frogatu
3. ICSim DoS bitartean erantzuteari uzten diola egiaztatu
4. Abiadura IDaren gaineko fuzzing zuzendua exekutatu eta portaera anomaloak dokumentatu

**Fase honetako flaga:**
- `FLAG-F4`: DoS bitartean lortutako frames/segundo tasa (formatua: `FLAG-F4: XXXXfps`)

**Beharrezkoak diren ebidentziak:**
- `canbusload`-en kaptura baldintza normaletan vs DoS bitartean
- DoS bitartean izoztutako ICSim-en pantaila-argazkiak
- Gutxienez portaera anomalo bat dokumentatuta duen fuzzing-log

---

## BONUS FASEA — Kontraesanerako neurriak (Defentsa) · 15 min · 100 puntu

**Testuingurua:** *Parte-hartzaileak (Blue Team rola) neurri tekniko erreala proposatu eta ezartzen du.*

`python-can` erabiliz **gutxienez bat** inplementatu:

**A aukera — Maiztasunaren anomalia-detektagailua:**  
ID batek oinarrizko maiztasunaren 2× gainditzen badu → alerta inprimatu kontsolan

**B aukera — ID whitelist-a:**  
Busa irakurri eta aurredefinitutako zerrendan ez dagoen IDa duen frame oro isilik baztertu (0x244, 0x188, 0x19B)

**C aukera — Rate limiter IDka:**  
ID bakoitzeko segundoko N frame gehienez; muga gainditzen duten frameak baztertu eta log-an erregistratu

**Fase honetako flaga:**
- `FLAG-BONUS`: Neurria zuzenean funtzionatzen erakutsi + iturburu-kodea

---

## Puntuazioa eta bonuak

| Fasea | Oinarrizko puntuak | Abiadura bonua |
|---|---|---|
| F1 — Ezagutza | 150 (50 flag bakoitzeko) | +50 F1 guztiak <15 min badira |
| F2 — Injekzioa | 200 (50 flag bakoitzeko) | +50 F2 guztiak <15 min badira |
| F3 — Replay-a | 150 | +50 <15 min badira |
| F4 — DoS/Fuzzing | 150 | +25 <10 min badira |
| Bonus — Defentsa | 100 | — |
| **Gehieneko totala** | **750 puntu** | **+175 puntu** |

---

## Azken entregariak

Denbora amaitzean, GM-ari eman `03_Hoja_flags_equipo_eu.md` beteta:
- Lortutako flag guztiak
- Ebidentzietarako erreferentziak (kaptura/script fitxategi-izena)
- GM-aren balioztapen galderei ahozko erantzuna
