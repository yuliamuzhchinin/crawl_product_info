import requests
from bs4 import BeautifulSoup
import time
from openpyxl import Workbook


def get_product_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    links = []
    for a in soup.find_all('a', class_='product photo product-item-photo'):
        links.append(a['href'])

    return links


def get_product_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    title_element = soup.find('div', class_='page-title-wrapper product')
    title = title_element.find('span', class_='base').text.strip() if title_element else 'N/A'

    sku_element = soup.find('div', class_='product attribute sku')
    sku = sku_element.find('h2', class_='value').text.strip() if sku_element else 'N/A'

    return {'title': title, 'sku': "RGD"+sku, 'url': url}


base_url = "https://www.rigidindustries.com/lights/product.html"
all_products = []

for page in range(1, 25):  # 24 pages in total
    url = f"{base_url}?p={page}&product_list_dir=asc&product_list_order=product_new"
    print(f"Crawling page {page}...")

    page_links = get_product_links(url)

    for link in page_links:
        print(f"Fetching product info from: {link}")
        product_info = get_product_info(link)
        all_products.append(product_info)
        time.sleep(1)  # Be polite and don't overwhelm the server

    time.sleep(2)  # Additional delay between pages

print(f"Total products collected: {len(all_products)}")

# Save the results to an Excel file
wb = Workbook()
ws = wb.active
ws.title = "Rigid Industries Products"

# Write headers
headers = ['Title', 'SKU', 'URL']
ws.append(headers)

# Write data
for product in all_products:
    ws.append([product['title'], product['sku'], product['url']])

# Save the workbook
excel_filename = 'rigid_industries_products.xlsx'
wb.save(excel_filename)

print(f"Data has been saved to {excel_filename}")