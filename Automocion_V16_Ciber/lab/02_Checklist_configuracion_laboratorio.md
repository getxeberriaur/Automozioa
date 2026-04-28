# Checklist de configuración del laboratorio (docente)

## A) Requisitos previos (host)
- Sistema: Windows 10/11, Linux o macOS.
- Python 3.11+ instalado.
- Editor (VS Code recomendado).
- Acceso local a terminal.
- Sin conexión a sistemas reales de tráfico.

## B) Preparación del entorno (por equipo)
1. Crear carpeta de laboratorio por equipo.
2. Crear entorno virtual de Python.
3. Instalar dependencias del backend y cliente de pruebas.
4. Verificar que el puerto del backend está libre.

## C) Componentes mínimos
- `backend/`: API de ingestión de eventos.
- `simulator/`: generador de eventos legítimos y de prueba.
- `logs/`: registro de decisiones (accepted/rejected + motivo).
- `reports/`: evidencias del equipo.

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
- Timestamp dentro de ventana temporal.
- Nonce no reutilizable.
- Control de tasa por identidad.

## F) Logging recomendado
Campos por evento:
- `event_id`
- `device_id`
- `timestamp`
- `decision` (accepted/rejected)
- `reason`
- `source_ip`
- `received_at`

## G) Criterio de “laboratorio listo”
- Se recibe 1 evento legítimo y se marca como `accepted`.
- Se envía replay y se marca `rejected` con razón explícita.
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
