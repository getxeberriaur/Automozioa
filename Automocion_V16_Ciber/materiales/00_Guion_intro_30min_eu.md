# Sarrera (30 min): Zibersegurtasuna larrialdiko baliza konektatuetan (V16)

[Gaztelaniazko bertsioa](00_Guion_intro_30min.md)

Diapositiben euskarri-materiala: [00_Diapositivas_intro_30min.md](00_Diapositivas_intro_30min.md)

Proiektore bertsioa (gaztelania): [00_Diapositivas_intro_30min_proyector.md](00_Diapositivas_intro_30min_proyector.md)

Proiektore bertsioa (euskara): [00_Diapositivas_intro_30min_proyector_eu.md](00_Diapositivas_intro_30min_proyector_eu.md)

## 1) Mini-saioaren helburuak
Sarrera amaitzean, irakasleek honako hau egiteko gai izan beharko dute:
- baliza konektatuaren rola azaltzea trafiko adimendunaren ekosisteman;
- aktibo kritikoak eta eraso-azalera identifikatzea;
- arrisku teknikoak bide-segurtasunean duten inpaktuarekin lotzea;
- 2 orduko laborategi praktikoan zer balidatuko den ulertzea.

---

## 2) Denbora-egitura (30 min)

### 0:00–0:03 | Irekiera eta testuingurua (3 min)
**Mezu nagusia:** ez da “IoT hutsa”; errepidean eragin zuzena duen sistema ziberfisiko bat da.

Galdera eragileak:
- Zer gertatzen da baliza batek gorabehera faltsuak jakinarazten baditu?
- Zer gertatzen da benetako gorabehera bat backend-era iristen ez bada?

### 0:03–0:10 | Arkitektura funtzional sinplifikatua (7 min)
Azaldu diagrama sinple batekin:
1. V16 gailu konektatua (firmware-a + identitatea)
2. Sare mugikorra / garraioa
3. Harrera- eta balidazio-backenda
4. Trafiko-plataformarekiko integrazioa
5. Hirugarrenen kontsumoa (panelak, app-ak, zerbitzuak)

**Aktibo kritikoak:**
- Gakoak/ziurtagiriak
- Firmware-aren osotasuna
- Gertaeraren osotasuna eta freskotasuna (`timestamp`/`nonce`)
- Backend-aren erabilgarritasuna
- Gertaeren trazabilitatea

### 0:10–0:20 | Mehatxu nagusiak (10 min)
Erabili STRIDE irakaskuntza-bertsioan:
- **S**uplantazioa: baliza faltsua edo klonatutako identitatea.
- **T**ampering: gertaera aldatzea transmisioan edo jatorrian.
- **R**epudioa: nork zer bidali duen frogatzeko ebidentziarik eza.
- **I**nformazioa: kokapenaren eta metadatuen ihesa.
- **D**enegazio-zerbitzua: APIaren saturazioa edo blokeo logikoa.
- **E**skalada: backend-ean edo plataforman pribilegioen abusua.

Azpimarratzeko inpaktu didaktikoa:
- Bide-segurtasuna (abisu okerrak / abisurik eza)
- Trafiko-eragiketa (zarata eta lehentasun txarra)
- Arau-betetzea eta ospea

### 0:20–0:26 | Espero daitezkeen kontrolak (6 min)
- Gailuaren identitate sendoa.
- Mezuen sinadura/autentikazioa.
- Replay erasoen aurkako babesa (`nonce` + denbora-leihoa).
- Garraio-zifratzea eta backend-ean balidazio zorrotza.
- Anomaliak detektatzeko logging-a eta korrelazioa.
- Ezeztapena eta gorabeheren aurreko erantzuna.

> **Laborategiarekiko lotura:** nonce-aren kontrolak (`nonce_cache`), denbora-leihoa (`TIMESTAMP_WINDOW_SECONDS = 30`) eta rate limiting-a (`RATE_LIMIT_MAX_EVENTS = 5`) backend-ean inplementatuta daude. Parte-hartzaileek funtzionatzen ikusteko aukera izango dute — eta balioak aldatuta hautsi ere bai.

### 0:26–0:30 | Laborategirako zubia (4 min)
**2 orduan egingo dutena:**
1. Trafiko legitimoa sortu eta panel bisualean eta log-etan behatu.
2. Logika-erasoak simulatu ingurune kontrolatuan (replay-a, timestamp manipulatua, identitate faltsua, ráfaga) eta HTTP erantzun-kodeak idatzi.
3. **Hardening-a:** backend-aren parametroak aldatu (`TIMESTAMP_WINDOW_SECONDS`, `RATE_LIMIT_MAX_EVENTS`) eta zuzeneko eragina neurtu — kontrol-teoria kode-lerro zehatz batzuekin lotuz.
4. Ebidentziak dokumentatu eta ondorioak txostenaren txantiloian idatzi.

> **Truko didaktikoa:** `backend/app.py`-ren konstante-blokea pantailan erakutsi zubi honetan. Parte-hartzaileek ikusiko dute azaldu berri dituzun kontrolak literalki 4 kode-lerro direla — segurtasuna desmitifikatzen du eta hardening-a motibatzen.

---

## 3) Diapositiben gidoia (10 diapositiba iradokitu)
1. Izenburua eta helburua
2. Errepideko benetako erabilera-kasua
3. Muturretik muturrerako arkitektura
4. Aktibo kritikoak
5. Mehatxu nagusiak
6. Inpaktu/probabilitate matrizea (azkarra)
7. Geruzaz geruzako kontrolak
8. Laborategian zer neurtuko dugun
9. Hondar-arriskua eta ikasgaiak
10. Itxiera + trantsizio praktikoa

---

## 4) Errepikatzeko mezu didaktiko nagusiak
- “Ez dugu benetako sistemarik ustiatu nahi; babesten ikasi nahi dugu.”
- “Automozioan, zibersegurtasuna pertsonen segurtasun bihurtzen da.”
- “Ebidentziarik gabe (log-ak eta trazabilitatea), ez dago erantzun eraginkorrik.”

---

## 5) Ulermen azkarraren mini-errubrika (aukerakoa, 5 min)
- 3 aktibo kritiko identifikatzen al ditu? (Bai/Ez)
- Spoofing-a eta replay-a bereizten al ditu? (Bai/Ez)
- Kontrol bat mehatxu jakin batekin lotzen al du? (Bai/Ez)
