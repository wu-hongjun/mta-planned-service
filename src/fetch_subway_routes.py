import os
import requests
import json

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
SUBWAY_ROUTES_FILE = os.path.join(script_dir, '../tmp/subway_routes.json')
SUBWAY_ROUTES_ENDPOINT = 'https://new.mta.info/mta-subway'

# Function to call the subway routes endpoint
def fetch_subway_routes():
    response = requests.get(SUBWAY_ROUTES_ENDPOINT)
    if response.status_code == 200:
        print("Subway routes fetched successfully.")
        return response.json()
    else:
        print(f"Failed to fetch subway routes with status code {response.status_code}.")
        return None

# Function to save the subway routes to a JSON file
def save_subway_routes_to_file(routes):
    with open(SUBWAY_ROUTES_FILE, 'w') as f:
        json.dump(routes, f)
    print(f"Subway routes saved to {SUBWAY_ROUTES_FILE}")

if __name__ == "__main__":
    routes = fetch_subway_routes()
    if routes:
        save_subway_routes_to_file(routes) 