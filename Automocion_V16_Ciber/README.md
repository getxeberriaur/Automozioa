# Automozioa

[Versión en euskara](README_eu.md)

Repositorio de apoyo para materiales docentes y laboratorio práctico sobre ciberseguridad en automoción, con foco en eventos conectados de balizas V16 en entorno simulado.

## Objetivo

Este repositorio está pensado para:

- apoyar sesiones docentes introductorias sobre ciberseguridad en sistemas ITS y automoción conectada;
- proporcionar un guion de laboratorio controlado, reproducible y orientado a defensa;
- servir como base para construir una práctica local con backend, simulador y evidencias.

> Importante: todo el contenido está orientado a formación defensiva en sandbox local o red aislada. No debe utilizarse sobre infraestructuras reales.

## Contenido actual

En esta primera versión, el repositorio contiene documentación base para preparar una sesión docente y un laboratorio de 2 horas:

- [Automocion_V16_Ciber/materiales/00_Guion_intro_30min.md](Automocion_V16_Ciber/materiales/00_Guion_intro_30min.md): guion de introducción de 30 minutos.
- [Automocion_V16_Ciber/materiales/01_Laboratorio_2h.md](Automocion_V16_Ciber/materiales/01_Laboratorio_2h.md): diseño del laboratorio práctico.
- [Automocion_V16_Ciber/lab/02_Checklist_configuracion_laboratorio.md](Automocion_V16_Ciber/lab/02_Checklist_configuracion_laboratorio.md): checklist docente de preparación.
- [Automocion_V16_Ciber/lab/03_Setup_rapido_windows.md](Automocion_V16_Ciber/lab/03_Setup_rapido_windows.md): guía rápida de referencia para Windows.

## Índice de documentación

### Documentación en castellano

- [Automocion_V16_Ciber/RUN_ME_FIRST.md](Automocion_V16_Ciber/RUN_ME_FIRST.md)
- [Automocion_V16_Ciber/materiales/00_Guion_intro_30min.md](Automocion_V16_Ciber/materiales/00_Guion_intro_30min.md)
- [Automocion_V16_Ciber/materiales/01_Laboratorio_2h.md](Automocion_V16_Ciber/materiales/01_Laboratorio_2h.md)
- [Automocion_V16_Ciber/lab/02_Checklist_configuracion_laboratorio.md](Automocion_V16_Ciber/lab/02_Checklist_configuracion_laboratorio.md)
- [Automocion_V16_Ciber/lab/03_Setup_rapido_windows.md](Automocion_V16_Ciber/lab/03_Setup_rapido_windows.md)
- [Automocion_V16_Ciber/lab/05_Demo_Vulnerabilidades_Help_Flash.md](Automocion_V16_Ciber/lab/05_Demo_Vulnerabilidades_Help_Flash.md) — Demo CVE-2025-65855 (docente)

### Documentación en euskara

- [README_eu.md](README_eu.md)
- [Automocion_V16_Ciber/materiales/00_Guion_intro_30min_eu.md](Automocion_V16_Ciber/materiales/00_Guion_intro_30min_eu.md)
- [Automocion_V16_Ciber/materiales/01_Laboratorio_2h_eu.md](Automocion_V16_Ciber/materiales/01_Laboratorio_2h_eu.md)
- [Automocion_V16_Ciber/lab/02_Checklist_configuracion_laboratorio_eu.md](Automocion_V16_Ciber/lab/02_Checklist_configuracion_laboratorio_eu.md)
- [Automocion_V16_Ciber/lab/03_Setup_rapido_windows_eu.md](Automocion_V16_Ciber/lab/03_Setup_rapido_windows_eu.md)

## Estructura del repositorio

```text
Automozioa/
├─ README_eu.md
├─ README.md
└─ Automocion_V16_Ciber/
	├─ backend/
	│  └─ app.py
	├─ lab/
	│  ├─ 02_Checklist_configuracion_laboratorio.md
	│  ├─ 02_Checklist_configuracion_laboratorio_eu.md
	│  ├─ 03_Setup_rapido_windows.md
	│  └─ 03_Setup_rapido_windows_eu.md
	├─ logs/
	│  └─ .gitkeep
	└─ materiales/
		├─ 00_Guion_intro_30min.md
		├─ 00_Guion_intro_30min_eu.md
		├─ 01_Laboratorio_2h.md
		└─ 01_Laboratorio_2h_eu.md
	├─ reports/
	│  └─ .gitkeep
	├─ samples/
	│  └─ event_legitimo.json
	├─ simulator/
	│  └─ send_event.py
	├─ requirements.txt
	└─ RUN_ME_FIRST.md
```

## Público objetivo

Especialmente útil para:

- profesorado de FP, universidad o formación técnica;
- equipos que quieran montar una demostración local de seguridad en automoción conectada;
- actividades de sensibilización sobre validación de eventos, trazabilidad y hardening básico.

## Enfoque pedagógico

El laboratorio propuesto compara dos situaciones:

1. un backend con validaciones insuficientes;
2. el mismo backend con controles defensivos activados.

Los controles que se trabajan en la documentación incluyen:

- validación estricta de esquema JSON;
- validación de coordenadas;
- ventana temporal para `timestamp`;
- prevención de replay mediante `nonce`;
- rate limiting por identidad;
- logging con motivo de aceptación o rechazo.

## Cómo usar este repositorio

### Opción 1: solo material docente

Si quieres usarlo solo como soporte de clase:

1. revisa el guion de introducción en [Automocion_V16_Ciber/materiales/00_Guion_intro_30min.md](Automocion_V16_Ciber/materiales/00_Guion_intro_30min.md);
2. adapta la sesión práctica con [Automocion_V16_Ciber/materiales/01_Laboratorio_2h.md](Automocion_V16_Ciber/materiales/01_Laboratorio_2h.md);
3. utiliza la checklist de [Automocion_V16_Ciber/lab/02_Checklist_configuracion_laboratorio.md](Automocion_V16_Ciber/lab/02_Checklist_configuracion_laboratorio.md) antes de impartirla.

### Opción 2: evolucionarlo a laboratorio ejecutable

Siguiente evolución recomendada del repositorio:

- crear `backend/` para la API local de ingestión;
- crear `simulator/` para generar eventos legítimos y de prueba;
- crear `logs/` para trazabilidad;
- crear `reports/` para evidencias de cada equipo;
- añadir `requirements.txt` y ejemplos de payloads.

## Flujo de laboratorio previsto

El flujo objetivo es el siguiente:

1. el simulador genera un evento;
2. el backend valida formato, tiempo, identidad y política;
3. el backend decide `accepted` o `rejected`;
4. la decisión se registra en logs;
5. el equipo documenta evidencias y conclusiones.

## Resultados de aprendizaje esperados

Al trabajar con este material, el alumnado o profesorado participante debería poder:

- identificar activos críticos en un sistema conectado de automoción;
- diferenciar spoofing, replay e inyección de datos inválidos;
- aplicar controles básicos de validación y trazabilidad;
- interpretar logs como evidencia técnica;
- justificar mitigaciones y riesgo residual.

## Estado del repositorio

Estado actual:

- documentación docente: disponible;
- guion del laboratorio: disponible;
- backend mínimo de referencia: disponible;
- simulador de pruebas: disponible;
- plantillas de evidencias: pendiente.

## Implementación mínima disponible

El repositorio ya incluye una primera base ejecutable:

- [Automocion_V16_Ciber/backend/app.py](Automocion_V16_Ciber/backend/app.py): API local con validación de esquema, ventana temporal, control anti-replay, control de tasa y logging.
- [Automocion_V16_Ciber/simulator/send_event.py](Automocion_V16_Ciber/simulator/send_event.py): simulador con escenarios `legitimo`, `replay`, `timestamp-atrasado`, `coordenadas-invalidas`, `identidad-invalida` y `rafaga`.
- [Automocion_V16_Ciber/samples/event_legitimo.json](Automocion_V16_Ciber/samples/event_legitimo.json): ejemplo de payload.
- [Automocion_V16_Ciber/RUN_ME_FIRST.md](Automocion_V16_Ciber/RUN_ME_FIRST.md): arranque rápido.
- [Automocion_V16_Ciber/requirements.txt](Automocion_V16_Ciber/requirements.txt): dependencias del laboratorio.

## Próximos pasos recomendados

1. completar la implementación mínima en Python;
2. añadir ejemplos de eventos válidos e inválidos;
3. preparar una plantilla de informe para `reports/`;
4. incluir instrucciones de arranque rápido para cada equipo;
5. validar el laboratorio en un entorno Windows real antes de impartirlo.

## Principios de seguridad y ética

- Solo entornos locales, simulados o aislados.
- Prohibido usar estos materiales contra sistemas reales.
- Objetivo exclusivamente formativo y defensivo.
- La práctica debe centrarse en validación, hardening, detección y respuesta.

## Licencia y uso

Si vas a reutilizar este material en un centro educativo, conviene añadir una licencia explícita al repositorio y, si quieres, una nota de autoría o contribución.