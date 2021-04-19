import pandas as pd
import functools
# doing it the old fashion way

# function to pull player data/statistics. More can be collected from the statsapi
def get_player(year):
    # create the link based on year
    link = f"https://www.hockey-reference.com/leagues/NHL_%s_skaters.html#stats" % year
    # use pandas to read in the table
    data = pd.read_html(link)[0]
    # rename the columns to be more usable/readable
    data.columns = [
        "rank", "player", "age", "team", "position", "games_played", "goals",
        "assists", "points", "plus_minus", "penalties_in_minutes", "point_shares",
        "even_strength_goals", "powerplay_goals", "shorthanded_goals", "game_winning_goals",
        "even_strength_assists", "powerplay_assists", "shorthanded_assists", "shots",
        "shooting_pct", "time_on_ice_min", "average_time_on_ice", "blocks", 
        "hits", "faceoff_wins", "faceoff_losses", "faceoff_win_pct"
    ]
    # adding a column indicating the season
    last_year = year-1
    data["season"] = f'%s/%s' % (last_year, year)
    return(data)


# function to pull salary data
def get_salary(team, year):
    link = f"https://www.spotrac.com/nhl/%s/cap/%s/" % (team, year)
    # try/except because there's been an expansion lately and the site requires a subscription...
    try: 
        data = pd.read_html(link)[0]
        data['team'] = team
        data['season'] = f'%s/%s' % (year, year+1)
        data.columns = ["player", "position", 'age', 'base_salary', 
                       'signing_bonus', 'perf_bonus', 'total_salary', 'na',
                       'total_cap_hit', 'adjusted_cap_hit', 'cap_pct',
                       'team', 'season']
        data.drop(columns = ['na'], inplace = True)
        return(data)
    except:
        print(f"Salary data not available for %s for %s/%s season" % (team, year, year + 1))

        
if __name__ == "__main__":

    # scraping player stats from the past 2 seasons
    player_list = [get_player(year) for year in range(2018, 2021)]
    # reducing into a single dataframe
    player_df = functools.reduce(lambda left, right: 
                                 pd.concat([left, right], axis = 0, ignore_index=True),
                    player_list)
    player_df.to_csv("/Users/sawyer/Desktop/data_science_denver/Spring_2021/capstone/homework/midterm_project/data/player_season.csv", index=False)
    print("Player season statistics saved.")
    
    # list of current NHL teams pulled from google with formatting
    # updated to fit the salary website
    current_nhl_teams = """Anaheim Ducks
Arizona Coyotes
Boston Bruins
Buffalo Sabres
Calgary Flames
Carolina Hurricanes
Chicago Blackhawks
Colorado Avalanche
Columbus Blue Jackets
Dallas Stars
Detroit Red Wings
Edmonton Oilers
Florida Panthers
Los Angeles Kings
Minnesota Wild
Montreal Canadiens
Nashville Predators
New Jersey Devils
New York Islanders
New York Rangers
Ottawa Senators
Philadelphia Flyers
Pittsburgh Penguins
San Jose Sharks
St Louis Blues
Tampa Bay Lightning
Toronto Maple Leafs
Vancouver Canucks
Vegas Golden Knights
Washington Capitals
Winnipeg Jets""".lower().replace(" ", "-").split("\n")

    # getting salaries from the last 2 years for all teams
    salary_list = [get_salary(team, year) for year in (2018, 2019) for team in current_nhl_teams]

    # reducing into a single dataframe
    salary_df = functools.reduce(lambda left, right: pd.concat([left, right], axis = 0, ignore_index=True),
                    salary_list)

    salary_df.sort_values(by = ['player', 'season'], ignore_index=True, inplace=True)
    salary_df.to_csv("/Users/sawyer/Desktop/data_science_denver/Spring_2021/capstone/homework/midterm_project/data/player_salary.csv", index=False)
    print("Player salaries save.")