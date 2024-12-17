import os
from dotenv import load_dotenv
###!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
###POZOR KONFIGURACE BYLA PŘESUNUTA DO ".env"  V TOMTO SOUBORU NIC NEMĚNIT!!!!!!	   
###!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# Načítání environmentálních proměnných
load_dotenv()


# Načtení hodnot z .env
INFLUXDB_URL = os.getenv('INFLUXDB_URL')
INFLUXDB_TOKEN = os.getenv('INFLUXDB_TOKEN')
INFLUXDB_ORG = os.getenv('INFLUXDB_ORG')
INFLUXDB_BUCKET = os.getenv('INFLUXDB_BUCKET')

# Ověření, zda byly všechny proměnné načteny
if not all([INFLUXDB_URL, INFLUXDB_TOKEN, INFLUXDB_ORG, INFLUXDB_BUCKET]):
    raise ValueError("Chybí jedna nebo více proměnných pro konfiguraci InfluxDB v souboru .env.")

# Konfigurace InfluxDB
INFLUXDB_CONFIG = {
    'url': INFLUXDB_URL,
    'token': INFLUXDB_TOKEN,
    'org': INFLUXDB_ORG,
    'bucket': INFLUXDB_BUCKET,
}