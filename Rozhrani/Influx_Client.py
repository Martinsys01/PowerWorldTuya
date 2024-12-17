from influxdb_client import InfluxDBClient
from config.config import INFLUXDB_URL, INFLUXDB_TOKEN, INFLUXDB_ORG

def get_influx_client():
    """Vytvoří a vrátí připojení k InfluxDB."""
    return InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)

def query_influx(query):
    """
    Provede dotaz na InfluxDB a vrátí výsledky.

    Args:
        query (str): Dotaz ve Flux jazyce.
    Returns:
        List: Záznamy výsledků.
    """
    client = get_influx_client()
    query_api = client.query_api()
    try:
        return query_api.query(query)
    except Exception as e:
        print(f"Chyba při dotazu na InfluxDB: {e}")
        return []
