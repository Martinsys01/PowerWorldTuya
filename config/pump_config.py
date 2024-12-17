import json
import os
from config.debug_config import DEBUG_MODE  # Načítáme DEBUG_MODE
# from services.debug_utils import debug_log
from config.log_config import setup_logging
import logging
from dotenv import load_dotenv

# Načtení proměnných z .env souboru
load_dotenv()

# Inicializace logování
setup_logging(DEBUG_MODE)

# Testovací zprávy
logging.info("Inicializace pump_config.py")


class HeatPumpParameters:
    DEVICE_ID_PUMP1 = os.getenv("PUMP1_DEVICE_ID", None)
    PUMP1_NAME = os.getenv("PUMP1_NAME", "Tepelko 1 L")
    PUMP1_ACTIVE = os.getenv("PUMP1_ACTIVE", "false").strip().lower() == "true"

    DEVICE_ID_PUMP2 = os.getenv("PUMP2_DEVICE_ID", None)
    PUMP2_NAME = os.getenv("PUMP2_NAME", "Tepelko 2 P")
    PUMP2_ACTIVE = os.getenv("PUMP2_ACTIVE", "false").strip().lower() == "true"

    debug = DEBUG_MODE  # Použití globálního debug režimu

    @classmethod
    def load_config(cls):
        try:
            logging.debug(f"Konfigurace načtena z .env souboru:")
            logging.debug(f"Pump1 Device ID: {cls.DEVICE_ID_PUMP1}")
            logging.debug(f"Pump1 Name: {cls.PUMP1_NAME}")
            logging.debug(f"Pump1 Active: {cls.PUMP1_ACTIVE}")
            logging.debug(f"Pump2 Device ID: {cls.DEVICE_ID_PUMP2}")
            logging.debug(f"Pump2 Name: {cls.PUMP2_NAME}")
            logging.debug(f"Pump2 Active: {cls.PUMP2_ACTIVE}")

            logging.info(f"Čerpadlo 1: {cls.PUMP1_NAME} (Aktivní: {cls.PUMP1_ACTIVE})")
            logging.info(f"Čerpadlo 2: {cls.PUMP2_NAME} (Aktivní: {cls.PUMP2_ACTIVE})")
        except Exception as e:
            logging.error(f"Chyba při načítání konfigurace čerpadel: {str(e)}")
            raise

    @classmethod
    def create_pump1(cls):
        """Vytvoří instanci pro čerpadlo 1, pokud je aktivní."""
        if cls.PUMP1_ACTIVE and cls.DEVICE_ID_PUMP1:
            return cls(cls.DEVICE_ID_PUMP1, cls.PUMP1_NAME)
        logging.warning("Čerpadlo 1 není aktivní nebo nemá přiřazené DEVICE_ID.")
        return None

    @classmethod
    def create_pump2(cls):
        """Vytvoří instanci pro čerpadlo 2, pokud je aktivní."""
        if cls.PUMP2_ACTIVE and cls.DEVICE_ID_PUMP2:
            return cls(cls.DEVICE_ID_PUMP2, cls.PUMP2_NAME)
        logging.warning("Čerpadlo 2 není aktivní nebo nemá přiřazené DEVICE_ID.")
        return None

    def __init__(self, device_id, name):
        self.device_id = device_id
        self.name = name
