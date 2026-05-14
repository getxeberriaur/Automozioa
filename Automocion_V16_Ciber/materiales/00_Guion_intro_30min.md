# Intro (30 min): Ciberseguridad en balizas de emergencia conectadas (V16)

[Bertsioa euskaraz](00_Guion_intro_30min_eu.md)

Material de apoyo de diapositivas: [00_Diapositivas_intro_30min.md](00_Diapositivas_intro_30min.md)

Versión proyector (castellano): [00_Diapositivas_intro_30min_proyector.md](00_Diapositivas_intro_30min_proyector.md)

Versión proyector (euskara): [00_Diapositivas_intro_30min_proyector_eu.md](00_Diapositivas_intro_30min_proyector_eu.md)

## 1) Objetivos de la mini-sesión
Al finalizar la introducción, el profesorado será capaz de:
- Explicar el papel de la baliza conectada en el ecosistema de tráfico inteligente.
- Identificar los activos críticos y la superficie de ataque.
- Relacionar riesgos técnicos con impacto en seguridad vial.
- Entender qué se va a validar en el laboratorio práctico (2h).

---

## 2) Estructura temporal (30 min)

### 0:00–0:03 | Apertura y contexto (3 min)
**Mensaje clave:** no es “solo IoT”; es un sistema ciberfísico con impacto directo en carretera.

Preguntas detonantes:
- ¿Qué pasa si una baliza reporta incidentes falsos?
- ¿Qué pasa si un incidente real no llega al backend?

### 0:03–0:10 | Arquitectura funcional simplificada (7 min)
Explicar con un diagrama simple:
1. Dispositivo V16 conectado (firmware + identidad)
2. Red móvil / transporte
3. Backend de recepción y validación
4. Integración con plataforma de tráfico
5. Consumo por terceros (paneles, apps, servicios)

**Activos críticos:**
- Claves/certificados
- Integridad del firmware
- Integridad y frescura del evento (timestamp/nonce)
- Disponibilidad del backend
- Trazabilidad de eventos

### 0:10–0:20 | Amenazas principales (10 min)
Usar STRIDE en versión docente:
- **S**uplantación: baliza falsa o identidad clonada.
- **T**ampering: modificación del evento en tránsito o en origen.
- **R**epudio: falta de evidencias de quién envió qué.
- **I**nformación: fuga de localización y metadatos.
- **D**enegación de servicio: saturación de API o bloqueo lógico.
- **E**levación: abuso de privilegios en backend o plataforma.

Impacto docente a remarcar:
- Seguridad vial (avisos erróneos / falta de aviso)
- Operación de tráfico (ruido y mala priorización)
- Cumplimiento normativo y reputación

### 0:20–0:26 | Controles esperables (6 min)
- Identidad fuerte del dispositivo.
- Firma/autenticación de mensajes.
- Protección anti-replay (nonce + ventana temporal).
- Cifrado en tránsito y validación estricta en backend.
- Logging y correlación para detección de anomalías.
- Revocación y respuesta ante incidente.

> **Conexión con el lab:** los controles de nonce (`nonce_cache`), ventana temporal (`TIMESTAMP_WINDOW_SECONDS = 30`) y rate limiting (`RATE_LIMIT_MAX_EVENTS = 5`) están implementados en el backend. Los participantes los verán funcionar — y los romperán cambiando los valores.

### 0:26–0:30 | Puente al laboratorio (4 min)
**Qué harán en 2h:**
1. Generar tráfico legítimo y observarlo en el panel visual y los logs.
2. Simular ataques de lógica (replay, timestamp manipulado, identidad falsa, ráfaga) en entorno controlado y anotar los códigos HTTP de respuesta.
3. **Hardening:** modificar parámetros del backend (`TIMESTAMP_WINDOW_SECONDS`, `RATE_LIMIT_MAX_EVENTS`) y medir el impacto directo — conectando la teoría de controles con líneas de código concretas.
4. Documentar evidencias y redactar conclusiones en la plantilla de informe.

> **Truco docente:** mostrar en pantalla el bloque de constantes de `backend/app.py` durante este puente. Los participantes verán que los controles que acabas de explicar son literalmente 4 líneas de código — desmitifica la seguridad y motiva el hardening.

---

## 3) Guion de diapositivas (10 diapositivas sugeridas)
1. Título y objetivo
2. Caso de uso real en carretera
3. Arquitectura extremo a extremo
4. Activos críticos
5. Amenazas principales
6. Matriz impacto/probabilidad (rápida)
7. Controles por capa
8. Qué mediremos en laboratorio
9. Riesgo residual y lecciones
10. Cierre + transición práctica

---

## 4) Mensajes docentes clave (para repetir)
- “No buscamos explotar sistemas reales; buscamos aprender a protegerlos.”
- “En automoción, la ciberseguridad se traduce en seguridad de personas.”
- “Sin evidencias (logs y trazabilidad), no hay respuesta efectiva.”

---

## 5) Mini-rúbrica de comprensión rápida (5 min opcional)
- ¿Sabe identificar 3 activos críticos? (Sí/No)
- ¿Diferencia spoofing de replay? (Sí/No)
- ¿Relaciona un control con una amenaza concreta? (Sí/No)
