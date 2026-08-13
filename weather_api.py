import requests
import pandas as pd

# 1. Base API endpoint
url = "https://api.open-meteo.com/v1/forecast"

# 2. Define query parameters (Latitude & Longitude for Berlin)
params = {
    "latitude": 52.52,
    "longitude": 13.41,
    "hourly": "temperature_2m,relative_humidity_2m",
    "forecast_days": 1
}

print("Fetching hourly weather forecast from API...")

# 3. Pass parameters directly into the request
response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    
    # 4. Drill into the nested "hourly" key
    hourly_data = data["hourly"]
    
    # 5. Convert the nested dictionary into a DataFrame
    df = pd.DataFrame(hourly_data)
    
    # Clean column names
    df.columns = ["time", "temperature_c", "humidity_pct"]
    
    # Format time string for better readability
    df["time"] = df["time"].str.replace("T", " ")
    
    # 6. Save to CSV
    output_file = "weather_forecast.csv"
    df.to_csv(output_file, index=False)
    
    print("\n--- First 5 Hours of Forecast ---")
    print(df.head())
    print(f"\nSuccessfully saved {len(df)} rows to {output_file}!")
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")
