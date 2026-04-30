# Ikastaroaren Egitura: Zibersegurtasuna Automozioan

[Gaztelaniazko bertsioa](00_Programa_curso.md)

---

## 1. eguna — Autoaren komunikazioak eta Erasoak

**Helburua:** Arkitektura elektronikoa ulertzea eta ibilgailuari "entzuten" ikastea.

| Ordutegia | Blokea |
|---|---|
| 09:00 – 09:30 | **Aurkezpena:** Ikastaroaren edukiak eta helburuak |
| 09:30 – 10:30 | **Teoria: Paradigma Aldaketa** |
| 10:30 – 11:30 | **Araudien Errepasoa** (UNECE R155) |
| 11:30 – 12:00 | Atsedenaldia |
| 12:00 – 14:00 | **I. Praktikoa: CAN Bus Laborategia — A Praktika (Ezagutza pasiboa)** |

### 09:30 – 10:30 | Teoria: Paradigma Aldaketa

- **Gakoa:** Lehen, auto baten segurtasuna balaztekin edo airbag-ekin lotzen zen. Orain, segurtasun digitala (*zibersegurtasuna*) funtsezkoa da segurtasun fisikoa bermatzeko.
- **Azaldu beharrekoa:** ECU (Electronic Control Unit) bakoitza ordenagailu txiki bat da. Auto moderno batek 100 ECU baino gehiago izan ditzake, Ethernet, CAN eta LIN bidez komunikatuak.
- **Adibide praktikoa:** "Jeep Hack" (2015). Nola lortu zuten bolantea eta balaztak kontrolatzea urrunetik, entretenimendu sistemaren bidez.

### 10:30 – 11:30 | Araudien Errepasoa (UNECE R155)

- Instituzio arautzaileak eta betebeharrak
- Fitxa teknikoak
- ISO/SAE 21434 sarrera

### 12:00 – 14:00 | I. Praktikoa — CAN Bus: A Praktika (Ezagutza pasiboa)

> Dokumentazioa: [`CANbus_ICSim_Ciber/lab/04_Practica_A_Reconocimiento_eu.md`](CANbus_ICSim_Ciber/lab/04_Practica_A_Reconocimiento_eu.md)

**12:00 – 12:30 — Ingurunea konfiguratu**
- `setup_vcan.sh` exekutatu → `vcan0` interfazea altxatu
- ICSim abiarazi (`./icsim vcan0` + `./controls vcan0`)
- `candump vcan0` lehen ikuspegia: pantaila datuz beteko da
- Erronka: zer gertatzen da azeleragailua sakatzean? (`0x244` IDa)

**12:30 – 14:00 — A Praktika: Ezagutza pasiboa**
- `can_scanner.py`: ID guztiak maiztasunarekin zerrendatu
- `cansniffer`: ekintza ↔ byte-aldaketa korrelazioa
- Helburua: abiadura, ateak eta txandakatze-adierazleen IDak identifikatu

---

## 2. eguna — Eraso motak Automozio Sareetan

**Helburua:** Eraso kontrolatuak egitea eta datuen manipulazioa ulertzea.

| Ordutegia | Blokea |
|---|---|
| 09:00 – 10:30 | **Teoria: Alderantzizko Ingeniaritzako Teknikak** |
| 10:30 – 11:30 | **II. Praktikoa: CAN Bus Laborategia — B Praktika (Frame Injekzioa)** |
| 11:30 – 12:00 | Atsedenaldia |
| 12:00 – 13:00 | **III. Praktikoa: CAN Bus Laborategia — C Praktika (Replay Erasoa)** |
| 13:00 – 14:00 | **IV. Praktikoa: CAN Bus Laborategia — D Praktika (Fuzzing eta DoS)** |

### 09:00 – 10:30 | Teoria: Alderantzizko Ingeniaritzako Teknikak

**09:00 – 09:15 — Erakustaldi proiektatua: SavvyCAN (irakasleak)**

> Irakaslea SavvyCAN `vcan0`-ra konektatuta proiektatzen du `controls`-en azeleragailua mugitzen duen bitartean. Parte-hartzaileek denbora errealean ikusten dute `0x244` IDaren byteek gorantz doan kurba nola marrazten duten — atzo `cansniffer`-ekin testuan ikusi zuten datu bera, orain profesional batek bezala grafikatuta.
>
> **Mezu nagusia:** *"Hori da ikertzaileek eta OEM-ek erabiltzen duten tresna. Gure laborategian `cansniffer` eta `can_scanner.py` erabiltzen ditugu, konfigurazio gehigarririk gabe terminaleko baliokideak baitira."*
>
> Erreferentzia: [SavvyCAN](https://github.com/collin80/SavvyCAN) — kode irekiko GUI-a, SocketCAN (`vcan0`) onartzen du Linux-en.

**09:15 – 10:30 — Alderantzizko ingeniaritza: teoria eta metodologia**

- Segundoko milaka trama artean komando espezifiko bat nola isolatu
- CAN trafiko-azterketa metodologia: kaptura → iragazketa → korrelazioa → hipotesia → egiaztapena
- DBC fitxategiak: industriak CAN seinaleak nola dokumentatzen dituen (Vector estandarra)
- SavvyCAN eta DBC fitxategien irakurketa benetako testuinguruan

### 10:30 – 11:30 | II. Praktikoa — CAN Bus: B Praktika (Frame Injekzioa)

> Dokumentazioa: [`CANbus_ICSim_Ciber/lab/05_Practica_B_Inyeccion_eu.md`](CANbus_ICSim_Ciber/lab/05_Practica_B_Inyeccion_eu.md)

- `cansend` bidez frame injekzioa: abiaduragailua, argiak eta ateak manipulatu
- Begizta kontrolatua: egoera iraunkorra mantendu
- Nodo gatazka: injekzioa vs. kontrol legitimoak

### 12:00 – 13:00 | III. Praktikoa — CAN Bus: C Praktika (Replay Erasoa)

> Dokumentazioa: [`CANbus_ICSim_Ciber/lab/06_Practica_C_Replay_eu.md`](CANbus_ICSim_Ciber/lab/06_Practica_C_Replay_eu.md)

- `candump -l` bidez sekuentzia grabatu (ateak irekitzea)
- `replay_attack.py` bidez automatikoki erreproduzitu
- **Erakustaldi teorikoa:** haririk gabeko sareetako erasoak — TPMS eta Keyless Entry irrati-frekuentzia bidez

### 13:00 – 14:00 | IV. Praktikoa — CAN Bus: D Praktika (Fuzzing eta DoS)

> Dokumentazioa: [`CANbus_ICSim_Ciber/lab/07_Practica_D_Fuzzing_DoS_eu.md`](CANbus_ICSim_Ciber/lab/07_Practica_D_Fuzzing_DoS_eu.md)

- `fuzz_can.py`: random, targeted eta mutate moduak
- `can_dos.py`: bus flooding eta `canbusload` bidez eraginaren neurketa
- Portaera anomaloak dokumentatu

---

## 3. eguna — Defentsa eta Ikasgelarako Aplikazioa

**Helburua:** Ibilgailua babestea eta ezagutza hori LHko ikasleei transmititzea.

| Ordutegia | Blokea |
|---|---|
| 09:00 – 09:30 | **OBD-II Portua eta Segurtasun Gateway-ak** |
| 09:30 – 10:15 | **Zuzeneko demo: V16 Balizetan Ahultasunak — CVE-2025-65855** |
| 10:15 – 10:30 | Eztabaida + galderak |
| 10:30 – 11:30 | **Zibersegurtasuna Automozio Tailerrean** |
| 11:30 – 12:00 | Atsedenaldia |
| 12:00 – 13:30 | **V. Praktikoa: CTF Automotive — UrbanFleet 2026 (Ariketa Integratzailea)** |
| 13:30 – 14:00 | **Ondorioak eta Ebaluazioa** |

### 09:00 – 09:30 | OBD-II Portua eta Segurtasun Gateway-ak

- Fabrikatzaileak **Security Gateway (SGW)** nola ezartzen ari diren baimenik gabeko idazketak blokeatzeko
- **Kontzeptua:** OBD-II portua diagnostikorako da, baina "atea" ere bada. Auto berriek (2020+) Security Gateway-ak dituzte, eta kanpoko tresnek ezin dute busera idatzi ziurtagiri digitalik gabe
- **Eztabaida:** Nola eragiten dio honek tailer libreari? Fabrikatzailearen pasahitza behar al dugu balazta-pastillak aldatzeko?

### 09:30 – 10:15 | Zuzeneko demo — V16 Balizetan Ahultasunak: CVE-2025-65855

> Dokumentazio osoa: [`Automocion_V16_Ciber/lab/05_Demo_Ahultasunak_Help_Flash_eu.md`](Automocion_V16_Ciber/lab/05_Demo_Ahultasunak_Help_Flash_eu.md)

**09:30 – 09:40 — V16/DGT 3.0 sistemaren arkitektura**
- V16 baliza baten funtzionamendua: GPS → NB-IoT → APN pribatua → fabrikatzailearen zerbitzaria → DGT 3.0 → Google Maps/panelak
- Analizatutako gailua: **Help Flash IoT** (Espainian 250.000+ unitate saldu)

**09:40 – 09:50 — Ahultasunak (teoria)**
- 1. ahultasuna: UDP komunikazioak argian, enkriptatu eta autentifikatu gabe (IMEI, GPS, Cell ID agerian)
- Bektore aurreratua: fake eNodeB SDR bidez — ehunka metroko erradioan baliza guztiak interceptatu/isilarazi
- 2. ahultasuna: OTA eguneratzea autentifikatu gabe — SSID eta pasahitza gailuz gailu berdinak, hardcoded

**09:50 – 10:10 — Zuzeneko demo: OTA erasoa (CVE-2025-65855)**

```bash
# 1. WiFi AP faltsua gailu guztien kredentzialak erabiliz
nmcli device wifi hotspot ssid "HF-UpdateAP-5JvqFV" password "HF-UpdateAP-5JvqFV"

# 2. HTTP zerbitzari faltsua firmware maltzurrarekin
sudo python3 Automocion_V16_Ciber/scripts/fake_ota_server.py --dns

# 3. Balizako botoia 8 segundoz eduki → deskarga automatikoa ~30-60 s-tan
```

Proiektutako terminalak denbora errealean erakusten du gailuak nola deskargatzen duen firmware nortasuna ez sinadura digitalik egiaztatu gabe.

**10:10 – 10:15 — Nola egin beharko litzateke?**
- Falta denaren checklist-a: MQTT/TLS, kredentzial bakarrak, HTTPS, firmware sinadura, Secure Boot
- Arau-esparruak: UNECE R155, ISO/SAE 21434, ETSI EN 303 645

### 10:15 – 10:30 | Eztabaida eta galderak

- *Gailu hau DGT-k homologatuta dago — zer esan nahi du horrek homologazio-prozesuari buruz?*
- *Zer kostu baxuko neurrik arrisku gehiena kenduko luke?*
- CVE-2025-65855 (MITRE) — jatorrizko ikerketa: Luis Miranda Acebedo

### 10:30 – 11:30 | Zibersegurtasuna Automozio Tailerrean

- Diagnostiko-tresna piraten arriskuak
- Software eguneratzeen (OTA) garrantzia eta ziurtagirien kudeaketa
- Inoiz ez konektatu diagnostiko makina bat sare publikoetara
- Kontuz USB eta pendrive-ekin autoaren infotainment-ean

### 12:00 – 13:30 | V. Praktikoa — CTF Automotive: UrbanFleet 2026

> Dokumentazioa: [`CTF_Automotive/lab/01_Enunciado_participantes_eu.md`](CTF_Automotive/lab/01_Enunciado_participantes_eu.md)

**Ariketa integratzailea — 90 minutu — Banakakoa**

Parte-hartzaile bakoitzak Red Team baten rola hartzen du eta *UrbanFleet 2026* ibilgailu simulatuaren gainean 4 faseko eraso-kate bat burutzen du:

| Fasea | Teknika | Iraupena | Puntuak |
|---|---|---|---|
| F1 — Infiltrazioa | Ezagutza pasiboa | 20 min | 150 |
| F2 — Sarbidea | Frame injekzioa | 20 min | 200 |
| F3 — Iraunkortasuna | Replay erasoa | 20 min | 150 |
| F4 — Inpaktu maximoa | DoS + Fuzzing | 15 min | 150 |
| Bonus — Defentsa | Kontraneurriak | 15 min | 100 |

### 13:30 – 14:00 | Ondorioak eta Ebaluazioa

- CTF emaitzen aurkezpena eta irabazlearen aitorpena
- Eztabaida kolektiboa: zein kontraesanerako neurrik saihestu zezakeen fase bakoitza?
- Araudien errepasoa: UNECE R155 eta ISO/SAE 21434
- Ikastaroaren itxiera eta ebaluazio-inkesta

---

## Beharrezko baliabideak

### Hardware
- Irakasle-ordenagailua (ICSim proiektatzeko) + parte-hartzaile bakoitzeko ordenagailua

### Software (kode irekikoa)
- **Kali Linux** (gomendatua) edo Ubuntu 22.04 — VM edo native
- `can-utils`, `python-can`, ICSim, SavvyCAN

### Ezaugarriak (jatorrizko proposamena)
1. **Binaka gomendatua:** Informatikari bat + Automozioko bat — profilak nahasten badira; batek terminalarekin laguntzen du eta besteak motorraren testuinguru mekanikoa ematen du *(CTF banakako moduan ere bideragarria)*
2. **Software:** Kali Linux, tresna guztiak kode irekikoak
