# Abiarazte azkarra — RF kaptura pasiboa

Erabili RTL-SDR hargailua eta isolatutako proba-igorlea. Ez egin transmisiorik, replay-rik edo interferentziarik.

## Baldintzak

- Raspberry Pi 4/5 eta RTL-SDR hargailua.
- 433.92 MHz-eko proba-igorle isolatua.
- Python 3 duen eramangarria, analizatzeko mendekotasunekin.

## Prestaketa

1. Irakurri [segurtasun-arauak](docs/04_ETICA_Y_SEGURIDAD.md).
2. Instalatu ekipoa [Raspberry Pi gidarekin](docs/01_GUIA_RASPBERRY.md) eta prestatu analisia [eramangarriaren gidarekin](docs/02_GUIA_PORTATIL.md).
3. Jarraitu [kaptura-prozedurari](docs/03_PROCEDIMIENTO_CAPTURA.md).

## Kapturatu eta aztertu

Raspberry Pi-n, `spectrum_capture.sh` scriptaren karpetan:

```bash
./spectrum_capture.sh 120 ~/rf_capture
```

Kopiatu sortutako CSVa eramangarrira eta exekutatu:

```bash
python3 scripts/analyze_spectrum.py data/spectrum_<data>.csv
```

Gorde grafikoak eta bete [txosten-txantiloia](templates/INFORME_ALUMNOS.md).

## Segurtasun-mugak

Erabili laborategian eta zaintzapean dagoen proba-igorlea soilik. Ez harrapatu benetako giltzen edo ibilgailuen seinalerik. Ez transmititu edo erreproduzitu seinalerik.
