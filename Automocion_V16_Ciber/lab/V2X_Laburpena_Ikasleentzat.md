# V2X Aurkezpena - Laburpena Ikasleentzat / Resumen Estudiantes

## 🚗 Zer da V2X? / ¿Qué es V2X?

**Vehicle-to-Everything (V2X)** = Ibilgailuek inguru osoarekin datorren teknologia.

### Komunikazio motak / Tipos:

| Motak | Zer da? | Adibidea |
|-------|---------|---------|
| **V2V** | Ibilgailutik ibilgailura | Aurrekoa duala bidean > sarrera-bideak baten |
| **V2I** | Ibilgailutik infraestrukturarainen | Semaforo inteligenteak lotzekotan |
| **V2P** | Ibilgailutik oinezkora | Oinezkoa detektatu abisuaren gain |
| **V2N** | Ibilgailutik sarean | Cloud zerbitzuak eta GPS komunera |

---

## 🛰️ Protokoloak / Protocolos

| Protokoloa | Banda | Tartea | Adibidea |
|-----------|-------|--------|---------|
| **DSRC** | 5.9 GHz | 100 m | AEBak, Japonia |
| **5G/C-V2X** | Zabalago | 500 m | Txina, berriketa autonoa |
| **NB-IoT** | Txarra zabala | 1-10 km | Help Flash baliza (Espainia) |

---

## 🔒 Seguritate-erronka / Desafíos de Seguridad

### Help Flash kasuan (Espainia):

❌ **Arazoak:**
- Datua testu garbian bidatzen da (GPS, IMEI, LTE signala)
- Ez da enkriptazioa
- Ez da autentifikazioa
- OTA eguneratzeak ez du sinaturik

✅ **Soluzioiak:**
- Enkriptazioa (TLS/DTLS)
- Autentifikazioa (ziurtagiak)
- Integritate kontseju (HMAC)
- Sinaturak (OTA segurua)

---

## 🧪 Laboratorio Praktika / Práctica de Laboratorio

### Zer egingo dugu? / Qué haremos:

1. **Baliza konfigurazioa deskubritu** → porto seriea ariketa
2. **Sare-trafikoa entzun** → Wireshark-rekin
3. **Baliza suplantatu** → IMEI duplika
4. **Alerta falsua bidali** → DGT 3.0-tik
5. **OTA firma falta** → Kaltegarri kodea sartu

### Denbora / Duración

- Aurkezpena: 30-40 min
- Praktika: 2 ordutan

### Materiala / Material

✓ Help Flash baliza (enpresa-taldeak bakoitza)
✓ Linux ordenagailua (WiFi)
✓ Wireshark edo tcpdump
✓ Python 3.8+

---

## 📊 Hamaika Gako Zenbakia / 11 Puntos Clave

1. V2X = lehenengo teknologia autobusarentzat
2. Dorriak baita balizak zure kokalekua irekitzen dute
3. Testu garbian = **ez da segurua**
4. Enkriptazioa = sarrera-aurrera gakoa
5. Autentifikazioa = nor zaude probatu
6. Integritatea = mezua ez datorik aldaturik
7. OTA sinaturak = eguneratzeak seguruak
8. Nonce + Timestamp = errepresia saihestu
9. IoT = ez du beti seguritate burua
10. Help Flash > 250,000 gailu Espainian
11. Gelan = **benetan egina jakitea abantaila!**

---

## 📚 Gehiago ikastekotan / Para saber más

- **Aurkezpena:** Askatu aurrean Web nabigatzailean
- **Praktikaaren deskribapena:** `05_Demo_Vulnerabilidades_Help_Flash.md` eta `05_Demo_Ahultasunak_Help_Flash_eu.md`
- **Skriptak:** `scripts/fake_ota_server.py` (OTA zerbitzaria simulatua)

---

## ❓ Ikasketaren Helburuak / Objetivos de Aprendizaje

Al final de esta práctica, deberías ser capaz de:

- ✓ Explicar qué es V2X y sus tipos (V2V, V2I, V2P, V2N)
- ✓ Identificar vulnerabilidades en comunicaciones inseguras
- ✓ Entender cómo funcionan los ataques a balizas IoT
- ✓ Proponer soluciones de seguridad basadas en criptografía
- ✓ Reflexionar sobre los riesgos de tecnología sin auditoría

---

**Gela ondoren burubeharra bilaketak eta ikusi zaitez onartzen!** 🎓

**¡Después de clase, seguid buscando y pasédselo bien aprendiendo!** 🚀
