"""Random but useful utilities for other classes."""

# CONSTANTS
G = 9.81 # meters per second squared
WATER_DENSITY = 977 # kg per meter cubed



def rainfall_inches_to_mPa(rain: float) -> float:
    """Converts inches of rain to mPa."""
    return rain*2.54*WATER_DENSITY*G*1e-8
