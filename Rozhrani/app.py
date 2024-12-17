from flask import Flask, render_template, jsonify
from Influx_Client import query_influx
from config.config import INFLUXDB_BUCKET
from config.debug_config import DEBUG  # Import konfigurace debug
from flask import request
from datetime import datetime
import os


app = Flask(__name__)

# Funkce pro logování s podmínkou na základě DEBUG
def debug_log(message):
    if DEBUG:
        print(message)

@app.before_request
def log_request_info():
    debug_log(f"Request Method: {request.method}")
    debug_log(f"Request Path: {request.path}")
    debug_log(f"Request Headers: {request.headers}")

@app.errorhandler(404)
def page_not_found(e):
    debug_log(f"404 Error: Path {request.path} was requested.")
    return jsonify({"error": "Endpoint not found"}), 404


@app.route('/')
def index():
    pump1_active = os.getenv('PUMP1_ACTIVE', 'false').lower() == 'true'
    pump2_active = os.getenv('PUMP2_ACTIVE', 'false').lower() == 'true'

    # Nastavení výchozího endpointu
    endpoint = "/data/tepelko1" if pump1_active else "/data/tepelko2" if pump2_active else None

    if not endpoint:
        return render_template(
            'index.html',
            pump1_active=pump1_active,
            pump2_active=pump2_active,
            error="Žádné čerpadlo není aktivní. Zkontrolujte nastavení.",
        )
    
    return render_template(
        'index.html',
        pump1_active=pump1_active,
        pump2_active=pump2_active,
        endpoint=endpoint,
    )

    # Předání stavů čerpadel do šablony
    return render_template('index.html', pump1_active=pump1_active, pump2_active=pump2_active)

@app.route('/tepelko1')
def index_tepelko1():
    return render_template('index.html', device_name="Tepelko 1 L", endpoint="/data/tepelko1")

@app.route('/tepelko2')
def index_tepelko2():
    pump1_active = os.getenv('PUMP1_ACTIVE', 'false').lower() == 'true'
    pump2_active = os.getenv('PUMP2_ACTIVE', 'false').lower() == 'true'

    return render_template(
        'index.html',
        pump1_active=pump1_active,
        pump2_active=pump2_active,
        device_name="Tepelko 2 P",
        endpoint="/data/tepelko2"
    )


@app.route('/data/tepelko1', methods=['GET'])
def get_data_tepelko1():
    return fetch_data_from_influx("Tepelko 1 L")

@app.route('/data/tepelko2', methods=['GET'])
def get_data_tepelko2():
    return fetch_data_from_influx("Tepelko 2 P")

    #Seznam požadovaných hodnot k zobrazení dále je definujeme v index.html
    #Další prměnné paramtry k zobrazení přidáme se  s a za předposlední dáme or
def fetch_data_from_influx(device_name):
    query = f'''
    from(bucket: "{INFLUXDB_BUCKET}")
      |> range(start: -1h)
      |> filter(fn: (r) => r["device_name"] == "{device_name}")
      |> filter(fn: (r) => 
          r["parameter"] == "Teplota chladiva před kompresorem" or 
          r["parameter"] == "Teplota chladiva za kompresorem" or
          r["parameter"] == "Teplota výparníku" or 
          r["parameter"] == "Teplota venkovní" or
          r["parameter"] == "Otáčky ventilátoru 1" or 
          r["parameter"] == "Otáčky ventilátoru 2" or 
          r["parameter"] == "Frekvence kompresoru" or 
          r["parameter"] == "Otevření hlavního exp. ventilu" or 
          r["parameter"] == "Otevření vedlejšího exp. ventilu" or 
          r["parameter"] == "Teplota přívodu" or 
          r["parameter"] == "Teplota zpátečky" or 
          r["parameter"] == "Teplota zásobníku TUV" or 
          r["parameter"] == "Teplota chladící cívky" or 
          r["parameter"] == "Teplota chladiče" or 
          r["parameter"] == "power" or 
          r["parameter"] == "Proud kompresoru" or 
          r["parameter"] == "Proud celého zařízení" or
          r["parameter"] == "Výkon vytápění/chlazení" or
          r["parameter"] == "COP" or
          r["parameter"] == "Aktuální rychlost čerpadla" 
          
      )
    '''
    debug_log(f"Query for device {device_name}: {query}")
    result = query_influx(query)
    debug_log(f"Result for device {device_name}: {result}")
    
    latest_timestamp = None  # Explicitní inicializace
    data = {}
    for table in result:
        for record in table.records:
            parameter = record.values["parameter"]
            value = record.get_value()
            data[parameter] = value
    
    # Získání posledního časového razítka
            record_time = record.get_time()
            if latest_timestamp is None or record_time > latest_timestamp:
                latest_timestamp = record_time

    # Přidání časové značky do odpovědi
    if latest_timestamp:
        data['timestamp'] = latest_timestamp.isoformat()

    return jsonify(data)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=DEBUG)
