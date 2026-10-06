#!/usr/bin/env python3
"""
can_scanner.py — Escaneo pasivo del bus CAN.

Captura tráfico durante un tiempo determinado y genera un resumen estadístico
de los Arbitration IDs activos, frecuencia y bytes que cambian.

Uso:
    python can_scanner.py --interface vcan0 --duration 30
    python can_scanner.py --interface vcan0 --duration 60 --output logs/scan.txt

Dependencias: python-can (pip install python-can)
"""

import can
import argparse
import time
import sys
from collections import defaultdict


def scan(interface: str, duration: float, output_file: str | None) -> None:
    results: dict[int, dict] = defaultdict(
        lambda: {
            "count": 0,
            "dlc_min": 8,
            "dlc_max": 0,
            "first_seen": None,
            "last_data": None,
            "changing_bytes": set(),
        }
    )

    print(f"[*] Escaneando {interface} durante {duration:.0f} segundos...")
    print("    (Pulsa Ctrl+C para detener antes de tiempo)\n")

    try:
        bus = can.interface.Bus(channel=interface, bustype="socketcan")
    except Exception as e:
        print(f"[!] Error al abrir {interface}: {e}")
        sys.exit(1)

    start = time.monotonic()
    total_frames = 0

    try:
        while time.monotonic() - start < duration:
            msg = bus.recv(timeout=0.1)
            if msg is None:
                continue

            aid = msg.arbitration_id
            total_frames += 1
            entry = results[aid]
            entry["count"] += 1

            if entry["first_seen"] is None:
                entry["first_seen"] = msg.timestamp

            dlc = msg.dlc
            if dlc < entry["dlc_min"]:
                entry["dlc_min"] = dlc
            if dlc > entry["dlc_max"]:
                entry["dlc_max"] = dlc

            data = list(msg.data)
            if entry["last_data"] is not None:
                for i, (prev, curr) in enumerate(zip(entry["last_data"], data)):
                    if prev != curr:
                        entry["changing_bytes"].add(i)
            entry["last_data"] = data

    except KeyboardInterrupt:
        print("\n[!] Escaneo interrumpido por el usuario.")
    finally:
        bus.shutdown()

    elapsed = time.monotonic() - start

    lines = []
    lines.append(f"\n{'=' * 60}")
    lines.append(f"  CAN Bus Scan — {interface}")
    lines.append(f"{'=' * 60}")
    lines.append(f"  Duración : {elapsed:.1f} s")
    lines.append(f"  Tramas   : {total_frames}")
    lines.append(f"{'=' * 60}")
    lines.append(
        f"  {'ID (hex)':<10} {'Tramas':>8}  {'Freq(Hz)':>9}  "
        f"{'DLC':>4}  {'Bytes cambiantes'}"
    )
    lines.append(f"  {'-'*10} {'-'*8}  {'-'*9}  {'-'*4}  {'-'*20}")

    for aid in sorted(results):
        entry = results[aid]
        freq = entry["count"] / elapsed if elapsed > 0 else 0
        dlc_str = (
            str(entry["dlc_min"])
            if entry["dlc_min"] == entry["dlc_max"]
            else f"{entry['dlc_min']}-{entry['dlc_max']}"
        )
        changing = (
            str(sorted(entry["changing_bytes"])) if entry["changing_bytes"] else "ninguno"
        )
        lines.append(
            f"  0x{aid:03X}       {entry['count']:>8}  {freq:>9.1f}  "
            f"{dlc_str:>4}  {changing}"
        )

    lines.append(f"{'=' * 60}\n")

    output = "\n".join(lines)
    print(output)

    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"[+] Resultados guardados en: {output_file}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Escaneo pasivo de bus CAN — ICSim Lab"
    )
    parser.add_argument(
        "--interface", "-i", default="vcan0", help="Interfaz CAN (default: vcan0)"
    )
    parser.add_argument(
        "--duration",
        "-d",
        type=float,
        default=30.0,
        help="Duración del escaneo en segundos (default: 30)",
    )
    parser.add_argument(
        "--output",
        "-o",
        default=None,
        help="Archivo de salida (opcional)",
    )
    args = parser.parse_args()
    scan(args.interface, args.duration, args.output)


if __name__ == "__main__":
    main()
