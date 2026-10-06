# Automozioa

[Versión en euskara](README_eu.md)

Repositorio de apoyo para materiales docentes y laboratorio práctico sobre ciberseguridad en automoción, con foco en eventos conectados de balizas V16 en entorno simulado.

## Objetivo

Este repositorio está pensado para:

- apoyar sesiones docentes introductorias sobre ciberseguridad en sistemas ITS y automoción conectada;
- proporcionar un guion de laboratorio controlado, reproducible y orientado a defensa;
- servir como base para construir una práctica local con backend, simulador y evidencias.

> Importante: todo el contenido está orientado a formación defensiva en sandbox local o red aislada. No debe utilizarse sobre infraestructuras reales.

## Práctica

Sigue el [arranque rápido](RUN_ME_FIRST.md). La API local, el simulador, el evento de muestra y las plantillas de informe están incluidos en esta carpeta.

## Recorrido

1. Lee [RUN_ME_FIRST.md](RUN_ME_FIRST.md).
2. Realiza los escenarios con `simulator/send_event.py`.
3. Revisa `logs/events.log` y entrega el informe de [reports/00_Plantilla_informe_evidencias.md](reports/00_Plantilla_informe_evidencias.md).

## Público

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

## Ejecución

El laboratorio se ejecuta localmente en `127.0.0.1`. No lo conectes a servicios externos ni envíes eventos a sistemas reales.

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

## Componentes

- `backend/app.py`: API local con validación y registro de decisiones.
- `simulator/send_event.py`: escenarios legítimo, replay, timestamp, coordenadas, identidad y ráfaga.
- `samples/event_legitimo.json`: payload de referencia.
- `reports/`: plantillas de evidencias en castellano y euskara.

## Implementación mínima disponible

El repositorio ya incluye una primera base ejecutable:

- [Automocion_V16_Ciber/backend/app.py](backend/app.py): API local con validación de esquema, ventana temporal, control anti-replay, control de tasa y logging.
- [Automocion_V16_Ciber/simulator/send_event.py](simulator/send_event.py): simulador con escenarios `legitimo`, `replay`, `timestamp-atrasado`, `coordenadas-invalidas`, `identidad-invalida` y `rafaga`.
- [Automocion_V16_Ciber/samples/event_legitimo.json](samples/event_legitimo.json): ejemplo de payload.
- [Automocion_V16_Ciber/RUN_ME_FIRST.md](RUN_ME_FIRST.md): arranque rápido.
- [Automocion_V16_Ciber/requirements.txt](requirements.txt): dependencias del laboratorio.

## Principios de seguridad y ética

- Solo entornos locales, simulados o aislados.
- Prohibido usar estos materiales contra sistemas reales.
- Objetivo exclusivamente formativo y defensivo.
- La práctica debe centrarse en validación, hardening, detección y respuesta.

## Licencia y uso

Si vas a reutilizar este material en un centro educativo, conviene añadir una licencia explícita al repositorio y, si quieres, una nota de autoría o contribución.