import csv
import re

# Define the input and output file paths
input_file = 'sensor_data.txt'

output_files = {
    'temperature': 'temperature_data.csv',
    'humidity': 'humidity_data.csv',
    'pressure': 'pressure_data.csv',
    'gas': 'gas_data.csv',
    'adc72_channel_0': 'adc72_channel_0.csv',
    'adc72_channel_1': 'adc72_channel_1.csv',
    'adc72_channel_2': 'adc72_channel_2.csv',
    'adc72_channel_3': 'adc72_channel_3.csv',
    'adc73_channel_0': 'adc73_channel_0.csv',
    'adc73_channel_1': 'adc73_channel_1.csv',
    'adc73_channel_2': 'adc73_channel_2.csv',
    'adc73_channel_3': 'adc73_channel_3.csv'
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
    'adc73_channel_3': []
}

# Read the input file and parse the data
with open(input_file, 'r') as file:
    for line in file:
        # Parse temperature, humidity, pressure, gas
        if line.startswith(('Temperature:', 'Humidity:', 'Pressure:', 'Gas:')):
            sensor_type, value = line.strip().split(': ')
            data[sensor_type.lower()].append([value])

        # Parse ADC72 values
        elif line.startswith('ADC72 Values:'):
            for i in range(4):
                line = next(file).strip()
                match = re.search(r'Channel (\d+): (\d+)', line)
                if match:
                    channel_num = match.group(1)
                    data_key = f'adc72_channel_{channel_num}'
                    if data_key in data:
                        data[data_key].append([match.group(2)])
                    else:
                        print(f"Error: Data key '{data_key}' not found.")
                else:
                    print(f"Error: Unable to parse line: {line}")

        # Parse ADC73 values
        elif line.startswith('ADC73 Values:'):
            for i in range(4):
                line = next(file).strip()
                match = re.search(r'Channel (\d+): (\d+)', line)
                if match:
                    channel_num = match.group(1)
                    data_key = f'adc73_channel_{channel_num}'
                    if data_key in data:
                        data[data_key].append([match.group(2)])
                    else:
                        print(f"Error: Data key '{data_key}' not found.")
                else:
                    print(f"Error: Unable to parse line: {line}")

# Write the parsed data to corresponding CSV files
for sensor_type, rows in data.items():
    with open(output_files[sensor_type], 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['value'])  # Write header
        writer.writerows(rows)

print("Data parsing and writing to CSV files completed successfully.")
