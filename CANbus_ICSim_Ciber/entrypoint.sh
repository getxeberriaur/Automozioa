#!/bin/bash
set -uo pipefail
# Note: -e removed intentionally so non-critical commands don't abort the script

# Simple entrypoint to run ICSim + controls and expose display via noVNC/x11vnc
export DISPLAY=:1

# Ensure X socket directory exists with correct permissions (sticky bit 1777
# is required by Xvfb to create its socket, same as on a real system).
echo "Setting up /tmp/.X11-unix"
mkdir -p /tmp/.X11-unix
chmod 1777 /tmp/.X11-unix

echo "Starting Xvfb on display $DISPLAY"
# Redirect Xvfb stderr to a log so we can diagnose failures
Xvfb $DISPLAY -screen 0 1024x768x24 -ac +extension GLX +render -noreset > /tmp/xvfb.log 2>&1 &
XVFB_PID=$!

# Wait for X server to become available (longer timeout)
echo "Waiting for X server to be ready..."
TRIES=0
MAX_TRIES=200
until ( [ -e "/tmp/.X11-unix/X${DISPLAY#:}" ] && /usr/bin/xdpyinfo -display "$DISPLAY" >/dev/null 2>&1 ) || [ $TRIES -ge $MAX_TRIES ]; do
  sleep 0.1
  TRIES=$((TRIES+1))
done

if [ $TRIES -ge $MAX_TRIES ]; then
  echo "X server did not become ready in time (display $DISPLAY) after ${MAX_TRIES} attempts"
else
  echo "X server ready (display $DISPLAY)"
fi

# Start openbox window manager so SDL windows get title bars and can be
# dragged/resized. Without a WM, windows overlap and cannot be moved.
echo "Starting openbox window manager"
DISPLAY=$DISPLAY openbox --sm-disable &
sleep 1

# Start tint2 taskbar so minimized windows are always recoverable
echo "Starting tint2 taskbar"
DISPLAY=$DISPLAY tint2 &
sleep 0.5

# Allow the local user to connect to the X server
if command -v xhost >/dev/null 2>&1; then
  echo "Authorizing local user labuser to access X server"
  xhost +SI:localuser:labuser || true
fi
# We'll start x11vnc after ICSim is running so that the VNC backend is
# available when websockify attempts to connect. This avoids "Connection
# refused" errors from websockify.

echo "Deferring x11vnc/websockify until ICSim is running"

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
  ls -la "$ICSIM_DIR/builddir" || true
  exit 1
fi

# Generate Xauthority for root (uses the already-running Xvfb on $DISPLAY)
# and copy it to labuser so ICSim/controls can connect to the X server.
echo "Generating Xauthority and setting up runtime dirs for labuser"
xauth generate $DISPLAY . trusted 2>/dev/null || true
XAUTH_FILE=/root/.Xauthority
if [ -f "$XAUTH_FILE" ]; then
  cp "$XAUTH_FILE" /home/labuser/.Xauthority
  chown labuser:labuser /home/labuser/.Xauthority
  chmod 600 /home/labuser/.Xauthority
  echo "Xauthority copied to labuser"
else
  echo "WARNING: /root/.Xauthority not found; X connections from labuser may fail"
fi

# Create XDG_RUNTIME_DIR for labuser (required by some SDL/PulseAudio paths)
XDG_DIR=/run/user/1000
mkdir -p $XDG_DIR
chown labuser:labuser $XDG_DIR
chmod 700 $XDG_DIR

# Allow labuser to access the X server (belt-and-suspenders alongside xauth)
xhost +SI:localuser:labuser 2>/dev/null || true

echo "Starting ICSim (dashboard) as labuser — top-left corner"
su - labuser -c "
  export DISPLAY=$DISPLAY
  export XAUTHORITY=/home/labuser/.Xauthority
  export XDG_RUNTIME_DIR=$XDG_DIR
  export SDL_VIDEODRIVER=x11
  export SDL_AUDIODRIVER=dummy
  export SDL_VIDEO_WINDOW_POS=0,0
  cd $ICSIM_DIR
  ./builddir/icsim vcan0 > /tmp/icsim.log 2>&1 &
  echo \$! > /tmp/icsim.pid
"
sleep 2

echo "Starting controls (joystick) as labuser — bottom-left corner"
su - labuser -c "
  export DISPLAY=$DISPLAY
  export XAUTHORITY=/home/labuser/.Xauthority
  export XDG_RUNTIME_DIR=$XDG_DIR
  export SDL_VIDEODRIVER=x11
  export SDL_AUDIODRIVER=dummy
  export SDL_VIDEO_WINDOW_POS=0,400
  cd $ICSIM_DIR
  ./builddir/controls vcan0 > /tmp/controls.log 2>&1 &
  echo \$! > /tmp/controls.pid
"

# Give ICSim/controls time to open windows on the X display
sleep 2

echo "Starting x11vnc"
x11vnc -display $DISPLAY -rfbport 5901 -noxdamage -nowf -nopw -forever -shared -bg -o /tmp/x11vnc.log 2>&1 || true
TRIES=0
MAX_X11VNC_TRIES=200
until ss -lntp 2>/dev/null | grep -q ":5901" || [ $TRIES -ge $MAX_X11VNC_TRIES ]; do
  sleep 0.2
  TRIES=$((TRIES+1))

done

if [ $TRIES -ge $MAX_X11VNC_TRIES ]; then
  echo "x11vnc did not open :5901 in time after ${MAX_X11VNC_TRIES} attempts"
else
  echo "x11vnc is listening on :5901"
fi
# Now start websockify/noVNC if available
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

# Wait for any child to exit
wait -n || true

echo "One of the processes exited, shutting down"
kill $XVFB_PID || true
