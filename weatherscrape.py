from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

cities = {
    "Worcester": "https://www.timeanddate.com/weather/usa/worcester/climate",
    "San Diego": "https://www.timeanddate.com/weather/usa/san-diego/climate",
    "Medellin": "https://www.timeanddate.com/weather/colombia/medellin/climate",
    "Malaga": "https://www.timeanddate.com/weather/spain/malaga/climate"
}

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install())
)

all_data = []

for city, url in cities.items():
    print(f"Scraping {city}")

    driver.get(url)
    time.sleep(4)

    tables = driver.find_elements(By.TAG_NAME, "table")

    print(f"Found {len(tables)} tables for {city}")

    for i, table in enumerate(tables):
        table_text = table.text

        if table_text.strip():
            all_data.append({
                "city": city,
                "table_index": i,
                "table_text": table_text
            })

driver.quit()

df = pd.DataFrame(all_data)

df.to_csv("weather_raw.csv", index=False)

print("Saved weather_raw.csv")
print(df.head())