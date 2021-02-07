"""Random but useful utilities for other classes."""

# CONSTANTS
G = 9.81 # meters per second squared
WATER_DENSITY = 977 # kg per meter cubed
MAX_HYPHAL_GROWTH = 8.63 #mm /day
TEMPERATURE_THRESHOLD_MULTIPLIER = 0.20
MOISTURE_THRESHOLD_MULTIPLIER = 0.40
PROBABILITY_THRESHOLD = 0.35




def rainfall_inches_to_mPa(rain: float) -> float:
    """Converts inches of rain to mPa."""
    return rain*2.54*WATER_DENSITY*G*1e-8
