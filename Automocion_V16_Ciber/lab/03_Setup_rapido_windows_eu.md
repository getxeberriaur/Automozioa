# Laborategiaren konfigurazio azkarra Windows-en (irakasleentzako erreferentzia)

[Gaztelaniazko bertsioa](03_Setup_rapido_windows.md)

## Aukera gomendatua: Python stack lokala (sinplea)

### 1) Ingurune birtuala sortu
- Ireki terminala laborategiaren karpetan.
- Sortu `venv` ingurunea.
- Aktibatu `venv` ingurunea.

### 2) Gutxieneko mendekotasunak instalatu
Iradokitako paketeak:
- fastapi
- uvicorn
- pydantic
- requests

### 3) Gutxieneko egitura
- `backend/app.py`
- `simulator/send_event.py`
- `samples/event_legitimo.json`
- `logs/events.log`
- `reports/`
- `RUN_ME_FIRST.md`

### 4) Egiaztapen funtzionala
- Abiarazi backend-a ataka lokalean (adibidez, 8080).
- Bidali gertaera legitimo bat simulagailutik.
- Baieztatu `accepted` egoera log-etan edo `/events/recent` endpoint-ean.
- Egiaztatu ikusizko panela: `/aginte-panela`.

### 5) Segurtasun-probak
- Payload beraren birbidalketa (replay-a).
- Denbora-leihotik kanpoko timestamp-a.
- Koordenatu baliogabeak.
- Gertaeren ráfaga.

### 6) Arrakasta-irizpideak
- Backend-ak replay-a eta politikatik kanpoko gertaerak baztertzen ditu.
- Bazterketa bakoitza `reason` eremuarekin dokumentatuta geratzen da.
- `/aginte-panela` panelean onarpenak eta bazterketak ageri dira.
- Taldeak ebidentziak entregatzen ditu `reports/` karpetan.

---

## Aukera alternatiboa: Docker (ikastetxean dagoeneko erabiltzen bada)
Osagaiak:
- `api` zerbitzua (FastAPI)
- `simulator` zerbitzua
- `logs` karpetarako bolumena

Abantailak:
- Aldakortasun txikiagoa taldeen artean.
- Ingurune-hutsegiteen aurrean berreskuratze azkarra.

Arriskua:
- Docker-ek ikasgelan huts egiten badu, erabili B plana Python stack lokalarekin.

---

## Eragiketa-irakaspraktika onak
- Prest eduki babeskopiako instantzia bat saioa hasi aurretik exekutatzen.
- Izan aurrez grabatutako trazak, talde bat blokeatzen bada ebaluazioa egin ahal izateko.
- Amaitu lehen/ondoren konparazio batekin eta beste ITS sistemetara transferi daitezkeen ikaskuntzekin.
