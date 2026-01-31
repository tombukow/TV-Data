import csv
import os
from datetime import datetime
import zoneinfo  # For timezone handling
import re
from playwright.sync_api import sync_playwright

# URL to scrape
url = 'https://www.ig.com/en/indices/markets-indices/us-tech-100'

# Launch Playwright and scrape
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(url)
    page.wait_for_timeout(2000)  # Wait 2 seconds for JS to load
    
    # Wait for the sentiment panel to appear and extract text
    sentiment_element = page.wait_for_selector('.sentiment-panel__text', timeout=10000)  # 10s timeout
    if sentiment_element:
        sentiment_text = sentiment_element.inner_text()
    else:
        raise ValueError("Sentiment panel not found. Check site structure or increase wait time.")
    
    browser.close()

# Extract the long percentage using regex
match = re.search(r'(\d+)% of client accounts are long on this market', sentiment_text)
if match:
    long_percentage = int(match.group(1))
else:
    raise ValueError("Could not find long percentage in the sentiment text. Check site structure.")

# Get current timestamp in Eastern Time
tz = zoneinfo.ZoneInfo('US/Eastern')
timestamp = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')

# CSV file path
csv_file = 'data.csv'

# Create CSV if it doesn't exist, with headers
if not os.path.exists(csv_file):
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'long_percentage'])

# Append the new row
with open(csv_file, 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([timestamp, long_percentage])

print(f"Appended: {timestamp}, {long_percentage}%")
