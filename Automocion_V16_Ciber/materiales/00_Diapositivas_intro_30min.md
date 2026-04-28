# Diapositivas (30 min): Ciberseguridad en balizas V16 conectadas

> Uso recomendado: una diapositiva cada 2-3 minutos.

---

## 1) Título y objetivo

### Ciberseguridad en balizas V16 conectadas
**Introducción a laboratorio práctico (2h)**

**Objetivo de la sesión**
- Entender por qué una baliza conectada es un sistema ciberfísico crítico.
- Identificar amenazas realistas y controles de defensa.
- Preparar el contexto de la práctica (simulación en entorno aislado).

**Mensaje clave**
- En automoción, ciberseguridad = seguridad vial + continuidad operativa.

---

## 2) Caso de uso real en carretera

### ¿Qué ocurre cuando una baliza emite un aviso?
- Un dispositivo conectado informa de una incidencia.
- El aviso viaja por red móvil hacia una plataforma de recepción.
- La plataforma valida, acepta/rechaza y distribuye información.

**Pregunta guía al grupo**
- ¿Qué impacto tendría un aviso falso aceptado por el backend?

---

## 3) Arquitectura extremo a extremo (simplificada)

1. Baliza V16 (identidad + firmware)
2. Red de comunicaciones (transporte)
3. Backend de recepción/validación
4. Integración con plataforma de tráfico
5. Consumo por paneles/apps/servicios

**Lectura docente**
- Cuantas más integraciones, mayor superficie de ataque y efecto cascada.

---

## 4) Activos críticos

- Identidad del dispositivo (`device_id`, credenciales, certificados)
- Integridad del aviso (contenido y metadatos)
- Frescura temporal (`security.sent_at`)
- Unicidad del mensaje (`security.nonce`)
- Disponibilidad de la API
- Trazabilidad de decisiones (`accepted` / `rejected` + `reason`)

**Idea fuerza**
- Sin trazabilidad no hay respuesta eficaz ante incidentes.

---

## 5) Amenazas principales (visión STRIDE docente)

- **Suplantación**: dispositivo no autorizado (`unknown_device_id`)
- **Manipulación**: campos alterados o fuera de rango
- **Replay**: reenvío del mismo mensaje (`replayed_nonce`)
- **Denegación de servicio**: ráfagas y saturación (`rate_limit_exceeded`)
- **Repudio**: falta de evidencias para auditar

**Impacto**
- Alertas erróneas, ruido operativo, peor priorización y riesgo vial.

---

## 6) Matriz rápida impacto/probabilidad

| Amenaza | Probabilidad | Impacto | Prioridad |
|---|---|---|---|
| Replay | Alta | Media-Alta | Alta |
| Suplantación identidad | Media | Alta | Alta |
| Timestamp fuera de ventana | Alta | Media | Media-Alta |
| Coordenadas inválidas | Media | Media | Media |
| Ráfaga / abuso API | Media-Alta | Alta | Alta |

**Conclusión docente**
- Primero se atacan controles de bajo coste y alto retorno (frescura, nonce, tasa, esquema).

---

## 7) Controles por capa (lo que sí debemos ver en backend)

- **Esquema estricto** (estructura esperada del aviso)
- **Validación geográfica** (lat/lon en rango)
- **Ventana temporal** (`security.sent_at`)
- **Anti-replay** (`security.nonce` único)
- **Rate limiting por identidad**
- **Registro de decisión con motivo técnico**

**En laboratorio actual**
- Estos controles ya están implementados y visibles en panel + logs.

---

## 8) Qué vamos a medir en el laboratorio

- Tasa de aceptación de mensajes inválidos
- Capacidad de rechazo con razón explícita
- Evidencias de trazabilidad para informe técnico

**Herramientas de observación**
- Panel operativo: http://127.0.0.1:8080/aginte-panela
- Vista JSON: http://127.0.0.1:8080/events/recent?limit=10
- Log: `logs/events.log`

---

## 9) Riesgo residual y próximos pasos

Aunque el laboratorio valida controles base, queda riesgo residual:
- Falsificación avanzada sin firma criptográfica fuerte
- Exposición de canal si no hay endurecimiento de transporte
- Gestión de identidades/certificados en despliegue real

**Escalado recomendado**
- Firma de mensaje, PKI, mTLS, monitorización SOC, respuesta a incidentes.

---

## 10) Cierre + transición a práctica

### Lo que hará cada equipo (2h)
1. Enviar aviso legítimo.
2. Probar replay e inyecciones inválidas.
3. Observar aceptación/rechazo y razones.
4. Documentar evidencias y conclusiones.

**Regla de oro**
- Solo entorno local/sandbox aislado. Objetivo: defensa y aprendizaje.

**Pregunta de arranque para el grupo**
- ¿Qué control creéis que reducirá más riesgo con menor coste?
