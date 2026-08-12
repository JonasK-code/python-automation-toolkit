import requests
import pandas as pd

print("Fetching live currency data from API...")

# 1. Send a GET request to a free, public API endpoint
url = "https://open.er-api.com/v6/latest/USD"
response = requests.get(url)

# Check if request was successful (HTTP Status Code 200)
if response.status_code == 200:
    # 2. Convert raw response directly into a Python Dictionary (JSON)
    data = response.json()
    
    # 3. Extract rates dictionary
    rates = data["rates"]
    
    # 4. Load dictionary straight into a Pandas DataFrame
    df = pd.DataFrame(list(rates.items()), columns=["Currency", "Rate_to_USD"])
    
    # 5. Filter for target currencies
    target_currencies = ["EUR", "GBP", "CAD", "AUD", "JPY", "CHF"]
    filtered_df = df[df["Currency"].isin(target_currencies)].reset_index(drop=True)
    
    # 6. Save to CSV
    output_file = "live_exchange_rates.csv"
    filtered_df.to_csv(output_file, index=False)
    
    print("\n--- Live Currency Rates (Base: 1 USD) ---")
    print(filtered_df)
    print(f"\nSuccessfully saved to {output_file}!")
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")
