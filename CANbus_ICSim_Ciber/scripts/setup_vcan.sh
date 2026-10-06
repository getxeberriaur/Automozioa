#!/usr/bin/env bash
# setup_vcan.sh — Crea y levanta la interfaz CAN virtual vcan0
# Uso: sudo bash setup_vcan.sh

set -e

echo "[*] Cargando módulos del kernel CAN..."
modprobe can
modprobe vcan
modprobe can_raw

echo "[*] Creando interfaz vcan0..."
if ip link show vcan0 &>/dev/null; then
    echo "[!] vcan0 ya existe. Bajando y recreando..."
    ip link set down vcan0 2>/dev/null || true
    ip link delete vcan0 2>/dev/null || true
fi

ip link add dev vcan0 type vcan
ip link set up vcan0

echo "[+] Interfaz vcan0 levantada correctamente."
ip -details link show vcan0
