# Práctica V2X — El cruce imposible

**Duración recomendada:** 90 minutos · **Modalidad:** parejas · **Entorno:** localhost

## Contexto

La flota `UrbanFleet` recibe mensajes de vehículos cercanos. Un receptor no puede confiar únicamente en que un mensaje tenga un formato correcto: debe comprobar quién lo envía, cuándo se generó, si ya se ha visto y si describe una situación físicamente posible.

En esta práctica el gateway representa el componente que recibe y filtra mensajes cooperativos antes de que otra parte de `UrbanFleet` los utilice. Se trabaja con una simulación HTTP en `127.0.0.1`: no hay radio V2X, vehículos reales ni infraestructura vial conectada. El objetivo es observar una decisión de confianza y justificarla con evidencias.

La comparación tiene dos niveles. El gateway **inseguro** conserva las validaciones básicas del mensaje, mientras que el gateway **protegido** añade identidad enrolada, firma HMAC de laboratorio, frescura mediante timestamp y secuencia, detección de replay y limitación de ráfagas. Una firma válida demuestra autenticidad e integridad del mensaje recibido, pero no demuestra por sí sola que sus coordenadas o velocidad sean verdaderas.

## Objetivos

1. Observar mensajes CAM y DENM.
2. Comparar un gateway inseguro con uno protegido.
3. Identificar replay, spoofing, antigüedad, datos imposibles y ráfagas.
4. Relacionar cada detección con una medida defensiva.

## Preparación

1. Comprueba que tienes Python 3.10 o posterior:

	```bash
	python --version
	```

2. Abre dos terminales en la raíz del repositorio `Automozioa`.
3. Usa la primera terminal para el gateway y la segunda para el generador de mensajes. Todos los comandos siguientes se ejecutan desde esa raíz.
4. No cambies el host ni utilices una dirección pública: la práctica debe permanecer limitada a `127.0.0.1`.

## Pasos de la práctica

### 1. Arrancar y verificar la línea base

En la primera terminal, inicia el gateway protegido:

```bash
python V2X_Simulacion_Ciber/scripts/v2x_gateway.py
```

Comprueba que aparece `Gateway V2X escuchando en http://127.0.0.1:8090 (protegido)`. En la segunda terminal ejecuta `legitimo` y registra la respuesta. Después reinicia el gateway para comenzar una sesión limpia y ejecuta:

```bash
python V2X_Simulacion_Ciber/scripts/send_v2x.py legitimo
python V2X_Simulacion_Ciber/scripts/send_v2x.py emergency
```

Registra el código HTTP, el estado (`accepted` o `rejected`) y los campos que diferencian un CAM normal de un DENM de emergencia. La respuesta esperada para cada mensaje, ejecutado en una sesión limpia, es `HTTP 202` con estado `accepted`.

### 2. Ejecutar los escenarios protegidos

Para obtener resultados comparables, reinicia el gateway protegido antes de cada escenario. Así se evita que el `sequence=1` usado por el generador sea interpretado como un replay de una ejecución anterior. En cada sesión, ejecuta uno de los comandos siguientes:

```bash
python V2X_Simulacion_Ciber/scripts/send_v2x.py replay
python V2X_Simulacion_Ciber/scripts/send_v2x.py spoof
python V2X_Simulacion_Ciber/scripts/send_v2x.py impossible
python V2X_Simulacion_Ciber/scripts/send_v2x.py old
python V2X_Simulacion_Ciber/scripts/send_v2x.py burst
```

Anota la respuesta HTTP y los motivos devueltos. `replay` envía dos veces el mismo mensaje; `spoof` usa un emisor no enrolado; `impossible` combina una velocidad y una latitud inválidas; `old` utiliza un timestamp de hace dos minutos; y `burst` envía 12 mensajes seguidos.

El gateway conserva las secuencias y los mensajes vistos durante su ejecución. Anota en el informe que cada escenario se ejecutó en una sesión limpia y conserva la salida del segundo envío de `replay`, que es el que debe mostrar el rechazo por repetición.

### 3. Repetir en modo inseguro

Detén el gateway y arráncalo así:

```bash
python V2X_Simulacion_Ciber/scripts/v2x_gateway.py --insecure
```

Reinicia el gateway inseguro antes de cada escenario y repite los comandos de la línea base y de los escenarios. Compara qué controles desaparecen y cuáles permanecen: incluso en modo inseguro, el gateway sigue comprobando el tipo de mensaje, los rangos de coordenadas, la velocidad, el rumbo y la antigüedad del timestamp.

### 4. Completar evidencias y análisis

Para cada ejecución, conserva la salida de la terminal o una captura donde se vea el comando y la respuesta HTTP. Después completa la tabla de comparación y el informe [`reports/00_Plantilla_informe.md`](../reports/00_Plantilla_informe.md). No basta con indicar que un mensaje fue rechazado: relaciona cada motivo con autenticidad, integridad, frescura, plausibilidad o disponibilidad.

### 5. Cerrar el laboratorio

Detén el gateway con `Ctrl+C`, verifica que no queda ningún proceso escuchando en el puerto 8090 y entrega el informe con las evidencias y tres medidas priorizadas para `UrbanFleet`.

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