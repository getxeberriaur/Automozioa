# Praktika Txostena — V16 Baliza Simulagailua ✅ IRAKASLEAREN BERTSIOA
**CVE-2025-65855 · Help Flash IoT · Ahultasun Analisia**

> ⚠️ **IRAKASLEAREN ERABILERA ESKLUSIBOARENTZAT — EZ BANATU PARTE HARTZAILEEI**

---

## Parte hartzailearen datuak

| Eremua | Balioa |
|--------|--------|
| **Izen-abizenak** | *(parte hartzaileak betetzeko)* |
| **Data** | *(parte hartzaileak betetzeko)* |
| **Modulua / Ikastaroa** | Automozioko Zibersegurtasuna |
| **Lan ingurunea** | Ubuntu 22 |

---

## 1. atala — Ingurunearen ezagupena ✅

### 1.1 Zer endpoint eskaintzen ditu backendak?

| Endpoint | Metodoa | Deskribapena |
|----------|---------|--------------|
| `/evento` | POST | Balizaren gertaerak jasotzen ditu (GPS posizioa, timestamp, ID) |
| `/health` | GET | Zerbitzaria aktibo dagoela egiaztatzen du |
| `/eventos` | GET | Erregistratutako gertaerak zerrendatzen ditu |

> ✅ **Zuzenketa**: Hiru endpointak onartzen dira. Parte hartzaileak `/evento` soilik identifikatzen badu, partzialki zuzena da. Endpoint nagusia identifikatzen ez bada penalizatu.

---

### 1.2 Zer eremu ditu gertaera legitimoak?

```json
{
  "device_id": "HF-IoT-TEST-001",
  "timestamp": "2026-05-26T10:00:00Z",
  "lat": 43.2627,
  "lon": -2.9253,
  "speed": 0.0,
  "battery": 85
}
```

> ✅ **Zuzenketa**: Gutxieneko eremu onargarriak: `device_id`, `timestamp`, `lat`, `lon`. `speed` eta `battery` aukerakoak dira. `timestamp` edo `device_id` falta badira penalizatu.

---

### 1.3 Zer erantzun ematen du backendak gertaera legitimo baten aurrean?

```json
{
  "status": "ok",
  "message": "Evento registrado correctamente",
  "event_id": "uuid-generatua"
}
```
**HTTP kodea: 200 OK**

> ✅ **Zuzenketa**: 200 kodea aipatzen duen eta gertaera onartzen dela deskribatzen duen edozein erantzun onartu.

---

## 2. atala — Eraso eszenatokiak ✅

### 2.1 Replay Attack

| Eremua | Balioa |
|--------|--------|
| **Exekutatutako komandoa** | `python3 simulator/send_event.py replay` |
| **Zerbitzariaren erantzuna** | `{"status": "error", "message": "Evento duplicado detectado"}` |
| **HTTP kodea** | `409 Conflict` |
| **Erasoak arrakasta izan du?** | ❌ Ez |
| **Zergatik?** | Backendak jasotako gertaera bakoitzaren SHA256 hash bat gordetzen du. Gertaera bera birritan bidaltzen bada, kolisioa detektatzen du eta baztertzen du. |

> ✅ **Zuzenketa**: Parte hartzaileak bikoiztuen detekzio mekanismoa identifikatu behar du (hash, UUID, nonce). Edozein erantzun tekniko zuzena onartzen da.
> ⚠️ **Akats ohikoa**: Timestamp ukoapena replay ukapenarekin nahastu. Mekanismo desberdinak dira.

---

### 2.2 Atzeratutako timestamp-a

| Eremua | Balioa |
|--------|--------|
| **Exekutatutako komandoa** | `python3 simulator/send_event.py timestamp-atrasado` |
| **Zerbitzariaren erantzuna** | `{"status": "error", "message": "Timestamp fuera de ventana permitida"}` |
| **HTTP kodea** | `400 Bad Request` |
| **Erasoak arrakasta izan du?** | ❌ Ez |
| **Zergatik?** | Backendak gertaeraren timestamp-a zerbitzariaren ordu nagusiarekin alderatzen du. Diferentzia 120 segundu baino gehiago bada (2 minutu), gertaera baztertzen du. |

> ✅ **Zuzenketa**: Parte hartzaileak "denbora-leihoa" edo "desfase maximoa" aipatu behar du. Leiho zehatza 120 segundu da — ez da beharrezkoa jakitea, baina kontzeptua bai.

---

### 2.3 Koordenatu baliogabeak

| Eremua | Balioa |
|--------|--------|
| **Exekutatutako komandoa** | `python3 simulator/send_event.py coordenadas-invalidas` |
| **Zerbitzariaren erantzuna** | `{"status": "error", "message": "Coordenadas GPS fuera de rango"}` |
| **HTTP kodea** | `422 Unprocessable Entity` |
| **Erasoak arrakasta izan du?** | ❌ Ez |
| **Zergatik?** | Backendak latitudea -90 eta +90 gradu artean eta longitudea -180 eta +180 gradu artean dagoela egiaztatzen du. Simulagailuak 123°-ko latitudea bidaltzen du, fisikoki ezinezkoa dena. |

> ✅ **Zuzenketa**: Koordinatuen tarte balioztapena aipatzen badu onartu. GPS spoofing prebentzioari buruz hitz egiten badu positiboki baloratu.

---

### 2.4 Identitate baliogabea

| Eremua | Balioa |
|--------|--------|
| **Exekutatutako komandoa** | `python3 simulator/send_event.py identidad-invalida` |
| **Zerbitzariaren erantzuna** | `{"status": "error", "message": "Dispositivo no registrado"}` |
| **HTTP kodea** | `401 Unauthorized` |
| **Erasoak arrakasta izan du?** | ❌ Ez |
| **Zergatik?** | Backendak baimendutako `device_id`-en zerrenda zuria mantentzen du. Ezezagunak diren IDak berehala baztertzen dira gertaera prozesatu gabe. |

> ✅ **Zuzenketa**: Zerrenda zuria (whitelist) edo ID autentifikazioaren kontzeptua identifikatu behar du. Balizaren OTA ahultasunarekin (autentifikaziorik gabe) erlazionatzen badu baloratu.

---

### 2.5 Rafaga (Rate Limiting)

| Eremua | Balioa |
|--------|--------|
| **Exekutatutako komandoa** | `python3 simulator/send_event.py rafaga --count 10` |
| **Zein eskaeratik aurrera hasi zen baztertzen?** | 6. eskaeratik aurrera |
| **Baztertzeko HTTP kodea** | `429 Too Many Requests` |
| **Ondorioa** | Backendak 5 eskaera mugatzen ditu gailu bakoitzeko 60 segunduko leiho batean. 6. eskaeratik aurrera 429 itzultzen du leihoa berrabiarazi arte. |

> ✅ **Zuzenketa**: Zenbaki zehatza (5 edo 6) inplementazioaren arabera alda daiteke. 429 kodea eta rate limiting kontzeptua ongi identifikatzen baditu onartu.

---

## 3. atala — Backendaren analisia ✅

### 3.1 Zer balioztapen inplementatzen ditu backendak?

| Balioztapena | Inplementatuta? | Kodea/lerroa |
|--------------|----------------|--------------|
| Timestamp egiaztapena | ✅ Bai | `backend/app.py` → `validar_timestamp()` funtzioa |
| Replay detekzioa | ✅ Bai | `backend/app.py` → `eventos_vistos` SHA256 hash-arekin |
| GPS koordenatuak balioztatzea | ✅ Bai | `backend/app.py` → `validar_coordenadas()` funtzioa |
| Gailuaren autentifikazioa | ✅ Bai | `backend/app.py` → `DISPOSITIVOS_AUTORIZADOS` zerrenda |
| Rate limiting | ✅ Bai | `backend/app.py` → `@limiter` dekoragailua SlowAPI-rekin |

> ✅ **Zuzenketa**: 5 balioztapenetatik gutxienez 4 identifikatzen baditu onartu. Ez da beharrezkoa lerro zehatza adieraztea, baina mekanismoa bai.

---

### 3.2 Identifikatu dituzun ahultasunak (arindu gabe daudenak)

1. **Enkriptaziorik gabe transmisioan**: Backendak HTTP arrunta erabiltzen du, ez HTTPS. Komunikazioak atzematen eta testu arrunt gisa irakurtzen dira.
2. **Gertaeren sinadura digitalik gabe**: Gertaerek ez dute sinadura kriptografikorik. `device_id` baliozkoa ezagutzen duen erasotzaile batek gertaera faltsuak fabrika ditzake.
3. **Zerrenda zuri estatikoa**: Baimendutako `device_id`-ak kodean bertan daude. Ez dago kredentzial txandakatzeko edo gailua baliogabetzeko modurik.

> ✅ **Zuzenketa**: Hiru hauek edo kodean identifikatutako ahultasunen edozein konbinazioa onartzen da. HTTPS edo sinadura kriptografikoa aipatzen badute bereziki baloratu.

---

### 3.3 Ebidentzia garrantzitsuenaren loga

```
INFO:     127.0.0.1:52341 - "POST /evento HTTP/1.1" 200 OK
INFO:     127.0.0.1:52342 - "POST /evento HTTP/1.1" 409 Conflict  ← replay detektatua
INFO:     127.0.0.1:52343 - "POST /evento HTTP/1.1" 400 Bad Request ← timestamp baliogabea
INFO:     127.0.0.1:52344 - "POST /evento HTTP/1.1" 422 Unprocessable Entity ← GPS baliogabea
INFO:     127.0.0.1:52345 - "POST /evento HTTP/1.1" 401 Unauthorized ← ID ezezaguna
INFO:     127.0.0.1:52350 - "POST /evento HTTP/1.1" 429 Too Many Requests ← rate limit
```

> ✅ **Zuzenketa**: Gutxienez 3 zerbitzariaren erantzun desberdin erakutsi behar ditu. Loga hutsik badago penalizatu.

---

## 4. atala — Hobekuntza proposamenak ✅

### 4.1 Nola hobetuko zenuke backendaren segurtasuna?

| Identifikatutako ahultasuna | Proposatutako hobekuntza |
|----------------------------|--------------------------|
| Enkriptaziorik gabeko HTTP | TLS/HTTPS inplementatu ziurtagiri baliodunarekin |
| Gertaeren sinadura falta | HMAC-SHA256 sinadura gehitu gailu bakoitzeko gako partekatuekin |
| Zerrenda zuri estatikoa | Token berritzaileekin erregistro sistema dinamikoa |
| IP bidezko rate limiting | `device_id` bidezko rate limiting + anomalien aurrean aldi baterako blokeo |
| Auditoriarik gabe | Segurtasun log iraunkorra eraso patroien aurrean alertekin |

> ✅ **Zuzenketa**: Identifikatutako ahultasunekin koherenteak diren gutxienez 3 proposamen onartzen dira. Estandarrak (TLS, HMAC, OAuth) aipatzen badituzte baloratu.

---

### 4.2 Zer aldaketa egingo zenituzke baliza → zerbitzari protokoloan?

1. **Mutur-muturrekoa enkriptatzea**: TLS 1.3 derrigorrezkoa komunikazio guztietan, bezeroaren ziurtagiriarekin gailua autentifikatzeko.
2. **Mezu bakoitzaren sinadura kriptografikoa**: Gertaera bakoitza ECDSA bidez sinatuta gailuaren secure element-ean gordetako gako pribatu batekin.
3. **Nonce + timestamp konbinatua**: Mezu bakoitzak zerbitzariak hasierako handshake-ean sortutako nonce bakarra darama, replay attackak ezinezkotuz.

> ✅ **Zuzenketa**: Proposamen tekniko sendoa duen edozein erantzun onartu. Secure element, PKI edo mutual TLS aipatzen badute bereziki baloratu.

---

## 5. atala — Azken hausnarketa ✅

### 5.1 Zer benetako eragin izango luke ahultasun hauek produkzioan ustiatzeak?

> **Eredu erantzuna:**
> Espainian 250.000 V16 IoT baliza baino gehiago zabalduta dituen benetako produkzio sistema batean, ahultasun hauen ustiapena ondorio larriak izango lituzke. Erasotzaile batek ehunka balizaren GPS posizioa aldi berean faltsu dezake, DGTri koordinatu falsoak bidaliz eta autobideko tarte hutsetan istripuaren alerta inexistenteak sortuz. Horrek larrialdi zentroak bete-betean saturaraziko lituzke eta larrialdi benetako baliabideak kokapen faltsuetara desbideratuko lituzke. Gainera, replay eraso masibo batek backend-a kolapsa dezake gertaera bikoiztuekin, sistemaren argi-itzaltze jakinarazpen zerbitzua etenda utziz. Autentifikazio sendorik ezak balizak erregistratzeko aukera ere emango luke benetako larrialdian inoiz aktibatuko ez direnak, sisteman konfiantza duten erabiltzaileen bide segurtasuna arriskuan jarriz.

> ✅ **Zuzenketa**: Erantzunak gutxienez hauek aipatu behar ditu: bide segurtasunean eragina, sistemaren saturazio posiblea eta larrialdi zerbitzuetarako ondorioak. 3 lerro baino gutxiagoko erantzunak edo ahultasun teknikoa benetako eraginarekin lotzen ez dituztenak penalizatu.

---

### 5.2 Zer erlazio du praktika honek UNECE R155 araudiarekin?

> **Eredu erantzuna:**
> UNECE R155 araudiak ibilgailuen eta sistema konektatuen fabrikatzaileei produktuaren bizi-ziklo osoa estaltzen duen Zibersegurtasun Kudeaketa Sistema (CSMS) bat ezartzeko behartzen die, mehatxuen identifikazioa, neurriak inplementatzea eta gertakariei erantzutea barne. Praktika honetan erakutsitako ahultasunak (autentifikaziorik eza, enkriptaziorik eza, osotasun balioztatzerik gabe) R155-ek arrisku analisian detektatu eta arintzeko eskatzen dituen hutsegite mota dira (TARA — Threat Analysis and Risk Assessment). DGTren azpiegiturarekin komunikatzen den V16 IoT baliza sistema R155-en aplikazio esparruaren barruan sartuko litzateke bide segurtasun sistema konektatu gisa, eta fabrikatzailea (Netun Solutions) ahultasun hauek zuzentzera behartuta egongo litzateke integratzen den ibilgailua edo sistema homologatu aurretik.

> ✅ **Zuzenketa**: Erantzunak UNECE R155, CSMS eta/edo TARA aipatu behar ditu. Praktika teknikoa arau esparruarekin ongi lotzen badute baloratu. Zehaztasun gutxiagoko erantzun laburrak onartzen dira.

---

## Irakaslearen zuzenketako zerrenda

- [ ] 1. atala osoa — endpointak eta JSON ongi identifikatu
- [ ] 2. atala — 5 eszenatoki exekutatu HTTP kode zuzenekin
- [ ] 3. atala — gutxienez 4 balioztapen identifikatu + 2 arindu gabeko ahultasun
- [ ] 4. atala — gutxienez 3 hobekuntza proposamen koherente
- [ ] 5. atala — hausnarketa teknika benetako eraginarekin eta R155-ekin lotzen du
- [ ] Ebidentzien loga erantsi edo itsatsi

### Ebaluazio irizpide orientagarria

| Puntuazioa | Irizpidea |
|------------|---------|
| **Bikaina** | Atal guztiak osoak, ahultasunak ongi identifikatuta, proposamen tekniko sendoak, hausnarketa R155-ekin lotuta |
| **Zuzena** | Gutxienez 4/5 atal osoak, HTTP kodeetan edo mekanismo izenetan akats txikiak |
| **Osatugabea** | 3 atal baino gutxiago osoak edo eszenatoki exekutatu gabe |
| **Ez egokia** | 2. atala hutsik (eszenatokiak exekutatu gabe) edo beste parte hartzaile baten kopia |

---
*Irakaslearen bertsioa — Automozioko Zibersegurtasun ikastaroa — Automozioa*