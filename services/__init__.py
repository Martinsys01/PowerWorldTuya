from .tuya_connection import TuyaConnection

class PumpControl:
    def __init__(self, parameters, debug=True):
        self.parameters = parameters
        self.connection = None
        self.debug = debug
        
        
__all__ = ['TuyaConnection', 'PumpControl']  # Přidána čárka mezi položkami
