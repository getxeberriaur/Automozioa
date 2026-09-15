# V2X Simulación — Laboratorio de Ciberseguridad

Laboratorio local para introducir la seguridad de comunicaciones **V2V, V2I y V2P** sin transmitir por radio ni conectarse a vehículos o infraestructuras reales.

## Qué se trabaja

- Mensajes CAM, DENM y una representación simplificada de SPATEM.
- Suplantación de identidad, replay, datos físicamente imposibles y ráfagas.
- Autenticación HMAC de laboratorio, ventana temporal, secuencias, plausibilidad y rate limiting.
- Diferencia entre autenticidad, integridad y veracidad de un mensaje.
- Relación con TARA, UNECE R155 e ISO/SAE 21434.

## Posición en el curso

Este módulo completa las superficies ya trabajadas:

| Superficie | Laboratorio | Pregunta principal |
|---|---|---|
| Bus interno | `CANbus_ICSim_Ciber/` | ¿Qué puede hacer un nodo dentro del vehículo? |
| Radio cercana | `RF_Lab_Seguro/` y prácticas TPMS/keyfob | ¿Qué puede observarse desde fuera? |
| IoT vial | `Automocion_V16_Ciber/` | ¿Cómo se valida un evento conectado? |
| Cooperación vial | `V2X_Simulacion_Ciber/` | ¿Cuándo debe confiar el vehículo en otro emisor? |

## Arranque

Consulta [`RUN_ME_FIRST.md`](RUN_ME_FIRST.md) y después realiza [`lab/01_Practica_V2X.md`](lab/01_Practica_V2X.md).

> Todo el tráfico se limita a `127.0.0.1`. No se incluye transmisión RF, jamming, replay por radio ni interacción con vehículos, semáforos o certificados reales.