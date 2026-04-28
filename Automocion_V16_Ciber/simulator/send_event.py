from __future__ import annotations

import argparse
import json
import sys
import time
import uuid
from datetime import UTC, datetime, timedelta
from typing import Any

import requests


DEFAULT_URL = "http://127.0.0.1:8080/events"
VALID_DEVICE_ID = "V16-001"
INVALID_DEVICE_ID = "V16-999"


def utc_now_iso() -> str:
    return datetime.now(UTC).isoformat()


def build_payload(
    *,
    device_id: str,
    timestamp: str | None = None,
    nonce: str | None = None,
    latitude: float = 43.2630,
    longitude: float = -2.9350,
    event_type: str = "hazard",
) -> dict[str, Any]:
    return {
        "event_id": f"evt-{uuid.uuid4().hex[:12]}",
        "device_id": device_id,
        "timestamp": timestamp or utc_now_iso(),
        "nonce": nonce or f"nonce-{uuid.uuid4().hex[:12]}",
        "latitude": latitude,
        "longitude": longitude,
        "event_type": event_type,
        "payload_version": "1.0",
    }


def post_event(url: str, payload: dict[str, Any], timeout: int = 5) -> tuple[int, Any]:
    response = requests.post(url, json=payload, timeout=timeout)
    try:
        body = response.json()
    except ValueError:
        body = response.text
    return response.status_code, body


def print_result(label: str, status_code: int, body: Any) -> None:
    print(f"[{label}] status={status_code}")
    if isinstance(body, dict):
        print(json.dumps(body, indent=2, ensure_ascii=False))
    else:
        print(body)
    print()


def run_legitimo(url: str, device_id: str) -> int:
    payload = build_payload(device_id=device_id)
    status_code, body = post_event(url, payload)
    print_result("legitimo", status_code, body)
    return 0 if status_code < 400 else 1


def run_replay(url: str, device_id: str) -> int:
    payload = build_payload(device_id=device_id)
    first_status, first_body = post_event(url, payload)
    second_status, second_body = post_event(url, payload)
    print_result("replay-1", first_status, first_body)
    print_result("replay-2", second_status, second_body)
    return 0 if first_status < 400 and second_status >= 400 else 1


def run_timestamp_atrasado(url: str, device_id: str) -> int:
    old_timestamp = (datetime.now(UTC) - timedelta(seconds=120)).isoformat()
    payload = build_payload(device_id=device_id, timestamp=old_timestamp)
    status_code, body = post_event(url, payload)
    print_result("timestamp-atrasado", status_code, body)
    return 0 if status_code >= 400 else 1


def run_coordenadas_invalidas(url: str, device_id: str) -> int:
    payload = build_payload(device_id=device_id, latitude=123.456, longitude=-2.9350)
    status_code, body = post_event(url, payload)
    print_result("coordenadas-invalidas", status_code, body)
    return 0 if status_code >= 400 else 1


def run_identidad_invalida(url: str) -> int:
    payload = build_payload(device_id=INVALID_DEVICE_ID)
    status_code, body = post_event(url, payload)
    print_result("identidad-invalida", status_code, body)
    return 0 if status_code >= 400 else 1


def run_rafaga(url: str, device_id: str, count: int) -> int:
    exit_code = 0
    for index in range(1, count + 1):
        payload = build_payload(device_id=device_id)
        status_code, body = post_event(url, payload)
        print_result(f"rafaga-{index}", status_code, body)
        if index > 5 and status_code < 400:
            exit_code = 1
        time.sleep(0.15)
    return exit_code


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Simulador de eventos V16 para laboratorio local.")
    parser.add_argument(
        "scenario",
        choices=[
            "legitimo",
            "replay",
            "timestamp-atrasado",
            "coordenadas-invalidas",
            "identidad-invalida",
            "rafaga",
        ],
        help="Caso de prueba a ejecutar.",
    )
    parser.add_argument("--url", default=DEFAULT_URL, help="URL del endpoint /events")
    parser.add_argument("--device-id", default=VALID_DEVICE_ID, help="Identidad de baliza válida")
    parser.add_argument("--count", type=int, default=8, help="Número de eventos para el escenario de ráfaga")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.scenario == "legitimo":
            return run_legitimo(args.url, args.device_id)
        if args.scenario == "replay":
            return run_replay(args.url, args.device_id)
        if args.scenario == "timestamp-atrasado":
            return run_timestamp_atrasado(args.url, args.device_id)
        if args.scenario == "coordenadas-invalidas":
            return run_coordenadas_invalidas(args.url, args.device_id)
        if args.scenario == "identidad-invalida":
            return run_identidad_invalida(args.url)
        if args.scenario == "rafaga":
            return run_rafaga(args.url, args.device_id, args.count)
    except requests.RequestException as exc:
        print(f"Error al conectar con el backend: {exc}", file=sys.stderr)
        return 2

    parser.error("Escenario no soportado")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
