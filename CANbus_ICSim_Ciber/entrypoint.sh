#!/bin/bash
set -euo pipefail

# Simple entrypoint to run ICSim + controls and expose display via noVNC/x11vnc
export DISPLAY=:1

# Ensure X socket directory exists and is writable. Use sudo to allow
# creating the directory when running as non-root inside the container.
if [ ! -d /tmp/.X11-unix ]; then
  echo "/tmp/.X11-unix missing; attempting to create"
  mkdir -p /tmp/.X11-unix || true
fi

echo "Starting Xvfb on display $DISPLAY"
# Start Xvfb; container capabilities should allow socket creation
Xvfb $DISPLAY -screen 0 1024x768x24 &
XVFB_PID=$!

# Wait for X server to become available
echo "Waiting for X server to be ready..."
TRIES=0
until /usr/bin/xdpyinfo -display "$DISPLAY" >/dev/null 2>&1 || [ $TRIES -ge 50 ]; do
  sleep 0.1
  TRIES=$((TRIES+1))
done
if [ $TRIES -ge 50 ]; then
  echo "X server did not become ready in time (display $DISPLAY)"
fi

echo "Starting x11vnc"
# Use -auth guess to try to find the correct Xauthority file
x11vnc -display $DISPLAY -auth guess -nopw -forever -shared -bg || true

# Start noVNC websocket proxy (prefers websockify). If websockify is
# available, serve the /usr/share/novnc web files; otherwise fall back to
# running novnc_proxy if present.
if command -v websockify >/dev/null 2>&1; then
  echo "Starting websockify (noVNC) proxy on :6080"
  websockify --web /usr/share/novnc 6080 localhost:5901 &
elif [ -x /usr/share/novnc/utils/novnc_proxy ]; then
  echo "Starting novnc_proxy on :6080"
  /usr/share/novnc/utils/novnc_proxy --vnc localhost:5901 --listen 6080 &
elif [ -d /usr/share/novnc ]; then
  echo "noVNC directory present but neither websockify nor novnc_proxy available; skipping web UI"
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

sleep 1
ICSIM_DIR=/opt/ICSim
if [ ! -x "$ICSIM_DIR/builddir/icsim" ]; then
  echo "ICSim binary not found or not executable: $ICSIM_DIR/builddir/icsim"
  echo "Listing $ICSIM_DIR/builddir"
  ls -la "$ICSIM_DIR/builddir" || true
  exit 1
fi


echo "Preparing X authority and runtime dirs for labuser"
# Create an Xauthority entry and copy it to labuser so the user can connect
if command -v xauth >/dev/null 2>&1; then
  echo "Generating Xauthority for $DISPLAY"
  xauth generate $DISPLAY . trusted || true
  if [ -f /root/.Xauthority ]; then
    cp /root/.Xauthority /home/labuser/.Xauthority || true
    chown labuser:labuser /home/labuser/.Xauthority || true
  fi
fi

# Create XDG_RUNTIME_DIR for labuser
XDG_DIR=/run/user/1000
mkdir -p $XDG_DIR || true
chown labuser:labuser $XDG_DIR || true

echo "Starting ICSim (display $DISPLAY) as root (temporary to ensure X access)"
# Start ICSim and controls as root so they can access the X server and display
# (we can drop privileges later once Xauthority is handled).
export SDL_VIDEODRIVER=x11
cd $ICSIM_DIR
./builddir/icsim vcan0 > /tmp/icsim.log 2>&1 & echo $! > /tmp/icsim.pid
sleep 1
./builddir/controls vcan0 > /tmp/controls.log 2>&1 & echo $! > /tmp/controls.pid

# Wait for any child to exit
wait -n || true

echo "One of the processes exited, shutting down"
kill $XVFB_PID || true
