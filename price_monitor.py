import os
import time
import sqlite3
import logging
import requests
import schedule
from bs4 import BeautifulSoup
from dotenv import load_dotenv


load_dotenv()
TARGET_URL = os.getenv("TARGET_URL", "http://books.toscrape.com")

logging.basicConfig(
    filename="automation.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def init_db():
    conn = sqlite3.connect("capstone.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS product_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE,
            price TEXT,
            scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def run_pipeline():
    logging.info("Starting capstone automation run...")
    print("Running automation job...")
    
    try:
        response = requests.get(TARGET_URL, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Network error during scrape: {e}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.find_all("article", class_="product_pod")
    
    conn = sqlite3.connect("capstone.db")
    cursor = conn.cursor()
    new_records = 0

    for book in books:
        title = book.h3.a["title"]
        price = book.find("p", class_="price_color").text
        
        
        cursor.execute(
            "INSERT OR IGNORE INTO product_prices (title, price) VALUES (?, ?)",
            (title, price)
        )
        if cursor.rowcount > 0:
            new_records += 1

    conn.commit()
    conn.close()
    
    logging.info(f"Pipeline complete. Processed {len(books)} items ({new_records} new).")
    print(f"Run complete. Added {new_records} new records.")


if __name__ == "__main__":
    init_db()
    
   
    run_pipeline()
    
   
    schedule.every(30).seconds.do(run_pipeline)
    
    print("Capstone scheduler actively running. Press Ctrl+C to exit.")
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nScheduler stopped by user.")