import json

import pandas as pd
import urllib3
import datetime
import time

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

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


# endpoints
def player_stats_url(season):
    return "https://stats.nba.com/stats/leaguedashplayerstats?College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=Totals&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season={0}&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&TwoWay=0&VsConference=&VsDivision=&Weight=".format(
        season)


# Extract json
def extract_data(http_client, url):
    r = http_client.request('GET', url, headers=header_data)    # Call the GET endpoint
    resp = json.loads(r.data)                                   # Convert the response to a json object
    results = resp['resultSets'][0]                             # take the first item in the resultsSet (This can be determined by inspection of the json response)
    headers = results['headers']                                # take the headers of the response (our column names)
    rows = results['rowSet']                                    # take the rows of our response
    frame = pd.DataFrame(rows)                                  # convert the rows to a dataframe
    frame.columns = headers                                     # set our column names using the  extracted headers
    return frame


client = urllib3.PoolManager()
#season = "2015-16"

#frame = extract_data(client, player_stats_url(season))

#frame.to_csv("nba_stats/stats_nba_player_data_{0}.csv".format(season), index=False)


current_year = datetime.datetime.now().year


# Loop through alotted timeframe (in this case the last 25 years)
for year in range(current_year - 25, current_year + 1):
    season = f"{year}-{str(year+1)[-2:]}"
    frame = extract_data(client, player_stats_url(season))
    frame.to_csv(f"nba_stats/stats_nba_player_data_{season}.csv", index=False)
    time.sleep(.75)
    print(f"Downloaded {season} data")
    if year == current_year:
        break    
    else:
        continue
