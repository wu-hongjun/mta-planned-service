import os
import json
from fetch_line_planned_services import call_endpoint, ensure_subway_routes_file, read_api_key
from format_json_to_csv import json_to_csv
from get_api_key import get_api_key

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Directory containing JSON files
JSON_DIR = os.path.join(script_dir, '../tmp')
# Output CSV file
CSV_FILE = os.path.join(script_dir, '../tmp/planned_services.csv')

if __name__ == "__main__":
    api_key = read_api_key()
    if not api_key:
        print("API key not found, fetching a new one.")
        api_key = get_api_key()

    if api_key:
        # Ensure subway routes file exists
        subway_routes_file = ensure_subway_routes_file()

        # Load subway routes
        with open(subway_routes_file, 'r') as f:
            subway_routes = json.load(f)

        # Fetch planned services for each route
        for route in subway_routes:
            route_id = route['field_route_short_name']
            result = call_endpoint(api_key, route_id)
            if not result:
                print(f"Retrying with a new API key for route {route_id}.")
                api_key = get_api_key()
                if api_key:
                    result = call_endpoint(api_key, route_id)
                    if not result:
                        print(f"Failed to call API with a new key for route {route_id}.")
                else:
                    print("Failed to fetch a new API key.")

        # Convert JSON files to CSV
        json_to_csv(JSON_DIR, CSV_FILE)
    else:
        print("Failed to fetch an API key.") 