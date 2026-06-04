import pandas as pd

df = pd.read_csv("weather_clean.csv")

def score(row):
    temp_range = abs(row["hottest_temp"] - row["coldest_temp"])

    # lower is better for all metrics
    temp_score = max(0, 100 - temp_range * 2)
    wind_score = max(0, 100 - row["wind_speed"] * 3)

    # precipitation penalty (missing treated as average)
    precip = row["annual_precip"] if pd.notna(row["annual_precip"]) else 50
    rain_score = max(0, 100 - precip)

    total = (
        temp_score * 0.4 +
        wind_score * 0.2 +
        rain_score * 0.4
    )

    return round(total, 2)

df["weather_score"] = df.apply(score, axis=1)

df = df.sort_values("weather_score", ascending=False)

print(df[["city", "weather_score"]])