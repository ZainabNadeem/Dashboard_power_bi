import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_page(page_number):
    url = f"https://www.ebay.com/sch/i.html?_dkr=1&iconV2Request=true&_blrs=recall_filtering&_ssn=partsouq&store_name=partsouq&_oac=1&_ipg=240&LH_Sold=1&LH_Complete=1&_pgn={page_number}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred while fetching page {page_number}: {e}")
    except Exception as e:
        print(f"An error occurred while fetching page {page_number}: {e}")
    return None

def parse_page(html):
    if html is None:
        return []

    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='s-item__info')

    data = []
    for item in items:
        title = item.find('h3', class_='s-item__title')
        title = title.get_text(strip=True) if title else None

        price = item.find('span', class_='s-item__price')
        price = price.get_text(strip=True) if price else None

        item_url = item.find('a', class_='s-item__link')
        item_url = item_url['href'] if item_url else None

        # Ensure URL is complete
        if item_url and not item_url.startswith('http'):
            item_url = f"https://www.ebay.com{item_url}"

        # Extract additional details from item_url page
        shipment = seller = date_sold = time_sold = None

        if item_url:
            item_html = fetch_item_details(item_url)
            if item_html:
                item_soup = BeautifulSoup(item_html, 'html.parser')
                
                shipment = item_soup.find('span', class_='vi-acc-del-range')
                shipment = shipment.get_text(strip=True) if shipment else None
                
                seller = item_soup.find('span', class_='mbg-nw')
                seller = seller.get_text(strip=True) if seller else None

                date_sold = item_soup.find('span', class_='vi-tm-left')
                date_sold = date_sold.get_text(strip=True) if date_sold else None

                time_sold = item_soup.find('span', class_='vi-tm-right')
                time_sold = time_sold.get_text(strip=True) if time_sold else None

        data.append({
            'Product Name': title,
            'Price': price,
            'URL': item_url,
            'Shipment': shipment,
            'Seller': seller,
            'Date Sold': date_sold,
            'Time Sold': time_sold
        })

    return data

def fetch_item_details(item_url):
    try:
        item_response = requests.get(item_url)
        item_response.raise_for_status()
        return item_response.text
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred while fetching item details from {item_url}: {e}")
    except Exception as e:
        print(f"An error occurred while fetching item details from {item_url}: {e}")
    return None

def main():
    all_data = []
    for page_number in range(1, 21):  # Adjust range as needed to cover all pages
        print(f"Fetching page {page_number}...")
        html = fetch_page(page_number)
        page_data = parse_page(html)
        if page_data:
            all_data.extend(page_data)
        else:
            print(f"No data found on page {page_number}. Ending scraping.")
            break  # Stop if no data is found (end of pages)

    df = pd.DataFrame(all_data)
    df.to_csv("partsouq_products.csv", index=False)
    print("Data saved to partsouq_products.csv")

if __name__ == "__main__":
    main()
