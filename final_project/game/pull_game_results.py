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
    print("Scraping data took:", (end - start)/60, "minutes")

