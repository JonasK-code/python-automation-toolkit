import sqlite3
import requests
from bs4 import BeautifulSoup

# Connect to database
conn = sqlite3.connect("automation.db")
cursor = conn.cursor()


cursor.execute("""
    CREATE TABLE IF NOT EXISTS scraped_books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT UNIQUE,
        price_gbp REAL
    )
""")

# Scrapeº page
url = "http://books.toscrape.com/catalogue/page-1.html"
response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
soup = BeautifulSoup(response.text, "html.parser")

new_records = 0
for item in soup.find_all("article", class_="product_pod"):
    title = item.h3.a["title"]
    price_str = item.find("p", class_="price_color").text
    price = float(price_str.replace("£", "").replace("Â", ""))

    cursor.execute("""
        INSERT OR IGNORE INTO scraped_books (title, price_gbp)
        VALUES (?, ?)
    """, (title, price))
    
    if cursor.rowcount > 0:
        new_records += 1

conn.commit()

# Verify stored records count
cursor.execute("SELECT COUNT(*) FROM scraped_books")
total_records = cursor.fetchone()[0]

conn.close()

print(f"Done! Inserted {new_records} new books. Total records in DB: {total_records}")