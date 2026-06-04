import pandas as pd
import re

df = pd.read_csv("weather_raw.csv")

rows = []

for _, r in df.iterrows():
    city = r["city"]
    text = r["table_text"]

    # ONLY process climate summary blocks
    if "Hottest Month" not in text:
        continue

    def extract(pattern):
        match = re.search(pattern, text)
        return match.group(1) if match else None

    def extract_float(pattern):
        match = re.search(pattern, text)
        return float(match.group(1)) if match else None

    rows.append({
        "city": city,
        "hottest_month": extract(r"Hottest Month (\w+)"),
        "hottest_temp": extract_float(r"Hottest Month \w+ \((\d+)\s*°F"),
        "coldest_month": extract(r"Coldest Month (\w+)"),
        "coldest_temp": extract_float(r"Coldest Month \w+ \((\d+)\s*°F"),
        "wettest_month": extract(r"Wettest Month (\w+)"),
        "annual_precip": extract_float(r"Annual precip.*\(([\d.]+)"),
        "windiest_month": extract(r"Windiest Month (\w+)"),
        "wind_speed": extract_float(r"Windiest Month \w+ \((\d+)")
    })

clean_df = pd.DataFrame(rows)

clean_df.to_csv("weather_clean.csv", index=False)

print(clean_df)
print("\nSaved weather_clean.csv")