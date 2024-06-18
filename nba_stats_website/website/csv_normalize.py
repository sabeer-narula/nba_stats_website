import csv
import numpy as np
from fuzzywuzzy import fuzz

def normalize_data(data):
    min_value = np.min(data, axis=0)
    max_value = np.max(data, axis=0)
    normalized_data = (data - min_value) / (max_value - min_value)
    return normalized_data

def fix_position(position):
    valid_positions = ['C', 'PG', 'SG', 'PF', 'SF']
    if '-' in position:
        position = position.split('-')[0]
    if position not in valid_positions:
        position = 'Unknown'
    return position

# Read the data from the first CSV file
with open('player_stats.csv', 'r') as file:
    reader = csv.reader(file)
    headers1 = next(reader)
    data1 = list(reader)

# Read the data from the second CSV file
with open('per.csv', 'r') as file:
    reader = csv.reader(file)
    headers2 = next(reader)
    data2 = list(reader)

# Create dictionaries to store the data from both files
data1_dict = {row[headers1.index('PLAYER_NAME')]: row for row in data1}
data2_dict = {row[headers2.index('Player')]: row for row in data2}

# Set a threshold for the fuzzy matching ratio (e.g., 90)
threshold = 90

# Create a dictionary to store the merged data
merged_data = {}

# Iterate over each player in data1
for player_name, row1 in data1_dict.items():
    # Find the best match for the player name using fuzzy string matching
    best_match = None
    best_ratio = 0
    for name, row2 in data2_dict.items():
        ratio = fuzz.ratio(player_name, name)
        if ratio > best_ratio:
            best_match = name
            best_ratio = ratio
    
    # Check if the best match ratio is above the threshold
    if best_ratio >= threshold:
        merged_data[player_name] = row1 + data2_dict[best_match]

# Define the columns to keep
columns_to_keep = [
    'PLAYER_ID', 'PLAYER_NAME', 'Pos', 'Age', 'GP', 'MIN', 'FG_PCT', 'FG3_PCT',
    'FT_PCT', 'OREB', 'DREB', 'AST', 'TOV', 'STL', 'BLK', 'PTS',
    'PLUS_MINUS', 'WS/48', 'BPM', 'VORP', 'PER'
]

# Find the indices of the columns to keep
indices_to_keep = [headers1.index(col) if col in headers1 else len(headers1) + headers2.index(col) for col in columns_to_keep]

# Remove unnecessary columns
filtered_data = [[row[i] for i in indices_to_keep] for row in merged_data.values()]

# Fix the position values
for row in filtered_data:
    row[columns_to_keep.index('Pos')] = fix_position(row[columns_to_keep.index('Pos')])

# Convert the data to a NumPy array
np_data = np.array(filtered_data)

# Convert string values to float (skip the first three columns which are PLAYER_ID, PLAYER_NAME, and Pos)
numeric_columns = np_data[:, 3:].astype(float)

# Normalize the data (skip the first three columns which are PLAYER_ID, PLAYER_NAME, and Pos)
normalized_numeric_columns = normalize_data(numeric_columns)

# Round the normalized numeric columns to 3 decimal places
rounded_normalized_numeric_columns = np.round(normalized_numeric_columns, decimals=3)

# Combine the non-numeric columns and rounded normalized numeric columns
normalized_data = np.column_stack((np_data[:, :3], rounded_normalized_numeric_columns))

# Combine the headers and normalized data
normalized_data_with_headers = [columns_to_keep] + normalized_data.tolist()

# Save the normalized data to the 'merged_normalized_player_stats.csv' file
with open('merged_normalized_player_stats.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(normalized_data_with_headers)

print("Merged and normalized data saved to 'merged_normalized_player_stats.csv'")