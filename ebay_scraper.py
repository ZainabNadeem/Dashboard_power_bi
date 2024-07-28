import requests
import pandas as pd

# Define the URL
url = "https://www.ebay.com/sh/research?marketplace=EBAY-US&keywords=Genuine+toyota&dayRange=30&endDate=1721871409135&startDate=1719279409135&categoryId=0&sellerCountry=SellerLocation%3A%3A%3AAE&excludedListings=375239379327&offset=0&limit=50&sorting=-itemssold&tabName=SOLD&tz=Africa%2FNairobi"

# Make a request to the URL
response = requests.get(url)
data = response.json()

# Extract relevant information
items = data.get('data', {}).get('searchResults', {}).get('items', [])

# Create a DataFrame from the extracted data
df = pd.DataFrame(items)

# Save DataFrame to CSV
csv_file_path = "ebay_data.csv"
df.to_csv(csv_file_path, index=False)

print(f"Data saved to {csv_file_path}")
