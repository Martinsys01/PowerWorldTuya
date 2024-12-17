# Příručka: Vytvoření účtu na Tuya Cloudu a konfigurace zařízení

Tento dokument popisuje kroky potřebné pro vytvoření developerského účtu na Tuya Cloudu, přidání zařízení pomocí mobilní aplikace, přidání potřebných služeb a získání ID zařízení a přístupového tokenu.

---

## 1. Vytvoření developerského účtu na Tuya Cloudu

### Krok 1.1: Registrace na Tuya IoT Platform
1. Přejděte na [Tuya IoT Platform](https://iot.tuya.com/).
2. Klikněte na tlačítko **Sign Up**.
3. Vyplňte:
   - Emailovou adresu
   - Heslo
   - Potvrďte ověřovací kód, který obdržíte na email.
4. Dokončete registraci a přihlaste se do účtu.

### Krok 1.2: Nastavení developerského účtu
1. Po přihlášení na IoT Platform klikněte na **Cloud Development**.
2. Zvolte **Create Cloud Project**.
   - Vyplňte název projektu (např. "HeatPumpIntegration").
   - Vyberte příslušný region (např. **Central Europe**, pokud jste v Evropě).
   - Zaškrtněte služby, které budete používat (např. **Smart Home** a **Device Status Notification**).
3. Klikněte na **Create**.

---

## 2. Přidání zařízení pomocí mobilní aplikace Tuya

### Krok 2.1: Stažení aplikace
1. Stáhněte si mobilní aplikaci Tuya Smart nebo Smart Life z obchodu Google Play nebo Apple App Store.

### Krok 2.2: Přihlášení do aplikace
1. Spusťte aplikaci a přihlaste se stejnými přístupovými účty jako na Tuya IoT Platform.

### Krok 2.3: Přidání zařízení
1. V aplikaci klikněte na **+** (Add Device).
2. Postupujte podle instrukcí pro přidání zařízení (např. připojení k Wi-Fi, spárování).
3. Po úspěšném přidání zařízení ověřte, zda je zařízení viditelé v aplikaci.

---

## 3. Autorizace zařízení v Tuya IoT Platform

### Krok 3.1: Vazba aplikace na IoT Platform
1. Na IoT Platform přejděte na **Cloud Development** > **Projects**.
2. Klikněte na svůj projekt.
3. Přejděte na záložku **Link Devices** > **Link Tuya App Account**.
4. Vygenerujte QR kód a naskenujte ho pomocí mobilní aplikace Tuya Smart.

### Krok 3.2: Připojená zařízení
1. Po vazbě budou všechna zařízení z aplikace automaticky přenesena na IoT Platform.
2. Otevřete sekci **Devices** a ověřte, že zařízení jsou viditelná.

---

## 4. Přidání služby Core +

### Krok 4.1: Aktivace Core +
1. Na IoT Platform přejděte na **Cloud Development** > **Service Management**.
2. Vyhledejte službu **Core +**.
3. Klikněte na **Subscribe**.

---

## 5. Získání ID zařízení a tokenu

### Krok 5.1: Získání Device ID
1. Na IoT Platform přejděte do sekce **Devices**.
2. Vyberte zařízení.
3. Zkopírujte **Device ID** z detailu zařízení.

### Krok 5.2: Generování přístupového tokenu
1. Přejděte na záložku **API Explorer**.
2. Vyberte API, které potřebujete (např. **Get Device Details**).
3. Vygenerujte token pomocí **Authorize** tlačítka.
4. Zkopírujte token pro další použití.

---

## 6. Poznámky
- Zkontrolujte, že je váš projekt správně propojen s aplikací a zařízení jsou autorizována.
- Udržujte svůj API klíč a tajný klíč v bezpečí.

---
Tento dokument poskytuje detailní návod pro vytvoření a konfiguraci účtu na Tuya IoT Platformě a propojení zařízení.

