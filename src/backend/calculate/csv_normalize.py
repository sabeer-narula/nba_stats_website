# import csv
# import numpy as np
# from fuzzywuzzy import fuzz

# def normalize_data(data):
#     min_value = np.min(data, axis=0)
#     max_value = np.max(data, axis=0)
#     normalized_data = (data - min_value) / (max_value - min_value)
#     return normalized_data

# def fix_position(position):
#     valid_positions = ['C', 'PG', 'SG', 'PF', 'SF']
#     if '-' in position:
#         position = position.split('-')[0]
#     if position not in valid_positions:
#         position = 'Unknown'
#     return position

# # Read the data from the first CSV file
# with open('../data/player_stats.csv', 'r') as file:
#     reader = csv.reader(file)
#     headers1 = next(reader)
#     data1 = list(reader)

# # Read the data from the second CSV file
# with open('../data/per.csv', 'r') as file:
#     reader = csv.reader(file)
#     headers2 = next(reader)
#     data2 = list(reader)

# # Create dictionaries to store the data from both files
# data1_dict = {row[headers1.index('PLAYER_NAME')]: row for row in data1}
# data2_dict = {row[headers2.index('Player')]: row for row in data2}

# # Set a threshold for the fuzzy matching ratio (e.g., 90)
# threshold = 90

# # Create a dictionary to store the merged data
# merged_data = {}

# # Iterate over each player in data1
# for player_name, row1 in data1_dict.items():
#     # Find the best match for the player name using fuzzy string matching
#     best_match = None
#     best_ratio = 0
#     for name, row2 in data2_dict.items():
#         ratio = fuzz.ratio(player_name, name)
#         if ratio > best_ratio:
#             best_match = name
#             best_ratio = ratio
    
#     # Check if the best match ratio is above the threshold
#     if best_ratio >= threshold:
#         merged_data[player_name] = row1 + data2_dict[best_match]

# # Define the columns to keep
# columns_to_keep = [
#     'PLAYER_ID', 'PLAYER_NAME', 'Pos', 'Age', 'GP', 'MIN', 'FG_PCT', 'FG3_PCT',
#     'FT_PCT', 'OREB', 'DREB', 'AST', 'TOV', 'STL', 'BLK', 'PTS',
#     'PLUS_MINUS', 'WS/48', 'BPM', 'VORP', 'PER'
# ]

# # Find the indices of the columns to keep
# indices_to_keep = [headers1.index(col) if col in headers1 else len(headers1) + headers2.index(col) for col in columns_to_keep]

# # Remove unnecessary columns
# filtered_data = [[row[i] for i in indices_to_keep] for row in merged_data.values()]

# # Fix the position values
# for row in filtered_data:
#     row[columns_to_keep.index('Pos')] = fix_position(row[columns_to_keep.index('Pos')])

# # Convert the data to a NumPy array
# np_data = np.array(filtered_data)

# # Convert string values to float (skip the first three columns which are PLAYER_ID, PLAYER_NAME, and Pos)
# numeric_columns = np_data[:, 4:].astype(float)

# # Normalize the data (skip the first three columns which are PLAYER_ID, PLAYER_NAME, and Pos)
# normalized_numeric_columns = normalize_data(numeric_columns)

# # Round the normalized numeric columns to 3 decimal places
# rounded_normalized_numeric_columns = np.round(normalized_numeric_columns, decimals=3)

# # Combine the non-numeric columns and rounded normalized numeric columns
# normalized_data = np.column_stack((np_data[:, :4], rounded_normalized_numeric_columns))

# # Combine the headers and normalized data
# normalized_data_with_headers = [columns_to_keep] + normalized_data.tolist()

# # Save the normalized data to the 'merged_normalized_player_stats.csv' file
# with open('../data/merged_normalized_player_stats.csv', 'w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerows(normalized_data_with_headers)

# print("Merged and normalized data saved to 'merged_normalized_player_stats.csv'")

import csv
import numpy as np
from fuzzywuzzy import fuzz

def min_max_scale(data):
    min_vals = np.min(data, axis=0)
    max_vals = np.max(data, axis=0)
    return (data - min_vals) / (max_vals - min_vals)

def scale_percentage(data, low_threshold, high_threshold):
    return np.clip(data, low_threshold, high_threshold)

def fix_position(position):
    valid_positions = ['C', 'PG', 'SG', 'PF', 'SF']
    if '-' in position:
        position = position.split('-')[0]
    if position not in valid_positions:
        position = 'Unknown'
    return position

# Read the data from the first CSV file
with open('/Users/sabeernarula/Desktop/NBA-Stats/NBA-Stats/src/backend/data/player_stats.csv', 'r') as file:
    reader = csv.reader(file)
    headers1 = next(reader)
    data1 = list(reader)

# Read the data from the second CSV file
with open('/Users/sabeernarula/Desktop/NBA-Stats/NBA-Stats/src/backend/data/per.csv', 'r') as file:
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
numeric_columns = np_data[:, 4:].astype(float)

# Define column groups for different preprocessing methods
regular_columns = ['Age', 'GP', 'MIN', 'OREB', 'DREB', 'AST', 'TOV', 'STL', 'BLK', 'PTS', 'PLUS_MINUS', 'WS/48', 'BPM', 'VORP', 'PER']
percentage_columns = ['FG_PCT', 'FG3_PCT', 'FT_PCT']

# Get indices for each column group
regular_indices = [columns_to_keep.index(col) - 4 for col in regular_columns]  # -4 to account for non-numeric columns
percentage_indices = [columns_to_keep.index(col) - 4 for col in percentage_columns]

# Apply preprocessing
preprocessed_numeric_columns = np.zeros_like(numeric_columns)
preprocessed_numeric_columns[:, regular_indices] = min_max_scale(numeric_columns[:, regular_indices])

# Handle percentage columns
fg_pct = scale_percentage(numeric_columns[:, percentage_indices[0]], 0.2, 0.8)
fg3_pct = scale_percentage(numeric_columns[:, percentage_indices[1]], 0.20, 0.55)
ft_pct = scale_percentage(numeric_columns[:, percentage_indices[2]], 0.5, 0.9)

preprocessed_numeric_columns[:, percentage_indices] = np.column_stack((fg_pct, fg3_pct, ft_pct))

# Round the preprocessed numeric columns to 3 decimal places
rounded_preprocessed_numeric_columns = np.round(preprocessed_numeric_columns, decimals=3)

# Combine the non-numeric columns and rounded preprocessed numeric columns
preprocessed_data = np.column_stack((np_data[:, :4], rounded_preprocessed_numeric_columns))

# Combine the headers and preprocessed data
preprocessed_data_with_headers = [columns_to_keep] + preprocessed_data.tolist()

# Save the preprocessed data to the 'merged_preprocessed_player_stats.csv' file
with open('/Users/sabeernarula/Desktop/NBA-Stats/NBA-Stats/src/backend/data/merged_normalized_player_stats.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(preprocessed_data_with_headers)

print("Merged and preprocessed data saved to 'merged_normalized_player_stats.csv'")