# Arranque rápido del laboratorio

Este laboratorio emula el envío de un aviso telemático de baliza V16 hacia una plataforma de recepción local.

Guía de despliegue para aula: [lab/04_Despliegue_participantes.md](lab/04_Despliegue_participantes.md)

## 1) Crear y activar entorno virtual

### Linux / Ubuntu 22
```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 2) Instalar dependencias

```bash
pip install -r requirements.txt
```

## 3) Levantar backend

```bash
uvicorn backend.app:app --host 127.0.0.1 --port 8080 --reload
```

### Ver documentación interactiva

`http://127.0.0.1:8080/docs`

### Ver panel visual de operación

`http://127.0.0.1:8080/aginte-panela`

## 4) Probar con el simulador

### Evento legítimo
```bash
python3 simulator/send_event.py legitimo
```

### Replay
```bash
python3 simulator/send_event.py replay
```

### Timestamp atrasado
```bash
python3 simulator/send_event.py timestamp-atrasado
```

### Coordenadas inválidas
```bash
python3 simulator/send_event.py coordenadas-invalidas
```

### Identidad inválida
```bash
python3 simulator/send_event.py identidad-invalida
```

### Ráfaga
```bash
python3 simulator/send_event.py rafaga --count 8
```

## 5) Revisar evidencias

- Log principal: `logs/events.log`
- Últimos avisos procesados: `http://127.0.0.1:8080/events/recent?limit=10`
- Panel visual en euskara: `http://127.0.0.1:8080/aginte-panela`
- Carpeta de informes: `reports/`

### Plantillas de informe

- Castellano: `reports/00_Plantilla_informe_evidencias.md`
- Euskara: `reports/00_Ebidentzia_txosten_txantiloia.md`

### Presentaciones intro (proyector)

- Castellano: `presentaciones/Intro_V16_30min_ES.html`
- Euskara: `presentaciones/Intro_V16_30min_EU.html`

## 6) Despliegue para participantes (resumen)

### Opción A (recomendada): online con Git
1. `git clone <URL_DEL_REPO>`
2. `cd Automozioa/Automocion_V16_Ciber`
3. `git checkout v1.0-aula` (o versión indicada por el docente)
4. Crear `venv`, instalar dependencias y arrancar backend.

### Opción B (plan B): ZIP offline
1. Descomprimir versión estable entregada por el docente.
2. Ejecutar los mismos pasos de entorno y arranque.

### Recomendación organizativa
- Mantener una versión/branch específica para participantes para reducir complejidad en clase.
