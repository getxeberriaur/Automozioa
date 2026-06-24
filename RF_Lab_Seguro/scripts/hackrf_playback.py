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
import struct
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
        """Carga archivo IQ8 (int8 I/Q samples)"""
        try:
            with open(self.filename, 'rb') as f:
                raw_data = f.read()
            
            # Convertir bytes a int8 (sin signo)
            iq_bytes = np.frombuffer(raw_data, dtype=np.int8)
            
            # Reconstruir pares I/Q complejos
            # Formato: I0 Q0 I1 Q1 I2 Q2 ...
            iq_float = iq_bytes.astype(np.float32) / 128.0
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
    
    def detect_events(self, threshold_db=10, min_samples=100):
        """
        Detecta eventos (pulsaciones) en los datos IQ
        
        Args:
            threshold_db: umbral sobre ruido de fondo
            min_samples: duración mínima de evento
            
        Returns:
            lista de eventos: (start_time_s, end_time_s, max_power_db)
        """
        # Potencia instantánea
        power = np.abs(self.data) ** 2
        power_db = 10 * np.log10(power + 1e-10)
        
        # Baseline
        baseline = np.percentile(power_db, 10)
        
        # Detectar actividad
        activity = power_db > (baseline + threshold_db)
        
        events = []
        in_event = False
        start_idx = 0
        max_power = baseline
        
        for i, is_active in enumerate(activity):
            if is_active and not in_event:
                start_idx = i
                in_event = True
                max_power = power_db[i]
            elif is_active and in_event:
                max_power = max(max_power, power_db[i])
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
                        'baseline_db': float(baseline)
                    })
                in_event = False
        
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
        events = self.detect_events()
        print(f"\n[*] Eventos detectados: {len(events)}")
        
        if events:
            print("\n    Evento | Tiempo Inicio | Duración | Potencia Máx | Baseline")
            print("    " + "-" * 65)
            for i, evt in enumerate(events, 1):
                print(f"      {i:2d}   | {evt['start_time']:6.2f}s      | "
                      f"{evt['duration']:6.3f}s   | {evt['max_power_db']:+7.1f} dBm | "
                      f"{evt['baseline_db']:+7.1f} dBm")
        
        # Estadísticas generales
        power = np.abs(self.data) ** 2
        power_db = 10 * np.log10(power + 1e-10)
        
        print(f"\n[*] Estadísticas de Potencia:")
        print(f"    Media:     {np.mean(power_db):+7.1f} dBm")
        print(f"    Mediana:   {np.median(power_db):+7.1f} dBm")
        print(f"    Desv. Est: {np.std(power_db):+7.1f} dB")
        print(f"    Mínima:    {np.min(power_db):+7.1f} dBm")
        print(f"    Máxima:    {np.max(power_db):+7.1f} dBm")
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
    
    args = parser.parse_args()
    
    # Validar archivo
    if not Path(args.file).exists():
        print(f"[✗] Archivo no encontrado: {args.file}")
        sys.exit(1)
    
    # Crear player
    player = IQPlayer(args.file, freq_hz=args.freq, sample_rate=args.rate)
    
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
