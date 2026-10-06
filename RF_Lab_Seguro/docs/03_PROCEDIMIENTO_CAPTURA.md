# Kaptura-prozedura — RF laborategi pasiboa

**Iraupena:** 90-120 minutu. **Taldea:** 3-4 ikasle. Irakaslea laborategian egongo da saio osoan.

## Hasi aurretik

- Irakurri [segurtasun- eta etika-gida](04_ETICA_Y_SEGURIDAD.md).
- Egiaztatu Raspberry Pi, RTL-SDR, antena eta proba-igorle isolatua prest daudela.
- Egiaztatu `rtl_test -t` komandoak hargailua aurkitzen duela.
- Ez konektatu proba-igorlea hartzaile edo ibilgailu erreal batera.
- Ez erabili SDR transmisiorako, seinalea erreproduzitzeko edo interferentziak sortzeko.

## 1. fasea — Oinarrizko kaptura

1. Raspberry Pi-ra konektatu eta ireki `~/rf_capture` karpeta.
2. Igorlea itzalita dagoela, jaso oinarrizko espektroa:

```bash
./spectrum_capture.sh 60 ~/rf_capture/data
```

3. Idatzi erabilitako antena, kapturaren iraupena eta inguruko baldintzak.

## 2. fasea — Proba-igorlearen kaptura

1. Kokatu proba-igorle isolatua jasotze-antenatik 50 cm ingurura, laborategiko mahaian.
2. Hasi 120 segundoko kaptura:

```bash
./spectrum_capture.sh 120 ~/rf_capture/data
```

3. Kaptura martxan dagoela, irakasleak adostutako uneetan sakatu proba-igorlearen botoia. Utzi gutxienez 7 segundo pultsazioen artean; ez erabili beste igorlerik.
4. Itxaron kaptura amaitu arte. Ez da seinalerik transmititu edo erreproduzitzen.

## 3. fasea — CSVa eramangarrira kopiatu eta aztertu

```bash
scp pi@<RASPBERRY_IP>:~/rf_capture/data/*.csv ./data/
python3 RF_Lab_Seguro/scripts/analyze_spectrum.py data/<KAPTURA>.csv
```

Konparatu oinarrizko kaptura eta pultsazio-kaptura. Markatu potentzia-aldaketak grafikoan, eta azaldu neurketaren mugak.

## 4. fasea — Txostena

Osatu `RF_Lab_Seguro/templates/INFORME_ALUMNOS.md`:

- erabili diren ekipoak eta ezarpenak;
- kapturen izenak eta pultsazioen orduak;
- sortutako grafikoak eta behaketak;
- emaitzaren ziurgabetasunak;
- defentsa-neurri proposatuak.

## Amaiera

Gelditu kaptura, itzali proba-igorlea eta gorde ekipoa. Ez gorde edo partekatu baimenik gabeko seinalerik.

