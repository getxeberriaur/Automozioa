from __future__ import annotations

import json
from collections import defaultdict, deque
from datetime import datetime, timedelta, timezone
UTC = timezone.utc
from html import escape
from pathlib import Path
from typing import Any

from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field, field_validator


APP_DIR = Path(__file__).resolve().parent
PROJECT_DIR = APP_DIR.parent
LOG_DIR = PROJECT_DIR / "logs"
LOG_FILE = LOG_DIR / "events.log"

ALLOWED_DEVICE_IDS = {"V16-001", "V16-002"}
ALLOWED_MESSAGE_TYPES = {"v16.alert.notification"}
ALLOWED_ALERT_TYPES = {"vehicle_stopped", "breakdown", "accident", "test"}
ALLOWED_ALERT_STATUS = {"activated", "update", "cleared"}
TIMESTAMP_WINDOW_SECONDS = 30
RATE_LIMIT_MAX_EVENTS = 5
RATE_LIMIT_WINDOW_SECONDS = 10
NONCE_RETENTION_SECONDS = 300

app = FastAPI(
    title="V16 Alert Reception Platform",
    version="0.2.0",
    description="Plataforma local de recepción de avisos V16 en entorno de laboratorio.",
)

LOG_DIR.mkdir(parents=True, exist_ok=True)

nonce_cache: dict[str, dict[str, datetime]] = defaultdict(dict)
rate_limit_cache: dict[str, deque[datetime]] = defaultdict(deque)


class DeviceInfo(BaseModel):
    model_config = ConfigDict(extra="forbid")

    device_id: str = Field(min_length=3, max_length=32)
    manufacturer: str = Field(min_length=2, max_length=64)
    model: str = Field(min_length=2, max_length=64)
    firmware_version: str = Field(min_length=1, max_length=32)
    vehicle_type: str = Field(default="turismo", min_length=2, max_length=32)


class AlertInfo(BaseModel):
    model_config = ConfigDict(extra="forbid")

    alert_id: str = Field(min_length=8, max_length=64)
    alert_type: str
    status: str
    severity: str = Field(default="medium", min_length=3, max_length=16)
    activated_at: datetime
    road_context: str = Field(default="road_shoulder", min_length=3, max_length=32)

    @field_validator("alert_type")
    @classmethod
    def validate_alert_type(cls, value: str) -> str:
        if value not in ALLOWED_ALERT_TYPES:
            raise ValueError(f"alert_type must be one of: {', '.join(sorted(ALLOWED_ALERT_TYPES))}")
        return value

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: str) -> str:
        if value not in ALLOWED_ALERT_STATUS:
            raise ValueError(f"status must be one of: {', '.join(sorted(ALLOWED_ALERT_STATUS))}")
        return value

    @field_validator("activated_at")
    @classmethod
    def ensure_activated_at_timezone(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            raise ValueError("activated_at must include timezone information")
        return value.astimezone(UTC)


class LocationInfo(BaseModel):
    model_config = ConfigDict(extra="forbid")

    latitude: float
    longitude: float
    heading_deg: float = Field(default=0, ge=0, le=360)
    accuracy_m: float = Field(default=5.0, gt=0, le=1000)

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


class SecurityInfo(BaseModel):
    model_config = ConfigDict(extra="forbid")

    nonce: str = Field(min_length=8, max_length=64)
    sent_at: datetime
    transport: str = Field(default="tls", min_length=3, max_length=16)

    @field_validator("sent_at")
    @classmethod
    def ensure_sent_at_timezone(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            raise ValueError("sent_at must include timezone information")
        return value.astimezone(UTC)


class V16AlertMessage(BaseModel):
    model_config = ConfigDict(extra="forbid")

    message_id: str = Field(min_length=8, max_length=64)
    protocol_version: str = Field(default="1.0")
    message_type: str = Field(default="v16.alert.notification")
    device: DeviceInfo
    alert: AlertInfo
    location: LocationInfo
    security: SecurityInfo

    @field_validator("message_type")
    @classmethod
    def validate_message_type(cls, value: str) -> str:
        if value not in ALLOWED_MESSAGE_TYPES:
            raise ValueError(f"message_type must be one of: {', '.join(sorted(ALLOWED_MESSAGE_TYPES))}")
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
    message: V16AlertMessage,
    decision: str,
    reason: str,
    source_ip: str,
    received_at: datetime,
) -> dict[str, Any]:
    return {
        "message_id": message.message_id,
        "protocol_version": message.protocol_version,
        "message_type": message.message_type,
        "device_id": message.device.device_id,
        "manufacturer": message.device.manufacturer,
        "model": message.device.model,
        "firmware_version": message.device.firmware_version,
        "alert_id": message.alert.alert_id,
        "alert_type": message.alert.alert_type,
        "alert_status": message.alert.status,
        "severity": message.alert.severity,
        "activated_at": message.alert.activated_at.isoformat(),
        "sent_at": message.security.sent_at.isoformat(),
        "nonce": message.security.nonce,
        "transport": message.security.transport,
        "decision": decision,
        "reason": reason,
        "source_ip": source_ip,
        "received_at": received_at.isoformat(),
        "latitude": message.location.latitude,
        "longitude": message.location.longitude,
        "heading_deg": message.location.heading_deg,
        "accuracy_m": message.location.accuracy_m,
    }


def append_log(record: dict[str, Any]) -> None:
    with LOG_FILE.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def read_recent_log_records(limit: int, decision: str | None = None) -> list[dict[str, Any]]:
    if not LOG_FILE.exists():
        return []

    records: list[dict[str, Any]] = []
    with LOG_FILE.open("r", encoding="utf-8") as handle:
        lines = handle.readlines()

    for raw in reversed(lines):
        raw = raw.strip()
        if not raw:
            continue

        try:
            record = json.loads(raw)
        except json.JSONDecodeError:
            continue

        if decision and record.get("decision") != decision:
            continue

        records.append(record)
        if len(records) >= limit:
            break

    return records


def translate_decision(decision: str) -> str:
    return {
        "accepted": "Onartua",
        "rejected": "Baztertua",
    }.get(decision, decision)


def translate_reason(reason: str) -> str:
    return {
        "accepted_for_processing": "Tratamendurako onartua",
        "unknown_device_id": "Gailu identifikatzaile ezezaguna",
        "message_out_of_time_window": "Mezua denbora-leihotik kanpo dago",
        "replayed_nonce": "Nonce bera berrerabili da",
        "rate_limit_exceeded": "Tasa-muga gainditua",
    }.get(reason, reason)


def translate_alert_status(status: str) -> str:
    return {
        "activated": "Aktibatua",
        "update": "Eguneratzea",
        "cleared": "Itxita",
    }.get(status, status)


def translate_alert_type(alert_type: str) -> str:
    return {
        "vehicle_stopped": "Ibilgailua geldituta",
        "breakdown": "Matxura",
        "accident": "Istripua",
        "test": "Proba",
    }.get(alert_type, alert_type)


def build_dashboard_html(records: list[dict[str, Any]]) -> str:
    accepted_count = sum(1 for record in records if record.get("decision") == "accepted")
    rejected_count = sum(1 for record in records if record.get("decision") == "rejected")
    latest_received_at = records[0].get("received_at") if records else "-"

    rows = []
    for record in records:
        decision = str(record.get("decision", "-"))
        badge_class = "badge accepted" if decision == "accepted" else "badge rejected"
        rows.append(
            """
            <tr>
                <td>{received_at}</td>
                <td>{device_id}</td>
                <td>{alert_type}</td>
                <td>{alert_status}</td>
                <td><span class=\"{badge_class}\">{decision}</span></td>
                <td>{reason}</td>
                <td>{location}</td>
                <td>{message_id}</td>
            </tr>
            """.format(
                received_at=escape(str(record.get("received_at", "-"))),
                device_id=escape(str(record.get("device_id", "-"))),
                alert_type=escape(translate_alert_type(str(record.get("alert_type", "-")))),
                alert_status=escape(translate_alert_status(str(record.get("alert_status", "-")))),
                badge_class=badge_class,
                decision=escape(translate_decision(decision)),
                reason=escape(translate_reason(str(record.get("reason", "-")))),
                location=escape(f"{record.get('latitude', '-')}, {record.get('longitude', '-') }"),
                message_id=escape(str(record.get("message_id", "-"))),
            )
        )

    table_body = "\n".join(rows) if rows else "<tr><td colspan=\"8\">Oraindik ez da abisurik jaso.</td></tr>"

    return f"""
    <!DOCTYPE html>
    <html lang=\"eu\">
    <head>
        <meta charset=\"utf-8\" />
        <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
        <meta http-equiv=\"refresh\" content=\"5\" />
        <title>V16 Aginte Panela</title>
        <style>
            :root {{
                color-scheme: dark;
                --bg: #081120;
                --panel: #101b2e;
                --panel-2: #15233b;
                --text: #e8f0ff;
                --muted: #9fb2cf;
                --accent: #49c2ff;
                --ok: #18c37e;
                --warn: #ffb84d;
                --bad: #ff5f7a;
                --line: #233552;
            }}
            * {{ box-sizing: border-box; }}
            body {{
                margin: 0;
                font-family: Segoe UI, Arial, sans-serif;
                background: radial-gradient(circle at top, #10213c 0%, var(--bg) 55%);
                color: var(--text);
            }}
            .wrap {{ max-width: 1400px; margin: 0 auto; padding: 24px; }}
            .hero {{
                display: flex; justify-content: space-between; align-items: center;
                gap: 16px; padding: 20px 24px; border: 1px solid var(--line);
                border-radius: 18px; background: linear-gradient(135deg, rgba(73,194,255,.16), rgba(16,27,46,.92));
                box-shadow: 0 12px 30px rgba(0,0,0,.25);
            }}
            .hero h1 {{ margin: 0 0 6px; font-size: 30px; }}
            .hero p, .hero small {{ margin: 0; color: var(--muted); }}
            .chips {{ display: flex; flex-wrap: wrap; gap: 10px; margin-top: 10px; }}
            .chip {{ padding: 8px 12px; border-radius: 999px; background: rgba(255,255,255,.06); border: 1px solid var(--line); color: var(--text); }}
            .grid {{ display: grid; grid-template-columns: repeat(4, minmax(0,1fr)); gap: 16px; margin-top: 18px; }}
            .card {{ background: var(--panel); border: 1px solid var(--line); border-radius: 16px; padding: 18px; }}
            .card .label {{ color: var(--muted); font-size: 13px; text-transform: uppercase; letter-spacing: .06em; }}
            .card .value {{ font-size: 30px; font-weight: 700; margin-top: 10px; }}
            .card.ok .value {{ color: var(--ok); }}
            .card.bad .value {{ color: var(--bad); }}
            .panel {{ margin-top: 18px; background: var(--panel); border: 1px solid var(--line); border-radius: 18px; overflow: hidden; }}
            .panel-head {{ display: flex; justify-content: space-between; align-items: center; gap: 12px; padding: 18px 20px; border-bottom: 1px solid var(--line); background: var(--panel-2); }}
            .panel-head h2 {{ margin: 0; font-size: 20px; }}
            .panel-head p {{ margin: 4px 0 0; color: var(--muted); }}
            .panel-head a {{ color: var(--accent); text-decoration: none; font-weight: 600; }}
            table {{ width: 100%; border-collapse: collapse; }}
            th, td {{ padding: 14px 16px; text-align: left; border-bottom: 1px solid rgba(35,53,82,.85); vertical-align: top; }}
            th {{ color: var(--muted); font-size: 12px; text-transform: uppercase; letter-spacing: .06em; background: rgba(255,255,255,.02); }}
            tr:hover td {{ background: rgba(255,255,255,.03); }}
            .badge {{ display: inline-flex; align-items: center; padding: 6px 10px; border-radius: 999px; font-weight: 700; font-size: 12px; }}
            .badge.accepted {{ color: #062b1d; background: var(--ok); }}
            .badge.rejected {{ color: #320815; background: var(--bad); }}
            .footer {{ margin-top: 12px; color: var(--muted); font-size: 13px; }}
            @media (max-width: 1100px) {{ .grid {{ grid-template-columns: repeat(2, minmax(0,1fr)); }} }}
            @media (max-width: 780px) {{
                .hero, .panel-head {{ flex-direction: column; align-items: flex-start; }}
                .grid {{ grid-template-columns: 1fr; }}
                .panel {{ overflow-x: auto; }}
                table {{ min-width: 980px; }}
            }}
        </style>
    </head>
    <body>
        <div class=\"wrap\">
            <section class=\"hero\">
                <div>
                    <h1>V16 Abisuen Aginte Panela</h1>
                    <p>Baliza konektatuen abisuen harrera, balidazioa eta egoeraren ikuspegi operatiboa.</p>
                    <div class=\"chips\">
                        <span class=\"chip\">Sistema egoera: martxan</span>
                        <span class=\"chip\">Azken eguneraketa: {escape(str(latest_received_at))}</span>
                        <span class=\"chip\">Freskatzea: 5 segundoro</span>
                    </div>
                </div>
                <div>
                    <small>Prestakuntza-ingurune isolatua · Plataforma lokala · Euskal interfazea</small>
                </div>
            </section>

            <section class=\"grid\">
                <article class=\"card\">
                    <div class=\"label\">Azken mezuak</div>
                    <div class=\"value\">{len(records)}</div>
                </article>
                <article class=\"card ok\">
                    <div class=\"label\">Onartutako abisuak</div>
                    <div class=\"value\">{accepted_count}</div>
                </article>
                <article class=\"card bad\">
                    <div class=\"label\">Baztertutako abisuak</div>
                    <div class=\"value\">{rejected_count}</div>
                </article>
                <article class=\"card\">
                    <div class=\"label\">Datu-iturria</div>
                    <div class=\"value\" style=\"font-size:18px\">/events/recent</div>
                </article>
            </section>

            <section class=\"panel\">
                <div class=\"panel-head\">
                    <div>
                        <h2>Azken abisu prozesatuak</h2>
                        <p>Baliza V16 emuladoreak bidalitako azken mezuen egoera operatiboa.</p>
                    </div>
                    <a href=\"/events/recent?limit=25\">JSON ikuspegia</a>
                </div>
                <table>
                    <thead>
                        <tr>
                            <th>Jasotze-ordua</th>
                            <th>Baliza</th>
                            <th>Abisu mota</th>
                            <th>Egoera</th>
                            <th>Erabakia</th>
                            <th>Arrazoia</th>
                            <th>Kokapena</th>
                            <th>Mezu IDa</th>
                        </tr>
                    </thead>
                    <tbody>
                        {table_body}
                    </tbody>
                </table>
            </section>

            <p class=\"footer\">Oharra: panel honek laborategiko logak bistaratzen ditu, irakaskuntza eta simulazio helburuetarako.</p>
        </div>
    </body>
    </html>
    """


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/events/recent")
def recent_events(
    limit: int = Query(default=20, ge=1, le=200),
    decision: str | None = Query(default=None, pattern="^(accepted|rejected)$"),
) -> dict[str, Any]:
    records = read_recent_log_records(limit=limit, decision=decision)
    return {
        "count": len(records),
        "limit": limit,
        "decision_filter": decision,
        "events": records,
    }


@app.get("/aginte-panela", response_class=HTMLResponse)
def command_dashboard(limit: int = Query(default=25, ge=1, le=100)) -> HTMLResponse:
    records = read_recent_log_records(limit=limit)
    return HTMLResponse(content=build_dashboard_html(records))


@app.post("/events")
def ingest_event(message: V16AlertMessage, request: Request) -> JSONResponse:
    now = utc_now()
    prune_nonce_cache(now)

    source_ip = request.client.host if request.client else "unknown"
    device_id = message.device.device_id

    decision = "accepted"
    reason = "accepted_for_processing"
    status_code = 202

    age_seconds = abs((now - message.security.sent_at).total_seconds())

    if device_id not in ALLOWED_DEVICE_IDS:
        decision = "rejected"
        reason = "unknown_device_id"
        status_code = 403
    elif age_seconds > TIMESTAMP_WINDOW_SECONDS:
        decision = "rejected"
        reason = "message_out_of_time_window"
        status_code = 400
    elif has_seen_nonce(device_id, message.security.nonce):
        decision = "rejected"
        reason = "replayed_nonce"
        status_code = 409
    elif is_rate_limited(device_id, now):
        decision = "rejected"
        reason = "rate_limit_exceeded"
        status_code = 429
    else:
        register_nonce(device_id, message.security.nonce, now)
        register_rate_event(device_id, now)

    record = build_log_record(
        message=message,
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
            "message_id": message.message_id,
            "device_id": device_id,
            "alert_id": message.alert.alert_id,
            "alert_status": message.alert.status,
            "alert_type": message.alert.alert_type,
        },
    )
