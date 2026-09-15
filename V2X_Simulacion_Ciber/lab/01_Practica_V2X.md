# Práctica V2X — El cruce imposible

**Duración recomendada:** 90 minutos · **Modalidad:** parejas · **Entorno:** localhost

## Contexto

La flota `UrbanFleet` recibe mensajes de vehículos cercanos. Un receptor no puede confiar únicamente en que un mensaje tenga un formato correcto: debe comprobar quién lo envía, cuándo se generó, si ya se ha visto y si describe una situación físicamente posible.

## Objetivos

1. Observar mensajes CAM y DENM.
2. Comparar un gateway inseguro con uno protegido.
3. Identificar replay, spoofing, antigüedad, datos imposibles y ráfagas.
4. Relacionar cada detección con una medida defensiva.

## Desarrollo

### Fase A — Línea base

Arranca el gateway protegido y envía `legitimo` y `emergency`. Anota qué campos cambian y qué decisión produce el gateway.

### Fase B — Comparación vulnerable/protegida

Repite `replay`, `spoof`, `impossible`, `old` y `burst` con `--insecure` y sin él. Completa:

| Escenario | Inseguro | Protegido | Control que marca la diferencia |
|---|---|---|---|
| Replay | | | |
| Emisor no registrado | | | |
| Velocidad/posición imposible | | | |
| Timestamp antiguo | | | |
| Ráfaga | | | |

### Fase C — Análisis

Para cada rechazo, identifica la propiedad afectada:

- **Autenticidad:** ¿el emisor está enrolado?
- **Integridad:** ¿la firma coincide con el contenido?
- **Frescura:** ¿el timestamp y la secuencia son nuevos?
- **Plausibilidad:** ¿la situación puede ocurrir físicamente?
- **Disponibilidad:** ¿la ráfaga impide procesar mensajes?

### Fase D — Informe

Entrega [`reports/00_Plantilla_informe.md`](../reports/00_Plantilla_informe.md) con capturas o copia de las respuestas HTTP y una recomendación para `UrbanFleet`.

## Extensión docente

Cambiad el `sender_id`, las coordenadas, la velocidad o el tipo de mensaje en `send_v2x.py` y predicid el resultado antes de ejecutarlo. La firma HMAC se invalida al modificar un mensaje firmado, lo que permite separar la autenticidad criptográfica de la plausibilidad del contenido.

## Límites de seguridad

La práctica no debe trasladarse a frecuencias V2X reales, carreteras, vehículos, semáforos ni certificados de producción. Para estudiar RF, apertura keyless y TPMS se utilizan exclusivamente los procedimientos aislados de `RF_Lab_Seguro/` y sus materiales específicos.