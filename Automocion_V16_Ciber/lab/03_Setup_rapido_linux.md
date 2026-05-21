# Setup rápido del laboratorio en Linux / Ubuntu 22
(referencia docente)

[Bertsioa euskaraz](03_Setup_rapido_linux_eu.md)

## Opción recomendada: stack Python local (simple)

### 1) Requisitos previos del sistema

```bash
# Verificar Python (necesario 3.10+)
python3 --version

# Instalar pip y venv si no están disponibles
sudo apt update
sudo apt install -y python3-pip python3-venv
```

### 2) Crear y activar entorno virtual

```bash
# Desde la carpeta del laboratorio
python3 -m venv .venv
source .venv/bin/activate
```

> El prompt del terminal mostrará `(.venv)` cuando esté activo.

### 3) Instalar dependencias mínimas

```bash
pip install -r requirements.txt
```

Paquetes instalados:
- `fastapi` — framework API
- `uvicorn` — servidor ASGI
- `pydantic` — validación de datos
- `requests` — cliente HTTP para el simulador

### 4) Estructura mínima del laboratorio
- `backend/app.py`
- `simulator/send_event.py`
- `samples/event_legitimo.json`
- `logs/events.log`
- `reports/`
- `RUN_ME_FIRST.md`

### 5) Arrancar el backend

```bash
uvicorn backend.app:app --host 127.0.0.1 --port 8080 --reload
```

### 6) Comprobación funcional

```bash
# En otra terminal (con .venv activado)
python3 simulator/send_event.py legitimo
```

Verificar:
- Respuesta `accepted` en terminal.
- Entrada en `logs/events.log`.
- Panel visual: `http://127.0.0.1:8080/aginte-panela`.

### 7) Pruebas de seguridad

```bash
python3 simulator/send_event.py replay
python3 simulator/send_event.py timestamp-atrasado
python3 simulator/send_event.py coordenadas-invalidas
python3 simulator/send_event.py rafaga --count 8
```

### 8) Criterios de éxito
- Backend rechaza replay y eventos fuera de política.
- Cada rechazo queda documentado con `reason`.
- El panel `/aginte-panela` refleja aceptaciones y rechazos.
- Equipo entrega evidencias en `reports/`.

---

## Opción alternativa: Docker (si el centro ya lo usa)

```bash
# Verificar Docker
docker --version
docker compose version

# Arrancar
docker compose up
```

Componentes:
- Servicio `api` (FastAPI)
- Servicio `simulator`
- Volumen para `logs`

Ventajas:
- Menor variabilidad entre equipos.
- Recuperación rápida ante fallos de entorno.

Riesgo:
- Si Docker falla en aula, usar plan B con stack Python local.

---

## Buenas prácticas docentes de operación
- Preparar una instancia de respaldo ejecutándose antes de la sesión.
- Tener trazas pregrabadas para evaluación si un equipo se bloquea.
- Cerrar con comparación antes/después y lecciones transferibles a otros sistemas ITS.
