# Praktika Txostena — V16 Baliza Simulagailua
**CVE-2025-65855 · Help Flash IoT · Ahultasun Analisia**

---

## Parte hartzailearen datuak

| Eremua | Balioa |
|--------|--------|
| **Izen-abizenak** | |
| **Data** | |
| **Modulua / Ikastaroa** | |
| **Lan ingurunea** | Ubuntu 22 / VM / beste bat: |

---

## 1. atala — Ingurunearen ezagupena

### 1.1 Zer endpoint eskaintzen ditu backendak?

| Endpoint | Metodoa | Deskribapena |
|----------|---------|--------------|
| | | |
| | | |
| | | |

### 1.2 Zer eremu ditu gertaera legitimoak?

```json
{

}
```

### 1.3 Zer erantzun ematen du backendak gertaera legitimo baten aurrean?

```
// zerbitzariaren erantzuna
```

---

## 2. atala — Eraso eszenatokiak

### 2.1 Replay Attack

| Eremua | Balioa |
|--------|--------|
| **Exekutatutako komandoa** | `python3 simulator/send_event.py replay` |
| **Zerbitzariaren erantzuna** | |
| **HTTP kodea** | |
| **Erasoak arrakasta izan du?** | ✅ Bai / ❌ Ez |
| **Zergatik?** | |

### 2.2 Atzeratutako timestamp-a

| Eremua | Balioa |
|--------|--------|
| **Exekutatutako komandoa** | `python3 simulator/send_event.py timestamp-atrasado` |
| **Zerbitzariaren erantzuna** | |
| **HTTP kodea** | |
| **Erasoak arrakasta izan du?** | ✅ Bai / ❌ Ez |
| **Zergatik?** | |

### 2.3 Koordenatu baliogabeak

| Eremua | Balioa |
|--------|--------|
| **Exekutatutako komandoa** | `python3 simulator/send_event.py coordenadas-invalidas` |
| **Zerbitzariaren erantzuna** | |
| **HTTP kodea** | |
| **Erasoak arrakasta izan du?** | ✅ Bai / ❌ Ez |
| **Zergatik?** | |

### 2.4 Identitate baliogabea

| Eremua | Balioa |
|--------|--------|
| **Exekutatutako komandoa** | `python3 simulator/send_event.py identidad-invalida` |
| **Zerbitzariaren erantzuna** | |
| **HTTP kodea** | |
| **Erasoak arrakasta izan du?** | ✅ Bai / ❌ Ez |
| **Zergatik?** | |

### 2.5 Rafaga (Rate Limiting)

| Eremua | Balioa |
|--------|--------|
| **Exekutatutako komandoa** | `python3 simulator/send_event.py rafaga --count 10` |
| **Zein eskaeratik aurrera hasi zen baztertzen?** | |
| **Baztertzeko HTTP kodea** | |
| **Ondorioa** | |

---

## 3. atala — Backendaren analisia

### 3.1 Zer balioztapen inplementatzen ditu backendak?

| Balioztapena | Inplementatuta? | Kodea/lerroa |
|--------------|----------------|--------------|
| Timestamp egiaztapena | | |
| Replay detekzioa | | |
| GPS koordenatuak balioztatzea | | |
| Gailuaren autentifikazioa | | |
| Rate limiting | | |

### 3.2 Identifikatu dituzun ahultasunak (arindu gabe daudenak)

1. 
2. 
3. 

### 3.3 Ebidentzia garrantzitsuenaren loga

```
// itsatsi hemen kapturatu duzun log garrantzitsuena
```

---

## 4. atala — Hobekuntza proposamenak

### 4.1 Nola hobetuko zenuke backendaren segurtasuna?

| Identifikatutako ahultasuna | Proposatutako hobekuntza |
|----------------------------|--------------------------|
| | |
| | |
| | |

### 4.2 Zer aldaketa egingo zenituzke baliza → zerbitzari protokoloan?

1. 
2. 
3. 

---

## 5. atala — Azken hausnarketa

### 5.1 Zer benetako eragin izango luke ahultasun hauek produkzioan ustiatzeak?

*// erantzun librea (gutxienez 5 lerro)*

### 5.2 Zer erlazio du praktika honek UNECE R155 araudiarekin?

*// erantzun librea*

---

## Entregatzeko zerrenda

- [ ] Simulagailuaren eszenatoki guztiak exekutatu
- [ ] Log kapturak txostenean itsatsita
- [ ] Ahultasunak identifikatu eta dokumentatu
- [ ] Hobekuntza proposamenak argudiatu
- [ ] Azken hausnarketa osatu

---
*Txantiloia Automozioko Zibersegurtasun ikastarorako sortua — Automozioa*