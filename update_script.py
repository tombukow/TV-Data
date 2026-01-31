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
    
    # Wait for the sentiment element to load (robust to dynamic content)
    page.wait_for_selector('.sentiment-panel__text', timeout=30000)  # 30s timeout
    page.wait_for_timeout(2000)  # Extra wait for any remaining JS
    
    # Get full page content as text
    page_text = page.content()

    browser.close()

# Extract the long percentage using regex on full page text
match = re.search(r'(\d+)% of client accounts are long on this market', page_text)
if match:
    long_percentage = int(match.group(1))
else:
    raise ValueError("Could not find long percentage on the page. Check site structure or increase selector timeout.")

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
