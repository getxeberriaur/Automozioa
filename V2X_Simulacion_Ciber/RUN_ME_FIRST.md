# V2X laborategia — abiarazte azkarra

**Baldintzak:** Python 3.10 edo berriagoa. Ez da kanpoko Python mendekotasunik behar.

## 1. Gateway babestua abiarazi

Lehen terminalean, biltegiaren erro-karpetatik:

```bash
python V2X_Simulacion_Ciber/scripts/v2x_gateway.py
```

Gateway-ak `http://127.0.0.1:8090` helbidean entzuten duela adieraziko du.

## 2. Mezu legitimoa bidali

Bigarren terminalean:

```bash
python V2X_Simulacion_Ciber/scripts/send_v2x.py legitimo
```

Espero den emaitza `HTTP 202` da, `accepted` egoerarekin.

## 3. Proba-agertokiak

```bash
python V2X_Simulacion_Ciber/scripts/send_v2x.py replay
python V2X_Simulacion_Ciber/scripts/send_v2x.py spoof
python V2X_Simulacion_Ciber/scripts/send_v2x.py impossible
python V2X_Simulacion_Ciber/scripts/send_v2x.py old
python V2X_Simulacion_Ciber/scripts/send_v2x.py burst
```

Agertoki horien izenak scriptaren interfazean erabiltzen dira; ez itzuli komandoak.

Babesik gabeko gateway-a alderatzeko, gelditu babestua eta abiarazi:

```bash
python V2X_Simulacion_Ciber/scripts/v2x_gateway.py --insecure
```

Alderatu erantzunak eta gorde ebidentziak [praktikaren txostenean](reports/00_Plantilla_informe.md).

## Amaiera

Gelditu gateway-a `Ctrl+C` sakatuz. Praktika osoa `127.0.0.1` helbidean egin; ez bidali mezurik kanpoko helbideetara.