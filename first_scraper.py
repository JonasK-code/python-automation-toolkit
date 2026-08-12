import requests
from bs4 import BeautifulSoup
import pandas as pd

# 1. Fetch the raw HTML from the website
url = "http://books.toscrape.com/"
response = requests.get(url)

# 2. Parse the HTML using BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")

# 3. Find all book containers on the page
books = soup.find_all("article", class_="product_pod")

# 4. Extract title and price for each book
data = []
for book in books:
    # Grab the book title inside the <h3> <a> tag
    title = book.h3.a["title"]
    
    # Grab the price string inside the <p> tag with class 'price_color'
    price_text = book.find("p", class_="price_color").text
    
    # Add to our structured list
    data.append({"title": title, "raw_price": price_text})

# 5. Pipeline straight into Pandas for instant cleaning!
df = pd.DataFrame(data)

# Clean the price: strip currency symbols like £ and convert to float
df["clean_price"] = (
    df["raw_price"]
    .str.replace(r"[^\d.]", "", regex=True)
    .astype(float)
)

# Save output automatically
df.to_csv("scraped_books.csv", index=False)

print("--- Scraped Data Sample ---")
print(df.head()) # Shows the first 5 rows
print(f"\nSuccessfully extracted and cleaned {len(df)} items!")