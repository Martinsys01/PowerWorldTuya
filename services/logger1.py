import logging
from logging.handlers import RotatingFileHandler

def setup_logger(name, log_file='debug.log', level=logging.DEBUG):
    """Funkce pro nastavení loggeru pro různé soubory"""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Nastavení rotujícího log souboru
    handler = RotatingFileHandler(log_file, maxBytes=2000, backupCount=3)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    return logger

# Pokud chcete vytvořit globální logger pro aplikaci, můžete jej nastavit takto:
main_logger = setup_logger('main_logger')
