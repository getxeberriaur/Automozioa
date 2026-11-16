# Hasiera azkarra laborategin

Laborategi honek V16 baliza baten abisua simulazio-plataforma bati bidaltzea emulatzea du helburu.

Ikastaldi-aula deskribitzeko gidabidea: [lab/04_Despliegue_participantes.md](lab/04_Despliegue_participantes.md)

## 1) Entorno birtuala sortzea eta aktibatzea

### Windows PowerShell
1. `python -m venv .venv`
2. `.\.venv\Scripts\Activate.ps1`

### macOS / Linux
1. `python3 -m venv .venv`
2. `source .venv/bin/activate`

## 2) Mendekotasunak instalatzea

`pip install -r requirements.txt`

## 3) Backend-a abiatzea

`uvicorn backend.app:app --host 127.0.0.1 --port 8080 --reload`

### Dokumentazioa interaktiboa ikustea

`http://127.0.0.1:8080/docs`

### Eragiketaren panela ikustea

`http://127.0.0.1:8080/aginte-panela`

## 4) Simuladorea probatzea

### Gertaera legitima
`python3 simulator/send_event.py legitimo`

### Replay-a
`python3 simulator/send_event.py replay`

### Atzeratutako denbora
`python3 simulator/send_event.py timestamp-atrasado`

### Baliogabeko koordenatuak
`python3 simulator/send_event.py coordenadas-invalidas`

### Baliogabeko identitatea
`python3 simulator/send_event.py identidad-invalida`

### Bultzada
`python3 simulator/send_event.py rafaga --count 8`

## 5) Ebidentziak berrikustea

- Log nagusia: `logs/events.log`
- Datorren abisua prozesutuak: `http://127.0.0.1:8080/events/recent?limit=10`
- Panela euskaraz: `http://127.0.0.1:8080/aginte-panela`
- Txostenen karpeta: `reports/`

### Txostenen plantilak

- Gaztelania: `reports/00_Plantilla_informe_evidencias.md`
- Euskara: `reports/00_Ebidentzia_txosten_txantiloia.md`

### Sarrera aurkezpenak (proiektua)

- Gaztelania: `presentaciones/Intro_V16_30min_ES.html`
- Euskara: `presentaciones/Intro_V16_30min_EU.html`

## 6) Partehartzaileentzako despliegua (laburreza)

### A aukera (gomendatua): Git bidez online
1. `git clone <URL_DEL_REPO>`
2. `cd Automozioa/Automocion_V16_Ciber`
3. `git checkout v1.0-aula` (edo irakaslearen adierazitako bertsioa)
4. `venv` sortzea, mendekotasunak instalatzea eta backend-a abiatzea.

### B aukera (B plana): Ergelaren ZIP
1. Irakaslearena emandako bertsio finkoaren deskonprimitzea.
2. Entorno eta abiarazte pausuak exekutatzea.

### Antolamenduko iruzkina
- Partehartzailentzat aula-zailtasuna murrizteko bertsioa/brancha zehaztuak mantentzea.

