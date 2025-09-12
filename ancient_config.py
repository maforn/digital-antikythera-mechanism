"""
Configuration for the Ancient Antikythera Simulation.
Geocentric model data, historical calendar details, and UI constants.
"""

# --- Screen Settings ---
MAX_WIDTH = 1200
SCREEN_HEIGHT_ADJUST = 80

# --- UI Colors ---
BG_COLOR = (10, 5, 0)
DIAL_COLOR = (180, 150, 100)
TEXT_COLOR = (220, 200, 180)
POINTER_COLOR = (255, 100, 100)
MOON_COLOR_LIT = (230, 230, 220)
MOON_COLOR_DARK = (50, 50, 40)

# --- Geocentric Model Data ---
# Simplified orbital periods (in days) for a geocentric model.
# These are not scientifically accurate but are set for visual representation.
GEOCENTRIC_DATA = {
    'Moon': {'period': 27.3, 'distance': 0.2, 'color': (200, 200, 200), 'size': 5},
    'Sun': {'period': 365.25, 'distance': 0.8, 'color': (255, 220, 0), 'size': 10},
    'Mercury': {'period': 88.0, 'distance': 0.3, 'color': (180, 180, 180), 'size': 4},
    'Venus': {'period': 224.7, 'distance': 0.5, 'color': (255, 220, 100), 'size': 6},
    'Mars': {'period': 687.0, 'distance': 1.0, 'color': (220, 70, 80), 'size': 5},
    'Jupiter': {'period': 4331.0, 'distance': 1.3, 'color': (230, 190, 140), 'size': 9},
    'Saturn': {'period': 10747.0, 'distance': 1.6, 'color': (240, 200, 150), 'size': 8},
}

# --- Calendar and Dial Data ---
# Based on the Antikythera Mechanism's front face inscriptions.
ZODIAC_INSCRIPTIONS_GREEK = [
    "ΚΡΙΟΣ", "ΤΑΥΡΟΣ", "ΔΙΔΥΜΟΙ", "ΚΑΡΚΙΝΟΣ", "ΛΕΩΝ", "ΠΑΡΘΕΝΟΣ",
    "ΧΗΛΑΙ", "ΣΚΟΡΠΙΟΣ", "ΤΟΞΟΤΗΣ", "ΑΙΓΟΚΕΡΩΣ", "ΥΔΡΟΧΟΟΣ", "ΙΧΘΥΕΣ"
]

EGYPTIAN_MONTHS = [
    "Thoth", "Phaophi", "Athyr", "Choiak", "Tybi", "Mechir",
    "Phamenoth", "Pharmuthi", "Pachon", "Payni", "Epiphi", "Mesore"
]

# --- Moon Phase Data ---
MOON_PHASE_NAMES = [
    "New", "Waxing Crescent", "First Quarter", "Waxing Gibbous",
    "Full", "Waning Gibbous", "Last Quarter", "Waning Crescent"
]

# --- Back Face Dial Data ---
METONIC_MONTHS = [
    "PHOINIKAIOS", "KRANEIOS", "LANOTROPIOS", "MACHANEYS", "DODEKATEYS", "EUKLEIOS",
    "ARTEMISIOS", "PSYDRUS", "GAMEILIOS", "AGRIANIOS", "PANAMOS", "APELLAIOS"
]

GAMES_INSCRIPTIONS = {
    1: ("ISTHMIA", "OLYMPIA"),
    2: ("NEMEA", "NAA"),
    3: ("ISTHMIA", "PYTHIA"),
    4: ("NEMEA", "HALIEIA")
}

EXELIGMOS_LABELS = ["", "H", "Iϛ"] # 0, 8, 16 hours
