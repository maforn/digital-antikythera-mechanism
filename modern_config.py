"""
Configuration data for the Modern Antikythera simulation.
This file contains static data such as planet properties, calendar details,
and UI constants.
"""

# --- Planet Data for Visualization ---
# Orbital periods in Earth days
ORBITAL_PERIODS = {
    'Mercury': 88.0,
    'Venus': 224.7,
    'Earth': 365.25,
    'Mars': 687.0,
    'Jupiter': 4331.0,
    'Saturn': 10747.0,
    'Uranus': 30687.0,
    'Neptune': 60190.0,
}

PLANET_VISUAL_DATA = {
    'Mercury': {'color': (180, 180, 180), 'speed': (360 / ORBITAL_PERIODS['Mercury']), 'size': 5},
    'Venus': {'color': (255, 220, 100), 'speed': (360 / ORBITAL_PERIODS['Venus']), 'size': 7},
    'Earth': {'color': (0, 150, 255), 'speed': (360 / ORBITAL_PERIODS['Earth']), 'size': 8},
    'Mars': {'color': (220, 70, 80), 'speed': (360 / ORBITAL_PERIODS['Mars']), 'size': 6},
    'Jupiter': {'color': (230, 190, 140), 'speed': (360 / ORBITAL_PERIODS['Jupiter']), 'size': 12},
    'Saturn': {'color': (240, 200, 150), 'speed': (360 / ORBITAL_PERIODS['Saturn']), 'size': 11},
    'Uranus': {'color': (150, 220, 230), 'speed': (360 / ORBITAL_PERIODS['Uranus']), 'size': 9},
    'Neptune': {'color': (80, 120, 200), 'speed': (360 / ORBITAL_PERIODS['Neptune']), 'size': 9},
}

# Data from the Antikythera Mechanism front face
MONTHS = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
ZODIAC_INSCRIPTIONS = [
    "ARIES", "TAURUS", "GEMINI", "CANCER", "LEO", "VIRGO",
    "LIBRA", "SCORPIO", "SAGITTARIUS", "CAPRICORN", "AQUARIUS", "PISCES"
]

# Modern equivalent days and symbols for some Parapegma events
PARAPEGMA_MARKERS = {
    'Vernal Equinox': {'day': 80, 'symbol': 'VE'},
    'Pleiades Rise': {'day': 135, 'symbol': 'PR'},
    'Summer Solstice': {'day': 172, 'symbol': 'SS'},
    'Orion Rises': {'day': 200, 'symbol': 'OR'},
    'Autumnal Equinox': {'day': 266, 'symbol': 'AE'},
    'Winter Solstice': {'day': 355, 'symbol': 'WS'},
}

# UI Colors
BG_COLOR_TOP = (20, 20, 50)
BG_COLOR_BOTTOM = (5, 5, 20)

# Moon phase data
MOON_PHASE_NAMES = [
    "New Moon", "Waxing Crescent", "First Quarter", "Waxing Gibbous",
    "Full Moon", "Waning Gibbous", "Last Quarter", "Waning Crescent"
]
SYNODIC_PERIOD = 29.53
MOON_EPOCH = "2000-01-06" # A known New Moon date

# --- Back Face Dial Data (Modern Interpretation) ---
METONIC_CYCLE_YEARS = 19
METONIC_TOTAL_MONTHS = 235

SAROS_CYCLE_MONTHS = 223
SAROS_CYCLE_YEARS = 18.03

EXELIGMOS_CYCLE_SAROS = 3
EXELIGMOS_CYCLE_YEARS = 54.09

# Modern equivalent for the "Games" dial
MODERN_GAMES = {
    0: "Summer Olympics",
    1: "World Cup",
    2: "Winter Olympics",
    3: "Continental Games"
}

# UI Colors for Back Face
DIAL_BG_COLOR = (25, 35, 60)
DIAL_OUTLINE_COLOR = (100, 120, 150)
PROGRESS_BAR_COLOR = (0, 180, 255)
PROGRESS_BG_COLOR = (40, 50, 80)
BACK_POINTER_COLOR = (255, 100, 100)
BACK_TEXT_COLOR = (220, 220, 220)
GLOW_COLOR = (0, 180, 255, 50) # With alpha
