# Sarrerako diapositibak (30 min) — Proiektore bertsioa (Euskara)

> Formatua: pantailan gutxieneko edukia + hizlariaren oharrak.

---

## 1. diapositiba — V16 konektatua: zibersegurtasuna eta bide-segurtasuna
### Pantaila
- Zibersegurtasuna V16 baliza konektatuetan
- Sarrera + laborategi praktikoa (2h)
- Defentsa ingurune simulatuan

### Hizlariaren oharrak
- Saioaren markoa: ez dugu ustiatu nahi, babestu baizik.
- Helburua: arriskua ulertu eta kontrolak balidatu.

---

## 2. diapositiba — Zer gertatzen da balizak abisu bat bidaltzen duenean?
### Pantaila
- Balizak gorabehera detektatzen du
- Abisua plataformara bidaltzen du
- Plataformak erabakitzen du: onartu ala baztertu

### Hizlariaren oharrak
- Galdera taldeari: zer gertatzen da abisu faltsu bat onartzen bada?

---

## 3. diapositiba — Muturretik muturrerako fluxua
### Pantaila
- V16 gailua
- Komunikazio-sarea
- Backend hartzailea
- Trafikoko plataforma / zerbitzuak

### Hizlariaren oharrak
- Azpimarratu jauzi bakoitzean dagoen eraso-azalera.

---

## 4. diapositiba — Aktibo kritikoak
### Pantaila
- Gailuaren identitatea
- Abisuaren osotasuna
- Denbora-freskotasuna
- Backend-aren erabilgarritasuna
- Trazabilitatea

### Hizlariaren oharrak
- Trazabilitaterik gabe, ez dago gorabeherari erantzun eraginkorrik.

---

## 5. diapositiba — Mehatxu nagusiak
### Pantaila
- Suplantazioa
- Replay-a
- Tartez kanpoko datuak
- Ráfaga / API abusua

### Hizlariaren oharrak
- Mehatxu bakoitza inpaktu operatibo erreal batekin lotu.

---

## 6. diapositiba — Lehentasun azkarra (inpaktua vs probabilitatea)
### Pantaila
- Lehentasun altua: replay-a, suplantazioa, ráfaga
- Lehentasun ertaina: timestamp/koordenatu baliogabeak

### Hizlariaren oharrak
- Defentsa-priorizazioaren irizpidea azaldu.

---

## 7. diapositiba — Backend-eko defentsa-kontrolak
### Pantaila
- JSON eskema zorrotza
- Denbora-leihoa (`security.sent_at`)
- Anti-replay (`security.nonce`)
- Identitateko rate limiting-a
- `reason` eremuarekin logging-a

### Hizlariaren oharrak
- Kontrol horiek laborategian dagoeneko ezarrita daudela erakutsi.

---

## 8. diapositiba — Praktikan zer neurtuko dugu
### Pantaila
- Baliogabeen onarpen-tasa
- Bazterketen kalitatea (arrazoiarekin)
- Ebidentzia tekniko trazagarria

### Hizlariaren oharrak
- Ikuspegi bisualak:
  - Panela: http://127.0.0.1:8080/aginte-panela
  - JSON: http://127.0.0.1:8080/events/recent?limit=10

---

## 9. diapositiba — Hondar-arriskua
### Pantaila
- Oraindik produkzio-mailako kontrolak falta dira
- Sinadura, PKI, mTLS, SOC

### Hizlariaren oharrak
- Laborategia oinarri errealista dela azaldu, ez azken produkzio-ingurunea.

---

## 10. diapositiba — Laborategirako trantsizioa
### Pantaila
- 1) Abisu legitimoa
- 2) Replay-a eta baliogabeak
- 3) Panela/log bidezko behaketa
- 4) Ebidentzia-txostena

### Hizlariaren oharrak
- Urrezko araua: tokiko sandbox-a edo sare isolatua soilik.
