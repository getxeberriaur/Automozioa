# 🎥 Guión de Vídeo — V2X Explicado en 10 minutos
## Script for Recording (Opcional)

*Tiempo total: 9-12 minutos*

---

## OPENING (0:00-0:30)

### [Pantalla: V2X_Aurkezpena_eu.html - Portada]

**Narrador:**
"Hola, soy [tu nombre], y hoy vamos a hablar de V2X — una tecnología que está revolucionando cómo se comunican los vehículos.

**[Pausa 2 segundos]**

Hace pocas semanas, descubrimos una vulnerabilidad grave en 250,000 balizas Help Flash en España. En este vídeo, te explico qué es V2X, por qué falló en Help Flash, y cómo se protege."

---

## BLOQUE 1: ¿QUÉ ES V2X? (0:30-2:00)

### [Diapositiva 3: Definición]

**Narrador:**
"V2X significa Vehicle-to-Everything. Es decir, vehículos que se comunican.

Hay cuatro tipos principales:

**[Pausa en cada tipo]**

**V2V — Vehicle-to-Vehicle:** Un coche le avisa a otro. Por ejemplo, frenas de emergencia en autopista. Tu coche lo sabe y prepara los frenos. Resultado: menos accidentes en cadena.

**V2I — Vehicle-to-Infrastructure:** Tu coche habla con los semáforos. Ejemplo: llegas a un semáforo en rojo, pero le avisa al semáforo. El semáforo puede ponerse verde, optimizando tráfico. Menos contaminación.

**V2P — Vehicle-to-Pedestrian:** Tu coche detecta peatones. Imagina a alguien cruzando con auriculares, sin ver el coche. El coche lo detecta y le avisa.

**V2N — Vehicle-to-Network:** Tu coche sube datos a la nube. Help Flash hace esto — cuando accidentas, la baliza avisa a emergencias."

### [Diapositiva 4: Protocolos]

**Narrador:**
"¿Cómo se comunican? Hay diferentes 'idiomas' o protocolos.

**DSRC** es como una radio privada de coches. Alcance 100 metros. Latencia baja — respuesta rápida. Usada en AEBak y Japón.

**5G/C-V2X** es el futuro. Usa redes 5G. Alcance 500 metros. Más servicios, más integración. Usada en China, USA.

**NB-IoT** es lo que Help Flash usa en España. Banda estrecha, bajo consumo, largo alcance. Perfecto para IoT... pero con problemas de seguridad."

---

## BLOQUE 2: DÓNDE FALLÓ (2:00-5:00)

### [Diapositiva 7: Desafíos de seguridad]

**Narrador:**
"Help Flash enviaba datos en **texto plano**. Eso significa: tu localización GPS exacta viajaba por internet para que cualquiera la viera.

**Problema 1:** Tenga cuidado. Datos sin cifrar. Si sé dónde está tu baliza, sé dónde ESTÁS TÚ. ¿Y si eres un abogado en un juicio? ¿Una víctima de violencia?

**Problema 2:** Falta de autenticación. ¿Cómo sabe la red que un mensaje viene de una baliza Help Flash real? No lo sabe. Un atacante puede fingir ser una baliza.

**Problema 3:** Suplantación. El IMEI es el ID único de Help Flash. Está impreso en la carcasa. Un atacante lo copia y se convierte en esa baliza. Ahora puede enviar alertas falsas.

**Problema 4:** OTA sin firma. Help Flash recibe actualizaciones de firmware por radio. ¿Problema? No están firmadas. Un atacante inyecta código malicioso."

### [Diapositiva 8: Diagrama de ataque]

**Narrador:**
"Aquí está el flujo de ataque:

[Señala diagrama]

1. Baliza envía GPS en claro
2. Red NB-IoT lo intercepta (parámetros expuestos)
3. Servidor recibe, envía OTA sin firma
4. Baliza acepta código malicioso
5. DGT 3.0 recibe alerta falsa
6. Paneles de autovía muestran congestión falsa

Cada flecha es un punto de fallo. Eso es una 'superficie de ataque'. Muchos puntos, muchas oportunidades para explotar."

---

## BLOQUE 3: LA SOLUCIÓN (5:00-8:00)

### [Diapositiva 13: Soluciones]

**Narrador:**
"¿Cómo se arregla?

**Encriptación (TLS/DTLS):** Poner un candado en la comunicación. Solo el remitente y receptor saben la clave. Como enviar una carta en caja de seguridad vs. postal abierta.

**Autenticación (Certificados):** Cada dispositivo tiene un certificado. Demuestra su identidad. Como tu pasaporte — prueba quién eres.

**Verificación de integridad (HMAC):** Código que verifica que el mensaje no fue alterado. Como una firma en un contrato.

**Firma de actualizaciones OTA:** El fabricante firma CADA actualización. Si no está firmada, la baliza la rechaza. Sin inyección de código malicioso.

**Nonce + Timestamp:** Número único y marca de tiempo en cada mensaje. Previene repetición de mensajes."

### [Diapositiva 14: Resumen]

**Narrador:**
"En resumen:

**Riesgos:** Comunicación en texto plano, sin autenticación, inyección de falsas alertas, actualizaciones sin verificar.

**Soluciones:** Encriptación, autenticación, verificación de integridad, firmas."

---

## BLOQUE 4: REFLEXIÓN FINAL (8:00-10:00)

### [Diapositiva 15: Conclusión]

**Narrador:**
"La tecnología V2X aporta grandes ventajas al sector automotriz. Pero la seguridad debe estar en la base.

En Help Flash, vimos una implementación que falló. 250,000 dispositivos reales afectados.

**¿La lección?** Las nuevas tecnologías se despliegan rápidamente, sin suficientes auditorías de seguridad.

Como futuros ingenieros o analistas de seguridad, vuestra responsabilidad es pensar en esto. Proteger, no dañar.

**[Pausa]**

En nuestra próxima sesión, haremos una práctica donde explotamos estas vulnerabilidades. Apreciarás por qué la seguridad es importante."

---

## CLOSING (10:00-10:30)

**Narrador:**
"Gracias por ver este vídeo. Si tienes preguntas sobre V2X, Help Flash o seguridad en automoción, déjala en comentarios.

Suscríbete para más contenido de ciberseguridad.

[Tu nombre] — [tu email/web]"

---

## 📹 NOTAS DE GRABACIÓN

### Equipo necesario:
- Micrófono de calidad (o auriculares con micrófono)
- Pantalla para mostrar diapositivas (OBS, Zoom screen share)
- Luz frontal (iluminar cara)
- Fondo limpio (blanco o azul)

### Configuración OBS:
1. Abre OBS Studio
2. Añade fuente: "Ventana de navegador" (presentación)
3. Añade fuente: "Dispositivo de video" (webcam)
4. Posiciona webcam en esquina
5. Graba (File > Start Recording)

### Timing:
- Lectura lenta: 1 minuto ≈ 120-140 palabras
- Pausas dramáticas: 2-3 segundos
- Entre bloques: 1-2 segundos
- Final: 3-5 segundos de silencio

### Edición (post-grabación):
- Corta silencios largos
- Añade títulos (Diapositiva X - Tema Y)
- Zoom en detalles importantes
- Música de fondo baja (10-20% volumen)
- Subtítulos (si es posible)

---

## 🎤 PUNTOS DE ÉNFASIS

Di lentamente y con énfasis:

1. **"250,000 dispositivos Help Flash en España"** — dato impactante
2. **"Texto plano"** — repetir 2-3 veces
3. **"Atacante"** — hacer personal (alguien te persigue)
4. **"Seguridad debe estar en la base"** — conclusión clave
5. **"Vuestra responsabilidad"** — llamada a acción

---

## 📊 VARIACIONES DEL SCRIPT

### Versión Corta (5 min):
- Salta Bloque 3 (soluciones)
- Mantén Opening, Bloques 1-2, Closing

### Versión Larga (15 min):
- Añade demo en vivo de Wireshark
- Explica cada línea de código de atacante
- Q&A extendido

### Versión Técnica:
- Enfatiza protocolos (DSRC vs. C-V2X vs. NB-IoT)
- Explicación detallada de criptografía
- Diagramas de flujo más complejos

### Versión Simplificada:
- Quita detalles técnicos
- Usa solo analogías
- Enfatiza impacto en vidas reales

---

## 🌐 TRADUCCIÓN A OTROS IDIOMAS

Si grabas en euskera y quieres traducir a español (o viceversa):

1. Traduce el script palabra por palabra
2. Ajusta pausas (algunas lenguas son más largas)
3. Mantén énfasis en puntos clave
4. Graba separadamente (voz, no subtítulos)

---

## ✅ CHECKLIST ANTES DE GRABAR

- [ ] Script impreso o en pantalla secundaria
- [ ] Micrófono probado (sin ruido de fondo)
- [ ] Iluminación correcta
- [ ] OBS o software de grabación configurado
- [ ] Presentación abierta y lista
- [ ] Cámara web posicionada
- [ ] Agua a mano (para beber entre bloques)
- [ ] Teléfono silenciado
- [ ] Puerta cerrada (sin distracciones)
- [ ] Test de grabación (5 segundos)

---

## 🎬 DESPUÉS DE GRABAR

1. **Exporta** en MP4 (1080p, 30fps)
2. **Revisa** — busca momentos de mejora
3. **Edita** si es necesario (corta silencios, añade títulos)
4. **Sube** a YouTube/Vimeo
5. **Comparte** en GitHub o web educativa
6. **Recopila feedback** — mejora para próximas versiones

---

## 📝 VERSIONES GRABADAS

Fecha de grabación: ____________  
Duración: ____________  
Plataforma: ____________  
Enlaces: ____________  
Feedback: ____________  

---

**Buena suerte grabando. ¡Que te divierta explicando V2X!** 🎥🚗

*Script versión 1.0 — Octubre 2026*
