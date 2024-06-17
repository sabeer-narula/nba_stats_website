import csv
import math

def calculate_overpaid_metric(player_data):
    ppg = player_data['PTS']
    apg = player_data['AST']
    rpg = player_data['REB']
    spg = player_data['STL']
    bpg = player_data['BLK'] * 0.33  # Reduced weighting for blocks
    topg = player_data['TOV']
    salary = player_data['SALARY']
    minutes_played = player_data['MIN']
    fg_pct = player_data['FG_PCT']
    fg3_pct = player_data['FG3_PCT'] if player_data['FG3_PCT'] != '**' else 0
    ftm = player_data['FTM']
    fta = player_data['FTA']

    # Calculate additional metrics
    efg_pct = (player_data['FGM'] + 0.5 * player_data['FG3M']) / player_data['FGA'] if player_data['FGA'] > 0 else 0
    ts_pct = ppg / (2 * (player_data['FGA'] + 0.44 * fta)) if (player_data['FGA'] + 0.44 * fta) > 0 else 0
    per = (ppg + rpg + apg + spg + bpg - topg) * (1 / minutes_played) if minutes_played > 0 else 0

    # Calculate the overpaid metric
    try:
        if minutes_played > 0 and (ppg + apg + rpg + spg + bpg) > 0:
            overpaid_metric = salary / (minutes_played * (ppg + apg + rpg + spg + bpg) * (efg_pct + fg_pct + fg3_pct + ts_pct) / (topg + 1))
            overpaid_metric = overpaid_metric / 10000000
        else:
            overpaid_metric = 0
    except ZeroDivisionError:
        overpaid_metric = 0

    # Determine the stat that contributed the most to the overpaid metric
    stats = {'PTS': ppg, 'AST': apg, 'REB': rpg, 'STL': spg, 'BLK': 3*bpg, 'TOV': topg}
    worst_stat = min(stats, key=stats.get)

    return overpaid_metric, worst_stat, per

def main():
    # Read the CSV file
    with open('updated_basketball_data.csv', 'r') as file:
        csv_reader = csv.DictReader(file)
        players = []
        for row in csv_reader:
            # Convert numeric values to floats, skipping empty strings
            for key in row:
                if key != 'PLAYER_NAME' and key != 'PLAYER_ID':
                    if row[key] != '':
                        row[key] = float(row[key])
                    else:
                        row[key] = 0.0  # or assign a default value

            # Check if the player has a valid salary
            if row['SALARY'] > 0:
                overpaid_metric, worst_stat, per = calculate_overpaid_metric(row)
                player_info = {
                    'name': row['PLAYER_NAME'],
                    'salary': row['SALARY'],
                    'overpaid_metric': overpaid_metric,
                    'worst_stat': worst_stat,
                    'per': per
                }
                players.append(player_info)

    # Filter players with salary under $10 million for the most overpaid list
    overpaid_players = [player for player in players if player['salary'] >= 10000000]
    overpaid_players.sort(key=lambda x: x['overpaid_metric'], reverse=True)

    print("Top 20 Most Overpaid Players (Salary >= $10 million):")
    for i, player in enumerate(overpaid_players[:20], start=1):
        print(f"{i}. {player['name']}: ${player['salary']}: Overpaid Metric: {player['overpaid_metric']:.2f}: Worst Stat: {player['worst_stat']}: PER: {player['per']:.2f}")

    print("\nOverpaid Metrics for the 20 Highest Paid Players:")
    players.sort(key=lambda x: x['salary'], reverse=True)
    for i, player in enumerate(players[:20], start=1):
        print(f"{i}. {player['name']}: ${player['salary']}: Overpaid Metric: {player['overpaid_metric']:.2f}: Worst Stat: {player['worst_stat']}: PER: {player['per']:.2f}")

    print("\nTop 20 Most Underpaid Players:")
    valid_players = [player for player in players if player['salary'] > 10000000]
    valid_players.sort(key=lambda x: x['overpaid_metric'])
    for i, player in enumerate(valid_players[:20], start=1):
        print(f"{i}. {player['name']}: ${player['salary']}: Underpaid Metric: {player['overpaid_metric']:.2f}")

if __name__ == '__main__':
    main()