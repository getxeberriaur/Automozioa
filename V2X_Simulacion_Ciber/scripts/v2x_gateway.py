from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import sys
import time
from collections import defaultdict, deque
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Lock
from typing import Any


HOST = "127.0.0.1"
PORT = 8090
SHARED_KEYS = {"car-017": b"lab-key-car-017", "car-021": b"lab-key-car-021"}
ALLOWED_TYPES = {"cam", "denm", "spatem"}


class V2XPolicy:
    def __init__(self, *, protected: bool, window_seconds: int = 30, burst_limit: int = 8) -> None:
        self.protected = protected
        self.window_seconds = window_seconds
        self.burst_limit = burst_limit
        self.seen: set[tuple[str, int]] = set()
        self.last_sequence: dict[str, int] = {}
        self.received: dict[str, deque[float]] = defaultdict(deque)
        self.lock = Lock()

    def evaluate(self, message: dict[str, Any]) -> tuple[bool, list[str]]:
        reasons: list[str] = []
        now = time.time()
        sender = message.get("sender_id")
        sequence = message.get("sequence")
        message_type = message.get("message_type")
        timestamp = message.get("timestamp")

        if message_type not in ALLOWED_TYPES:
            reasons.append("message_type_not_allowed")
        if not isinstance(sender, str) or not sender:
            reasons.append("sender_id_missing")
        if not isinstance(sequence, int) or sequence < 0:
            reasons.append("sequence_invalid")
        if not isinstance(timestamp, (int, float)) or abs(now - timestamp) > self.window_seconds:
            reasons.append("timestamp_outside_window")

        location = message.get("location", {})
        if not (-90 <= location.get("latitude", 999) <= 90):
            reasons.append("latitude_invalid")
        if not (-180 <= location.get("longitude", 999) <= 180):
            reasons.append("longitude_invalid")
        if not (0 <= message.get("speed_kmh", -1) <= 250):
            reasons.append("speed_implausible")
        if not (0 <= message.get("heading_deg", -1) < 360):
            reasons.append("heading_invalid")

        if self.protected:
            if sender not in SHARED_KEYS:
                reasons.append("sender_not_enrolled")
            else:
                expected = sign_message(message, SHARED_KEYS[sender])
                if not hmac.compare_digest(message.get("signature", ""), expected):
                    reasons.append("signature_invalid")

            if isinstance(sender, str) and isinstance(sequence, int):
                key = (sender, sequence)
                if key in self.seen or sequence <= self.last_sequence.get(sender, -1):
                    reasons.append("replay_or_old_sequence")

            if isinstance(sender, str):
                recent = self.received[sender]
                while recent and now - recent[0] > 1:
                    recent.popleft()
                if len(recent) >= self.burst_limit:
                    reasons.append("rate_limit_exceeded")

        accepted = not reasons
        with self.lock:
            if isinstance(sender, str):
                self.received[sender].append(now)
                if accepted and isinstance(sequence, int):
                    self.seen.add((sender, sequence))
                    self.last_sequence[sender] = sequence
        return accepted, reasons


def sign_message(message: dict[str, Any], key: bytes) -> str:
    unsigned = {name: value for name, value in message.items() if name != "signature"}
    encoded = json.dumps(unsigned, sort_keys=True, separators=(",", ":")).encode()
    return hmac.new(key, encoded, hashlib.sha256).hexdigest()


class GatewayHandler(BaseHTTPRequestHandler):
    policy: V2XPolicy

    def do_POST(self) -> None:  # noqa: N802 - required by BaseHTTPRequestHandler
        if self.path != "/v2x/messages":
            self.respond(404, {"status": "rejected", "reasons": ["path_not_found"]})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            message = json.loads(self.rfile.read(length))
        except (ValueError, json.JSONDecodeError):
            self.respond(400, {"status": "rejected", "reasons": ["invalid_json"]})
            return
        if not isinstance(message, dict):
            self.respond(400, {"status": "rejected", "reasons": ["message_not_object"]})
            return

        accepted, reasons = self.policy.evaluate(message)
        result = {"status": "accepted" if accepted else "rejected", "reasons": reasons}
        print(json.dumps({"message": message, "decision": result}, ensure_ascii=False), flush=True)
        self.respond(202 if accepted else 422, result)

    def respond(self, status: int, body: dict[str, Any]) -> None:
        encoded = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def log_message(self, format: str, *args: Any) -> None:
        return


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Gateway V2X local para laboratorio defensivo.")
    parser.add_argument("--host", default=HOST)
    parser.add_argument("--port", type=int, default=PORT)
    parser.add_argument("--insecure", action="store_true", help="Desactiva controles para observar ataques.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    GatewayHandler.policy = V2XPolicy(protected=not args.insecure)
    server = HTTPServer((args.host, args.port), GatewayHandler)
    mode = "inseguro" if args.insecure else "protegido"
    print(f"Gateway V2X escuchando en http://{args.host}:{args.port} ({mode})", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nGateway detenido.")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())