# Laboratorio práctico (2h): Seguridad de avisos V16 en entorno simulado

[Bertsioa euskaraz](01_Laboratorio_2h_eu.md)

## 1) Objetivo
Validar cómo cambian los resultados de seguridad cuando el backend **no** tiene controles robustos frente a cuando sí los tiene.

> Importante: laboratorio totalmente simulado y aislado de sistemas reales de tráfico.

---

## 2) Resultado de aprendizaje
Al finalizar, cada equipo podrá:
- Detectar vulnerabilidades lógicas en envío de avisos V16.
- Ejecutar pruebas controladas de replay/inyección en sandbox.
- Implementar mitigaciones básicas y comprobar su eficacia.
- Presentar evidencias (capturas, logs, conclusiones).

---

## 3) Agenda detallada (120 min)

### Fase A — Preparación y baseline (0–25 min)
- Levantar entorno local.
- Enviar avisos legítimos desde el emulador.
- Revisar panel visual `/aginte-panela` y logs del backend.

**Entregable A:** 1 captura de evento legítimo y latencia observada.

### Fase B — Ataque controlado (25–55 min)
- Escenario 1: replay de evento válido.
- Escenario 2: inyección de evento malformado/fuera de rango.

**Entregable B:** evidencias de aceptación indebida (si ocurre) y explicación.

### Fase C — Hardening (55–95 min)
Activar/validar controles:
- `security.nonce` único por aviso
- Ventana temporal (ej. ±30 s)
- Validaciones estrictas de esquema y coordenadas
- Rate limiting por identidad

**Entregable C:** tabla antes/después con éxito/fracaso de ataques.

### Fase D — Detección y cierre (95–120 min)
- Revisar logs y alertas.
- Documentar IOCs simples (patrones de replay, bursts, coordenadas imposibles).
- Presentación corta por equipo (3 min).

**Entregable D:** mini informe técnico (1 página).

---

## 4) Arquitectura mínima del laboratorio
- **Emulador de baliza** (script cliente)
- **API de recepción de avisos** (backend local)
- **Almacenamiento de eventos** (JSON/SQLite)
- **Consola de observación** (`/aginte-panela` + `/events/recent` + logs)

Flujo:
1. Emulador genera aviso V16 (device/alert/location/security).
2. API valida identidad, `security.sent_at`, `security.nonce` y formato.
3. API acepta o rechaza.
4. Logs registran decisión y motivo.

---

## 5) Casos de prueba obligatorios
1. Evento legítimo con firma/credenciales válidas.
2. Replay exacto del mismo evento.
3. Evento con timestamp antiguo.
4. Evento con coordenadas fuera de rango.
5. Ráfaga de eventos para probar rate limiting.

---

## 6) Métricas de evaluación
- Tasa de aceptación de eventos inválidos (debe tender a 0).
- Tasa de falsos positivos sobre eventos legítimos.
- Tiempo de detección de anomalía.
- Calidad de evidencias y trazabilidad.

---

## 7) Rúbrica rápida (10 puntos)
- 3 pt: ejecución técnica del baseline y ataques
- 3 pt: implementación/validación de controles
- 2 pt: detección y análisis de logs
- 2 pt: claridad del informe y recomendaciones

---

## 8) Debrief final (preguntas guía)
- ¿Qué control evitó más ataques con menor coste?
- ¿Qué riesgo residual permanece?
- ¿Qué añadiríais para entorno productivo (PKI, OTA, SOC, respuesta)?
