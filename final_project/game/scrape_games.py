import pandas as pd
import functools
from game import *
import time

data_dir = "/Users/sawyer/Desktop/data_science_denver/Spring_2021/capstone/homework/final_project/data/"


if __name__ == "__main__":
    # might as well time these for future reference. Each should take probably around 25 minutes
    # give or take...
    start = time.time()
    
    # scraping game results from the past 10 seasons
    all_game_results = [pd.DataFrame(get_season_game_results(str(year))) for year in range(2010, 2020)]
    # reducing into a single dataframe
    all_game_results_df = functools.reduce(lambda left, right: 
                                 pd.concat([left, right], axis = 0, ignore_index=True),
                    all_game_results)
    all_game_results_df.to_csv(data_dir + "game_results.csv", index=False)
    print("Game results saved in the directory below\n", data_dir + "game_results.csv\n")
    
    end = time.time()
    print("Scraping data took:", round((end - start)/60, 2), "minutes")
    start = time.time()
    
    # scraping game results from the past 10 seasons
    all_game_officials = [pd.DataFrame(get_game_officials(str(year))) for year in range(2010, 2020)]
    # reducing into a single dataframe
    all_game_officials_df = functools.reduce(lambda left, right: 
                                 pd.concat([left, right], axis = 0, ignore_index=True),
                    all_game_officials)
    all_game_officials_df.to_csv(data_dir + "game_officials.csv", index=False)
    print("Game officials saved in the directory below\n", data_dir + "game_officials.csv\n")
    
    end = time.time()
    print("Scraping data took:", round((end - start)/60, 2), "minutes")
    start = time.time()
    
    
    # scraping game results from the past 10 seasons
    all_team_stats = [pd.DataFrame(get_team_stats_season(str(year))) for year in range(2010, 2020)]
    # reducing into a single dataframe
    all_team_stats_df = functools.reduce(lambda left, right: 
                                 pd.concat([left, right], axis = 0, ignore_index=True),
                    all_team_stats)
    all_team_stats_df.to_csv(data_dir + "game_team_stats.csv", index=False)
    print("Team game statistics saved in the directory below\n", data_dir + "game_team_stats.csv\n")
    
    end = time.time()
    print("Scraping data took:", round((end - start)/60, 2), "minutes")
    start = time.time()
    
    
    # scraping game results from the past 10 seasons
    all_player_stats = [pd.DataFrame(get_player_stats_season(str(year))) for year in range(2010, 2020)]
    # reducing into a single dataframe
    all_player_stats_df = functools.reduce(lambda left, right: 
                                 pd.concat([left, right], axis = 0, ignore_index=True),
                    all_player_stats)
    all_player_stats_df.to_csv(data_dir + "game_player_stats.csv", index=False)
    print("Player game statistics saved in the directory below\n", data_dir + "game_player_stats.csv\n")
    
    end = time.time()
    print("Scraping data took:", round((end - start)/60, 2), "minutes")
    start = time.time()
    
    
    # scraping game results from the past 10 seasons
    all_goalie_stats = [pd.DataFrame(get_goalie_stats_season(str(year))) for year in range(2010, 2020)]
    # reducing into a single dataframe
    all_goalie_stats_df = functools.reduce(lambda left, right: 
                                 pd.concat([left, right], axis = 0, ignore_index=True),
                    all_goalie_stats)
    all_goalie_stats_df.to_csv(data_dir + "game_goalie_stats.csv", index=False)
    print("Goalie game statistics saved in the directory below\n", data_dir + "game_goalie_stats.csv\n")
    
    end = time.time()
    print("Scraping data took:", round((end - start)/60, 2), "minutes")
    