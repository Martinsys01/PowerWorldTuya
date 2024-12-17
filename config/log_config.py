import logging
import os
from logging.handlers import RotatingFileHandler

# Nastavení cesty k log souboru
LOG_FILE = os.path.join(os.path.dirname(__file__), "../Log/tepelka_main.log")  # Relativní cesta

def setup_logging(debug_mode, max_log_size=5*1024*1024, backup_count=3):
    """
    Nastavení logování s rotací souborů.
    
    :param debug_mode: Zapnutí/vypnutí debug režimu
    :param max_log_size: Maximální velikost log souboru v bytech (default: 5 MB)
    :param backup_count: Počet záložních kopií (default: 3)
    """
    # Zajištění existence složky Log
    log_dir = os.path.dirname(LOG_FILE) or "."
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Odstranění stávajících handlerů
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # Vytvoření rotujícího file handleru
    file_handler = RotatingFileHandler(LOG_FILE, maxBytes=max_log_size, backupCount=backup_count, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG if debug_mode else logging.INFO)
    
    # Stream handler pro konzoli
    stream_handler = logging.StreamHandler() if debug_mode else None

    handlers = [file_handler]
    if stream_handler:
        handlers.append(stream_handler)

    # Nastavení loggeru
    logging.basicConfig(
        level=logging.DEBUG if debug_mode else logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=handlers
    )
    logging.info("Logování bylo nastaveno.")

