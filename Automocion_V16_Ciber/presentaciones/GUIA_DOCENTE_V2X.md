# Guía del Docente - Presentación V2X
## Gela Prestatzeko Gida / Instructor's Guide

---

## 📋 Resumen Ejecutivo / Laburpen Egitura

Esta guía acompaña las presentaciones HTML5 interactivas sobre V2X y contextualizan la **práctica Help Flash** (CVE-2025-65855).

**Materiales:**
- `V2X_Presentacion_es.html` (español)
- `V2X_Aurkezpena_eu.html` (euskera)
- `V2X_Laburpena_Ikasleentzat.md` (resumen para estudiantes)

**Duración sugerida:** 30-45 minutos (sin incluir debates profundos)

**Público:** Estudiantes de seguridad en automoción, IoT, ciberseguridad

---

## 🎯 Objetivos Pedagógicos / Pedagogiko Helburuak

### Al final de esta sesión, los estudiantes podrán:

1. **Definir V2X** y sus variantes (V2V, V2I, V2P, V2N)
2. **Comprender los protocolos** (DSRC, 5G/C-V2X, NB-IoT)
3. **Identificar vulnerabilidades** en sistemas de comunicación vehicular
4. **Conectar teoría con práctica:** entender por qué hacemos la práctica Help Flash
5. **Proponer soluciones** basadas en criptografía y autenticación

---

## 📊 Flujo de la Sesión / Saiorako Fluxua

### **Bloque 1: Introducción (5 min)**
**Diapositivas 1-2**

**Objetivo:** Captar atención y presentar contexto.

**Notas para el docente:**
- Comienza con la diapositiva de título (1) — déjala visible 30 segundos
- Pregunta al aula: *"¿Alguien ha oído hablar de V2X?"* (levanta manos)
- Diapositiva 2: Presenta la sección "¿Qué es V2X?" con dramatismo

**Puntos clave a enfatizar:**
- V2X = vehículos que hablan entre sí y con el mundo
- Beneficio: mayor seguridad vial
- Problema (nuestro foco): ¿cómo se protege esa comunicación?

**Tiempo de pausa sugerida:** 1 min después de la diapositiva 1 para preguntas iniciales

---

### **Bloque 2: Conceptos Fundamentales (7 min)**
**Diapositivas 3-5**

**Objetivo:** Establecer vocabulario y ejemplos reales.

**Diapositiva 3: Definición y tipos**

Léela lentamente, pausando en cada tipo:
- **V2V:** Cuéntales de coches que se avisan mutuamente en autopista (ejemplo real: frenada de emergencia)
- **V2I:** Semáforos adaptativos en ciudades (Japón, Sudáfrica)
- **V2P:** Coche detecta peatón (importante para ciudades)
- **V2N:** Coches que suben datos a la nube

**Pregunta interactiva:**
*"¿Cuál de estos tipos crees que es más importante para la seguridad? ¿V2V o V2I?"*
(Espera respuestas — ambas son válidas)

**Diapositiva 4: Protocolos**

Explica brevemente la diferencia:
- **DSRC:** antiguo, radio directa (100 m)
- **5G/C-V2X:** nuevo, usa redes móviles (500 m, más rápido)
- **NB-IoT:** banda estrecha, bajo consumo (nuestro caso Help Flash)

**Punto importante:**
*"En España, Help Flash usa NB-IoT de Vodafone. Eso es importante porque...*" (transición a seguridad)

**Diapositiva 5: Aplicaciones reales**

Muestra la tabla. Destaca:
- Help Flash: 250,000+ unidades en España
- Esto es real, no es teórico
- Si la baliza falla, personas en emergencia pueden no recibir ayuda

---

### **Bloque 3: Seguridad y Vulnerabilidades (7 min)**
**Diapositivas 6-8**

**Objetivo:** Transicionar de "qué es" a "qué puede salir mal"

**Diapositiva 6: Sección (transición)**

Pausa dramática de 5 segundos. Cambio de tono:
*"Hasta ahora todo suena bien. Pero... ¿qué pasa si alguien quiere atacar V2X?"*

**Diapositiva 7: Desafíos de seguridad**

**CRUCIAL:** Lee cada punto y explica el impacto:

1. **Falta de encriptación:**
   - *"Tenga cuidado: si envías coordenadas GPS en texto plano, cualquiera en la red puede verlas."*
   - Analogía: *"Como gritar tu ubicación por radio abierto"*

2. **Falta de autenticación:**
   - *"¿Cómo sabe la red que es una baliza legítima? Puede ser cualquiera."*
   - Analogía: *"Como un email sin firma — no sabes quién lo mandó"*

3. **Suplantación:**
   - *"Un atacante puede copiar el IMEI de una baliza real y fingir ser esa baliza."*
   - CVE-2025-65855: esto es lo que sucedió en Help Flash

4. **Localización expuesta:**
   - *"Si sé dónde está la baliza, sé dónde está la persona en emergencia."*
   - Implicación: privacidad y seguridad física

**Pregunta para reflexionar:**
*"¿Cuál de estos problemas os parece más grave?"* (deja que debate 30 segundos)

**Diapositiva 8: Superficie de ataque (diagrama)**

Explica el flujo paso a paso:
1. Baliza envía GPS en claro
2. Red (APN privado) — pero el parámetros están expuestos
3. Servidor (fabrica ota updates sin firma)
4. DGT 3.0 (recibe alerta, puede ser falsa)
5. Paneles de autovía muestran falsa congestión

**Punto crítico:**
*"¿Veis el diagrama? Cada flecha es un punto donde algo puede ir mal. Eso es una 'superficie de ataque'."*

---

### **Bloque 4: Contexto de la Práctica (8 min)**
**Diapositivas 9-12**

**Objetivo:** Conectar teoría con la práctica real que van a hacer.

**Diapositiva 9: Sección (transición)**

*"Ahora que sabemos qué puede salir mal, vamos a ver cómo lo hacemos en el lab."*

**Diapositiva 10: Descripción general**

Repasa los 5 pasos que van a seguir:
1. Baliza config — descubrir parámetros
2. Escucha de tráfico — ver GPS en Wireshark
3. Suplantación — copiar IMEI
4. Ataque OTA — sin firma
5. Conclusiones — qué falló

**Pregunta:**
*"¿Quién cree que puede hacer esto en una tarde de lab?"* (genera confianza: sí, es posible)

**Diapositiva 11: Configuración**

Presenta el material:
- Baliza Help Flash (muéstrala si la tienes)
- Linux ordenador (con Wireshark)
- Python fake_ota_server.py

**Objetivos de aprendizaje:**
Léelos y enfatiza:
*"No es solo 'hackear' — es entender cómo funcionan IoT, cómo se comunican, por qué fallan."*

**Diapositiva 12: Demostración en vivo**

Explica qué verán:
- **Wireshark:** datos GPS en texto plano (muestro un ejemplo si tienes captura)
- **IMEI:** descubierto en 2 minutos
- **Alerta falsa:** enviada a DGT 3.0 (simulada)
- **OTA:** firmware sin firma inyectada

**Punto importante:**
*"Todo esto sucedió en 2025 con 250,000 dispositivos reales en España."*

---

### **Bloque 5: Soluciones y Aprendizajes (8 min)**
**Diapositivas 13-15**

**Objetivo:** Cerrar la brecha entre problema y solución.

**Diapositiva 13: Soluciones y mejoras**

Explica cada solución:

1. **Encriptación (TLS/DTLS):**
   - *"Poner un candado en la comunicación. Solo el remitente y receptor saben la clave."*
   - Analógía: *"Enviar carta en caja de seguridad vs. postal abierta"*

2. **Autenticación (Certificados X.509):**
   - *"Cada dispositivo tiene un certificado que prueba quién es."*
   - Analogía: *"Como tu pasaporte — demuestra tu identidad"*

3. **Verificación de integridad (HMAC/SHA256):**
   - *"Un código que verifica que el mensaje no fue alterado en el camino."*
   - Analogía: *"Como una firma en un contrato"*

4. **Firma de actualizaciones OTA:**
   - *"El fabricante firma cada actualización. Si no está firmada, el dispositivo la rechaza."*

5. **Nonce + Timestamp:**
   - *"Cada mensaje tiene un número único y una marca de tiempo. Evita repetición de mensajes."*

**Pregunta:** 
*"¿Cuál de estas soluciones crees que es más importante?"* (discute 1 min)

**Diapositiva 14: Aprendizajes clave (resumen)**

Dos columnas — 🔴 Riesgos vs. 🟢 Soluciones

Resumen rápido:
- Riesgos: comunicación abierta, sin verificación, sin firma
- Soluciones: encriptación, autenticación, integridad, firma

**Pregunta para cerrar:**
*"¿Alguien puede decirme en una frase qué es lo más importante que hemos aprendido?"*
(espera respuesta — probablemente: "encriptación" o "autenticación")

**Diapositiva 15: Conclusión**

Lee el párrafo inicial lentamente:
*"La tecnología V2X aporta grandes ventajas al sector automotriz, pero la seguridad debe estar en la base. En esta práctica, hemos visto cómo una implementación completa puede fallar."*

**Punto final:**
*"Reto: Las nuevas tecnologías se despliegan rápidamente sin suficientes auditorías de seguridad. Vosotros, como futuros ingenieros o analistas de seguridad, tenéis la responsabilidad de pensar en estos problemas."*

**Cierre:**
*"¿Preguntas antes de pasar a la práctica?"* (deja 2-3 min para Q&A)

---

## 🎓 Estrategias de Engagement / Estrategiak Ikasleen Bahean

### **Preguntas interactivas por bloques:**

| Bloque | Pregunta | Respuesta esperada |
|--------|----------|-------------------|
| 1 | ¿Alguien ha oído de V2X? | Múltiples respuestas |
| 2 | ¿V2V o V2I más importante? | Ambas válidas (debate) |
| 3 | ¿Cuál es el riesgo más grave? | Privacidad / suplantación |
| 4 | ¿Se puede hackear en un día? | Sí, por eso hacemos el lab |
| 5 | ¿Cuál es la solución clave? | Encriptación + autenticación |

### **Elementos de drama pedagógico:**

- Diapositiva 6 (transición): cambio de tono (de esperanzador a crítico)
- Diapositiva 8 (diagrama): flujo de ataque — muestra la complejidad
- Diapositiva 12: "esto pasó en 2025 con 250,000 dispositivos reales"
- Diapositiva 15: responsabilidad ética

---

## 🛠️ Recursos Técnicos para el Docente / Teknika Baliabideak

### Antes de la sesión:

- [ ] Abre las presentaciones HTML en tu navegador (prueba navegación)
- [ ] Sirve localmente con `python3 -m http.server 8000` si proyectas
- [ ] Prueba proyector/pantalla (1920×1080 recomendado)
- [ ] Ten abierta `05_Demo_Vulnerabilidades_Help_Flash.md` para referencias
- [ ] Si tienes una captura de Wireshark de Help Flash, muéstrala en Diapositiva 12

### Durante la sesión:

- Usa **F11** para pantalla completa
- Navega con **flechas del teclado** (más rápido que botones)
- **Pausa entre diapositivas de sección** (2-3, 6, 9) para transiciones claras
- Si un estudiante pregunta sobre detalles técnicos: *"Buena pregunta — la respondemos en el lab"*

### Después de la sesión:

- Distribuye `V2X_Laburpena_Ikasleentzat.md` (resumen para estudiantes)
- Recuerda: *"La práctica empieza mañana/en el siguiente bloque"*
- Deja claro: *"Todo lo que hemos hablado, lo experimentaréis en el lab"*

---

## 📝 Notas de Adaptación / Egokitze Notak

### Si tienes poco tiempo (20 min):

Salta:
- Diapositiva 5 (aplicaciones reales) — demasiado tiempo
- Diapositiva 8 (diagrama detallado) — muy técnico

Mantén:
- 1-4: Introducción + concepto
- 6-7: Seguridad (lo importante)
- 13-15: Soluciones + cierre

### Si tienes mucho tiempo (60+ min):

Añade:
- Demo en vivo de Wireshark (Diapositiva 12)
- Preguntas largas entre bloques (debate)
- Vídeo de Help Flash CVE-2025-65855 (si disponible)
- Casos adicionales: Tesla OTA, WhatsApp en coche, etc.

### Si tu aula es técnica (ingenieros):

Enfatiza:
- Protocolos (Diapositiva 4) — menos "qué es", más "por qué ese y no otro"
- Diapositiva 8 (superficie de ataque) — análisis profundo
- Diapositiva 13 (soluciones) — implementación técnica

### Si tu aula es gerencial (decisores):

Enfatiza:
- Diapositiva 1 (contexto empresarial)
- Diapositiva 5 (aplicaciones reales, números)
- Diapositiva 7 (riesgos de reputación)
- Diapositiva 13 (coste de soluciones vs. riesgo)

---

## 🎬 Transiciones Sugeridas Entre Diapositivas / Trantsizio Loterak

### Dinámica:

**Diapositiva 1 → 2:**
*"Comencemos con una pregunta: ¿qué es V2X?"* [muestra 2]

**Diapositiva 2 → 3:**
*"Hay cuatro tipos principales de V2X. Vamos a verlos."* [muestra 3]

**Diapositiva 5 → 6:**
*"Ahora que entendemos las aplicaciones, el problema: ¿son seguras?"* [muestra 6]

**Diapositiva 8 → 9:**
*"Este es el riesgo. En nuestra práctica, vamos a explotarlo."* [muestra 9]

**Diapositiva 12 → 13:**
*"Eso fue el problema. Ahora, las soluciones."* [muestra 13]

**Diapositiva 14 → 15:**
*"En conclusión... os toca a vosotros en el lab."* [muestra 15]

---

## 🔍 Preguntas de Cierre / Itxiera Galderak

Escoge una (o todas) para el final:

1. **Técnica:** *"¿Qué protocolo V2X crees que es más seguro: DSRC o C-V2X? ¿Por qué?"*

2. **Práctica:** *"En el lab, ¿por dónde empezarías el ataque a Help Flash?"*

3. **Ética:** *"Si descubrimos una vulnerabilidad en un dispositivo real, ¿qué hacemos?"* (responsible disclosure)

4. **Empresarial:** *"¿Cuánto costaría implementar encriptación + autenticación en Help Flash?"* (estimaciones)

5. **Reflexiva:** *"¿Qué tecnología que usas a diario no has pensado que tenga estos riesgos?"*

---

## 📖 Referencias Adicionales / Gehiago Ikastekotan

- **CVE-2025-65855:** [CVE Official](https://www.cve.org/CVERecord?id=CVE-2025-65855)
- **Help Flash IoT:** [Sitio web oficial](https://www.helpflash.es)
- **V2X Estándares:** IEEE 802.11p, 3GPP C-V2X specs
- **Práctica completa:** Fichero `05_Demo_Vulnerabilidades_Help_Flash.md`
- **OTA Seguridad:** [NIST Guidelines](https://csrc.nist.gov/)

---

## ✅ Checklist Previo a Presentación / Aurkezpenaren Aurreko Checklist

- [ ] Presentaciones abiertas en navegador (ambos idiomas)
- [ ] Pantalla de proyección conectada y probada
- [ ] Sonido probado (si usas audio)
- [ ] Aula con estudiantes sentados cómodamente
- [ ] Baliza Help Flash física (opcional pero impactante)
- [ ] Wireshark abierto en tu ordenador (para demo)
- [ ] `V2X_Laburpena_Ikasleentzat.md` lista para distribuir
- [ ] `05_Demo_Vulnerabilidades_Help_Flash.md` abierto como referencia
- [ ] Reloj / cronómetro para respetar tiempos
- [ ] Agua / micrófono (si es sala grande)

---

## 📞 Notas Finales / Amaierako Notak

**Tono:** Mantén un equilibrio entre educativo y entretenido. V2X puede parecer abstracto, pero CVE-2025-65855 es real y recientemente se exploró.

**Ritmo:** No apures. Mejor ir un poco lento y responder bien que acabar prisa y dejar gente perdida.

**Engagement:** Cada bloque tiene una pregunta interactiva — úsalas para mantener el aula despierta.

**Cierre fuerte:** La Diapositiva 15 es tu punto de apoyo — deja que suene.

¡Mucho éxito en la presentación! 🚀

---

*Última actualización: Octubre 2026*  
*Autor: Equipo Educativo Automozioa*
