import csv
import numpy as np

def read_normalized_data(filename):
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)
        data = list(reader)
    return headers, np.array(data)

def calculate_player_value_score(player_stats, weights):
    return np.dot(player_stats, weights)

# Read the normalized data from the CSV file
headers, normalized_data = read_normalized_data('normalized_player_stats.csv')

# Exclude players with minimal playing time
min_minutes_played = 100

# Filter players based on minutes played
filtered_data = []
for player in normalized_data:
    minutes_played = float(player[headers.index('MIN')])
    filtered_data.append(player)
filtered_data = np.array(filtered_data)

# Define the weights for each stat (adjust as needed)
weights = {
    'MIN': -1,
    'FGM': 1,
    'FGA': -0.5,
    'FG_PCT': 1,
    'FG3M': 1,
    'FG3A': -0.5,
    'FG3_PCT': 1,
    'FTM': 1,
    'OREB': 1,
    'DREB': 1,
    'REB': 1,
    'AST': 1,
    'TOV': -1,
    'STL': 1,
    'BLK': 1,
    'PTS': 1,
    'PLUS_MINUS': 1
}

# Calculate the player value score for each player
player_values = []
for player in filtered_data:
    player_stats = [float(player[headers.index(stat)]) for stat in weights.keys()]
    value_score = calculate_player_value_score(player_stats, list(weights.values()))
    player_id = player[headers.index('PLAYER_ID')]
    player_name = player[headers.index('PLAYER_NAME')]
    player_values.append((player_id, player_name, value_score))

# Sort the players based on their value score in ascending order
player_values.sort(key=lambda x: x[2])

# Display the top 10 least valuable players
print("Top 10 Least Valuable Players:")
print(player_values)
for i, (player_id, player_name, value_score) in enumerate(player_values[:10], 1):
    print(f"{i}. {player_name} (Value Score: {value_score:.2f})")