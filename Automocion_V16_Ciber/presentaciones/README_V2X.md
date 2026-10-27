# Presentaciones V2X | V2X Presentazioak

## Español (Spanish)

### Descripción

Estas presentaciones HTML5 interactivas explican la tecnología **V2X (Vehicle-to-Everything)** en el contexto de la seguridad de sistemas automotivos. Están diseñadas para contextualizar la **práctica de laboratorio sobre vulnerabilidades en balizas IoT (Help Flash)** y explicar cómo funcionan las comunicaciones vehiculares inseguras.

### Archivos

- **`V2X_Presentacion_es.html`** — Presentación en español (15 diapositivas)
- **`V2X_Aurkezpena_eu.html`** — Presentación en euskera (15 diapositivas)

### Cómo usar

1. **Abrir en navegador:**
   ```bash
   # Opción 1: Abrir archivo directamente
   firefox V2X_Presentacion_es.html
   
   # Opción 2: Servir localmente (recomendado para proyector)
   python3 -m http.server 8000
   # Luego abre: http://localhost:8000/V2X_Presentacion_es.html
   ```

2. **Navegar por diapositivas:**
   - **Botones:** "Anterior" y "Siguiente" en la parte inferior
   - **Puntos:** Haz clic en cualquier punto para ir a esa diapositiva
   - **Teclado:** Usa las flechas `←` y `→` para navegar
   - **Pantalla completa:** F11 (en la mayoría de navegadores)

3. **En el aula:**
   - Proyecta la presentación en pantalla grande
   - Usa los botones o teclado para navegar
   - Pausa en cada diapositiva para explicar y responder preguntas
   - Las diapositivas están numeradas (p. ej., "3/15")

### Contenido de las diapositivas

| Diapositiva | Tema | Duración sugerida |
|---|---|---|
| 1 | Portada: V2X Tecnología | 1 min |
| 2 | Sección: ¿Qué es V2X? | - |
| 3 | Definición y tipos (V2V, V2I, V2P, V2N) | 3 min |
| 4 | Protocolos (DSRC, 5G/C-V2X) | 2 min |
| 5 | Aplicaciones reales mundiales | 2 min |
| 6 | Sección: V2X y Seguridad | - |
| 7 | Desafíos de seguridad (Help Flash case) | 3 min |
| 8 | Superficie de ataque (diagrama) | 2 min |
| 9 | Sección: Nuestra práctica de laboratorio | - |
| 10 | Descripción general de la práctica | 3 min |
| 11 | Configuración y objetivos | 2 min |
| 12 | Demostración en vivo | 1 min |
| 13 | Soluciones y mejoras | 3 min |
| 14 | Aprendizajes clave (resumen) | 2 min |
| 15 | Conclusión | 1 min |

**Tiempo total:** ~30-40 minutos (sin incluir preguntas y debates)

### Estructura pedagógica

1. **Introducción (5 min)**
   - Portada y presentación general de V2X

2. **Conceptos fundamentales (7 min)**
   - Qué es V2X, tipos de comunicación, protocolos
   - Aplicaciones reales en el mundo

3. **Seguridad y vulnerabilidades (7 min)**
   - Desafíos de seguridad
   - Superficie de ataque

4. **Práctica de laboratorio (8 min)**
   - Contexto: qué van a explotar los estudiantes
   - Cómo funciona el laboratorio
   - Objetivos de aprendizaje

5. **Soluciones (8 min)**
   - Cómo debería implementarse
   - Aprendizajes clave
   - Conclusión

### Recursos adicionales (relacionados)

- **Práctica Help Flash:** `lab/05_Demo_Vulnerabilidades_Help_Flash.md` (español)
- **Práctica Help Flash:** `lab/05_Demo_Ahultasunak_Help_Flash_eu.md` (euskera)
- **Scripts:** `scripts/fake_ota_server.py` (servidor OTA simulado)

### Personalización

Puedes editar las presentaciones directamente en el HTML si necesitas:

- Cambiar colores: busca `background: linear-gradient(...)` en la sección `<style>`
- Añadir/eliminar diapositivas: copia un `<div class="slide">` y modifica el contenido
- Cambiar fuentes: busca `font-family:` en `<style>`
- Ajustar tamaños: modifica valores de `font-size` en las clases `h1`, `h2`, etc.

### Requisitos técnicos

- Navegador moderno (Chrome, Firefox, Safari, Edge)
- Conexión a internet **no necesaria** (HTML/CSS/JS locales)
- Pantalla de al menos 1024×768 (recomendado 1920×1080 para proyector)
- Altavoces (opcional, para video de demostración si lo añades)

---

## Euskera (Basque)

### Deskribapena

HTML5 aurkezpen interaktiboak **V2X (Vehicle-to-Everything)** teknologia azaltzen dute automozioa seguritate testuinguruan. **IoT balizetan kalteen praktika (Help Flash)** testualizatzeko diseinatuak daude, eta nola funtzionatzen duten ibilgailuen komunikazio kalten ditzuke azaldu.

### Fitxategiak

- **`V2X_Presentacion_es.html`** — Aurkezpena gaztelaniaz (15 diapositiba)
- **`V2X_Aurkezpena_eu.html`** — Aurkezpena euskaraz (15 diapositiba)

### Nola erabili

1. **Nabigatzailean ireki:**
   ```bash
   # Aukera 1: Fitxategiak zuzenean ireki
   firefox V2X_Aurkezpena_eu.html
   
   # Aukera 2: Lokalean zerbitzua (gomendatua proiektorerentzat)
   python3 -m http.server 8000
   # Ondoren: http://localhost:8000/V2X_Aurkezpena_eu.html
   ```

2. **Diapositibetan nabigatu:**
   - **Botoiak:** "Aurrekoa" eta "Hurrengoa" behean
   - **Puntua:** Egin klik diapositiba batera joatzeko
   - **Teklatua:** `←` eta `→` gakoak erabili nabigatzeko
   - **Pantaila osoa:** F11 (gehienetan)

3. **Gelan:**
   - Proiektatu aurkezpena pantaila handian
   - Botoiak edo teklatua erabili nabigatzeko
   - Pausatu diapositiba bakoitzean azaltzeko eta galderentzat
   - Diapositibak zenbakituak daude ("3/15" adibidez)

### Diapositiben edukia

| Diapositiba | Gaia | Denbora |
|---|---|---|
| 1 | Azala: V2X Teknologia | 1 min |
| 2 | Atala: Zer da V2X? | - |
| 3 | Definizioa eta motak (V2V, V2I, V2P, V2N) | 3 min |
| 4 | Protokoloak (DSRC, 5G/C-V2X) | 2 min |
| 5 | Erreale aplikazioak munduan | 2 min |
| 6 | Atala: V2X eta Seguritatea | - |
| 7 | Seguritate erronkak (Help Flash kasua) | 3 min |
| 8 | Atake aztarnagusia (diagrama) | 2 min |
| 9 | Atala: Gure laboratorio praktika | - |
| 10 | Praktikaren deskribapena orokorra | 3 min |
| 11 | Konfigurazioa eta helburuak | 2 min |
| 12 | Demostrazioa bizi | 1 min |
| 13 | Soluzio eta hobeak | 3 min |
| 14 | Ikasitako gakoetara (laburpena) | 2 min |
| 15 | Ondorioa | 1 min |

**Denbora osoa:** ~30-40 minutu (galderak eta desberdintzak ez dira sartuak)

### Pedagogia egitura

1. **Sarrera (5 min)**
   - Azala eta V2X-en aurkezpen orokorra

2. **Oinarrizko kontzeptuak (7 min)**
   - Zer da V2X, komunikazio motak, protokoloak
   - Erreale aplikazioak munduan

3. **Seguritatea eta kalteen (7 min)**
   - Seguritate erronkak
   - Atake aztarnagusia

4. **Laboratorio praktika (8 min)**
   - Testuingura: zer esplotatuko duten ikasleek
   - Nola funtzionatzen du laboratoriak
   - Ikasketaren helburuak

5. **Soluzio (8 min)**
   - Nola inplementatu beharko litzateke
   - Ikasitako gakoetara
   - Ondorioa

### Baliabide osagarria (lotuta)

- **Help Flash praktika:** `lab/05_Demo_Vulnerabilidades_Help_Flash.md` (gaztelaniaz)
- **Help Flash praktika:** `lab/05_Demo_Ahultasunak_Help_Flash_eu.md` (euskaraz)
- **Skriptak:** `scripts/fake_ota_server.py` (simulatutako OTA zerbitzaria)

### Pertsonalizazioa

Zuzenean editatu ahal ditzakezu aurkezpenak HTML-en jarraitu behar bada:

- Kolore aldatzea: bilatu `background: linear-gradient(...)` `<style>` atalean
- Diapositibak gehitzea/ezabatzea: kopiatu `<div class="slide">` eta aldatu edukia
- Letra-tipoa aldatzea: bilatu `font-family:` `<style>` atalean
- Tamaina zuzentzea: aldatu `font-size` balioak `h1`, `h2` klasetan, etab.

### Teknika baldintzak

- Nabigatzaile modernoa (Chrome, Firefox, Safari, Edge)
- Interneta konexioa **ez dira beharrezkoa** (HTML/CSS/JS lokalak)
- Pantaila gutxienez 1024×768 (gomendiatu 1920×1080 proiektorerentzat)
- Altabozak (aukerakoa, demostrazioa bideoagatik gehitzekotan)

---

## Notas técnicas / Noten teknikoa

### Estilo y diseño

Ambas presentaciones usan:
- **Gradientes de color** para diapositivas atractivas
- **Animaciones suaves** (fade-in de 0.5s) al cambiar diapositivas
- **Responsive design** para ajustarse a pantallas pequeñas (responsive hasta 768px)
- **Tablas con hover effects** para mejor interactividad
- **Tipografía clara** (Segoe UI para máxima legibilidad)

### Navegación

- **JavaScript vanilla** (sin dependencias)
- **Navegación por puntos** (dots) rápida
- **Contador de diapositivas** en tiempo real
- **Botones deshabilitados** al llegar al inicio/fin
- **Atajo de teclado:** ← (anterior) y → (siguiente)

### Accesibilidad

- Textos con suficiente contraste
- Tamaños de fuente escalables
- Estructura HTML semántica
- Compatible con lectores de pantalla (parcialmente)

---

## Licencia / Lizentzia

Estos documentos forman parte del repositorio **Automozioa** (educativo, código abierto).

---

## Contacto / Kontaktua

Para sugerencias o correcciones, abre un issue en GitHub o contacta al instructor.

Para iradokizunak edo zuzenketak, ireki GitHub-en isue bat edo kontaktatu instructorra.
