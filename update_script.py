import requests
from bs4 import BeautifulSoup
import csv
import os
from datetime import datetime
import zoneinfo  # Built-in for timezone handling
import re

# URL to scrape
url = 'https://www.ig.com/en/indices/markets-indices/us-tech-100'

# Fetch page content
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Extract the long percentage using regex on page text (robust to HTML changes)
page_text = soup.get_text()
match = re.search(r'(\d+)% of client accounts are long on this market', page_text)
if match:
    long_percentage = int(match.group(1))  # Extract number as int
else:
    raise ValueError("Could not find long percentage on the page. Check site structure.")

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
