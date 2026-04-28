# Arranque rápido del laboratorio

## 1) Crear y activar entorno virtual

### Windows PowerShell
1. `python -m venv .venv`
2. `.\.venv\Scripts\Activate.ps1`

## 2) Instalar dependencias

`pip install -r requirements.txt`

## 3) Levantar backend

`uvicorn backend.app:app --host 127.0.0.1 --port 8080 --reload`

## 4) Probar con el simulador

### Evento legítimo
`python simulator/send_event.py legitimo`

### Replay
`python simulator/send_event.py replay`

### Timestamp atrasado
`python simulator/send_event.py timestamp-atrasado`

### Coordenadas inválidas
`python simulator/send_event.py coordenadas-invalidas`

### Identidad inválida
`python simulator/send_event.py identidad-invalida`

### Ráfaga
`python simulator/send_event.py rafaga --count 8`

## 5) Revisar evidencias

- Log principal: `logs/events.log`
- Carpeta de informes: `reports/`
