import requests
from bs4 import BeautifulSoup
import pandas as pd

print("--- Starting Week 1 Automation Pipeline ---")

# 1. FETCH LIVE EXCHANGE RATE FROM API (GBP -> EUR)
print("1. Fetching live GBP to EUR exchange rate...")
api_url = "https://open.er-api.com/v6/latest/GBP"
api_response = requests.get(api_url)

if api_response.status_code == 200:
    gbp_to_eur_rate = api_response.json()["rates"]["EUR"]
    print(f"   Current Rate: 1 GBP = {gbp_to_eur_rate:.4f} EUR")
else:
    gbp_to_eur_rate = 1.17  # Fallback rate if API fails
    print("   API request failed, using fallback rate.")

# 2. SCRAPE WEBPAGE DATA
print("\n2. Scraping book titles and prices...")
scrape_url = "http://books.toscrape.com/catalogue/page-1.html"
headers = {"User-Agent": "Mozilla/5.0"}
scrape_response = requests.get(scrape_url, headers=headers)

soup = BeautifulSoup(scrape_response.text, "html.parser")
books = soup.find_all("article", class_="product_pod")

book_list = []
for book in books:
    title = book.h3.a["title"]
    # Strip the £ symbol and convert string to float
    price_gbp_str = book.find("p", class_="price_color").text
    price_gbp = float(price_gbp_str.replace("£", "").replace("Â", ""))
    
    book_list.append({
        "Title": title,
        "Price_GBP": price_gbp
    })

# 3. TRANSFORM DATA WITH PANDAS
print("\n3. Processing data with Pandas...")
df = pd.DataFrame(book_list)

# Calculate dynamic EUR price using live API rate
df["Price_EUR"] = (df["Price_GBP"] * gbp_to_eur_rate).round(2)

# 4. EXPORT TO CSV
output_file = "week1_capstone_output.csv"
df.to_csv(output_file, index=False)

print("\n--- Pipeline Execution Summary ---")
print(df.head(5))
print(f"\nPipeline finished successfully! Output saved to '{output_file}'.")
