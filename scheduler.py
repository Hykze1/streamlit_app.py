import schedule
import time
from scraper import scrape_ibdb, save_data

def job():
    print("Starting scrape...")
    shows_list = scrape_ibdb()
    save_data(shows_list,
              sender_email="you@gmail.com",
              sender_password="your_app_password",
              recipient_email="you@gmail.com")

schedule.every(3).minutes.do(job)

print("Scheduler running. Press Ctrl+C to stop.")

while True:
    schedule.run_pending()
    time.sleep(1)
