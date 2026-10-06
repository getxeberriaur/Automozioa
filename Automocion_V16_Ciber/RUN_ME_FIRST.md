# Arranque rápido — Laboratorio V16

El laboratorio simula el envío de avisos V16 a una API local. Ejecuta los comandos desde `Automocion_V16_Ciber/`.

## 1. Preparar Python

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Linux o macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instala las dependencias:

```text
pip install -r requirements.txt
```

## 2. Iniciar el backend

```text
uvicorn backend.app:app --host 127.0.0.1 --port 8080
```

Abre `http://127.0.0.1:8080/docs` o `http://127.0.0.1:8080/aginte-panela`.

## 3. Ejecutar escenarios

En una segunda terminal, también desde `Automocion_V16_Ciber/`:

```text
python simulator/send_event.py legitimo
python simulator/send_event.py replay
python simulator/send_event.py timestamp-atrasado
python simulator/send_event.py coordenadas-invalidas
python simulator/send_event.py identidad-invalida
python simulator/send_event.py rafaga --count 8
```

## 4. Revisar y entregar evidencias

Consulta `logs/events.log`, el panel local y `http://127.0.0.1:8080/events/recent?limit=10`. Completa una de las plantillas de informe en `reports/`.

Todo el tráfico queda en `127.0.0.1`. No configures otro host ni conectes el laboratorio a servicios reales.
