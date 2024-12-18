# Instalační příručka pro InfluxDB

## Újel a popis InfluxDB

InfluxDB je časově řadová databáze, která je ideální pro ukládání a dotazování na data monitoringu, IoT a aplikací zaměřených na analýzu časových řad. V tomto projektu slouží pro ukládání dat tepelných čerpadel.

---

## **1. Instalace InfluxDB**

### **1.1 Stažení InfluxDB**

1. Přejděte na oficiální web InfluxDB: [https://www.influxdata.com/](https://www.influxdata.com/)
2. Zvolte **Download** a vyberte verzi podle vašeho operačního systému (Windows, Linux, macOS).  verze InfluxDB v2.7.11 nebo vyšší  Platforma  Windows Bin...(64-bit)-using powershell+
   Rozbalte influxdb2-2.7.10-windows.zip  a spusťte influxd.exe. Spustí se  influx  v Powershelovém okně  - nezapomeňte že pokud  chceme ukládat data do databáze tento server musí být spuštěň 
   (spustit po startum nebo jako službu)  viz krok 1.2

---

### **1.2 Instalace na Windows**

1. Spusťte stáhnutý instalační balíček.
2. Dokončete instalaci podle pokynů instalátoru.
3. Po instalaci spusťte **InfluxDB** jako službu nebo pomocí spustitelného souboru:
   ```powershell
   influxd.exe
   ```

---

### **1.3 Instalace na Linux**

1. Pro Debian/Ubuntu:
   ```bash
   wget https://dl.influxdata.com/influxdb/releases/influxdb2_x.x.x_amd64.deb
   sudo dpkg -i influxdb2_x.x.x_amd64.deb
   ```

2. Pro CentOS/Red Hat:
   ```bash
   wget https://dl.influxdata.com/influxdb/releases/influxdb2.x.x.x.x86_64.rpm
   sudo yum localinstall influxdb2.x.x.x.x86_64.rpm
   ```

3. Spusťte službu:
   ```bash
   sudo systemctl start influxdb
   ```

4. Otestujte, že InfluxDB běží:
   ```bash
   curl http://localhost:8086/health
   ```

---

## **2. Konfigurace InfluxDB**

### **2.1 Přístup do administrace**
1. Otevřete webový prohlížeč a přejděte na adresu (server v okně PW musí být spuštěn!!):
   ```
   http://localhost:8086
   ```
   Zvolte tlačítko GET STARTED ,
2. Vytvořte administrátorský účet: Jméno uživatele   (tímto jmenem se budete do InfluxDB přihlašovat na edistaci dat 
   - Zadejte jméno firmy (např. `MARSYS`). (Tyto názvy se pak musí schodovat jako v konfiguraci)
   - Vytvořte bucket (např. `heat_pump`).(Tyto názvy se pak musí schodovat jako v konfiguraci)
   - Nastavte heslo.
		Zobrazí se hlavní MASTER token    - tento token si ulžte - již ho neuvudíte!!

---

### **2.2 Generování tokenů**

1. Přihlaste se do administrace.
2. Přejděte na sekci **Data**  v levo nahoře šipka  nahoru  a vybete > **API Tokens**.
3. Klikněte v pravo nahoře na **Generate Token**: Token může být generální na všechno, nebo užovatelský jen na určitý bucket a na určuté práva (čtení - zápis)
   - **All Access Token**: Pokud chcete jeden univerzální token.
   - **Read/Write Token**: Pokud chcete oddělit tokeny pro čtení a zápis dat.

4. Poznamenejte si vygenerovaný token, bude potřeba pro konfiguraci.

---

### **2.3 Vytvoření dalšího bucketu (volitelné)**

1. Přejděte na sekci **Data** > **Buckets**.
2. Klikněte na **Create Bucket**.
3. Vyplňte:
   - **Name**: Např. `backup_data`.
   - **Retention Period**: Nastavte podle potřeby (např. 30 dní).
   
   Tínto je InflucDB nakonfigurován a připraven 

---

## **3. Testování připojení k InfluxDB**


   ```

---

## **4. Použití v projektu Tepelka**

1. **Zadejte konfiguraci do `.env`**:
   ```dotenv
   INFLUXDB_URL=http://localhost:8086
   INFLUXDB_TOKEN=VašToken
   INFLUXDB_ORG=MARSYS
   INFLUXDB_BUCKET=heat_pump
   ```

2. Ujistěte se, že InfluxDB běží.
3. Spusťte hlavní program projektu:  Zpátky do souboru README.md
   ```bash
   python main.py
   ```

4. Pro vizualizaci spusťte webovou aplikaci:
   ```bash
   cd Rozhrani
   python app.py
   ```
   Otevřete prohlížeč a přejděte na `http://127.0.0.1:5000`.

---

## **5. Řešení častých problémů**

### Chyba při připojení k InfluxDB
- Zkontrolujte, zda služba InfluxDB běží.
- Ujistěte se, že je správně nastavená URL a token.

### Chybná data v databázi
- Zkontrolujte strukturu dotazů a vstupní data.

### Chyba čtení dat ve vizualizaci
- Otestujte, zda jsou data uložena v bucketu pomocí Influx klienta.

---

Pro další dotazy nebo podporu kontaktujte správce projektu.

