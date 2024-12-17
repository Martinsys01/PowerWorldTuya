from typing import Any

def validate_temperature(value: Any) -> bool:
    """Validace teplotních hodnot"""
    return isinstance(value, (int, float)) and -50 <= value <= 100

def validate_pressure(value: Any) -> bool:
    """Validace tlakových hodnot"""
    return isinstance(value, (int, float)) and 0 <= value <= 50

def validate_boolean(value: Any) -> bool:
    """Validace boolean hodnot"""
    return isinstance(value, (int, bool)) and value in (0, 1, True, False)

def validate_any(value: Any) -> bool:
    """Obecná validace - přijme jakoukoliv hodnotu"""
    return True

# Mapování validačních funkcí na skupiny parametrů
VALIDATION_FUNCTIONS = {
    1: validate_temperature,  # pro skupinu teplotních čidel
    2: validate_pressure,     # pro skupinu tlakových čidel
    3: validate_boolean,      # pro skupinu stavových hodnot
    # Přidejte další mapování podle potřeby
}