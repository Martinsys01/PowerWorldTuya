## **Na Linuxu můžete aktivovat virtuální prostředí a nastavovat proměnné prostředí podle následujících kroků:##
1. **Vytvoření a aktivace virtuálního prostředí**

	Virtuální prostředí je izolované prostředí pro Python, které vám umožní instalovat závislosti projektu bez ovlivnění globálních balíčků.
	**a) Vytvoření virtuálního prostředí**

	V terminálu přejděte do adresáře projektu a spusťte:

```python3 -m venv venv
```

	To vytvoří adresář venv, kde budou uloženy všechny závislosti projektu.
	**b) Aktivace virtuálního prostředí**

**Aktivujte virtuální prostředí příkazem:**
```
	source venv/bin/activate
```

Po aktivaci by se měl v terminálu objevit prefix **(venv)** na začátku řádku, například:
```
(venv) user@hostname:~/project$
```
**c) Deaktivace virtuálního prostředí**

Pro deaktivaci virtuálního prostředí použijte příkaz:

```
deactivate
```
2. **Nastavení proměnných prostředí
	a) Nastavení proměnných do .env

	**Pokud používáte soubor .env, zajistěte, aby byl v kořenovém adresáři projektu. A byl správně nakonfigurován dle .env.template Například:**

TUYA_API_KEY=exampleApiKey
UYA_API_SECRET=exampleApiSecret
TUYA_API_REGION=eu

PUMP1_DEVICE_ID=exampleDeviceId1


DEBUG=true
DATABASE_URL=postgresql://user:password@localhost/dbname

**b) Načtení proměnných prostředí**

V projektech používáme knihovnu python-dotenv, abyste načetli proměnné z .env do aplikace:

```
from dotenv import load_dotenv
import os
```

## **Načíst proměnné prostředí ze souboru .env**##
```load_dotenv()
```

	# Použít proměnné prostředí

```api_key = os.getenv("API_KEY")
debug_mode = os.getenv("DEBUG", "false").lower() == "true"
```

	**c) Ruční nastavení proměnných prostředí (pouze dočasné)**

Proměnné prostředí můžete nastavit přímo v terminálu. Tyto proměnné budou aktivní pouze po dobu trvání relace terminálu:

export API_KEY=abc123
export DEBUG=true

Pro kontrolu nastavených proměnných použijte:

echo $API_KEY

3. **Automatická aktivace prostředí při spuštění**

Pro zjednodušení aktivace virtuálního prostředí a načtení proměnných můžete přidat do svého skriptu spouštěcí logiku.
	**a) Vytvoření spouštěcího skriptu*

Vytvořte soubor, například start.sh, a vložte do něj:

#!/bin/bash
```
source venv/bin/activate
python3 main.py
```

Udělejte skript spustitelný:
```
chmod +x start.sh
```

Spusťte aplikaci:

```
./start.sh
```

	**b) Automatizace při startu systému (volitelné)**

Pokud chcete, aby se aplikace spouštěla automaticky při startu systému, můžete použít systemd nebo cron.
4. **Testování**

Po aktivaci virtuálního prostředí a nastavení proměnných prostředí spusťte aplikaci:
```
python3 main.py
```

Pokud je vše správně nastaveno, aplikace by měla běžet bez problémů.


