# Laborategiaren konfigurazio azkarra Linux / Ubuntu 22-n
(irakasleentzako erreferentzia)

[Gaztelaniazko bertsioa](03_Setup_rapido_linux.md)

## Aukera gomendatua: Python stack lokala (sinplea)

### 1) Sistemaren aurretiazko baldintzak

```bash
# Python egiaztatu (3.10+ behar da)
python3 --version

# pip eta venv instalatu behar badira
sudo apt update
sudo apt install -y python3-pip python3-venv
```

### 2) Ingurune birtuala sortu eta aktibatu

```bash
# Laborategiaren karpetatik
python3 -m venv .venv
source .venv/bin/activate
```

> Terminalaren prompts-ak `(.venv)` erakutsiko du aktibatuta dagoenean.

### 3) Gutxieneko mendekotasunak instalatu

```bash
pip install -r requirements.txt
```

Instalatutako paketeak:
- `fastapi` — API framework-a
- `uvicorn` — ASGI zerbitzaria
- `pydantic` — datuen baliozkotzea
- `requests` — simulagailurako HTTP bezeroa

### 4) Laborategiaren gutxieneko egitura
- `backend/app.py`
- `simulator/send_event.py`
- `samples/event_legitimo.json`
- `logs/events.log`
- `reports/`
- `RUN_ME_FIRST.md`

### 5) Backend-a abiarazi

```bash
uvicorn backend.app:app --host 127.0.0.1 --port 8080 --reload
```

### 6) Egiaztapen funtzionala

```bash
# Terminal berri batean (.venv aktibatuta)
python3 simulator/send_event.py legitimo
```

Egiaztatu:
- `accepted` erantzuna terminalean.
- Sarrera `logs/events.log` fitxategian.
- Panel bisuala: `http://127.0.0.1:8080/aginte-panela`.

### 7) Segurtasun-probak

```bash
python3 simulator/send_event.py replay
python3 simulator/send_event.py timestamp-atrasado
python3 simulator/send_event.py coordenadas-invalidas
python3 simulator/send_event.py rafaga --count 8
```

### 8) Arrakasta-irizpideak
- Backend-ak replay-a eta politikatik kanpoko gertaerak baztertzen ditu.
- Bazterketa bakoitza `reason` eremuarekin dokumentatuta geratzen da.
- `/aginte-panela` panelean onarpenak eta bazterketak ageri dira.
- Taldeak ebidentziak entregatzen ditu `reports/` karpetan.

---

## Aukera alternatiboa: Docker (ikastetxean dagoeneko erabiltzen bada)

```bash
# Docker egiaztatu
docker --version
docker compose version

# Abiarazi
docker compose up
```

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
