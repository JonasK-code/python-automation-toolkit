# Python Automation Toolkit

A collection of lightweight Python scripts built to scrape web data, store records in SQLite, and handle background task scheduling.

## Included Scripts
* `scrape_to_sql.py` – Scrapes books.toscrape.com and saves title/price directly to SQL.
* `robust_scraper.py` – Handles network timeouts gracefully and logs errors to `automation.log`.
* `scheduled_job.py` – Runs automation scripts on a recurring background loop using `schedule`.
* `secure_config.py` – Loads private API keys and database logins safely from a `.env` file.

## Quickstart
1. Clone the repo: `git clone https://github.com/JonasK-code/python-automation-toolkit.git`
2. Add a `.env` file with your credentials.
3. Run any script: `python3 robust_scraper.py`
