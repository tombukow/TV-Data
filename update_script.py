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
    # Launch with user-agent and flags to evade headless detection
    browser = p.chromium.launch(
        headless=True,
        args=[
            '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            '--disable-blink-features=AutomationControlled'
        ]
    )
    page = browser.new_page()
    page.goto(url)
    
    # Fixed wait for JS to load (30s - adjust if needed)
    page.wait_for_timeout(30000)
    
    # Check if the element exists
    sentiment_locator = page.locator('.sentiment-panel__text')
    if sentiment_locator.count() == 0:
        raise ValueError("Sentiment element not found after wait. Check selector, site changes, or increase wait time.")
    
    # Extract clean text from the specific element (strips HTML tags)
    sentiment_text = sentiment_locator.inner_text()
    
    browser.close()

# Extract the long percentage using regex on clean text (handles bold/strong tags implicitly via inner_text)
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
