import sqlite3
import pandas as pd

books = [
    {"title": "A Light in the Attic", "price_eur": 60.56},
    {"title": "Tipping the Velvet", "price_eur": 62.87},
    {"title": "Soumission", "price_eur": 58.61},
    {"title": "Sharp Objects", "price_eur": 55.94}
]

# Connect to database file
conn = sqlite3.connect("automation.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT UNIQUE,
        price_eur REAL
    )
""")

# Insert records, skipping duplicates
for book in books:
    cursor.execute("""
        INSERT OR IGNORE INTO books (title, price_eur)
        VALUES (?, ?)
    """, (book["title"], book["price_eur"]))

conn.commit()

# Query expensive books into pandas
df = pd.read_sql_query("SELECT title, price_eur FROM books WHERE price_eur > 60", conn)
conn.close()

print("--- Books Over €60 (Queried from SQL) ---")
print(df)