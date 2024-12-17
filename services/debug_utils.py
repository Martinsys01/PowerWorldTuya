# debug_utils.py
from typing import Any

from config.debug_config import DEBUG_MODE
# DEBUG_MODE = False  # Globální proměnná, můžete ji nastavit podle potřeby

def debug_log(message: str, data: Any = None, level: str = "DEBUG"):
    """Loguje zprávu pouze pokud je DEBUG_MODE povolen."""
    if DEBUG_MODE:
        if data is not None:
            message = f"{message} {data}"
        print(f"[{level}] {message}")
