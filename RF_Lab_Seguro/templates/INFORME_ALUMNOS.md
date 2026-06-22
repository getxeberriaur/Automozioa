# Informe de Laboratorio: Análisis de Espectro RF

**Especialización:** Ciberseguridad en Automoción  
**Práctica:** RF_Lab_Seguro - Captura y Análisis de Señales de Radiofrecuencia  
**Nivel:** Intermedio

---

## 1. Portada

| Campo | Dato |
|---|---|
| **Grupo:** | \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ |
| **Miembros:** | 1. \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ |
| | 2. \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ |
| | 3. \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ |
| | 4. \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ |
| **Profesor:** | \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ |
| **Fecha:** | \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ |
| **Centro:** | \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ |

---

## 2. Objetivos

**Objetivo General:**  
Comprender los fundamentos de captura y análisis de señales de radiofrecuencia en banda ISM 433 MHz, con enfoque en detección defensiva de vulnerabilidades en sistemas de acceso remoto.

**Objetivos Específicos:**

- [ ] Configurar correctamente Raspberry Pi + RTL-SDR
- [ ] Capturar datos pasivamente de un emisor de prueba aislado
- [ ] Identificar frecuencia central, ancho de banda y duración de transmisión
- [ ] Detectar automáticamente eventos de pulsación
- [ ] Comparar comportamiento normal vs con interferencia
- [ ] Proponer mitigaciones defensivas basadas en observaciones

---

## 3. Marco Teórico (Resumen 1-2 páginas)

**Escribe aquí un resumen de:**

1. **Radiofrecuencia (RF) e ISM:**
   - ¿Por qué 433 MHz es común en mandos?
   - ¿Qué significa "ISM"?
   - Regulación en España/Europa para banda 433 MHz

2. **Modulación ASK/OOK:**
   - Diferencia entre fixed code y rolling code
   - Por qué rolling code es más seguro

3. **Vulnerabilidades Conocidas:**
   - RollJam attack (teórico)
   - Replay attacks
   - Jamming/interferencia

4. **Defensa en Profundidad:**
   - Detección de jamming
   - Time window limits
   - Distance bounding

---

## 4. Metodología

### 4.1 Hardware Utilizado

| Componente | Modelo | Especificación |
|---|---|---|
| Raspberry Pi | \_\_\_\_\_\_\_\_\_\_ | \_\_\_\_\_\_\_\_\_\_ |
| RTL-SDR | \_\_\_\_\_\_\_\_\_\_ | \_\_\_\_\_\_\_\_\_\_ |
| Mando RF | \_\_\_\_\_\_\_\_\_\_ | Frecuencia: 433 MHz |
| Antena | \_\_\_\_\_\_\_\_\_\_ | Longitud: ~34 cm |
| Portátil | \_\_\_\_\_\_\_\_\_\_ | OS: \_\_\_\_\_\_\_\_ |

### 4.2 Procedimiento

**Fase 1: Captura Baseline (sin emisor)**
- Duración: \_\_\_ segundos
- Ganancia RTL-SDR: \_\_\_\_ dB
- Archivo: `baseline_no_tx.csv`

**Fase 2: Captura con Pulsaciones**
- Duración: \_\_\_ segundos
- Número de pulsaciones: \_\_\_\_
- Separación entre pulsaciones: \_\_\_ segundos
- Archivo: `mando_pulsaciones.csv`

**Fase 3: Captura con Ruido (si se realizó)**
- Tipo de interferencia: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
- Duración ruido: \_\_\_ segundos
- Archivo: `con_ruido_ambiente.csv`

### 4.3 Software y Análisis

```
Script utilizado: analyze_spectrum.py
Librerías: matplotlib, pandas, numpy, scipy
Parámetros de detección:
  - Threshold: 5 dB sobre baseline
  - Duración mínima evento: 3 muestras
```

---

## 5. Resultados

### 5.1 Estadísticas Generales

**Captura baseline (sin emisor):**

| Parámetro | Valor |
|---|---|
| Rango de potencia | \_\_\_ a \_\_\_ dBm |
| Potencia media | \_\_\_\_ dBm |
| Potencia mínima | \_\_\_\_ dBm |
| Eventos detectados | \_\_\_\_ |

**Captura con mando:**

| Parámetro | Valor |
|---|---|
| Rango de potencia | \_\_\_ a \_\_\_ dBm |
| Potencia media | \_\_\_\_ dBm |
| Potencia máxima | \_\_\_\_ dBm |
| Eventos detectados | \_\_\_\_ |
| SNR (Signal-to-Noise Ratio) | \_\_\_\_ dB |

### 5.2 Análisis de Frecuencia

| Parámetro | Observado | Esperado | ✓/✗ |
|---|---|---|---|
| Frecuencia central (MHz) | \_\_\_\_ | 433.92 | |
| Ancho de banda (kHz) | \_\_\_\_ | ~500 | |
| Desviación frecuencia | \_\_\_\_ | <100 kHz | |

### 5.3 Análisis Temporal de Eventos

**Tabla de pulsaciones detectadas:**

| Evento | Inicio (s) | Fin (s) | Duración (s) | P_máx (dBm) |
|---|---|---|---|---|
| 1 | \_\_\_ | \_\_\_ | \_\_\_ | \_\_\_ |
| 2 | \_\_\_ | \_\_\_ | \_\_\_ | \_\_\_ |
| 3 | \_\_\_ | \_\_\_ | \_\_\_ | \_\_\_ |
| 4 | \_\_\_ | \_\_\_ | \_\_\_ | \_\_\_ |
| 5 | \_\_\_ | \_\_\_ | \_\_\_ | \_\_\_ |

**Estadísticas de eventos:**

- Duración promedio: \_\_\_ segundos
- Desviación estándar: \_\_\_ segundos
- Espaciamiento promedio entre eventos: \_\_\_ segundos
- Consistencia: \_\_\_\_\_\_\_\_\_\_\_\_ (comentario)

### 5.4 Gráficos Generados

**Incluir aquí:**
1. Foto/captura de `spectrum_XXXX.png` (espectro promedio)
2. Foto/captura de `events_XXXX.png` (eventos temporales)

*[Pegar imágenes aquí]*

---

## 6. Análisis e Interpretación

### 6.1 Interpretación del Espectro

**Descripción del gráfico de potencia vs frecuencia:**

¿Dónde está el pico? ¿Por qué? ¿Cómo lo sabes?

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

### 6.2 Detección de Eventos

¿Cómo el algoritmo detectó los eventos? ¿Fue correcto? ¿Hubo falsos positivos?

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

### 6.3 Impacto de Interferencia (si aplica)

Si capturaste con ruido ambiente, ¿cómo cambió la detección?

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

### 6.4 Comparación: Baseline vs Mando

¿Cuál es la diferencia más importante entre la captura sin emisor y con emisor?

Diferencia de potencia: \_\_\_\_\_ dB

Conclusión: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

---

## 7. Vulnerabilidades Identificadas

**Basándote en tus observaciones, enumera 5 vulnerabilidades potenciales en este tipo de sistemas:**

1. \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

2. \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

3. \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

4. \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

5. \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

---

## 8. Mitigaciones Propuestas

**Para cada vulnerabilidad, proponer una defensa:**

| Vulnerabilidad | Mitigación Propuesta |
|---|---|
| 1. | \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ |
| 2. | \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ |
| 3. | \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ |
| 4. | \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ |
| 5. | \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ |

---

## 9. Conclusiones

### 9.1 Resumen de Hallazgos

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

### 9.2 Importancia de la Defensa en Profundidad

Explica por qué no es suficiente una única defensa contra ataques RF:

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

### 9.3 Aprendizajes Clave

3 cosas que aprendiste en esta práctica:

1. \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

2. \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

3. \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

---

## 10. Reflexión Ética

**¿Cómo aplicarías este conocimiento de forma responsable y legal?**

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

---

## 11. Referencias

**Libros/Papers consultados:**
- [ ] Hoppe & Kiltz, "Rolling Code Security" (IEEE, 2008)
- [ ] Garcia et al., "Weaknesses in RKE Systems" (USENIX, 2015)
- [ ] NIST SP 800-153 (RF Security)
- Otros: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

---

## 12. Apéndice

### A. Logs de Ejecución

**Comando ejecutado en RPi:**
```bash
./spectrum_capture.sh
```

**Salida:**
```
[copiar aquí salida de terminal]
```

### B. Comando de Análisis

**Comando ejecutado en portátil:**
```bash
python3 scripts/analyze_spectrum.py data/mando_pulsaciones.csv
```

**Salida:**
```
[copiar aquí salida de análisis]
```

### C. Dificultades Encontradas

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

---

**Informe completado por:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_  
**Fecha:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_  
**Firma del grupo:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_  
**Revisado por profesor:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_  

