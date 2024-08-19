from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

def wait_for_element(driver, by, value, timeout=10):
    WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))

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
    part_number = part_number_elem.text.strip().replace('Mfg. Part Number: ', '') if part_number_elem else "Part number not found"

    # Extract key features (dynamic content)
    key_features = []
    key_features_elems = soup.select('div.no-opacity.full-opacity .typo-body p')
    for elem in key_features_elems:
        key_features.append(elem.text.strip())

    # Format key features as HTML list
    key_features_html = "<ul>" + "".join(f"<li>{feature}</li>" for feature in key_features) + "</ul>"

    # Extract specs
    specs = {}
    specs_elems = soup.select('div[id^="ra-catalog-accordion-"] li.content-secondary')
    for elem in specs_elems:
        key = elem.select_one('.content-primary').text.strip().replace(':', '')
        value = elem.text.replace(key + ':', '').strip()
        specs[key] = value

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
            wait_for_element(driver, By.CSS_SELECTOR, 'a.ra-product-card__top')  # Wait for the product links to be present

            # Allow some extra time for content to load
            time.sleep(2)

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            # Ensure we capture the correct product links
            links = soup.select('a.ra-product-card__top')
            if not links:
                links = soup.select('div.product-item a')
            if not links:
                links = soup.select('div.item-box a')

            unique_links = set()
            for link in links:
                product_url = link.get('href')
                if product_url:
                    if not product_url.startswith('http'):
                        product_url = 'https://rackattack.com' + product_url
                    if product_url not in unique_links:
                        unique_links.add(product_url)
                        print(f"Scraping product: {product_url}")
                        product_info = scrape_product_page(driver, product_url)
                        all_products.append(product_info)
                        time.sleep(1)  # Delay between product page requests

            # Allow some time before moving to the next page
            time.sleep(2)

    finally:
        driver.quit()

    return all_products

# Run the scraper
product_details = scrape_all_pages()

# Print the results in <ul><li></li></ul> format
print(f"Total products found: {len(product_details)}")
for product in product_details:
    print("\nTitle:", product['title'])
    print("Overview:", product['overview'])
    print("Part Number:", product['part_number'])
    print("Key Features (HTML):", product['key_features_html'])
    print("Specs:", product['specs'])
    print("-" * 50)
