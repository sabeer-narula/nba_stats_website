import csv
from django.shortcuts import render
from nba_api.stats.endpoints import leagueleaders, leaguedashplayerstats

def get_leaders(category):
    leaders = leagueleaders.LeagueLeaders(season="2023-24", stat_category_abbreviation=category)
    data = leaders.get_dict()['resultSet']
    headers = data['headers']
    rows = data['rowSet']
    return headers, rows

def get_top_and_bottom(headers, rows, category):
    category_index = headers.index(category)
    sorted_rows = sorted(rows, key=lambda x: x[category_index], reverse=True)
    top_5 = sorted_rows[:5]
    bottom_5 = sorted_rows[-5:]
    top_5_players = [{'rank': row[headers.index("RANK")], 'player': row[headers.index("PLAYER")], 'value': row[category_index]} for row in top_5]
    bottom_5_players = [{'rank': row[headers.index("RANK")], 'player': row[headers.index("PLAYER")], 'value': row[category_index]} for row in bottom_5]
    return top_5_players, bottom_5_players

def get_player_stats():
    stats = leaguedashplayerstats.LeagueDashPlayerStats(season="2023-24", per_mode_detailed="PerGame")
    data = stats.get_dict()['resultSets'][0]
    headers = data['headers']
    rows = data['rowSet']
    return headers, rows

def save_to_csv(headers, rows, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(rows)

def home(request):
    categories = {
        "PTS": "Points Per Game",
        "REB": "Rebounds",
        "AST": "Assists",
        "STL": "Steals",
        "MIN": "Minutes",
        "BLK": "Blocks"
    }
    data = {}
    for abbreviation, full_name in categories.items():
        headers, rows = get_leaders(abbreviation)
        top_5, bottom_5 = get_top_and_bottom(headers, rows, abbreviation)
        data[full_name] = {
            'top_5': top_5,
            'bottom_5': bottom_5
        }

    # Get player stats and save to CSV
    player_stats_headers, player_stats_rows = get_player_stats()
    save_to_csv(player_stats_headers, player_stats_rows, 'player_stats.csv')

    return render(request, 'index.html', {'data': data})