import pandas as pd
import functools
import requests
# doing it the old fashion way

# def get_player(year):
#     # create the link based on year
#     link = f"https://www.hockey-reference.com/leagues/NHL_%s_skaters.html#stats" % year
#     # use pandas to read in the table
#     data = pd.read_html(link)[0]
#     # rename the columns to be more usable/readable
#     data.columns = [
#         "rank", "player", "age", "team", "position", "games_played", "goals",
#         "assists", "points", "plus_minus", "penalties_in_minutes", "point_shares",
#         "even_strength_goals", "powerplay_goals", "shorthanded_goals", "game_winning_goals",
#         "even_strength_assists", "powerplay_assists", "shorthanded_assists", "shots",
#         "shooting_pct", "time_on_ice_min", "average_time_on_ice", "blocks", 
#         "hits", "faceoff_wins", "faceoff_losses", "faceoff_win_pct"
#     ]
#     # adding a column indicating the season
#     last_year = year-1
#     data["season"] = f'%s/%s' % (last_year, year)
#     return(data)


# function to pull player data/statistics. Collected from the NHL statsapi
def get_players(season):
    """
    Arguments:
        season - The season player statistics are requested. Character. Example: "20192020"
                 for the 2019/2020 season
    """
    # setting the base API url for use throughout
    base_api = "https://statsapi.web.nhl.com"
    # getting the full list of teams
    teams = requests.get(base_api + "/api/v1/teams").json()
    # expand needed for getting the roster for the season
    roster_link = f"?expand=team.roster&season=%s" % season
    # looping through each team
    for team in range(len(teams['teams'])):
        # progress check
        print(f"%s for %s season" % (teams['teams'][team]['name'], season))
        # this is the link specific to the team
        team_api = teams['teams'][team]['link']
        # getting the roster for the team on each passthrough
        roster = requests.get(base_api + team_api + "/roster" + roster_link).json()
        # looping through each player on the roster to get their data/stats
        for player in range(len(roster['roster'])):
            # skipping goalies because they have completely different stats
            if roster['roster'][player]['position']['code'] == "G":
                continue
            # collecting the player data now
            else:
                # initializing dictionary to grab everything
                player_dict = {}
                # unique player ID
                player_id = roster['roster'][player]['person']['id']
                # print(player_id)
                # the API link for each unique player
                player_link = roster['roster'][player]['person']['link']
                # collecting player position and team
                player_dict['position'] = roster['roster'][player]['position']['code']
                player_dict['team'] = teams['teams'][team]['name']
                
                # getting the player 'characteristics' so to speak
                player_char_json = requests.get(base_api + player_link).json()
                
                # looping through to add these data to the dictionary
                for key in list(player_char_json['people'][0].keys())[:-2]:
                        player_dict[key] = player_char_json['people'][0][key]
                # getting the more traditional player statistics
                stat_json = requests.get(base_api + player_link + f"/stats?stats=statsSingleSeason&season=%s" % season).json()['stats'][0]
                # more detailed goal statistics
                goal_json = requests.get(base_api + player_link + f"/stats?stats=goalsByGameSituation&season=%s" % season).json()['stats'][0]
                # adding the season type (i.e. Regular Season, Playoff)) and season
                player_dict['season_type'] = stat_json['type']['gameType']['id']
                # player has no stats for the regular season if 'splits' is empty so skip player
                if len(stat_json['splits']) == 0:
                    continue
                player_dict['season'] = stat_json['splits'][0]['season']
                # looping through to add these data to the dictionary
                for stat in stat_json['splits'][0]['stat'].keys():
                    player_dict[stat] = stat_json['splits'][0]['stat'][stat]
                # some players have scored no goals so checking for that, skipping if so
                if len(goal_json['splits']) > 0:
                    for goal in goal_json['splits'][0]['stat'].keys():
                        player_dict[goal] = goal_json['splits'][0]['stat'][goal]
                # yield the player dictionary at this point, then the loop will repeat
                yield(player_dict)

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
    player_list = [pd.DataFrame(get_players(year)) for year in ["20182019", '20192020']]
    # reducing into a single dataframe
    player_df = functools.reduce(lambda left, right: 
                                 pd.concat([left, right], axis = 0, ignore_index=True),
                    player_list)
    player_df.to_csv("/Users/sawyer/Desktop/data_science_denver/Spring_2021/capstone/homework/midterm_project/data/player_season.csv", index=False)
    print("Player season statistics saved in the directory below\
/Users/sawyer/Desktop/data_science_denver/Spring_2021/capstone/homework/midterm_project/data/player_season.csv\n")
    
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
    print("Player salaries saved in the directory below\
/Users/sawyer/Desktop/data_science_denver/Spring_2021/capstone/homework/midterm_project/data/player_salary.csv\n.")