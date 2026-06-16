import sqlite3
import argparse

DB_FILE = "weather.db"


def get_connection():
    return sqlite3.connect(DB_FILE)

# Running a SQL query that selects every row from the database ordered by city & date. It then prints it as a formatted table in the terminal.

def query_all():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT city, year, month_name, avg_f FROM weather ORDER BY city, date")
    rows = cursor.fetchall()
    conn.close()
    print(f"\n{'City':<12} {'Year':<6} {'Month':<12} {'Avg Temp (F)':<12}")
    print("-" * 44)
    for row in rows:
        print(f"{row[0]:<12} {row[1]:<6} {row[2]:<12} {row[3]:<12}")

#This adds a filter so it returns only the rows for a specific city, ordered by date.

def query_city(city):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT city, year, month_name, avg_f FROM weather WHERE city = ? ORDER BY date",
        (city,)
    )
    rows = cursor.fetchall()
    conn.close()
    if not rows:
        print(f"No data found for city: {city}")
        return
    print(f"\n{'City':<12} {'Year':<6} {'Month':<12} {'Avg Temp (F)':<12}")
    print("-" * 44)
    for row in rows:
        print(f"{row[0]:<12} {row[1]:<6} {row[2]:<12} {row[3]:<12}")

# Filters month number and returns my four cities for that month sorted by temp from hottest to coldest.

def query_month(month):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT city, year, month_name, avg_f FROM weather WHERE month = ? ORDER BY avg_f DESC",
        (month,)
    )
    rows = cursor.fetchall()
    conn.close()
    if not rows:
        print(f"No data found for month: {month}")
        return
    print(f"\n{'City':<12} {'Year':<6} {'Month':<12} {'Avg Temp (F)':<12}")
    print("-" * 44)
    for row in rows:
        print(f"{row[0]:<12} {row[1]:<6} {row[2]:<12} {row[3]:<12}")

# Next two do the same thing but sort differently. Hottest sorts so that the highest return first. Coldest does the opposite.

def query_hottest():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT city, year, month_name, avg_f FROM weather ORDER BY avg_f DESC LIMIT 5"
    )
    rows = cursor.fetchall()
    conn.close()
    print("\nTop 5 hottest months across all cities:")
    print(f"\n{'City':<12} {'Year':<6} {'Month':<12} {'Avg Temp (F)':<12}")
    print("-" * 44)
    for row in rows:
        print(f"{row[0]:<12} {row[1]:<6} {row[2]:<12} {row[3]:<12}")


def query_coldest():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT city, year, month_name, avg_f FROM weather ORDER BY avg_f ASC LIMIT 5"
    )
    rows = cursor.fetchall()
    conn.close()
    print("\nTop 5 coldest months across all cities:")
    print(f"\n{'City':<12} {'Year':<6} {'Month':<12} {'Avg Temp (F)':<12}")
    print("-" * 44)
    for row in rows:
        print(f"{row[0]:<12} {row[1]:<6} {row[2]:<12} {row[3]:<12}")

# This is the controller. It sets up all the possible arguments, reads what is in the termal and then calls the function based on what argument passed.

def main():
    parser = argparse.ArgumentParser(description="Query the weather database")
    parser.add_argument("--all", action="store_true", help="Show all data")
    parser.add_argument("--city", type=str, help="Filter by city name")
    parser.add_argument("--month", type=int, help="Filter by month number (1-12)")
    parser.add_argument("--hottest", action="store_true", help="Show top 5 hottest months")
    parser.add_argument("--coldest", action="store_true", help="Show top 5 coldest months")
    args = parser.parse_args()

    if args.all:
        query_all()
    elif args.city:
        query_city(args.city)
    elif args.month:
        query_month(args.month)
    elif args.hottest:
        query_hottest()
    elif args.coldest:
        query_coldest()
    else:
        print("Please provide an argument. Options:")
        print("  --all           Show all data")
        print("  --city NAME     Filter by city (Worcester, Medellin, San Diego, Malaga)")
        print("  --month NUMBER  Filter by month number (1-12)")
        print("  --hottest       Show top 5 hottest months")
        print("  --coldest       Show top 5 coldest months")


if __name__ == "__main__":
    main()