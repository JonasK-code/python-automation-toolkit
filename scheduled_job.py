import time
import schedule
import logging

# Configure log file
logging.basicConfig(
    filename="schedule.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def run_automation_job():
    logging.info("Executing scheduled task...")
    print("Task executed. Check 'schedule.log'.")

# Run every 10 seconds
schedule.every(10).seconds.do(run_automation_job)

print("Scheduler active. Press Ctrl+C to stop.")

while True:
    schedule.run_pending()
    time.sleep(1)