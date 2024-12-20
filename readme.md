### Název projektu: **Monitorování a vizualizace dat tepelných čerpadel**

---

## **Popis projektu**

Tento projekt slouží k monitorování jednoho až dvou tepelných čerpadel (PowerWorld PW58410) prostřednictvím Tuya Cloud API. Naměřená data jsou ukládána do databáze **InfluxDB**, 
odkud jsou dále přístupná pro analýzu a vizualizaci. Součástí projektu je jednoduché webové rozhraní, které umožňuje vizualizaci aktuálních dat přímo z databáze InfluxDB.
Sběr dat:
        Získávání aktuálních stavů a měřených hodnot čerpadel z Tuya Cloud API.
        Ukládání dat do databáze InfluxDB.

    Podpora jednoho nebo dvou čerpadel:
        Volba aktivních čerpadel prostřednictvím konfiguračního souboru .env.

    Webová vizualizace dat:
        Zobrazení naměřených hodnot v reálném čase na interaktivní webové stránce.
        Přehledné grafické rozhraní přizpůsobené pro stolní počítače i mobilní zařízení.

    Modulární design:
        Konfigurační soubory umožňují snadné přizpůsobení aplikace pro různé scénáře.
        Možnost ladění a diagnostiky prostřednictvím debugovacího režimu.

Popis jednotlivých částí projektu

Hlavní funkce:
- **Sběr dat**: Data jsou vyčítána přes Tuya Cloud API a zpracována hlavním programem.
- **Ukládání dat**: Data jsou ukládána do InfluxDB v pravidelných intervalech.
- **Vizualizace dat**: Webové rozhraní zobrazuje aktuální data včetně časového razítka posledního vzorku.
- **Flexibilita**: Projekt umožňuje přepínání mezi jednou nebo dvěma tepelnými čerpadly prostřednictvím konfiguračního souboru `.env`.

---


## Licence

Tento projekt je licencován pod **MIT License**. Podrobnosti najdete v souboru [LICENSE](LICENSE).

## **Instalační příručka**

### **0. Požadavky před instalací**

1. **Tuya Cloud Developer účet** ** readmeTuay.md **:
   - Tuya developer účet s připojenými zařízení a přidáním služby core+  viz soubor ** readmeTuay.md **
	- Instalace InfluxDB serveru  na PC  Windows nebo Linux verzi, vytvoření uživatele se jménem a heslem, vytvoření názvu firmy (MARSYS) a buketu (heat_pump), vytvoření tokenu s právy pro zápis a pro čtení 
		můžete použivat jeden nebo dva (pro zápis hlavní a pro čtení na zobrazení vizualizace)  viz soubor readmeInfluxDB.md
	- Budete li chtít data zpracovávat i v Grafaně  tak nainstalovat Grafanu, vytvořit uživatele a nakonfigurovat Datové zdroje v jazyku FLUX, přístupový token vložit z InfluxDB, rovněž jméno firmy a buketu (heat_pump)  

   - Přidání tepelných čerpadel na developerský účet Tuya a aktivace služby "Core+".
   - Konfigurace API klíčů a přístupových údajů.

2. **InfluxDB**    viz **influxDB.md  **:
   - Nainstalujte InfluxDB a vytvořte firmu, bucket a přístupový token.
   - Doporučujeme vytvořit samostatné tokeny pro zápis dat a jejich čtení.
3. **Grafana (volitelné)** viz   **readmeGrafana.md**:
   - Instalace a konfigurace pro vizualizaci dat z InfluxDB pomocí jazyka Flux.
4. **Další software**:
   - **Python**: Verze 3.9 a vyšší (doporučená 3.12).
   - **Pip**: Správce balíčků Pythonu.
## 1. Požadavky na systém
Před instalací se ujistěte, že máte nainstalováno:

- **Python**: Verze 3.9 a vyšší (doporučená 3.12)  https://www.python.org/ftp/python/3.13.1/python-3.13.1-amd64.exe
	Stáhněte instalaci a spusťte instalátor, nezapomeňte zaškrtnou  v instalaci  ADd Python to enviromant variable  (aby byl dostupný PowerShelu) a pokračujte v instalaci
	Po instalaci  spustit PowerShel 
	Ověřit instalaci
	``` Pyhon  - vypíše se verze 
	pip     - výpis balíčků
	pip install  --upgrade pip    - nainstalujeme update 
	```
	
	
- **Pip**: Správce balíčků Pythonu
- **Operační systém**: Windows 10/11 nebo Linux
- **Internetové připojení**: Pro stahování balíčků a připojení k Tuya cloudu a InfluxDB
---

### **1. Stažení projektu**

1. **Stažení zdrojového kódu**:
   - Klonujte nebo stáhněte projekt z [GitHub repozitáře](https://github.com/Martinsys01/PowerWorldTuya).
   - Rozbalte soubory do cílové složky, např. `C:\Tepelka\`.

2. **Přesun do složky projektu**:
   - **Windows (PowerShell)**:
     ```powershell
     cd C:\Tepelka\PowerWorldTuya\ 
     ```
   - **Linux (Terminál)**:
     ```bash
     cd /path/to/Tepelka/PowerWorldTuya
     ```

---

### **2. Vytvoření virtuálního prostředí**

Doporučujeme používat virtuální prostředí pro správu závislostí.

1. **Vytvoření virtuálního prostředí**:  Nejprve ověřte zda Pyhon je správně  nainstalován. Napište v PowerShellu 
 python - vrátí se jeho verze  a příkazem  pip  ověříme správnou instalaci balíčků
   - **Windows**:
**powershell**  

```
     python -m venv venv
```
	
     
   - **Linux**:

```bash
     python3 -m venv venv
     ```

2. **Aktivace virtuálního prostředí**:
   - **Windows**:
     **powershell**
 ```
     .\venv\Scripts\Activate				
```
	 **(.venv)(PS C:\Tepelka\PowerWorldTuya>)**
	 
	 **Pokud se vypíše chybová hláška**
	 **.\venv\Scripts\Activate : File C:\Tepelka\PowerWorldTuya\venv\Scripts\Activate.ps1 
	 **cannot be loaded because running scripts is disabled on this system. **
	 
		Zavřete okno powershell  spussťte ho znovu s právy administrátora  
		( Start /Powershell - pravé tlačítko myši  - spustit jako Administrator
		Změňte politiku     příkazem 
		
``` 
Set-ExecutionPolicy RemoteSigned
	
	```
Potvrďte bezpečnostní dotaz  odpovědí **Yes   [Y] **
		
Znovu spusťte

```	
.\venv\Scripts\Activate
```
Teď by mělo  prostředí být aktivováno a před PS  by se mělo zobrazit venv  
**(venv) PS C:\Tepelko\PowerWorldTuay**
		
     
   - **Linux**:
     ```bash
     source venv/bin/activate
     ```



---

### **3. Instalace závislostí**

**Nainstalujte požadované balíčky pomocí souboru `requirements.txt`  stáhnou se všechny balíčka a závislosti, instalace chvilku potrvá tak vyčkejte dokonce:**
		Vždy musíte být  v  adresáři v aktivním projektu  zde   (venv).  PS C:\Tepelka\PowerWorld\>

```bash
pip install -r requirements.txt

```

---

### **4. Konfigurace projektu** vetšina konfigurace bude vytvořena v proměném prostředí v souboru .env**
	vvzorový soubor /config/env.template   otevřte v editoru  změnťe  za vaše hodnoty.
	Soubor uložte pod názvem ** .env   ( bez jakékoliv přípony) do kořenu složky PS C:\Tepelka\PowerWorld\**
	

1. **.env soubor**:
   - Vytvořte soubor `.env` ve složce projektu podle šablony `/config/env.template`.
   - Vyplňte údaje:
     - **Tuya API**: Klíče a region z developerského účtu.
     - **InfluxDB**: URL, token, firmu a bucket.
     - **Tepelná čerpadla**: Identifikátory zařízení a aktivace čerpadel.

2. **Šablona `.env.template`**:
   ```dotenv
   # InfluxDB konfigurace
   INFLUXDB_URL=http://localhost:8086
   INFLUXDB_TOKEN=VášInfluxToken
   INFLUXDB_ORG=VašeFirma
   INFLUXDB_BUCKET=heat_pump

   # Tuya API konfigurace
   TUYA_API_KEY=VášApiKey
   TUYA_API_SECRET=VášApiSecret
   TUYA_API_REGION=eu

   # Konfigurace čerpadel
   PUMP1_DEVICE_ID=DeviceIdPump1
   PUMP1_NAME=Tepelko 1 L
   PUMP1_ACTIVE=true

   PUMP2_DEVICE_ID=DeviceIdPump2
   PUMP2_NAME=Tepelko 2 P
   PUMP2_ACTIVE=true
   ```

3. ** Uložení .env
	Ulužte soubor do kořenu projektu  C:\Tepelka\PowerWorld\  pod názvem .env
---

### **5. Spuštění projektu**

1. **Spuštění hlavního programu**:
   - Program, který stahuje data z Tuya Cloud a ukládá je do InfluxDB:
     ```bash
     python main.py
     ```
	Pokud jste vytvořili správně  soubor *.env  a je srávně umístěn v kořenu  /PowerWorld/.env   projektu  mělo by vše běžet
		Při vypnutém debugu budete vidět zápis dat dle id čerpadla
		
		
2. **Spuštění webového rozhraní**:  Pusťte nový terminál (Powershell)
		 změna adresáře na adresář projektu

	```cd C:\Tepelka\PowerWorldTuya\
	
	```
	
	**	 Aktivace prostředí   **
	
	```
	.\venv\Scripts\Activate
	
	```
	
   -*Přesuňte se v projektu do složky `Rozhrani`:**
     
	 ```bash
     cd Rozhrani
     ```
   - *Spusťte Flask aplikaci:
     ```bash
     python app.py
     ```
   - Otevřete webový prohlížeč a přejděte na:
     ```
     http://127.0.0.1:5000 (nebo IP adresi zařízení na kterém to jede)
     ```

---

		**Vizualizace**

  **Webové rozhraní zobrazuje aktuální měřená data z InfluxDB:**
- **Tlačítka Tepelko 1 a Tepelko 2**: Přepínání mezi vizualizacemi pro jednotlivá čerpadla (aktivní dle `.env`).
- **Dynamická data**: Aktualizace hodnot každých 5 sekund.
- **Časová značka**: Zobrazuje čas posledního vzorku načteného z InfluxDB.
- **Responsivní design**: Optimalizace pro zobrazení na mobilních zařízeních.

	**Vytvoření služby na win serveru**

	**Pokud budme chtít  oba scripty aby běželi jako služba na serveru po startu ve  we win a nemuseli jsme je spouštět ručne:**
		
	**Postup pro vytvoření služby na Windows**
	
1. **Vytvoření spouštěcího skriptu**

    Vytvořte .bat soubor, který aktivuje virtuální prostředí a spustí skripty.

	**Obsah souboru run_main.bat:**

```@echo off
cd /d C:\Tepelka\PowerWorldTuya
call venv\Scripts\activate
python main.py

```

	**Obsah souboru run_app.bat:**

```@echo off
cd /d C:\Tepelka\PowerWorldTuya\Rozhrani
call ..\venv\Scripts\activate
python app.py
```



2. **Vytvoření služby pomocí nssm**

    *Stažení nssm:*
        Stáhněte Non-Sucking Service Manager (nssm) z oficiálního webu.

  **Instalace služby pro main.py:**
        Otevřete terminál (PowerShell nebo CMD) jako správce.
        Spusťte příkaz:
```
nssm install TepelkaMain
```

V zobrazeném dialogu nastavte:

    Path: Cesta k souboru run_main.bat.
    Startup directory: Adresář projektu (např. C:\Tepelka\PowerWorldTuya).
	
	
	**Instalace služby pro app.py:**

    Spusťte příkaz:
```
    nssm install TepelkaApp
```
    Nastavte podobně jako u main.py:
        Path: Cesta k souboru run_app.bat.
        Startup directory: Adresář projektu (např. C:\Tepelka\PowerWorldTuya\Rozhrani).

Spuštění služeb:

    Po instalaci spusťte služby:
```
nssm start TepelkaMain
```

```
nssm start TepelkaApp
```



3. **Alternativa: Použití sc příkazu (bez nssm)**
	**Registrace služby:**

    Vytvořte skript .bat (např. **run_all.bat**) se spouštěním obou skriptů:

```@echo off
start cmd /k "cd /d C:\Tepelka\PowerWorldTuya && call venv\Scripts\activate && python main.py"
start cmd /k "cd /d C:\Tepelka\PowerWorldTuya\Rozhrani && call ..\venv\Scripts\activate && python app.py"
```

**Vytvořte službu:**

```sc create Tepelka binPath= "cmd /c C:\cesta\k\run_all.bat" start= auto
```

Spusťte službu:
```
    sc start Tepelka
```

4. **Další kroky**

    Ověřte, že služby běží správně:

```sc query TepelkaMain
```
```sc query TepelkaApp
```

Pro ukončení služeb použijte:
```
nssm stop TepelkaMain
```
```
nssm stop TepelkaApp
```


5. 	**Další možnost přidání služby přímo v oknech WIN **


	

---


Pro další informace nebo podporu kontaktujte správce projektu.

