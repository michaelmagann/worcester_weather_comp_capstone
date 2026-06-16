import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

DB_FILE = "weather.db"

def load_data():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql("SELECT * FROM weather ORDER BY date", conn)
    conn.close()
    return df

df = load_data()
df["avg_f"] = pd.to_numeric(df["avg_f"], errors="coerce")

st.title("Global Weather Comparison")
st.write("omparing average monthly temperatures across Worcester, MA; Medellín, Columbia; San Diego, CA; and Malaga, Spain over the last 13 months.")

st.markdown("---")

# VISUALIZATION 1: Overall average temperature by city bar chart
st.subheader("Overall Average Temperature by City")
st.write("Which cities would you want to live in? Which would you not?")

avg_by_city = df.groupby("city")["avg_f"].mean().reset_index()
avg_by_city.columns = ["city", "avg_temp"]
avg_by_city = avg_by_city.sort_values("avg_temp", ascending=False)

fig1 = px.bar(
    avg_by_city,
    x="city",
    y="avg_temp",
    color="city",
    labels={"avg_temp": "Avg Temp (°F)", "city": "City"},
    title="Overall Average Temperature by City"
)
st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")

# VISUALIZATION 2: Temperature overtime line chart
st.subheader("Average Monthly Temperature Over Time")
st.write("Each line represents one city. Use the date range slider to zoom in on a specific period.")

min_date = pd.to_datetime(df["date"]).min()
max_date = pd.to_datetime(df["date"]).max()

start_date, end_date = st.slider(
    "Select date range",
    min_value=min_date.to_pydatetime(),
    max_value=max_date.to_pydatetime(),
    value=(min_date.to_pydatetime(), max_date.to_pydatetime()),
    format="MMM YYYY"
)

filtered_df = df[
    (pd.to_datetime(df["date"]) >= start_date) &
    (pd.to_datetime(df["date"]) <= end_date)
]

fig2 = px.line(
    filtered_df,
    x="date",
    y="avg_f",
    color="city",
    markers=True,
    labels={"avg_f": "Avg Temp (°F)", "date": "Month", "city": "City"},
    title="Average Monthly Temperature by City"
)
st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# VISUALIZATION 3: Temperature by city and month heatmap
st.subheader("Temperature Heatmap by City and Month")
st.write("Each cell shows the average temperature for that city and month. Darker colors mean cooler temperatures, warmer colors mean hotter temperatures")

heatmap_df = df.pivot_table(index="city", columns="month_name", values="avg_f")

month_order = ["January", "February", "March", "April", "May", "June",
               "July", "August", "September", "October", "November", "December"]

heatmap_df = heatmap_df.reindex(columns=[m for m in month_order if m in heatmap_df.columns])

fig3 = px.imshow(
    heatmap_df,
    color_continuous_scale="RdYlBu_r",
    labels={"color": "Avg Temp (°F)"},
    title="Average Temperature by City and Month",
)
fig3.update_layout(
    xaxis_title="Month",
    yaxis_title="City"
)
st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# VISUALIZATION 4: Comfort score leaderboard bar chart
st.subheader("Comfort Score Leaderboard")
st.write("Scoring: 65°F to 72°F earns 2 points (perfect), 50°F to 64°F or 73°F to 80°F earns 1 point (good enough), 45°F to 49°F or 81°F to 90°F earns 0 points (could be better, could be worse), 32°F to 44°F loses 2 points (cold but if there is no wind and sun it's bad but not terrible), and below 32°F or above 90°F loses 3 points (stay inside).")

def comfort_score(temp):
    if 65 <= temp <= 72:
        return 2
    elif 50 <= temp < 65 or 72 < temp <= 80:
        return 1
    elif 45 <= temp < 50:
        return 0
    elif temp < 32 or temp > 90:
        return -3
    elif temp < 45:
        return -2
    else:
        return -1

df["comfort"] = df["avg_f"].apply(comfort_score)
scores = df.groupby("city")["comfort"].sum().reset_index()
scores.columns = ["city", "comfort_score"]
scores = scores.sort_values("comfort_score", ascending=False)

fig4 = px.bar(
    scores,
    x="city",
    y="comfort_score",
    color="city",
    labels={"comfort_score": "Comfort Score", "city": "City"},
    title="Comfort Score by City (Higher is Better)"
)

fig4.update_traces(textposition="outside")
fig4.update_layout(yaxis=dict(range=[-5, 20], dtick=5))

st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")
st.caption("Data scraped from timeanddate.com. Showing the weather of my Worcester, MA vs Medellín, Columbia, San Diego, CA and Malaga, Spain.")