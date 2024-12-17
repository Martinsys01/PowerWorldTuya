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

---

### **1. Stažení projektu**

1. **Stažení zdrojového kódu**:
   - Klonujte nebo stažněte projekt z [GitHub repozitáře](https://github.com/Martinsys01/PowerWorldTuya).
   - Rozbalte soubory do cílové složky, např. `C:\Tepelka`.

2. **Přesun do složky projektu**:
   - **Windows (PowerShell)**:
     ```powershell
     cd C:\Tepelka
     ```
   - **Linux (Terminál)**:
     ```bash
     cd /path/to/Tepelka
     ```

---

### **2. Vytvoření virtuálního prostředí**

Doporučujeme používat virtuální prostředí pro správu závislostí.

1. **Vytvoření virtuálního prostředí**:
   - **Windows**:
     ```powershell
     python -m venv venv
     ```
   - **Linux**:
     ```bash
     python3 -m venv venv
     ```

2. **Aktivace prostředí**:
   - **Windows**:
     ```powershell
     .\venv\Scripts\Activate
     ```
   - **Linux**:
     ```bash
     source venv/bin/activate
     ```

3. **Aktualizace pip**:
   ```bash
   pip install --upgrade pip
   ```

---

### **3. Instalace závislostí**

Nainstalujte požadované balíčky pomocí souboru `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

### **4. Konfigurace projektu**

1. **.env soubor**:
   - Vytvořte soubor `.env` ve složce projektu podle šablony `.env.template`.
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

---

### **5. Spuštění projektu**

1. **Spuštění hlavního programu**:
   - Program, který stahuje data z Tuya Cloud a ukládá je do InfluxDB:
     ```bash
     python main.py
     ```

2. **Spuštění webového rozhraní**:
   - Přesuňte se do složky `Rozhrani`:
     ```bash
     cd Rozhrani
     ```
   - Spusťte Flask aplikaci:
     ```bash
     python app.py
     ```
   - Otevřete webový prohlížeč a přejděte na:
     ```
     http://127.0.0.1:5000 (nebo IP adresi zařízení na kterém to jede)
     ```

---

## **Vizualizace**

Webové rozhraní zobrazuje aktuální měřená data z InfluxDB:
- **Tlačítka Tepelko 1 a Tepelko 2**: Přepínání mezi vizualizacemi pro jednotlivá čerpadla (aktivní dle `.env`).
- **Dynamická data**: Aktualizace hodnot každých 5 sekund.
- **Časová značka**: Zobrazuje čas posledního vzorku načteného z InfluxDB.
- **Responsivní design**: Optimalizace pro zobrazení na mobilních zařízeních.

---


Pro další informace nebo podporu kontaktujte správce projektu.

