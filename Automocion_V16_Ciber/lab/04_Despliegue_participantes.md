# Despliegue para participantes (aula)

## 1) ¿Git clone es la mejor opción?
Sí, en general es la mejor opción para clase si hay internet estable.

Ventajas:
- Todos parten de la misma versión.
- Permite corregir rápido con `git pull`.
- Facilita soporte docente (mismo árbol de carpetas).

Recomendación docente:
- Publicar una versión congelada (tag), por ejemplo: `v1.0-aula`.
- Indicar a todos que usen esa versión.

---

## 2) Flujo online recomendado (con Git)

### Paso A — Clonar
```powershell
git clone <URL_DEL_REPO>
cd Automozioa/Automocion_V16_Ciber
```

### Paso B — Ir a versión estable
```powershell
git checkout v1.0-aula
```

### Paso C — Crear entorno e instalar
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Paso D — Arrancar y validar
```powershell
uvicorn backend.app:app --host 127.0.0.1 --port 8080
```

Comprobar:
- `http://127.0.0.1:8080/health`
- `http://127.0.0.1:8080/aginte-panela`

---

## 3) Flujo offline (plan B)
Si falla internet o GitHub:

1. El docente distribuye un ZIP de la versión estable.
2. Cada equipo descomprime la carpeta.
3. Ejecuta exactamente los mismos pasos de entorno virtual y arranque.

Sugerencia:
- Llevar el ZIP en USB y también en recurso compartido local.

---

## 4) ¿Crear versión específica para participantes?
Sí, es recomendable.

No tanto por “seguridad fuerte”, sino por:
- reducir ruido (menos archivos irrelevantes),
- evitar errores de navegación,
- simplificar soporte en aula,
- homogeneizar evidencias.

---

## 5) Contenido mínimo recomendado para participantes

Mantener:
- `backend/`
- `simulator/`
- `samples/`
- `logs/`
- `reports/`
- `requirements.txt`
- `RUN_ME_FIRST.md`
- plantilla de informe en `reports/`

Opcional para participantes:
- guía breve del laboratorio (1 archivo)

No necesario para participantes (puede quedarse solo en versión docente):
- materiales extensos de preparación docente,
- presentaciones del ponente,
- documentación interna de diseño.

---

## 6) Estrategia práctica de mantenimiento

### Opción recomendada: dos ramas
- `main` → versión completa docente.
- `participants` → versión reducida para alumnado.

Flujo sugerido:
1. Actualizar y validar en `main`.
2. Propagar cambios necesarios a `participants`.
3. Publicar tag de aula en `participants` (ej. `v1.0-aula`).

---

## 7) Checklist previo a clase
- [ ] Tag de versión creado
- [ ] URL de clonación validada
- [ ] ZIP offline preparado
- [ ] Arranque probado en un equipo limpio
- [ ] Panel y simulador funcionando
