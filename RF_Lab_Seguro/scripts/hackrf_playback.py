#!/usr/bin/env python3

"""
hackrf_playback.py
Reproducción y visualización de archivos IQ capturados con RTL-SDR
en HackRF One, con análisis espectral en tiempo real.

Uso: 
    python3 hackrf_playback.py capture_20260624_123456.iq8
    python3 hackrf_playback.py capture.iq8 --freq 433920000 --rate 2000000
"""

import argparse
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.fft import fft, fftfreq
import sys
from pathlib import Path

class IQPlayer:
    def __init__(self, filename, freq_hz=433920000, sample_rate=2000000, block_size=4096):
        """
        Inicializa reproductor IQ
        
        Args:
            filename: ruta a archivo .iq8
            freq_hz: frecuencia central en Hz
            sample_rate: tasa de muestreo en Hz
            block_size: tamaño de bloque para procesamiento
        """
        self.filename = filename
        self.freq_hz = freq_hz
        self.sample_rate = sample_rate
        self.block_size = block_size
        self.data = None
        self.load_file()
        
    def load_file(self):
        """Carga archivo IQ8 (uint8 I/Q samples, formato rtl_sdr)."""
        try:
            with open(self.filename, 'rb') as f:
                raw_data = f.read()
            
            # rtl_sdr genera uint8 intercalado: I0 Q0 I1 Q1 ... (centro ~127.5)
            iq_bytes = np.frombuffer(raw_data, dtype=np.uint8)
            
            # Reconstruir pares I/Q complejos
            # Formato: I0 Q0 I1 Q1 I2 Q2 ...
            iq_float = (iq_bytes.astype(np.float32) - 127.5) / 128.0
            self.data = iq_float[0::2] + 1j * iq_float[1::2]
            
            duration_sec = len(self.data) / self.sample_rate
            print(f"[✓] Archivo cargado: {self.filename}")
            print(f"    Muestras IQ: {len(self.data):,}")
            print(f"    Duración: {duration_sec:.2f} segundos")
            print(f"    Frecuencia: {self.freq_hz / 1e6:.3f} MHz")
            print(f"    Sample Rate: {self.sample_rate / 1e6:.2f} MHz")
            
        except Exception as e:
            print(f"[✗] Error al cargar: {e}")
            sys.exit(1)
    
    def compute_spectrum(self, start_sample=0, num_samples=None):
        """Calcula espectro FFT"""
        if num_samples is None:
            num_samples = min(self.block_size * 10, len(self.data) - start_sample)
        
        segment = self.data[start_sample:start_sample + num_samples]
        
        # FFT
        fft_result = fft(segment, n=4096)
        magnitude = np.abs(fft_result) ** 2
        magnitude_db = 10 * np.log10(magnitude + 1e-10)
        
        # Frecuencias relativas a portadora
        freqs = fftfreq(4096, 1/self.sample_rate) / 1e6  # en MHz relativo
        
        return freqs, magnitude_db
    
    def detect_events(self, threshold_db=6.0, min_duration_ms=8.0, smooth_ms=2.0, merge_gap_ms=5.0):
        """
        Detecta eventos (pulsaciones) en los datos IQ
        
        Args:
            threshold_db: umbral sobre baseline en dB
            min_duration_ms: duración mínima de evento (ms)
            smooth_ms: ventana de suavizado para envolvente (ms)
            merge_gap_ms: une fragmentos separados por huecos cortos (ms)
            
        Returns:
            lista de eventos: (start_time_s, end_time_s, max_power_db)
        """
        if self.data is None or len(self.data) == 0:
            return []

        # Envolvente de potencia (dBFS) + suavizado para evitar microcortes OOK
        power = np.abs(self.data) ** 2
        power_db = 10 * np.log10(power + 1e-12)

        smooth_samples = max(1, int(self.sample_rate * smooth_ms / 1000.0))
        if smooth_samples > 1:
            kernel = np.ones(smooth_samples, dtype=np.float32) / smooth_samples
            smooth_db = np.convolve(power_db, kernel, mode='same')
        else:
            smooth_db = power_db

        baseline = float(np.percentile(smooth_db, 20))
        median = float(np.median(smooth_db))
        mad = float(np.median(np.abs(smooth_db - median)))
        robust_sigma = 1.4826 * mad

        adaptive_threshold = max(baseline + threshold_db, median + 4.0 * robust_sigma)
        activity = smooth_db > adaptive_threshold

        # Cerrar huecos cortos entre fragmentos del mismo evento
        merge_gap_samples = max(1, int(self.sample_rate * merge_gap_ms / 1000.0))
        gap_count = 0
        for i in range(len(activity)):
            if activity[i]:
                gap_count = 0
            else:
                gap_count += 1
                if 0 < gap_count <= merge_gap_samples:
                    activity[i] = True

        min_samples = max(1, int(self.sample_rate * min_duration_ms / 1000.0))
        events = []
        in_event = False
        start_idx = 0
        max_power = baseline

        for i, is_active in enumerate(activity):
            if is_active and not in_event:
                start_idx = i
                in_event = True
                max_power = smooth_db[i]
            elif is_active and in_event:
                max_power = max(max_power, smooth_db[i])
            elif not is_active and in_event:
                duration = i - start_idx
                if duration >= min_samples:
                    start_time = start_idx / self.sample_rate
                    end_time = i / self.sample_rate
                    events.append({
                        'start_sample': start_idx,
                        'end_sample': i,
                        'start_time': start_time,
                        'end_time': end_time,
                        'duration': end_time - start_time,
                        'max_power_db': float(max_power),
                        'baseline_db': float(baseline),
                        'threshold_db': float(adaptive_threshold),
                    })
                in_event = False

        # Cierre de evento si llega al final del archivo
        if in_event:
            duration = len(activity) - start_idx
            if duration >= min_samples:
                start_time = start_idx / self.sample_rate
                end_time = len(activity) / self.sample_rate
                events.append({
                    'start_sample': start_idx,
                    'end_sample': len(activity),
                    'start_time': start_time,
                    'end_time': end_time,
                    'duration': end_time - start_time,
                    'max_power_db': float(max_power),
                    'baseline_db': float(baseline),
                    'threshold_db': float(adaptive_threshold),
                })

        return events
    
    def plot_overview(self, output_file=None):
        """Genera gráfica general de potencia"""
        power = np.abs(self.data) ** 2
        power_db = 10 * np.log10(power + 1e-10)
        
        time_s = np.arange(len(power_db)) / self.sample_rate
        
        fig, ax = plt.subplots(figsize=(14, 6))
        ax.plot(time_s, power_db, linewidth=0.5, alpha=0.7)
        ax.set_xlabel('Tiempo (s)')
        ax.set_ylabel('Potencia (dBm)')
        ax.set_title(f'Potencia en el Tiempo - {self.filename}')
        ax.grid(True, alpha=0.3)
        
        if output_file:
            plt.savefig(output_file, dpi=150, bbox_inches='tight')
            print(f"[✓] Gráfico guardado: {output_file}")
        else:
            plt.show()
        
        plt.close()
    
    def plot_spectrogram(self, output_file=None):
        """Genera espectrograma (tiempo-frecuencia)"""
        # Calcular espectrograma
        f, t, Sxx = signal.spectrogram(
            self.data,
            self.sample_rate,
            nperseg=1024,
            noverlap=512,
            scaling='density'
        )
        
        # Convertir a dB
        Sxx_db = 10 * np.log10(Sxx + 1e-10)
        
        # Frequencies relativas a portadora (en kHz)
        f_rel = f / 1e3
        
        fig, ax = plt.subplots(figsize=(14, 8))
        pcm = ax.pcolormesh(t, f_rel, Sxx_db, shading='gouraud', cmap='viridis')
        ax.set_ylabel('Frecuencia Relativa (kHz)')
        ax.set_xlabel('Tiempo (s)')
        ax.set_title(f'Espectrograma - {self.filename}')
        cbar = fig.colorbar(pcm, ax=ax, label='Potencia (dB)')
        
        if output_file:
            plt.savefig(output_file, dpi=150, bbox_inches='tight')
            print(f"[✓] Espectrograma guardado: {output_file}")
        else:
            plt.show()
        
        plt.close()
    
    def generate_report(self):
        """Genera informe de análisis"""
        print("\n" + "="*70)
        print("ANÁLISIS DE ARCHIVO IQ")
        print("="*70)
        
        # Detectar eventos
        events = self.detect_events(
            threshold_db=self.threshold_db,
            min_duration_ms=self.min_duration_ms,
            smooth_ms=self.smooth_ms,
            merge_gap_ms=self.merge_gap_ms,
        )
        print(f"\n[*] Eventos detectados: {len(events)}")
        
        if events:
            print("\n    Evento | Tiempo Inicio | Duración | Potencia Máx | Baseline | Umbral")
            print("    " + "-" * 78)
            for i, evt in enumerate(events, 1):
                print(f"      {i:2d}   | {evt['start_time']:6.2f}s      | "
                      f"{evt['duration']:6.3f}s   | {evt['max_power_db']:+7.1f} dBFS | "
                      f"{evt['baseline_db']:+7.1f} dBFS | {evt['threshold_db']:+7.1f} dBFS")
        else:
            print("\n[!] No se detectaron eventos con los parámetros actuales.")
            print("[!] Prueba: --threshold 3 --min-duration-ms 2 --smooth-ms 1")
        
        # Estadísticas generales
        power = np.abs(self.data) ** 2
        power_db = 10 * np.log10(power + 1e-10)
        
        print(f"\n[*] Estadísticas de Potencia (dBFS):")
        print(f"    Media:     {np.mean(power_db):+7.1f} dBFS")
        print(f"    Mediana:   {np.median(power_db):+7.1f} dBFS")
        print(f"    Desv. Est: {np.std(power_db):+7.1f} dB")
        print(f"    Mínima:    {np.min(power_db):+7.1f} dBFS")
        print(f"    Máxima:    {np.max(power_db):+7.1f} dBFS")
        print("="*70 + "\n")

def main():
    parser = argparse.ArgumentParser(
        description='Reproduce y analiza archivos IQ capturados con RTL-SDR'
    )
    parser.add_argument('file', help='Archivo .iq8 de entrada')
    parser.add_argument('--freq', type=int, default=433920000,
                       help='Frecuencia central en Hz (default: 433.92 MHz)')
    parser.add_argument('--rate', type=int, default=2000000,
                       help='Tasa de muestreo en Hz (default: 2 MHz)')
    parser.add_argument('--report', action='store_true',
                       help='Mostrar informe de análisis')
    parser.add_argument('--plot-power', metavar='FILE',
                       help='Guardar gráfico de potencia en tiempo')
    parser.add_argument('--plot-spectrogram', metavar='FILE',
                       help='Guardar espectrograma')
    parser.add_argument('--threshold', type=float, default=6.0,
                       help='Umbral sobre baseline en dB (default: 6)')
    parser.add_argument('--min-duration-ms', type=float, default=8.0,
                       help='Duración mínima de evento en ms (default: 8)')
    parser.add_argument('--smooth-ms', type=float, default=2.0,
                       help='Ventana de suavizado en ms (default: 2)')
    parser.add_argument('--merge-gap-ms', type=float, default=5.0,
                       help='Une huecos menores a X ms (default: 5)')
    
    args = parser.parse_args()
    
    # Validar archivo
    if not Path(args.file).exists():
        print(f"[✗] Archivo no encontrado: {args.file}")
        sys.exit(1)
    
    # Crear player
    player = IQPlayer(args.file, freq_hz=args.freq, sample_rate=args.rate)
    player.threshold_db = args.threshold
    player.min_duration_ms = args.min_duration_ms
    player.smooth_ms = args.smooth_ms
    player.merge_gap_ms = args.merge_gap_ms
    
    # Generar reporte si se solicita
    if args.report:
        player.generate_report()
    
    # Generar gráficos
    if args.plot_power:
        player.plot_overview(args.plot_power)
    
    if args.plot_spectrogram:
        player.plot_spectrogram(args.plot_spectrogram)
    
    # Si no hay opciones, mostrar reporte por defecto
    if not (args.report or args.plot_power or args.plot_spectrogram):
        player.generate_report()
        print("[*] Tip: Usa --plot-power o --plot-spectrogram para gráficos")

if __name__ == '__main__':
    main()
