#!/usr/bin/env python3
"""
decoy_traffic.py — Inyector de tráfico señuelo para CTF Automotive

Genera tráfico CAN ficticio sobre vcan0 para que la Fase 1 del CTF
sea un reconocimiento genuino: los participantes deben correlacionar
acciones del controls con cambios en el bus para identificar los IDs
reales de ICSim entre varios IDs señuelo.

IDs REALES de ICSim (NO tocados por este script):
  0x244  — velocidad
  0x188  — señalización (intermitentes)
  0x19B  — puertas

IDs SEÑUELO inyectados por este script:
  0x300  — "RPM motor" falso      — varía de forma senoidal, ~20 Hz
  0x4AA  — "Temperatura motor"    — varía muy lento, ~0.5 Hz
  0x1F0  — "Presión neumáticos"   — 4 bytes, cambia raramente
  0x3C0  — "Batería 12V"          — casi estático, varía ±0.2V
  0x520  — "Sensor lluvia/luz"    — pulsos irregulares aleatorios
  0x6B0  — "Timestamp ECU"        — contador incremental

Clave pedagógica: los señuelos varían siguiendo su PROPIO ritmo interno,
NO en respuesta a las acciones del simulador (controls). La correlación
"muevo el acelerador → ¿qué ID cambia?" sigue siendo el método correcto
para distinguir reales de señuelos.

Uso (Game Master):
  python3 decoy_traffic.py
  python3 decoy_traffic.py --channel vcan0
  python3 decoy_traffic.py --verbose   # muestra cada frame enviado

Detener: Ctrl+C
"""

import argparse
import math
import random
import signal
import sys
import time

try:
    import can
except ImportError:
    print("[decoy] ERROR: python-can no está instalado.")
    print("        Instalar con: pip install python-can")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Configuración de señuelos
# ---------------------------------------------------------------------------

DECOY_IDS = {
    0x300: "RPM motor (falso)",
    0x4AA: "Temperatura motor (falso)",
    0x1F0: "Presión neumáticos (falso)",
    0x3C0: "Batería 12V (falso)",
    0x520: "Sensor lluvia/luz (falso)",
    0x6B0: "Timestamp ECU (falso)",
}

# IDs reales de ICSim — este script NO debe emitir frames con estos IDs
ICSIM_REAL_IDS = {0x244, 0x188, 0x19B}


# ---------------------------------------------------------------------------
# Estado global
# ---------------------------------------------------------------------------

running = True


def signal_handler(sig, frame):
    global running
    running = False
    print("\n[decoy] Señal recibida — deteniendo inyector...")


# ---------------------------------------------------------------------------
# Lógica de generación de señuelos
# ---------------------------------------------------------------------------

def build_decoy_frames(t: float, counter: int) -> list:
    """
    Devuelve una lista de (arb_id, data_bytes) para enviar en este tick.
    t       — tiempo transcurrido en segundos
    counter — tick actual (incrementa cada 50 ms)
    """
    frames = []

    # 0x300 — "RPM motor": oscilación senoidal lenta (período ~16s)
    # byte 0-1: RPM (0-8000 rpm → 0x0000-0x1F40), byte 2: marcha (1-6)
    rpm = int((math.sin(t * 0.4) + 1) * 4000)
    gear = min(6, max(1, int(t / 5) % 6 + 1))
    frames.append((0x300, [
        (rpm >> 8) & 0xFF,
        rpm & 0xFF,
        gear,
        0x00, 0x00, 0x00, 0x00, 0x00
    ]))

    # 0x4AA — "Temperatura motor": sube de 70°C a 95°C y baja lentamente
    # Solo emitir cada 2 s (counter % 40 con tick de 50ms)
    if counter % 40 == 0:
        temp = int(70 + (math.sin(t * 0.04) + 1) * 12)  # 70-94°C
        frames.append((0x4AA, [temp, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]))

    # 0x1F0 — "Presión neumáticos": 4 bytes (uno por rueda, en PSI)
    # Solo emitir cada 4 s (counter % 80)
    if counter % 80 == 0:
        pressures = [
            32 + random.randint(-1, 1),  # delantera izq
            32 + random.randint(-1, 1),  # delantera der
            31 + random.randint(-1, 1),  # trasera izq
            33 + random.randint(-1, 1),  # trasera der
        ]
        frames.append((0x1F0, pressures + [0x00, 0x00, 0x00, 0x00]))

    # 0x3C0 — "Batería 12V": casi estático (12.2-12.6V × 10 → 122-126)
    # Solo emitir cada 10 s (counter % 200)
    if counter % 200 == 0:
        volt = 124 + random.randint(-2, 2)
        frames.append((0x3C0, [0x00, volt & 0xFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]))

    # 0x520 — "Sensor lluvia/luz": pulsos aleatorios breves
    # ~3% de probabilidad por tick → aparece ~2-3 veces cada 5 s
    if random.random() < 0.03:
        rain_val = random.choice([0x00, 0x01, 0x03, 0x07])
        frames.append((0x520, [rain_val, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]))

    # 0x6B0 — "Timestamp ECU": contador incremental siempre activo (20 Hz)
    ts = counter & 0xFFFFFFFF
    frames.append((0x6B0, [
        (ts >> 24) & 0xFF,
        (ts >> 16) & 0xFF,
        (ts >> 8) & 0xFF,
        ts & 0xFF,
        0x00, 0x00, 0x00, 0x00
    ]))

    return frames


# ---------------------------------------------------------------------------
# Bucle principal
# ---------------------------------------------------------------------------

def run(channel: str, verbose: bool):
    global running

    try:
        bus = can.interface.Bus(channel=channel, bustype="socketcan")
    except Exception as e:
        print(f"[decoy] ERROR: No se puede conectar a {channel}: {e}")
        print(f"[decoy] ¿Está {channel} activo?")
        print(f"        sudo modprobe vcan")
        print(f"        sudo ip link add dev {channel} type vcan")
        print(f"        sudo ip link set up {channel}")
        sys.exit(1)

    print(f"[decoy] Inyector señuelo iniciado en {channel}")
    print(f"[decoy] IDs señuelo activos:")
    for arb_id, desc in DECOY_IDS.items():
        print(f"          0x{arb_id:03X}  — {desc}")
    print(f"[decoy] IDs reales ICSim (NO afectados): "
          f"{[hex(i) for i in sorted(ICSIM_REAL_IDS)]}")
    print(f"[decoy] Ctrl+C para detener\n")

    t_start = time.monotonic()
    counter = 0

    while running:
        t = time.monotonic() - t_start
        frames = build_decoy_frames(t, counter)

        for arb_id, data in frames:
            msg = can.Message(
                arbitration_id=arb_id,
                data=bytes(data),
                is_extended_id=False,
            )
            try:
                bus.send(msg)
                if verbose:
                    data_hex = " ".join(f"{b:02X}" for b in data)
                    print(f"[decoy] TX  0x{arb_id:03X}  [{data_hex}]")
            except can.CanError as e:
                print(f"[decoy] WARN: error al enviar 0x{arb_id:03X}: {e}")

        counter += 1
        time.sleep(0.05)  # tick cada 50 ms → frecuencia base 20 Hz

    bus.shutdown()
    print("[decoy] Bus cerrado. Inyector detenido.")


# ---------------------------------------------------------------------------
# Punto de entrada
# ---------------------------------------------------------------------------

def main():
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    parser = argparse.ArgumentParser(
        description="Inyector de tráfico señuelo CAN para CTF Automotive"
    )
    parser.add_argument(
        "--channel",
        default="vcan0",
        help="Interfaz CAN virtual (default: vcan0)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Imprimir cada frame enviado por stdout",
    )
    args = parser.parse_args()

    # Validación de seguridad: rechazar interfaces físicas
    if not args.channel.startswith("vcan"):
        print(f"[decoy] ERROR: '{args.channel}' no parece una interfaz virtual.")
        print("[decoy] Este script solo debe usarse con interfaces vcan* en entornos de laboratorio.")
        sys.exit(1)

    run(args.channel, args.verbose)


if __name__ == "__main__":
    main()
