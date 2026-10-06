from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import time
import urllib.error
import urllib.request
from urllib.parse import urlparse
from typing import Any


KEYS = {"car-017": b"lab-key-car-017", "car-021": b"lab-key-car-021"}


def sign_message(message: dict[str, Any], key: bytes) -> str:
    unsigned = {name: value for name, value in message.items() if name != "signature"}
    encoded = json.dumps(unsigned, sort_keys=True, separators=(",", ":")).encode()
    return hmac.new(key, encoded, hashlib.sha256).hexdigest()


def build_message(sender_id: str, sequence: int, *, scenario: str) -> dict[str, Any]:
    message: dict[str, Any] = {
        "message_type": "cam",
        "sender_id": sender_id,
        "timestamp": time.time(),
        "sequence": sequence,
        "location": {"latitude": 43.2630, "longitude": -2.9350},
        "speed_kmh": 48,
        "heading_deg": 90,
        "event": "normal_traffic",
    }
    if scenario == "spoof":
        message["sender_id"] = "car-999"
        message["event"] = "emergency_braking"
    elif scenario == "impossible":
        message["speed_kmh"] = 420
        message["location"] = {"latitude": 143.2, "longitude": -2.9350}
    elif scenario == "emergency":
        message["message_type"] = "denm"
        message["event"] = "emergency_braking"
    elif scenario == "old":
        message["timestamp"] -= 120
    return message


def post(url: str, message: dict[str, Any]) -> None:
    parsed_url = urlparse(url)
    if not parsed_url.path or parsed_url.path == "/":
        url = url.rstrip("/") + "/v2x/messages"
    request = urllib.request.Request(
        url,
        data=json.dumps(message).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=3) as response:
            body = response.read().decode()
            print(f"HTTP {response.status}: {body}")
    except urllib.error.HTTPError as error:
        print(f"HTTP {error.code}: {error.read().decode()}")
    except urllib.error.URLError as error:
        raise SystemExit(f"No se pudo conectar con el gateway: {error.reason}") from error


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generador de mensajes V2X para laboratorio local.")
    parser.add_argument(
        "scenario",
        choices=["legitimo", "replay", "spoof", "impossible", "old", "emergency", "burst"],
    )
    parser.add_argument("--url", default="http://127.0.0.1:8090/v2x/messages")
    parser.add_argument("--sender-id", default="car-017")
    parser.add_argument("--count", type=int, default=12)
    parser.add_argument("--unsigned", action="store_true", help="No añade firma HMAC de laboratorio.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    message = build_message(args.sender_id, 1, scenario=args.scenario)
    if not args.unsigned and args.sender_id in KEYS:
        message["signature"] = sign_message(message, KEYS[args.sender_id])

    if args.scenario == "replay":
        post(args.url, message)
        post(args.url, message)
    elif args.scenario == "burst":
        for sequence in range(1, args.count + 1):
            burst_message = build_message(args.sender_id, sequence, scenario="legitimo")
            if not args.unsigned and args.sender_id in KEYS:
                burst_message["signature"] = sign_message(burst_message, KEYS[args.sender_id])
            post(args.url, burst_message)
    else:
        post(args.url, message)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())