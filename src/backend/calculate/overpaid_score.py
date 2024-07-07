import csv
from matplotlib import pyplot as plt
import matplotlib
import seaborn as sns

matplotlib.use('Agg')

def calculate_age_factor(age):
    if age < 21:
        return 0.85
    elif age > 35:
        return 1.15
    else:
        return 0.85 + (age - 21) * (1.15 - 0.85) / (35 - 21)
    
def calculate_gp_weight(games_played):
    if games_played < 25:
        return 0.4
    elif games_played >= 75:
        return 0.05
    else:
        return 0.4 - (games_played - 25) * (0.4 - 0.05) / (75 - 25)

def load_original_stats():
    per_stats = {}
    player_stats = {}
    
    with open('/Users/sabeernarula/Desktop/NBA-Stats/NBA-Stats/src/backend/data/per.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            per_stats[row['Player']] = row
    
    with open('/Users/sabeernarula/Desktop/NBA-Stats/NBA-Stats/src/backend/data/player_stats.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            player_stats[row['PLAYER_NAME']] = row
    
    return per_stats, player_stats

def get_original_stat(player_name, stat, per_stats, player_stats):
    if stat in ['PER', 'VORP']:
        return float(per_stats.get(player_name, {}).get(stat, 0))
    else:
        return float(player_stats.get(player_name, {}).get(stat, 0))

def calculate_overpaid_metric(player_data, per_stats, player_stats):
    POSITION_WEIGHTS = {
        'C': {'BLK': 0.10, 'PTS': 0.23, 'AST': 0.04, 'FG_PCT': 0.04, 'FT_PCT': 0.03, 'FG3_PCT': 0.02, 'OREB': 0.05, 'DREB': 0.05},
        'PG': {'BLK': 0.01, 'PTS': 0.28, 'AST': 0.06, 'FG_PCT': 0.06, 'FT_PCT': 0.05, 'FG3_PCT': 0.05, 'OREB': 0.02, 'DREB': 0.02},
        'SG': {'BLK': 0.01, 'PTS': 0.29, 'AST': 0.04, 'FG_PCT': 0.06, 'FT_PCT': 0.05, 'FG3_PCT': 0.05, 'OREB': 0.03, 'DREB': 0.02},
        'SF': {'BLK': 0.04, 'PTS': 0.26, 'AST': 0.04, 'FG_PCT': 0.05, 'FT_PCT': 0.04, 'FG3_PCT': 0.04, 'OREB': 0.04, 'DREB': 0.04},
        'PF': {'BLK': 0.05, 'PTS': 0.26, 'AST': 0.04, 'FG_PCT': 0.04, 'FT_PCT': 0.04, 'FG3_PCT': 0.02, 'OREB': 0.05, 'DREB': 0.05}
    }

    DEFAULT_WEIGHTS = {
        'BLK': 0.03, 'PTS': 0.25, 'AST': 0.04, 'FG_PCT': 0.07, 'FT_PCT': 0.04, 'FG3_PCT': 0.05, 'OREB': 0.03, 'DREB': 0.03
    }

    position = player_data['Pos']
    position_weights = POSITION_WEIGHTS.get(position, {})
    weights = {**DEFAULT_WEIGHTS, **position_weights}
    gp_weight = calculate_gp_weight(player_data['GP'])

    value_score = (
        (gp_weight * player_data['GP']) + (0.06 * player_data['MIN']) +
        (weights['FG_PCT'] * player_data['FG_PCT']) + (weights['FG3_PCT'] * player_data['FG3_PCT']) +
        (weights['FT_PCT'] * player_data['FT_PCT']) + (weights['OREB'] * player_data['OREB']) +
        (weights['DREB'] * player_data['DREB']) + (weights['AST'] * player_data['AST']) +
        (-0.04 * player_data['TOV']) + (0.02 * player_data['STL']) + (weights['BLK'] * player_data['BLK']) +
        (weights['PTS'] * player_data['PTS']) + (0.08 * player_data['PLUS_MINUS']) +
        (0.06 * player_data['WS/48']) + (0.05 * player_data['BPM']) + (0.08 * player_data['VORP']) +
        (0.26 * player_data['PER'])
    )

    salary = player_data['SALARY']
    age_factor = calculate_age_factor(player_data['Age'])
    overpaid_metric = (salary / (value_score * age_factor)) / 10000000 if value_score != 0 else 0
    
    percentiles = {}
    stats_to_check = ['GP', 'FG_PCT', 'TOV', 'PTS', 'PLUS_MINUS']
    
    if position in ['C', 'PF']:
        stats_to_check.extend(['BLK', 'OREB', 'DREB'])
    
    if position in ['PG', 'SG']:
        stats_to_check.extend(['AST', 'FT_PCT', 'FG3_PCT'])

    for stat in stats_to_check:
        normalized_value = player_data[stat]
        original_value = get_original_stat(player_data['PLAYER_NAME'], stat, per_stats, player_stats)
        
        if stat == 'FG3_PCT' and normalized_value > 0.32:
            continue
        if stat == 'FG_PCT' and normalized_value > 0.42:
            continue
        if stat == 'FT_PCT' and normalized_value > 0.70:
            continue
        if stat == 'PTS' and original_value > 20:
            continue
        if stat == 'TOV' and original_value < 1:
            continue
        if stat == 'AST' and original_value > 5:
            continue
        if stat == 'GP' and original_value > 65:
            continue
        percentiles[stat] = (normalized_value, original_value)

    return overpaid_metric, percentiles

def main():
    per_stats, player_stats = load_original_stats()
    
    with open('/Users/sabeernarula/Desktop/NBA-Stats/NBA-Stats/src/backend/data/merged_normalized_player_stats.csv', 'r') as file:
        csv_reader = csv.DictReader(file)
        all_players_data = list(csv_reader)
        players = []
        for row in all_players_data:
            for key in row:
                if key not in ['PLAYER_NAME', 'PLAYER_ID', 'Pos']:
                    row[key] = float(row[key]) if row[key] != '' else 0.0

            if row['SALARY'] > 0:
                overpaid_metric, percentiles = calculate_overpaid_metric(row, per_stats, player_stats)
                player_info = {
                    'name': row['PLAYER_NAME'],
                    'salary': row['SALARY'],
                    'GP': row['GP'],
                    'minutes': row['MIN'],
                    'overpaid_metric': overpaid_metric,
                    'percentiles': percentiles
                }
                players.append(player_info)

    overpaid_players = [player for player in players if player['salary'] >= 10000000]
    overpaid_players.sort(key=lambda x: x['overpaid_metric'], reverse=True)
    print("Top 20 Most Overpaid Players (Salary >= $10 million):")
    for i, player in enumerate(overpaid_players[:100], start=1):
        worst_percentiles = sorted(player['percentiles'].items(), key=lambda x: x[1][0])[:3]
        worst_stats = [f"{stat}: {original_value:.1f}" for stat, (_, original_value) in worst_percentiles]
        print(f"{i}. {player['name']}: ${player['salary']}: Overpaid Metric: {player['overpaid_metric']:.2f}. Worst stats: {', '.join(worst_stats)}")

    print("\nOverpaid Metrics for the 20 Highest Paid Players:")
    players.sort(key=lambda x: x['salary'], reverse=True)
    for i, player in enumerate(players[:20], start=1):
        worst_percentiles = sorted(player['percentiles'].items(), key=lambda x: x[1][0])[:3]
        worst_stats = [f"{stat}: {original_value:.1f}" for stat, (_, original_value) in worst_percentiles]
        print(f"{i}. {player['name']}: ${player['salary']}: Overpaid Metric: {player['overpaid_metric']:.2f}. Worst stats: {', '.join(worst_stats)}")

    print("\nTop 20 Most Underpaid Players:")
    valid_players = [player for player in players if (player['salary'] >= 10000000 and (player['GP']*player['minutes'] > 0.3))]
    valid_players.sort(key=lambda x: x['overpaid_metric'])
    for i, player in enumerate(valid_players[:100], start=1):
        best_percentiles = sorted(player['percentiles'].items(), key=lambda x: x[1][0], reverse=True)[:3]
        best_stats = [f"{stat}: {original_value:.1f}" for stat, (_, original_value) in best_percentiles]
        print(f"{i}. {player['name']}: ${player['salary']}: Underpaid Metric: {player['overpaid_metric']:.2f}. Best stats: {', '.join(best_stats)}")

if __name__ == '__main__':
    main()

def get_overpaid_underpaid_data():
    per_stats, player_stats = load_original_stats()
    players = []
    with open('/Users/sabeernarula/Desktop/NBA-Stats/NBA-Stats/src/backend/data/merged_normalized_player_stats.csv', 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            # Convert numeric values to floats, skipping empty strings
            for key in row:
                if key not in ['PLAYER_NAME', 'PLAYER_ID', 'Pos']:
                    if row[key] != '':
                        row[key] = float(row[key])
                    else:
                        row[key] = 0.0

            # Check if the player has a valid salary
            if row['SALARY'] > 0:
                overpaid_metric, percentiles = calculate_overpaid_metric(row, per_stats, player_stats)
                
                # Get worst stats
                worst_stats = sorted(percentiles.items(), key=lambda x: x[1][0])[:5]
                worst_stats = [stat for stat, (norm_val, orig_val) in worst_stats 
                               if stat != 'PLUS_MINUS' or orig_val < 0][:3]
                
                # Get best stats
                best_stats = sorted(percentiles.items(), key=lambda x: x[1][0], reverse=True)[:5]
                best_stats = [stat for stat, (norm_val, orig_val) in best_stats 
                               if stat != 'TOV' and (stat != 'PLUS_MINUS' or orig_val > 1)][:3]
                
                player_info = {
                    'name': row['PLAYER_NAME'],
                    'salary': row['SALARY'],
                    'overpaid_metric': overpaid_metric,
                    'worst_stats': {stat: percentiles[stat][1] for stat in worst_stats},
                    'best_stats': {stat: percentiles[stat][1] for stat in best_stats}
                }
                players.append(player_info)

    # Filter players with salary under $10 million for the most overpaid list
    overpaid_players = [player for player in players if player['salary'] >= 10000000]
    overpaid_players.sort(key=lambda x: x['overpaid_metric'], reverse=True)
    overpaid_players = overpaid_players[:100]  # Slice after sorting

    # Get the 20 highest paid players
    highest_paid_players = sorted(players, key=lambda x: x['salary'], reverse=True)[:20]

    # Get the top 100 most underpaid players
    valid_players = [player for player in players if player['salary'] >= 10000000]
    valid_players.sort(key=lambda x: x['overpaid_metric'])
    underpaid_players = valid_players[:100]

    return {
        'overpaid_players': overpaid_players,
        'highest_paid_players': highest_paid_players,
        'underpaid_players': underpaid_players
    }