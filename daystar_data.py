import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import time
from openpyxl import Workbook

# Define the folder and excel file paths
image_folder = r"C:\Users\YMuzhchinina\GMCFeed\popularityFeeds\images"
excel_file = r"C:\Users\YMuzhchinina\GMCFeed\popularityFeeds\products.xlsx"


def crawl_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    product_links = []

    # Find all 'a' tags that are likely to be product links
    for a_tag in soup.find_all('a', class_=lambda x: x and 'product photo product-item-photo' in x):
        if 'href' in a_tag.attrs:
            product_links.append(a_tag['href'])

    return product_links


def extract_product_info(product_url):
    response = requests.get(product_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract product title
    title_tag = soup.find('h1', class_='text-content page-title title-font')
    title = None
    if title_tag:
        title_span = title_tag.find('span', itemprop='name')
        if title_span:
            title = title_span.text.strip()

    # Extract part number
    part_number_tag = soup.find('div', class_='mb-4 leading-relaxed product-description prose')
    part_number = None
    if part_number_tag:
        for strong_tag in part_number_tag.find_all('strong'):
            if 'Part Number' in strong_tag.text:
                part_number = strong_tag.next_sibling.strip()
                part_number = "DAY" + part_number

    # Extract vehicle fitment
    fitments = []
    fitment_section = soup.find('section', id='vehicle')
    if fitment_section:
        fitment_list = fitment_section.find('ul',
                                            class_='list-inside list-disc w-full columns-1 gap-4 pb-4 text-sm sm:columns-2 md:columns-3 lg:columns-4')
        if fitment_list:
            for li in fitment_list.find_all('li', class_='text-base'):
                fitments.append(li.text.strip())

    # Extract description
    description = None
    description_section = soup.find('section', id='description')
    if description_section:
        description_div = description_section.find('div', class_='prose')
        if description_div:
            paragraphs = description_div.find_all('p')
            description = ''.join([str(p) for p in paragraphs])

    # Extract features
    features = None
    features_section = soup.find('section', id='product_features')
    if features_section:
        features_div = features_section.find('div', id='product-features')
        if features_div:
            ul = features_div.find('ul')
            if ul:
                features = str(ul)

    # Extract image URL and download the image
    image_url = None

    image_tag = soup.find('img', itemprop='image')
    print(f"Image tag found: {image_tag}")
    if image_tag and 'src' in image_tag.attrs:
        image_url = image_tag['src']
        print(f"Image URL: {image_url}")
        print(f"Part number: {part_number}")
        if part_number:
            download_image(image_url, part_number.lower())
        else:
            print("Part number is None, skipping image download")
    else:
        print("Image tag not found or doesn't have 'src' attribute")

    return title, part_number, fitments, description, features


def download_image(img_url, part_number):
    print(f"Attempting to download image from {img_url} for part number {part_number}")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(img_url, headers=headers)
    if response.status_code == 200:
        os.makedirs(image_folder, exist_ok=True)
        img_name = f"{part_number}-001.jpg"
        img_path = os.path.join(image_folder, img_name)
        with open(img_path, 'wb') as f:
            f.write(response.content)
        print(f"Image saved as {img_path}")
    else:
        print(f"Failed to download image from {img_url}")


base_url = "https://dpioffroad.com/brands/daystar?brand=285&p={}&product_list_order=bestsellers"
all_product_links = []

for page_num in range(1, 15):  # Pages 1 to 14
    url = base_url.format(page_num)
    print(f"Crawling page {page_num}...")
    page_links = crawl_page(url)
    all_product_links.extend(page_links)
    time.sleep(2)  # Add a 2-second delay between requests

# Extract and print product titles, part numbers, fitments, descriptions, and features
product_info_list = []
all_fitments = []
for link in all_product_links:
    title, part_number, fitments, description, features = extract_product_info(link)
    if title and part_number:
        product_info_list.append({
            "Title": title,
            "Part Number": part_number,
            "Fitments": ', '.join(fitments),
            "Description": description,
            "Features": features
        })
        print(f"Title: {title}")
        print(f"Part Number: {part_number}")
        print(f"Fitments: {fitments}")
        print(f"Description: {description}")
        print(f"Features: {features}")
        all_fitments.extend(fitments)
    else:
        print(f"Info not found for link: {link}")
    time.sleep(1)  # Add a 1-second delay between requests

print(f"\nTotal products found: {len(product_info_list)}")

# Print all fitments
print("\nVehicle Fitments:")
for fitment in all_fitments:
    print(fitment)

# Save product information to an Excel file using openpyxl
wb = Workbook()
ws = wb.active
ws.title = "Products"

# Write header row
ws.append(["Title", "Part Number", "Fitments", "Description", "Features"])

# Write product info
for product in product_info_list:
    ws.append([
        product["Title"],
        product["Part Number"],
        product["Fitments"],
        product["Description"],
        product["Features"]
    ])

wb.save(excel_file)
print(f"Product information saved to {excel_file}")
