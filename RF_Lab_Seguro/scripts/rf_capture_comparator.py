#!/usr/bin/env python3

"""
rf_capture_comparator.py
Herramienta para comparar múltiples archivos IQ capturados.

Funcionalidades:
  - Comparar potencia y eventos entre archivos
  - Visualización lado a lado de espectros
  - Correlación temporal de eventos
  - Estadísticas comparativas
  - Exportar reporte de comparación

Uso:
  python3 rf_capture_comparator.py capture1.iq8 capture2.iq8
  python3 rf_capture_comparator.py *.iq8
  python3 rf_capture_comparator.py capture1.iq8 capture2.iq8 --report comparison.txt
"""

import argparse
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.fft import fft, fftfreq
from pathlib import Path
import sys


class IQCapture:
    """Representa una captura IQ individual."""
    
    def __init__(self, filename, freq_hz=433920000, sample_rate=2000000):
        self.filename = filename
        self.freq_hz = freq_hz
        self.sample_rate = sample_rate
        self.data = None
        self.power = None
        self.events = []
        self.stats = {}
        
        self.load_file()
        self.analyze()
    
    def load_file(self):
        """Carga archivo IQ8."""
        try:
            with open(self.filename, 'rb') as f:
                raw_data = f.read()
            
            iq_bytes = np.frombuffer(raw_data, dtype=np.uint8)
            iq_float = (iq_bytes.astype(np.float32) - 127.5) / 128.0
            self.data = iq_float[0::2] + 1j * iq_float[1::2]
            
            self.power = 10 * np.log10(np.abs(self.data) ** 2 + 1e-10)
            
        except Exception as e:
            print(f"[✗] Error cargando {self.filename}: {e}")
            raise
    
    def analyze(self):
        """Análisis completo de la captura."""
        # Estadísticas de potencia
        self.stats['duration_sec'] = len(self.data) / self.sample_rate
        self.stats['mean_power'] = np.mean(self.power)
        self.stats['median_power'] = np.median(self.power)
        self.stats['std_power'] = np.std(self.power)
        self.stats['min_power'] = np.min(self.power)
        self.stats['max_power'] = np.max(self.power)
        self.stats['samples'] = len(self.data)
        
        # Detectar eventos
        self._detect_events()
        self.stats['num_events'] = len(self.events)
    
    def _detect_events(self, threshold_db=5):
        """Detecta eventos en los datos."""
        baseline = np.percentile(self.power, 10)
        activity = self.power > (baseline + threshold_db)
        
        self.events = []
        in_event = False
        start_idx = 0
        
        for i, active in enumerate(activity):
            if active and not in_event:
                start_idx = i
                in_event = True
            elif not active and in_event:
                if i - start_idx > 100:
                    event_power = self.power[start_idx:i]
                    self.events.append({
                        'start': start_idx,
                        'end': i,
                        'duration_sec': (i - start_idx) / self.sample_rate,
                        'max_power': np.max(event_power),
                        'mean_power': np.mean(event_power)
                    })
                in_event = False
    
    def get_name(self):
        """Retorna nombre del archivo para display."""
        return Path(self.filename).stem


class CaptureComparator:
    """Compara múltiples capturas IQ."""
    
    def __init__(self, captures):
        """
        Args:
            captures: lista de objetos IQCapture
        """
        self.captures = captures
        self.comparison = None
    
    def compare_events(self):
        """Compara eventos temporales entre capturas."""
        comparison = {
            'total_captures': len(self.captures),
            'captures': []
        }
        
        for i, cap in enumerate(self.captures):
            cap_info = {
                'name': cap.get_name(),
                'num_events': len(cap.events),
                'events': cap.events
            }
            comparison['captures'].append(cap_info)
        
        return comparison
    
    def plot_comparison(self):
        """Visualiza comparación de todas las capturas."""
        n_caps = len(self.captures)
        
        fig = plt.figure(figsize=(16, 12))
        fig.suptitle(f'Comparación de Capturas RF ({n_caps} archivos)', 
                     fontsize=14, fontweight='bold')
        
        # ─────────────────────────────────────────────────────────
        # 1. POTENCIA EN TIEMPO (SUPERPUESTO)
        # ─────────────────────────────────────────────────────────
        ax1 = plt.subplot(3, 2, 1)
        colors = plt.cm.tab10(np.linspace(0, 1, n_caps))
        
        for cap, color in zip(self.captures, colors):
            time_array = np.arange(len(cap.power)) / cap.sample_rate
            ax1.plot(time_array, cap.power, label=cap.get_name(), color=color, alpha=0.7, linewidth=0.8)
        
        ax1.set_xlabel('Tiempo (s)', fontsize=10)
        ax1.set_ylabel('Potencia (dBm)', fontsize=10)
        ax1.set_title('Potencia Superpuesta (todas las capturas)', fontsize=11, fontweight='bold')
        ax1.legend(fontsize=9, loc='upper right')
        ax1.grid(True, alpha=0.3)
        
        # ─────────────────────────────────────────────────────────
        # 2. ESTADÍSTICAS EN TABLA
        # ─────────────────────────────────────────────────────────
        ax2 = plt.subplot(3, 2, 2)
        ax2.axis('tight')
        ax2.axis('off')
        
        table_data = [['Captura', 'Duración (s)', 'Eventos', 'Media (dBm)', 'Min/Max (dBm)']]
        for cap in self.captures:
            stats = cap.stats
            table_data.append([
                cap.get_name(),
                f"{stats['duration_sec']:.1f}",
                f"{stats['num_events']}",
                f"{stats['mean_power']:.1f}",
                f"{stats['min_power']:.1f} / {stats['max_power']:.1f}"
            ])
        
        table = ax2.table(cellText=table_data, cellLoc='center', loc='center',
                         colWidths=[0.25, 0.15, 0.15, 0.15, 0.3])
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1, 2)
        
        # Colorear encabezado
        for i in range(len(table_data[0])):
            table[(0, i)].set_facecolor('#4CAF50')
            table[(0, i)].set_text_props(weight='bold', color='white')
        
        ax2.set_title('Estadísticas Comparativas', fontsize=11, fontweight='bold')
        
        # ─────────────────────────────────────────────────────────
        # 3-4. ESPECTROS FFT
        # ─────────────────────────────────────────────────────────
        for idx, (cap, color) in enumerate(zip(self.captures[:2], colors)):
            ax = plt.subplot(3, 2, 3 + idx)
            
            # FFT sobre todo el archivo (o los primeros 10s)
            duration_sec = min(10, cap.stats['duration_sec'])
            end_idx = int(duration_sec * cap.sample_rate)
            segment = cap.data[:end_idx]
            
            windowed = segment * np.hanning(len(segment))
            fft_result = fft(windowed)
            magnitude = np.abs(fft_result)
            magnitude_db = 10 * np.log10(magnitude + 1e-10)
            freqs = fftfreq(len(segment), 1 / cap.sample_rate)[:len(segment)//2]
            
            ax.semilogy(freqs / 1e6, magnitude_db[:len(segment)//2], color=color, linewidth=1.5)
            ax.set_xlabel('Frecuencia (MHz)', fontsize=10)
            ax.set_ylabel('Magnitud (dB)', fontsize=10)
            ax.set_title(f'Espectro: {cap.get_name()} (primeros {duration_sec:.1f}s)', 
                        fontsize=11, fontweight='bold')
            ax.grid(True, alpha=0.3)
        
        # ─────────────────────────────────────────────────────────
        # 5. COMPARACIÓN DE EVENTOS (TIMELINE)
        # ─────────────────────────────────────────────────────────
        ax5 = plt.subplot(3, 2, 5)
        
        y_pos = 0
        for cap, color in zip(self.captures, colors):
            time_array = np.arange(len(cap.power)) / cap.sample_rate
            ax5.plot(time_array, cap.power / 10 + y_pos, label=cap.get_name(), 
                    color=color, alpha=0.7, linewidth=0.8)
            
            # Marcar eventos
            for evt in cap.events:
                evt_start = evt['start'] / cap.sample_rate
                evt_end = evt['end'] / cap.sample_rate
                ax5.axvline(evt_start, color=color, linestyle=':', alpha=0.5, linewidth=1)
            
            y_pos += 5
        
        ax5.set_xlabel('Tiempo (s)', fontsize=10)
        ax5.set_ylabel('Potencia (dB, offset por captura)', fontsize=10)
        ax5.set_title('Eventos Detectados (líneas punteadas)', fontsize=11, fontweight='bold')
        ax5.legend(fontsize=9, loc='upper right')
        ax5.grid(True, alpha=0.3)
        
        # ─────────────────────────────────────────────────────────
        # 6. CORRELACIÓN DE DURACIONES DE EVENTOS
        # ─────────────────────────────────────────────────────────
        ax6 = plt.subplot(3, 2, 6)
        
        for cap, color in zip(self.captures, colors):
            if cap.events:
                event_durations = [e['duration_sec'] * 1000 for e in cap.events]  # ms
                ax6.hist(event_durations, bins=20, alpha=0.6, label=cap.get_name(), color=color)
        
        ax6.set_xlabel('Duración de Evento (ms)', fontsize=10)
        ax6.set_ylabel('Conteo', fontsize=10)
        ax6.set_title('Distribución de Duraciones de Eventos', fontsize=11, fontweight='bold')
        ax6.legend(fontsize=9)
        ax6.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.show()
    
    def generate_report(self, output_file=None):
        """Genera reporte de comparación."""
        report = "╔════════════════════════════════════════════════════════════════╗\n"
        report += "║           REPORTE DE COMPARACIÓN DE CAPTURAS RF                ║\n"
        report += "╚════════════════════════════════════════════════════════════════╝\n\n"
        
        report += f"[*] Total de capturas analizadas: {len(self.captures)}\n\n"
        
        for i, cap in enumerate(self.captures, 1):
            report += f"─────────────────────────────────────────────────────────────────\n"
            report += f"CAPTURA {i}: {cap.get_name()}\n"
            report += f"─────────────────────────────────────────────────────────────────\n"
            report += f"  Archivo:           {cap.filename}\n"
            report += f"  Duración:          {cap.stats['duration_sec']:.2f} segundos\n"
            report += f"  Total muestras:    {cap.stats['samples']:,}\n"
            report += f"  Frecuencia:        {cap.freq_hz / 1e6:.3f} MHz\n"
            report += f"  Sample rate:       {cap.sample_rate / 1e6:.2f} MHz\n"
            report += f"\n  ESTADÍSTICAS DE POTENCIA:\n"
            report += f"    Media:           {cap.stats['mean_power']:.2f} dBm\n"
            report += f"    Mediana:         {cap.stats['median_power']:.2f} dBm\n"
            report += f"    Desv. Est.:      {cap.stats['std_power']:.2f} dB\n"
            report += f"    Mínima:          {cap.stats['min_power']:.2f} dBm\n"
            report += f"    Máxima:          {cap.stats['max_power']:.2f} dBm\n"
            report += f"    Rango:           {cap.stats['max_power'] - cap.stats['min_power']:.2f} dB\n"
            report += f"\n  EVENTOS DETECTADOS: {cap.stats['num_events']}\n"
            
            if cap.events:
                report += f"\n    Nº │ Inicio (s) │ Duración (ms) │ Potencia Máx (dBm) │ Potencia Media (dBm)\n"
                report += f"    ─────────────────────────────────────────────────────────────────────────────\n"
                for j, evt in enumerate(cap.events[:10], 1):
                    report += f"    {j:2d} │ {evt['start']/cap.sample_rate:9.3f} │ "
                    report += f"{evt['duration_sec']*1000:13.1f} │ {evt['max_power']:17.1f} │ {evt['mean_power']:19.1f}\n"
                
                if len(cap.events) > 10:
                    report += f"\n    ... (+{len(cap.events) - 10} eventos más)\n"
            else:
                report += f"    (Sin eventos detectados)\n"
            
            report += "\n"
        
        # Comparativa global
        report += "═════════════════════════════════════════════════════════════════\n"
        report += "RESUMEN COMPARATIVO\n"
        report += "═════════════════════════════════════════════════════════════════\n\n"
        
        # Captura más corta y más larga
        durations = [cap.stats['duration_sec'] for cap in self.captures]
        min_cap = self.captures[np.argmin(durations)]
        max_cap = self.captures[np.argmax(durations)]
        report += f"Captura más corta:  {min_cap.get_name()} ({min(durations):.2f}s)\n"
        report += f"Captura más larga:  {max_cap.get_name()} ({max(durations):.2f}s)\n\n"
        
        # Potencia
        mean_powers = [cap.stats['mean_power'] for cap in self.captures]
        strongest = self.captures[np.argmax(mean_powers)]
        weakest = self.captures[np.argmin(mean_powers)]
        report += f"Señal más fuerte:   {strongest.get_name()} ({max(mean_powers):.1f} dBm media)\n"
        report += f"Señal más débil:    {weakest.get_name()} ({min(mean_powers):.1f} dBm media)\n\n"
        
        # Eventos
        event_counts = [cap.stats['num_events'] for cap in self.captures]
        most_events = self.captures[np.argmax(event_counts)]
        report += f"Más eventos:        {most_events.get_name()} ({max(event_counts)} eventos)\n"
        report += f"Menos eventos:      {self.captures[np.argmin(event_counts)].get_name()} ({min(event_counts)} eventos)\n\n"
        
        report += "═════════════════════════════════════════════════════════════════\n"
        
        if output_file:
            Path(output_file).parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, 'w') as f:
                f.write(report)
            print(f"[✓] Reporte guardado: {output_file}")
        
        print(report)
        return report


def main():
    parser = argparse.ArgumentParser(
        description='Compara múltiples archivos IQ capturados.'
    )
    parser.add_argument('files', nargs='+', help='Rutas a archivos .iq8')
    parser.add_argument('--freq', type=int, default=433920000,
                       help='Frecuencia central en Hz (default: 433.92 MHz)')
    parser.add_argument('--rate', type=int, default=2000000,
                       help='Sample rate en Hz (default: 2 MHz)')
    parser.add_argument('--report', type=str, default=None,
                       help='Guardar reporte en archivo')
    
    args = parser.parse_args()
    
    # Cargar capturas
    captures = []
    for filepath in args.files:
        if not Path(filepath).exists():
            print(f"[✗] Archivo no encontrado: {filepath}")
            continue
        
        try:
            cap = IQCapture(filepath, freq_hz=args.freq, sample_rate=args.rate)
            captures.append(cap)
            print(f"[✓] Cargada: {cap.get_name()} ({cap.stats['duration_sec']:.1f}s, {cap.stats['num_events']} eventos)")
        except Exception as e:
            print(f"[✗] Error cargando {filepath}: {e}")
    
    if not captures:
        print("[✗] No se cargaron capturas válidas")
        sys.exit(1)
    
    if len(captures) == 1:
        print("[!] Se requieren al menos 2 capturas para comparar. Use hackrf_interactive.py para una sola captura.")
        sys.exit(1)
    
    # Comparar
    print(f"\n[*] Comparando {len(captures)} capturas...\n")
    comparator = CaptureComparator(captures)
    comparator.generate_report(args.report)
    comparator.plot_comparison()


if __name__ == '__main__':
    main()
