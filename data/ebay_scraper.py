import requests
from bs4 import BeautifulSoup
import pandas as pd

# Define the URL
url = "https://www.ebay.com/sch/i.html?_dkr=1&iconV2Request=true&_blrs=recall_filtering&_ssn=partsouq&store_name=partsouq&_oac=1&_ipg=240&LH_Sold=1&LH_Complete=1&_pgn=2"

try:
    # Make a request to the URL
    response = requests.get(url)
    response.raise_for_status()  # Check if the request was successful

    # Check if the response content is as expected
    if "html" in response.headers["Content-Type"]:
        print("Successfully fetched the HTML content.")

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'lxml')

        # Find the relevant data (this may need adjustment based on actual HTML structure)
        items = soup.find_all('div', class_='s-item__info')

        if not items:
            print("No items found. The structure might have changed.")
        else:
            # Extract data into a list of dictionaries
            data = []
            for item in items:
                title = item.find('h3', class_='s-item__title').get_text(strip=True) if item.find('h3', class_='s-item__title') else None
                price = item.find('span', class_='s-item__price').get_text(strip=True) if item.find('span', class_='s-item__price') else None
                data.append({'Product Name': title, 'Price': price})

            # Create a DataFrame from the extracted data
            df = pd.DataFrame(data)

            # Save DataFrame to CSV
            csv_file_path = "ebay_data.csv"
            df.to_csv(csv_file_path, index=False)

            print(f"Data saved to {csv_file_path}")
    else:
        print("The content fetched is not HTML. Please check the URL and try again.")
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
