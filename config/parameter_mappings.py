from typing import Dict, Tuple, Callable, Any, Union
from dataclasses import dataclass
from enum import Enum

# Typové aliasy
ParameterFormatter = Callable[[Any], str]
ParameterMapping = Dict[int, Tuple[str, ParameterFormatter]]

# Konstanty pro jednotky
UNIT_CELSIUS = "°C"
UNIT_BAR = "bar"
UNIT_HERTZ = "Hz"
UNIT_VOLT = "V"
UNIT_AMP = "A"
UNIT_RPM = "rpm"


# Enum třídy
class DeviceState(Enum):
    ENABLED = "Povoleno"
    DISABLED = "Zakázáno"


class WorkingMode(Enum):
    HEATING = "Topení"
    COOLING = "Chlazení"
    DHW = "TUV"


# Třídy pro parametry
@dataclass
class Parameter:
    code: int
    name: str
    formatter: ParameterFormatter
    group: int
    unit: str = ""

    def format_value(self, value: Any) -> str:
        return self.formatter(value)


# Pomocné funkce
def convert_to_signed(value: int) -> int:
    """
    Převede unsigned int na signed int.

    Args:
        value: Unsigned integer hodnota

    Returns:
        Signed integer hodnota
    """
    if value > 0x7FFFFFFF:
        return value - 0x100000000
    return value


def format_temperature(value: int) -> str:
    """Formátuje teplotní hodnotu."""
    return f"{convert_to_signed(value)}{UNIT_CELSIUS}"


def format_pressure(value: int) -> str:
    """Formátuje tlakovou hodnotu."""
    return f"{value/10}{UNIT_BAR}"


def validate_parameter_code(group: int, code: int) -> bool:
    """Ověří, zda je kód parametru platný pro danou skupinu."""
    return code in PARAMETER_GROUPS.get(group, {})


def validate_parameter_value(value: Any, expected_type: type) -> bool:
    """Ověří, zda hodnota parametru odpovídá očekávanému typu."""
    return isinstance(value, expected_type)


def get_parameter_name(group: int, code: int) -> str:
    """Vrátí název parametru pro daný kód a skupinu."""
    mapping = PARAMETER_GROUPS.get(group, {})
    return mapping.get(code, ("Unknown", str))[0]


def format_parameter_value(group: int, code: int, value: Any) -> str:
    """Naformátuje hodnotu parametru podle definovaného formátování."""
    mapping = PARAMETER_GROUPS.get(group, {})
    formatter = mapping.get(code, ("Unknown", str))[1]
    return formatter(value)


# Status Parameter Group 1
STATUS_GROUP_1_MAPPING: Dict[int, Tuple[str, Callable[[Any], str]]] = {
    0: ("Teplota zpátečky", lambda x: f"{convert_to_signed(x)}°C"),
    1: ("Teplota přívodu", lambda x: f"{convert_to_signed(x)}°C"),
    2: ("Teplota venkovní", lambda x: f"{convert_to_signed(x)}°C"),
    3: ("Teplota chladiva za kompresorem", lambda x: f"{convert_to_signed(x)}°C"),
    4: ("Teplota chladiva před kompresorem", lambda x: f"{convert_to_signed(x)}°C"),
    5: ("Teplota výparníku", lambda x: f"{convert_to_signed(x)}°C"),
    6: ("Teplota chladící cívky", lambda x: f"{convert_to_signed(x)}°C"),
    7: ("Teplota zásobníku TUV", lambda x: f"{convert_to_signed(x)}°C"),
    8: ("Otevření hlavního exp. ventilu", lambda x: f"{x}P"),
    9: ("Otevření vedlejšího exp. ventilu", lambda x: f"{x}P"),
    10: ("Proud kompresoru", lambda x: f"{x}A"),
    11: ("Teplota chladiče", lambda x: f"{convert_to_signed(x)}°C"),
    12: ("Napětí DC sběrnice", lambda x: f"{x}V"),
    13: ("Frekvence kompresoru", lambda x: f"{x}Hz"),
    14: ("Otáčky ventilátoru 1", lambda x: f"{x}rpm"),
    15: ("Otáčky ventilátoru 2", lambda x: f"{x}rpm"),
    16: ("Tlak chladiva - nízký", lambda x: f"{x}bar"),
    17: ("Konverzní hodnota nízkého tlaku", lambda x: f"{convert_to_signed(x)}°C"),
    18: ("EVU signál", str),
    19: ("SG signál", str),
}

# Parametrická skupina 1
PARAM_GROUP_1_MAPPING: Dict[int, Tuple[str, Callable[[Any], str]]] = {
    0: ("Teplotní rozdíl topné vody", lambda x: f"{x}°C"),
    1: ("Teplotní rozdíl TUV", lambda x: f"{x}°C"),
    2: ("Cílová teplota TUV", lambda x: f"{x}°C"),
    3: ("Cílová teplota chlazení", lambda x: f"{x}°C"),
    4: ("Cílová teplota vytápění", lambda x: f"{x}°C"),
    5: ("Kompenzace teploty vody", lambda x: f"{x}°C"),
    6: ("Dny cyklu dezinfekce", str),
    7: ("Čas spuštění dezinfekce", lambda x: f"{x}h"),
    8: ("Délka cyklu dezinfekce", lambda x: f"{x}min"),
    9: ("Cílová teplota dezinfekce", lambda x: f"{x}°C"),
    10: ("Nastavení dezinfekce tepelným čerpadlem", lambda x: f"{x}°C"),
    11: ("Ekvitermní regulace", lambda x: "Zapnuto" if x == 1 else "Vypnuto"),
    12: ("Korekční bod teploty vytápění", lambda x: f"{x}°C"),
    13: ("Koeficient teplotní křivky", lambda x: f"{x/10}"),
    14: ("Frekvenční provoz", lambda x: "Sníženo" if x == 0 else "Nesníženo"),
    15: ("Venkovní teplota pro elektrický ohřívač", lambda x: f"{convert_to_signed(x)}°C"),
    16: ("Doba spuštění elektrického ohřevu", lambda x: f"{x}min"),
    17: ("Funkce tepelného čerpadla", lambda x: {
            1: "Topení",
            2: "Topení+Chlazení",
            3: "Topení+TUV",
            4: "Topení+Chlazení+TUV",
        }.get(x, "Neznámý"),
    ),
    18: ("Stav cirkulačního čerpadla", lambda x: {
            0: "Interval",
            1: "Vždy",
            2: "Stop po dosažení teploty"
        }.get(x, "Neznámý"),
    ),
    19: ("Cyklus cirkulačního čerpadla", lambda x: f"{x}min"),
}


# Parameter Group 2
PARAM_GROUP_2_MAPPING: Dict[int, Tuple[str, Callable[[Any], str]]] = {
    0: ("DC circulation pump mode", lambda x: {0: "Off", 1: "Auto", 2: "Manual"}.get(x, "Unknown")),
    1: ("DC circulation pump manual speed", lambda x: f"{x}%"),
    2: ("Frekvence kompresoru při odmrazení", lambda x: f"{x}Hz"),
    3: ("Interval odmrazení", lambda x: f"{x}min"),
    4: ("Teplota výparníku pro spuštění odmrazení", lambda x: f"{convert_to_signed(x)}°C"),
    5: ("Doba odmrazení", lambda x: f"{x}min"),
    6: ("Teplota výparníku pro odmrazení", lambda x: f"{x}°C"),
    7: ("Teplotní rozdíl 1 venkovního prostředí", lambda x: f"{x}°C"),
    8: ("Teplotní rozdíl 2 výparníku pro odmrazení", lambda x: f"{x}°C"),
    9: ("Venkovní teplota pro spuštění odmrazení", lambda x: f"{x}°C"),
    10: ("Frekvence 1", lambda x: f"{x}Hz"),
    11: ("Frekvence 2", lambda x: f"{x}Hz"),
    12: ("Frekvence 3", lambda x: f"{x}Hz"),
    13: ("Frekvence 4", lambda x: f"{x}Hz"),
    14: ("Frekvence 5", lambda x: f"{x}Hz"),
    15: ("Frekvence 6", lambda x: f"{x}Hz"),
    16: ("Frekvence 7", lambda x: f"{x}Hz"),
    17: ("Frekvence 8", lambda x: f"{x}Hz"),
    18: ("Frekvence 9", lambda x: f"{x}Hz"),
    19: ("Frekvence 10", lambda x: f"{x}Hz"),
}

# Parameter Group 3
PARAM_GROUP_3_MAPPING: Dict[int, Tuple[str, Callable[[Any], str]]] = {
    0: ("Frekvence 11", lambda x: f"{x}Hz"),  # 80 Hz
    1: ("Frekvence 12", lambda x: f"{x}Hz"),  # 85 Hz
    2: ("Dolní limit frekvence", lambda x: f"{x}Hz"),  # 40 Hz
    3: ("Horní limit frekvence", lambda x: f"{x}Hz"),  # 80 Hz
    4: ("Kompenzace teploty vody", lambda x: f"{convert_to_signed(x)}°C"),  # -5 °C
    5: ("Rezervováno", lambda x: f"{x}"),  # Rezervováno
    6: ("Nastavení teploty výfuku TP0", lambda x: f"{x}°C"),  # 93 °C
    7: ("Spodní limit frekvence 01", lambda x: f"{x}Hz"),  # 125 Hz
    8: ("Spodní limit frekvence 02", lambda x: f"{x}Hz"),  # 125 Hz
    9: ("Spodní limit frekvence 03", lambda x: f"{x}Hz"),  # 125 Hz
    10: ("Spodní limit frekvence 04", lambda x: f"{x}Hz"),  # 125 Hz
    11: ("Horní limit frekvence 01", lambda x: f"{x}Hz"),  # 125 Hz
    12: ("Horní limit frekvence 02", lambda x: f"{x}Hz"),  # 125 Hz
    13: ("Horní limit frekvence 03", lambda x: f"{x}Hz"),  # 125 Hz
    14: ("Horní limit frekvence 04", lambda x: f"{x}Hz"),  # 125 Hz
    15: ("Výkonná frekvence ADD", lambda x: f"{x}Hz"),  # 15 Hz
    16: ("Tichý režim max. frekvence", lambda x: f"{x}Hz"),  # 60 Hz
    17: ("Power Cooling frekvence ADD", lambda x: f"{x}Hz"),  # 10 Hz
    18: ("Tichý režim chlazení max. frekvence", lambda x: f"{x}Hz"),  # 60 Hz
    19: ("Nastavovací cyklus DC oběhové pumpy", lambda x: f"{x}s"),  # 60 s
}


# Parameter Group 4
# Parameter Group 4
PARAM_GROUP_4_MAPPING: Dict[int, Tuple[str, Callable[[Any], str]]] = {
    0: ("Maximální rychlost DC cirkulačního čerpadla", lambda x: f"{x}%"),
    1: ("Maximální rychlost DC oběhového čerpadla", lambda x: f"{x}%"),
    2: ("Nastavovací rychlost DC cirkulačního čerpadla", lambda x: f"{x}%"),
    3: ("Vstupní a výstupní teplotní rozdíl pro DC cirkulační čerpadlo", lambda x: f"{x}°C"),
    4: ("Akční perioda hlavního expanzního ventilu", lambda x: f"{x}s"),
    5: ("Hlavní expanzní ventil - topení superheat 1", lambda x: f"{x}°C"),
    6: ("Hlavní expanzní ventil - topení superheat 2", lambda x: f"{x}°C"),
    7: ("Hlavní expanzní ventil - topení superheat 3", lambda x: f"{x}°C"),
    8: ("Hlavní expanzní ventil - topení superheat 4", lambda x: f"{x}°C"),
    9: ("Hlavní expanzní ventil - topení superheat 5", lambda x: f"{x}°C"),
    10: ("Hlavní expanzní ventil - topení superheat 6", lambda x: f"{x}°C"),
    11: ("Hlavní expanzní ventil - topení superheat 7", lambda x: f"{x}°C"),
    12: ("Hlavní expanzní ventil - topení superheat 8", lambda x: f"{x}°C"),
    13: ("Hlavní expanzní ventil - chlazení superheat 1", lambda x: f"{x}°C"),
    14: ("Hlavní expanzní ventil - chlazení superheat 2", lambda x: f"{x}°C"),
    15: ("Hlavní expanzní ventil - chlazení superheat 3", lambda x: f"{x}°C"),
    16: ("Hlavní expanzní ventil - chlazení superheat 4", lambda x: f"{x}°C"),
    17: ("Nespecifikováno 1", lambda x: f"{x}Hz"),
    18: ("Nespecifikováno 2", lambda x: f"{x}Hz"),
    19: ("Nespecifikováno 3", lambda x: f"{x}Hz"),
}


# Parameter Group 5
# Skupina parametrů 5 (neznámé parametry)
PARAM_GROUP_5_MAPPING: Dict[int, Tuple[str, Callable[[Any], str]]] = {
    0: ("Neznámý parametr G5_0", str),
    1: ("Neznámý parametr G5_1", str),
    2: ("Neznámý parametr G5_2", str),
    3: ("Neznámý parametr G5_3", str),
    4: ("Neznámý parametr G5_4", str),
    5: ("Neznámý parametr G5_5", str),
    6: ("Neznámý parametr G5_6", str),
    7: ("Neznámý parametr G5_7", str),
    8: ("Neznámý parametr G5_8", str),
    9: ("Neznámý parametr G5_9", str),
    10: ("Neznámý parametr G5_10", str),
    11: ("Neznámý parametr G5_11", str),
    12: ("Neznámý parametr G5_12", str),
    13: ("Neznámý parametr G5_13", str),
    14: ("Neznámý parametr G5_14", str),
    15: ("Neznámý parametr G5_15", str),
    16: ("Neznámý parametr G5_16", str),
    17: ("Neznámý parametr G5_17", str),
    18: ("Neznámý parametr G5_18", str),
    19: ("Neznámý parametr G5_19", str),
    }

# Parameter Group 6
# Skupina parametrů 6 (neznámé parametry)
PARAM_GROUP_6_MAPPING: Dict[int, Tuple[str, Callable[[Any], str]]] = {
    0: ("Neznámý parametr  G6_0", str),
    1: ("Neznámý parametr G6_1", str),
    2: ("Neznámý parametr G6_2", str),
    3: ("Neznámý parametr G6_3", str),
    4: ("Neznámý parametr G6_4", str),
    5: ("Neznámý parametr G6_5", str),
    6: ("Neznámý parametr G6_6", str),
    7: ("Neznámý parametr G6_7", str),
    8: ("Neznámý parametr G6_8", str),
    9: ("Neznámý parametr G6_9", str),
    10: ("Neznámý parametr G6_10", str),
    11: ("Neznámý parametr G6_11", str),
    12: ("Neznámý parametr G6_12", str),
    13: ("Neznámý parametr G6_13", str),
    14: ("Neznámý parametr G6_14", str),
    15: ("Neznámý parametr G6_15", str),
    16: ("Neznámý parametr G6_16", str),
    17: ("Neznámý parametr G6_17", str),
    18: ("Neznámý parametr G6_18", str),
    19: ("Neznámý parametr G6_19", str),
}


# Parameter Group 7
# Skupina parametrů 7
PARAM_GROUP_7_MAPPING: Dict[int, Tuple[str, Callable[[Any], str]]] = {
    0: ("Chladicí pomocný obvod", lambda x: "Zakázáno" if x == 1 else "Povoleno"),
    1: ("Teplotní rozdíl výfukových plynů", lambda x: f"{x}°C"),
    2: ("Režim ovládání pomocného expanzního ventilu", str),
    3: ("Maximální otáčky ventilátoru - tichý režim (topení)", lambda x: f"{x}rpm"),
    4: ("Maximální otáčky ventilátoru - tichý režim (chlazení)", lambda x: f"{x}rpm"),
    5: ("Korekce přehřátí 1", lambda x: f"{convert_to_signed(x)}°C"),
    6: ("Korekce přehřátí 2", lambda x: f"{x}°C"),
    7: ("Korekce přehřátí 3", lambda x: f"{x}°C"),
    8: ("Korekce přehřátí 4", lambda x: f"{x}°C"),
    9: ("Korekce přehřátí 5", lambda x: f"{x}°C"),
    10: ("Korekce přehřátí 6", lambda x: f"{x}°C"),
    11: ("Korekce přehřátí 7", lambda x: f"{x}°C"),
    12: ("Kompenzace fáze A", lambda x: f"{x}mA"),
    13: ("Rezervováno G7_13", str),
    14: ("Rezervováno G7_14", str),
    15: ("Rezervováno G7_15", str),
    16: ("Rezervováno G7_16", str),
    17: ("Rezervováno G7_17", str),
    18: ("Rozšiřující deska", str),
    19: ("Lineární kompenzace výkonu", lambda x: f"{x}"),
}


# Parameter Group 8 (all zeros/reserved)
# Skupina parametrů 8 (neznámé parametry)
PARAM_GROUP_8_MAPPING: Dict[int, Tuple[str, Callable[[Any], str]]] = {
    0: ("Neznámý parametr G8_0", str),
    1: ("Neznámý parametr G8_1", str),
    2: ("Neznámý parametr G8_2", str),
    3: ("Neznámý parametr G8_3", str),
    4: ("Neznámý parametr G8_4", str),
    5: ("Neznámý parametr G8_5", str),
    6: ("Neznámý parametr G8_6", str),
    7: ("Neznámý parametr G8_7", str),
    8: ("Neznámý parametr G8_8", str),
    9: ("Neznámý parametr G8_9", str),
    10: ("Neznámý parametr G8_10", str),
    11: ("Neznámý parametr G8_11", str),
    12: ("Neznámý parametr G8_12", str),
    13: ("Neznámý parametr G8_13", str),
    14: ("Neznámý parametr G8_14", str),
    15: ("Neznámý parametr G8_15", str),
    16: ("Neznámý parametr G8_16", str),
    17: ("Neznámý parametr G8_17", str),
    18: ("Neznámý parametr G8_18", str),
    19: ("Neznámý parametr G8_19", str),
}

# Skupina parametrů 23 (Stavové/Statistické údaje)
PARAM_GROUP_23_MAPPING: Dict[int, Tuple[str, Callable[[Any], str]]] = {
    0: ("Výkon vytápění/chlazení", lambda x: f"{x/10}kW"),
    1: ("Aktuální průtok vody", lambda x: f"{x/100}m³/h"),
    2: ("Proud celého zařízení", lambda x: f"{x/10}A"),
    3: ("Napětí celého zařízení", lambda x: f"{x}V"),
    4: ("Výkon celého zařízení", lambda x: f"{x}W"),
    5: ("COP", lambda x: f"{x/10}"),
    6: ("Cílový průtok", lambda x: f"{x}%"),
    7: ("Aktuální rychlost čerpadla", lambda x: f"{x/10}%"),
    8: ("Rezervováno", str),
    9: ("Rezervováno", str),
    10: ("Denní spotřeba", lambda x: f"{x}kWh"),
    11: ("Rok", str),
    12: ("Měsíc", str),
    13: ("Den", str),
    14: ("Hodina", str),
    15: ("Minuta", str),
    16: ("Sekunda", str),
    17: ("Rezervováno G23_17", str),
    18: ("Rezervováno G23_18", str),
    19: ("Rezervováno G23_19", str),
}


# Hlavní slovník všech skupin parametrů
PARAMETER_GROUPS = {
    1: PARAM_GROUP_1_MAPPING,
    2: PARAM_GROUP_2_MAPPING,
    3: PARAM_GROUP_3_MAPPING,
    4: PARAM_GROUP_4_MAPPING,
    5: PARAM_GROUP_5_MAPPING,
    6: PARAM_GROUP_6_MAPPING,
    7: PARAM_GROUP_7_MAPPING,
    8: PARAM_GROUP_8_MAPPING,
    23: PARAM_GROUP_23_MAPPING,
}

# Slovník s názvy skupin parametrů
PARAMETER_GROUPS_CODES = {
    1: "Základní parametry",  # Přidáno
    2: "Ochranné limity",
    3: "Parametry odmrazování",
    4: "Parametry kompresoru a ventilátoru",
    5: "PID parametry",
    6: "Provozní parametry",
    7: "Rozšířené parametry",
    8: "Rezervováno",
    23: "Stavové informace",
}

# Hlavní slovník status  skupin parametrů
STATUS_GROUPS = {
    "S1": STATUS_GROUP_1_MAPPING,
    # další status skupiny...
}

# Slovník s názvy status parametrů
STATUS_GROUPS_CODES = {
    "S1": "Stavové hodnoty",
}
