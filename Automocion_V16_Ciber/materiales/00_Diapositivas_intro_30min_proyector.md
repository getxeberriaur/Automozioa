# Diapositivas intro (30 min) — Versión proyector (Castellano)

> Formato: contenido mínimo en pantalla + notas del ponente.

---

## Slide 1 — V16 conectada: ciberseguridad y seguridad vial
### Pantalla
- Ciberseguridad en balizas V16 conectadas
- Introducción + laboratorio práctico (2h)
- Defensa en entorno simulado

### Notas del ponente
- Enmarcar la sesión: no es explotación, es protección.
- Objetivo: entender riesgo y validar controles.

---

## Slide 2 — ¿Qué pasa cuando una baliza emite un aviso?
### Pantalla
- Baliza detecta incidencia
- Envía aviso a plataforma
- La plataforma decide: aceptar o rechazar

### Notas del ponente
- Pregunta al grupo: ¿qué pasa si se acepta un aviso falso?

---

## Slide 3 — Flujo extremo a extremo
### Pantalla
- Dispositivo V16
- Red de comunicaciones
- Backend receptor
- Plataforma / servicios de tráfico

### Notas del ponente
- Recalcar superficie de ataque en cada salto.

---

## Slide 4 — Activos críticos
### Pantalla
- Identidad del dispositivo
- Integridad del aviso
- Frescura temporal
- Disponibilidad del backend
- Trazabilidad

### Notas del ponente
- Sin trazabilidad no hay respuesta de incidente.

---

## Slide 5 — Amenazas clave
### Pantalla
- Suplantación
- Replay
- Datos fuera de rango
- Ráfaga / abuso de API

### Notas del ponente
- Conectar cada amenaza con impacto operativo real.

---

## Slide 6 — Priorización rápida (impacto vs probabilidad)
### Pantalla
- Alta prioridad: replay, suplantación, ráfaga
- Prioridad media: timestamp/coords inválidas

### Notas del ponente
- Introducir criterio de priorización defensiva.

---

## Slide 7 — Controles defensivos del backend
### Pantalla
- Esquema JSON estricto
- Ventana temporal (`security.sent_at`)
- Anti-replay (`security.nonce`)
- Rate limiting por identidad
- Logging con `reason`

### Notas del ponente
- Mostrar que son controles ya implementados en el laboratorio.

---

## Slide 8 — Qué medimos en la práctica
### Pantalla
- Tasa de aceptación de inválidos
- Calidad de rechazo con motivo
- Evidencia técnica trazable

### Notas del ponente
- Referencias visuales:
  - Panel: http://127.0.0.1:8080/aginte-panela
  - JSON: http://127.0.0.1:8080/events/recent?limit=10

---

## Slide 9 — Riesgo residual
### Pantalla
- Aún faltan controles de nivel producción
- Firma, PKI, mTLS, SOC

### Notas del ponente
- Explicar que el laboratorio es base funcional realista, no entorno final.

---

## Slide 10 — Transición al laboratorio
### Pantalla
- 1) Aviso legítimo
- 2) Replay e inválidos
- 3) Observación en panel/log
- 4) Informe de evidencias

### Notas del ponente
- Regla de oro: solo sandbox local o red aislada.
