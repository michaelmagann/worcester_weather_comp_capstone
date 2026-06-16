import pandas as pd
import sqlite3

INPUT_FILE = "raw_weather.csv"
DB_FILE = "weather.db"

# Load raw data
df = pd.read_csv(INPUT_FILE)
print("BEFORE CLEANING:")
print(df.head(10))
print(f"Shape: {df.shape}")
print(f"Data types:\n{df.dtypes}")
print(f"Missing values:\n{df.isnull().sum()}")

# Drop duplicates
df = df.drop_duplicates()

# Drop any rows with missing values
df = df.dropna()

# Convert columns to correct types
df["year"] = df["year"].astype(int)
df["month"] = df["month"].astype(int)
df["avg_f"] = df["avg_f"].astype(float)

# Add a month name column for easier reading
month_names = {
    1: "January", 2: "February", 3: "March", 4: "April",
    5: "May", 6: "June", 7: "July", 8: "August",
    9: "September", 10: "October", 11: "November", 12: "December"
}
df["month_name"] = df["month"].map(month_names)

# Add a sortable date column
df["date"] = pd.to_datetime(df[["year", "month"]].assign(day=1))

# Sort by city and date
df = df.sort_values(["city", "date"])

print("\nAFTER CLEANING:")
print(df.head(10))
print(f"Shape: {df.shape}")

# Save to SQLite
conn = sqlite3.connect(DB_FILE)
df.to_sql("weather", conn, if_exists="replace", index=False)
conn.close()

print(f"\nDone. Data saved to {DB_FILE}")