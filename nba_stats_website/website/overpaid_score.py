import csv

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
        'C': {'BLK': 0.09, 'PTS': 0.18, 'AST': 0.04, 'FG_PCT': 0.04, 'FT_PCT': 0.03, 'FG3_PCT': 0.02, 'OREB': 0.05, 'DREB': 0.05},
        'PG': {'BLK': 0.01, 'PTS': 0.23, 'AST': 0.06, 'FG_PCT': 0.06, 'FT_PCT': 0.05, 'FG3_PCT': 0.05, 'OREB': 0.02, 'DREB': 0.02},
        'SG': {'BLK': 0.01, 'PTS': 0.24, 'AST': 0.04, 'FG_PCT': 0.06, 'FT_PCT': 0.05, 'FG3_PCT': 0.05, 'OREB': 0.03, 'DREB': 0.02},
        'SF': {'BLK': 0.04, 'PTS': 0.21, 'AST': 0.04, 'FG_PCT': 0.05, 'FT_PCT': 0.04, 'FG3_PCT': 0.04, 'OREB': 0.04, 'DREB': 0.04},
        'PF': {'BLK': 0.05, 'PTS': 0.21, 'AST': 0.04, 'FG_PCT': 0.04, 'FT_PCT': 0.04, 'FG3_PCT': 0.02, 'OREB': 0.05, 'DREB': 0.05}
    }

    DEFAULT_WEIGHTS = {
        'BLK': 0.03,
        'PTS': 0.21,
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
        (gp_weight * player_data['GP']) + (0.05 * player_data['MIN']) +
        (weights['FG_PCT'] * player_data['FG_PCT']) + (weights['FG3_PCT'] * player_data['FG3_PCT']) +
        (weights['FT_PCT'] * player_data['FT_PCT']) + (weights['OREB'] * player_data['OREB']) +
        (weights['DREB'] * player_data['DREB']) + (weights['AST'] * player_data['AST']) +
        (-0.04 * player_data['TOV']) + (0.02 * player_data['STL']) + (weights['BLK'] * player_data['BLK']) +
        (weights['PTS'] * player_data['PTS']) + (0.8 * player_data['PLUS_MINUS']) +
        (0.04 * player_data['WS/48']) + (0.05 * player_data['BPM']) + (0.07 * player_data['VORP']) +
        (0.20 * player_data['PER'])
    )

    salary = player_data['SALARY']
    age_factor = calculate_age_factor(player_data['Age'])
    overpaid_metric = (salary / (value_score * age_factor)) / 10000000 if value_score != 0 else 0
    return overpaid_metric

def main():
    # Read the CSV file
    with open('merged_normalized_player_stats.csv', 'r') as file:
        csv_reader = csv.DictReader(file)
        players = []
        for row in csv_reader:
            # Convert numeric values to floats, skipping empty strings
            for key in row:
                if key not in ['PLAYER_NAME', 'PLAYER_ID', 'Pos']:
                    if row[key] != '':
                        row[key] = float(row[key])
                    else:
                        row[key] = 0.0  # or assign a default value

            # Check if the player has a valid salary
            if row['SALARY'] > 0:
                overpaid_metric = calculate_overpaid_metric(row)
                player_info = {
                    'name': row['PLAYER_NAME'],
                    'salary': row['SALARY'],
                    'overpaid_metric': overpaid_metric
                }
                players.append(player_info)


    # Filter players with salary under $10 million for the most overpaid list
    overpaid_players = [player for player in players if player['salary'] >= 10000000]
    overpaid_players.sort(key=lambda x: x['overpaid_metric'], reverse=True)
    print("Top 20 Most Overpaid Players (Salary >= $10 million):")
    for i, player in enumerate(overpaid_players[:20], start=1):
        print(f"{i}. {player['name']}: ${player['salary']}: Overpaid Metric: {player['overpaid_metric']:.2f}")

    print("\nOverpaid Metrics for the 20 Highest Paid Players:")
    players.sort(key=lambda x: x['salary'], reverse=True)
    for i, player in enumerate(players[:20], start=1):
        print(f"{i}. {player['name']}: ${player['salary']}: Overpaid Metric: {player['overpaid_metric']:.2f}")

    print("\nTop 20 Most Underpaid Players:")
    valid_players = [player for player in players if player['salary'] > 10000000]
    valid_players.sort(key=lambda x: x['overpaid_metric'])
    for i, player in enumerate(valid_players[:20], start=1):
        print(f"{i}. {player['name']}: ${player['salary']}: Underpaid Metric: {player['overpaid_metric']:.2f}")

if __name__ == '__main__':
    main()