# V2X - Paquete Educativo Completo
## Complete Educational Package

---

## 📚 Índice de Materiales / Materialen Aurkibidea

Esta carpeta contiene un paquete educativo **completo** para enseñar V2X (Vehicle-to-Everything) en el contexto de seguridad automotriz, contextualizando la **práctica Help Flash (CVE-2025-65855)**.

### Archivo: Estructura

```
Automocion_V16_Ciber/
│
├── presentaciones/                    ← Diapositivas interactivas
│   ├── V2X_Aurkezpena_eu.html         [ABRE AQUÍ - Euskera]
│   ├── V2X_Presentacion_es.html       [ABRE AQUÍ - Español]
│   ├── README_V2X.md                  Guía de uso y características
│   ├── GUIA_DOCENTE_V2X.md            Guía pedagógica (45 págs)
│   ├── PUNTOS_ORADOR.md               Speaker notes por diapositiva
│   └── CHULETA_RAPIDA.md              Quick reference en aula
│
├── lab/
│   ├── V2X_Laburpena_Ikasleentzat.md  Resumen para estudiantes
│   ├── 05_Demo_Vulnerabilidades_Help_Flash.md      [Práctica Help Flash ES]
│   └── 05_Demo_Ahultasunak_Help_Flash_eu.md        [Práctica Help Flash EU]
│
└── scripts/
    └── fake_ota_server.py             Script OTA simulado (Help Flash)
```

---

## 🚀 Inicio Rápido / Hastapen Azkarra

### 1. Abre la presentación (30-45 min)

```bash
# Opción A: Directo
firefox Automocion_V16_Ciber/presentaciones/V2X_Aurkezpena_eu.html

# Opción B: Servidor local (mejor para proyector)
cd /home/geu/Dokumentuak/GitHub/Automozioa
python3 -m http.server 8000
# Luego: http://localhost:8000/Automocion_V16_Ciber/presentaciones/V2X_Aurkezpena_eu.html
```

### 2. Navega con teclado o botones

- Flecha `→` = siguiente diapositiva
- Flecha `←` = anterior diapositiva
- Puntos (dots) = ir a diapositiva específica
- F11 = pantalla completa

### 3. Abre PUNTOS_ORADOR.md en otra pestaña

Para speaker notes detalladas de cada diapositiva.

### 4. Después: Dirige la práctica

Abre `05_Demo_Vulnerabilidades_Help_Flash.md` para el laboratorio.

---

## 📋 Contenido de Cada Material

### **Presentaciones HTML (15 diapositivas)**

#### `V2X_Aurkezpena_eu.html` (Euskera)
- 15 diapositivas interactivas
- Gradientes visuales atractivos
- Navegación fluida
- Tablas, diagramas, boxes

#### `V2X_Presentacion_es.html` (Español)
- Mismo contenido que euskera
- Interfaz idéntica
- Colores y diseño profesional

**Temas cubiertos:**
1. Portada
2. ¿Qué es V2X?
3. Definición y tipos (V2V, V2I, V2P, V2N)
4. Protocolos (DSRC, 5G, NB-IoT)
5. Aplicaciones reales mundiales
6. Seguridad en V2X
7. Desafíos (Help Flash case)
8. Superficie de ataque (diagrama)
9. Práctica de laboratorio
10. Descripción general
11. Configuración
12. Demostración en vivo
13. Soluciones
14. Aprendizajes clave
15. Conclusión

### **README_V2X.md**
- Descripción de cada presentación
- Cómo abrir y navegar
- Estructura pedagógica
- Recursos adicionales
- Requisitos técnicos

### **GUIA_DOCENTE_V2X.md** ⭐ MÁS IMPORTANTE
- Guía pedagógica completa (45+ páginas)
- Objetivos de aprendizaje
- Flujo de sesión por bloque
- Notas para cada diapositiva
- Preguntas interactivas
- Estrategias de engagement
- Checklist previo
- Adaptaciones (tiempo corto/largo, público técnico/gerencial)

### **PUNTOS_ORADOR.md**
- Speaker notes detalladas
- Qué decir en cada diapositiva
- Preguntas sugeridas
- Pausas recomendadas
- Timing total
- Preguntas frecuentes

### **CHULETA_RAPIDA.md**
- Quick reference para aula
- Archivos creados
- Cómo abrir
- Estructura de presentación
- Preguntas clave
- Puntos críticos
- Checklist antes de presentación

### **V2X_Laburpena_Ikasleentzat.md**
- Resumen de 1 página para distribuir a estudiantes
- Conceptos clave
- Tabla de protocolos
- Problemas y soluciones
- 11 puntos clave
- Objetivos de aprendizaje

### **05_Demo_Vulnerabilidades_Help_Flash.md**
- Práctica completa de Help Flash
- CVE-2025-65855
- Descripción de vulnerabilidades
- Steps para explotar
- Materiales necesarios
- Resultado esperado

---

## 🎯 Cómo usar este Paquete

### Flujo Completo (2-3 horas)

**Sesión 1: Presentación (45 min)**
1. Abre `V2X_Aurkezpena_eu.html` o `V2X_Presentacion_es.html`
2. Consulta `GUIA_DOCENTE_V2X.md` y `PUNTOS_ORADOR.md` mientras presentas
3. Imprime `V2X_Laburpena_Ikasleentzat.md` para distribuir
4. Deja espacio para Q&A

**Sesión 2: Práctica (1.5-2 horas)**
- Abre `05_Demo_Vulnerabilidades_Help_Flash.md`
- Sigue los pasos con los estudiantes
- Usa baliza Help Flash real (si disponible)
- Ejecuta `fake_ota_server.py` para demostración

**Opcional: Verificación**
- Preguntas de la guía pedagógica
- Ejercicios adicionales
- Debate sobre seguridad ética

### Flujo Corto (30 min presentación + lab después)

- Presenta diapositivas 1-5, 13-15 (conceptos y soluciones)
- Salta detalles técnicos
- Enfatiza Help Flash real
- Dirige práctica inmediatamente después

### Flujo Largo (60+ min presentación + demo en vivo)

- Presenta todas las diapositivas lentamente
- Debate después de cada bloque
- Demo en vivo de Wireshark (Diapositiva 12)
- Q&A extenso
- Práctica más profunda

---

## 🛠️ Requisitos Técnicos

### Para la Presentación:
- Navegador moderno (Chrome, Firefox, Safari, Edge)
- Pantalla: mínimo 1024×768 (recomendado 1920×1080)
- Proyector (opcional pero recomendado)
- Sin conexión a internet necesaria

### Para la Práctica:
- Baliza Help Flash IoT (por cada grupo)
- Ordenador Linux (Ubuntu/Kali) con WiFi
- Wireshark instalado
- Python 3.8+
- `fake_ota_server.py` disponible

---

## 📊 Estadísticas del Paquete

| Componente | Detalle |
|---|---|
| Diapositivas | 15 (en 2 idiomas) |
| Páginas guía docente | ~45 |
| Speaker notes | 1 archivo completo |
| Resúmenes estudiantes | 1 página |
| Tiempo presentación | 30-45 min |
| Tiempo práctica | 1.5-2 horas |
| Idiomas | Euskera + Español |
| Interactividad | 100% (HTML5 vanilla) |
| Dependencias externas | 0 |

---

## 🎓 Objetivos de Aprendizaje

Al terminar esta sesión + práctica, los estudiantes podrán:

- ✅ Definir V2X y sus tipos (V2V, V2I, V2P, V2N)
- ✅ Explicar protocolos V2X (DSRC, 5G, NB-IoT)
- ✅ Identificar vulnerabilidades en Help Flash
- ✅ Explicar superficie de ataque en IoT
- ✅ Proponer soluciones criptográficas
- ✅ Implementar ataque a Help Flash (práctica)
- ✅ Reflexionar sobre seguridad ética

---

## 🔐 Consideraciones de Seguridad Ética

### ⚠️ Importante:

Este material educativo está diseñado para:
- **Investigación académica** en seguridad automotriz
- **Educación** en ciberseguridad
- **Auditoría responsable** de sistemas IoT
- **Conciencia** sobre vulnerabilidades reales

### ❌ NO para:

- Atacar Help Flash u otros sistemas reales sin autorización
- Inyectar código malicioso en dispositivos reales
- Interferir con sistemas de emergencia
- Otros propósitos ilegales

**Responsabilidad:** Los estudiantes deben usar este conocimiento ética y legalmente.

---

## 📞 Contacto / Referencia

### Si necesitas:

- **Editar contenido:** Abre archivos HTML o .md en VS Code
- **Más información técnica:** Busca CVE-2025-65855
- **Información Help Flash:** https://www.helpflash.es
- **Estándares V2X:** Busca IEEE 802.11p, 3GPP C-V2X

### Estructura del repositorio:

```
GitHub Automozioa
└── Automocion_V16_Ciber
    ├── presentaciones/     ← Diapositivas (AQUÍ)
    ├── lab/                ← Prácticas
    └── scripts/            ← Herramientas
```

---

## 🌐 Idiomas Disponibles

| Idioma | Archivo |
|--------|---------|
| Euskera 🇪🇸 | `V2X_Aurkezpena_eu.html` |
| Español 🇪🇸 | `V2X_Presentacion_es.html` |

Ambas versiones tienen contenido idéntico, solo lenguaje diferente.

---

## ✅ Checklist Antes de Usar

- [ ] Descargaste toda la carpeta `Automocion_V16_Ciber`
- [ ] Tienes navegador moderno instalado
- [ ] Probaste abrir una presentación HTML
- [ ] Leíste `GUIA_DOCENTE_V2X.md`
- [ ] Imprimiste o preparaste `V2X_Laburpena_Ikasleentzat.md` para estudiantes
- [ ] Probaste proyector (si lo usas)
- [ ] Tienes material Help Flash (si es para práctica)
- [ ] Leíste consideraciones éticas (arriba)

---

## 📝 Versión y Licencia

**Versión:** 1.0 (Octubre 2026)  
**Autor:** Equipo Educativo Automozioa  
**Licencia:** Educational (Código Abierto — ver repo principal)

---

## 🚀 ¡Listo para empezar!

```bash
# 1. Abre la presentación:
firefox Automocion_V16_Ciber/presentaciones/V2X_Aurkezpena_eu.html

# 2. Pantalla completa:
# Presiona F11

# 3. Navega:
# Usa flechas del teclado o botones

# 4. ¡Presenta!
```

**¡Mucho éxito en tu sesión de V2X!** 🎓🚗💡

---

*Creado con educación en mente. Para preguntas, consulta la guía pedagógica.*
