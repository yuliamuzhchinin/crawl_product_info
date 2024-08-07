import requests
from bs4 import BeautifulSoup
import re
from openpyxl import Workbook


def get_product_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.select('a.productitem--image-link')
    return [f"https://www.oraclelights.com{link['href']}" for link in links]


def extract_numbers(text):
    numbers = re.findall(r'\b\d+(?:-\d+)*\b', text)
    return numbers


def extract_product_info(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch the product page. Status code: {response.status_code}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    title = soup.find('h1', class_='product-title')
    title = title.text.strip() if title else "Title not found"

    # Extract part numbers from the table
    part_numbers = []
    td_tags = soup.find_all('td')
    for td_tag in td_tags:
        numbers = extract_numbers(td_tag.text.strip())
        part_numbers.extend(numbers)

    # Remove duplicates and add "ORA" prefix
    unique_part_numbers = [f"ORA{number}" for number in set(part_numbers)]

    # Create a dictionary with part numbers as keys and titles as values
    product_info = {part_number: {'title': title, 'url': url} for part_number in unique_part_numbers}

    return product_info


base_url = 'https://www.oraclelights.com/collections/popular-products?page={}&grid_list=grid-view'
all_product_info = {}

for page in range(1, 64):  # 63 pages total
    url = base_url.format(page)
    product_links = get_product_links(url)

    for link in product_links:
        info = extract_product_info(link)
        if info:
            all_product_info.update(info)

    print(f"Processed page {page}, total products found: {len(all_product_info)}")

# Create a new workbook and select the active sheet
wb = Workbook()
ws = wb.active

# Write headers
ws.append(["SKU", "Title", "URL"])

# Write data to the Excel sheet
for sku, info in all_product_info.items():
    ws.append([sku, info['title'], info['url']])

# Save the Excel file
excel_file = "oracle_products.xlsx"
wb.save(excel_file)

print(f"Successfully saved {len(all_product_info)} products to {excel_file}")