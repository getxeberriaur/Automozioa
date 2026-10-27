# V2X - Chuleta Rápida para Aula

## Quick Reference / Bilaketa Azkarra

### Archivos creados

```
presentaciones/
├── V2X_Aurkezpena_eu.html          ← Presentación euskera (15 slides)
├── V2X_Presentacion_es.html        ← Presentación español (15 slides)
├── README_V2X.md                   ← Guía de uso
├── GUIA_DOCENTE_V2X.md             ← Guía pedagógica completa
├── PUNTOS_ORADOR.md                ← Speaker notes detalladas
└── CHULETA_RAPIDA.md               ← Este archivo

lab/
└── V2X_Laburpena_Ikasleentzat.md   ← Resumen para estudiantes
```

---

## Cómo abrir las presentaciones

### Opción 1: Directo
```bash
firefox presentaciones/V2X_Aurkezpena_eu.html
```

### Opción 2: Servidor local (mejor para proyector)
```bash
cd /home/geu/Dokumentuak/GitHub/Automozioa/Automocion_V16_Ciber
python3 -m http.server 8000
# Abre en navegador: http://localhost:8000/presentaciones/V2X_Aurkezpena_eu.html
```

---

## Controles de Navegación

| Acción | Método |
|--------|--------|
| Siguiente diapositiva | Botón "Hurrengoa" o Flecha → |
| Anterior diapositiva | Botón "Aurrekoa" o Flecha ← |
| Ir a diapositiva X | Hacer clic en punto (dot) |
| Pantalla completa | F11 |
| Cerrar pantalla completa | F11 o ESC |

---

## Estructura de la Presentación

**Bloque 1: Introducción (5 min)**
- Diapositivas 1-2: Portada y qué es V2X

**Bloque 2: Conceptos (7 min)**
- Diapositivas 3-5: Definición, protocolos, aplicaciones

**Bloque 3: Seguridad (7 min)**
- Diapositivas 6-8: Desafíos, vulnerabilidades, superficie de ataque

**Bloque 4: Práctica (8 min)**
- Diapositivas 9-12: Descripción del lab, setup, demo

**Bloque 5: Soluciones (8 min)**
- Diapositivas 13-15: Soluciones, aprendizajes, conclusión

**Tiempo total: 30-40 minutos**

---

## Preguntas Clave para hacer al Aula

| Diapositiva | Pregunta |
|-------------|----------|
| 2 | ¿Alguien ha oído hablar de V2X? |
| 3 | ¿Cuál de estos tipos (V2V, V2I, V2P, V2N) es más importante? |
| 7 | ¿Cuál de estos problemas (encriptación, autenticación, etc.) es más grave? |
| 10 | ¿Se puede hackear Help Flash en una sesión de lab? |
| 13 | ¿Cuál es la solución más importante? |
| 15 | ¿Qué responsabilidad tenemos como ingenieros/analistas? |

---

## Puntos Críticos a Enfatizar

1. **Help Flash es REAL**
   - 250,000+ dispositivos en España
   - CVE-2025-65855 descubierto en 2025
   - Afecta a personas reales

2. **Tenga cuidado: Comunicación en claro**
   - GPS en texto plano = localización expuesta
   - IMEI duplicable = identidad falsificable

3. **OTA sin firma**
   - Actualizaciones sin validar = código malicioso inyectable
   - Esto es crítico

4. **Soluciones son criptografía**
   - Encriptación (TLS/DTLS)
   - Autenticación (certificados)
   - Integridad (HMAC)
   - Firma (OTA seguro)

---

## Materiales de Soporte

### Para distribuir a estudiantes:
- `lab/V2X_Laburpena_Ikasleentzat.md` — Resumen en 1 página

### Para referencia durante presentación:
- `presentaciones/PUNTOS_ORADOR.md` — Speaker notes por diapositiva
- `presentaciones/GUIA_DOCENTE_V2X.md` — Guía pedagógica completa

### Para después (práctica):
- `lab/05_Demo_Vulnerabilidades_Help_Flash.md` — Práctica Help Flash

---

## Requisitos Técnicos

- Navegador moderno (Chrome, Firefox, Safari, Edge)
- Pantalla: mínimo 1024×768 (recomendado 1920×1080)
- Internet: NO necesario (HTML/CSS/JS locales)
- Proyector: probado antes de sesión

---

## Colores de la Presentación

| Sección | Gradiente |
|---------|-----------|
| Portada | Azul-púrpura |
| Secciones | Rosa-rojo |
| Contenido | Azul-gris |

Todos los colores tienen suficiente contraste para lectura.

---

## Personalización

Para editar:

### Cambiar contenido:
- Abre el HTML en editor de texto (VS Code)
- Busca `<div class="slide">` para cada diapositiva
- Modifica texto dentro

### Cambiar colores:
- Busca `background: linear-gradient()` en `<style>`
- Modifica valores de color (hex o rgba)

### Cambiar fuentes:
- Busca `font-family:` en `<style>`
- Modifica a tu fuente preferida

### Añadir diapositivas:
- Copia un `<div class="slide">` completo
- Modifica clase (title-slide, section-slide, content-slide)
- Cambia contenido

---

## Checklist Antes de Presentación

- [ ] Navegador abierto con presentación
- [ ] Proyector conectado y probado
- [ ] Pantalla en 16:9 (no 4:3)
- [ ] Sonido probado (si usas audio)
- [ ] Baliza Help Flash física (optional pero impactante)
- [ ] Wireshark abierto (para demo)
- [ ] Reloj/cronómetro a vista
- [ ] Agua para beber
- [ ] Micrófono (si aula grande)
- [ ] Documentos impresos o digitales de resumen para repartir

---

## Timing Recomendado

| Bloque | Tiempo | Notas |
|--------|--------|-------|
| Presentación total | 35 min | Sin Q&A |
| Q&A | 5-10 min | Dejar tiempo |
| Prep sala | 5 min | Antes de empezar |
| Transición a práctica | 5 min | Después de presentación |

---

## Contacto / Referencia

Si necesitas:
- **Editar contenido:** Abre archivo HTML o .md en VS Code
- **Añadir ejemplos:** Referencia a `05_Demo_Vulnerabilidades_Help_Flash.md`
- **Más información:** Busca CVE-2025-65855 en web

---

## Idiomas

- **Euskera:** `V2X_Aurkezpena_eu.html`
- **Español:** `V2X_Presentacion_es.html`

Ambas tienen **exactamente el mismo contenido**, solo en diferente idioma.

---

**Creada:** Octubre 2026  
**Autor:** Equipo Educativo Automozioa  
**Versión:** 1.0
