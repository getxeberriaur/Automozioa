# Raspberry Pi eta RTL-SDR prestatzea

**Aurre-baldintzak:** Raspberry Pi 4/5, Raspberry Pi OS, sare-konexioa eta RTL-SDR hargailua.

## 1. Instalatu tresnak

```bash
sudo apt update
sudo apt install -y git rtl-sdr python3 python3-pip
```

Egiaztatu hargailua:

```bash
rtl_test -t
```

Ez badu gailurik aurkitzen, egiaztatu USB konexioa eta sistema eragilearen gailu-baimenak. Ez erabili RTL-SDR transmisiorako.

## 2. Prestatu kaptura-karpeta

```bash
mkdir -p ~/rf_capture/data
```

Ekarri biltegiko `RF_Lab_Seguro/scripts/spectrum_capture.sh` script-a Raspberry Pi-ra, edo exekutatu biltegiko karpetatik. Ziurtatu exekutatzeko baimena duela:

```bash
chmod +x spectrum_capture.sh
```

## 3. Egin kaptura pasiboa

```bash
./spectrum_capture.sh 120 ~/rf_capture/data
```

Script-ak 433.5-434.5 MHz tarteko espektroa jasotzen du CSV fitxategian. Igorlea itzalita eduki oinarrizko kapturan; ondoren, erabili laborategiko prozeduran zehaztutako pultsazioak soilik.

## 4. Kopiatu emaitzak eramangarrira

Aurkitu Raspberry Pi-ren IP helbidea eta erabili `scp` eramangarritik:

```bash
scp pi@<RASPBERRY_IP>:~/rf_capture/data/*.csv ./data/
```

Ez ireki SSH edo beste zerbitzurik sare publikora. Erabili ikastetxeko sare lokala eta irakaslearen jarraibideak.

