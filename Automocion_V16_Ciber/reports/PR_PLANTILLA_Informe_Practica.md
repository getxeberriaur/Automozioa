# Informe de Práctica — Simulador Baliza V16 ✅ VERSIÓN PROFESOR
**CVE-2025-65855 · Help Flash IoT · Análisis de Vulnerabilidades**

> ⚠️ **USO EXCLUSIVO DEL DOCENTE — NO DISTRIBUIR A LOS PARTICIPANTES**

---

## Datos del participante

| Campo | Valor |
|-------|-------|
| **Nombre y apellidos** | *(rellenar por el participante)* |
| **Fecha** | *(rellenar por el participante)* |
| **Módulo / Curso** | Ciberseguridad en Automoción |
| **Entorno de trabajo** | Ubuntu 22 |

---

## Parte 1 — Reconocimiento del entorno ✅

### 1.1 ¿Qué endpoints expone el backend?

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/evento` | POST | Recibe eventos de la baliza (posición GPS, timestamp, ID) |
| `/health` | GET | Comprueba que el servidor está activo |
| `/eventos` | GET | Lista los eventos registrados |

> ✅ **Corrección**: Se aceptan los tres endpoints. Si el participante solo identifica `/evento` se considera correcto parcialmente. Penalizar si no identifica el endpoint principal.

---

### 1.2 ¿Qué campos contiene el evento legítimo?

```json
{
  "device_id": "HF-IoT-TEST-001",
  "timestamp": "2026-05-26T10:00:00Z",
  "lat": 43.2627,
  "lon": -2.9253,
  "speed": 0.0,
  "battery": 85
}
```

> ✅ **Corrección**: Campos mínimos aceptables: `device_id`, `timestamp`, `lat`, `lon`. Los campos `speed` y `battery` son opcionales. Penalizar si falta `timestamp` o `device_id`.

---

### 1.3 ¿Qué respuesta devuelve el backend ante un evento legítimo?

```json
{
  "status": "ok",
  "message": "Evento registrado correctamente",
  "event_id": "uuid-generado"
}
```
**Código HTTP: 200 OK**

> ✅ **Corrección**: Aceptar cualquier descripción que mencione código 200 y que el evento se acepta.

---

## Parte 2 — Escenarios de ataque ✅

### 2.1 Replay Attack

| Campo | Valor |
|-------|-------|
| **Comando ejecutado** | `python3 simulator/send_event.py replay` |
| **Respuesta del servidor** | `{"status": "error", "message": "Evento duplicado detectado"}` |
| **Código HTTP** | `409 Conflict` |
| **¿El ataque tuvo éxito?** | ❌ No |
| **¿Por qué?** | El backend almacena un hash de cada evento recibido. Si el mismo evento se envía dos veces, detecta la colisión y lo rechaza. |

> ✅ **Corrección**: El participante debe identificar que el servidor usa algún mecanismo de detección de duplicados (hash, UUID, nonce). Aceptar cualquier explicación técnicamente correcta.
> ⚠️ **Error común**: Confundir el rechazo por timestamp con el rechazo por replay. Son mecanismos diferentes.

---

### 2.2 Timestamp atrasado

| Campo | Valor |
|-------|-------|
| **Comando ejecutado** | `python3 simulator/send_event.py timestamp-atrasado` |
| **Respuesta del servidor** | `{"status": "error", "message": "Timestamp fuera de ventana permitida"}` |
| **Código HTTP** | `400 Bad Request` |
| **¿El ataque tuvo éxito?** | ❌ No |
| **¿Por qué?** | El backend compara el timestamp del evento con la hora actual del servidor. Si la diferencia supera 120 segundos (2 minutos), rechaza el evento. Esto previene ataques de replay con eventos capturados anteriormente. |

> ✅ **Corrección**: El participante debe mencionar la "ventana de tiempo" o "tiempo máximo de desfase". La ventana exacta es de 120 segundos — no es necesario que la conozcan, pero sí el concepto.

---

### 2.3 Coordenadas inválidas

| Campo | Valor |
|-------|-------|
| **Comando ejecutado** | `python3 simulator/send_event.py coordenadas-invalidas` |
| **Respuesta del servidor** | `{"status": "error", "message": "Coordenadas GPS fuera de rango"}` |
| **Código HTTP** | `422 Unprocessable Entity` |
| **¿El ataque tuvo éxito?** | ❌ No |
| **¿Por qué?** | El backend valida que la latitud esté entre -90 y +90 grados y la longitud entre -180 y +180 grados. El simulador envía latitud 123°, que es físicamente imposible. |

> ✅ **Corrección**: Aceptar si menciona validación de rango de coordenadas. Valorar positivamente si explica que esto previene falsificación de posición GPS (GPS spoofing).

---

### 2.4 Identidad inválida

| Campo | Valor |
|-------|-------|
| **Comando ejecutado** | `python3 simulator/send_event.py identidad-invalida` |
| **Respuesta del servidor** | `{"status": "error", "message": "Dispositivo no registrado"}` |
| **Código HTTP** | `401 Unauthorized` |
| **¿El ataque tuvo éxito?** | ❌ No |
| **¿Por qué?** | El backend mantiene una lista blanca de `device_id` autorizados. Un ID desconocido es rechazado inmediatamente sin procesar el evento. |

> ✅ **Corrección**: El participante debe identificar el concepto de lista blanca (whitelist) o autenticación por ID. Valorar si menciona que esto simula lo que falla en la baliza real (sin autenticación en el OTA).

---

### 2.5 Ráfaga (Rate Limiting)

| Campo | Valor |
|-------|-------|
| **Comando ejecutado** | `python3 simulator/send_event.py rafaga --count 10` |
| **¿A partir de qué petición empezó a rechazar?** | A partir de la petición número 6 |
| **Código HTTP de rechazo** | `429 Too Many Requests` |
| **Conclusión** | El backend limita a 5 peticiones por dispositivo en una ventana de 60 segundos. A partir de la 6ª petición devuelve 429 hasta que la ventana se reinicia. |

> ✅ **Corrección**: El número exacto (5 o 6) puede variar según la implementación. Aceptar si el participante identifica correctamente el código 429 y el concepto de rate limiting.
> ⚠️ **Error común**: Confundir el límite por dispositivo con un límite global del servidor.

---

## Parte 3 — Análisis del backend ✅

### 3.1 ¿Qué validaciones implementa el backend?

| Validación | ¿Implementada? | Código/línea donde se valida |
|------------|---------------|------------------------------|
| Verificación de timestamp | ✅ Sí | `backend/app.py` → función `validar_timestamp()` |
| Detección de replay | ✅ Sí | `backend/app.py` → set `eventos_vistos` con hash SHA256 |
| Validación de coordenadas GPS | ✅ Sí | `backend/app.py` → función `validar_coordenadas()` |
| Autenticación del dispositivo | ✅ Sí | `backend/app.py` → lista `DISPOSITIVOS_AUTORIZADOS` |
| Rate limiting | ✅ Sí | `backend/app.py` → decorador `@limiter` con SlowAPI |

> ✅ **Corrección**: Aceptar si el participante identifica al menos 4 de las 5 validaciones. No es necesario que indiquen la línea exacta, pero sí el mecanismo.

---

### 3.2 ¿Qué vulnerabilidades has identificado que NO están mitigadas?

1. **Sin cifrado en tránsito**: El backend usa HTTP plano, no HTTPS. Las comunicaciones pueden ser interceptadas y leídas en texto claro.
2. **Sin firma digital de los eventos**: Los eventos no llevan firma criptográfica. Un atacante que conozca el formato puede fabricar eventos falsos con un `device_id` válido.
3. **Lista blanca estática**: Los `device_id` autorizados están hardcodeados en el código. No hay rotación de credenciales ni revocación de dispositivos comprometidos.

> ✅ **Corrección**: Se aceptan estas tres o cualquier combinación de vulnerabilidades reales identificadas en el código. Valorar especialmente si mencionan la falta de HTTPS o la ausencia de firma criptográfica.
> ⚠️ **No aceptar**: Vulnerabilidades inventadas que no existen en el código.

---

### 3.3 Log de la evidencia más relevante

```
INFO:     127.0.0.1:52341 - "POST /evento HTTP/1.1" 200 OK
INFO:     127.0.0.1:52342 - "POST /evento HTTP/1.1" 409 Conflict  ← replay detectado
INFO:     127.0.0.1:52343 - "POST /evento HTTP/1.1" 400 Bad Request ← timestamp inválido
INFO:     127.0.0.1:52344 - "POST /evento HTTP/1.1" 422 Unprocessable Entity ← GPS inválido
INFO:     127.0.0.1:52345 - "POST /evento HTTP/1.1" 401 Unauthorized ← ID desconocido
INFO:     127.0.0.1:52350 - "POST /evento HTTP/1.1" 429 Too Many Requests ← rate limit
```

> ✅ **Corrección**: El participante debe mostrar al menos 3 respuestas distintas del servidor que evidencien los ataques ejecutados. Penalizar si el log está vacío.

---

## Parte 4 — Propuestas de mejora ✅

### 4.1 ¿Cómo mejorarías la seguridad del backend?

| Vulnerabilidad identificada | Mejora propuesta |
|----------------------------|-----------------|
| HTTP sin cifrar | Implementar TLS/HTTPS con certificado válido |
| Sin firma de eventos | Añadir firma HMAC-SHA256 con clave compartida por dispositivo |
| Lista blanca estática | Sistema de registro dinámico con tokens renovables |
| Rate limiting por IP | Rate limiting por `device_id` + bloqueo temporal ante anomalías |
| Sin auditoría | Log de seguridad persistente con alertas ante patrones de ataque |

> ✅ **Corrección**: Se aceptan al menos 3 propuestas coherentes con las vulnerabilidades identificadas. Valorar propuestas que mencionen estándares (TLS, HMAC, OAuth).

---

### 4.2 ¿Qué cambios harías en el protocolo de comunicación baliza → servidor?

1. **Cifrado extremo a extremo**: TLS 1.3 obligatorio en todas las comunicaciones, con certificado de cliente para autenticar el dispositivo.
2. **Firma criptográfica de cada mensaje**: Cada evento firmado con ECDSA usando una clave privada almacenada en el secure element del dispositivo.
3. **Nonce + timestamp combinados**: Cada mensaje incluye un nonce único generado por el servidor en el handshake inicial, imposibilitando los replay attacks aunque se capture el tráfico.

> ✅ **Corrección**: Aceptar cualquier propuesta técnicamente sólida. Valorar especialmente si mencionan secure element, PKI o mutual TLS.

---

## Parte 5 — Reflexión final ✅

### 5.1 ¿Qué impacto real tendría explotar estas vulnerabilidades en producción?

> **Respuesta modelo:**
> En un sistema de producción real con más de 250.000 balizas V16 IoT desplegadas en España, la explotación de estas vulnerabilidades tendría consecuencias graves. Un atacante podría falsificar la posición GPS de cientos de balizas simultáneamente, enviando coordenadas falsas a la DGT y generando alertas de accidente inexistentes en tramos de autopista vacíos. Esto saturaría los centros de control y podría desviar recursos de emergencia reales hacia ubicaciones falsas. Adicionalmente, un ataque de replay masivo podría colapsar el backend con eventos duplicados, dejando fuera de servicio el sistema de notificación a conductores. La falta de autenticación robusta también permitiría registrar balizas falsas que nunca se activarían en caso de emergencia real, comprometiendo la seguridad vial de los usuarios que confían en el sistema.

> ✅ **Corrección**: La respuesta debe mencionar al menos: impacto en la seguridad vial, posible saturación del sistema, y consecuencias para los servicios de emergencia. Penalizar respuestas de menos de 3 líneas o que no conecten la vulnerabilidad técnica con el impacto real.

---

### 5.2 ¿Qué relación tiene esta práctica con la normativa UNECE R155?

> **Respuesta modelo:**
> La normativa UNECE R155 obliga a los fabricantes de vehículos y sistemas conectados a implementar un Sistema de Gestión de Ciberseguridad (CSMS) que cubra todo el ciclo de vida del producto, incluyendo la identificación de amenazas, la implementación de contramedidas y la respuesta ante incidentes. Las vulnerabilidades demostradas en esta práctica (falta de autenticación, ausencia de cifrado, sin validación de integridad) son exactamente el tipo de fallos que R155 exige detectar y mitigar en la fase de análisis de riesgos (TARA — Threat Analysis and Risk Assessment). Un sistema de baliza V16 IoT que comunica con infraestructura de la DGT entraría en el ámbito de aplicación de R155 como sistema de seguridad vial conectado, y el fabricante (Netun Solutions) estaría obligado a corregir estas vulnerabilidades antes de la homologación del vehículo o sistema en el que se integre.

> ✅ **Corrección**: La respuesta debe mencionar UNECE R155, CSMS y/o TARA. Valorar si conectan correctamente la práctica técnica con el marco regulatorio. Aceptar respuestas más cortas si son precisas.

---

## Checklist de corrección del docente

- [ ] Parte 1 completa — endpoints y JSON identificados correctamente
- [ ] Parte 2 — los 5 escenarios ejecutados con códigos HTTP correctos
- [ ] Parte 3 — al menos 4 validaciones identificadas + 2 vulnerabilidades no mitigadas
- [ ] Parte 4 — al menos 3 propuestas de mejora coherentes
- [ ] Parte 5 — reflexión conecta técnica con impacto real y R155
- [ ] Log de evidencias adjunto o pegado

### Criterio de evaluación orientativo

| Puntuación | Criterio |
|------------|---------|
| **Excelente** | Todas las partes completas, vulnerabilidades correctamente identificadas, propuestas técnicamente sólidas, reflexión conecta con R155 |
| **Correcto** | Al menos 4/5 partes completas, errores menores en códigos HTTP o nombres de mecanismos |
| **Incompleto** | Menos de 3 partes completas o escenarios sin ejecutar |
| **No apto** | Parte 2 vacía (escenarios no ejecutados) o copia literal de otro participante |

---
*Versión profesor — Curso de Ciberseguridad en Automoción — Automozioa*