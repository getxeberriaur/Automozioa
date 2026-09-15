# Plantilla de informe de evidencias — Laboratorio V16 (equipo)

## 1) Datos del equipo
- Centro:
- Curso / grupo:
- Equipo nº:
- Integrantes:
- Fecha:
- Docente:

## 2) Objetivo de la práctica
Describir en 3-5 líneas qué se ha validado en el laboratorio (recepción de avisos V16 simulados, controles de seguridad y trazabilidad).

## 3) Entorno utilizado
- Sistema operativo:
- Python:
- Dependencias instaladas (`requirements.txt`): Sí / No
- Backend operativo (`/health`): Sí / No
- Panel visual operativo (`/aginte-panela`): Sí / No

## 4) Casos de prueba ejecutados

| Caso | Comando | Resultado esperado | Resultado observado | ¿OK? |
|---|---|---|---|---|
| legítimo | `python simulator/send_event.py legitimo` | `accepted_for_processing` |  |  |
| replay | `python simulator/send_event.py replay` | 1º accepted, 2º rejected (`replayed_nonce`) |  |  |
| timestamp atrasado | `python simulator/send_event.py timestamp-atrasado` | rejected (`message_out_of_time_window`) |  |  |
| coordenadas inválidas | `python simulator/send_event.py coordenadas-invalidas` | rejected (validación de rango) |  |  |
| identidad inválida | `python simulator/send_event.py identidad-invalida` | rejected (`unknown_device_id`) |  |  |
| ráfaga | `python simulator/send_event.py rafaga --count 8` | últimos eventos rejected (`rate_limit_exceeded`) |  |  |

## 5) Evidencias (capturas o extractos)
Añadir mínimo 3 evidencias:

1. Captura de evento legítimo aceptado (respuesta o panel).
2. Captura de replay rechazado con razón `replayed_nonce`.
3. Captura de rechazo por timestamp o rate limiting.

Referencias opcionales:
- Vista JSON: `http://127.0.0.1:8080/events/recent?limit=10`
- Panel operativo: `http://127.0.0.1:8080/aginte-panela`
- Log: `logs/events.log`

## 6) Análisis técnico breve
### 6.1 Controles verificados
- Validación de esquema:
- Ventana temporal (`security.sent_at`):
- Anti-replay (`security.nonce`):
- Rate limiting por identidad:

### 6.2 Observaciones
- ¿Qué control detectó más ataques?
- ¿Hubo falsos positivos?
- ¿Qué problema práctico apareció durante la sesión?

## 7) Conclusiones y mejoras
- Conclusión principal (1-2 frases):
- Mejora 1 (corto plazo):
- Mejora 2 (medio plazo):
- Mejora 3 (entorno más productivo: firma, PKI, monitorización, etc.):

## 8) Checklist de entrega
- [ ] Tabla de casos completada
- [ ] Mínimo 3 evidencias adjuntas
- [ ] Conclusiones redactadas
- [ ] Archivo guardado en `reports/`
