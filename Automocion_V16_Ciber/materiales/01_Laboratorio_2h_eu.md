# Laborategi praktikoa (2h): V16 abisuen segurtasuna ingurune simulatuan

[Gaztelaniazko bertsioa](01_Laboratorio_2h.md)

## 1) Helburua
Balidatzea nola aldatzen diren segurtasun-emaitzak backend-ak kontrol sendoak **ez** dituenean eta bai dituenean.

> Garrantzitsua: laborategia guztiz simulatua da eta trafiko-sistema errealetatik isolatuta dago.

---

## 2) Ikaskuntza-emaitza
Amaieran, talde bakoitzak honako hau egiteko gai izango da:
- V16 abisuen bidalketan dauden ahultasun logikoak detektatzea;
- replay/injekzio proba kontrolatuak exekutatzea sandbox-ean;
- oinarrizko mitigazioak ezarri eta haien eraginkortasuna egiaztatzea;
- ebidentziak aurkeztea (pantaila-argazkiak, log-ak, ondorioak).

---

## 3) Agenda xehea (120 min)

### A fasea — Prestaketa eta baseline-a (0–25 min)
- Ingurune lokala abiarazi.
- Emuladoretik abisu legitimoak bidali.
- `/aginte-panela` panela eta backend-aren log-ak berrikusi.

**A entregagaia:** gertaera legitimo baten pantaila-argazkia eta ikusitako latentzia.

### B fasea — Eraso kontrolatua (25–55 min)
- 1. eszenarioa: baliozko gertaera baten replay-a.
- 2. eszenarioa: gaizki formatutako edo tartez kanpoko gertaeraren injekzioa.

**B entregagaia:** onarpen desegokiaren ebidentziak (hala gertatzen bada) eta azalpena.

### C fasea — Hardening-a (55–95 min)
Aktibatu/egiaztatu kontrol hauek:
- Abisu bakoitzeko `security.nonce` bakarra
- Denbora-leihoa (adibidez, ±30 s)
- Eskema- eta koordenatu-balidazio zorrotzak
- Identitate bakoitzeko rate limiting-a

**C entregagaia:** erasoen arrakasta/porrota jasotzen duen aurretik/ondoren taula.

### D fasea — Detekzioa eta itxiera (95–120 min)
- Log-ak eta alertak berrikusi.
- IOC sinpleak dokumentatu (replay ereduak, burst-ak, koordenatu ezinezkoak).
- Talde bakoitzaren aurkezpen laburra (3 min).

**D entregagaia:** txosten tekniko laburra (orrialde 1).

---

## 4) Laborategiaren gutxieneko arkitektura
- **Baliza-simulagailua** (bezero-script-a)
- **Abisuak jasotzeko APIa** (backend lokala)
- **Gertaeren biltegiratzea** (JSON/SQLite)
- **Behaketa-kontsola** (`/aginte-panela` + `/events/recent` + log-ak)

Fluxua:
1. Emuladoreak V16 abisu bat sortzen du (`device`/`alert`/`location`/`security`).
2. APIak identitatea, `security.sent_at`, `security.nonce` eta formatua balidatzen ditu.
3. APIak onartu edo baztertu egiten du.
4. Log-ek erabakia eta arrazoia erregistratzen dituzte.

---

## 5) Nahitaezko proba-kasuak
1. Sinadura/kredentzial baliozkoak dituen gertaera legitimoa.
2. Gertaera beraren replay zehatza.
3. Timestamp zaharra duen gertaera.
4. Tartez kanpoko koordenatuak dituen gertaera.
5. Rate limiting-a probatzeko gertaera-ráfaga.

---

## 6) Ebaluazio-metrikak
- Gertaera baliogabeen onarpen-tasa (0ra hurbildu behar du).
- Gertaera legitimoetan dauden positibo faltsuen tasa.
- Anomalia detektatzeko denbora.
- Ebidentzien eta trazabilitatearen kalitatea.

---

## 7) Errubrika azkarra (10 puntu)
- 3 pt: baseline-aren eta erasoen exekuzio teknikoa
- 3 pt: kontrolen inplementazioa/egiaztapena
- 2 pt: log-en detekzioa eta analisia
- 2 pt: txostenaren argitasuna eta gomendioak

---

## 8) Azken debrief-a (galdera gidariak)
- Zein kontrol izan da eraginkorrena kostu txikienarekin?
- Zein hondar-arrisku geratzen da?
- Zer gehituko zenukete produkzio-ingurunerako (PKI, OTA, SOC, erantzuna)?
