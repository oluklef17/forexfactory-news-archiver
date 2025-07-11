import asyncio
import os
import csv
from datetime import datetime, timedelta
from playwright.async_api import async_playwright
from playwright_stealth import stealth_sync

# Mapping of impact class names to readable impact levels
IMPACT_MAPPING = {
    "icon icon--ff-impact-red": "High",
    "icon icon--ff-impact-ora": "Medium",
    "icon icon--ff-impact-yel": "Low",
    "icon icon--ff-impact-gra": "Holiday"
}

# Function to create a 'data' folder if it doesn't exist
def create_data_folder():
    if not os.path.exists("data"):
        os.makedirs("data", exist_ok=True)

# Function to save news data to a CSV file
def save_to_csv(date_str, news_data):
    create_data_folder()  # Ensure 'data' folder exists
    filename = f"data/{date_str}.csv"

    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Time", "Currency", "Impact", "Event", "Actual", "Forecast", "Previous"])

        for news in news_data:
            writer.writerow([
                news["time"], news["currency"], news["impact"], news["event"],
                news["actual"], news["forecast"], news["previous"]
            ])

    print(f"✅ Data for {date_str} saved to {filename}")

# Function to fetch news data for a given date
async def scrape_forex_news(date_str: str):
    global IMPACT_MAPPING
    print("Impacts: ", IMPACT_MAPPING)
    url = f"https://www.forexfactory.com/calendar?day={date_str}"
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Run headless
        page = await browser.new_page()
        stealth_sync(page)  # Enable stealth mode

        await page.goto(url, timeout=60000)
        await page.wait_for_load_state("networkidle")

        try:
            await page.wait_for_selector("table.calendar__table", timeout=20000)
        except Exception as e:
            print(f"⚠️ Table not found for {date_str}. Skipping...")
            return []

        news_data = []
        rows = await page.query_selector_all("table.calendar__table tbody tr")

        prev_time = "N/A"

        for row in rows:
            try:
                time_element = await row.query_selector("td.calendar__time")
                currency_element = await row.query_selector("td.calendar__currency")
                impact_element = await row.query_selector("td.calendar__impact span")
                event_element = await row.query_selector("td.calendar__event")
                actual_element = await row.query_selector("td.calendar__actual")
                forecast_element = await row.query_selector("td.calendar__forecast")
                previous_element = await row.query_selector("td.calendar__previous")

                # Extract text safely (Check if element exists)
                time = await time_element.inner_text() if time_element else "N/A"
                currency = await currency_element.inner_text() if currency_element else "N/A"
                impact_class = await impact_element.get_attribute("class") if impact_element else ""
                event = await event_element.inner_text() if event_element else "N/A"
                actual = await actual_element.inner_text() if actual_element else "N/A"
                forecast = await forecast_element.inner_text() if forecast_element else "N/A"
                previous = await previous_element.inner_text() if previous_element else "N/A"

                if time == "N/A" or time.strip() == "":
                    time = prev_time

                # Convert impact class to human-readable format
                impact = IMPACT_MAPPING.get(impact_class.strip(), "Unknown")

                news_data.append({
                    "time": time.strip(),
                    "currency": currency.strip(),
                    "impact": impact,
                    "event": event.strip(),
                    "actual": actual.strip(),
                    "forecast": forecast.strip(),
                    "previous": previous.strip(),
                })

                if time != "N/A":
                    prev_time = time

            except Exception as e:
                print(f"Error parsing row for {date_str}: {e}")

        await browser.close()
    
    return news_data

# Function to generate date range list
def generate_date_range(start_date, end_date):
    date_list = []
    current_date = start_date

    while current_date <= end_date:
        date_list.append(current_date.strftime("%b%d.%Y").lower())  # Format as 'aug1.2022'
        current_date += timedelta(days=1)

    return date_list

# Function to check if a CSV file already exists
def csv_exists(date_str):
    return os.path.exists(f"data/{date_str}.csv")

# Main function to handle user input and fetch data for the date range
async def main():
    # Get user input
    start_date_str = input("Enter start date (format: YYYY-MM-DD): ")
    end_date_str = input("Enter end date (format: YYYY-MM-DD): ")

    # Convert input to datetime objects
    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    except ValueError:
        print("❌ Invalid date format! Please use YYYY-MM-DD.")
        return

    # Generate the list of dates in ForexFactory format
    date_list = generate_date_range(start_date, end_date)

    print(f"📅 Fetching news data from {start_date_str} to {end_date_str}...")

    # Loop through each date and fetch news data if CSV doesn't exist
    for date_str in date_list:
        if csv_exists(date_str):
            print(f"⚠️ Skipping {date_str} (CSV already exists)")
            continue
        
        news_data = await scrape_forex_news(date_str)
        if news_data:
            save_to_csv(date_str, news_data)
        else:
            print(f"⚠️ No data available for {date_str}")

if __name__ == "__main__":
    asyncio.run(main())
