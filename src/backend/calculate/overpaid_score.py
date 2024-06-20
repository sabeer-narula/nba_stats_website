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

def calculate_overpaid_metric(player_data):
    POSITION_WEIGHTS = {
        'C': {'BLK': 0.10, 'PTS': 0.23, 'AST': 0.04, 'FG_PCT': 0.04, 'FT_PCT': 0.03, 'FG3_PCT': 0.02, 'OREB': 0.05, 'DREB': 0.05},
        'PG': {'BLK': 0.01, 'PTS': 0.28, 'AST': 0.06, 'FG_PCT': 0.06, 'FT_PCT': 0.05, 'FG3_PCT': 0.05, 'OREB': 0.02, 'DREB': 0.02},
        'SG': {'BLK': 0.01, 'PTS': 0.29, 'AST': 0.04, 'FG_PCT': 0.06, 'FT_PCT': 0.05, 'FG3_PCT': 0.05, 'OREB': 0.03, 'DREB': 0.02},
        'SF': {'BLK': 0.04, 'PTS': 0.26, 'AST': 0.04, 'FG_PCT': 0.05, 'FT_PCT': 0.04, 'FG3_PCT': 0.04, 'OREB': 0.04, 'DREB': 0.04},
        'PF': {'BLK': 0.05, 'PTS': 0.26, 'AST': 0.04, 'FG_PCT': 0.04, 'FT_PCT': 0.04, 'FG3_PCT': 0.02, 'OREB': 0.05, 'DREB': 0.05}
    }

    DEFAULT_WEIGHTS = {
        'BLK': 0.03,
        'PTS': 0.25,
        'AST': 0.04,
        'FG_PCT': 0.07,
        'FT_PCT': 0.04,
        'FG3_PCT': 0.05,
        'OREB': 0.03,
        'DREB': 0.03
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
    for stat in ['GP', 'FG_PCT', 'TOV', 'PTS', 'PLUS_MINUS', 'PER']:
        percentiles[stat] = player_data[stat]

    if position == 'C':
        for stat in ['BLK', 'OREB', 'DREB']:
            percentiles[stat] = player_data[stat]

    elif position in ['PG', 'SG']:
        for stat in ['FT_PCT', 'FG3_PCT']:
            percentiles[stat] = player_data[stat]

    return overpaid_metric, percentiles

def calculate_percentile(value, data):
    count = sum(1 for v in data if v <= value)
    percentile = count / len(data)
    return percentile

def main():
    # Read the CSV file
    with open('/Users/sabeernarula/Desktop/NBA-Stats/NBA-Stats/src/backend/data/merged_normalized_player_stats.csv', 'r') as file:
        csv_reader = csv.DictReader(file)
        all_players_data = list(csv_reader)
        players = []
        for row in all_players_data:
            # Convert numeric values to floats, skipping empty strings
            for key in row:
                if key not in ['PLAYER_NAME', 'PLAYER_ID', 'Pos']:
                    if row[key] != '':
                        row[key] = float(row[key])
                    else:
                        row[key] = 0.0

            # Check if the player has a valid salary
            if row['SALARY'] > 0:
                overpaid_metric, percentiles = calculate_overpaid_metric(row)
                player_info = {
                    'name': row['PLAYER_NAME'],
                    'salary': row['SALARY'],
                    'GP': row['GP'],
                    'minutes': row['MIN'],
                    'overpaid_metric': overpaid_metric,
                    'percentiles': percentiles
                }
                players.append(player_info)

    # Filter players with salary under $10 million for the most overpaid list
    overpaid_players = [player for player in players if player['salary'] >= 10000000]
    overpaid_players.sort(key=lambda x: x['overpaid_metric'], reverse=True)
    print("Top 20 Most Overpaid Players (Salary >= $10 million):")
    for i, player in enumerate(overpaid_players[:20], start=1):
        worst_percentiles = sorted(player['percentiles'].items(), key=lambda x: x[1])[:3]
        worst_stats = [f"{stat}: {percentile:.2f}" for stat, percentile in worst_percentiles]
        print(f"{i}. {player['name']}: ${player['salary']}: Overpaid Metric: {player['overpaid_metric']:.2f}. Worst percentiles: {', '.join(worst_stats)}")

    print("\nOverpaid Metrics for the 20 Highest Paid Players:")
    players.sort(key=lambda x: x['salary'], reverse=True)
    for i, player in enumerate(players[:20], start=1):
        worst_percentiles = sorted(player['percentiles'].items(), key=lambda x: x[1])[:3]
        worst_stats = [f"{stat}: {percentile:.2f}" for stat, percentile in worst_percentiles]
        print(f"{i}. {player['name']}: ${player['salary']}: Overpaid Metric: {player['overpaid_metric']:.2f}. Worst percentiles: {', '.join(worst_stats)}")

    print("\nTop 20 Most Underpaid Players:")
    valid_players = [player for player in players if (player['salary'] >= 10000000 and (player['GP']*player['minutes'] > 0.3))]
    valid_players.sort(key=lambda x: x['overpaid_metric'])
    for i, player in enumerate(valid_players[:20], start=1):
        best_percentiles = sorted(player['percentiles'].items(), key=lambda x: x[1], reverse=True)[:3]
        best_stats = [f"{stat}: {percentile:.2f}" for stat, percentile in best_percentiles]
        print(f"{i}. {player['name']}: ${player['salary']}: Underpaid Metric: {player['overpaid_metric']:.2f}. Best percentiles: {', '.join(best_stats)}")

if __name__ == '__main__':
    main()

# def generate_overpaid_chart(overpaid_players):
#     names = [player['name'] for player in overpaid_players]
#     overpaid_metrics = [player['overpaid_metric'] for player in overpaid_players]

#     plt.figure(figsize=(10, 6))
#     plt.bar(names, overpaid_metrics)
#     plt.xticks(rotation=45, ha='right')
#     plt.xlabel('Player')
#     plt.ylabel('Overpaid Metric')
#     plt.title('Top 20 Most Overpaid Players (Salary >= $10 million)')
#     plt.tight_layout()
#     plt.savefig('/Users/sabeernarula/Downloads/nba_stats_website/nba_stats_website/website/static/overpaid_chart.png')
#     plt.close()

# def generate_highest_paid_chart(highest_paid_players):
#     names = [player['name'] for player in highest_paid_players]
#     overpaid_metrics = [player['overpaid_metric'] for player in highest_paid_players]

#     plt.figure(figsize=(8, 8))
#     plt.pie(overpaid_metrics, labels=names, autopct='%1.1f%%')
#     plt.title('Overpaid Metrics for the 20 Highest Paid Players')
#     plt.tight_layout()
#     plt.savefig('/Users/sabeernarula/Downloads/nba_stats_website/nba_stats_website/website/static/highest_paid_chart.png')
#     plt.close()

# def generate_underpaid_chart(underpaid_players):
#     names = [player['name'] for player in underpaid_players]
#     underpaid_metrics = [player['overpaid_metric'] for player in underpaid_players]

#     plt.figure(figsize=(8, 8))
#     sns.set(style='whitegrid')
#     sns.lineplot(x=names, y=underpaid_metrics, marker='o')
#     plt.xticks(rotation=45, ha='right')
#     plt.xlabel('Player')
#     plt.ylabel('Underpaid Metric')
#     plt.title('Top 20 Most Underpaid Players')
#     plt.tight_layout()
#     plt.savefig('/Users/sabeernarula/Downloads/nba_stats_website/nba_stats_website/website/static/underpaid_chart.png')
#     plt.close()

def get_overpaid_underpaid_data():
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
                overpaid_metric, _ = calculate_overpaid_metric(row)
                player_info = {
                    'name': row['PLAYER_NAME'],
                    'salary': row['SALARY'],
                    'GP': row['GP'],
                    'minutes': row['MIN'],
                    'overpaid_metric': overpaid_metric
                }
                players.append(player_info)

    # Filter players with salary under $10 million for the most overpaid list
    overpaid_players = [player for player in players if player['salary'] >= 10000000]
    overpaid_players.sort(key=lambda x: x['overpaid_metric'], reverse=True)

    # Get the 20 highest paid players
    highest_paid_players = sorted(players, key=lambda x: x['salary'], reverse=True)[:20]

    # Get the top 20 most underpaid players
    valid_players = [player for player in players if (player['salary'] >= 10000000 and (player['GP']*player['minutes'] > 0.3))]
    valid_players.sort(key=lambda x: x['overpaid_metric'])
    underpaid_players = valid_players[:25]

    # generate_overpaid_chart(overpaid_players[:20])
    # generate_highest_paid_chart(highest_paid_players)
    # generate_underpaid_chart(underpaid_players[:20])

    return {
        'overpaid_players': overpaid_players[:40],
        'highest_paid_players': highest_paid_players,
        'underpaid_players': underpaid_players
    }
