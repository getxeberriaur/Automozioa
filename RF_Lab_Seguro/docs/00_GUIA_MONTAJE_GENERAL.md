# RF laborategia muntatzeko gida

## Helburua eta irismena

Laborategiak 433 MHz inguruko espektroa behatzeko aukera ematen du RTL-SDR hargailuarekin. Datuak jasotzea eta aztertzea da xedea; ez da transmisiorik egiten, eta ez da seinalerik erreproduzitzen edo nahasten.

```text
Proba-igorle isolatua -> jasotze-antena -> RTL-SDR -> Raspberry Pi
                                                  | CSV
                                                  v
                                         analisirako eramangarria
```

## Beharrezko materiala

- Raspberry Pi 4 edo 5, Raspberry Pi OSarekin.
- RTL-SDR donglea eta 433 MHz-eko jasotze-antena.
- 433.92 MHz-eko proba-igorle propioa, laborategian isolatua.
- Python 3 eta SSH duen eramangarria.
- Antenaren eta igorlearen arteko tartea: gutxi gorabehera 50 cm, laborategiko mahaian.

Ez erabili auto bati, ate-sistema bati edo bestelako hartzaile erreal bati lotutako igorlerik. Ez erabili RF transmisio-gailurik.

## Lan-fluxua

1. Egiaztatu RTL-SDR donglea `rtl_test -t` komandoarekin.
2. Sortu oinarrizko kaptura igorlea erabili gabe.
3. Egin bigarren kaptura, proba-igorlearen pultsazioak aurrez adostutako uneetan eginda.
4. Kopiatu CSV fitxategiak eramangarrira eta aztertu `analyze_spectrum.py` erabilita.
5. Gorde grafikoak, oharrak eta segurtasun-neurriak txostenean.

## Datuak interpretatzea

RTL-SDRk jasotako potentzia neurtzen du; ez du protokoloaren edukia edo igorlearen identitatea frogatzen. Grafikoan agertzen den pultsua denboran egindako pultsazioarekin lotu behar da, eta ondorioek neurketa horren mugak azaldu behar dituzte.

## Gelditu eta jaso

Amaitzean gelditu `rtl_power`, itzali proba-igorlea, deskonektatu antena eta gorde ekipoa. Ez kopiatu edo banatu laborategian jaso ez diren hirugarrenen seinaleak.

