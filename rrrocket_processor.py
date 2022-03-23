import json
import pandas as pd


def process_match_overview(match_data: dict):
    team_size = match_data['TeamSize']

    blue_team_stats = process_team_stats(0, team_size, match_data)
    orange_team_stats = process_team_stats(1, team_size, match_data)

    return pd.DataFrame.from_dict(blue_team_stats), pd.DataFrame.from_dict(orange_team_stats)


def process_team_stats(team_number: int, team_size: int, match_data: dict) -> dict:
    players = []

    for player in match_data['PlayerStats']:
        if player['Team'] == team_number:
            players.append({
                'Platform': 'PC' if player['Platform']['value'].split('_')[1] in ['Steam', 'Epic'] else 'Console',
                'Name': player['Name'],
                'Score': player['Score'],
                'Goals': player['Goals'],
                'Assists': player['Assists'],
                'Saves': player['Saves'],
                'incomplete': False
            })

    for goal in match_data['Goals']:
        player_names = [player['Name'] for player in players]
        if goal['PlayerTeam'] == team_number:
            # If we aren't tracking this player add them as incomplete
            if goal['PlayerName'] not in player_names:
                players.append({
                    'Platform': 'N/A',
                    'Name': goal['PlayerName'],
                    'Score': 'N/A',
                    'Goals': 1,
                    'Assists': 'N/A',
                    'Saves': 'N/A',
                    'incomplete': True
                })
            # If we are tracking this player, and they are incomplete we need to manually bump goals
            elif goal['PlayerName'] in player_names:
                for player in players:
                    if player['Name'] == goal['PlayerName'] and player['incomplete']:
                        player['Goals'] += 1

    # Build dataframe structure
    team_stats = {
        'Platform': [player['Platform'] for player in players],
        'PlayerName': [player['Name'] for player in players],
        'Score': [player['Score'] for player in players],
        'Goals': [player['Goals'] for player in players],
        'Assists': [player['Assists'] for player in players],
        'Saves': [player['Saves'] for player in players]
    }

    # Fill unknowns until we match team_size
    while len(team_stats['PlayerName']) < team_size:
        team_stats['Players'].append('Unknown Player')
        team_stats['Score'].append('N/A')
        team_stats['Goals'].append('N/A')
        team_stats['Assists'].append('N/A')
        team_stats['Saves'].append('N/A')
        team_stats['Platform'].append('N/A')

    return team_stats
