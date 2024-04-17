import requests
import json
from datetime import datetime, timedelta
import time
import os

def load_config():
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
    return config

def fetch_best_sellers_monthly(api_key, year):
    base_url = "https://api.nytimes.com/svc/books/v3/lists/full-overview.json"
    results = {}
    start_date = datetime(year, 1, 1)

    for month in range(1, 13):  # For each month in the year
        try:
            date = start_date.strftime('%Y-%m-%d')
            params = {
                'api-key': api_key,
                'published_date': date
            }
            response = requests.get(base_url, params=params)
            if response.status_code == 200:
                results[date] = response.json()
                print(f"Data fetched for {date}")
            else:
                print(f"Failed to fetch data for {date}: {response.status_code}")

            # Add a delay of 12 seconds to manage API rate limits
            print("Waiting 12 seconds before next API call...")
            time.sleep(12)

            start_date += timedelta(days=31)  # Move to the next month
            start_date = start_date.replace(day=1)  # Ensure we start at the first of the month
        except Exception as e:
            print(f"Error processing date {date}: {str(e)}")

    return results

def save_data(year, data):
    # Ensure the directory exists
    os.makedirs('../data/raw_data', exist_ok=True)

    # File path where the JSON will be saved
    file_path = f'../data/raw_data/{year}.json'

    # Writing JSON data to a file
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)
        print(f"Data for {year} successfully saved to {file_path}")

