import os
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("API_KEY")
db_pass = os.getenv("DB_PASSWORD")

if not api_key or not db_pass:
    print("Error: Required environment variables are missing.")
else:
    print("Environment variables loaded safely!")
    print(f"API Key: {api_key}")
    print(f"DB Password: {'*' * len(db_pass)}")