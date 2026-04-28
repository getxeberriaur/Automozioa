# Setup rápido del laboratorio en Windows (referencia docente)

[Bertsioa euskaraz](03_Setup_rapido_windows_eu.md)

## Opción recomendada: stack Python local (simple)

### 1) Crear entorno virtual
- Abrir terminal en la carpeta del laboratorio.
- Crear venv.
- Activar venv.

### 2) Instalar dependencias mínimas
Paquetes sugeridos:
- fastapi
- uvicorn
- pydantic
- requests
- python-dateutil

### 3) Estructura mínima
- `backend/app.py`
- `simulator/send_event.py`
- `logs/events.log`
- `reports/`

### 4) Comprobación funcional
- Iniciar backend en puerto local (ej. 8080).
- Enviar un evento legítimo desde simulador.
- Confirmar `accepted` en logs.

### 5) Pruebas de seguridad
- Reenvío del mismo payload (replay).
- Timestamp fuera de ventana.
- Coordenadas inválidas.
- Ráfaga de eventos.

### 6) Criterios de éxito
- Backend rechaza replay y eventos fuera de política.
- Cada rechazo queda documentado con `reason`.
- Equipo entrega evidencias en `reports/`.

---

## Opción alternativa: Docker (si el centro ya lo usa)
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
