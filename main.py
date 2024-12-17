from config.tuya_config import TuyaConfig
from config.pump_config import HeatPumpParameters
from services.tuya_connection import TuyaConnection
from services.pump_control import PumpControl
from main_v2 import process_pump_data
import time
from config.debug_config import DEBUG_MODE
# from services.debug_utils import debug_log
from config.log_config import setup_logging
import logging
import os 
from dotenv import load_dotenv




# Inicializace logování
setup_logging(DEBUG_MODE)

# Zjistit aktuální pracovní adresář
logging.debug(f"Aktuální pracovní složka: {os.getcwd()}")

# Načtení .env
load_dotenv()

# Zjistit, zda byly proměnné načteny
logging.debug(f"INFLUXDB_URL: {os.getenv('INFLUXDB_URL')}")

def check_env():
    # Zkontrolujeme, zda .env soubor existuje
    if not os.path.exists(".env"):
        raise FileNotFoundError(
            "Soubor .env nebyl nalezen. Vytvořte ho podle šablony .env.template a vyplňte potřebné údaje."
        )

    # Načtení proměnných z .env souboru
    load_dotenv()

    # Kontrola, zda všechny potřebné proměnné existují
    required_vars = ["TUYA_API_KEY", "TUYA_API_SECRET", "TUYA_API_REGION", 
                     "INFLUXDB_URL", "INFLUXDB_TOKEN", "INFLUXDB_ORG", "INFLUXDB_BUCKET", "PUMP1_DEVICE_ID", "PUMP2_DEVICE_ID"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        raise EnvironmentError(
            f"Některé požadované proměnné nejsou nastaveny v .env souboru: {', '.join(missing_vars)}"
        )



def create_tuya_connection(config):
    """Vytvoření připojení k Tuya API."""

    return TuyaConnection(
        api_key=config.API_KEY,
        api_secret=config.API_SECRET,
        api_region=config.API_REGION
    )

def main():
    try:
        # Načtení konfigurace
        logging.info("Načítám Tuya konfiguraci...")
        TuyaConfig.load_config()
        logging.info("Načítám konfiguraci čerpadel...")
        HeatPumpParameters.load_config()

        # Výpis konfigurace
        logging.debug(f"Konfigurace: Pump1 Active = {HeatPumpParameters.PUMP1_ACTIVE}, "
                      f"Pump2 Active = {HeatPumpParameters.PUMP2_ACTIVE}")
        
                    
        logging.debug("\nKontrolní výpis konfigurace:")
        logging.debug(f"API Key: {TuyaConfig.API_KEY}")
        logging.debug(f"API Secret: {TuyaConfig.API_SECRET}")
        logging.debug(f"API Region: {TuyaConfig.API_REGION}")
        logging.debug(f"Pump1 ID: {HeatPumpParameters.DEVICE_ID_PUMP1}")
        logging.debug(f"Pump2 ID: {HeatPumpParameters.DEVICE_ID_PUMP2}")
        logging.debug("Načtené parametry čerpadel:")
        logging.debug(f"Pump1 ID: {HeatPumpParameters.DEVICE_ID_PUMP1}")
        logging.debug(f"Pump1 Name: {HeatPumpParameters.PUMP1_NAME}")
        logging.debug(f"Pump2 ID: {HeatPumpParameters.DEVICE_ID_PUMP2}")
        logging.debug(f"Pump2 Name: {HeatPumpParameters.PUMP2_NAME}")
        
        logging.info("Konfigurace načtena. Připravuji připojení k Tuya API...")
        # Inicializace připojení k Tuya
        tuya_connection = create_tuya_connection(TuyaConfig)
        
        # Kontrola připojení
        if not tuya_connection.connect():
            raise Exception("Nepodařilo se připojit k Tuya API")
        logging.info("Připojení k Tuya API úspěšné.")

        # Inicializace ovladačů pro čerpadla
        pumps = []  # Seznam aktivních čerpadel

        # Inicializace čerpadla 1, pokud je aktivní
        pump1_config = HeatPumpParameters.create_pump1()
        if pump1_config:
            pump1 = PumpControl(tuya_connection, pump1_config, debug=DEBUG_MODE)
            pumps.append(pump1)
            logging.info(f"Čerpadlo 1 ({pump1_config.name}) inicializováno.")

        # Inicializace čerpadla 2, pokud je aktivní
        pump2_config = HeatPumpParameters.create_pump2()
        if pump2_config:
            pump2 = PumpControl(tuya_connection, pump2_config, debug=DEBUG_MODE)
            pumps.append(pump2)
            logging.info(f"Čerpadlo 2 ({pump2_config.name}) inicializováno.")

        # Kontrola, zda je alespoň jedno čerpadlo aktivní
        if not pumps:
            logging.warning("Žádné čerpadlo není aktivní! Ukončuji program.")
            return

        logging.info("Systém je připraven. Spouštím smyčku pro sběr dat...")

        while True:
            try:
                for pump in pumps:
                    status = pump.get_status()
                    if status:
                        process_pump_data(status, pump.parameters.device_id, pump.parameters.name)
                        logging.info(f"Data čerpadla {pump.parameters.name} zpracována.")
                    else:
                        logging.warning(f"Žádná data od čerpadla {pump.parameters.name}.")

                logging.debug("Cyklus ukládání dokončen, čekám 30 sekund.")
                time.sleep(30)

            except Exception as e:
                logging.error(f"Chyba v hlavní smyčce: {e}")
                time.sleep(10)  # Při chybě čekáme kratší dobu

    except Exception as e:
        logging.critical(f"Kritická chyba: {e}")
        raise

if __name__ == "__main__":
    check_env()
    main()