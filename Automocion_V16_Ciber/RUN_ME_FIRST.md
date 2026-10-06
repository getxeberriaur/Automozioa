# Abiarazte azkarra — V16 laborategia

V16 abisuak tokiko API batera bidaltzea simulatzen duen laborategia da. Exekutatu komandoak `Automocion_V16_Ciber/` karpetatik.

## 1. Python ingurunea prestatu

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Linux edo macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instalatu mendekotasunak:

```text
pip install -r requirements.txt
```

## 2. Backend-a abiarazi

```text
uvicorn backend.app:app --host 127.0.0.1 --port 8080
```

Ireki `http://127.0.0.1:8080/docs` edo `http://127.0.0.1:8080/aginte-panela`.

## 3. Agertokiak exekutatu

Bigarren terminal batean, oraindik `Automocion_V16_Ciber/` karpetan:

```text
python simulator/send_event.py legitimo
python simulator/send_event.py replay
python simulator/send_event.py timestamp-atrasado
python simulator/send_event.py coordenadas-invalidas
python simulator/send_event.py identidad-invalida
python simulator/send_event.py rafaga --count 8
```

Agertokien izenak simulagailuaren komando-interfazearen parte dira; ez itzuli komando horiek.

## 4. Ebidentziak berrikusi eta entregatu

Aztertu `logs/events.log`, tokiko panela eta `http://127.0.0.1:8080/events/recent?limit=10`. Bete `reports/00_Ebidentzia_txosten_txantiloia.md` txantiloia.

Trafiko guztia `127.0.0.1` helbidean geratzen da. Ez erabili beste ostalaririk eta ez konektatu laborategia kanpoko zerbitzuetara.
