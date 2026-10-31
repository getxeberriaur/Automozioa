#!/usr/bin/env python3

"""
hackrf_interactive.py
Interfaz interactiva para reproducción y análisis en tiempo real de archivos IQ.

Características:
  - Cargar archivos IQ capturados (RTL-SDR o HackRF)
  - Navegación interactiva (slider de tiempo)
  - Visualización en vivo de espectro, potencia y espectrograma
  - Detección automática de eventos (pulsaciones)
  - Exportación de gráficos individuales
  - Comparación visual entre eventos

Uso:
  python3 hackrf_interactive.py capture.iq8
  python3 hackrf_interactive.py capture.iq8 --freq 433920000 --rate 2000000
"""

import argparse
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from matplotlib.animation import FuncAnimation
from scipy import signal
from scipy.fft import fft, fftfreq
from pathlib import Path
import sys


class InteractiveIQPlayer:
    """Reproductor IQ interactivo con interfaz gráfica."""
    
    def __init__(self, filename, freq_hz=433920000, sample_rate=2000000, 
                 window_size=4096, event_threshold_db=5):
        """
        Inicializa reproductor interactivo.
        
        Args:
            filename: ruta a archivo .iq8
            freq_hz: frecuencia central en Hz
            sample_rate: tasa de muestreo en Hz
            window_size: número de muestras para FFT
            event_threshold_db: umbral para detectar eventos (dB sobre baseline)
        """
        self.filename = filename
        self.freq_hz = freq_hz
        self.sample_rate = sample_rate
        self.window_size = window_size
        self.event_threshold_db = event_threshold_db
        
        self.data = None
        self.power = None
        self.events = []
        self.current_position = 0
        
        self.load_file()
        self.detect_events()
        
    def load_file(self):
        """Carga archivo IQ8 (uint8 I/Q samples)."""
        try:
            with open(self.filename, 'rb') as f:
                raw_data = f.read()
            
            iq_bytes = np.frombuffer(raw_data, dtype=np.uint8)
            iq_float = (iq_bytes.astype(np.float32) - 127.5) / 128.0
            self.data = iq_float[0::2] + 1j * iq_float[1::2]
            
            # Calcular potencia
            self.power = 10 * np.log10(np.abs(self.data) ** 2 + 1e-10)
            
            duration_sec = len(self.data) / self.sample_rate
            print(f"[✓] Archivo cargado: {self.filename}")
            print(f"    Muestras IQ: {len(self.data):,}")
            print(f"    Duración: {duration_sec:.2f} segundos")
            print(f"    Frecuencia: {self.freq_hz / 1e6:.3f} MHz")
            print(f"    Sample Rate: {self.sample_rate / 1e6:.2f} MHz")
            
        except Exception as e:
            print(f"[✗] Error cargando {self.filename}: {e}")
            sys.exit(1)
    
    def detect_events(self):
        """Detecta automáticamente eventos (pulsaciones) en los datos."""
        # Calcular baseline
        baseline = np.percentile(self.power, 10)
        
        # Detectar actividad
        activity = self.power > (baseline + self.event_threshold_db)
        
        # Agrupar eventos consecutivos
        self.events = []
        in_event = False
        start_idx = 0
        
        for i, active in enumerate(activity):
            if active and not in_event:
                start_idx = i
                in_event = True
            elif not active and in_event:
                if i - start_idx > 100:  # Duración mínima
                    event_power = self.power[start_idx:i]
                    self.events.append({
                        'start': start_idx,
                        'end': i,
                        'duration_samples': i - start_idx,
                        'duration_sec': (i - start_idx) / self.sample_rate,
                        'max_power': np.max(event_power),
                        'mean_power': np.mean(event_power),
                        'baseline': baseline
                    })
                in_event = False
        
        print(f"\n[*] Eventos detectados: {len(self.events)}")
        for i, evt in enumerate(self.events[:10], 1):
            print(f"    E{i}: {evt['start']/self.sample_rate:.2f}s - {evt['end']/self.sample_rate:.2f}s "
                  f"(duracion {evt['duration_sec']:.3f}s, potencia máx {evt['max_power']:.1f} dBm)")
    
    def get_segment(self, start_idx, end_idx):
        """Extrae segmento de datos IQ."""
        if start_idx < 0:
            start_idx = 0
        if end_idx > len(self.data):
            end_idx = len(self.data)
        return self.data[start_idx:end_idx]
    
    def compute_fft(self, segment):
        """Calcula FFT de un segmento."""
        windowed = segment * np.hanning(len(segment))
        fft_result = fft(windowed)
        magnitude = np.abs(fft_result)
        magnitude_db = 10 * np.log10(magnitude + 1e-10)
        return magnitude_db
    
    def compute_spectrogram(self, start_sample, duration_samples, nperseg=1024):
        """Calcula espectrograma de una ventana."""
        end_sample = min(start_sample + duration_samples, len(self.data))
        segment = self.data[start_sample:end_sample]
        
        frequencies, times, Sxx = signal.spectrogram(
            segment, 
            fs=self.sample_rate, 
            nperseg=nperseg,
            noverlap=nperseg//2,
            window='hann',
            scaling='spectrum'
        )
        
        Sxx_db = 10 * np.log10(Sxx + 1e-10)
        return frequencies, times + start_sample / self.sample_rate, Sxx_db
    
    def plot_interactive(self):
        """Crea interfaz interactiva con subgráficos."""
        # Configurar figura
        fig = plt.figure(figsize=(16, 10))
        fig.suptitle(f'Análisis Interactivo: {Path(self.filename).name}', fontsize=14, fontweight='bold')
        
        # Subgráficos
        ax_timeline = plt.subplot(4, 2, (1, 2))  # Potencia en tiempo (arriba, ancho)
        ax_fft = plt.subplot(4, 2, 3)             # FFT/Espectro
        ax_power_hist = plt.subplot(4, 2, 4)      # Histograma potencia
        ax_spectrogram = plt.subplot(4, 2, (5, 6)) # Espectrograma (ancho)
        ax_waterfall = plt.subplot(4, 2, 7)       # Waterfall zoomed
        ax_event_list = plt.subplot(4, 2, 8)      # Lista de eventos
        
        # Variables de estado
        self.current_time_sec = 0.0
        self.window_duration_sec = 10.0  # Ventana por defecto de 10 segundos
        
        # ─────────────────────────────────────────────────────────
        # 1. GRÁFICO DE POTENCIA EN TIEMPO (TIMELINE)
        # ─────────────────────────────────────────────────────────
        time_array = np.arange(len(self.power)) / self.sample_rate
        ax_timeline.plot(time_array, self.power, 'b-', linewidth=0.5, alpha=0.7)
        ax_timeline.fill_between(time_array, self.power, alpha=0.3)
        
        # Marcar eventos
        for i, evt in enumerate(self.events):
            start_sec = evt['start'] / self.sample_rate
            end_sec = evt['end'] / self.sample_rate
            ax_timeline.axvspan(start_sec, end_sec, alpha=0.2, color='red')
            ax_timeline.text(start_sec, evt['max_power'], f"E{i+1}", fontsize=8)
        
        # Línea de posición actual
        self.timeline_vline = ax_timeline.axvline(x=0, color='red', linestyle='--', linewidth=2)
        ax_timeline.set_xlabel('Tiempo (s)', fontsize=10)
        ax_timeline.set_ylabel('Potencia (dBm)', fontsize=10)
        ax_timeline.set_title('Potencia a lo largo del tiempo', fontsize=11, fontweight='bold')
        ax_timeline.grid(True, alpha=0.3)
        
        # ─────────────────────────────────────────────────────────
        # 2. SLIDER DE TIEMPO
        # ─────────────────────────────────────────────────────────
        ax_slider = plt.axes([0.2, 0.02, 0.6, 0.03])
        max_time = len(self.data) / self.sample_rate
        slider_time = Slider(ax_slider, 'Tiempo (s)', 0, max(0, max_time - self.window_duration_sec),
                             valinit=0, color='green')
        
        def update_time(val):
            """Callback para actualizar con slider."""
            self.current_time_sec = slider_time.val
            update_all()
        
        slider_time.on_changed(update_time)
        
        # ─────────────────────────────────────────────────────────
        # FUNCIÓN PRINCIPAL DE ACTUALIZACIÓN
        # ─────────────────────────────────────────────────────────
        def update_all():
            """Actualiza todos los gráficos con la ventana actual."""
            start_sec = self.current_time_sec
            end_sec = min(start_sec + self.window_duration_sec, max_time)
            
            start_idx = int(start_sec * self.sample_rate)
            end_idx = int(end_sec * self.sample_rate)
            
            # Actualizar línea en timeline
            self.timeline_vline.set_xdata([start_sec, start_sec])
            
            # ─── Segmento actual ───
            segment = self.get_segment(start_idx, end_idx)
            window_time = np.arange(len(segment)) / self.sample_rate + start_sec
            window_power = 10 * np.log10(np.abs(segment) ** 2 + 1e-10)
            
            # ─── FFT ───
            ax_fft.clear()
            fft_mag = self.compute_fft(segment)
            freqs = fftfreq(len(segment), 1 / self.sample_rate)[:len(segment)//2]
            ax_fft.semilogy(freqs / 1e6, fft_mag[:len(segment)//2])
            ax_fft.set_xlabel('Frecuencia relativa (MHz)', fontsize=9)
            ax_fft.set_ylabel('Magnitud (dB)', fontsize=9)
            ax_fft.set_title('Espectro FFT (ventana actual)', fontsize=10)
            ax_fft.grid(True, alpha=0.3)
            
            # ─── Histograma de Potencia ───
            ax_power_hist.clear()
            ax_power_hist.hist(window_power, bins=30, color='cyan', edgecolor='black', alpha=0.7)
            ax_power_hist.axvline(np.mean(window_power), color='red', linestyle='--', label=f'Media: {np.mean(window_power):.1f} dBm')
            ax_power_hist.set_xlabel('Potencia (dBm)', fontsize=9)
            ax_power_hist.set_ylabel('Conteo', fontsize=9)
            ax_power_hist.set_title('Distribución de Potencia', fontsize=10)
            ax_power_hist.legend(fontsize=8)
            ax_power_hist.grid(True, alpha=0.3, axis='y')
            
            # ─── Espectrograma ───
            ax_spectrogram.clear()
            freqs, times, Sxx = self.compute_spectrogram(start_idx, end_idx - start_idx)
            im = ax_spectrogram.pcolormesh(times, freqs / 1e3, Sxx, shading='auto', cmap='viridis')
            ax_spectrogram.set_ylabel('Frecuencia (kHz)', fontsize=9)
            ax_spectrogram.set_xlabel('Tiempo (s)', fontsize=9)
            ax_spectrogram.set_title('Espectrograma (Potencia vs Frecuencia vs Tiempo)', fontsize=10)
            plt.colorbar(im, ax=ax_spectrogram, label='Potencia (dB)')
            
            # ─── Waterfall zoomed ───
            ax_waterfall.clear()
            window_power_zoomed = window_power[::max(1, len(window_power) // 500)]  # Limitar puntos
            ax_waterfall.plot(window_time[::max(1, len(window_time) // 500)], window_power_zoomed, 'b-', linewidth=1.5)
            ax_waterfall.fill_between(window_time[::max(1, len(window_time) // 500)], window_power_zoomed, alpha=0.3)
            ax_waterfall.set_xlabel('Tiempo (s)', fontsize=9)
            ax_waterfall.set_ylabel('Potencia (dBm)', fontsize=9)
            ax_waterfall.set_title('Potencia (zoom ventana actual)', fontsize=10)
            ax_waterfall.grid(True, alpha=0.3)
            
            # ─── Lista de eventos ───
            ax_event_list.clear()
            ax_event_list.axis('off')
            event_text = "EVENTOS DETECTADOS\n" + "="*30 + "\n\n"
            for i, evt in enumerate(self.events[:5], 1):
                evt_start_sec = evt['start'] / self.sample_rate
                evt_end_sec = evt['end'] / self.sample_rate
                in_window = (evt_start_sec >= start_sec) and (evt_start_sec < end_sec)
                marker = "► " if in_window else "  "
                event_text += f"{marker}E{i}: {evt_start_sec:.2f}s ({evt['duration_sec']:.3f}s)\n"
                event_text += f"      Pmax={evt['max_power']:.1f} dBm\n"
                event_text += f"      Pmean={evt['mean_power']:.1f} dBm\n\n"
            
            if len(self.events) > 5:
                event_text += f"... (+{len(self.events) - 5} más)\n"
            
            ax_event_list.text(0.05, 0.95, event_text, transform=ax_event_list.transAxes,
                             fontsize=8, verticalalignment='top', family='monospace',
                             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
            
            fig.canvas.draw_idle()
        
        # Actualización inicial
        update_all()
        
        # Botones de control
        # Anterior
        ax_prev = plt.axes([0.05, 0.05, 0.08, 0.04])
        btn_prev = Button(ax_prev, '◀ Anterior', color='lightblue')
        def prev_window(event):
            slider_time.set_val(max(0, slider_time.val - self.window_duration_sec / 2))
        btn_prev.on_clicked(prev_window)
        
        # Siguiente
        ax_next = plt.axes([0.87, 0.05, 0.08, 0.04])
        btn_next = Button(ax_next, 'Siguiente ▶', color='lightblue')
        def next_window(event):
            slider_time.set_val(min(max_time - self.window_duration_sec, slider_time.val + self.window_duration_sec / 2))
        btn_next.on_clicked(next_window)
        
        plt.tight_layout(rect=[0, 0.08, 1, 0.97])
        plt.show()


def main():
    parser = argparse.ArgumentParser(
        description='Interfaz interactiva para análisis de archivos IQ capturados.'
    )
    parser.add_argument('filename', help='Ruta a archivo .iq8')
    parser.add_argument('--freq', type=int, default=433920000, 
                       help='Frecuencia central en Hz (default: 433.92 MHz)')
    parser.add_argument('--rate', type=int, default=2000000,
                       help='Sample rate en Hz (default: 2 MHz)')
    parser.add_argument('--threshold', type=float, default=5,
                       help='Umbral de detección de eventos en dB (default: 5)')
    
    args = parser.parse_args()
    
    if not Path(args.filename).exists():
        print(f"[✗] Archivo no encontrado: {args.filename}")
        sys.exit(1)
    
    player = InteractiveIQPlayer(
        args.filename,
        freq_hz=args.freq,
        sample_rate=args.rate,
        event_threshold_db=args.threshold
    )
    
    player.plot_interactive()


if __name__ == '__main__':
    main()
