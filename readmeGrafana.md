# Instalace a konfigurace Grafana

Tento dokument poskytuje podrobný návod k instalaci a konfiguraci Grafany pro monitorování dat z projektu Tepelka.

---

## 1. Požadavky na instalaci

Před zahájením instalace ověřte, že vaše systém splňuje následující požadavky:

- **Operační systém**: Windows 10/11, Linux, nebo macOS
- **Hardwarové požadavky**:
  - 2 CPU
  - 2 GB RAM
  - 10 GB volného diskového prostoru
- **Internetové připojení**: Pro stažení instalačních souborů a přístup k databázi

---

## 2. Instalace Grafana

### 2.1 Instalace na Windows

1. **Stažení instalátoru**:
   - Přejděte na oficiální web Grafany: [Download Grafana](https://grafana.com/grafana/download).
   - Stáhněte instalační balíček pro Windows.

2. **Instalace**:
   - Spusťte instalační soubor a postupujte podle pokynů instalačního průvodce.
   - Po dokončení instalace spusťte službu Grafana.

3. **Kontrola instalace**:
   - Otevřete PowerShell a spusťte:
     ```powershell
     grafana-server -v
     ```
   - Zobrazí se verze Grafany.

### 2.2 Instalace na Linux

1. **Stažení a instalace**:
   - Spusťte následující příkazy v terminálu:
     ```bash
     wget https://dl.grafana.com/oss/release/grafana-10.0.0.linux-amd64.tar.gz
     tar -zxvf grafana-10.0.0.linux-amd64.tar.gz
     sudo mv grafana-10.0.0 /usr/local/grafana
     ```

2. **Spuštění služby**:
   - Spusťte Grafana server:
     ```bash
     /usr/local/grafana/bin/grafana-server &
     ```

3. **Kontrola instalace**:
   - Zkontrolujte dostupnost na URL: `http://localhost:3000`.

### 2.3 Instalace na macOS

1. **Použití Homebrew**:
   - Spusťte následující příkazy:
     ```bash
     brew update
     brew install grafana
     ```

2. **Spuštění služby**:
   - Spusťte Grafana server:
     ```bash
     grafana-server &
     ```

3. **Kontrola instalace**:
   - Otevřete prohlížeč a přejděte na `http://localhost:3000`.

---

## 3. Počáteční konfigurace

### 3.1 První spuštění

1. **Přihlášení**:
   - Při prvním spuštění použijte následující přihlašovací údaje:
     - **Uživatelské jméno**: `admin`
     - **Heslo**: `admin`
   - Po přihlášení budete vyzváni ke změně hesla.

2. **Vytvoření organizace**:
   - Přejděte do sekce **Configuration** > **Organizations** a vytvořte novou organizaci, např. `Tepelka`.

### 3.2 Přidání datového zdroje

1. **Připojení k InfluxDB**:
   - Přejděte do sekce **Configuration** > **Data Sources** > **Add Data Source**.
   - Vyberte **InfluxDB**.
   - Vyplňte následující údaje:
     - **URL**: `http://localhost:8086`
     - **Token**: Token vytvořený v InfluxDB
     - **Organization**: Např. `MARSYS`
     - **Bucket**: Např. `heat_pump`

2. **Test připojení**:
   - Klikněte na **Save & Test**.
   - Pokud je konfigurace správná, zobrazí se zpráva o úspěchu.

### 3.3 Vytvoření dashboardu

1. **Nový dashboard**:
   - Přejděte do sekce **Dashboards** > **New Dashboard**.
   - Klikněte na **Add a New Panel**.

2. **Konfigurace grafu**:
   - Vyberte datový zdroj (InfluxDB).
   - Napište dotaz v jazyce Flux pro zobrazení dat, např.:
     ```flux
     from(bucket: "heat_pump")
       |> range(start: -1h)
       |> filter(fn: (r) => r["device_name"] == "Tepelko 1 L")
     ```

3. **Přizpůsobení vizualizace**:
   - Zvolte typ grafu (např. čarový graf, sloupcový graf apod.).
   - Nastavte osy, barvy a další vizuální vlastnosti.

4. **Použití Script Editoru**:
   - Po vytvoření dotazu přejděte na záložku **Script Editor**.
   - Skript můžete zkopírovat a upravit přímo zde.
   - Tento editor umožňuje pokročilé ladění dotazů a kopírování přesného kódu dotazu.

5. **Uložení dashboardu**:
   - Klikněte na **Save Dashboard** a zadejte název.

---

## 4. Řešení potíží

### 4.1 Grafana není dostupná
- Zkontrolujte, zda je služba Grafana spuštěna.
- Otestujte dostupnost na URL pomocí prohlížeče nebo curl:
  ```bash
  curl http://localhost:3000
  ```

### 4.2 Chyba při připojení k InfluxDB
- Ořevěřte, zda je URL, token, organizace a bucket správně nastaveny.
- Zkontrolujte, zda je služba InfluxDB spuštěna.

---

## 5. Další zdroje

- [Oficiální dokumentace Grafana](https://grafana.com/docs/)
- [Oficiální dokumentace InfluxDB](https://docs.influxdata.com/)

Tento dokument pokrývá instalaci a konfiguraci Grafany pro použití v projektu Tepelka. Pokud potřebujete další pomoc, obraťte se na správce projektu.

