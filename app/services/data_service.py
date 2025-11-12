import pandas as pd
from functools import lru_cache
from pathlib import Path

# We use lru_cache to load the data only once and cache the result.
# This is much more efficient than reading from disk on every API call.
@lru_cache()
def load_and_clean_data():
    """
    Loads, cleans, and returns the vaccine dataset as a Pandas DataFrame.
    The result is cached to prevent reloading from disk on every request.
    """
    try:
        # Build path relative to this file: app/data/country_vaccinations.csv
        data_path = Path(__file__).parents[1] / "data" / "country_vaccinations.csv"
        df = pd.read_csv(data_path)

        # --- Data Cleaning ---
        df['date'] = pd.to_datetime(df['date'])
        df['year'] = df['date'].dt.year

        # Create a 'vaccine_brand' list column from the comma-separated string
        df['vaccine_brand'] = df['vaccines'].apply(lambda x: [v.strip() for v in x.split(',')])

        # Fill missing numerical values
        numeric_cols = ['total_vaccinations', 'people_vaccinated', 'people_fully_vaccinated', 'daily_vaccinations']
        df[numeric_cols] = df.groupby('country')[numeric_cols].ffill().fillna(0)

        print("✅ Service: Dataset loaded and cleaned.")
        return df

    except FileNotFoundError:
        print("❌ SERVICE ERROR: Data file not found.")
        return pd.DataFrame()

def get_filtered_vaccine_data(country: str | None = None, vaccine: str | None = None, year: int | None = None):
    """
    Filters the vaccine data based on country, vaccine brand, and year.
    """
    df = load_and_clean_data()
    if df.empty:
        return []

    # Make a copy to avoid changing the cached original DataFrame
    filtered_df = df.copy()

    # Apply filters sequentially
    if country:
        filtered_df = filtered_df[filtered_df['country'] == country]

    if year:
        filtered_df = filtered_df[filtered_df['year'] == year]

    if vaccine:
        # Explode list column to allow filtering by a specific vaccine brand
        filtered_df = filtered_df.explode('vaccine_brand')
        filtered_df = filtered_df[filtered_df['vaccine_brand'] == vaccine]

    # Convert the resulting DataFrame to a list of dictionaries for the API response
    return filtered_df.to_dict(orient='records')