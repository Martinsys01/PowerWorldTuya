# Detailní nastavení konfigurace v adresáři `config`

Tento dokument popisuje jednotlivé konfigurační soubory v adresáři `config` projektu "Tepelka". Obsahuje informace o jejich účelu, struktůře a ukázky nastavení.

---

## **1. `debug_config.py`** (Diagnostika)
Používá se pro řízení diagnostického režimu aplikace.

### Struktura souboru:
```python
# Povolení/zakázání diagnostického režimu
DEBUG_MODE = True  # True = diagnostický režim zapnut, False = vypnut
```

### Popis:
- `DEBUG_MODE`: Pokud je nastavena hodnota `True`, aplikace vypisuje podrobné diagnostické informace do logů i na konzoli.

### Použití:
- Zapnutý režim ladění: `DEBUG_MODE = True`
- Vypnutý režim ladění: `DEBUG_MODE = False`

---

## **2. `influxdb_config.py`** (Připojení na InfluxDB server)
Obsahuje konfiguraci pro přístup k databázi InfluxDB, kde se ukládají data z čerpadel.

### Struktura souboru: 
###!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
###POZOR KONFIGURACE BYLA PŘESUNUTA DO ".env"  V TOMTO SOUBORU NIC NEMĚNIT	   
###!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
```python
# Nastavení připojení k InfluxDB
url = "http://localhost:8086"  # URL InfluxDB serveru
token = "VašeToken"  # Token pro přístup
org = "VašeOrganizace"  # Jméno organizace (např. MARSYS)
bucket = "heat_pump"  # Bucket pro ukládání dat
```

### Popis:
- `url`: URL serveru InfluxDB. Standardně je to `http://localhost:8086`.
- `token`: Token pro autentizaci, který lze vygenerovat v InfluxDB.
- `org`: Organizace, do které patří bucket a data.
- `bucket`: Bucket, kam budou data ukládána.

### Ukázka nastavení:
```python
url = "http://192.168.1.100:8086"
token = "exampleGeneratedToken123"
org = "MARSYS"
bucket = "heat_pump"
```

---

## **3. `log_config.py`** (Logování)
Slouží k nastavení logův aplikace.

### Struktura souboru:
```python
import logging
import os

# Nastavení cesty k log souboru
LOG_FILE = os.path.join(os.path.dirname(__file__), "../Log/tepelka_main.log")

def setup_logging(debug_mode):
    # Zajištění existence složky Log
    log_dir = os.path.dirname(LOG_FILE)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Odstranění stávajících handlerů
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # Nastavení logování
    logging.basicConfig(
        level=logging.DEBUG if debug_mode else logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE, encoding="utf-8"),
            logging.StreamHandler() if debug_mode else None
        ]
    )
    logging.info("Logování bylo nastaveno.")
```

### Popis:
- `LOG_FILE`: Cesta k souboru, kam se budou ukládat logy.
- `setup_logging(debug_mode)`: Funkce pro inicializaci logování. Zohledňuje, zda je zapnut režim ladění (`debug_mode`).

---

## **4. `pump_config.json`** (Konfigurace čerpadel z Tuya Cloudu)
## !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
##!!!Soubor zrušen a konfigurace v ".env"  !!!!!!!!!!!!!!!!!!!!!!!!!!!
##!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
Tento soubor definuje ID, názvy a stav aktivace pro jednotlivá čerpadla.

### Struktura souboru:
```json
{
    "pump1": {
        "deviceId": "exampleDeviceId1",
        "name": "Tepelko 1 L",
        "active": true
    },
    "pump2": {
        "deviceId": "exampleDeviceId2",
        "name": "Tepelko 2 P",
        "active": false
    }
}
```

### Popis:
- `deviceId`: Identifikátor zařízení na Tuya Cloudu.
- `name`: Čitelý název zařízení.
- `active`: Boolean hodnota (true/false), určuje, zda je čerpadlo aktivní.

### Ukázka nastavení:
```json
{
    "pump1": {
        "deviceId": "exampleDeviceId1",
        "name": "Tepelko 1 L",
        "active": true
    },
    "pump2": {
        "deviceId": "exampleDeviceId2",
        "name": "Tepelko 2 P",
        "active": true
    }
}
```

---

## **5. `tuya_config.json`** (Přístupová data na Tuya Cloud Developer)
## !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
##!!!Soubor zrušen a konfigurace v ".env"  !!!!!!!!!!!!!!!!!!!!!!!!!!!
##!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
Obsahuje konfiguraci pro připojení k Tuya Cloud API.

### Struktura souboru:
```json
{
    "API_KEY": "exampleApiKey",
    "API_SECRET": "exampleApiSecret",
    "API_REGION": "eu"
}
```

### Popis:
- `API_KEY`: Veřejný klíč z Tuya Developer Console.
- `API_SECRET`: Tajný klíč z Tuya Developer Console.
- `API_REGION`: Region Tuya serveru, kde je zařízení registrováno (např. `eu`, `us`, `cn`).

### Ukázka nastavení:
```json
{
    "API_KEY": "exampleApiKey",
    "API_SECRET": "exampleApiSecret",
    "API_REGION": "eu"
}
```

---

## **Doporučení**
1. Uchovávejte soubory `tuya_config.json` a `pump_config.json` na bezpečném místě, aby nedošlo k neautorizovanému přístupu.
2. Pro testování nastavte `DEBUG_MODE = True`.
3. Po změně konfigurace restartujte aplikaci, aby se nové nastavení nahrálo.

