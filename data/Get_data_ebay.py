import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_ebay_data(page_number):
    url = f"https://www.ebay.com/sch/i.html?_dkr=1&iconV2Request=true&_blrs=recall_filtering&_ssn=tema4x4&store_name=tema4x4&_oac=1&_ipg=240&_pgn={page_number}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    items = []
    for item in soup.find_all('div', class_='s-item__info'):
        title = item.find('h3', class_='s-item__title')
        price = item.find('span', class_='s-item__price')
        shipping = item.find('span', class_='s-item__shipping')
        
        if title and price:
            items.append({
                'Product Name': title.text,
                'Price': price.text,
                'Shipping': shipping.text if shipping else 'N/A'
            })
    
    # Print the items fetched from this page for debugging purposes
    print(f"Page {page_number}: Found {len(items)} items")
    for item in items:
        print(item)
    
    return items

all_items = []
for page in range(1, 6):  # Fetch first 5 pages
    all_items.extend(fetch_ebay_data(page))

# Check if any items were fetched
if all_items:
    df = pd.DataFrame(all_items)
    df.to_excel('ebay_products.xlsx', index=False)
    print("Data has been saved to ebay_productts.xlsx")
else:
    print("No items were fetched from eBay.")
