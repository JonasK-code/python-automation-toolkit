import sqlite3
import requests
import logging
from bs4 import BeautifulSoup

# Configure logging to save events to a file
logging.basicConfig(
    filename="automation.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

url = "http://books.toscrape.com/catalogue/page-1.html"

try:
    logging.info("Starting scrape job...")
    response = requests.get(url, timeout=5)
    response.raise_for_status()  
    
    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.find_all("article", class_="product_pod")
    
    conn = sqlite3.connect("automation.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scraped_books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE,
            price_gbp REAL
        )
    """)
    
    inserted_count = 0
    for book in books:
        title = book.h3.a["title"]
        price = float(book.find("p", class_="price_color").text.replace("£", "").replace("Â", ""))
        
        cursor.execute("INSERT OR IGNORE INTO scraped_books (title, price_gbp) VALUES (?, ?)", (title, price))
        if cursor.rowcount > 0:
            inserted_count += 1
            
    conn.commit()
    conn.close()
    
    logging.info(f"Scrape completed successfully. Added {inserted_count} new records.")
    print(f"Success! Check 'automation.log' to see the execution log.")

except requests.exceptions.RequestException as e:
    logging.error(f"Network error occurred: {e}")
    print("Network error caught and logged.")

except Exception as e:
    logging.error(f"Unexpected error: {e}")
    print("Unexpected error caught and logged.")