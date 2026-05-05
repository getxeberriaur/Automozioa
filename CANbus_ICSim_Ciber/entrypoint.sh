#!/bin/bash
set -euo pipefail

# Simple entrypoint to run ICSim + controls and expose display via noVNC/x11vnc
export DISPLAY=:1

echo "Starting Xvfb on display $DISPLAY"
Xvfb $DISPLAY -screen 0 1024x768x24 &
XVFB_PID=$!

echo "Starting x11vnc"
x11vnc -display $DISPLAY -nopw -forever -shared -bg

# Start noVNC websocket proxy (uses websockify)
if [ -d /usr/share/novnc ]; then
  echo "Starting noVNC proxy on :6080"
  /usr/share/novnc/utils/novnc_proxy --vnc localhost:5901 --listen 6080 &
else
  echo "noVNC not found at /usr/share/novnc, skipping web UI"
fi

# Create vcan0 if not present and if we have privileges
if ! ip link show vcan0 >/dev/null 2>&1; then
  echo "vcan0 not found. Attempting to create inside container (requires CAP_NET_ADMIN)."
  sudo bash -c 'modprobe vcan || true'
  sudo ip link add dev vcan0 type vcan || true
  sudo ip link set up vcan0 || true
fi

ICSIM_DIR=/opt/ICSim
if [ ! -x "$ICSIM_DIR/builddir/icsim" ]; then
  echo "ICSim binary not found or not executable: $ICSIM_DIR/builddir/icsim"
  echo "Listing $ICSIM_DIR/builddir"
  ls -la "$ICSIM_DIR/builddir" || true
  exit 1
fi

echo "Starting ICSim (display $DISPLAY)"
cd $ICSIM_DIR
./builddir/icsim vcan0 &
sleep 1
./builddir/controls vcan0 &

wait -n

echo "One of the processes exited, shutting down"
kill $XVFB_PID || true
