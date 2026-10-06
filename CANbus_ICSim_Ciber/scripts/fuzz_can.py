#!/usr/bin/env python3
"""
fuzz_can.py — Fuzzer de frames CAN para entornos de laboratorio.

Modos disponibles:
  - random   : IDs y datos completamente aleatorios.
  - targeted : datos aleatorios en un ID específico.
  - mutate   : muta byte a byte desde una trama base conocida.

Uso:
    python fuzz_can.py --interface vcan0 --mode random --duration 60
    python fuzz_can.py --interface vcan0 --mode targeted --target-id 0x244 --duration 30
    python fuzz_can.py --interface vcan0 --mode mutate --target-id 0x244 \
        --base-data 0000000000000000 --duration 30

Dependencias: python-can (pip install python-can)
"""

import can
import argparse
import time
import random
import sys
import os

# Rango de IDs válidos CAN 2.0A (11 bits)
_ID_MAX = 0x7FF


def _random_id() -> int:
    return random.randint(0, _ID_MAX)


def _random_data(dlc: int = 8) -> list[int]:
    return [random.randint(0, 255) for _ in range(dlc)]


def _mutate_data(base: list[int]) -> list[int]:
    """Muta un byte aleatorio del payload."""
    data = base.copy()
    byte_idx = random.randint(0, len(data) - 1)
    data[byte_idx] = random.randint(0, 255)
    return data


def fuzz(
    interface: str,
    mode: str,
    duration: float,
    rate: int,
    target_id: int | None,
    base_data: list[int] | None,
    log_file: str | None,
) -> None:
    try:
        bus = can.interface.Bus(channel=interface, bustype="socketcan")
    except Exception as e:
        print(f"[!] Error al abrir {interface}: {e}")
        sys.exit(1)

    log_fh = None
    if log_file:
        os.makedirs(os.path.dirname(log_file) if os.path.dirname(log_file) else ".", exist_ok=True)
        log_fh = open(log_file, "w", encoding="utf-8")
        log_fh.write("timestamp,arbitration_id,data\n")

    interval = 1.0 / rate
    start = time.monotonic()
    total_sent = 0

    print(f"[*] Fuzzing en {interface} | modo={mode} | {duration:.0f}s | {rate} tramas/s")
    print("    Pulsa Ctrl+C para detener.\n")

    try:
        while time.monotonic() - start < duration:
            iter_start = time.monotonic()

            # Construir la trama según el modo
            if mode == "random":
                aid = _random_id()
                data = _random_data(random.randint(0, 8))
            elif mode == "targeted":
                if target_id is None:
                    print("[!] --target-id requerido para modo 'targeted'")
                    sys.exit(1)
                aid = target_id
                data = _random_data(8)
            elif mode == "mutate":
                if target_id is None or base_data is None:
                    print("[!] --target-id y --base-data requeridos para modo 'mutate'")
                    sys.exit(1)
                aid = target_id
                data = _mutate_data(base_data)
            else:
                print(f"[!] Modo desconocido: {mode}")
                sys.exit(1)

            msg = can.Message(
                arbitration_id=aid,
                data=data,
                is_extended_id=False,
            )

            try:
                bus.send(msg)
                total_sent += 1
            except can.CanError:
                pass  # En vcan0 casi nunca falla, ignorar

            if log_fh:
                ts = time.time()
                hex_data = "".join(f"{b:02X}" for b in data)
                log_fh.write(f"{ts:.6f},0x{aid:03X},{hex_data}\n")

            if total_sent % 500 == 0:
                elapsed = time.monotonic() - start
                actual_rate = total_sent / elapsed if elapsed > 0 else 0
                print(f"  [{elapsed:5.1f}s] {total_sent:7d} tramas enviadas | {actual_rate:.0f} tps")

            # Control de tasa
            elapsed_iter = time.monotonic() - iter_start
            sleep_time = interval - elapsed_iter
            if sleep_time > 0:
                time.sleep(sleep_time)

    except KeyboardInterrupt:
        print("\n[!] Fuzzing interrumpido.")
    finally:
        bus.shutdown()
        if log_fh:
            log_fh.close()

    elapsed = time.monotonic() - start
    print(f"\n[+] Sesión terminada. Tramas enviadas: {total_sent} en {elapsed:.1f}s")
    if log_file:
        print(f"[+] Log guardado en: {log_file}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Fuzzer CAN — ICSim Lab")
    parser.add_argument("--interface", "-i", default="vcan0")
    parser.add_argument(
        "--mode",
        "-m",
        choices=["random", "targeted", "mutate"],
        default="random",
        help="Modo de fuzzing (default: random)",
    )
    parser.add_argument("--duration", "-d", type=float, default=30.0)
    parser.add_argument(
        "--rate", "-r", type=int, default=100, help="Tramas por segundo (default: 100)"
    )
    parser.add_argument(
        "--target-id",
        type=lambda x: int(x, 16),
        default=None,
        metavar="HEX_ID",
        help="Arbitration ID objetivo (hex, ej: 0x244)",
    )
    parser.add_argument(
        "--base-data",
        default=None,
        metavar="HEX_DATA",
        help="Datos base para modo mutate (16 hex chars, ej: 0000000000000000)",
    )
    parser.add_argument("--log", "-o", default=None, help="Archivo de log CSV (opcional)")

    args = parser.parse_args()

    base_data = None
    if args.base_data:
        raw = args.base_data.replace(" ", "")
        if len(raw) != 16:
            print("[!] --base-data debe tener exactamente 16 caracteres hex (8 bytes)")
            sys.exit(1)
        base_data = [int(raw[i : i + 2], 16) for i in range(0, 16, 2)]

    fuzz(
        interface=args.interface,
        mode=args.mode,
        duration=args.duration,
        rate=args.rate,
        target_id=args.target_id,
        base_data=base_data,
        log_file=args.log,
    )


if __name__ == "__main__":
    main()
