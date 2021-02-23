"""Random but useful utilities for other classes."""

# CONSTANTS
G = 9.81 # meters per second squared
WATER_DENSITY = 977 # kg per meter cubed
MAX_HYPHAL_GROWTH = 8.63 #mm /day
TEMPERATURE_THRESHOLD_MULTIPLIER = 0.20
MOISTURE_THRESHOLD_MULTIPLIER = 0.4 #0,.4 default
MEDIAN_GROWTH_RATE = 3.55 #mm /day
DAYS_UNTIL_EXPANSION = 8

probability_thresholds = {  "Phlebia rufa"              : 0.80,
                            "Lentinus crinitus"         : 0.7538,
                            "Laetiporus conifericola"   : 0.7077,
                            "Fomes fomentarius"         : 0.6615,
                            "Hyphoderma setigerum"      : 0.6154,
                            "Porodisculus pendulus"     : 0.5692,
                            "Phellinus gilvus"          : 0.5231,
                            "Tyromyces chioneus"        : 0.4769,
                            "Phellinus robiniae"        : 0.4308,
                            "Hyphodontia crustosa"      : 0.3846,
                            "Schizophyllum commune"     : 0.3385,
                            "Phellinus hartigii"        : 0.2923,
                            "Armillaria tabescens"      : 0.2462,
                            "Xylobolus subpileatus"     : 0.20}

def rainfall_inches_to_mPa(rain: float) -> float:
    """Converts inches of rain to mPa."""
    return rain*2.54*WATER_DENSITY*G*1e-8
