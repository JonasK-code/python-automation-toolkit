import time
import requests
from bs4 import BeautifulSoup
import pandas as pd

all_books = []

# 1. Loop through pages 1 to 3
for page in range(1, 4):
    url = f"http://books.toscrape.com/catalogue/page-{page}.html"
    print(f"Fetching page {page}...")
    
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Could not reach page {page}. Skipping...")
        continue

    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.find_all("article", class_="product_pod")

    # 2. Extract data from each book on the current page
    for book in books:
        title = book.h3.a["title"]
        price_text = book.find("p", class_="price_color").text
        
        all_books.append({
            "page_number": page,
            "title": title,
            "raw_price": price_text
        })

    # 3. Polite Scraper rule: pause 1 second between requests
    time.sleep(1)

# 4. Pipeline into Pandas
df = pd.DataFrame(all_books)

# Clean prices using your Regex formula from Day 3
df["clean_price"] = (
    df["raw_price"]
    .str.replace(r"[^\d.]", "", regex=True)
    .astype(float)
)

# 5. Export master dataset
output_file = "all_books_multipage.csv"
df.to_csv(output_file, index=False)

print("\n--- Scraping Complete ---")
print(f"Total items extracted across 3 pages: {len(df)}")
print(f"Saved to: {output_file}")
print("\nFirst 5 rows:")
print(df.head())
