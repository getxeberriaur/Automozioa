# Puntos de Orador - V2X Presentación
## Speaker Notes / Entzuleak baterako Notak

**Uso:** Mantén este archivo abierto en otra pestaña mientras presentas.

---

## DIAPOSITIVA 1 (Portada - 1 min)

### Qué decir:
- "Buenos días/tardes, vamos a hablar de V2X — una tecnología cada día más importante en vehículos"
- "V2X significa Vehicle-to-Everything — es decir, vehículos que hablan con todo lo que les rodea"
- "Por qué os lo cuento? Porque dentro de poco haréis una práctica donde 'hackeamos' esta tecnología"

### Preguntas:
- ¿Alguien ha oído hablar de V2X?
- ¿Alguien sabe qué es?

### Tiempo de pausa:
- Espera 30 segundos de silencio — déjales pensar

---

## DIAPOSITIVA 2 (Sección - Transición)

### Qué decir:
- "Comencemos con lo básico: ¿qué es V2X?"
- "Para eso, necesitamos entender cómo se comunican los coches"

### Transición:
- "Sigamos adelante..."

---

## DIAPOSITIVA 3 (Definición)

### Qué decir (lentamente):

**Introducción:**
- "V2X tiene cuatro tipos principales de comunicación"

**V2V — Vehicle-to-Vehicle:**
- "Un coche le dice a otro: cuidado, freno de emergencia"
- "Ejemplo: estás en autopista, ves que un coche más adelante frena. Tu coche recibe esa alerta y te prepara"
- "¿Beneficio? Evitar accidentes en cadena"

**V2I — Vehicle-to-Infrastructure:**
- "Tu coche habla con la infraestructura: semáforos, señales, sistemas de tráfico"
- "Ejemplo: llego a un semáforo en rojo, pero el coche le dice al semáforo que vengo — el semáforo se pone verde optimizando el flujo"
- "¿Beneficio? Menos congestión, menos contaminación"

**V2P — Vehicle-to-Pedestrian:**
- "Tu coche detecta a un peatón que no ve el coche — le avisa"
- "Ejemplo: peatón con auriculares cruzando la calle"
- "¿Beneficio? Reducir accidentes con peatones (muy importante en ciudades)"

**V2N — Vehicle-to-Network:**
- "Tu coche sube datos a la nube — datos de tráfico, de mantenimiento, de seguridad"
- "Ejemplo: Help Flash sube tu localización para que sepan dónde estás en emergencia"
- "¿Beneficio? Servicios centralizados, análisis de datos, trazabilidad"

### Pregunta interactiva:
- "¿Cuál de estos cuatro os parece más importante para la seguridad?"
- (Espera respuestas — todas son válidas, pero V2P es la más dramática)

### Tiempo:
- 3 minutos total

---

## DIAPOSITIVA 4 (Protocolos)

### Qué decir:

**Introducción:**
- "Ahora bien, ¿cómo se comunican realmente?"
- "Hay diferentes 'idiomas' o protocolos"

**DSRC (Dedicated Short Range Communications):**
- "Es como una radio que solo hablan coches entre sí"
- "Frecuencia: 5.9 GHz (la misma que WiFi, casi)"
- "Alcance: 100 metros"
- "Ventaja: latencia baja — respuesta rápida"
- "Desventaja: no usamos internet, es red privada"
- "Usado en: AEBak, Japón, algunos sitios en Europa"

**5G / C-V2X:**
- "Es el futuro — usa las redes 5G que ya conocemos"
- "Alcance: 500 metros (mucho más que DSRC)"
- "Ventaja: se integra con internet, más servicios"
- "Desventaja: latencia ligeramente mayor (pero aceptable)"
- "Usado en: China, USA, próximamente Europa"

**NB-IoT (nuestro caso — Help Flash):**
- "Banda estrecha — consume muy poco, pensada para dispositivos que no tienen mucha batería"
- "Alcance: 1-10 kilómetros"
- "Ventaja: bajo consumo, largo alcance"
- "Desventaja: latencia alta, menos seguridad en el protocolo"
- "Usado en: España (Vodafone) para Help Flash y otros IoT"

### Punto crítico:
- "En España, Help Flash usa NB-IoT de Vodafone. Eso es importante porque — spoiler — es donde está el problema"

### Tiempo:
- 2 minutos

---

## DIAPOSITIVA 5 (Aplicaciones Reales)

### Qué decir:

**Introducción:**
- "Veamos dónde se está usando V2X en el mundo real"

**Tabla — comenta fila por fila:**

1. **DGT 3.0 (Help Flash) — Espainia:**
   - "250,000+ balizas Help Flash en España"
   - "Usa NB-IoT de Vodafone"
   - "Si accidentas, la baliza avisa a DGT"
   - "¿El problema? Veremos después"

2. **Vehículos conectados con 5G — China, USA:**
   - "Tesla, BYD, Geely ya tienen V2X"
   - "C-V2X es el estándar emergente"

3. **Semáforos inteligentes — Japón, algunos países europeos:**
   - "Ciudades inteligentes"
   - "Tráfico optimizado"

4. **Seguridad de peatones — USA (piloto):**
   - "Todavía muy nuevo"
   - "Aún en fase de prueba"

### Punto crítico:
- "El único que toca a España es Help Flash — 250,000 dispositivos reales"
- "Si hay una vulnerabilidad, afecta a 250,000 personas en España"
- "Por eso hacemos esta práctica"

### Tiempo:
- 2 minutos

---

## DIAPOSITIVA 6 (Sección - Transición Crítica)

### Qué decir:
- **PAUSA DRAMÁTICA** — 5 segundos de silencio
- "Hasta ahora todo suena maravilloso: coches que se hablan, tráfico optimizado, menos accidentes"
- "Pero... ¿qué pasa si alguien quiere atacar esto?"
- **OTRA PAUSA** — déjales pensar 3 segundos
- "Porque eso es seguridad — pensar en lo malo"

### Transición:
- "Veamos qué puede salir mal"

---

## DIAPOSITIVA 7 (Seguridad - Desafíos)

### Qué decir (muy importante):

**Introducción:**
- "Help Flash usa NB-IoT de Vodafone"
- "Todos los datos viajan por internet"
- "¿Cómo se protegen?"

**Problema 1 — Tenga cuidado: Datos en texto plano:**
- "Imagina que subes tu localización por WhatsApp sin cifrar — alguien en la red la ve"
- "Con Help Flash: mismo problema"
- "GPS en claro = alguien sabe dónde estás"
- "CVE-2025-65855 dice exactamente: todo en texto plano"

**Problema 2 — Falta de autenticación:**
- "¿Cómo sabe la red que un mensaje viene de una baliza Help Flash legítima?"
- "Analogía: email sin firma — podrías ser cualquiera"
- "En Help Flash: no hay verificación de identidad"
- "Resultado: un atacante puede fingir ser una baliza"

**Problema 3 — Suplantación:**
- "¿Conoces el IMEI? Es el ID único de tu móvil"
- "Help Flash también tiene IMEI"
- "¿Y si alguien copia ese IMEI?"
- "Resultado: el atacante se convierte en esa baliza"
- "Puedes enviar alertas falsas desde tu identidad"

**Problema 4 — Localización expuesta:**
- "Si sé dónde está tu baliza (porque transmite en claro), sé dónde estás TÚ"
- "¿Qué pasa si eres un abogado defensor en un juicio? ¿Una víctima de violencia?"
- "Privacidad = seguridad física"

### Pregunta interactiva:
- "¿Cuál de estos cuatro os parece más grave?"
- (Escucha: privacidad es la más importante, pero suplantación es la que exploraremos)

### Dato importante:
- "CVE-2025-65855 no es teoría — fue descubierto en 2025, hace poco"
- "250,000 dispositivos Help Flash afectados"
- "El fabricante ha emitido parches"

### Tiempo:
- 3 minutos

---

## DIAPOSITIVA 8 (Superficie de Ataque)

### Qué decir (explica el diagrama paso a paso):

**Paso 1 — Baliza IoT:**
- "Una baliza Help Flash en un coche"
- "Tiene puerto serie expuesto (problema 1)"
- "APN privado no es secreto (problema 2)"
- "¿Por qué? Porque los parámetros están escritos en la documentación"

**Paso 2 — Sarearen pasagunen (Vodafone APN):**
- "Aquí es donde viajan los datos"
- "Teóricamente privado, pero..."
- "Un atacante puede interceptar (man-in-the-middle)"
- "¿Cómo? Inyectándose en la red NB-IoT"
- "¿Difícil? No es trivial, pero posible con radio definida por software"

**Paso 3 — Servidor del fabricante:**
- "Recibe los datos de la baliza"
- "Envía actualizaciones OTA (Over-The-Air)"
- "¿Problema? Las actualizaciones NO ESTÁN FIRMADAS"
- "Significa: un atacante puede inyectar código malicioso"

**Paso 4 — DGT 3.0:**
- "Recibe alertas de Help Flash"
- "Las muestra en paneles de autovía"
- "Si un atacante envía alerta falsa..."
- "...DGT 3.0 la muestra como real"
- "Resultado: congestión falsa, pánico innecesario"

### Punto crítico:
- "Ves el diagrama? Cada flecha es un punto donde algo puede fallar"
- "Eso es una 'superficie de ataque'"
- "Cuantos más puntos, más probabilidad de explotación"

### Tiempo:
- 2 minutos

---

## DIAPOSITIVA 9 (Sección - Transición)

### Qué decir:
- "Ahora que sabemos qué PUEDE salir mal..."
- "...vamos a ver cómo lo HACEMOS en el laboratorio"
- "Porque el lab no es teórico — es práctico"

---

## DIAPOSITIVA 10 (Descripción de la Práctica)

### Qué decir (cinco pasos):

**Paso 1 — Configuración de baliza:**
- "Descubrimos los parámetros NB-IoT"
- "¿Cómo? Mirando el puerto serie"
- "APN, banda, velocidad — todo está ahí"

**Paso 2 — Escucha de tráfico en red:**
- "Abrimos Wireshark"
- "Vemos los paquetes que envía Help Flash"
- "¿Qué vemos? GPS en texto plano"
- "Coordenadas exactas: latitud, longitud, timestamp"

**Paso 3 — Suplantación de baliza:**
- "Capturamos el IMEI"
- "Lo copiamos"
- "Ahora somos esa baliza (según la red)"
- "Podemos enviar mensajes usando su identidad"

**Paso 4 — Ataque OTA:**
- "Enviamos una actualización falsa"
- "El firmware no está firmado, la acepta"
- "Hemos inyectado código en la baliza"

**Paso 5 — Conclusiones:**
- "¿Qué falló? Encriptación, autenticación, integridad, firmas"
- "¿Cómo lo arreglamos? (siguiente diapositiva)"

### Pregunta:
- "¿Alguien piensa que se puede hacer todo en una sesión de lab?"
- (Sí, es posible en 2 horas)

### Tiempo:
- 3 minutos

---

## DIAPOSITIVA 11 (Configuración)

### Qué decir:

**Material:**
- "Cada grupo tiene una baliza Help Flash"
- "Linux ordenador con Wireshark"
- "Python 3.8+ para script fake_ota_server.py"

**Objetivos de aprendizaje — léelos uno a uno:**
1. "Nola funtzionatzen duten IoT baliak testu garbian"
2. "Nola gertatzen da suplantazioa praktikan"
3. "OTA eguneratzeen seguritatea (edo eza)"
4. "Nola sortzea zizta mezu"

### Punto importante:
- "No es solo 'hackear' para hackear"
- "Es ENTENDER cómo funcionan estas cosas"
- "Luego podríais auditar, proteger, mejorar"

### Tiempo:
- 2 minutos

---

## DIAPOSITIVA 12 (Demostración en Vivo)

### Qué decir:

**Introducción:**
- "Aquí es donde hacemos la magia"

**Qué veremos:**
1. "Wireshark con datos GPS en texto plano — vemos ubicación exacta"
2. "IMEI descubierto en 2 minutos — identidad de la baliza"
3. "Alerta falsa enviada a DGT 3.0 — creamos congestión falsa"
4. "OTA sin firma — inyectamos código en firmware"

### Dato importante:
- "Todo esto sucedió en 2025"
- "Con dispositivos reales"
- "250,000 personas potencialmente afectadas"

### Tiempo:
- 1 minuto (luego pasas a soluciones)

---

## DIAPOSITIVA 13 (Soluciones)

### Qué decir (explica cada solución):

**Introducción:**
- "Bien, hemos visto todos los problemas"
- "¿Cómo se arregla?"

**1. Encriptación (TLS/DTLS):**
- "Poner un candado en la comunicación"
- "Solo remitente y receptor saben la clave"
- "Analogía: enviar carta en caja de seguridad vs. postal abierta"
- "Técnica: protocolo TLS (igual que HTTPS en navegadores)"

**2. Autenticación (Certificados X.509):**
- "Cada dispositivo tiene un certificado"
- "Demuestra su identidad"
- "Analogía: pasaporte"
- "Cómo funciona: handshake de certificados al conectar"

**3. Verificación de integridad (HMAC/SHA256):**
- "Código que verifica que el mensaje no fue alterado"
- "Analogía: firma en un contrato"
- "Técnica: hash criptográfico incluido en cada mensaje"

**4. Firma de actualizaciones OTA:**
- "El fabricante firma CADA actualización"
- "Si no está firmada, baliza la rechaza"
- "Técnica: clave privada del fabricante + validación de firma"

**5. Nonce + Timestamp:**
- "Número único en cada mensaje"
- "Marca de tiempo"
- "Previene repetición y replay attacks"

### Pregunta:
- "¿Cuál crees que es más importante?"
- (Probablemente: encriptación o autenticación — ambas son críticas)

### Tiempo:
- 3 minutos

---

## DIAPOSITIVA 14 (Aprendizajes Clave)

### Qué decir (resumen rápido):

**🔴 Riesgos:**
- Comunicación en texto plano
- Falta de autenticación
- Inyección de falsas alertas
- Actualizaciones sin verificar

**🟢 Soluciones:**
- Encriptación (TLS/DTLS)
- Autenticación (Certificados)
- Verificación de integridad (HMAC)
- Firmas en actualizaciones (OTA seguro)

### Punto importante:
- "Esto no es una lista mágica"
- "Esto es el MÍNIMO para seguridad básica"
- "En la industria, hay más capas"

### Tiempo:
- 2 minutos

---

## DIAPOSITIVA 15 (Conclusión)

### Qué decir (lentamente y con peso):

**Párrafo principal:**
- "La tecnología V2X aporta grandes ventajas al sector automotriz"
- "Pero la seguridad debe estar en la BASE"
- "No puede ser un añadido"
- "En esta práctica, hemos visto cómo una implementación 'completa' puede fallar"

**Reto final:**
- "Las nuevas tecnologías se despliegan rápidamente"
- "Sin suficientes auditorías de seguridad"
- "Vosotros, como futuros ingenieros o analistas de seguridad"
- "Tenéis la responsabilidad de pensar en estos problemas"

**Cierre:**
- "¿Preguntas antes de la práctica?"
- (Espera 2-3 minutos de Q&A)

### Tiempo:
- 1 minuto (más Q&A)

---

## PREGUNTAS FRECUENTES (para si te preguntan):

**P: ¿Esto es ilegal? ¿Podemos hacerlo?**
A: "Es ilegal si lo haces contra Help Flash real. En nuestro lab, simulamos con una baliza controlada y en red privada. Es investigación y educación autorizadas."

**P: ¿Help Flash lo arregló?**
A: "Sí, hay parches. Pero 250,000 dispositivos aún pueden estar vulnerables. Por eso es importante que aprendáis."

**P: ¿V2X es peligroso? ¿No debería usarse?**
A: "V2X es seguro si se implementa bien. El problema es cuando se implementa mal. Nuestra responsabilidad es pensar en lo malo."

**P: ¿Puedo explotar Help Flash en mi coche?**
A: "No es aconsejable. Pero ahora sabéis cómo se haría. Responsabilidad."

**P: ¿Qué otros sistemas tienen problemas similares?**
A: "Muchos. IoT en general es frágil. Tesla OTA, sistemas de telemedicina, etc. Siempre aplica los mismos principios."

---

## TIMING TOTAL:

- Diapositivas 1-2: 1 min
- Diapositivas 3-5: 7 min
- Diapositivas 6-8: 7 min
- Diapositivas 9-12: 8 min
- Diapositivas 13-15: 8 min
- Q&A: 5-10 min

**Total: 36-46 minutos** (sin contar debates largos)

---

**Usa este documento como referencia rápida. ¡Mucho éxito!** 🚀
