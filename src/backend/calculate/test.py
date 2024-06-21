import csv
import statistics
import numpy as np

def calculate_stats(file_path, column_name):
    # List to store the values of the specified column
    values = []

    # Open and read the CSV file
    with open(file_path, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        
        # Extract values from the specified column
        for row in csvreader:
            try:
                value = float(row[column_name])
                values.append(value)
            except ValueError:
                print(f"Skipping non-numeric value: {row[column_name]}")
    
    # Calculate statistics
    if values:
        min_value = min(values)
        max_value = max(values)
        mean_value = statistics.mean(values)
        median_value = statistics.median(values)
        
        # Calculate 25th and 75th percentiles
        percentile_25 = np.percentile(values, 25)
        percentile_75 = np.percentile(values, 75)
        
        return {
            'min': min_value,
            'max': max_value,
            'mean': mean_value,
            'median': median_value,
            'percentile_25': percentile_25,
            'percentile_75': percentile_75
        }
    else:
        return None

# Example usage
file_path = '/Users/sabeernarula/Desktop/NBA-Stats/NBA-Stats/src/backend/data/merged_normalized_player_stats.csv'
column_name = 'VORP'

results = calculate_stats(file_path, column_name)

if results:
    print(f"Minimum: {results['min']}")
    print(f"Maximum: {results['max']}")
    print(f"Mean: {results['mean']}")
    print(f"Median: {results['median']}")
    print(f"25th Percentile: {results['percentile_25']}")
    print(f"75th Percentile: {results['percentile_75']}")
else:
    print("No valid numeric values found in the specified column.")