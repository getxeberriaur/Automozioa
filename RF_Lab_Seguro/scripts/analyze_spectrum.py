#!/usr/bin/env python3

"""
analyze_spectrum.py
Análisis de datos de captura RF (espectro en CSV)
Entrada: archivo CSV de rtl_power
Salida: gráficos PNG y reporte de eventos
"""

import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime
from scipy.signal import find_peaks

def load_csv(filepath):
    """Carga y parsea CSV de rtl_power"""
    try:
        # Saltar comentarios y cargar
        df = pd.read_csv(filepath, comment='#', skipinitialspace=True)
        print(f"[✓] CSV cargado: {len(df)} filas, {len(df.columns)} columnas")
        return df
    except Exception as e:
        print(f"[✗] Error al cargar {filepath}: {e}")
        sys.exit(1)

def detect_events(power_data, threshold_db=5, min_duration=3):
    """
    Detecta eventos (pulsaciones) en datos de potencia.
    
    Args:
        power_data: array 1D de potencia (dBm)
        threshold_db: umbral en dB sobre baseline
        min_duration: duración mínima en muestras
    
    Returns:
        lista de dicts con (start, end, max_power, duration)
    """
    # Calcular baseline
    baseline = np.percentile(power_data, 10)
    
    # Detectar actividad
    activity = power_data > (baseline + threshold_db)
    
    events = []
    in_event = False
    start_idx = 0
    max_power = baseline
    
    for i, is_active in enumerate(activity):
        if is_active and not in_event:
            start_idx = i
            in_event = True
            max_power = power_data[i]
        elif is_active and in_event:
            max_power = max(max_power, power_data[i])
        elif not is_active and in_event:
            duration = i - start_idx
            if duration >= min_duration:
                events.append({
                    'start': start_idx,
                    'end': i,
                    'max_power': float(max_power),
                    'duration': duration,
                    'baseline': float(baseline)
                })
            in_event = False
    
    return events

def plot_spectrum(df, output_dir="plots"):
    """Genera gráficos de espectro promedio y espectrograma"""
    Path(output_dir).mkdir(exist_ok=True)
    
    # Extraer columnas de potencia (dBm)
    power_cols = [c for c in df.columns if 'dBm' in str(c) and '-' not in str(c)[:1]]
    
    if not power_cols:
        # Alternativa: todas excepto metadatos
        metadata = ['Date', 'Time', 'Hz_low', 'Hz_high', 'Hz_step', 'Samples']
        power_cols = [c for c in df.columns if c not in metadata]
    
    if not power_cols:
        print("[!] No se encontraron columnas de potencia (dBm)")
        return None
    
    power_data = df[power_cols].values
    
    # Frecuencias: desde 433.5 MHz en pasos de 100 kHz (10 bins)
    freq_mhz = np.linspace(433.5, 434.5, power_data.shape[1])
    
    # Potencia promedio
    mean_power = np.mean(power_data, axis=0)
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8))
    
    # Gráfico 1: Potencia vs Frecuencia
    ax1.plot(freq_mhz, mean_power, 'b-', linewidth=2)
    ax1.fill_between(freq_mhz, mean_power, alpha=0.3)
    ax1.set_xlabel('Frecuencia (MHz)', fontsize=11)
    ax1.set_ylabel('Potencia (dBm)', fontsize=11)
    ax1.set_title('Espectro Promedio 433-434 MHz', fontsize=13, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # Marcar pico máximo
    max_idx = np.argmax(mean_power)
    peak_freq = freq_mhz[max_idx]
    peak_power = mean_power[max_idx]
    ax1.scatter([peak_freq], [peak_power], color='red', s=100, zorder=5)
    ax1.annotate(f'{peak_freq:.2f} MHz\n{peak_power:.1f} dBm',
                xy=(peak_freq, peak_power), 
                xytext=(peak_freq + 0.1, peak_power - 5),
                fontsize=10, 
                bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7),
                arrowprops=dict(arrowstyle='->', color='red'))
    
    # Gráfico 2: Espectrograma (Waterfall)
    im = ax2.imshow(power_data.T, aspect='auto', origin='lower', 
                    cmap='viridis', extent=[0, power_data.shape[0], 433.5, 434.5],
                    interpolation='nearest')
    ax2.set_xlabel('Tiempo (muestras)', fontsize=11)
    ax2.set_ylabel('Frecuencia (MHz)', fontsize=11)
    ax2.set_title('Espectrograma: Potencia vs Tiempo', fontsize=13, fontweight='bold')
    cbar = plt.colorbar(im, ax=ax2, label='Potencia (dBm)')
    
    # Guardar
    out_path = Path(output_dir) / f"spectrum_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    plt.tight_layout()
    plt.savefig(out_path, dpi=100, bbox_inches='tight')
    print(f"[✓] Gráfico de espectro: {out_path}")
    plt.close()
    
    return freq_mhz, mean_power

def plot_events(time_array, power, events, output_dir="plots"):
    """Grafica eventos detectados en timeline"""
    Path(output_dir).mkdir(exist_ok=True)
    
    fig, ax = plt.subplots(figsize=(14, 5))
    
    # Potencia vs tiempo
    ax.plot(time_array, power, 'b-', linewidth=1.2, label='Potencia')
    baseline = np.percentile(power, 10)
    ax.axhline(y=baseline, color='gray', linestyle='--', alpha=0.5, label=f'Baseline: {baseline:.1f} dBm')
    
    # Marcar eventos
    colors = plt.cm.Reds(np.linspace(0.4, 0.9, len(events)))
    for i, evt in enumerate(events):
        start, end = evt['start'], evt['end']
        ax.axvspan(time_array[start], time_array[end], alpha=0.3, color=colors[i])
        
        mid = (start + end) // 2
        mid_time = time_array[mid] if mid < len(time_array) else time_array[-1]
        ax.text(mid_time, evt['max_power'] + 2, f"E{i+1}", 
               ha='center', fontsize=9, fontweight='bold',
               bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    ax.set_xlabel('Tiempo (muestras)', fontsize=11)
    ax.set_ylabel('Potencia (dBm)', fontsize=11)
    ax.set_title(f'Detección de Eventos ({len(events)} pulsaciones detectadas)', 
                fontsize=13, fontweight='bold')
    ax.legend(loc='upper right', fontsize=10)
    ax.grid(True, alpha=0.3)
    
    out_path = Path(output_dir) / f"events_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    plt.tight_layout()
    plt.savefig(out_path, dpi=100, bbox_inches='tight')
    print(f"[✓] Gráfico de eventos: {out_path}")
    plt.close()

def generate_report(csv_path, freq_mhz, power, events, output_dir="plots"):
    """Genera un informe de texto con resultados"""
    
    report_path = Path(output_dir) / f"reporte_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    # Calcular estadísticas
    baseline = np.percentile(power, 10)
    peak_freq_idx = np.argmax(power)
    peak_freq = freq_mhz[peak_freq_idx]
    peak_power = power[peak_freq_idx]
    snr = peak_power - baseline
    
    with open(report_path, 'w') as f:
        f.write("╔════════════════════════════════════════════════════════════════╗\n")
        f.write("║  REPORTE DE ANÁLISIS DE ESPECTRO RF                           ║\n")
        f.write("╚════════════════════════════════════════════════════════════════╝\n\n")
        
        f.write(f"Archivo analizado: {csv_path}\n")
        f.write(f"Fecha/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("ESTADÍSTICAS GENERALES:\n")
        f.write(f"  • Líneas de datos: {len(power)}\n")
        f.write(f"  • Bins de frecuencia: {len(freq_mhz)}\n")
        f.write(f"  • Rango de potencia: {power.min():.2f} a {power.max():.2f} dBm\n")
        f.write(f"  • Potencia media: {power.mean():.2f} dBm\n")
        f.write(f"  • Baseline (P10): {baseline:.2f} dBm\n\n")
        
        f.write("PICO DETECTADO:\n")
        f.write(f"  • Frecuencia: {peak_freq:.3f} MHz\n")
        f.write(f"  • Potencia: {peak_power:.2f} dBm\n")
        f.write(f"  • SNR (Signal-to-Noise): {snr:.2f} dB\n\n")
        
        f.write(f"EVENTOS DETECTADOS: {len(events)}\n\n")
        
        if events:
            f.write("Detalle de eventos:\n")
            for i, evt in enumerate(events, 1):
                f.write(f"\n  Evento {i}:\n")
                f.write(f"    Inicio:     {evt['start']:6d} (índice)\n")
                f.write(f"    Fin:        {evt['end']:6d} (índice)\n")
                f.write(f"    Duración:   {evt['duration']:6d} muestras\n")
                f.write(f"    Potencia máx: {evt['max_power']:8.2f} dBm\n")
                f.write(f"    Sobre baseline: {evt['max_power'] - baseline:6.2f} dB\n")
        else:
            f.write("  (Ningún evento detectado)\n\n")
        
        f.write("\nCONCLUSIONES:\n")
        if peak_power > baseline + 5:
            f.write(f"  ✓ Se detecta claramente un pico en {peak_freq:.3f} MHz\n")
            f.write(f"  ✓ SNR favorable ({snr:.1f} dB)\n")
            if len(events) > 0:
                f.write(f"  ✓ Se detectaron {len(events)} eventos de pulsación\n")
                avg_duration = np.mean([e['duration'] for e in events])
                f.write(f"  ✓ Duración promedio de evento: {avg_duration:.0f} muestras\n")
        else:
            f.write("  ⚠ Potencia baja o ausencia de señal clara\n")
            f.write("  ✓ Captura baseline exitosa\n")
    
    print(f"[✓] Reporte guardado: {report_path}")

def main():
    if len(sys.argv) < 2:
        print("═" * 70)
        print("  ANALIZADOR DE ESPECTRO RF (rtl_power CSV)")
        print("═" * 70)
        print("")
        print("Uso: python3 analyze_spectrum.py <archivo.csv> [output_dir]")
        print("")
        print("Ejemplo:")
        print("  python3 analyze_spectrum.py data/spectrum_*.csv")
        print("  python3 analyze_spectrum.py data/captura.csv plots/")
        print("")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "plots"
    
    print("═" * 70)
    print("  ANÁLISIS DE ESPECTRO")
    print("═" * 70)
    print("")
    print(f"[*] Analizando: {csv_file}")
    print("")
    
    # Cargar CSV
    df = load_csv(csv_file)
    
    # Extraer potencia
    power_cols = [c for c in df.columns if 'dBm' in str(c) and '-' not in str(c)[:1]]
    if not power_cols:
        metadata = ['Date', 'Time', 'Hz_low', 'Hz_high', 'Hz_step', 'Samples']
        power_cols = [c for c in df.columns if c not in metadata]
    
    if not power_cols:
        print("[✗] Error: No se encontraron columnas de potencia")
        sys.exit(1)
    
    power_array = df[power_cols].values
    mean_power = np.mean(power_array, axis=1)
    
    print(f"[*] Rango de potencia: {mean_power.min():.1f} a {mean_power.max():.1f} dBm")
    
    # Detectar eventos
    events = detect_events(mean_power)
    print(f"[*] Eventos detectados: {len(events)}")
    
    if events:
        for i, evt in enumerate(events, 1):
            print(f"    E{i}: muestras {evt['start']:4d}-{evt['end']:4d}, "
                  f"P_max={evt['max_power']:7.2f} dBm, dur={evt['duration']:4d}")
    
    print("")
    
    # Generar gráficos
    freq_mhz, peak_power = plot_spectrum(df, output_dir)
    
    if events:
        time_array = np.arange(len(mean_power))
        plot_events(time_array, mean_power, events, output_dir)
    
    # Generar reporte
    generate_report(csv_file, freq_mhz, peak_power, events, output_dir)
    
    print("")
    print("═" * 70)
    print("[✓] ANÁLISIS COMPLETADO")
    print("═" * 70)
    print("")

if __name__ == "__main__":
    main()
