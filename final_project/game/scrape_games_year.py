import pandas as pd
import functools
from game import *
import time
from datetime import date 
import os
import sys
# data_dir = "/Users/sawyer/Desktop/data_science_denver/Spring_2021/capstone/homework/final_project/data/"


if __name__ == "__main__":
    # setting year as a command line option
    try:
        year = int(sys.argv[1]) # checking for numeric simulations
    except ValueError: 
        raise ValueError("Value for year must be numeric.")
    if year > date.today().year: # raising error if there is not at least 1 simulation
        raise ValueError("Must be a past year.")
    # setting the data directory as as command line option
    try:
        data_dir = str(sys.argv[2])
    except ValueError: # checking the type
        raise ValueError("Directory to save data in must be a string.")
    if not os.path.isdir(data_dir):
        raise ValueError("The data directory must exist.")
    
    # might as well time these for future reference. Each should take probably around 2-3 minutes
    # give or take...
    start = time.time()
    
    # scraping game results from the desired season
    all_game_results = pd.DataFrame(get_season_game_results(str(year)))
    all_game_results.to_csv(data_dir + "game_results_" + str(year) + ".csv", index=False)
    print("Game results from the " + str(year) + "/" + str(year+1) + " season saved in the directory below\n" + data_dir + "game_results_" + str(year) + ".csv\n", sep='')
    
    end = time.time()
    print("Scraping data took:", round((end - start)/60, 2), "minutes")
    start = time.time()
    
    # scraping game results from the desired season
    all_game_officials = pd.DataFrame(get_game_officials(str(year)))
    all_game_officials.to_csv(data_dir + "game_officials_" + str(year) + ".csv", index=False)
    print("Game officials from the " + str(year) + "/" + str(year+1) + " season saved in the directory below\n" + data_dir + "game_officials_" + str(year) + ".csv\n", sep='')
    
    end = time.time()
    print("Scraping data took:", round((end - start)/60, 2), "minutes")
    start = time.time()
    
    
    # scraping game results from the desired season
    all_team_stats = pd.DataFrame(get_team_stats_season(str(year)))
    all_team_stats.to_csv(data_dir + "game_team_stats_" + str(year) + ".csv", index=False)
    print("Team game statistics from the " + str(year) + "/" + str(year+1) + " season saved in the directory below\n" + data_dir + "game_team_stats_" + str(year) + ".csv\n", sep='')
    
    end = time.time()
    print("Scraping data took:", round((end - start)/60, 2), "minutes")
    start = time.time()
    
    
    # scraping game results from the desired season
    all_player_stats = pd.DataFrame(get_player_stats_season(str(year)))
    all_player_stats.to_csv(data_dir + "game_player_stats_" + str(year) + ".csv", index=False)
    print("Player game statistics from the " + str(year) + "/" + str(year+1) + " season saved in the directory below\n" + data_dir + "game_player_stats_" + str(year) + ".csv\n", sep='')
    
    end = time.time()
    print("Scraping data took:", round((end - start)/60, 2), "minutes")
    start = time.time()
    
    
    # scraping game results from the desired season
    all_goalie_stats = pd.DataFrame(get_goalie_stats_season(str(year)))
    all_goalie_stats.to_csv(data_dir + "game_goalie_stats_" + str(year) + ".csv", index=False)
    print("Goalie game statistics from the " + str(year) + "/" + str(year+1) + " season saved in the directory below\n" + data_dir + "game_goalie_stats_" + str(year) + ".csv\n", sep='')
    
    end = time.time()
    print("Scraping data took:", round((end - start)/60, 2), "minutes")
    
