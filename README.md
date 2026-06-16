# worcester_weather_comp_capstone
I am going to create a dashboard that compare my beautiful city of Worcester, Massachusetts and compares it's weather to what are considered to be the 3 cities in the world with the best weather, San Diego, CA, Medillin, Columbia and Malaga, Spain.

# Summary 

I scraped timeanddate.com to get historical weather data for four cities, Worcester, MA; Medellin, Columbia; San Diego, CA; and Malaga, Spain.  I took the data of the past almost 13 months (June 2025 to June 2026) and compared the monthly average temperature. My scraper uses Selenium to navigate the site and collect data, which is saved to a CSV file and then cleaned and transformed using Pandas before being stored in a SQLite database. A command line query tool allows users to explore the data directly from the terminal, filtering by city, month, or temperature extremes.  I then took all of that to create my four visualizations in my Streamlit dashboard. The first visualization shows the average temperature of each city on a bar chart. The second is a line chart showing temperature trends over the time period.  There is an a slider for the date range so the user can check out a smaller period of time. The third visualization is a heatmap.  There is no better way to show the extreme temperatures than visualizing it as red hot or icy blue. My last visualization is another bar chart that shows a comfort score leaderboard.  I created a point system that rewards ideal temperatures and penalizes extreme temperatures.

It took me a long time to finally figure out a way to build something that successfully scraped the average monthly data.  I had to use a lot of trial and error.  It was so difficult that at one point I considered scrapping it and starting over. I am glad that I didn't for a number of reasons.  The main one being I have had fun poking fun at my city in both of my classes now.  The weather where I live has managed to be terrible every time I have been called on to create something with weather data.  I also think all of the failure pushed me to dig deeper on what I was doing.  I knew it could be done I just was getting frustrated in how to figure it out.  Once I had it functional it felt like a real achievement rather than quitting and going with something easier.

# Set up

1. Clone the repository to your local machine
2. Navigate to the project folder
3. Create a virtual environment and activate it:
    python3 -m venv .venv
    source .venv/bin/activate
4. Install dependencies:
    pip install -r requirements.txt
5. Run the scraper to collect data:
    python3 scrape_weather.py
6. Run the cleaner to process and store the data:
    python3 weather_cleaner.py
7. Query the database from the command line:
    python3 weather_query.py --all
8. Launch the dashboard:
    streamlit run dashboard.py