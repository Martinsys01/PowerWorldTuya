import json
import os


from dotenv import load_dotenv

# Načítání environmentálních proměnných
load_dotenv()

class TuyaConfig:
    API_KEY = os.getenv("TUYA_API_KEY", "")
    API_SECRET = os.getenv("TUYA_API_SECRET", "")
    API_REGION = os.getenv("TUYA_API_REGION", "eu")

    PUMP1_NAME = os.getenv("PUMP1_NAME", "Tepelko 1 L")
    PUMP2_NAME = os.getenv("PUMP2_NAME", "Tepelko 2 P")

    @classmethod
    def load_config(cls):
        """Zajištění, že konfigurace obsahuje všechny potřebné údaje."""
        missing_keys = []
        if not cls.API_KEY:
            missing_keys.append("TUYA_API_KEY")
        if not cls.API_SECRET:
            missing_keys.append("TUYA_API_SECRET")
        if not cls.API_REGION:
            missing_keys.append("TUYA_API_REGION")
        if not cls.PUMP1_NAME:
            missing_keys.append("TUYA_PUMP1_NAME")
        if not cls.PUMP2_NAME:
            missing_keys.append("TUYA_PUMP2_NAME")    
        
        if missing_keys:
            raise ValueError(f"Chybí následující klíče v konfiguraci Tuya API: {', '.join(missing_keys)}")
        
        return True  # Vše je v pořádku
    @classmethod
    def get_config_dict(cls):
        return {
            'apiKey': cls.API_KEY,
            'apiSecret': cls.API_SECRET,
            'apiRegion': cls.API_REGION,
            "pump1_name": cls.PUMP1_NAME,
            "pump2_name": cls.PUMP2_NAME
        }