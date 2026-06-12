import sqlite3
import pandas as pd


df = pd.read_csv("weather_clean.csv")

# weather score 
def score(row):
    temp_range = abs(row["hottest_temp"] - row["coldest_temp"])

    temp_score = max(0, 100 - temp_range * 2)
    wind_score = max(0, 100 - row["wind_speed"] * 3)

    precip = row["annual_precip"] if pd.notna(row["annual_precip"]) else 50
    rain_score = max(0, 100 - precip)

    total = (
        temp_score * 0.4 +
        wind_score * 0.2 +
        rain_score * 0.4
    )

    return round(total, 2)

df["weather_score"] = df.apply(score, axis=1)


conn = sqlite3.connect("weather.db")


df.to_sql(
    "weather_summary",
    conn,
    if_exists="replace",
    index=False
)

cursor = conn.cursor()

cursor.execute("""
SELECT city, weather_score
FROM weather_summary
ORDER BY weather_score DESC
""")

print("\nWeather Rankings\n")

for row in cursor.fetchall():
    print(row)

conn.close()

print("\nDatabase saved as weather.db")