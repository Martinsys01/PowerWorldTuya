from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from typing import Dict, Any, List
from datetime import datetime
from retrying import retry
from influxdb_client.client.query_api import QueryApi  # Nový import
# from services.debug_utils import debug_log

from config.log_config import setup_logging
import logging
from config.parameter_mappings import (
    PARAMETER_GROUPS,
    PARAMETER_GROUPS_CODES,  # přidejte tento import, protože ho používáte v create_points
)
from config.debug_config import DEBUG_MODE  # Import globální konfigurace debug módu

# Inicializace logování
setup_logging(DEBUG_MODE)

# Testovací zprávy
logging.info("Inicializace measurements.py")

class InfluxDBWriter:
    def __init__(self, url: str, token: str, org: str, bucket: str):
        """
        Inicializace InfluxDB klienta

        Args:
            url: URL adresa InfluxDB serveru
            token: Autentizační token
            org: Název organizace
            bucket: Název bucketu pro ukládání dat
        """
        
        self.client = InfluxDBClient(url=url, token=token, org=org)

        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.query_api = self.client.query_api()  # Nový řádek
        self.bucket = bucket
        self.org = org
        self.debug = DEBUG_MODE  # Použití globálního debug módu

    

    def create_points(self, data: Dict[str, Any], device_id: str, device_name: str) -> List[Point]:
        """
        Vytvoření bodů pro zápis do InfluxDB

        Args:
            data: Slovník dat k zápisu ve formátu {'basic_status': {...}, 'decoded_parameters': {...}}
            device_id: ID zařízení

        Returns:
            List bodů pro zápis do InfluxDB
        """
        points = []
        timestamp = datetime.utcnow()
        
        # Zpracování basic_status
        if 'basic_status' in data:
            for param_name, value in data['basic_status'].items():
                try:
                    point = (
                        Point("heat_pump_basic_status")
                        .tag("device_id", device_id)
                        .tag("device_name", device_name)  # Přidání jména zařízení jako tag
                        .tag("parameter", param_name)
                    )
                    
                    if isinstance(value, (int, float)):
                        point.field("value", float(value))
                    else:
                        point.field("value_str", str(value))
                    
                    point.time(timestamp)
                    points.append(point)
                except Exception as e:
                    print(f"Error creating point for basic_status {param_name}: {e}")
           

        # Zpracování decoded_parameters
        if 'decoded_parameters' in data:
            for param_name, value in data['decoded_parameters'].items():
                try:
                    point = (
                        Point("heat_pump_decoded_parameters")
                        .tag("device_id", device_id)
                        .tag("device_name", device_name)  # Přidání jména zařízení jako tag
                        .tag("parameter", param_name)
                    )
                    
                    # Pokud je hodnota string s číslem a jednotkou (např. "70°C")
                    if isinstance(value, str):
                        # Extrahujeme číselnou hodnotu
                        numeric_str = ''.join(filter(lambda x: x.isdigit() or x in ['.', '-'], value))
                        if numeric_str:
                            try:
                                numeric_value = float(numeric_str)
                                point.field("value", numeric_value)
                            except ValueError:
                                pass
                        point.field("value_str", value)
                    elif isinstance(value, (int, float)):
                        point.field("value", float(value))
                    else:
                        point.field("value_str", str(value))
                    
                    point.time(timestamp)
                    points.append(point)
                except Exception as e:
                    logging.error(f"Error creating point for decoded_parameter {param_name}: {e}")

        return points


    


     
     
    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    def write_data(self, data: Dict[str, Any], device_id: str, device_name: str):
        print("Zapisuji data",device_id)
        """
        Zápis dat do InfluxDB

        Args:
            data: Data k zápisu ve formátu {'basic_status': {...}, 'decoded_parameters': {...}}
            device_id: ID zařízení
            device_name: Jméno zařízení
        """
        try:
            logging.debug(f"\nAttempting to write data for device {device_id} ({device_name})")  # Debug log
            points = self.create_points(data, device_id, device_name)
            if points:
                self.write_api.write(bucket=self.bucket, org=self.org, record=points)
                logging.debug(f"Successfully wrote {len(points)} points to InfluxDB")  # Debug log
            else:
                logging.warning("[WARNING] No points created from data")  # Debug log
        except Exception as e:
            logging.error(f"Error writing to InfluxDB for {device_name}: {e}", level="ERROR")
            raise

    def check_data(self):
        """
        Kontrolní funkce pro zobrazení posledních dat uložených v InfluxDB
        """
        logging.debug("\nChecking recent data in InfluxDB...")
        query = f'''
        from(bucket: "{self.bucket}")
            |> range(start: -1h)
            |> filter(fn: (r) => r["_measurement"] == "heat_pump_basic_status" or r["_measurement"] == "heat_pump_decoded_parameters")
        '''
        
        try:
            result = self.query_api.query(query=query, org=self.org)
            
            if not result:
                logging.debug("No data found in the last hour")
                return

            data_count = 0
            for table in result:
                for record in table.records:
                    data_count += 1
                    print("\nRecord:")
                    print(f"Measurement: {record.get_measurement()}")
                    print(f"Field: {record.get_field()}")
                    print(f"Value: {record.get_value()}")
                    print(f"Time: {record.get_time()}")
                    print(f"Tags: {record.values}")
                    print("---")
                    
                    # Omezení výpisu na prvních 10 záznamů
                    if data_count >= 10:
                        logging.debug("\nShowing only first 10 records...")
                        return
                        
        except Exception as e:
            logging.error(f"Error checking data: {e}")
    
    
    
    def validate_data(self, data: Dict[str, Any]) -> bool:
        """
        Validace vstupních dat

        Args:
            data: Data k validaci ve formátu slovníku s parametry zařízení

        Returns:
            bool: True pokud jsou data validní
        """
        try:
            # Kontrola, zda je vstup slovník
            if not isinstance(data, dict):
                logging.error(f"Invalid data format: expected dict, got {type(data)}")
                return False

            # Kontrola základní struktury dat
            required_keys = {'basic_status', 'parameters', 'decoded_parameters'}
            if not any(key in data for key in required_keys):
                logging.error(f"Missing required keys. Expected at least one of {required_keys}")
                return False

            # Kontrola parametrů, pokud existují
            if 'parameters' in data:
                for param_name, param_value in data['parameters'].items():
                    # Zde můžete přidat specifickou validaci parametrů podle potřeby
                    if param_value is None:
                        logging.error(f"Parameter {param_name} has None value")
                        continue

            # Kontrola basic_status, pokud existuje
            if 'basic_status' in data:
                if not isinstance(data['basic_status'], dict):
                    logging.error("Invalid basic_status format")
                    return False

            # Kontrola decoded_parameters, pokud existují
            if 'decoded_parameters' in data:
                if not isinstance(data['decoded_parameters'], dict):
                    logging.error("Invalid decoded_parameters format")
                    return False

            return True

        except Exception as e:
            logging.error(f"Error during data validation: {e}")
            return False

    def close(self):
        """Uzavření spojení s InfluxDB"""
        self.client.close()
