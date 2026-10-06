#!/bin/bash
# =============================================================================
# setup_ova_vm.sh — Preparación automática de VM para exportar como OVA
# =============================================================================
# Ejecutar dentro de Ubuntu 22.04 LTS limpio (VirtualBox o VMware):
#
#   chmod +x setup_ova_vm.sh
#   sudo bash setup_ova_vm.sh
#
# Al finalizar, apagar la VM y exportarla desde VirtualBox:
#   Archivo → Exportar servicio virtualizado → formato OVA 2.0
# =============================================================================
set -euo pipefail

ICSIM_DIR="/opt/ICSim"
LAB_USER="${SUDO_USER:-canlab}"
LOG_FILE="/tmp/setup_ova.log"

# Colores
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
ok()   { echo -e "${GREEN}[OK]${NC} $*"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $*"; }
fail() { echo -e "${RED}[FAIL]${NC} $*"; exit 1; }
step() { echo -e "\n${YELLOW}==>${NC} $*"; }

exec > >(tee -a "$LOG_FILE") 2>&1
echo "=== setup_ova_vm.sh — $(date) ==="

# ---------------------------------------------------------------------------
# 0. Comprobaciones previas
# ---------------------------------------------------------------------------
step "Comprobando entorno"
[[ $EUID -eq 0 ]] || fail "Ejecutar con sudo"
grep -qE "Ubuntu 22" /etc/os-release 2>/dev/null || \
  grep -qE "Ubuntu 24" /etc/os-release 2>/dev/null || \
  warn "Distro no probada. Se recomienda Ubuntu 22.04 LTS."
ok "Entorno OK"

# ---------------------------------------------------------------------------
# 1. Actualizar sistema
# ---------------------------------------------------------------------------
step "Actualizando paquetes"
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get upgrade -y -qq
ok "Sistema actualizado"

# ---------------------------------------------------------------------------
# 2. Instalar dependencias
# ---------------------------------------------------------------------------
step "Instalando dependencias del laboratorio"
apt-get install -y -qq \
    can-utils \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-ttf-dev \
    meson ninja-build pkg-config \
    python3 python3-pip python3-venv \
    git build-essential \
    docker.io \
    curl wget net-tools \
    wireshark-common tshark \
    xvfb x11-xserver-utils
ok "Dependencias instaladas"

# ---------------------------------------------------------------------------
# 3. Módulos CAN kernel
# ---------------------------------------------------------------------------
step "Configurando módulos CAN"
modprobe can      || warn "modprobe can falló (puede ser built-in)"
modprobe vcan     || fail "modprobe vcan falló — este kernel no tiene soporte vcan"
modprobe can_raw  || warn "modprobe can_raw falló (puede ser built-in)"

# Hacer persistentes los módulos
cat > /etc/modules-load.d/can.conf << 'EOF'
can
vcan
can_raw
EOF
ok "Módulos CAN configurados (persistentes en arranque)"

# ---------------------------------------------------------------------------
# 4. Crear interfaz vcan0 y hacer persistente con systemd
# ---------------------------------------------------------------------------
step "Creando interfaz vcan0"
ip link add dev vcan0 type vcan 2>/dev/null || true
ip link set up vcan0

cat > /etc/systemd/system/vcan0.service << 'EOF'
[Unit]
Description=Virtual CAN interface vcan0
After=network.target

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=/bin/bash -c "modprobe vcan; ip link add dev vcan0 type vcan 2>/dev/null || true; ip link set up vcan0"
ExecStop=/bin/bash -c "ip link set down vcan0; ip link delete vcan0 2>/dev/null || true"

[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload
systemctl enable vcan0.service
ok "vcan0 configurado y habilitado en arranque"

# ---------------------------------------------------------------------------
# 5. Compilar ICSim
# ---------------------------------------------------------------------------
step "Compilando ICSim"
if [[ ! -d "$ICSIM_DIR" ]]; then
    git clone https://github.com/zombieCraig/ICSim.git "$ICSIM_DIR"
fi

cd "$ICSIM_DIR"
git pull --ff-only 2>/dev/null || true
meson setup builddir --wipe 2>/dev/null || meson setup builddir
ninja -C builddir

[[ -x "$ICSIM_DIR/builddir/icsim" ]]     || fail "icsim no compilado"
[[ -x "$ICSIM_DIR/builddir/controls" ]]  || fail "controls no compilado"
ok "ICSim compilado en $ICSIM_DIR/builddir/"

# ---------------------------------------------------------------------------
# 6. Instalar Docker y dar permisos al usuario de lab
# ---------------------------------------------------------------------------
step "Configurando Docker"
systemctl enable docker
systemctl start docker

if id "$LAB_USER" &>/dev/null; then
    usermod -aG docker "$LAB_USER"
    ok "Usuario $LAB_USER añadido al grupo docker"
else
    warn "Usuario $LAB_USER no existe. Añádelo manualmente: usermod -aG docker <usuario>"
fi

# ---------------------------------------------------------------------------
# 7. Pre-descargar imagen Docker de ICSim (opcional pero acelera el lab)
# ---------------------------------------------------------------------------
step "Pre-construyendo imagen Docker icsim:local"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ROOT="$(dirname "$SCRIPT_DIR")"

if [[ -f "$LAB_ROOT/Dockerfile" ]]; then
    docker build -t icsim:local "$LAB_ROOT" && ok "Imagen icsim:local construida" \
      || warn "Build Docker falló — los participantes pueden construirla en el lab"
else
    warn "Dockerfile no encontrado en $LAB_ROOT. Skipping Docker build."
fi

# ---------------------------------------------------------------------------
# 8. Crear script de inicio rápido en el escritorio del usuario
# ---------------------------------------------------------------------------
step "Creando acceso directo en escritorio"
if id "$LAB_USER" &>/dev/null; then
    DESKTOP_DIR="/home/$LAB_USER/Escritorio"
    [[ -d "$DESKTOP_DIR" ]] || DESKTOP_DIR="/home/$LAB_USER/Desktop"
    mkdir -p "$DESKTOP_DIR"

    cat > "$DESKTOP_DIR/Iniciar_ICSim_Lab.sh" << SCRIPT
#!/bin/bash
# Arranque rápido del laboratorio ICSim
set -e

# Asegurar vcan0
sudo modprobe vcan 2>/dev/null || true
sudo ip link add dev vcan0 type vcan 2>/dev/null || true
sudo ip link set up vcan0

# Lanzar con Docker (método recomendado)
docker rm -f icsim_run 2>/dev/null || true
docker run --name icsim_run \\
    -p 5901:5901 -p 6080:6080 \\
    --cap-add NET_ADMIN \\
    -d icsim:local

echo "Contenedor arrancado. Abre: http://localhost:6080/vnc_lite.html"
xdg-open http://localhost:6080/vnc_lite.html 2>/dev/null || true
SCRIPT
    chmod +x "$DESKTOP_DIR/Iniciar_ICSim_Lab.sh"
    chown "$LAB_USER:$LAB_USER" "$DESKTOP_DIR/Iniciar_ICSim_Lab.sh"
    ok "Script de inicio creado en $DESKTOP_DIR"
fi

# ---------------------------------------------------------------------------
# 9. Test de integración final
# ---------------------------------------------------------------------------
step "Test de integración"
ip link show vcan0 | grep -q UP && ok "vcan0 UP" || fail "vcan0 no está UP"
command -v candump &>/dev/null && ok "candump disponible" || fail "candump no encontrado"
"$ICSIM_DIR/builddir/icsim" --help &>/dev/null 2>&1 || \
  [[ -x "$ICSIM_DIR/builddir/icsim" ]] && ok "ICSim ejecutable" || fail "ICSim no ejecutable"

# ---------------------------------------------------------------------------
echo ""
echo "================================================================"
echo "  SETUP COMPLETADO — La VM está lista para exportar como OVA"
echo "================================================================"
echo ""
echo "Pasos siguientes:"
echo "  1. Apagar la VM:  sudo shutdown now"
echo "  2. En VirtualBox: Archivo → Exportar servicio virtualizado"
echo "     Formato: OVA 2.0 | Nombre: CANbus_ICSim_Lab.ova"
echo "  3. Distribuir la OVA a los participantes (importar con doble clic)"
echo ""
echo "Log completo en: $LOG_FILE"
