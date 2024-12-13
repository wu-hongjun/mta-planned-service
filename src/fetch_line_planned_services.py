import os
import requests
import json
from get_api_key import get_api_key
from datetime import datetime

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
API_KEY_FILE = os.path.join(script_dir, '../tmp/planned_work_api_key.txt')
SUBWAY_ROUTES_FILE = os.path.join(script_dir, '../tmp/subway_routes.json')
ENDPOINT = 'https://collector-otp-prod.camsys-apps.com/realtime/gtfsrt/filtered/alerts'

# Define start and end dates
start_date = datetime.now().strftime('%Y-%m-%dT00:00:00')
end_date = datetime.now().strftime('%Y-%m-%dT23:59:59')

# Function to read the API key from the file
def read_api_key():
    if os.path.exists(API_KEY_FILE):
        with open(API_KEY_FILE, 'r') as f:
            return f.read().strip()
    return None

# Function to save the result to a JSON file
def save_result_to_file(result, agency_id, route_id, start_date, end_date):
    filename = f"{agency_id}_{route_id}_{start_date}_{end_date}.json"
    filepath = os.path.join(script_dir, '../tmp', filename)
    with open(filepath, 'w') as f:
        json.dump(result, f)
    print(f"Result saved to {filepath}")

# Function to call the endpoint with the API key
def call_endpoint(api_key, route_id):
    params = {
        'type': 'json',
        'apikey': api_key,
        'routeId': route_id,
        'agencyId': 'MTASBWY',
        'startDate': start_date,
        'endDate': end_date
    }
    response = requests.get(ENDPOINT, params=params)
    if response.status_code == 200:
        print(f"API call successful for route {route_id}.")
        result = response.json()
        save_result_to_file(result, params['agencyId'], route_id, params['startDate'], params['endDate'])
        return result
    else:
        print(f"API call failed for route {route_id} with status code {response.status_code}.")
        return None

# Function to fetch subway routes and save to file if not present
def ensure_subway_routes_file():
    # Ensure the tmp directory exists
    os.makedirs(os.path.dirname(SUBWAY_ROUTES_FILE), exist_ok=True)

    if not os.path.exists(SUBWAY_ROUTES_FILE):
        print("Subway routes file not found, fetching new data.")
        response = requests.get('https://new.mta.info/mta-subway')
        if response.status_code == 200:
            routes = response.json()
            with open(SUBWAY_ROUTES_FILE, 'w') as f:
                json.dump(routes, f)
            print(f"Subway routes saved to {SUBWAY_ROUTES_FILE}")
        else:
            print("Failed to fetch subway routes.")

    return SUBWAY_ROUTES_FILE

if __name__ == "__main__":
    api_key = read_api_key()
    if not api_key:
        print("API key not found, fetching a new one.")
        api_key = get_api_key()

    if api_key:
        # Ensure subway routes file exists
        ensure_subway_routes_file()

        # Load subway routes
        with open(SUBWAY_ROUTES_FILE, 'r') as f:
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
    else:
        print("Failed to fetch an API key.")
