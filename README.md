# FF News History Bot

This project is a Python-based tool for scraping and archiving historical ForexFactory news data. It automates the process of collecting economic news events for specified date ranges and saves the results as CSV files for further analysis.

## Features

- **Automated Data Scraping:** Uses Playwright with stealth mode to fetch news data from ForexFactory.
- **Custom Date Range:** Specify any start and end date to fetch news for multiple days.
- **CSV Export:** Saves each day's news as a separate CSV file in the `data/` directory.
- **Impact Mapping:** Converts ForexFactory's impact icons to human-readable levels (High, Medium, Low, Holiday).
- **Duplicate Prevention:** Skips dates that have already been downloaded.

## Project Structure

. ├── main.py # Main script for scraping and saving news data ├── main2.py # Alternate or experimental script (ignored by git) ├── requirements.txt # Python dependencies ├── README.md # Project documentation ├── data/ # Folder containing CSV files for each date └── .gitignore # Git ignore rules

## Requirements

- Python 3.7+
- [Playwright](https://playwright.dev/python/)
- [playwright-stealth](https://github.com/AtuboDad/playwright-stealth)
- See [requirements.txt](requirements.txt) for full list

## Installation

1. **Clone the repository:**

   ```sh
   git clone <repo-url>
   cd ff_news_history_bot

   ```

2. Create and activate a virtual environment (optional but recommended):

python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate

3. Install dependencies:
   pip install -r requirements.txt
   playwright install

Usage

1. Run the main script:
   python main.py

2. Input the date range when prompted:
   Enter start date (format: YYYY-MM-DD): 2022-08-01
   Enter end date (format: YYYY-MM-DD): 2022-08-10

3. CSV files will be saved in the data/ directory, named as aug01.2022.csv, aug02.2022.csv, etc.

Output Format
Each CSV file contains the following columns:

Time
Currency
Impact (High, Medium, Low, Holiday)
Event
Actual
Forecast
Previous

Customization
Change Date Format: The date format for CSV filenames is generated in generate_date_range in main.py.
Modify Impact Mapping: Adjust the IMPACT_MAPPING dictionary in main.py to change how impact icons are interpreted.

Notes
If a CSV file for a date already exists, it will be skipped to avoid redundant downloads.
Troubleshooting

If you encounter issues with Playwright, ensure all browsers are installed:
playwright install

For stealth mode issues, check the playwright-stealth documentation.
License
MIT License

This project is not affiliated with ForexFactory. Use responsibly and respect the website's terms of service.
