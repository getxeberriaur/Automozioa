# Checklist de Seguridad: Laboratorio RF

**Este checklist DEBE completarse antes y después de CADA sesión de laboratorio.**

---

## ✋ PRE-SESIÓN: Verificación de Equipo (Profesor)

**Fecha:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_  
**Profesor:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_  
**Hora inicio:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_  

### Hardware RF

- [ ] **Raspberry Pi:** Encendida, accesible por SSH
  - IP: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
  - Test SSH: `ssh pi@192.168.1.X` → OK

- [ ] **RTL-SDR Dongle:** Conectado, reconocido por USB
  - Verificación: `lsusb | grep Realtek` → Found
  - Test: `rtl_test -t` → Test passed

- [ ] **Antena Dipolo:** 433 MHz, ~34 cm longitud
  - Conectada a RTL-SDR: Sí / No
  - Estado físico: OK / Dañada

- [ ] **Mando de Prueba:** 433.92 MHz, aislado
  - Pilas nuevas: Sí / No
  - Funcionalidad (test en receptor): OK / No responde
  - Conexión con sistema real: None / Describe: \_\_\_\_\_\_\_\_\_\_

- [ ] **Receptor RF (referencia):** Relé 10A sin carga
  - Desconectado de motor/puerta: Sí / No
  - Alimentación: AC 230V / DC 12V
  - Estado: OK / Dañado

### Software

- [ ] **Python 3.9+:** Instalado en RPi y Portátil
  - RPi: `python3 --version` → 3.X.X
  - Portátil: `python3 --version` → 3.X.X

- [ ] **Librerías Python:** Todas presentes
  - RTL-SDR: `rtl_power` disponible en PATH
  - Análisis: matplotlib, pandas, numpy, scipy importables

- [ ] **Scripts descargados:** Presentes y ejecutables
  - `spectrum_capture.sh`: Sí / No, Permisos: \_\_\_\_
  - `analyze_spectrum.py`: Sí / No, Permisos: \_\_\_\_

- [ ] **Carpetas de trabajo:** Creadas y accesibles
  - RPi `~/rf_capture/`: Sí / No
  - Portátil `~/rf-analysis/`: Sí / No
  - Permisos escritura: OK / Problemas

### Conectividad

- [ ] **Red WiFi/Ethernet:** RPi conectada
  - IP obtenida: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
  - Ping desde portátil: OK / Error

- [ ] **SSH funcional:** Portátil → RPi
  - Comando: `ssh pi@IP` → Conecta sin contraseña
  - Status: ✓ OK / ✗ Requiere contraseña

### Cumplimiento Ético

- [ ] **Declaración de ética:** Disponible (doc 04_ETICA_Y_SEGURIDAD.md)
- [ ] **Aprobación institucional:** Obtenida del centro
- [ ] **Supervisión:** \_\_\_\_\_ profesor(es) presentes (mín 1 por 8 alumnos)
- [ ] **Zona controlada:** Aula cerrada, sin tráfico público

---

## 📋 POR CADA GRUPO: Inicio de Sesión

**Grupo:** \_\_\_\_\_\_\_\_\_\_\_\_\_  
**Miembros:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_  
**Hora inicio:** \_\_\_\_\_\_\_\_  

### Firma de Declaración Ética

- [ ] **Todos los alumnos han leído** `04_ETICA_Y_SEGURIDAD.md`
- [ ] **Todos los alumnos han firmado** la declaración de cumplimiento
- [ ] **Profesor ha revisado** y aprobado las firmas

### Explicación de Límites

- [ ] Profesor ha explicado qué está PERMITIDO
- [ ] Profesor ha explicado qué está PROHIBIDO
- [ ] Alumnos comprenden diferencia entre:
  - [ ] Captura pasiva (RX) vs transmisión activa (TX)
  - [ ] Análisis defensivo vs ofensivo (jamming/replay)
  - [ ] Equipo de prueba vs sistema real
- [ ] Q&A resueltas, alumnos sin dudas

### Equipo Asignado

- [ ] **Mando de prueba:** Entregado a grupo, registrado
- [ ] **RPi + RTL-SDR:** Verificado funcionando, asignado
- [ ] **Antenas:** Corta (no amplificada), específicamente para laboratorio
- [ ] **Portátil:** Con Python/librerías instaladas
- [ ] **Documentación:** Impresa o disponible en pantalla

### Requisitos Pre-Captura

- [ ] Mando posicionado a ~50 cm de antena dentro del aula
- [ ] Receptor RF (si presente) está desconectado de sistemas reales
- [ ] No hay transmisores con licencia activa operando
- [ ] Profesor presente y monitoreando grupo

---

## ⚡ DURANTE LA SESIÓN: Monitoreo Continuo

**Monitorear cada 10-15 minutos:**

| Hora | Actividad | Observaciones | Profesor | ✓ |
|---|---|---|---|---|
| \_\_ : \_\_ | Grupo 1: \_\_\_\_\_\_\_\_\_\_\_\_ | \_\_\_\_\_\_\_\_\_\_\_\_ | \_\_\_\_\_\_ | |
| \_\_ : \_\_ | Grupo 2: \_\_\_\_\_\_\_\_\_\_\_\_ | \_\_\_\_\_\_\_\_\_\_\_\_ | \_\_\_\_\_\_ | |
| \_\_ : \_\_ | Grupo 3: \_\_\_\_\_\_\_\_\_\_\_\_ | \_\_\_\_\_\_\_\_\_\_\_\_ | \_\_\_\_\_\_ | |

### Verificaciones de Seguridad Continuas

- [ ] **Mando:** Solo en aula, bajo supervisión
- [ ] **Antenas:** Longitud normal (no amplificadas)
- [ ] **Potencia:** RTL-SDR ganancia ≤ 50 (no máxima)
- [ ] **Área RF:** Confinada al aula (puertas cerradas)
- [ ] **HackRF/TX:** NO está presente (solo RX con RTL-SDR)

### Banderas Rojas (Stop Inmediato si Ocurre)

**SI observas algo de esto, DETENER sesión inmediatamente:**

- [ ] Alumno intenta llevar equipo fuera del aula
- [ ] Alumno conecta mando a sistema real (puerta, coche, etc.)
- [ ] Alumno intenta transmitir (no solo capturar)
- [ ] Equipo no supervisado o desatendido
- [ ] Conducta sospechosa o intento de "hack"

**Acción:** Confiscar equipo, documentar, reportar a dirección.

---

## ✅ POST-SESIÓN: Cierre Seguro

**Hora fin:** \_\_\_\_\_\_\_\_  

### Devolución de Equipo

**Por cada grupo:**

- [ ] **Mando:** Devuelto, intacto, pilas OK
  - Estado: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
  - Firma grupo: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

- [ ] **RTL-SDR + Antena:** Sin daños físicos
  - Estado: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
  - Firma grupo: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

- [ ] **RPi:** Apagada, almacenada en gabinete
  - Integridad: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

- [ ] **Cables/Accesorios:** Completos
  - Falta: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

### Gestión de Datos

- [ ] **CSVs de captura:** Descargados a almacenamiento seguro
- [ ] **Datos en RPi:** Borrados (si requiere privacidad)
  - `rm ~/rf_capture/*.csv`
- [ ] **Respaldos:** En carpeta protegida del centro

### Finalización

- [ ] **Informe:** Comenzado o completado (plazo: \_\_\_\_\_\_\_\_)
- [ ] **Equipo:** Guardado bajo llave en gabinete cerrado
- [ ] **Registro:** Entrada en log de laboratorio
- [ ] **Anormalidades:** Documentadas (si las hay)

---

## 📊 REGISTRO DE SESIONES

### Sesión 1

| Campo | Dato |
|---|---|
| Fecha | \_\_\_\_\_\_\_\_\_\_\_\_ |
| Grupos | \_\_\_\_\_\_\_\_\_\_\_\_ |
| Profesor responsable | \_\_\_\_\_\_\_\_\_\_\_\_ |
| Incidentes | \_\_\_\_\_\_\_\_\_\_\_\_ |
| Estado final | ✓ OK / ⚠ Alerta |

### Sesión 2

| Campo | Dato |
|---|---|
| Fecha | \_\_\_\_\_\_\_\_\_\_\_\_ |
| Grupos | \_\_\_\_\_\_\_\_\_\_\_\_ |
| Profesor responsable | \_\_\_\_\_\_\_\_\_\_\_\_ |
| Incidentes | \_\_\_\_\_\_\_\_\_\_\_\_ |
| Estado final | ✓ OK / ⚠ Alerta |

### Sesión 3

| Campo | Dato |
|---|---|
| Fecha | \_\_\_\_\_\_\_\_\_\_\_\_ |
| Grupos | \_\_\_\_\_\_\_\_\_\_\_\_ |
| Profesor responsable | \_\_\_\_\_\_\_\_\_\_\_\_ |
| Incidentes | \_\_\_\_\_\_\_\_\_\_\_\_ |
| Estado final | ✓ OK / ⚠ Alerta |

---

## ⚠️ REPORTE DE INCIDENTES

**Si ocurre CUALQUIER incidente, completar esto:**

```
Fecha:     _______________
Hora:      _______________
Descripción: ___________________________________
             ___________________________________
             ___________________________________

Gravedad:   ☐ Leve  ☐ Moderada  ☐ Grave  ☐ Crítica

Acciones tomadas:
  ☐ Parada inmediata
  ☐ Confiscación de equipo
  ☐ Reportado a dirección
  ☐ Otro: _________________________________

Responsable:  _______________________
Firma profesor: _______________________
Fecha: _______________________
```

---

## 🔐 Almacenamiento Seguro de Equipo

**Gabinete de laboratorio:**
- [ ] Cerrado con llave
- [ ] Solo profesor tiene acceso
- [ ] Inventario verificado: \_\_\_\_\_ equipos presentes
- [ ] Revisar semanal

---

## 📞 Contactos de Emergencia

| Rol | Nombre | Teléfono | Email |
|---|---|---|---|
| Profesor responsable | \_\_\_\_\_\_\_\_ | \_\_\_\_\_\_\_\_ | \_\_\_\_\_\_\_\_ |
| Jefe seguridad informática | \_\_\_\_\_\_\_\_ | \_\_\_\_\_\_\_\_ | \_\_\_\_\_\_\_\_ |
| Director centro | \_\_\_\_\_\_\_\_ | \_\_\_\_\_\_\_\_ | \_\_\_\_\_\_\_\_ |

---

## ✍️ Firma Final

**Este checklist ha sido completado y verificado:**

Profesor responsable: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_  
Firma: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_  
Fecha: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_  

---

**⚡ RECORDATORIO:**  
La seguridad en este laboratorio es RESPONSABILIDAD COMPARTIDA.  
Profesor: supervisión y cumplimiento.  
Alumnos: honestidad y cumplimiento ético.  

**Violar estos límites resulta en expulsión inmediata y sanciones académicas.**

