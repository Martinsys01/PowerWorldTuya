import os
from dotenv import load_dotenv

# Načtení proměnných z .env
load_dotenv()

# Připojení na InfluxDB
INFLUXDB_URL = os.getenv("INFLUXDB_URL", "http://localhost:8086/")
INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN", "default_token")
INFLUXDB_ORG = os.getenv("INFLUXDB_ORG", "default_org")
INFLUXDB_BUCKET = os.getenv("INFLUXDB_BUCKET", "default_bucket")
