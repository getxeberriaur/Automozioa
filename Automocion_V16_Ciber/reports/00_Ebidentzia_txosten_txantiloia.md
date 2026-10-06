# Ebidentzia txostenaren txantiloia — V16 laborategia (taldea)

## 1) Taldearen datuak
- Ikastetxea:
- Ikastaroa / taldea:
- Talde zk.:
- Kideak:
- Data:
- Irakaslea:

## 2) Praktikaren helburua
Azaldu 3-5 lerrotan zer balidatu den laborategian (simulatutako V16 abisuen harrera, segurtasun-kontrolak eta trazabilitatea).

## 3) Erabilitako ingurunea
- Sistema eragilea:
- Python:
- Mendekotasunak instalatuta (`requirements.txt`): Bai / Ez
- Backend martxan (`/health`): Bai / Ez
- Panel bisuala martxan (`/aginte-panela`): Bai / Ez

## 4) Exekutatutako proba-kasuak

| Kasua | Komandoa | Espero den emaitza | Ikusitako emaitza | Ongi? |
|---|---|---|---|---|
| legitimoa | `python simulator/send_event.py legitimo` | `accepted_for_processing` |  |  |
| replay-a | `python simulator/send_event.py replay` | 1.a accepted, 2.a rejected (`replayed_nonce`) |  |  |
| timestamp atzeratua | `python simulator/send_event.py timestamp-atrasado` | rejected (`message_out_of_time_window`) |  |  |
| koordenatu baliogabeak | `python simulator/send_event.py coordenadas-invalidas` | rejected (tarte-balidazioa) |  |  |
| identitate baliogabea | `python simulator/send_event.py identidad-invalida` | rejected (`unknown_device_id`) |  |  |
| ráfaga | `python simulator/send_event.py rafaga --count 8` | azken mezuak rejected (`rate_limit_exceeded`) |  |  |

## 5) Ebidentziak (pantaila-argazkiak edo zatiak)
Gehitu gutxienez 3 ebidentzia:

1. Onartutako abisu legitimoaren pantaila (erantzuna edo panela).
2. `replayed_nonce` arrazoiarekin baztertutako replay-aren pantaila.
3. Timestamp edo rate limiting arrazoiz baztertutako mezuaren pantaila.

Aukerako erreferentziak:
- JSON ikuspegia: `http://127.0.0.1:8080/events/recent?limit=10`
- Panel operatiboa: `http://127.0.0.1:8080/aginte-panela`
- Log-a: `logs/events.log`

## 6) Analisi tekniko laburra
### 6.1 Balidatutako kontrolak
- Eskema-balidazioa:
- Denbora-leihoa (`security.sent_at`):
- Anti-replay (`security.nonce`):
- Identitatearen araberako rate limiting-a:

### 6.2 Oharrak
- Zein kontrol izan da eraginkorrena?
- Positibo faltsurik egon da?
- Saioan zein arazo praktiko agertu da?

## 7) Ondorioak eta hobekuntzak
- Ondorio nagusia (1-2 esaldi):
- 1. hobekuntza (epe laburra):
- 2. hobekuntza (epe ertaina):
- 3. hobekuntza (produkzio-inguruneagoa: sinadura, PKI, monitorizazioa...):

## 8) Entregaren checklista
- [ ] Kasuen taula osatuta
- [ ] Gutxienez 3 ebidentzia erantsita
- [ ] Ondorioak idatzita
- [ ] Fitxategia `reports/` karpetan gordeta
