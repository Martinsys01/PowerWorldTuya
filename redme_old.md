Popis projektu Tepelka

Projekt Tepelka je určen pro monitorování a vizualizaci dat ze dvou tepelných čerpadel PowerWorld PW58410 s možností volby aktivace jednoho nebo obou čerpadel prostřednictvím konfiguračního souboru. Data jsou získávána z Tuya Cloud API a ukládána do databáze InfluxDB. Projekt zahrnuje aplikaci pro sběr a ukládání dat, stejně jako webovou vizualizaci, která umožňuje sledování provozních parametrů čerpadel.
Hlavní funkce projektu

    Sběr dat:
        Získávání aktuálních stavů a měřených hodnot čerpadel z Tuya Cloud API.
        Ukládání dat do databáze InfluxDB.

    Podpora jednoho nebo dvou čerpadel:
        Volba aktivních čerpadel prostřednictvím konfiguračního souboru pump_config.json.

    Webová vizualizace dat:
        Zobrazení naměřených hodnot v reálném čase na interaktivní webové stránce.
        Přehledné grafické rozhraní přizpůsobené pro stolní počítače i mobilní zařízení.

    Modulární design:
        Konfigurační soubory umožňují snadné přizpůsobení aplikace pro různé scénáře.
        Možnost ladění a diagnostiky prostřednictvím debugovacího režimu.

Popis jednotlivých částí projektu
1. Sběr dat

Hlavní program main.py zajišťuje komunikaci s Tuya Cloud API, získává data o provozu čerpadel a ukládá je do databáze InfluxDB. Aktivní čerpadla jsou definována v souboru pump_config.json.

Příklad konfigurace:

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

Pokud je active nastaveno na false, odpovídající čerpadlo nebude dotazováno na stav.
2. Databázové ukládání

Data získaná z Tuya Cloud API jsou ukládána do databáze InfluxDB. Konfigurace připojení je definována v souboru influxdb_config.py:

url = "http://localhost:8086"
token = "exampleToken"
org = "MARSYS"
bucket = "heat_pump"

3. Webová vizualizace

Vizualizační aplikace je umístěna ve složce /Rozhrani. Spouští se pomocí Flask serveru (app.py) a umožňuje uživateli přístup k aktuálním datům prostřednictvím webového rozhraní.

Hlavní funkce:

    Zobrazení hodnot jako teploty, tlaků, rychlostí ventilátorů atd.
    Responzivní design optimalizovaný pro PC i mobilní zařízení.
    Dynamické aktualizace dat z InfluxDB.

Spuštění vizualizace:

cd Rozhrani
python app.py

Po spuštění aplikace je možné přejít na webovou adresu:

http://127.0.0.1:5000

4. Konfigurace a ladění

    Diagnostický režim (DEBUG_MODE): Nastavení pro podrobné logování a ladění aplikace. Aktivuje se v souboru debug_config.py.

    DEBUG_MODE = True

    Logování: Logy jsou ukládány do souboru tepelka_main.log ve složce Log. Nastavení je definováno v log_config.py.
    Přístupové údaje: API klíče a tajné klíče pro Tuya Cloud API jsou uloženy v tuya_config.json.

Přednosti projektu

    Možnost připojení až dvou čerpadel s flexibilní konfigurací.
    Webová vizualizace, která umožňuje snadný přehled o provozu čerpadel.
    Modulární architektura zajišťující jednoduché přizpůsobení a údržbu.

Projekt "Tepelka" je navržen tak, aby poskytoval kompletní řešení pro monitorování a vizualizaci teplotních čerpadel, přičemž uživatelům nabízí jednoduchost použití a robustní funkcionalitu.











# Instalační příručka pro projekt "Tepelka"

## 0 Požadavky před instalací
	- Tuya developer účet s připojenými zařízení a přidáním služby core+  viz soubor readmeTuay.md
	- Instalace InfluxDB serveru  na PC  Windows nebo Linux verzi, vytvoření uživatele se jménem a heslem, vytvoření názvu firmy (MARSYS) a buketu (heat_pump), vytvoření tokenu s právy pro zápis a pro čtení 
		můžete použivat jeden nebo dva (pro zápis hlavní a pro čtení na zobrazení vizualizace)  viz soubor readmeInfluxDB.md
	- Budete li chtít data zpracovávat i v Grafaně  tak nainstalovat Grafanu, vytvořit uživatele a nakonfigurovat Datové zdroje v jazyku FLUX, přístupový token vložit z InfluxDB, rovněž jméno firmy a buketu (heat_pump)  



## 1. Požadavky na systém
Před instalací se ujistěte, že máte nainstalováno:

- **Python**: Verze 3.9 a vyšší (doporučená 3.12)
- **Pip**: Správce balíčků Pythonu
- **Operační systém**: Windows 10/11 nebo Linux
- **Internetové připojení**: Pro stahování balíčků a připojení k Tuya cloudu a InfluxDB

## 2. Stažení a příprava projektu
1. **Stažení projektu**:
   - Získejte zdrojové soubory projektu z repozitáře nebo z distribuovaného balíčku.
   - Rozbalte projekt do cílové složky, například `C:\Tepelka`.

2. **Přesun do složky projektu**:
   - **Windows (PowerShell)**: Otevřete PowerShell, přejděte do složky projektu pomocí:
     ```powershell
     cd C:\Tepelka
     ```
   - **Linux (Terminál)**: Použijte:
     ```bash
     cd /path/to/Tepelka
     ```

## 3. Nastavení virtuálního prostředí
Doporučuje se používat virtuální prostředí pro správu závislostí.

1. **Vytvoření virtuálního prostředí**:
   - **Windows (PowerShell)**:
     ```powershell
     python -m venv venv
     ```
   - **Linux (Terminál)**:
     ```bash
     python3 -m venv venv
     ```

2. **Aktivace prostředí**:
   - **Windows (PowerShell)**:
     ```powershell
     .\venv\Scripts\Activate
     ```
   - **Linux (Terminál)**:
     ```bash
     source venv/bin/activate
     ```

3. **Aktualizace pip**:
   ```bash
   pip install --upgrade pip
   ```

## 4. Instalace závislostí
Instalace všech požadovaných balíčků pomocí souboru `requirements.txt`.

```bash
pip install -r requirements.txt
```

## 5. Konfigurace projektu
Projekt je navržen pro monitorování dvou tepelných čerpadel. Data z těchto čerpadel se získávají prostřednictvím Tuya Cloud API a ukládají se do InfluxDB. Před spuštěním je nutné správně nastavit konfiguraci.

1. **Tuya Cloud**:
   - V souboru `config/tuya_config.json` nastavte:
     - `API_KEY`: Klíč API z Tuya Developer Console.
     - `API_SECRET`: Tajný klíč z Tuya Developer Console.
     - `API_REGION`: Region kde máte vytvořený server  předpokládáme eu  (např. `eu`, `us`, `cn`).

2. **InfluxDB**:
   - V souboru `config/influxdb_config.py` nastavte:
     - `url`: URL vaší instance InfluxDB.
     - `token`: Token pro přístup do InfluxDB.
     - `org`: Název organizace v InfluxDB.
     - `bucket`: Název bucketu, kde budou ukládána data.

3. **Konfigurace čerpadel**:
   - V souboru `config/pump_config.py`:
     - Zadejte `DEVICE_ID_PUMP1`, `DEVICE_ID_PUMP2` a jejich názvy.

## 6. Spuštění projektu
### 6.1 Hlavní aplikace
Spuštění hlavního programu, který stahuje data z Tuya Cloud a ukládá je do InfluxDB:

```bash
python main.py
```

### 6.2 Vizualizace dat
Pro spuštění vizualizace dat:

1. Přejděte do složky `Rozhrani`:
   ```bash
   cd Rozhrani
   ```

2. Spusťte Flask aplikaci:
   ```bash
   python app.py
   ```

3. Otevřete webový prohlížeč a přejděte na adresu:
   ```
   http://127.0.0.1:5000
   ```

## 7. Další informace
### 7.1 Přidání nových parametrů pro měření
Pokud potřebujete přidat nové parametry pro měření:

1. Aktualizujte `config/parameter_mappings.py` s novými parametry.
2. Upravte dotazy v `main.py` nebo `app.py`, aby zahrnovaly nové parametry.

### 7.2 Debugging
Pro ladění nastavte `DEBUG_MODE = True` v `config/debug_config.py`.

### 7.3 Správa závislostí
Pokud přidáváte nové balíčky, nezapomeňte aktualizovat `requirements.txt` pomocí:

```bash
pip freeze > requirements.txt
```

## 8. Odinstalace
Pro odstranění prostředí a projektu:

1. Deaktivujte virtuální prostředí:
   ```bash
deactivate
   ```

2. Smažte složku projektu:
   - **Windows (PowerShell)**:
     ```powershell
     Remove-Item -Recurse -Force Tepelka
     ```
   - **Linux (Terminál)**:
     ```bash
     rm -rf Tepelka
     ```

## 9. Časté problémy
### Chyba při připojení k InfluxDB
- Ověřte správnost nastavení URL a tokenu.
- Zkontrolujte, zda je služba InfluxDB spuštěná.

### Chyba při připojení k Tuya Cloud
- Ujistěte se, že API klíč a tajný klíč jsou správné.
- Zkontrolujte internetové připojení.

---
Tato příručka by měla pokrýt základní kroky pro instalaci a spuštění projektu. Pro další pomoc nebo dotazy se obraťte na správce projektu.

