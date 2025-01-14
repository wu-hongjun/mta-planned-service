# MTA Planned Service Tool

This tool is designed to scrape and access the MTA's planned service changes and alerts data. It automatically retrieves the necessary API key from the MTA's website and can be used to collect planned service information for the New York City transit system.

## Features

- Automatic API key extraction from MTA's website
- Secure storage of API credentials
- Compatible with MTA's planned work endpoints
- Uses Playwright for reliable web scraping

## Prerequisites

- Python 3.7+
- Playwright
- Internet connection to access MTA's website

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/mta-planned-service.git
cd mta-planned-service
```

2. Install required dependencies:
```bash
pip install playwright
playwright install chromium
```

## Usage

1. First, obtain the API key by running:
```bash
python src/get_api_key.py
```
This will:
- Launch a headless browser
- Navigate to MTA's website
- Extract the API key
- Save it to `tmp/planned_work_api_key.txt`

The API key is required for accessing MTA's planned service data endpoints.

## Project Structure

```
mta-planned-service/
├── src/
│   ├── get_api_key.py    # API key extraction script
│   └── main.py           # Main application script
├── tmp/                  # Temporary files and API key storage
└── README.md
```

## Security Note

The API key is stored locally in the `tmp` directory. Make sure to add this directory to your `.gitignore` to prevent accidentally committing sensitive credentials.

## Contributing

Feel free to open issues or submit pull requests for any improvements.

## License

[Add your chosen license here]

