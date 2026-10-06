# CAN bus laborategia — abiarazte azkarra

ICSim-ek Linux kernel-eko `vcan` modulua behar du. Windows erabiltzen baduzu, prestatu Linux VM bat [konfigurazio-gidari](lab/03_Setup_entorno_linux_eu.md) jarraituz. Ez erabili Docker Desktop Windowsen.

## 1. `vcan0` abiarazi

```bash
sudo bash scripts/setup_vcan.sh
ip link show vcan0
```

## 2. ICSim abiarazi

Docker bidez, Linux ostalarian:

```bash
docker build -t icsim:local .
docker run --name icsim_run --network host --cap-add NET_ADMIN -d icsim:local
```

Interfazea `http://localhost:6080/vnc_lite.html` helbidean dago. Instalazio natiboa erabiltzen baduzu, jarraitu Linux konfigurazio-gidari.

## 3. Trafikoa egiaztatu

```bash
candump vcan0
```

Trafikoa agertzen denean, ingurunea prest dago. Jarraitu [A praktikari](lab/04_Practica_A_Reconocimiento_eu.md), eta gero egin B, C eta D praktikak.

## Segurtasun-muga

Komando guztiak `vcan0` interfaze birtualean soilik exekutatu. Ez konektatu bus fisiko batera edo ibilgailu batera.
