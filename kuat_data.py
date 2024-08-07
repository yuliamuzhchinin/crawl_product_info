from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
from openpyxl import Workbook
import os


def scrape_product_page(driver, url):
    driver.get(url)
    time.sleep(3)  # Adjust sleep time if necessary

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Extract title
    title_elem = soup.select_one('div.product-name.typo-heading4')
    title = title_elem.text.strip() if title_elem else "Title not found"

    # Extract overview
    overview_elem = soup.select_one('div.ra-typo-wrapper.text-block4')
    overview = str(overview_elem.find('p')) if overview_elem else "<p>Overview not found</p>"

    # Extract manufacturer part number
    part_number_elem = soup.select_one('div[id^="ra-catalog-accordion-"] li:-soup-contains("Mfg. Part Number:")')
    part_number = part_number_elem.text.strip().replace('Mfg. Part Number: ',
                                                        '') if part_number_elem else "Part number not found"

    # Extract key features (dynamic content)
    key_features = []
    key_features_elems = soup.select('div.no-opacity.full-opacity .typo-body p')
    for elem in key_features_elems:
        key_features.append(elem.text.strip())

    # Format key features as HTML list
    key_features_html = "<ul>" + "".join(f"<li>{feature}</li>" for feature in key_features) + "</ul>"

    # Extract specs
    specs = []
    specs_elems = soup.select('div[id^="ra-catalog-accordion-"] li.content-secondary')
    for elem in specs_elems:
        key_elem = elem.select_one('.content-primary')
        if key_elem:
            key = key_elem.text.strip().replace(':', '')
            value = elem.text.replace(key_elem.text + ':', '').strip()
            specs.append((key, value))

    return {
        "title": title,
        "overview": overview,
        "part_number": part_number,
        "key_features_html": key_features_html,
        "specs": specs
    }


def scrape_all_pages():
    base_url = "https://rackattack.com/kuat"
    all_products = []

    # Set up Selenium WebDriver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    try:
        for page in range(1, 11):  # 10 pages
            url = f"{base_url}?pagenumber={page}&orderby=0&pagesize=0"
            print(f"Scraping page {page}...")

            driver.get(url)
            time.sleep(3)  # Adjust sleep time if necessary

            soup = BeautifulSoup(driver.page_source, 'html.parser')

            links = soup.select('a.ra-product-card__top')
            if not links:
                links = soup.select('div.product-item a')
            if not links:
                links = soup.select('div.item-box a')

            for link in links:
                product_url = link.get('href')
                if product_url:
                    if not product_url.startswith('http'):
                        product_url = 'https://rackattack.com' + product_url
                    print(f"Scraping product: {product_url}")
                    product_info = scrape_product_page(driver, product_url)
                    all_products.append(product_info)
                    time.sleep(1)  # Delay between product page requests

            time.sleep(2)  # Delay between page requests

    finally:
        driver.quit()

    return all_products


def save_to_excel(data, filename='kuat_product_data.xlsx'):
    wb = Workbook()
    ws = wb.active
    ws.title = 'Products'

    # Write header for product details
    ws.append(['Title', 'Overview', 'Part Number', 'Key Features (HTML)', 'Name', 'Value'])

    # Write data
    for product in data:
        title = product['title']
        overview = product['overview']
        part_number = product['part_number']
        key_features_html = product['key_features_html']

        if product['specs']:
            for name, value in product['specs']:
                ws.append([title, overview, part_number, key_features_html, name, value])
        else:
            # If there are no specs, still create a row with empty 'Name' and 'Value'
            ws.append([title, overview, "KUA"+part_number, key_features_html, '', ''])

    # Save the workbook to the same directory as the script
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, filename)
        wb.save(file_path)
        print(f"Data successfully saved to {file_path}")
    except Exception as e:
        print(f"An error occurred while saving to Excel: {e}")


# Run the scraper and save results
product_details = scrape_all_pages()
print(f"Total products found: {len(product_details)}")
save_to_excel(product_details)
