import csv
import os
from datetime import datetime
import zoneinfo  # For timezone handling
import re
from playwright.sync_api import sync_playwright

# URL to scrape
url = 'https://www.ig.com/uk/indices/markets-indices/us-tech-100'

# Launch Playwright and scrape
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(url)
    
    # Wait for the sentiment element with longer timeout
    page.wait_for_selector('.sentiment-panel__text', timeout=60000)  # 60s timeout
    
    # Extract clean text from the specific element (strips HTML tags)
    sentiment_text = page.locator('.sentiment-panel__text').inner_text()
    
    browser.close()

# Extract the long percentage using regex on clean text
match = re.search(r'(\d+)% of client accounts are long on this market', sentiment_text)
if match:
    long_percentage = int(match.group(1))
else:
    raise ValueError("Could not find long percentage in the text. Check regex or site structure.")

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
