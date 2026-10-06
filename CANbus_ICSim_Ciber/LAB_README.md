ICSim Docker deployment (noVNC)
===============================

This folder contains a `Dockerfile`, `entrypoint.sh` and `docker-compose.yml` to build an ICSim image
that exposes a web UI via noVNC and uses `vcan0` for the virtual CAN bus.

Quick start (host preparation)
------------------------------
1. Create `vcan0` on the host (recommended):

```bash
sudo modprobe vcan
sudo ip link add dev vcan0 type vcan
sudo ip link set up vcan0
```

2. Build the image:

```bash
cd CANbus_ICSim_Ciber
docker build -t icsim-novnc:latest .
```

3. Run with host networking (UI at http://HOST:6080):

```bash
docker run --rm -it --network host --cap-add NET_ADMIN --shm-size=1g --name icsim-lab icsim-novnc:latest
```

Or use docker-compose:

```bash
cd CANbus_ICSim_Ciber
docker-compose up --build
```

Validation
----------
- Open http://<HOST_IP>:6080 in a browser to see the ICSim UI (noVNC).
- In another terminal run:

```bash
candump vcan0
cansend vcan0 244#00000000FF000000  # increase speed
```

Troubleshooting
---------------
- If the web UI does not appear, check container logs: `docker logs icsim-lab`.
- If ICSim binary is missing, ensure build completed successfully during image build (meson/ninja steps).
- For headless environments, ensure `xvfb`, `x11vnc` and `noVNC` are present in the image.

Security note
-------------
This container requires `--network host` and `NET_ADMIN` for simple access to `vcan0`. Use only in trusted lab environments.
