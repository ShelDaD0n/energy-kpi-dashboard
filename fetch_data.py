import requests
import pandas as pd
from dotenv import load_dotenv
import os

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=dotenv_path)
API_KEY = os.getenv("EIA_API_KEY")
print(f"API KEY LOADED: {API_KEY}")

def fetch_solar_generation():
    url = "https://api.eia.gov/v2/electricity/rto/region-data/data/"

    params = {
    
        "api_key": API_KEY,
        "frequency": "hourly",
        "data[0]": "value",
        "facets[type][]": "NG",
        "facets[respondent][]": "CAL",
        "start": "2024-01-01T00",
        "end": "2024-03-31T23",
        "sort[0][column]": "period",
        "sort[0][direction]": "asc",
        "length": 5000,
        "offset": 0
        
    }

    print("Fetching data from EIA API...")
    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

    raw = response.json()
    records = raw["response"]["data"]
    print(f"Retrieved {len(records)} records")

    df = pd.DataFrame(records)
    print(df.head())

    df.to_csv("data/raw_generation.csv", index=False)
    print("Saved to data/raw_generation.csv")

    return df

if __name__ == "__main__":
    fetch_solar_generation()