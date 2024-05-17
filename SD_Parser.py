import csv
import re
import os
import pandas as pd
import matplotlib.pyplot as plt

# Define the input file path
input_file = 'test01.txt'

# Define output directory paths for raw, PPM data, and final complete data
raw_data_dir = 'raw_data'
ppm_data_dir = 'ppm_data'
final_data_dir = 'final_csv_complete'
graphs_dir = os.path.join(final_data_dir, 'graphs')

# Using `os.makedirs` to create directories only if they don't already exist
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


# Plotting the data

def plot_data(file_path, title, ylabel, output_path):
    df = pd.read_csv(file_path)
    plt.figure(figsize=(10, 6))
    for column in df.columns:
        if column != 'Unnamed: 0':
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
plot_data(combined_ppm_data_file, 'Combined PPM Data', 'Values (PPM)',
          os.path.join(graphs_dir, 'combined_ppm_data.png'))

print(f"Graphs have been generated and saved in {graphs_dir}.")