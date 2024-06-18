import csv

def calculate_age_factor(age):
    if age < 21:
        return 0.85
    elif age > 35:
        return 1.15
    else:
        return 0.85 + (age - 21) * (1.15 - 0.85) / (35 - 21)

def calculate_overpaid_metric(player_data):
    gp_norm = player_data['GP']
    min_norm = player_data['MIN']
    fg_pct_norm = player_data['FG_PCT']
    fg3_pct_norm = player_data['FG3_PCT']
    ft_pct_norm = player_data['FT_PCT']
    oreb_norm = player_data['OREB']
    dreb_norm = player_data['DREB']
    ast_norm = player_data['AST']
    tov_norm = player_data['TOV']
    stl_norm = player_data['STL']
    blk_norm = player_data['BLK']
    pts_norm = player_data['PTS']
    plus_minus_norm = player_data['PLUS_MINUS']
    ws_48_norm = player_data['WS/48']
    bpm_norm = player_data['BPM']
    vorp_norm = player_data['VORP']
    per_norm = player_data['PER']

    age = player_data['Age']
    position = player_data['Pos']

    # Adjust weights based on player's position
    position_weights = {
        'C': {'BLK': 0.09, 'FG_PCT': 0.05, 'FG3_PCT': 0.03, 'FT_PCT': 0.03, 'OREB': 0.05, 'DREB': 0.03, 'PTS': 0.18},
        'PG': {'AST': 0.05, 'PTS': 0.24, 'FG_PCT': 0.08, 'FT_PCT': 0.06, 'FG3_PCT': 0.07, 'OREB': 0.02, 'DREB': 0.02},
        'SG': {'PTS': 0.24, 'AST': 0.04},
        'SF': {'PTS': 0.22, 'AST': 0.03, 'BLK': 0.03},
        'PF': {'BLK': 0.05, 'PTS': 0.20, 'AST': 0.02}
    }

    position_weight = position_weights.get(position, {})
    blk_weight = position_weight.get('BLK', 0.03)
    pts_weight = position_weight.get('PTS', 0.21)
    ast_weight = position_weight.get('AST', 0.03)
    fg_pct_weight = position_weight.get('FG_PCT', 0.07)
    ft_pct_weight = position_weight.get('FT_PCT', 0.05)
    fg3_pct_weight = position_weight.get('FG3_PCT', 0.05)
    oreb_weight = position_weight.get('OREB', 0.03)
    dreb_weight = position_weight.get('DREB', 0.03)

    value_score = (
        (0.02 * gp_norm) + (0.05 * min_norm) + (fg_pct_weight * fg_pct_norm) + (fg3_pct_weight * fg3_pct_norm) +
        (ft_pct_weight * ft_pct_norm) + (oreb_weight * oreb_norm) + (dreb_weight * dreb_norm) + (ast_weight * ast_norm) +
        (-0.05 * tov_norm) + (0.02 * stl_norm) + (blk_weight * blk_norm) + (pts_weight * pts_norm) +
        (0.8 * plus_minus_norm) + (0.04 * ws_48_norm) + (0.05 * bpm_norm) + (0.07 * vorp_norm) +
        (0.20 * per_norm)
    )

    salary = player_data['SALARY']
    age_factor = calculate_age_factor(age)
    overpaid_metric = salary / (value_score * age_factor) if value_score != 0 else 0
    overpaid_metric = overpaid_metric / 10000000

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