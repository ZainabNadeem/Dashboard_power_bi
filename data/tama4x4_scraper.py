import requests
from bs4 import BeautifulSoup

def fetch_store_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred while fetching the store page: {e}")
    except Exception as e:
        print(f"An error occurred while fetching the store page: {e}")
    return None

def parse_store_page(html):
    if html is None:
        return []

    soup = BeautifulSoup(html, 'html.parser')
    
    # Extract product names
    items = soup.find_all('div', class_='s-item__info')
    product_names = []

    for item in items:
        title = item.find('h3', class_='s-item__title')
        if title:
            product_names.append(title.get_text(strip=True))

    return product_names

def main():
    # URL for the PartSouq eBay store page
    url = 'https://www.ebay.com/sch/i.html?_dkr=1&iconV2Request=true&_blrs=recall_filtering&_ssn=partsouq&store_name=partsouq&_oac=1&_ipg=240&LH_Sold=1&LH_Complete=1'
    html = fetch_store_page(url)
    product_names = parse_store_page(html)
    
    if product_names:
        print("Product Names:")
        for name in product_names:
            print(name)
    else:
        print("No product names found.")

if __name__ == "__main__":
    main()
