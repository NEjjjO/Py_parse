import csv
import re
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Define the input file path
input_file = 'test02.txt'

# Define output directory paths for raw, PPM data, and final complete data
raw_data_dir = 'raw_data'
ppm_data_dir = 'ppm_data'
final_data_dir = 'final_csv_complete'
graphs_dir = os.path.join(final_data_dir, 'graphs')

# Ensure the directories exist
os.makedirs(raw_data_dir, exist_ok=True)
os.makedirs(ppm_data_dir, exist_ok=True)
os.makedirs(final_data_dir, exist_ok=True)
os.makedirs(graphs_dir, exist_ok=True)

# Define output CSV file names for each type of data and PPM values
output_files = {
    'temperature': os.path.join(raw_data_dir, 'temperature_data.csv'),
    'humidity': os.path.join(raw_data_dir, 'humidity_data.csv'),
    'pressure': os.path.join(raw_data_dir, 'pressure_data.csv'),
    'gas': os.path.join(raw_data_dir, 'gas_data.csv'),
    'adc1_channel_0': os.path.join(raw_data_dir, 'adc1_channel_0.csv'),
    'adc1_channel_1': os.path.join(raw_data_dir, 'adc1_channel_1.csv'),
    'adc1_channel_2': os.path.join(raw_data_dir, 'adc1_channel_2.csv'),
    'adc1_channel_3': os.path.join(raw_data_dir, 'adc1_channel_3.csv'),
    'adc2_channel_0': os.path.join(raw_data_dir, 'adc2_channel_0.csv'),
    'adc2_channel_1': os.path.join(raw_data_dir, 'adc2_channel_1.csv'),
    'adc2_channel_2': os.path.join(raw_data_dir, 'adc2_channel_2.csv'),
    'adc2_channel_3': os.path.join(raw_data_dir, 'adc2_channel_3.csv'),
    'adc1_channel_0_ppm': os.path.join(ppm_data_dir, 'adc1_channel_0_ppm.csv'),
    'adc1_channel_1_ppm': os.path.join(ppm_data_dir, 'adc1_channel_1_ppm.csv'),
    'adc1_channel_2_ppm': os.path.join(ppm_data_dir, 'adc1_channel_2_ppm.csv'),
    'adc1_channel_3_ppm': os.path.join(ppm_data_dir, 'adc1_channel_3_ppm.csv'),
    'adc2_channel_0_ppm': os.path.join(ppm_data_dir, 'adc2_channel_0_ppm.csv'),
    'adc2_channel_1_ppm': os.path.join(ppm_data_dir, 'adc2_channel_1_ppm.csv'),
    'adc2_channel_2_ppm': os.path.join(ppm_data_dir, 'adc2_channel_2_ppm.csv'),
    'adc2_channel_3_ppm': os.path.join(ppm_data_dir, 'adc2_channel_3_ppm.csv')
}

# Initialize dictionaries to store data
data = {
    'temperature': [],
    'humidity': [],
    'pressure': [],
    'gas': [],
    'adc1_channel_0': [],
    'adc1_channel_1': [],
    'adc1_channel_2': [],
    'adc1_channel_3': [],
    'adc2_channel_0': [],
    'adc2_channel_1': [],
    'adc2_channel_2': [],
    'adc2_channel_3': [],
    'adc1_channel_0_ppm': [],
    'adc1_channel_1_ppm': [],
    'adc1_channel_2_ppm': [],
    'adc1_channel_3_ppm': [],
    'adc2_channel_0_ppm': [],
    'adc2_channel_1_ppm': [],
    'adc2_channel_2_ppm': [],
    'adc2_channel_3_ppm': []
}

# Define min/max PPM values for each ADC channel (these should be adjusted as needed)
ppm_ranges = {
    'adc1_channel_0': {'min': 10, 'max': 1000},  # O3
    'adc1_channel_1': {'min': 300, 'max': 10000},  # CH4
    'adc1_channel_2': {'min': 0.05, 'max': 10},  # NO2
    'adc1_channel_3': {'min': 1, 'max': 500},  # NH3
    'adc2_channel_0': {'min': 1, 'max': 1000},  # CO
    'adc2_channel_1': {'min': 1, 'max': 100},  # NOx
    'adc2_channel_2': {'min': 10, 'max': 10000},  # CO2
    'adc2_channel_3': {'min': 0, 'max': 0}  # NC - not connected
}


def adc_to_ppm(adc_value, min_ppm, max_ppm):
    """Convert ADC value to PPM based on min and max PPM values."""
    return min_ppm + (adc_value / 65535.0) * (max_ppm - min_ppm)


print("Starting data parsing...")

# Read the input file and parse the data
with open(input_file, 'r') as file:
    for line in file:
        # Parse temperature, humidity, pressure, gas
        if line.startswith(('Temperature:', 'Humidity:', 'Pressure:', 'Gas:')):
            sensor_type, value_with_unit = line.strip().split(': ')
            # Extract the numeric value using regex
            value = re.findall(r"[-+]?\d*\.\d+|\d+", value_with_unit)[0]
            data[sensor_type.lower()].append([value])
            print(f"Parsed {sensor_type.lower()} value: {value}")

        # Parse ADC1 values
        elif line.startswith('ADC1 Channel'):
            match = re.search(r'ADC1 Channel (\d+): (\d+)', line)
            if match:
                channel_num = match.group(1)
                adc_value = int(match.group(2))
                data_key = f'adc1_channel_{channel_num}'
                ppm_data_key = f'{data_key}_ppm'
                if data_key in data and ppm_data_key in data:
                    # Convert ADC value to PPM
                    ppm_value = adc_to_ppm(adc_value, ppm_ranges[data_key]['min'], ppm_ranges[data_key]['max'])
                    data[data_key].append([adc_value])
                    data[ppm_data_key].append([ppm_value])
                    print(f"Parsed {data_key} ADC value: {adc_value}, converted to PPM: {ppm_value}")
                else:
                    print(f"Error: Data key '{data_key}' or '{ppm_data_key}' not found.")
            else:
                print(f"Error: Unable to parse line: {line}")

        # Parse ADC2 values
        elif line.startswith('ADC2 Channel'):
            match = re.search(r'ADC2 Channel (\d+): (\d+)', line)
            if match:
                channel_num = match.group(1)
                adc_value = int(match.group(2))
                data_key = f'adc2_channel_{channel_num}'
                ppm_data_key = f'{data_key}_ppm'
                if data_key in data and ppm_data_key in data:
                    # Convert ADC value to PPM
                    ppm_value = adc_to_ppm(adc_value, ppm_ranges[data_key]['min'], ppm_ranges[data_key]['max'])
                    data[data_key].append([adc_value])
                    data[ppm_data_key].append([ppm_value])
                    print(f"Parsed {data_key} ADC value: {adc_value}, converted to PPM: {ppm_value}")
                else:
                    print(f"Error: Data key '{data_key}' or '{ppm_data_key}' not found.")
            else:
                print(f"Error: Unable to parse line: {line}")

print("Finished parsing data. Writing to CSV files...")

# Write the parsed data to corresponding CSV files
for sensor_type, rows in data.items():
    with open(output_files[sensor_type], 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['value'])  # Write header
        writer.writerows(rows)
        print(f"Wrote data to {output_files[sensor_type]}")

# Write the combined raw data to a final CSV file
combined_raw_data_file = os.path.join(final_data_dir, 'combined_raw_data.csv')
with open(combined_raw_data_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['temperature', 'humidity', 'pressure', 'gas', 'adc1_channel_0', 'adc1_channel_1', 'adc1_channel_2',
                     'adc1_channel_3', 'adc2_channel_0', 'adc2_channel_1', 'adc2_channel_2',
                     'adc2_channel_3'])  # Write header
    for i in range(len(data['temperature'])):
        row = [
            data['temperature'][i][0] if i < len(data['temperature']) else '',
            data['humidity'][i][0] if i < len(data['humidity']) else '',
            data['pressure'][i][0] if i < len(data['pressure']) else '',
            data['gas'][i][0] if i < len(data['gas']) else '',
            data['adc1_channel_0'][i][0] if i < len(data['adc1_channel_0']) else '',
            data['adc1_channel_1'][i][0] if i < len(data['adc1_channel_1']) else '',
            data['adc1_channel_2'][i][0] if i < len(data['adc1_channel_2']) else '',
            data['adc1_channel_3'][i][0] if i < len(data['adc1_channel_3']) else '',
            data['adc2_channel_0'][i][0] if i < len(data['adc2_channel_0']) else '',
            data['adc2_channel_1'][i][0] if i < len(data['adc2_channel_1']) else '',
            data['adc2_channel_2'][i][0] if i < len(data['adc2_channel_2']) else '',
            data['adc2_channel_3'][i][0] if i < len(data['adc2_channel_3']) else ''
        ]
        writer.writerow(row)
    print(f"Wrote combined raw data to {combined_raw_data_file}")

# Write the combined PPM data to a final CSV file
combined_ppm_data_file = os.path.join(final_data_dir, 'combined_ppm_data.csv')
with open(combined_ppm_data_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(
        ['temperature', 'humidity', 'pressure', 'gas', 'adc1_channel_0_ppm', 'adc1_channel_1_ppm', 'adc1_channel_2_ppm',
         'adc1_channel_3_ppm', 'adc2_channel_0_ppm', 'adc2_channel_1_ppm', 'adc2_channel_2_ppm',
         'adc2_channel_3_ppm'])  # Write header
    for i in range(len(data['temperature'])):
        row = [
            data['temperature'][i][0] if i < len(data['temperature']) else '',
            data['humidity'][i][0] if i < len(data['humidity']) else '',
            data['pressure'][i][0] if i < len(data['pressure']) else '',
            data['gas'][i][0] if i < len(data['gas']) else '',
            data['adc1_channel_0_ppm'][i][0] if i < len(data['adc1_channel_0_ppm']) else '',
            data['adc1_channel_1_ppm'][i][0] if i < len(data['adc1_channel_1_ppm']) else '',
            data['adc1_channel_2_ppm'][i][0] if i < len(data['adc1_channel_2_ppm']) else '',
            data['adc1_channel_3_ppm'][i][0] if i < len(data['adc1_channel_3_ppm']) else '',
            data['adc2_channel_0_ppm'][i][0] if i < len(data['adc2_channel_0_ppm']) else '',
            data['adc2_channel_1_ppm'][i][0] if i < len(data['adc2_channel_1_ppm']) else '',
            data['adc2_channel_2_ppm'][i][0] if i < len(data['adc2_channel_2_ppm']) else '',
            data['adc2_channel_3_ppm'][i][0] if i < len(data['adc2_channel_3_ppm']) else ''
        ]
        writer.writerow(row)
    print(f"Wrote combined PPM data to {combined_ppm_data_file}")

print("Data parsing and writing to CSV files completed successfully.")

# Define the weightings
weights = {
    'O3': 0.2,
    'CO2': 0.1,
    'H2S': 0.1,
    'humidity': 0.1,
    'temperature': 0.2,
    'VOC': 0.2,
    'other': 0.1
}

# Define scoring thresholds
# Thresholds for CO2
co2_thresholds = [
    (0, 400, 'Yellow', 2),
    (401, 999, 'Green', 3),
    (1000, 1500, 'Red', 4),
    (1501, float('inf'), 'Red', 5)
]

# Thresholds for Humidity
humidity_thresholds = [
    (0, 50, 'Red', 0),
    (50, 60, 'Yellow', 5),
    (60, 80, 'Green', 10),
    (80, 90, 'Green', 8),
    (90, float('inf'), 'Red', 0)
]

# Thresholds for H2S
h2s_thresholds_no_sulfur = [
    (0, 0.02, 'Red', 0),
    (0.02, 0.05, 'Yellow', 6),
    (0.05, float('inf'), 'Green', 10)
]

h2s_thresholds_with_sulfur = [
    (0, 0.05, 'Red', 0),
    (0.05, 0.1, 'Yellow', 6),
    (0.1, float('inf'), 'Green', 10)
]

# We use h2s_thresholds_no_sulfur in the example
h2s_thresholds = h2s_thresholds_no_sulfur

# Thresholds for O3
o3_thresholds = [
    (0, 0.025, 'Red', 0),
    (0.025, 0.054, 'Green', 10),
    (0.054, 0.085, 'Yellow', 8),
    (0.085, 0.1, 'Yellow', 7),
    (0.1, float('inf'), 'Red', 0)
]

# Load the combined PPM data
ppm_df = pd.read_csv(combined_ppm_data_file)


def get_score(value, thresholds):
    for min_val, max_val, result, score in thresholds:
        if min_val <= value <= max_val:
            return result, score
    return 'Unknown', 0


def get_temperature_score(value, is_daytime):
    if is_daytime:
        return get_score(value, [
            (10, 20, 'Green', 10),
            (20, 30, 'Yellow', 8),
            (30, 35, 'Red', 4),
            (35, float('inf'), 'Red', 0)
        ])
    else:
        return get_score(value, [
            (17, 20, 'Green', 10),
            (20, 30, 'Yellow', 8),
            (30, 35, 'Red', 4),
            (35, float('inf'), 'Red', 0)
        ])


def calculate_final_score(row, is_daytime):
    o3_value = float(row['adc1_channel_0_ppm'])
    co2_value = float(row['adc2_channel_2_ppm'])
    h2s_value = 0  # Replace with correct assignment
    humidity_value = float(row['humidity'])
    temperature_value = float(row['temperature'])
    voc_value = float(row['adc1_channel_3_ppm'])

    o3_score = get_score(o3_value, o3_thresholds)[1]
    co2_score = get_score(co2_value, co2_thresholds)[1]
    h2s_score = get_score(h2s_value, h2s_thresholds)[1]
    humidity_score = get_score(humidity_value, humidity_thresholds)[1]
    temperature_score = get_temperature_score(temperature_value, is_daytime)[1]
    voc_score = get_score(voc_value, o3_thresholds)[1]  # Replace with correct assignment

    final_score = (o3_score * weights['O3'] +
                   co2_score * weights['CO2'] +
                   h2s_score * weights['H2S'] +
                   humidity_score * weights['humidity'] +
                   temperature_score * weights['temperature'] +
                   voc_score * weights['VOC'] +
                   0)

    return final_score


# Determine if daytime or nighttime
is_daytime = True  # Replace with actual logic to determine if it's daytime or not

# Calculate final scores for each row
final_scores = [calculate_final_score(row, is_daytime) for index, row in ppm_df.iterrows()]

# Add final scores to the data frame
ppm_df['final_score'] = final_scores

# Save the results to a new CSV
results_file = os.path.join(final_data_dir, 'results_with_scores.csv')
ppm_df.to_csv(results_file, index=False)
print(f"Results with scores saved to {results_file}")


# Plotting function
def plot_data(file_path, title, ylabel, output_path):
    df = pd.read_csv(file_path)
    plt.figure(figsize=(10, 6))
    for column in df.columns:
        df[column] = pd.to_numeric(df[column], errors='coerce')  # Ensure numeric data
        if column != 'Unnamed: 0' and 'datetime' not in column:
            plt.plot(df.index, df[column], label=column)
    plt.title(title)
    plt.xlabel('Index')
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(True)
    plt.savefig(output_path)
    plt.close()


print("Generating graphs...")

plot_data(combined_raw_data_file, 'Combined Raw Data', 'Values', os.path.join(graphs_dir, 'combined_raw_data.png'))