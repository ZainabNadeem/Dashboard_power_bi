import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_page(page_number):
    url = f"https://www.ebay.com/sch/Tema4x4/m.html?item=150849563082&_ssn=tema4x4&_pgn={page_number}&rt=nc"
    response = requests.get(url)
    response.raise_for_status()  # Ensure the request was successful
    return response.text

def parse_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='s-item__info')

    data = []
    for item in items:
        title = item.find('h3', class_='s-item__title').get_text(strip=True) if item.find('h3', class_='s-item__title') else None
        price = item.find('span', class_='s-item__price').get_text(strip=True) if item.find('span', class_='s-item__price') else None
        item_url = item.find('a', class_='s-item__link')['href'] if item.find('a', class_='s-item__link') else None
        data.append({'Product Name': title, 'Price': price, 'URL': item_url})

    return data

def main():
    all_data = []
    for page_number in range(1, 21):  # Adjust range as needed to cover all pages
        print(f"Fetching page {page_number}...")
        html = fetch_page(page_number)
        page_data = parse_page(html)
        if not page_data:
            break  # Stop if no data is found (end of pages)
        all_data.extend(page_data)

    df = pd.DataFrame(all_data)
    df.to_csv("tema4x4_products.csv", index=False)
    print("Data saved to tema4x4_products.csv")

if __name__ == "__main__":
    main()
