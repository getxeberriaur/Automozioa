# Checklist de configuración del laboratorio (docente)

[Bertsioa euskaraz](02_Checklist_configuracion_laboratorio_eu.md)

## A) Requisitos previos (host)
- Sistema: **Ubuntu 22.04 LTS** (máquina virtual o física).
- Python 3.10+ instalado (`python3 --version`).
- `python3-venv` y `python3-pip` disponibles (`sudo apt install -y python3-venv python3-pip`).
- Editor (VS Code recomendado).
- Acceso local a terminal.
- Sin conexión a sistemas reales de tráfico.

## B) Preparación del entorno (por equipo)
1. Crear carpeta de laboratorio por equipo.
2. Crear entorno virtual: `python3 -m venv .venv`
3. Activar entorno: `source .venv/bin/activate`
4. Instalar dependencias: `pip install -r requirements.txt`
5. Verificar que el puerto 8080 está libre: `ss -tlnp | grep 8080`

## C) Componentes mínimos
- `backend/`: API de recepción de avisos V16 simulados.
- `simulator/`: emulador de baliza con escenarios de prueba.
- `logs/`: registro de decisiones (`accepted/rejected` + motivo).
- `reports/`: evidencias del equipo.
- Panel visual: `http://127.0.0.1:8080/aginte-panela`.

## D) Datos de prueba sugeridos
- 2 identidades válidas de baliza.
- 1 identidad inválida.
- Plantillas de eventos:
  - legítimo
  - replay
  - timestamp atrasado
  - coordenadas inválidas
  - ráfaga (burst)

## E) Validaciones mínimas en backend
- Esquema JSON obligatorio.
- Coordenadas en rango válido.
- `security.sent_at` dentro de ventana temporal.
- `security.nonce` no reutilizable.
- Control de tasa por identidad.

## F) Logging recomendado
Campos por aviso:
- `message_id`
- `device_id`
- `alert_id`
- `alert_type`
- `alert_status`
- `sent_at`
- `decision` (accepted/rejected)
- `reason`
- `source_ip`
- `received_at`

## G) Criterio de “laboratorio listo”
- Se recibe 1 evento legítimo y se marca como `accepted`.
- Se envía replay y se marca `rejected` con razón `replayed_nonce`.
- Se genera informe con al menos 3 evidencias.

## H) Plan de contingencia docente
Si falla el entorno de un equipo:
- Opción 1: usar instancia compartida de backup del docente.
- Opción 2: pasar a modo análisis sobre trazas pregrabadas.
- Opción 3: evaluación parcial centrada en modelado y mitigaciones.

## I) Seguridad y ética del laboratorio
- Solo sandbox local o red aislada.
- Prohibido escanear o probar infraestructuras externas.
- Objetivo formativo: defensa, hardening y detección.
