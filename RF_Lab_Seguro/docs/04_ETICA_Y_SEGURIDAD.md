# Ética, Seguridad y Límites Legales

**LECTURA OBLIGATORIA ANTES DE CADA SESIÓN**

---

## ⚠️ Declaración de Responsabilidad

Este laboratorio está diseñado EXCLUSIVAMENTE para propósitos educativos y de investigación en ciberseguridad en automoción.

**Cualquier uso no autorizado, malintencionado o fuera de contexto de los procedimientos, herramientas o conocimientos adquiridos es ILEGAL y sujeto a sanciones penales.**

---

## 🔴 Lo que ESTÁ ABSOLUTAMENTE PROHIBIDO

### 1. Capturar y Reproducir Señales Reales
```
❌ PROHIBIDO: Capturar la llave de un coche real
❌ PROHIBIDO: Reproducir esa señal desde otro dispositivo
❌ PROHIBIDO: Intentar abrir un vehículo no tuyo
```
**Consecuencias legales:** Robo, acceso no autorizado, cargos criminales.

### 2. Jamming (Interferencia Activa)
```
❌ PROHIBIDO: Transmitir en 433 MHz para bloquear otras señales
❌ PROHIBIDO: Interferir con sistemas de emergencia
❌ PROHIBIDO: Usar HackRF o similar para jamming
```
**Consecuencias legales:** Delito federal, multas de €10.000+, cárcel.

### 3. Transmisión No Autorizada
```
❌ PROHIBIDO: Transmitir en bandas reguladas sin licencia
❌ PROHIBIDO: Usar equipo de transmisión fuera del laboratorio
❌ PROHIBIDO: Amplificar potencia de emisor de prueba
```
**Consecuencias legales:** Violación de normativa FCC/AEPD.

### 4. Trabajo Fuera de la Aula
```
❌ PROHIBIDO: Llevar equipo RF a casa
❌ PROHIBIDO: Capturar datos de vehículos en la calle
❌ PROHIBIDO: Trabajar sin supervisión del profesor
```
**Consecuencias legales:** Expulsión, antecedentes, sanciones.

### 5. Distribución de Código Ofensivo
```
❌ PROHIBIDO: Compartir scripts de jamming/replay
❌ PROHIBIDO: Publicar resultados de captura en redes
❌ PROHIBIDO: Vender herramientas o datos a terceros
```
**Consecuencias legales:** Instigación, complicidad criminal.

---

## ✅ Lo que SÍ Está PERMITIDO

### Captura Pasiva
```
✓ PERMITIDO: Capturar espectro (solo lectura) con RTL-SDR
✓ PERMITIDO: Registrar potencia, frecuencia, duración
✓ PERMITIDO: Usar un mando de prueba propio aislado
```
**Justificación:** No interfiere con sistemas reales, solo observa.

### Análisis Defensivo
```
✓ PERMITIDO: Estudiar vulnerabilidades teóricamente
✓ PERMITIDO: Proponer mitigaciones
✓ PERMITIDO: Escribir papers académicos
```
**Justificación:** Contribuye a seguridad, investigación legítima.

### Medidas de Detección
```
✓ PERMITIDO: Crear sistemas de detección de jamming
✓ PERMITIDO: Analizar resiliencia a interferencia
✓ PERMITIDO: Evaluar arquitectura defensiva
```
**Justificación:** Enfoque defensivo, aumenta seguridad.

### Documentación Educativa
```
✓ PERMITIDO: Documentar procedimientos seguros
✓ PERMITIDO: Crear plantillas de informe
✓ PERMITIDO: Diseñar prácticas para otros grupos
```
**Justificación:** Conocimiento compartido en contexto académico.

---

## 📋 Declaración de Cumplimiento (Firmar Antes de Empezar)

**TODO alumno DEBE firmar esto ante el profesor:**

```
══════════════════════════════════════════════════════════════════

DECLARACIÓN DE CUMPLIMIENTO ÉTICO

Yo, __________________ (nombre), alumno de ____________ (curso),

DECLARO que:

1. He leído y entiendo los límites éticos y legales en el documento
   "04_ETICA_Y_SEGURIDAD.md"

2. Me comprometo a:
   ✓ Usar el equipo SOLO dentro del aula bajo supervisión
   ✓ Capturar SOLO señales de emisor de prueba aislado
   ✓ NO intentar reproducir o hacer jamming
   ✓ NO llevar equipo fuera del laboratorio
   ✓ NO compartir resultados sin autorización
   ✓ Devolver todo el material en buen estado

3. Entiendo que violar estos compromisos resulta en:
   ✓ Expulsión inmediata de la práctica
   ✓ Sanciones académicas
   ✓ Posibles cargos criminales
   ✓ Antecedentes legales

4. Acepto responsabilidad total por mis acciones.

Firma: ______________________     Fecha: ______________

Profesor: ____________________    Fecha: ______________

══════════════════════════════════════════════════════════════════
```

---

## 🔒 Protocolos de Seguridad en el Laboratorio

### Antes de la Sesión
- [ ] Profesor revisa que no haya transmisores con licencia activa en el aula
- [ ] Profesor configura antenas con longitud máxima (no amplificadas)
- [ ] Profesor verifica que mando de prueba es aislado (no conectado a sistema real)
- [ ] Se establece zona de operación (aula solo)

### Durante la Sesión
- [ ] Profesor presente en todo momento
- [ ] Un profesor por cada 6-8 alumnos máximo
- [ ] Equipo permanece en bancada de laboratorio
- [ ] Solo mando aislado permite transmitir
- [ ] Monitoreo visual continuo de actividad RF
- [ ] Registro de asistencia y firmas de declaración

### Después de la Sesión
- [ ] Verificar que RTL-SDR se devuelve intacto
- [ ] Apagar todos los equipos
- [ ] Guardar bajo llave en gabinete cerrado
- [ ] Documentar en registro de laboratorio
- [ ] Eliminar datos si están fuera de protocolo

---

## 📞 Reporte de Violaciones

Si sospechas que otro alumno está violando estos límites:

1. **NO confrontes directamente**
2. **Reporta al profesor inmediatamente**
3. **Proporciona detalles específicos (qué, cuándo, dónde)**
4. **Espera investigación formal**

**Línea de reporte:** 
- Profesor de la asignatura
- Jefe de Ciberseguridad
- Departamento de Integridad Académica

---

## ⚖️ Marco Legal Aplicable

### España (AEPD, Código Penal)
- **Art. 255 CP:** Sabotaje de sistemas telemáticos (cárcel 1-4 años)
- **Art. 264 CP:** Acceso no autorizado (1-2 años)
- **Art. 278 CP:** Interceptación de comunicaciones (2-4 años)

### Europa (GDPR, Directiva 2006/24/EC)
- Interferencia con comunicaciones → Ilegal
- Acceso no autorizado → Delito informático
- Jamming de servicios → Crimen federal

### Banda ISM 433 MHz
- **Permitida:** Captura pasiva (RX only)
- **Prohibida:** Transmisión (TX) sin licencia
- **Límite potencia:** <10 dBm EIRP
- **Aplicaciones legales:** Mandos, sensores, sistemas cerrados

---

## 🛡️ Casos Reales de Sanciones

### Caso 1: Ataque RollJam (2015)
- **Investigadores:** Hoppe & Kiltz demostraron vulnerabilidad teórica
- **Contexto:** Paper académico publicado, bajo supervisión
- **Resultado:** Aumento de seguridad en industria ✓
- **Si no hubiera sido académico:** Cargos criminales por jamming/acceso no autorizado

### Caso 2: HackRF Jamming (2019)
- **Acusado:** Persona transmitiendo con HackRF en band 433 MHz
- **Cargo:** Interferencia con sistemas de emergencia
- **Sentencia:** €50.000 multa + 2 años cárcel (suspendida)

### Caso 3: Keyfob Cloning (2018)
- **Acusado:** Vendía códigos capturados para abrir coches
- **Cargo:** Robo agravado, acceso no autorizado
- **Sentencia:** 5 años cárcel

**Lección:** El contexto académico protege SOLO si es genuinamente defensivo y bajo supervisión.

---

## 🔬 Cómo Hacer Investigación LEGAL en RF

### Enfoque Correcto
1. ✓ Trabajar con equipos de prueba aislados
2. ✓ Capturar datos SOLO pasivamente
3. ✓ Obtener aprobación ética del centro
4. ✓ Documentar procedimientos de seguridad
5. ✓ Publicar resultados académicamente
6. ✓ Proponer defensas, no ataques

### Enfoque INCORRECTO
1. ✗ Capturar señales de sistemas reales
2. ✗ Intentar reproducir (replay)
3. ✗ Usar sin supervisión institucional
4. ✗ No documentar métodos
5. ✗ Compartir datos sin consentimiento
6. ✗ Publicar guías de ataque operativo

---

## 📚 Recursos para Aprender Correctamente

### Papers Académicos (LEGAL)
- Hoppe & Kiltz, "Attacking Plain OFDM-based Modulation in WLAN" (IEEE, 2008)
- García et al., "Weaknesses in Remote Keyless Entry Systems" (USENIX, 2015)
- Baghaei & Roux, "RF Security in Automotive" (SAE, 2020)

### Estándares Internacionales
- ISO/IEC 27034: Seguridad en aplicaciones
- NIST SP 800-153: Directrices RF security
- 3GPP TS 33.900: Seguridad en telecomunicaciones

### Cursos Certificados
- ECIC (Embedded and Cyber-Physical Systems Security) — Certificado
- SAE ADAS/AV Security — Industrial
- SANS SEC504: Advanced Security Testing — Profesional

---

## 🎓 Alternativas Constructivas

Si quieres profundizar en RF Security sin violar límites:

1. **Investigación Defensiva:** Diseña detectores de jamming
2. **Arquitectura Segura:** Propone rolling code mejorado
3. **Distance Bounding:** Estudia defensa contra relay attacks
4. **Machine Learning:** Clasifica patrones RF para detección de anomalías
5. **Hardware Security:** Diseña transceptor con autenticación

---

## ✋ Preguntas Frecuentes (FAQ)

**P: ¿Puedo llevarme el equipo a casa?**  
R: No. Prácticas de laboratorio = equipo se queda en el laboratorio.

**P: ¿Puedo capturar una llave de coche real "solo para ver"?**  
R: No. Es robo de datos, delito de acceso no autorizado.

**P: ¿Está permitido hacer jamming "experimental"?**  
R: No. Jamming es delito federal incluso experimental.

**P: Si uso VPN, ¿puedo evitar ser detectado?**  
R: VPN no te protege legalmente de delitos como jamming o robo.

**P: ¿Qué pasa si solo estudio el código sin transmitir?**  
R: Está permitido SOLO si es pasiva (captura). Replay/transmisión es delito.

---

## 📞 Contacto de Apoyo Ético

Si tienes preguntas sobre límites o incertidumbre:

- **Profesor de la asignatura:** [nombre, email]
- **Jefe de Seguridad Informática:** [nombre, email]
- **Consejería de Cumplimiento:** [nombre, email]

**Recuerda:** Es mejor preguntar antes que pedir perdón después.

---

## 🏁 Conclusión

Este laboratorio es una oportunidad INCREÍBLE para aprender:
- Fundamentos de RF y seguridad en automoción
- Análisis de espectro y detección de anomalías
- Importancia de defensa en profundidad
- Ética en ciberseguridad

Pero SOLO si lo haces correctamente, dentro de límites legales y éticos.

**El conocimiento sin ética es arma; con ética es solución.**

Firma esta declaración y diviértete aprendiendo. 🚀

