import pandas as pd
import functools
import requests
example_game_url = "http://statsapi.web.nhl.com/api/v1/game/2017020100/feed/live"

# helper function to see the structure of the JSON in the different levels
def print_game_keys(game, level=0):
    for key in game.keys():
        if isinstance(game[key], dict):
            print(" " * level, key, " ", "{")
            print_game_keys(game[key], level+4)
            print(" " * (level+4), "}")
        else:
            print(" "* level, key)

# function to pull player data/statistics. Collected from the NHL statsapi
def get_game_result(game):
    """
    Arguments:
        game - Game ID for a particular game. Character. Example: "2017020001"
                 for the 2017/2018 season
    Returns:
        Single game results based on input game_id
    Example: 
        import pandas as pd
        import requests
        
        pd.DataFrame(get_game_result("2019020300"))
    """
    # setting the base API url for use throughout
    base_api = "https://statsapi.web.nhl.com"
    game_link = f"/api/v1/game/%s/feed/live"% game
    # getting the full list of teams
    try:
        game_url = requests.get(base_api + game_link)
        game_url.raise_for_status()
        game = game_url.json()
        data = {}
        data['gameID'] = game['gamePk']
        data['season'] = game['gameData']['game']['season']
        data['dateTime'] = game['gameData']["datetime"]["dateTime"]
        data['gameType'] = game['gameData']['game']['type']
        data['homeTeamID'] = game['gameData']['teams']['home']['id']
        data['homeTeamName'] = game['gameData']['teams']['home']['name']
        data['awayTeamID'] = game['gameData']['teams']['away']['id']
        data['awayTeamName'] = game['gameData']['teams']['away']['name']
        data['homeGoals'] = game['liveData']['linescore']['teams']['home']['goals']
        data['awayGoals'] = game['liveData']['linescore']['teams']['away']['goals']
        data['homeTeamWin'] = game['liveData']['linescore']['teams']['home']['goals'] > game['liveData']['linescore']['teams']['away']['goals']
        data['venue'] = game['gameData']['venue']['name']
        return(data)
    except:
        print(f"Game %s not found" % game_link)


def get_season_game_results(season):
    """
    Arguments:
        season - Start of a particular season. Character. Example: "2017"
                 for the 2017/2018 season
    Returns:
        All regular season game results for a specified season
    Example: 
        import pandas as pd
        import requests
        # takes a few minutes to run
        pd.DataFrame(get_season_game_results("2019"))
    """
    # setting the base API url for use throughout
    if int(season) == 2012:
        game_range = list(range(1, 721))
    elif int(season) >= 2017:
        game_range = list(range(1, 1272))
    else:
        game_range = list(range(1, 1231))
    for game in game_range:
        game_id = str(game).zfill(4)
        base_api = "https://statsapi.web.nhl.com"
        game_link = f"/api/v1/game/%s/feed/live/"% (season + "02" + game_id)
        # getting the full list of teams
        try:
            game_url = requests.get(base_api + game_link)
            game_url.raise_for_status()
            game = game_url.json()
            data = {}
            data['gameID'] = game['gamePk']
            data['season'] = game['gameData']['game']['season']
            data['dateTime'] = game['gameData']["datetime"]["dateTime"]
            data['gameType'] = game['gameData']['game']['type']
            data['homeTeamID'] = game['gameData']['teams']['home']['id']
            data['homeTeamName'] = game['gameData']['teams']['home']['name']
            data['awayTeamID'] = game['gameData']['teams']['away']['id']
            data['awayTeamName'] = game['gameData']['teams']['away']['name']
            data['homeGoals'] = game['liveData']['linescore']['teams']['home']['goals']
            data['awayGoals'] = game['liveData']['linescore']['teams']['away']['goals']
            data['homeTeamWin'] = game['liveData']['linescore']['teams']['home']['goals'] > game['liveData']['linescore']['teams']['away']['goals']
            data['venue'] = game['gameData']['venue']['name']
            yield(data)
        except: 
            print(f"Game %s not found" % (season + "02" + game_id))
            continue


def get_game_officials(season):
    """
    Arguments:
        season - Start of a particular season. Character. Example: "2017"
                 for the 2017/2018 season
    Returns:
        All regular season game officials for a specified season
    Example: 
        import pandas as pd
        import requests
        # takes a few minutes to run
        pd.DataFrame(get_game_officials("2019"))
    """
    # setting the base API url for use throughout
    if int(season) == 2012:
        game_range = list(range(1, 721))
    elif int(season) >= 2017:
        game_range = list(range(1, 1272))
    else:
        game_range = list(range(1, 1231))
    for game in game_range:
        game_id = str(game).zfill(4)
        base_api = "https://statsapi.web.nhl.com"
        game_link = f"/api/v1/game/%s/feed/live/"% (season + "02" + game_id)
        # getting the full list of teams
        try:
            game_url = requests.get(base_api + game_link)
            game_url.raise_for_status()
            game = game_url.json()
            for i in range(len(game['liveData']['boxscore']['officials'])):
                data = {}
                data['gameID'] = game['gamePk']
                data['officialName'] = game['liveData']['boxscore']['officials'][i]['official']['fullName']
                data['officialType'] = game['liveData']['boxscore']['officials'][i]['officialType']
                yield(data)
        except:
            print(f"Game %s not found" % (season + "02" + game_id))
            continue

            
def get_team_stats_season(season):
    """
    Arguments:
        season - Start of a particular season. Character. Example: "2017"
                 for the 2017/2018 season
    Returns:
        All regular season team stats for a specified season. One row for home, one for away.
    Example: 
        import pandas as pd
        import requests
        # takes a few minutes to run
        pd.DataFrame(get_team_stats_season("2019"))
    """
    # setting the base API url for use throughout
    if int(season) == 2012:
        game_range = list(range(1, 721))
    elif int(season) >= 2017:
        game_range = list(range(1, 1272))
    else:
        game_range = list(range(1, 1231))
    for game in game_range:
        game_id = str(game).zfill(4)
        base_api = "https://statsapi.web.nhl.com"
        game_link = f"/api/v1/game/%s/feed/live/"% (season + "02" + game_id)
        # getting the full list of teams
        try:
            game_url = requests.get(base_api + game_link)
            game_url.raise_for_status()
            game = game_url.json()
            for team in ['home', 'away']:
                data = {}
                data['gameID'] = game['gamePk']
                data['homeAway'] = team
                data['homeTeamWin'] = game['liveData']['linescore']['teams']['home']['goals'] > game['liveData']['linescore']['teams']['away']['goals']
                data['periodsPlayed'] = game['liveData']['linescore']['currentPeriod']
                data['headCoach'] = game['liveData']["boxscore"]['teams'][team]['coaches'][0]['person']['fullName']
                data['teamID'] = game['gameData']['teams'][team]['id']
                data['teamName'] = game['gameData']['teams'][team]['name']
                for key in game['liveData']["boxscore"]['teams'][team]['teamStats']['teamSkaterStats'].keys():
                    data[key] = game['liveData']["boxscore"]['teams'][team]['teamStats']['teamSkaterStats'][key]
                yield(data)
        except: 
            print(f"Game %s not found" % (season + "02" + game_id))
            continue


def get_team_stats_game(game):
    """
    Arguments:
        game - Game ID for a particular game. Character. Example: "2017020001"
                 for the 2017/2018 season
        All regular season game results for a specified season
    Example: 
        import pandas as pd
        import requests
        # takes a few minutes to run
        pd.DataFrame(get_team_stats_game("2017020001"))
    """
    # setting the base API url for use throughout
    
    base_api = "https://statsapi.web.nhl.com"
    game_link = f"/api/v1/game/%s/feed/live/"% game
    # getting the full list of teams
    try:
        game_url = requests.get(base_api + game_link)
        game_url.raise_for_status()
        game = game_url.json()
        for team in ['home', 'away']:
            data = {}
            data['gameID'] = game['gamePk']
            data['homeAway'] = team
            data['homeTeamWin'] = game['liveData']['linescore']['teams']['home']['goals'] > game['liveData']['linescore']['teams']['away']['goals']
            data['periodsPlayed'] = game['liveData']['linescore']['currentPeriod']
            data['headCoach'] = game['liveData']["boxscore"]['teams'][team]['coaches'][0]['person']['fullName']
            data['teamID'] = game['gameData']['teams'][team]['id']
            data['teamName'] = game['gameData']['teams'][team]['name']
            for key in game['liveData']["boxscore"]['teams'][team]['teamStats']['teamSkaterStats'].keys():
                data[key] = game['liveData']["boxscore"]['teams'][team]['teamStats']['teamSkaterStats'][key]
            yield(data)
    except: 
        print(f"Game %s not found" % game_link)


def get_player_stats_game(game):
    """
    Arguments:
        game - Game ID for a particular game. Character. Example: "2017020001"
                 for the 2017/2018 season
        All regular season game results for a specified season
    Example: 
        import pandas as pd
        import requests
        # takes a few minutes to run
        pd.DataFrame(get_player_stats_game("2017020001"))
    """
    base_api = "https://statsapi.web.nhl.com"
    game_link = f"/api/v1/game/%s/feed/live/"% game
    # getting the full list of teams
    try:
        game_url = requests.get(base_api + game_link)
        game_url.raise_for_status()
        game = game_url.json()
        for team in ['home', 'away']:
            for player in game['liveData']["boxscore"]['teams'][team]['players']:
                if game['liveData']["boxscore"]['teams'][team]['players'][player]['position']['code'] not in ("N/A", "G"):
                    data = {}
                    data['gameID'] = game['gamePk']
                    data['playerID'] = game['liveData']["boxscore"]['teams'][team]['players'][player]['person']['id']
                    data['fullName'] = game['liveData']["boxscore"]['teams'][team]['players'][player]['person']['fullName']
                    data['position'] = game['liveData']["boxscore"]['teams'][team]['players'][player]['position']['code']
                    data['homeAway'] = team
                    data['teamID'] = game['gameData']['teams'][team]['id']
                    data['teamName'] = game['gameData']['teams'][team]['name']
                    if isinstance(game['liveData']["boxscore"]['teams'][team]['players'][player]['stats']['skaterStats'], dict):
                        for key in game['liveData']["boxscore"]['teams'][team]['players'][player]['stats']['skaterStats'].keys():
                            data[key] = game['liveData']["boxscore"]['teams'][team]['players'][player]['stats']['skaterStats'][key]
                    yield(data)
                else: 
                    continue
    except: 
        print(f"Game %s not found" % (season + "02" + game_id))


def get_player_stats_season(season):
    """
    Arguments:
        season - Start of a particular season. Character. Example: "2017"
                 for the 2017/2018 season
    Returns:
        All regular season team stats for a specified season. One row for home, one for away.
    Example: 
        import pandas as pd
        import requests
        # takes a few minutes to run
        pd.DataFrame(get_player_stats_season("2019"))
    """
    # setting the base API url for use throughout
    if int(season) == 2012:
        game_range = list(range(1, 721))
    elif int(season) >= 2017:
        game_range = list(range(1, 1272))
    else:
        game_range = list(range(1, 1231))
    for game in game_range:
        game_id = str(game).zfill(4)
        base_api = "https://statsapi.web.nhl.com"
        game_link = f"/api/v1/game/%s/feed/live/"% (season + "02" + game_id)
        # getting the full list of teams
        try:
            game_url = requests.get(base_api + game_link)
            game_url.raise_for_status()
            game = game_url.json()
            for team in ['home', 'away']:
                for player in game['liveData']["boxscore"]['teams'][team]['players']:
                    if game['liveData']["boxscore"]['teams'][team]['players'][player]['position']['code'] not in ("N/A", "G"):
                        data = {}
                        data['gameID'] = game['gamePk']
                        data['playerID'] = game['liveData']["boxscore"]['teams'][team]['players'][player]['person']['id']
                        data['fullName'] = game['liveData']["boxscore"]['teams'][team]['players'][player]['person']['fullName']
                        data['position'] = game['liveData']["boxscore"]['teams'][team]['players'][player]['position']['code']
                        data['homeAway'] = team
                        data['teamID'] = game['gameData']['teams'][team]['id']
                        data['teamName'] = game['gameData']['teams'][team]['name']
                        if isinstance(game['liveData']["boxscore"]['teams'][team]['players'][player]['stats']['skaterStats'], dict):
                            for key in game['liveData']["boxscore"]['teams'][team]['players'][player]['stats']['skaterStats'].keys():
                                data[key] = game['liveData']["boxscore"]['teams'][team]['players'][player]['stats']['skaterStats'][key]
                        yield(data)
                    else: 
                        continue
        except: 
            print(f"Game %s not found" % (season + "02" + game_id))


def get_goalie_stats_game(game):
    """
    Arguments:
        game - Game ID for a particular game. Character. Example: "2017020001"
                 for the 2017/2018 season
        All regular season game results for a specified season
    Example: 
        import pandas as pd
        import requests
        # takes a few minutes to run
        pd.DataFrame(get_goalie_stats_game("2017020001"))
    """
    base_api = "https://statsapi.web.nhl.com"
    game_link = f"/api/v1/game/%s/feed/live/"% game
    # getting the full list of teams
    try:
        game_url = requests.get(base_api + game_link)
        game_url.raise_for_status()
        game = game_url.json()
        for team in ['home', 'away']:
            for player in game['liveData']["boxscore"]['teams'][team]['players']:
                if game['liveData']["boxscore"]['teams'][team]['players'][player]['position']['code'] == "G":
                    data = {}
                    data['gameID'] = game['gamePk']
                    data['playerID'] = game['liveData']["boxscore"]['teams'][team]['players'][player]['person']['id']
                    data['fullName'] = game['liveData']["boxscore"]['teams'][team]['players'][player]['person']['fullName']
                    data['position'] = game['liveData']["boxscore"]['teams'][team]['players'][player]['position']['code']
                    data['homeAway'] = team
                    data['teamID'] = game['gameData']['teams'][team]['id']
                    data['teamName'] = game['gameData']['teams'][team]['name']
                    if isinstance(game['liveData']["boxscore"]['teams'][team]['players'][player]['stats']['goalieStats'], dict):
                        for key in game['liveData']["boxscore"]['teams'][team]['players'][player]['stats']['goalieStats'].keys():
                            data[key] = game['liveData']["boxscore"]['teams'][team]['players'][player]['stats']['goalieStats'][key]
                    yield(data)
                else: 
                    continue
    except: 
        print("Game not found")


def get_goalie_stats_season(season):
    """
    Arguments:
        season - Start of a particular season. Character. Example: "2017"
                 for the 2017/2018 season
    Returns:
        All regular season team stats for a specified season. One row for home, one for away.
    Example: 
        import pandas as pd
        import requests
        # takes a few minutes to run
        pd.DataFrame(get_goalie_stats_season("2019"))
    """
    # setting the base API url for use throughout
    if int(season) == 2012:
        game_range = list(range(1, 721))
    elif int(season) >= 2017:
        game_range = list(range(1, 1272))
    else:
        game_range = list(range(1, 1231))
    for game in game_range:
        game_id = str(game).zfill(4)
        base_api = "https://statsapi.web.nhl.com"
        game_link = f"/api/v1/game/%s/feed/live/"% (season + "02" + game_id)
        # getting the full list of teams
        try:
            game_url = requests.get(base_api + game_link)
            game_url.raise_for_status()
            game = game_url.json()
            for team in ['home', 'away']:
                for player in game['liveData']["boxscore"]['teams'][team]['players']:
                    if game['liveData']["boxscore"]['teams'][team]['players'][player]['position']['code'] == "G":
                        data = {}
                        data['gameID'] = game['gamePk']
                        data['playerID'] = game['liveData']["boxscore"]['teams'][team]['players'][player]['person']['id']
                        data['fullName'] = game['liveData']["boxscore"]['teams'][team]['players'][player]['person']['fullName']
                        data['position'] = game['liveData']["boxscore"]['teams'][team]['players'][player]['position']['code']
                        data['homeAway'] = team
                        data['teamID'] = game['gameData']['teams'][team]['id']
                        data['teamName'] = game['gameData']['teams'][team]['name']
                        if isinstance(game['liveData']["boxscore"]['teams'][team]['players'][player]['stats']['goalieStats'], dict):
                            for key in game['liveData']["boxscore"]['teams'][team]['players'][player]['stats']['goalieStats'].keys():
                                data[key] = game['liveData']["boxscore"]['teams'][team]['players'][player]['stats']['goalieStats'][key]
                        yield(data)
                    else: 
                        continue
        except: 
            print(f"Game %s not found" % (season + "02" + game_id))
