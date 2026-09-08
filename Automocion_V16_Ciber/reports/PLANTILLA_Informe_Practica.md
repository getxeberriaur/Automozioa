# Informe de Práctica — Simulador Baliza V16
**CVE-2025-65855 · Help Flash IoT · Análisis de Vulnerabilidades**

---

## Datos del participante

| Campo | Valor |
|-------|-------|
| **Nombre y apellidos** | |
| **Fecha** | |
| **Módulo / Curso** | |
| **Entorno de trabajo** | Ubuntu 22 / VM / otro: |

---

## Parte 1 — Reconocimiento del entorno

### 1.1 ¿Qué endpoints expone el backend?

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| | | |
| | | |
| | | |

### 1.2 ¿Qué campos contiene el evento legítimo?

```json
{

}
```

### 1.3 ¿Qué respuesta devuelve el backend ante un evento legítimo?

```
// respuesta del servidor
```

---

## Parte 2 — Escenarios de ataque

### 2.1 Replay Attack

| Campo | Valor |
|-------|-------|
| **Comando ejecutado** | `python3 simulator/send_event.py replay` |
| **Respuesta del servidor** | |
| **Código HTTP** | |
| **¿El ataque tuvo éxito?** | ✅ Sí / ❌ No |
| **¿Por qué?** | |

### 2.2 Timestamp atrasado

| Campo | Valor |
|-------|-------|
| **Comando ejecutado** | `python3 simulator/send_event.py timestamp-atrasado` |
| **Respuesta del servidor** | |
| **Código HTTP** | |
| **¿El ataque tuvo éxito?** | ✅ Sí / ❌ No |
| **¿Por qué?** | |

### 2.3 Coordenadas inválidas

| Campo | Valor |
|-------|-------|
| **Comando ejecutado** | `python3 simulator/send_event.py coordenadas-invalidas` |
| **Respuesta del servidor** | |
| **Código HTTP** | |
| **¿El ataque tuvo éxito?** | ✅ Sí / ❌ No |
| **¿Por qué?** | |

### 2.4 Identidad inválida

| Campo | Valor |
|-------|-------|
| **Comando ejecutado** | `python3 simulator/send_event.py identidad-invalida` |
| **Respuesta del servidor** | |
| **Código HTTP** | |
| **¿El ataque tuvo éxito?** | ✅ Sí / ❌ No |
| **¿Por qué?** | |

### 2.5 Ráfaga (Rate Limiting)

| Campo | Valor |
|-------|-------|
| **Comando ejecutado** | `python3 simulator/send_event.py rafaga --count 10` |
| **¿A partir de qué petición empezó a rechazar?** | |
| **Código HTTP de rechazo** | |
| **Conclusión** | |

---

## Parte 3 — Análisis del backend

### 3.1 ¿Qué validaciones implementa el backend?

| Validación | ¿Implementada? | Código/línea donde se valida |
|------------|---------------|------------------------------|
| Verificación de timestamp | | |
| Detección de replay | | |
| Validación de coordenadas GPS | | |
| Autenticación del dispositivo | | |
| Rate limiting | | |

### 3.2 ¿Qué vulnerabilidades has identificado que NO están mitigadas?

1. 
2. 
3. 

### 3.3 Log de la evidencia más relevante

```
// pega aquí el log más importante que hayas capturado
```

---

## Parte 4 — Propuestas de mejora

### 4.1 ¿Cómo mejorarías la seguridad del backend?

| Vulnerabilidad identificada | Mejora propuesta |
|----------------------------|-----------------|
| | |
| | |
| | |

### 4.2 ¿Qué cambios harías en el protocolo de comunicación baliza → servidor?

1. 
2. 
3. 

---

## Parte 5 — Reflexión final

### 5.1 ¿Qué impacto real tendría explotar estas vulnerabilidades en producción?

*// respuesta libre (mínimo 5 líneas)*

### 5.2 ¿Qué relación tiene esta práctica con la normativa UNECE R155?

*// respuesta libre*

---

## Checklist de entrega

- [ ] Todos los escenarios del simulador ejecutados
- [ ] Capturas de log adjuntas o pegadas en el informe
- [ ] Vulnerabilidades identificadas y documentadas
- [ ] Propuestas de mejora argumentadas
- [ ] Reflexión final completada

---
*Plantilla generada para el curso de Ciberseguridad en Automoción — Automozioa*