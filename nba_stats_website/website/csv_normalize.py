import csv
import numpy as np

def normalize_data(data):
    min_value = np.min(data, axis=0)
    max_value = np.max(data, axis=0)
    normalized_data = (data - min_value) / (max_value - min_value)
    return normalized_data

# Read the data from the CSV file
with open('player_stats.csv', 'r') as file:
    reader = csv.reader(file)
    headers = next(reader)
    data = list(reader)

# Define the columns to keep
columns_to_keep = [
    'PLAYER_ID', 'PLAYER_NAME', 'GP', 'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT',
    'FTM', 'FTA', 'OREB', 'DREB', 'REB', 'AST', 'TOV', 'STL', 'BLK', 'PTS', 'PLUS_MINUS'
]

# Find the indices of the columns to keep
indices_to_keep = [headers.index(col) for col in columns_to_keep]

# Remove unnecessary columns
filtered_data = [[row[i] for i in indices_to_keep] for row in data]

# Convert the data to a NumPy array
np_data = np.array(filtered_data)

# Convert string values to float (skip the first two columns which are PLAYER_ID and PLAYER_NAME)
numeric_columns = np_data[:, 2:].astype(float)

# Normalize the data (skip the first two columns which are PLAYER_ID and PLAYER_NAME)
normalized_numeric_columns = normalize_data(numeric_columns)

# Round the normalized numeric columns to 3 decimal places
rounded_normalized_numeric_columns = np.round(normalized_numeric_columns, decimals=3)

# Combine the non-numeric columns and rounded normalized numeric columns
normalized_data = np.column_stack((np_data[:, :2], rounded_normalized_numeric_columns))

# Combine the headers and normalized data
normalized_data_with_headers = [columns_to_keep] + normalized_data.tolist()

# Save the normalized data to the 'normalized_player_stats.csv' file
with open('normalized_player_stats.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(normalized_data_with_headers)

print("Normalized data saved to 'normalized_player_stats.csv'")