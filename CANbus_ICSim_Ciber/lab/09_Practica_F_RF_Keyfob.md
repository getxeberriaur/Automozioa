# Práctica F — Captura y relay attack de señal RF de keyfob

[Bertsioa euskaraz](09_Practica_F_RF_Keyfob_eu.md)

**Duración estimada:** 50 minutos  
**Dificultad:** Media-Alta  
**Herramientas:** RTL-SDR, `rtl_433`, Universal Radio Hacker (URH), `rpitx` o segundo SDR (relay)

---

## Objetivo

Capturar la señal de radiofrecuencia emitida por el mando de un vehículo (keyfob) usando un receptor SDR de bajo coste, analizar su estructura, y comprender por qué los ataques de relay son el método de robo de vehículos más extendido actualmente — sin necesidad de acceder al bus CAN ni al puerto OBD-II.

---

## Contexto

El vector de ataque más utilizado por el crimen organizado para robar vehículos de gama media-alta no es el CAN bus — es la **extensión de la señal RF del keyfob**. No requiere acceso físico al coche ni conocimiento del protocolo CAN. Solo necesita estar cerca del propietario y del vehículo.

### ¿Por qué funciona?

Los sistemas de entrada sin llave (*keyless entry / passive entry*) funcionan así:

```
[Coche emite señal LF 125 kHz] → [Keyfob responde en UHF 433/868 MHz]
         ↑                                      ↓
   "¿Hay un keyfob cerca?"           "Sí, soy el keyfob autorizado"
         ↑                                      ↓
              [Coche desbloquea y permite arranque]
```

El relay attack **no descifra ni clona** el código — simplemente **extiende la distancia** de la comunicación:

```
[Coche] ←—LF—→ [Relay B junto al coche] ~~~cable/RF~~~ [Relay A junto al propietario] ←—LF—→ [Keyfob en bolsillo]
```

El coche cree que el keyfob está a 1 metro. En realidad puede estar a 100 metros o en otra planta del edificio.

### Rolling codes — por qué el simple replay no funciona

Los mandos modernos usan **rolling codes (KeeLoq, AUT64, Hitag2...)**:
- Cada pulsación genera un código diferente.
- El código anterior ya no es válido.
- Un código capturado y reproducido días después → el coche lo rechaza.

**El relay attack sí funciona** porque no replica el código: retransmite la señal en tiempo real. El keyfob genera el código legítimo respondiendo a la señal del coche.

> ⚠️ **Aviso legal:**
> - Esta práctica se realiza únicamente sobre vehículo propio o con autorización expresa.
> - Interceptar comunicaciones de terceros sin autorización es delito (Art. 197 CP).
> - El objetivo es comprender el ataque para poder implementar contramedidas.
> - No retransmitir señales sobre vehículos ajenos en ningún caso.

---

## Hardware necesario

| Dispositivo | Precio aprox. | Función |
|---|---|---|
| **RTL-SDR v3** (o RTL-SDR Blog v4) | ~25–35€ | Receptor SDR — captura señal keyfob |
| Antena 433/868 MHz (incluida con RTL-SDR) | — | Recepción |
| Segundo RTL-SDR o **HackRF One** | ~25€ / ~330€ | Retransmisión (relay) — opcional |
| Portátil Linux | — | Con USB disponible |

> Para la demo de captura y análisis basta con **un solo RTL-SDR** (~25€).  
> Para la demo de relay completo se necesita capacidad de transmisión: HackRF, YARD Stick One (~100€) o una Raspberry Pi con `rpitx`.

---

## Instalación de herramientas

```bash
# RTL-SDR drivers
sudo apt install -y rtl-sdr librtlsdr-dev

# rtl_433 — decodificador automático de protocolos RF
sudo apt install -y rtl_433
# o compilar desde fuente para la versión más reciente:
# git clone https://github.com/merbanan/rtl_433 && cd rtl_433 && mkdir build && cd build && cmake .. && make && sudo make install

# Universal Radio Hacker (URH) — análisis visual de señales RF
pip3 install urh
# o con GUI completa:
sudo apt install -y python3-pyqt5
pip3 install urh

# GNU Radio (opcional — análisis avanzado)
sudo apt install -y gnuradio
```

---

## Ejercicio F.1 — Verificar la recepción con RTL-SDR

### Detectar el adaptador

```bash
rtl_test -t
# Debe mostrar: Found 1 device(s)
```

### Escanear actividad en 433 MHz

```bash
# Escuchar en 433.92 MHz (frecuencia estándar europea de keyfobs)
rtl_433 -f 433920000 -A

# Con más detalle:
rtl_433 -f 433920000 -A -R 0 -v
```

Pulsar el botón del mando del coche — debe aparecer algo similar a:
```
time      : 2026-05-19 10:23:45
model     : Generic-Remote  id: 0xA3F2
data      : aa bb cc dd
```

> Si no detecta nada en 433.92 MHz, probar **868.35 MHz** (frecuencia alternativa en Europa):
> ```bash
> rtl_433 -f 868350000 -A
> ```

---

## Ejercicio F.2 — Captura y análisis en URH

### Capturar la señal raw

```bash
# Capturar 5 segundos de señal alrededor de 433.92 MHz
rtl_sdr -f 433920000 -s 250000 -n 1250000 captura_keyfob.cu8
```

Pulsar el botón del mando **2-3 veces** durante la captura.

### Abrir en URH

```bash
urh captura_keyfob.cu8
```

En URH:
1. **File → Open** → seleccionar `captura_keyfob.cu8`
2. Ajustar el **Sample Rate** a `250000`
3. Identificar los pulsos — cada pulsación del mando es una ráfaga de señal
4. Usar **Analysis → Assign Labels** para marcar preámbulo, datos y CRC
5. Comparar las ráfagas de **dos pulsaciones distintas** — los datos cambian (rolling code)

### Qué observar

| Elemento | Descripción |
|---|---|
| **Modulación** | ASK/OOK en la mayoría de keyfobs baratos; FSK en algunos modernos |
| **Frecuencia de portadora** | 433.92 MHz o 868.35 MHz |
| **Longitud del mensaje** | 32–64 bits típico (KeeLoq: 66 bits) |
| **Rolling code** | Los últimos N bits cambian en cada pulsación |
| **Preámbulo fijo** | Los primeros bits son iguales en todas las pulsaciones |

---

## Ejercicio F.3 — Demostración del relay attack (conceptual)

> Este ejercicio explica el ataque y lo simula conceptualmente. La retransmisión real requiere hardware de transmisión (HackRF / YARD Stick One).

### Diagrama del ataque

```
Escenario real de robo:

  [Propietario en casa]          [Coche en garaje / parking]
       keyfob en bolsillo              coche con keyless entry

  [Ladrón A — cerca del propietario]    [Ladrón B — junto al coche]
       Antena LF + receptor            Transmisor LF + antena UHF

  Ladrón B activa señal LF → keyfob responde en UHF →
  Ladrón A captura UHF → retransmite a Ladrón B →
  Ladrón B reenvía al coche → coche desbloquea y permite arranque
```

### Tiempo necesario para el ataque real: < 30 segundos

### Con hardware de transmisión (HackRF o YARD Stick One)

```bash
# Capturar la señal con RTL-SDR
rtl_sdr -f 433920000 -s 250000 -n 1250000 relay_capture.cu8

# Retransmitir inmediatamente con HackRF
hackrf_transfer -t relay_capture.cu8 -f 433920000 -s 2000000 -x 20
```

> El relay en tiempo real requiere latencia < 8ms. En la práctica se usan dispositivos hardware especializados (relay boxes comerciales, ~100-300€) que hacen esto automáticamente.

---

## Ejercicio F.4 — Captura RollJam (ataque avanzado — solo demo teórica)

> El **RollJam** (Samy Kamkar, DEF CON 2015) es un ataque que sí captura un código válido para uso posterior.

### Cómo funciona

```
Pulsación 1:
  [Keyfob envía código N]
  [Atacante: bloquea la señal (jammer) + captura código N]
  [Coche no recibe nada → propietario vuelve a pulsar]

Pulsación 2:
  [Keyfob envía código N+1]
  [Atacante: bloquea señal N+1 + captura N+1 + RETRANSMITE código N]
  [Coche recibe código N → se desbloquea]
  [Atacante tiene código N+1 guardado → válido para uso futuro]
```

El atacante se queda con un código válido no usado. El propietario no nota nada.

### Hardware necesario para RollJam

- **YARD Stick One** (~100€) — transmisor/receptor en la misma banda
- O **HackRF One** (~330€) con GNU Radio

> Esta técnica funciona en vehículos con sistemas KeeLoq clásico. Los sistemas modernos con **Ultrawideband (UWB)** (Apple CarKey, nuevos BMW/Audi/Tesla) son resistentes a relay attacks.

---

## Contramedidas — qué pueden hacer los fabricantes y propietarios

| Contramedida | Efectividad | Coste |
|---|---|---|
| **Guardar keyfob en bolsa Faraday** | Alta — bloquea señal LF | ~5€ |
| **Desactivar keyless entry** (algunos modelos permiten) | Alta | Gratis |
| **UWB (Ultra-Wideband)** — mide distancia precisa | Muy alta — imposibilita relay | Hardware nuevo |
| **Inmovilizador PIN** adicional | Alta | Variable |
| **Sensor de movimiento en keyfob** | Media — desactiva si está quieto | Algunos modelos modernos |

---

## Comparativa de vectores de ataque sobre vehículos

| Vector | Requiere acceso físico | Funciona en movimiento | Dificultad | Hardware |
|---|---|---|---|---|
| Inyección CAN (OBD-II) | Sí — al coche | No | Media | ~25€ |
| Replay CAN (puertas) | Sí — al coche | No | Media | ~25€ |
| Relay RF keyfob | No | No (arranque en frío) | Baja | ~100-300€ |
| RollJam | No (2-5 metros) | No | Media | ~100€ |
| OBD-II remoto (Macchina A0) | Sí — OBD-II | Sí | Alta | ~50€ |

---

## Preguntas de reflexión

1. ¿Por qué el relay attack no se puede mitigar simplemente cambiando a rolling codes más complejos?
2. ¿Qué tecnología usan los vehículos más modernos para defenderse del relay attack y cómo funciona?
3. ¿En qué se diferencian técnicamente el relay attack y el RollJam? ¿Cuál es más peligroso?
4. Una empresa de seguros detecta un patrón de robos sin signos de entrada forzada. ¿Qué técnica están probablemente usando los ladrones?
5. ¿Qué medida de seguridad puede tomar un propietario hoy, con coste casi cero, para protegerse del relay attack?

---

## Evidencias para el informe

- [ ] Captura de pantalla de `rtl_433` detectando la señal del keyfob
- [ ] Captura de URH con las ráfagas de 2 pulsaciones distintas
- [ ] Anotación de la frecuencia portadora y modulación identificadas
- [ ] Comparativa de los bits de rolling code entre las dos pulsaciones
- [ ] Diagrama del relay attack dibujado/documentado por el equipo
- [ ] Respuestas a las preguntas de reflexión
