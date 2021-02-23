"""
Authors: Therese Aglialoro, Cameron Nottingham, and William Kostuch
2021 MCM, Problem A: Fungi
"""
import graphing

if __name__ == "__main__":
    # DONE:
    
    #temperature_over_time(CLIMATE_NAMES, [], trials=5, time_limit=365)

    # RUNNING:
    #TODO: Run these with varying temperature and rainfall
    #number_fungi_over_time_per_climate(CLIMATE_NAMES, FUNGUS_NAMES, trials = 3, time_limit=365*3)
    #decomposition_with_respect_to_biodiversity("Rainforest", FUNGUS_NAMES, trials = 1, time_limit=365*3)
    #total_food_eaten_over_time(CLIMATE_NAMES, FUNGUS_NAMES, trials=3, time_limit=365*3)


    # OTHER:
    #biomass_over_time(CLIMATE_NAMES, FUNGUS_NAMES, trials=5, time_limit=365*YEARS)
    #food_eaten_by_day_per_fungi_vs_moisture("Rainforest", FUNGUS_NAMES[0:15], trials = 1, time_limit=365)
    #temperature_over_time(CLIMATE_NAMES, [], trials=3, time_limit=365)

    
    # BRACKET
    #number_fungi_over_time_per_climate(CLIMATE_NAMES, FUNGUS_NAMES, trials = 3, time_limit=365*2)
    #decomposition_with_respect_to_biodiversity("Rainforest", FUNGUS_NAMES, trials = 1, time_limit=365*2)
    #total_food_eaten_over_time(CLIMATE_NAMES, FUNGUS_NAMES, trials=3, time_limit=365*2)

    #fungal_heat_map("Rainforest", ["Phlebia rufa"],365)
    graphing.fungal_heat_map_all_climates(time_limit=365, file_name="Sensitivity growth rate - 2 - heat map (one Year).png")

