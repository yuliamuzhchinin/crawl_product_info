import requests
from bs4 import BeautifulSoup
import openpyxl


def process_product_page(url):
    response = requests.get(url)

    # Handle potential encoding issues
    response.encoding = response.apparent_encoding

    # Try using 'lxml' parser instead of 'html.parser'
    try:
        soup = BeautifulSoup(response.text, 'lxml')
    except Exception as e:
        print(f"Failed to parse {url} with error: {e}")
        return None

    # Find the product title
    product_title = ''
    title_div = soup.find('div', class_='product__title')
    if title_div:
        h1_tag = title_div.find('h1')
        if h1_tag:
            product_title = h1_tag.text.strip()

    # Find the SKU number and prepend 'WNJ'
    sku = ''
    sku_p = soup.find('p', class_='product__sku no-js-hidden')
    if sku_p:
        sku_span = sku_p.find('span', class_='visually-hidden')
        if sku_span:
            sku = "WNJ" + sku_p.text.replace(sku_span.text, '').strip()

    # Find the specific div
    product_div = soup.find('div', class_='product__description rte quick-add-hidden')

    if product_div:
        # Extract fitment list
        fitment_list = []
        fitment_ul = product_div.find('ul')
        if fitment_ul:
            fitment_list = [li.text.strip() for li in fitment_ul.find_all('li')]

        # Extract description paragraph with <p> tag
        description_html = ''
        all_p = product_div.find_all('p')
        if len(all_p) > 1:  # Ensure there's more than one <p> tag
            description_html = str(all_p[1])  # Get the second <p> tag as a string, preserving HTML

        # Extract features list with HTML
        features_html = ''
        all_ul = product_div.find_all('ul')
        if all_ul:
            features_ul = all_ul[-1]  # Assuming the last ul is the features list
            features_html = str(features_ul)

        return {
            'title': product_title,
            'sku': sku,
            'fitment': ', '.join(fitment_list),  # Joining fitment list as a single string for Excel
            'description': description_html,
            'features': features_html
        }
    else:
        return None


# Initialize a workbook and select the active worksheet
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Product Data"

# Set up the headers in the Excel sheet
headers = ["Title", "SKU", "Fitment", "Description", "Features"]
ws.append(headers)

# URL of the sitemap
sitemap_url = "https://winjetinc.com/sitemap_products_1.xml?from=8693017182529&to=9679377924417"

# Fetch the content of the sitemap
response = requests.get(sitemap_url)
xml_content = response.text

# Parse the XML content with BeautifulSoup
soup = BeautifulSoup(xml_content, 'xml')

# Find all <loc> tags and extract their text (URLs)
loc_tags = soup.find_all('loc')

# Process each product page and save data to the Excel sheet
for loc in loc_tags:
    product_url = loc.text
    print("processing page", product_url)
    result = process_product_page(product_url)
    if result:
        ws.append([
            result['title'],
            result['sku'],
            result['fitment'],
            result['description'],
            result['features']
        ])

# Save the workbook
wb.save("Product_Data.xlsx")
