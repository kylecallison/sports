# scrape NBA stats play by play data

import time
import pandas as pd
import requests
import datetime
import os
import json


#from players_on_court import calculate_time_at_period, split_subs, frame_to_row, advanced_boxscore_url


pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

# 7:39
# 22-23 Time: 

# Headers for API Request
header_data  = {
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/plain, */*',
    'x-nba-stats-token': 'true',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    'x-nba-stats-origin': 'stats',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Referer': 'https://stats.nba.com/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
}

# constants for season type
regular_season = 'Regular Season'
playoffs = 'Playoffs'

# build play by play url
def play_by_play_url(game_id):
    return "https://stats.nba.com/stats/playbyplayv2/?gameId={0}&startPeriod=0&endPeriod=14".format(game_id)

# build game log url
def game_log_url(season, season_type):
    return "http://stats.nba.com/stats/leaguegamelog/?leagueId=00&season={}&seasonType={}&playerOrTeam=T&counter=0&sorter=PTS&direction=ASC&dateFrom=&dateTo=".format(season, season_type)

# extracts pbp data from api response
def extract_data(url):
    print(url)
    r = requests.get(url, headers=header_data)
    resp = r.json()
    results = resp['resultSets'][0]
    headers = results['headers']
    rows = results['rowSet']
    frame = pd.DataFrame(rows)
    frame.columns = headers
    return frame


###
### Download and Save Play by Play Data
###




def download_pbp(game_id):
    pbp_file_path = "data/{}_pbp.csv".format(game_id)
    # Check to see if the game pbp file already exists / has already been downloaded
    if os.path.exists(pbp_file_path):
        print("Play-by-play data for {} already exists. Skipping to the next game.".format(game_id))
        return
    
    try:
        play_by_play = extract_data(play_by_play_url(game_id))
        play_by_play.to_csv(pbp_file_path, index=False)
        print("Downloaded {}".format(game_id))
    except json.decoder.JSONDecodeError:
        print("Error: Failed to decode JSON response for game_id {}".format(game_id))






# Set the seasons and season types
current_year = datetime.datetime.now().year 

previous_seasons = 0
seasons = [str(year) + '-' + str(year+1)[-2:] for year in range(current_year-previous_seasons, current_year+1)]

season_types = [regular_season]
if playoffs in season_types:
    season_types.append(playoffs)



# Create a list to store all the schedules
all_schedules = []

# Iterate over the seasons and season types
for season in seasons:
    for season_type in season_types:
        print("Schedule For Current Season: {}".format(season))
        # Check if the schedule file already exists
        schedule_file_path = 'data/schedules/schedule_{}_{}.csv'.format(season, season_type)
        if os.path.exists(schedule_file_path):
            print("Schedule for {} already exists. Skipping to the next season.".format(season))
            break
    # Download the league game log
    schedule = extract_data(game_log_url(season, season_type))
    # Save the game log in case you want it for future reference
    schedule.to_csv('data/schedules/schedule_{}_{}.csv'.format(season, season_type), index=False)
    # Append the schedule to the list
    all_schedules.append(schedule)

    # Check if the current season is the current year
    if season == str(current_year):
        break


# Get all of the unique game ids from all the schedules
game_ids = pd.concat(all_schedules)['GAME_ID'].dropna().unique()



# Iterate over the seasons and season types
for season in seasons:
    print("Current Season: {}".format(season))
    for season_type in season_types:
        # Download the league game log
        schedule = extract_data(game_log_url(season, season_type))
        

        # Get all of the unique game ids
        game_ids = schedule['GAME_ID'].unique()
        # For each game id, download the play by play then sleep for .75 seconds so that we don't hit the stats nba rate limit
        for index, id in enumerate(game_ids):
            download_pbp(id)
            remaining_games = len(game_ids) - index - 1
            print("Remaining games in {} {}: {}".format(season, season_type, remaining_games))
            time.sleep(.75)






