import os
import json
import csv

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Directory containing JSON files
JSON_DIR = os.path.join(script_dir, '../tmp')
# Output CSV file
CSV_FILE = os.path.join(script_dir, '../tmp/planned_services.csv')

# Function to extract data from JSON and write to CSV
def json_to_csv(json_dir, csv_file):
    # Ensure the directory for the CSV file exists
    os.makedirs(os.path.dirname(csv_file), exist_ok=True)
    
    # Collect all JSON files
    json_files = [f for f in os.listdir(json_dir) if f.endswith('.json')]
    
    # Open CSV file for writing
    with open(csv_file, 'w', newline='') as csvfile:
        # Define CSV column headers
        fieldnames = ['id', 'start', 'end', 'route_id', 'header_text', 'description_text', 'alert_type']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Process each JSON file
        for json_file in json_files:
            print(f"Processing file: {json_file}")  # Debugging statement
            with open(os.path.join(json_dir, json_file), 'r') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON from file {json_file}: {e}")
                    continue
                if 'entity' not in data:
                    print(f"No 'entity' key in file {json_file}. This may indicate no planned service alerts.")  # Updated message
                    continue
                for entity in data.get('entity', []):
                    alert = entity.get('alert', {})
                    active_period = alert.get('active_period', [{}])[0]
                    informed_entity = alert.get('informed_entity', [{}])[0]
                    header_text = alert.get('header_text', {}).get('translation', [{}])[0].get('text', '')
                    description_text = alert.get('description_text', {}).get('translation', [{}])[0].get('text', '')
                    alert_type = entity.get('transit_realtime.mercury_alert', {}).get('alert_type', '')

                    # Write row to CSV
                    writer.writerow({
                        'id': entity.get('id', ''),
                        'start': active_period.get('start', ''),
                        'end': active_period.get('end', ''),
                        'route_id': informed_entity.get('route_id', ''),
                        'header_text': header_text,
                        'description_text': description_text,
                        'alert_type': alert_type
                    })
    print(f"CSV file created at {csv_file}")

if __name__ == "__main__":
    json_to_csv(JSON_DIR, CSV_FILE) 