# V2X Simulación — Laboratorio de Ciberseguridad

Laboratorio local para introducir la seguridad de comunicaciones **V2V, V2I y V2P** sin transmitir por radio ni conectarse a vehículos o infraestructuras reales.

## Qué se trabaja

- Mensajes CAM, DENM y una representación simplificada de SPATEM.
- Suplantación de identidad, replay, datos físicamente imposibles y ráfagas.
- Autenticación HMAC de laboratorio, ventana temporal, secuencias, plausibilidad y rate limiting.
- Diferencia entre autenticidad, integridad y veracidad de un mensaje.
- Relación con TARA, UNECE R155 e ISO/SAE 21434.

## Recorrido

1. Sigue [RUN_ME_FIRST.md](RUN_ME_FIRST.md) para iniciar el gateway y ejecutar los escenarios.
2. Completa [lab/01_Practica_V2X.md](lab/01_Practica_V2X.md).
3. Guarda las evidencias en la plantilla de [`reports/`](reports/00_Plantilla_informe.md).

> Todo el tráfico se limita a `127.0.0.1`. No se incluye transmisión RF, jamming, replay por radio ni interacción con vehículos, semáforos o certificados reales.