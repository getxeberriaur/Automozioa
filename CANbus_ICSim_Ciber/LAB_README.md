# ICSim Docker bidez — Linux laborategia

Dokumentu honek Docker bidez ICSim abiarazteko urratsak azaltzen ditu. Erabili Linux makina batean edo Linux VM batean; Windows-eko Docker Desktop-ek ez du beharrezko `vcan` kernel-modulua eskaintzen.

## 1. `vcan0` prestatu

```bash
sudo modprobe vcan
sudo ip link add dev vcan0 type vcan
sudo ip link set up vcan0
```

## 2. Irudia eraiki

```bash
cd CANbus_ICSim_Ciber
docker build -t icsim-novnc:latest .
```

## 3. Edukiontzia abiarazi

```bash
docker run --rm -it --network host --cap-add NET_ADMIN --shm-size=1g --name icsim-lab icsim-novnc:latest
```

Edo Compose erabilita:

```bash
docker compose up --build
```

## 4. Egiaztatu

Ireki `http://localhost:6080/vnc_lite.html`. Beste terminal batean:

```bash
candump vcan0
cansend vcan0 244#00000000FF000000
```

## Arazoak konpontzea

- Web-interfazea ez bada agertzen, aztertu `docker logs icsim-lab`.
- ICSim falta bada, egiaztatu Docker irudia behar bezala eraiki dela.
- `vcan0` falta bada, egiaztatu kernelak `vcan` modulua duela eta interfazea ostalarian sortu dela.

Edukiontziak `--network host` eta `NET_ADMIN` behar ditu `vcan0`-ra sartzeko. Erabili laborategi-ingurune fidagarrian soilik.
