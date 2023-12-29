# sports

NBA play-by-play data -> box scores / game data -> aggregated season (team/player) data

current files -

nba_play_by_play_scraper.py : scrapes all season game's play_by_play files.
  - data
  - 
box_score_from_pbp.py : Takes an individual game's play-by-play and aggregates to player/team level
- produces box score

download_nba_stats.py : Downloads season stats by player for a given season - use for validating play-by-play aggregation at a a later time.
  - nba_stats -> sports\nba_stats\stats_nba_player_data_1998-99.csv

pbp_defense.py : used for determining rebounds between players, logic for off/def reb should work.
  - produces rebounds.csv



