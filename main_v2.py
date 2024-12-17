from services.measurements import InfluxDBWriter
from services.data_processor import HeatPumpDataProcessor
from config.influxdb_config import INFLUXDB_CONFIG
from config.debug_config import DEBUG_MODE
# from services.debug_utils import debug_log, DEBUG_MODE
from config.log_config import setup_logging
import logging


setup_logging(DEBUG_MODE)

def process_pump_data(pump_data, device_id, device_name):
    """
    Zpracování dat z čerpadla a zápis do InfluxDB
    
    Args:
        pump_data (dict): Data z čerpadla
        device_id (Any): Identifikátor čerpadla (bude převeden na string)
        device_name (str): Jméno zařízení
    """
    # Převedení device_id na string
    device_id = str(device_id)
    
    processor = HeatPumpDataProcessor()
    writer = InfluxDBWriter(
        url=INFLUXDB_CONFIG['url'],
        token=INFLUXDB_CONFIG['token'],
        org=INFLUXDB_CONFIG['org'],
        bucket=INFLUXDB_CONFIG['bucket']
    )
    
    try:
        success, processed_data = processor.process_data(pump_data)
        if success:
            writer.write_data(processed_data, device_id=device_id, device_name=device_name)
            logging.info(f"Data byla úspěšně zpracována a zapsána pro zařízení {device_id} ({device_name})")
    except Exception as e:
        logging.error(f"Error processing/writing pump data: {e}", level="ERROR")
    finally:
        writer.close()
        # Zkontrolujte, zda `processed_data` má hodnotu, než ji použijete
        if processed_data is not None:
            logging.debug(f"data u čerpadel {device_name}: {processed_data}")
        else:
            logging.warning("Žádná data nebyla zpracována.")
        


def test_run():
    """Testovací funkce pro ověření základní funkcionality"""
    logging.debug("=== Starting Test Run ===")

    # Test data
    test_data = {
        1: {  # Temperatures
            0: 22.5,  # Outside temp
            1: 45.0,  # Flow temp
        },
        2: {  # Pressures
            0: 25.5,  # High pressure
        },
        23: {  # Performance
            0: 4.2,   # COP
        }
    }

    logging.debug("\nTest data:")
    logging.debug(test_data)

    # Inicializace komponent
    processor = HeatPumpDataProcessor()
    
    # Test zpracování dat
    logging.debug("\nProcessing data...")
    success, processed_data = processor.process_data(test_data)
    
    logging.debug(f"Processing success: {success}")
    logging.debug("Processed data:")
    logging.debug(processed_data)

    if success:
        logging.debug("\nFormatted structure:")
        structured_data = processor.get_formatted_structure()
        logging.debug(structured_data)

        # Test zápisu do InfluxDB
        logging.debug("\nTrying to write to InfluxDB...")
        writer = InfluxDBWriter(
            url=INFLUXDB_CONFIG['url'],
            token=INFLUXDB_CONFIG['token'],
            org=INFLUXDB_CONFIG['org'],
            bucket=INFLUXDB_CONFIG['bucket']
        )
        try:
            writer.write_data(processed_data, device_id="heat_pump_test")
            logging.debug("Data successfully written to InfluxDB")
        except Exception as e:
            logging.debug(f"Error writing to InfluxDB: {e}")
        finally:
            writer.close()

    logging.debug("\n=== Test Run Completed ===")

    if __name__ == "__main__":
         test_run()