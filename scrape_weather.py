import csv
import time
import re
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

# Set up the city list, length of time to look and build the CSV file.
CITIES = {
    "Worcester": "https://www.timeanddate.com/weather/usa/worcester/historic",
    "Medellin":  "https://www.timeanddate.com/weather/colombia/medellin/historic",
    "San Diego": "https://www.timeanddate.com/weather/usa/san-diego/historic",
    "Malaga":    "https://www.timeanddate.com/weather/spain/malaga/historic",
}

MONTHS_BACK = 12
OUTPUT_FILE = "raw_weather.csv"

# Launches chrome browswer for Selenium to control. It also makes it so that it identifies as human rather than a bot.

def create_driver():
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
    driver = webdriver.Chrome(options=options)
    return driver

# Builds the months to scrape. I went back a year. 

def get_month_year_list(months_back):
    now = datetime.now()
    results = []
    month = now.month
    year = now.year
    for _ in range(months_back + 1):
        results.append((month, year))
        month -= 1
        if month == 0:
            month = 12
            year -= 1
    return results

# This is where most of my scraping is done. It does four things: loads the city historic page, finds the month dropdown and selects the right year and month, reads all the text into a single string and then uses a regex pattern to search for the average temerpature. Easily the hardest part of this build for me.

def scrape_page(driver, url, city, month, year):
    try:
        driver.get(url)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "wt-his"))
        )
        time.sleep(2)

        try:
            month_select = Select(driver.find_element(By.ID, "month"))
            month_value = f"{year}-{month:02d}"
            month_select.select_by_value(month_value)
            time.sleep(3)
        except Exception as e:
            print(f"  Could not select month {month}/{year} for {city}: {e}")
            return None

        page_text = driver.find_element(By.TAG_NAME, "body").text

        avg = re.search(r"Average\s+([\d]+)\s*°F", page_text)

        if avg:
            return {
                "city":  city,
                "year":  year,
                "month": month,
                "avg_f": avg.group(1),
            }
        else:
            print(f"  Could not find temp data for {city} {month}/{year}")
            return None

    except Exception as e:
        print(f"  Failed for {city} {month}/{year}: {e}")
        return None

# This launches the browser, builds the list of months to scrape and then loops through the cities and months.  Every successful results gets added to all rows.  When it is done it writes my CSV.

def main():
    driver = create_driver()
    all_rows = []
    months = get_month_year_list(MONTHS_BACK)

    for city, url in CITIES.items():
        print(f"\nScraping {city}...")
        for month, year in months:
            print(f"  {month}/{year}...")
            row = scrape_page(driver, url, city, month, year)
            if row:
                print(f"    Avg: {row['avg_f']}")
                all_rows.append(row)
            time.sleep(2)

    driver.quit()

    if all_rows:
        fieldnames = ["city", "year", "month", "avg_f"]
        with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_rows)
        print(f"\nDone. {len(all_rows)} rows saved to {OUTPUT_FILE}")
    else:
        print("\nNo data was collected.")


if __name__ == "__main__":
    main()