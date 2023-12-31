# sports

NBA play-by-play data -> box scores / game data -> aggregated season (team/player) data



Scraping Data - nba_play_by_play_scraper.py
  - Scrapes full season (by season_type - Regular Season / Playoffs) NBA play-by-play data.
  - Saves to csv in the format of : 0022300121
      - 002 / 004 prefix signifies regular season (002) or playoffs (004)
      - Next 2 digits signify season year (22 = 2022-23 season)



current files -

nba_play_by_play_scraper.py : scrapes all season game's play_by_play files.
  - data



box_score_from_pbp.py : Takes an individual game's play-by-play and aggregates to player/team level
- produces box score


Need: MINS, PF, +/- 
Box Score:
![image](https://github.com/kylecallison/sports/assets/100173107/897ead92-afa0-4176-8d16-9d2cb2cd5188)


NEED:
Line Score:

![image](https://github.com/kylecallison/sports/assets/100173107/1c5cd9c7-a8a2-47ee-a943-dc896c2f9312)



download_nba_stats.py : Downloads season stats by player for a given season - use for validating play-by-play aggregation at a a later time.
  - nba_stats -> sports\nba_stats\stats_nba_player_data_1998-99.csv



pbp_defense.py : used for determining rebounds between players, logic for off/def reb should work.
  - produces rebounds.csv



