FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /opt

# Install build dependencies, runtime deps, can-utils and novnc/websockify
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    build-essential git meson ninja-build pkg-config python3 python3-pip \
    libsdl2-dev libsdl2-image-dev libsdl2-ttf-dev \
    xvfb x11vnc websockify novnc can-utils iproute2 sudo iputils-ping \
    ca-certificates wget net-tools procps \
 && rm -rf /var/lib/apt/lists/*

# Clone and build ICSim
RUN git clone https://github.com/zombieCraig/ICSim.git ICSim \
 && cd ICSim \
 && meson setup builddir || meson setup builddir . \
 && ninja -C builddir

# Create non-root user
RUN useradd -m -s /bin/bash labuser && chown -R labuser:labuser /opt/ICSim

# Add entrypoint and lab helper
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

EXPOSE 5901 6080

USER labuser
WORKDIR /home/labuser

CMD ["/usr/local/bin/entrypoint.sh"]
