# Eramangarria prestatzea — RF datuen analisia

## Baldintzak

- Python 3 eta `pip`.
- Raspberry Pi-ra SSH bidez sartzeko aukera edo CSVak transferitzeko bide lokala.
- Grafikoak gordetzeko leku nahikoa.

## 1. Python mendekotasunak instalatu

Biltegiko `RF_Lab_Seguro/` karpetatik:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install matplotlib pandas numpy scipy
```

Windows PowerShell-en, aktibatu ingurunea honekin:

```powershell
.\.venv\Scripts\Activate.ps1
```

## 2. CSV fitxategiak kopiatu

Raspberry Pi-ko kaptura eramangarrira kopiatu, SSH bidez:

```bash
mkdir -p data
scp pi@<RASPBERRY_IP>:~/rf_capture/data/*.csv ./data/
```

## 3. Kaptura aztertu

Exekutatu biltegiaren erro-karpetatik:

```bash
python3 RF_Lab_Seguro/scripts/analyze_spectrum.py data/spectrum_<data>.csv
```

Aztertu sortutako grafikoak eta idatzi oinarrizko kapturaren eta proba-igorlearen kapturaren arteko aldeak. Datuetan jasotako potentzia soilik ikus daiteke; ez atera ondorio ziurrik igorlearen identitateari edo mezuaren edukiari buruz.

## 4. Emaitzak gorde

Gorde kaptura-fitxategia, grafikoak eta laburpen-oharrak. Bete `RF_Lab_Seguro/templates/INFORME_ALUMNOS.md` txantiloia. Ez igo hirugarrenen seinaleak edo kokapen-datuak biltegi publikora.

