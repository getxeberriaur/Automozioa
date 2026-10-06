# RF laborategi segurua — Espektroaren analisi pasiboa

RTL-SDR hargailuarekin 433 MHz inguruko espektroa neurtzeko laborategia. Erabili isolatutako proba-igorle propioa eta tokiko laborategi kontrolatua. Ez da transmisiorik, replay-rik, jamming-ik edo ibilgailu errealen probatzerik egiten.

## Helburuak

- RTL-SDR eta Raspberry Pi prestatzea.
- Oinarrizko espektroa eta proba-igorlearen pultsuak CSVn jasotzea.
- Kaptura eramangarrira kopiatu, grafikoki aztertu eta emaitzak dokumentatzea.
- Datuetatik defentsa-neurriak proposatzea.

## Ibilbidea

1. Irakurri [segurtasun- eta etika-arauak](docs/04_ETICA_Y_SEGURIDAD.md).
2. Prestatu ekipoak [Raspberry Pi gidari](docs/01_GUIA_RASPBERRY.md) eta [eramangarriaren gidari](docs/02_GUIA_PORTATIL.md) jarraituz.
3. Egin [kaptura-prozedura](docs/03_PROCEDIMIENTO_CAPTURA.md).
4. Bete [ikasleen txostena](templates/INFORME_ALUMNOS.md) eta [segurtasun-zerrenda](templates/CHECKLIST_SEGURIDAD.md).

## Tresnak

- `scripts/spectrum_capture.sh`: RTL-SDR bidezko kaptura pasiboa.
- `scripts/analyze_spectrum.py`: CSV kargatu, analisia eta grafikoak.

## Ekipoa

Raspberry Pi, RTL-SDR hargailua, jasotze-antena, 433.92 MHz-eko proba-igorle isolatua eta analisirako Python duen eramangarria behar dira. Ez konektatu igorlea hartzaile edo instalazio erreal batera.

## Segurtasun-arauak

Harrapatu proba-igorle isolatuaren seinaleak soilik, irakaslearen zaintzapean. Debekatuta dago auto-giltzak, TPMS edo beste sistema erreal batzuen seinaleak harrapatzea, transmititzea edo erreproduzitzea. Ez eraman ekipoa laborategitik kanpora.

