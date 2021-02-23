import random
import math
from utilities import rainfall_inches_to_mPa

BIOMASS_WEIGHT = 0.3

class Climate:
    """Climate class for handling different biomes."""

    def __init__(self, climate_type: str, 
                temperature_range: tuple,
                moisture_base: float, 
                annual_rain: tuple, 
                evaporation_rate: float, 
                biomass_density: float,
                raindays_per_year: float) -> None:
        # Static values per subclass
        self.climate_type = climate_type
        self.temperature_range = temperature_range
        self.moisture_base = moisture_base
        self.annual_rain = annual_rain
        self.evaporation_rate = evaporation_rate
        self.biomass_density = biomass_density
        self.raindays_per_year = raindays_per_year
        # Dynamic values and their initial conditions
        self.current_moisture = self.moisture_base
        self.current_temperature = self.update_temperature(0)

    def __str__(self) -> str:
        """Returns a pretty-print string of the Climate data."""
        return f"Climate type: {self.climate_type}\n" + \
            f"Temperature range: {self.temperature_range} degrees C\n" + \
            f"Moisture base: {self.moisture_base} mPa\n" + \
            f"Annual rainfall: {self.annual_rain} inches\n" + \
            f"Evaporation rate: {self.evaporation_rate} inches per day\n" + \
            f"Biomass density: {self.biomass_density} kilograms\n" + \
            f"Days of rain per year: {self.raindays_per_year}\n" 



    # Climate functions for day-by-day operation

    ## Rain functions
    def __is_raining(self) -> bool:
        """Determines if the Climate is raining that day."""
        rain_probability = self.raindays_per_year / 365
        random_roll = random.random()
        return random_roll <= rain_probability
    
    def __add_rainfall_to_moisture(self):
        """Adds the requisite amount of moisture to the Climate's
            current moisture value per day of rain."""
        # 1.177e-3 is the average amount of rain in one day in mPa
        self.current_moisture += random.uniform(.85, 1.15) * 1.177e-3 

    def __evaporate_moisture(self):
        """Evaporates the requisite amount of moisture depending 
            on the Climate type."""
        self.current_moisture -= rainfall_inches_to_mPa(self.evaporation_rate)

    def update_rain(self):
        """Probabilistically determines if the Climate is raining
            and then updates the all necessary Climate components."""
        if self.__is_raining():
            self.__add_rainfall_to_moisture()
        self.__evaporate_moisture()

    ## Temperature functions
    def __set_current_temperature(self, new_temp: float):
        """Sets the current temperature of the Climate to new_temp."""
        self.current_temperature = new_temp

    def update_temperature(self, time: int):
        """Updates the current Climate temperature according to time
            given by the Environment and by Climate specifics."""
        a,b = self.temperature_range
        new_temp = ((a + b) / 2) + ((b - a) / 2)*math.sin((2*math.pi*time) / 365) * random.uniform(0.85, 1.15)
        self.__set_current_temperature(new_temp)

    ## Biomass functions
    def get_inbound_biomass(self, time: int) -> float:
        """Returns the amount of biomass that enters the Climate at 
            a specific time."""
        return (self.biomass_density + self.biomass_density*0.2*math.sin((2*math.pi*time) / 365)) * BIOMASS_WEIGHT

    # Function that Environment calls each day
    def update_climate_per_day(self, time: int):
        """Updates the Climate's moisture and temperature."""
        self.update_rain()
        self.update_temperature(time)
    
    def get_climate_biomass_density(self):
        """Returns the Climate's biomass density."""
        return self.biomass_density

    # Climate functions to be used by fungi
    def get_climate_temperature(self) -> float:
        """Returns the Climate's current temperature in Celsius."""
        return self.current_temperature

    def get_climate_moisture(self) -> float:
        """Returns the Climate's current moisture level in mPa."""
        return self.current_moisture



# Climate subclasses

class Desert(Climate):
    """Desert Climate."""

    def __init__(self, climate_type="Desert (Arid)", 
                temperature_range=(-3.9, 38), 
                moisture_base=(-1.5), 
                annual_rain=(10, 10), 
                evaporation_rate=0.027, 
                biomass_density=1, 
                raindays_per_year=2.08) -> None:
        super().__init__(climate_type, 
                        temperature_range, 
                        moisture_base, 
                        annual_rain, 
                        evaporation_rate, 
                        biomass_density, 
                        raindays_per_year)


class Tundra(Climate):
    """Tundra Climate."""

    def __init__(self, climate_type="Tundra (Arid)", 
                temperature_range=(-40, 18), 
                moisture_base=(-1.5), 
                annual_rain=(6, 10), 
                evaporation_rate=0.027, 
                biomass_density=1, 
                raindays_per_year=1.66) -> None:
        super().__init__(climate_type, 
                        temperature_range, 
                        moisture_base, 
                        annual_rain, 
                        evaporation_rate, 
                        biomass_density, 
                        raindays_per_year)


class Grassland(Climate):
    """Grassland Climate."""

    def __init__(self, climate_type="Grassland (Semi-Arid)", 
                temperature_range=(-20, 30), 
                moisture_base=(-1.13325), 
                annual_rain=(20, 35), 
                evaporation_rate=0.075, 
                biomass_density=3.25, 
                raindays_per_year=5.73) -> None:
        super().__init__(climate_type, 
                        temperature_range, 
                        moisture_base, 
                        annual_rain, 
                        evaporation_rate, 
                        biomass_density, 
                        raindays_per_year)


class Shrubland(Climate):
    """Shrubland Climate."""

    def __init__(self, climate_type="Shrubland (Temperate)", 
                temperature_range=(-1, 38), 
                moisture_base=(-0.7665), 
                annual_rain=(12, 61), 
                evaporation_rate=0.1, 
                biomass_density=5.5, 
                raindays_per_year=7.6) -> None:
        super().__init__(climate_type, 
                        temperature_range, 
                        moisture_base, 
                        annual_rain, 
                        evaporation_rate, 
                        biomass_density, 
                        raindays_per_year)


class TemperateDeciduousForest(Climate):
    """Temperate Decidiuous Forest Climate."""

    def __init__(self, climate_type="Temperate Decidiuous Forest (Arboreal)", 
                temperature_range=(-22, 30), 
                moisture_base=(-0.39975), 
                annual_rain=(30, 59), 
                evaporation_rate=0.122, 
                biomass_density=7.75, 
                raindays_per_year=9.27) -> None:
        super().__init__(climate_type, 
                        temperature_range, 
                        moisture_base, 
                        annual_rain, 
                        evaporation_rate, 
                        biomass_density, 
                        raindays_per_year)


class ConiferousForest(Climate):
    """ConiferousForest Climate."""

    def __init__(self, climate_type="ConiferousForest (Arboreal)", 
                temperature_range=(-40, 20), 
                moisture_base=(-0.39975), 
                annual_rain=(12, 35), 
                evaporation_rate=0.064, 
                biomass_density=7.75, 
                raindays_per_year=4.9) -> None:
        super().__init__(climate_type, 
                        temperature_range, 
                        moisture_base, 
                        annual_rain, 
                        evaporation_rate, 
                        biomass_density, 
                        raindays_per_year)


class Rainforest(Climate):
    """Rainforest Climate."""

    def __init__(self, climate_type="Rainforest (Rainforest)", 
                temperature_range=(20, 25), 
                moisture_base=(-0.033), 
                annual_rain=(79, 395), 
                evaporation_rate=0.649, 
                biomass_density=10.0, 
                raindays_per_year=49.38) -> None:
        super().__init__(climate_type, 
                        temperature_range, 
                        moisture_base, 
                        annual_rain, 
                        evaporation_rate, 
                        biomass_density, 
                        raindays_per_year)
