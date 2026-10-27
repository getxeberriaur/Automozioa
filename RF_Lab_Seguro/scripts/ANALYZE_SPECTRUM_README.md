# analyze_spectrum.py — Análisis de Espectro RF

## 📋 Descripción
Script Python para analizar capturas de espectro en formato CSV (salida de `rtl_power`).

**Entradas:** CSV con datos de potencia (dBm) por frecuencia y tiempo  
**Salidas:** Gráficos PNG + reporte de eventos en texto

---

## 🔧 Requisitos

```bash
pip install pandas numpy matplotlib scipy
```

---

## ⚡ Uso

```bash
python3 analyze_spectrum.py <archivo.csv>
```

**Ejemplo:**
```bash
python3 analyze_spectrum.py capture_433_mhz.csv
```

**Salida:**
- `plots/spectrum_YYYYMMDD_HHMMSS.png` — Gráfico de espectro + espectrograma
- `plots/reporte_YYYYMMDD_HHMMSS.txt` — Reporte con eventos detectados

---

## 📊 Estructura CSV esperada

El CSV debe contener:
- Metadatos: `Date`, `Time`, `Hz_low`, `Hz_high`, `Hz_step`, `Samples`
- Columnas de potencia: Cualquier columna que contenga `"dBm"` en el nombre (ej: `433500 dBm`, `433600 dBm`, etc.)

**Ejemplo de formato:**
```
Date,Time,Hz_low,Hz_high,Hz_step,Samples,433500 dBm,433600 dBm,...
2024-10-27,14:00:00,433500000,434500000,100000,10,-75.2,-76.1,...
```

---

## 🐛 Solución de Errores

### Error: `TypeError: can only concatenate str (not "int") to str`

**Causa:** Las columnas de potencia contienen valores string en lugar de números.

**Solución:** ✅ Ya corregido en v1.1 — el script convierte automáticamente a float.

### Otros errores:
- **"No se encontraron columnas de potencia"** → Verifica que el CSV tenga columnas con `dBm` en el nombre.
- **"No module named 'pandas'"** → Instala dependencias: `pip install pandas numpy matplotlib scipy`

---

## 📈 Ejemplos de Captura

### Con rtl_power (recomendado):
```bash
rtl_power -f 433500000-434500000 -g 40 -p 0 -d 0 -r 60 capture.csv
```

### Con rtl_433:
```bash
rtl_433 -f 433920000 -s 250000 -S unknown -R 0 | tee capture.log
# Luego convertir a CSV si es necesario
```

---

## 📝 Notas

- El script detecta automáticamente eventos (pulsaciones/ráfagas) usando análisis de baseline.
- Los gráficos incluyen espectro promedio y espectrograma (waterfall).
- Los eventos se marcan en el reporte si están presentes.

---

## ✅ Última actualización

- **v1.1** (2024-10-27): Correción de tipos — convierte power columns a float automáticamente.
- **v1.0** (2024-10-xx): Release inicial.
