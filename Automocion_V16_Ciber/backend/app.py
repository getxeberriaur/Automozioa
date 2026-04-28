from __future__ import annotations

import json
from collections import defaultdict, deque
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field, field_validator


APP_DIR = Path(__file__).resolve().parent
PROJECT_DIR = APP_DIR.parent
LOG_DIR = PROJECT_DIR / "logs"
LOG_FILE = LOG_DIR / "events.log"

ALLOWED_DEVICE_IDS = {"V16-001", "V16-002"}
ALLOWED_EVENT_TYPES = {"hazard", "breakdown", "test"}
TIMESTAMP_WINDOW_SECONDS = 30
RATE_LIMIT_MAX_EVENTS = 5
RATE_LIMIT_WINDOW_SECONDS = 10
NONCE_RETENTION_SECONDS = 300

app = FastAPI(
    title="V16 Event Ingestion Lab",
    version="0.1.0",
    description="Backend local para validar eventos V16 en un laboratorio simulado.",
)

LOG_DIR.mkdir(parents=True, exist_ok=True)

nonce_cache: dict[str, dict[str, datetime]] = defaultdict(dict)
rate_limit_cache: dict[str, deque[datetime]] = defaultdict(deque)


class EventIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    event_id: str = Field(min_length=8, max_length=64)
    device_id: str = Field(min_length=3, max_length=32)
    timestamp: datetime
    nonce: str = Field(min_length=8, max_length=64)
    latitude: float
    longitude: float
    event_type: str = Field(default="hazard")
    payload_version: str = Field(default="1.0")

    @field_validator("timestamp")
    @classmethod
    def ensure_timezone(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            raise ValueError("timestamp must include timezone information")
        return value.astimezone(UTC)

    @field_validator("latitude")
    @classmethod
    def validate_latitude(cls, value: float) -> float:
        if not -90 <= value <= 90:
            raise ValueError("latitude out of valid range")
        return value

    @field_validator("longitude")
    @classmethod
    def validate_longitude(cls, value: float) -> float:
        if not -180 <= value <= 180:
            raise ValueError("longitude out of valid range")
        return value

    @field_validator("event_type")
    @classmethod
    def validate_event_type(cls, value: str) -> str:
        if value not in ALLOWED_EVENT_TYPES:
            raise ValueError(f"event_type must be one of: {', '.join(sorted(ALLOWED_EVENT_TYPES))}")
        return value


def utc_now() -> datetime:
    return datetime.now(UTC)


def prune_nonce_cache(now: datetime) -> None:
    cutoff = now - timedelta(seconds=NONCE_RETENTION_SECONDS)
    for device_id, device_nonces in list(nonce_cache.items()):
        expired = [nonce for nonce, first_seen in device_nonces.items() if first_seen < cutoff]
        for nonce in expired:
            del device_nonces[nonce]
        if not device_nonces:
            del nonce_cache[device_id]


def is_rate_limited(device_id: str, now: datetime) -> bool:
    cutoff = now - timedelta(seconds=RATE_LIMIT_WINDOW_SECONDS)
    bucket = rate_limit_cache[device_id]
    while bucket and bucket[0] < cutoff:
        bucket.popleft()
    return len(bucket) >= RATE_LIMIT_MAX_EVENTS


def register_rate_event(device_id: str, now: datetime) -> None:
    rate_limit_cache[device_id].append(now)


def register_nonce(device_id: str, nonce: str, now: datetime) -> None:
    nonce_cache[device_id][nonce] = now


def has_seen_nonce(device_id: str, nonce: str) -> bool:
    return nonce in nonce_cache.get(device_id, {})


def build_log_record(
    *,
    event: EventIn,
    decision: str,
    reason: str,
    source_ip: str,
    received_at: datetime,
) -> dict[str, Any]:
    return {
        "event_id": event.event_id,
        "device_id": event.device_id,
        "timestamp": event.timestamp.isoformat(),
        "decision": decision,
        "reason": reason,
        "source_ip": source_ip,
        "received_at": received_at.isoformat(),
        "latitude": event.latitude,
        "longitude": event.longitude,
        "event_type": event.event_type,
    }


def append_log(record: dict[str, Any]) -> None:
    with LOG_FILE.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/events")
def ingest_event(event: EventIn, request: Request) -> JSONResponse:
    now = utc_now()
    prune_nonce_cache(now)

    source_ip = request.client.host if request.client else "unknown"

    decision = "accepted"
    reason = "accepted"
    status_code = 202

    age_seconds = abs((now - event.timestamp).total_seconds())

    if event.device_id not in ALLOWED_DEVICE_IDS:
        decision = "rejected"
        reason = "unknown_device_id"
        status_code = 403
    elif age_seconds > TIMESTAMP_WINDOW_SECONDS:
        decision = "rejected"
        reason = "timestamp_out_of_window"
        status_code = 400
    elif has_seen_nonce(event.device_id, event.nonce):
        decision = "rejected"
        reason = "replayed_nonce"
        status_code = 409
    elif is_rate_limited(event.device_id, now):
        decision = "rejected"
        reason = "rate_limit_exceeded"
        status_code = 429
    else:
        register_nonce(event.device_id, event.nonce, now)
        register_rate_event(event.device_id, now)

    record = build_log_record(
        event=event,
        decision=decision,
        reason=reason,
        source_ip=source_ip,
        received_at=now,
    )
    append_log(record)

    return JSONResponse(
        status_code=status_code,
        content={
            "decision": decision,
            "reason": reason,
            "received_at": now.isoformat(),
            "event_id": event.event_id,
            "device_id": event.device_id,
        },
    )
