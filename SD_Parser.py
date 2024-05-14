import csv
import re
import os

# Define the input file path
input_file = 'sensor_data.txt'

# Define output directory paths for raw and PPM data
raw_data_dir = 'raw_data'
ppm_data_dir = 'ppm_data'

# Ensure the directories exist
os.makedirs(raw_data_dir, exist_ok=True)
os.makedirs(ppm_data_dir, exist_ok=True)

# Define output CSV file names for each type of data and PPM values
output_files = {
    'temperature': os.path.join(raw_data_dir, 'temperature_data.csv'),
    'humidity': os.path.join(raw_data_dir, 'humidity_data.csv'),
    'pressure': os.path.join(raw_data_dir, 'pressure_data.csv'),
    'gas': os.path.join(raw_data_dir, 'gas_data.csv'),
    'adc72_channel_0': os.path.join(raw_data_dir, 'adc72_channel_0.csv'),
    'adc72_channel_1': os.path.join(raw_data_dir, 'adc72_channel_1.csv'),
    'adc72_channel_2': os.path.join(raw_data_dir, 'adc72_channel_2.csv'),
    'adc72_channel_3': os.path.join(raw_data_dir, 'adc72_channel_3.csv'),
    'adc73_channel_0': os.path.join(raw_data_dir, 'adc73_channel_0.csv'),
    'adc73_channel_1': os.path.join(raw_data_dir, 'adc73_channel_1.csv'),
    'adc73_channel_2': os.path.join(raw_data_dir, 'adc73_channel_2.csv'),
    'adc73_channel_3': os.path.join(raw_data_dir, 'adc73_channel_3.csv'),
    'adc72_channel_0_ppm': os.path.join(ppm_data_dir, 'adc72_channel_0_ppm.csv'),
    'adc72_channel_1_ppm': os.path.join(ppm_data_dir, 'adc72_channel_1_ppm.csv'),
    'adc72_channel_2_ppm': os.path.join(ppm_data_dir, 'adc72_channel_2_ppm.csv'),
    'adc72_channel_3_ppm': os.path.join(ppm_data_dir, 'adc72_channel_3_ppm.csv'),
    'adc73_channel_0_ppm': os.path.join(ppm_data_dir, 'adc73_channel_0_ppm.csv'),
    'adc73_channel_1_ppm': os.path.join(ppm_data_dir, 'adc73_channel_1_ppm.csv'),
    'adc73_channel_2_ppm': os.path.join(ppm_data_dir, 'adc73_channel_2_ppm.csv'),
    'adc73_channel_3_ppm': os.path.join(ppm_data_dir, 'adc73_channel_3_ppm.csv')
}

# Initialize dictionaries to store data
data = {
    'temperature': [],
    'humidity': [],
    'pressure': [],
    'gas': [],
    'adc72_channel_0': [],
    'adc72_channel_1': [],
    'adc72_channel_2': [],
    'adc72_channel_3': [],
    'adc73_channel_0': [],
    'adc73_channel_1': [],
    'adc73_channel_2': [],
    'adc73_channel_3': [],
    'adc72_channel_0_ppm': [],
    'adc72_channel_1_ppm': [],
    'adc72_channel_2_ppm': [],
    'adc72_channel_3_ppm': [],
    'adc73_channel_0_ppm': [],
    'adc73_channel_1_ppm': [],
    'adc73_channel_2_ppm': [],
    'adc73_channel_3_ppm': []
}

# Define min/max PPM values for each ADC channel (these should be adjusted as needed)
ppm_ranges = {
    'adc72_channel_0': {'min': 0, 'max': 100},
    'adc72_channel_1': {'min': 0, 'max': 100},
    'adc72_channel_2': {'min': 0, 'max': 100},
    'adc72_channel_3': {'min': 0, 'max': 100},
    'adc73_channel_0': {'min': 0, 'max': 100},
    'adc73_channel_1': {'min': 0, 'max': 100},
    'adc73_channel_2': {'min': 0, 'max': 100},
    'adc73_channel_3': {'min': 0, 'max': 100}
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
            sensor_type, value = line.strip().split(': ')
            data[sensor_type.lower()].append([value])
            print(f"Parsed {sensor_type.lower()} value: {value}")

        # Parse ADC72 values
        elif line.startswith('ADC72 Values:'):
            for i in range(4):
                line = next(file).strip()
                match = re.search(r'Channel (\d+): (\d+)', line)
                if match:
                    channel_num = match.group(1)
                    adc_value = int(match.group(2))
                    data_key = f'adc72_channel_{channel_num}'
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

        # Parse ADC73 values
        elif line.startswith('ADC73 Values:'):
            for i in range(4):
                line = next(file).strip()
                match = re.search(r'Channel (\d+): (\d+)', line)
                if match:
                    channel_num = match.group(1)
                    adc_value = int(match.group(2))
                    data_key = f'adc73_channel_{channel_num}'
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
        writer = csv.writer(csvfile, delimiter='|')
        writer.writerow(['value'])  # Write header
        writer.writerows(rows)
        print(f"Wrote data to {output_files[sensor_type]}")

print("Data parsing and writing to CSV files completed successfully.")
