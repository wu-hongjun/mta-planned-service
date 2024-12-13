from playwright.sync_api import sync_playwright
import os

# Function to extract the API key from the index.js file
def get_api_key():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        api_key = None  # Initialize api_key variable

        # Intercept network requests
        def handle_response(response):
            nonlocal api_key  # Use nonlocal to modify the outer scope variable
            content_type = response.headers.get('content-type', '')
            if 'application/javascript' in content_type or 'text/javascript' in content_type:
                if response.url == 'https://consist.mta.info/planned-work/index.js':
                    try:
                        content = response.text()
                        print(f"JavaScript URL: {response.url}", f"\nStatus: {response.status}")
                        # Improved logic to extract the API key
                        key_phrase = 'ZZ="'
                        if key_phrase in content:
                            start_index = content.find(key_phrase) + len(key_phrase)
                            end_index = content.find('"', start_index)
                            api_key = content[start_index:end_index]
                            print("Extracted API Key:", api_key)
                            # Get the directory of the current script
                            script_dir = os.path.dirname(os.path.abspath(__file__))
                            # Ensure the directory exists
                            tmp_dir = os.path.join(script_dir, '../tmp')
                            os.makedirs(tmp_dir, exist_ok=True)
                            # Save the API key to a file
                            with open(os.path.join(tmp_dir, 'planned_work_api_key.txt'), 'w') as f:
                                f.write(api_key)
                                print("API Key saved to ../tmp/planned_work_api_key.txt")
                    except Exception as e:
                        print(f"Error processing JavaScript response from {response.url}: {e}")

        page.on('response', handle_response)

        # Navigate to the MTA alerts page
        page.goto('https://new.mta.info/alerts?selectedRoutes=MTASBWY%3A1')
        # Wait for the page to load completely
        page.wait_for_load_state('networkidle')

        browser.close()
        return api_key

if __name__ == "__main__":
    api_key = get_api_key()
    if api_key:
        print(f"API Key: {api_key}")
    else:
        print("API Key not found.") 