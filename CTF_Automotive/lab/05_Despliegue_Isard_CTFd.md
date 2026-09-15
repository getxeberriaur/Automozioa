# Despliegue en Isard — CTF Automotive y CTFd

Esta guía describe el despliegue recomendado para una prueba de aula con **Isard VDI**, una VM del Game Master, VMs independientes para los equipos y una VM separada para CTFd.

## 1. Arquitectura

```text
VM CTFd
└── CTFd + base de datos + Redis
    └── HTTP accesible por las VMs del aula

VM Game Master
├── ICSim + controls
├── vcan0 propio
├── decoy_traffic.py
└── respuestas_master.md

VM participante N
├── ICSim + controls
├── vcan0 propio
└── herramientas CAN y scripts del CTF
```

CTFd administra equipos, retos, flags y puntuaciones. No se conecta a `vcan0`. Cada VM participante tiene un bus virtual independiente; el tráfico del GM no aparece automáticamente en el bus de los equipos.

## 2. Plantillas de Isard

1. Preparar una VM Linux base con el repositorio y las dependencias del laboratorio.
2. Verificar ICSim, `vcan0`, `can-utils`, `python-can` y el acceso noVNC.
3. Apagar la VM y crear una plantilla o snapshot.
4. Clonar la plantilla para el GM y para cada equipo.
5. Asignar nombres distintos: `automotive-gm`, `automotive-team-01`, etc.
6. Mantener `vcan0` local en cada clon; no interconectar los buses CAN por la red de Isard.

La VM del GM puede partir de la misma plantilla, pero debe conservar los materiales confidenciales de `lab/04_Respuestas_master.md` y ejecutar el tráfico señuelo en su propio entorno.

## 3. Preparar cada VM participante

```bash
ip link show vcan0
python3 -c "import can; print(can.__version__)"
```

Si la interfaz no existe:

```bash
sudo modprobe can vcan can_raw
sudo ip link add dev vcan0 type vcan
sudo ip link set up vcan0
```

Arrancar ICSim según la configuración elegida:

```bash
cd CANbus_ICSim_Ciber
docker compose up -d --build
docker logs -f icsim-lab
```

La interfaz noVNC estará disponible en `http://IP_DE_LA_VM:6080/vnc_lite.html` cuando el contenedor se ejecute con red de host.

En la VM del participante debe ejecutarse también:

```bash
python3 CTF_Automotive/scripts/decoy_traffic.py
```

El GM puede verificar el funcionamiento con `candump vcan0`, pero el participante debe tener su propio inyector para que su Fase 1 sea independiente.

## 4. Preparar la VM Game Master

```bash
ip link show vcan0
python3 -c "import can; print('python-can OK')"
cd CTF_Automotive
python3 scripts/decoy_traffic.py
```

El GM conserva el enunciado maestro, valida las evidencias y controla el tiempo. El `vcan0` de esta VM sirve para una demostración o para verificar la plantilla, no para alimentar los buses de los participantes.

## 5. Desplegar CTFd

CTFd se recomienda en una VM independiente. Con Docker Compose, la VM necesita Docker Engine, Compose v2, Redis y la base de datos definidos por la distribución de CTFd.

```bash
sudo apt update
sudo apt install -y ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
  -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo \"$VERSION_CODENAME\") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo systemctl enable --now docker
```

```bash
sudo git clone https://github.com/CTFd/CTFd.git /opt/CTFd
sudo chown -R "$USER:$USER" /opt/CTFd
cd /opt/CTFd
docker compose up -d
docker compose ps
```

Abrir desde una VM del aula la URL que indique el Compose de la versión instalada de CTFd, normalmente `http://IP_CTFD:8000`.

## 6. Configurar retos

Crear un reto por flag facilita la puntuación automática:

| Reto | Puntos |
|---|---:|
| F1A, F1B, F1C | 50 cada uno |
| F2A, F2B, F2C, F2D | 50 cada uno |
| F3 — Replay | 150 |
| F4 — DoS y fuzzing | 150 |
| Bonus — Defensa | 100 |

Las flags fijas pueden validarse automáticamente. F4 y Bonus conviene validarlas manualmente o mediante un reto pendiente de revisión, porque requieren comprobar evidencias y explicación técnica.

## 7. Prueba de conectividad

Desde una VM participante:

```bash
ping -c 3 IP_CTFD
curl -I http://IP_CTFD:8000
```

Desde el navegador, crear un equipo de prueba, introducir una flag de prueba y comprobar que el marcador se actualiza. Después eliminar el reto y la cuenta de prueba antes del curso.

## 8. Comprobación de aislamiento CAN

En el GM, solo durante la preparación, enviar un frame de prueba:

```bash
cansend vcan0 6F0#DEADBEEF
```

En la VM participante:

```bash
candump vcan0,6F0:7FF
```

No debe aparecer nada. Si aparece, los entornos comparten indebidamente el bus y no se debe iniciar el CTF hasta corregirlo.

## 9. Problemas frecuentes

| Problema | Solución |
|---|---|
| `docker-compose-plugin` no se encuentra | Añadir el repositorio oficial de Docker y repetir `apt update` |
| `permission denied` en `/var/run/docker.sock` | `sudo usermod -aG docker $USER`, cerrar sesión y volver a entrar; comprobar con `docker run hello-world` |
| `vcan0` no aparece | Cargar `vcan` y crear la interfaz con `ip link` |
| El GM ve tráfico pero el participante no | Es normal si son VMs distintas; ejecutar ICSim y `decoy_traffic.py` en cada VM |
| CTFd no responde | Comprobar `docker compose ps`, logs, IP de la VM y firewall del puerto publicado |

No usar `chmod 666 /var/run/docker.sock`: el socket Docker equivale a acceso administrativo sobre la VM.

## 10. Copias de seguridad

Antes de una sesión importante, detener temporalmente CTFd y guardar su directorio persistente o el mecanismo de backup que recomiende la versión desplegada. No guardar contraseñas ni secretos en el repositorio del curso.