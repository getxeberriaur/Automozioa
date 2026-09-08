# Laborategia konfiguratzeko checklista (irakaslea)

[Gaztelaniazko bertsioa](02_Checklist_configuracion_laboratorio.md)

## A) Aurretiazko baldintzak (host)
- Sistema: **Ubuntu 22.04 LTS** (makina birtuala edo fisikoa).
- Python 3.10+ instalatuta (`python3 --version`).
- `python3-venv` eta `python3-pip` eskuragarri (`sudo apt install -y python3-venv python3-pip`).
- Editorea (VS Code gomendatua).
- Terminal lokalerako sarbidea.
- Trafiko-sistema errealekin konexiorik ez.

## B) Ingurunearen prestaketa (talde bakoitzeko)
1. Laborategiko karpeta sortu talde bakoitzarentzat.
2. Ingurune birtuala sortu: `python3 -m venv .venv`
3. Ingurunea aktibatu: `source .venv/bin/activate`
4. Mendekotasunak instalatu: `pip install -r requirements.txt`
5. Egiaztatu 8080 ataka libre dagoela: `ss -tlnp | grep 8080`

## C) Gutxieneko osagaiak
- `backend/`: simulatutako V16 abisuak jasotzeko APIa.
- `simulator/`: baliza-emuladorea, proba-eszenatokiekin.
- `logs/`: erabakien erregistroa (`accepted/rejected` + arrazoia).
- `reports/`: taldearen ebidentziak.
- Panel bisuala: `http://127.0.0.1:8080/aginte-panela`.

## D) Probarako datu gomendatuak
- Balizaren 2 identitate baliozko.
- Identitate baliogabe 1.
- Gertaera-txantiloiak:
  - legitimoa
  - replay-a
  - atzeratutako timestamp-a
  - koordenatu baliogabeak
  - ráfaga edo burst-a

## E) Backend-ean egin beharreko gutxieneko balidazioak
- Derrigorrezko JSON eskema.
- Koordenatuak baliozko tartean egotea.
- `security.sent_at` denbora-leihoaren barruan egotea.
- `security.nonce` berriro erabili ezin izatea.
- Identitate bakoitzeko tasa-kontrola.

## F) Gomendatutako logging-a
Gertaera bakoitzeko eremuak:
- `message_id`
- `device_id`
- `alert_id`
- `alert_type`
- `alert_status`
- `sent_at`
- `decision` (`accepted/rejected`)
- `reason`
- `source_ip`
- `received_at`

## G) “Laborategia prest” irizpidea
- Gertaera legitimo 1 jasotzen da eta `accepted` gisa markatzen da.
- Replay bat bidaltzen da eta `rejected` gisa markatzen da, `replayed_nonce` arrazoiarekin.
- Gutxienez 3 ebidentzia dituen txostena sortzen da.

## H) Irakaslearen kontingentzia-plana
Talde baten inguruneak huts egiten badu:
- 1. aukera: irakaslearen babeskopiako instantzia partekatua erabiltzea.
- 2. aukera: aurrez grabatutako trazen analisi modura pasatzea.
- 3. aukera: modelatzean eta mitigazioetan oinarritutako ebaluazio partziala egitea.

## I) Laborategiaren segurtasuna eta etika
- Tokiko sandbox-a edo sare isolatua bakarrik.
- Debekatuta dago kanpoko azpiegiturak eskaneatzea edo probatzea.
- Helburua hezitzailea da: defentsa, hardening-a eta detekzioa.
