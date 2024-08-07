import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
import time


def get_product_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.select('a.grid-product__link')
    return [f"https://attica4x4.com{link['href']}" for link in links]


def extract_product_info(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch the product page. Status code: {response.status_code}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    sku_element = soup.find('p', class_='product-single__sku')
    sku = sku_element.text.strip() if sku_element else "SKU not found"

    title = soup.find('h1', class_='product-single__title')
    title = title.text.strip() if title else "Title not found"

    return {sku: {'title': title, 'url': url}}


base_url = 'https://attica4x4.com/collections/shop?page={}'
all_product_info = {}

for page in range(1, 4):  # 3 pages total
    url = base_url.format(page)
    product_links = get_product_links(url)

    for link in product_links:
        info = extract_product_info(link)
        if info:
            all_product_info.update(info)
        time.sleep(1)  # Add a 1-second delay between requests

    print(f"Processed page {page}, total products found: {len(all_product_info)}")
    time.sleep(2)  # Add a 2-second delay between pages

# Create a new workbook and select the active sheet
wb = Workbook()
ws = wb.active

# Write headers
ws.append(["SKU", "Title", "URL"])

# Write data to the Excel sheet
for sku, info in all_product_info.items():
    ws.append([sku, info['title'], info['url']])

# Save the Excel file
excel_file = "attica_products.xlsx"
wb.save(excel_file)

print(f"Successfully saved {len(all_product_info)} products to {excel_file}")