# Instalación: Portátil (Análisis y Visualización)

**Tiempo estimado:** 20-30 minutos  
**Aplicable a:** Linux, macOS, Windows+WSL2

---

## Requisitos

- Python 3.8+
- Conexión SSH a Raspberry Pi
- ~500 MB de espacio libre
- Git (opcional pero recomendado)

---

## Paso 1: Instalar Python (Si No lo Tienes)

### En Ubuntu/Debian:
```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv git
```

### En macOS:
```bash
brew install python3 git
```

### En Windows (WSL2):
```bash
# En terminal WSL2 (Ubuntu)
sudo apt update && sudo apt install -y python3-pip git
```

---

## Paso 2: Crear Entorno Virtual

```bash
mkdir -p ~/rf-analysis
cd ~/rf-analysis

python3 -m venv venv

# Activar (Linux/macOS):
source venv/bin/activate

# Activar (Windows CMD):
# venv\Scripts\activate

# Activar (Windows PowerShell):
# venv\Scripts\Activate.ps1
```

**Verificar:** Deberías ver `(venv)` al inicio del prompt.

---

## Paso 3: Instalar Dependencias Python

```bash
# Actualizar pip
pip install --upgrade pip

# Instalar librerías base
pip install matplotlib pandas numpy scipy jupyter ipython

# Opcional (análisis avanzado)
pip install scikit-learn peakutils
```

**Verificar:**
```bash
python3 -c "import matplotlib, pandas, numpy, scipy; print('✓ OK')"
```

---

## Paso 4: Crear Estructura de Carpetas

```bash
cd ~/rf-analysis

mkdir -p data      # Archivos CSV desde RPi
mkdir -p scripts   # Scripts de análisis
mkdir -p plots     # Gráficos generados
mkdir -p notebooks # Jupyter notebooks
```

---

## Paso 5: Descargar Scripts de Análisis

### Opción A: Desde GitHub

```bash
cd ~/rf-analysis/scripts

wget https://github.com/getxeberriaur/Automozioa/raw/main/RF_Lab_Seguro/scripts/analyze_spectrum.py
wget https://github.com/getxeberriaur/Automozioa/raw/main/RF_Lab_Seguro/scripts/event_detector.py

chmod +x *.py
```

### Opción B: Crear Manualmente

Ver documentación en `scripts/` del repositorio.

---

## Paso 6: Descargar Datos desde Raspberry

```bash
cd ~/rf-analysis/data

# Copiar todos los CSVs desde RPi
scp pi@192.168.1.100:~/rf_capture/data/*.csv .

# Listar archivos
ls -lh
```

**Salida esperada:**
```
-rw-r--r-- 1 user group 1.2M Jun 22 14:30 spectrum_20260622_143021.csv
```

---

## Paso 7: Ejecutar Análisis Básico

```bash
cd ~/rf-analysis

# Activar entorno (si no lo está)
source venv/bin/activate

# Analizar primer CSV
python3 scripts/analyze_spectrum.py data/spectrum_*.csv
```

**Salida esperada:**
```
[✓] CSV cargado: 2000 filas, 3605 columnas
[*] Rango de potencia: -90.5 a -45.2 dBm
[*] Eventos detectados: 7
    E1: t=125-135s, P_max=-47.8 dBm, dur=10s
    E2: t=245-256s, P_max=-46.5 dBm, dur=11s
    ...
[✓] Gráfico guardado: plots/spectrum_20260622_143021.png
[✓] Gráfico de eventos: plots/events_20260622_143021.png
```

---

## Paso 8: Visualizar Gráficos

```bash
# Listar gráficos generados
ls plots/

# Abrir en visor de imágenes
# Linux:
eog plots/spectrum_*.png

# macOS:
open plots/spectrum_*.png

# Windows (desde WSL2):
explorer.exe plots/
```

---

## Paso 9: Jupyter Notebook (Análisis Interactivo)

Crear un notebook interactivo para análisis paso a paso:

```bash
cd ~/rf-analysis
jupyter notebook
```

**En el navegador que abre:**
1. New → Python 3
2. Pega este código:

```python
# Celda 1: Cargar datos
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('data/spectrum_example.csv', comment='#')
print(f"Datos cargados: {df.shape}")
print(df.head())

# Celda 2: Visualizar potencia
power = df[[c for c in df.columns if 'dBm' in c]].mean(axis=1)
plt.figure(figsize=(14, 4))
plt.plot(power, 'b-', linewidth=1)
plt.xlabel('Tiempo (muestras)')
plt.ylabel('Potencia (dBm)')
plt.title('Potencia vs Tiempo')
plt.grid(True, alpha=0.3)
plt.show()

# Celda 3: Detectar picos
from scipy.signal import find_peaks
peaks, _ = find_peaks(power, height=-50, distance=50)
print(f"✓ Eventos detectados: {len(peaks)}")
for i, p in enumerate(peaks[:10]):
    print(f"  E{i+1}: índice={p}, potencia={power[p]:.1f} dBm")
```

---

## Paso 10: Herramientas Complementarias (Opcionales)

### GNU Radio Companion (Visualización en Tiempo Real)

```bash
# Linux
sudo apt install -y gnuradio gnuradio-dev gr-osmosdr

# macOS
brew install gnuradio

# Iniciar
gnuradio-companion
```

### FFmpeg (Convertir Gráficos a Video)

```bash
pip install pillow
ffmpeg -framerate 2 -pattern_type glob -i 'plots/*.png' -c:v libx264 spectrum_video.mp4
```

---

## 🧪 Verificación Final

```bash
#!/bin/bash
# Script de verificación

echo "=== VERIFICACIÓN ANÁLISIS ==="

# 1. Python
python3 --version && echo "✓ Python OK"

# 2. Librerías
python3 -c "import matplotlib, pandas, numpy, scipy; print('✓ Librerías OK')" || echo "✗ Falta algo"

# 3. Carpetas
ls -d ~/rf-analysis/{data,scripts,plots,notebooks} && echo "✓ Estructura OK" || echo "✗ Carpetas no existen"

# 4. Scripts
ls ~/rf-analysis/scripts/*.py && echo "✓ Scripts OK" || echo "✗ No hay scripts"

# 5. Datos
ls ~/rf-analysis/data/*.csv && echo "✓ Datos OK" || echo "✗ No hay CSVs"

echo "=== FIN ==="
```

---

## 📋 Flujo Típico de Trabajo

```
1. SSH a RPi desde portátil
2. Ejecutar captura: ./spectrum_capture.sh
3. Esperar a que termine
4. SCP de datos: scp pi@192.168.1.100:~/rf_capture/data/*.csv ~/rf-analysis/data/
5. Analizar: python3 scripts/analyze_spectrum.py data/*.csv
6. Visualizar gráficos en plots/
7. Completar informe con resultados
```

---

## 🐛 Troubleshooting

| Problema | Causa | Solución |
|---|---|---|
| `ModuleNotFoundError: matplotlib` | Librería no instalada | `pip install matplotlib` |
| `Permission denied` en SSH | Credenciales incorrectas | Verificar IP, usuario (pi), contraseña |
| Python 2 por defecto | Sistema antiguo | Usar explícitamente `python3` |
| No hay CSVs en data/ | SCP falló | Verificar ruta en RPi: `ls ~/rf_capture/data/` |
| Jupyter no arranca | Puerto ocupado | `jupyter notebook --port 8889` |
| Gráficos distorsionados | Outliers en datos | Filtrar datos antes de graficar |

---

## 📚 Ejemplo: Script Completo de Análisis

**Archivo:** `~/rf-analysis/scripts/full_analysis.py`

```python
#!/usr/bin/env python3
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.signal import find_peaks

def main():
    # Cargar
    csv_file = "data/spectrum_*.csv" if len(sys.argv) < 2 else sys.argv[1]
    files = list(Path(".").glob(csv_file.replace("*", "*")))
    
    if not files:
        print(f"[!] No CSVs encontrados: {csv_file}")
        return
    
    for f in files:
        print(f"\n[*] Analizando: {f}")
        df = pd.read_csv(f, comment='#')
        
        # Potencia promedio
        power_cols = [c for c in df.columns if 'dBm' in c]
        power = df[power_cols].mean(axis=1).values
        
        # Detectar eventos
        peaks, _ = find_peaks(power, height=-50, distance=50)
        
        print(f"    Rango: {power.min():.1f} a {power.max():.1f} dBm")
        print(f"    Eventos: {len(peaks)}")
        
        # Graficar
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(power, 'b-', linewidth=1)
        ax.scatter(peaks, power[peaks], color='red', s=50)
        ax.set_xlabel('Tiempo (muestras)')
        ax.set_ylabel('Potencia (dBm)')
        ax.set_title(f'Análisis: {f.name}')
        ax.grid(True, alpha=0.3)
        
        output = Path("plots") / f"{f.stem}_analyzed.png"
        output.parent.mkdir(exist_ok=True)
        plt.savefig(output, dpi=100)
        print(f"    [✓] Guardado: {output}")
        plt.close()

if __name__ == "__main__":
    main()
```

---

## ✅ Checklist Post-Instalación

- [ ] Entorno virtual activado
- [ ] Python importa todas librerías sin errores
- [ ] Carpetas `data/`, `scripts/`, `plots/` creadas
- [ ] Scripts descargados desde GitHub
- [ ] SSH conecta a RPi
- [ ] CSV descargado desde RPi a `data/`
- [ ] Script de análisis ejecuta sin errores
- [ ] Gráficos generados en `plots/`

---

## ⏭️ Siguiente Paso

→ Ejecutar práctica: **[03_PROCEDIMIENTO_CAPTURA.md](03_PROCEDIMIENTO_CAPTURA.md)**

