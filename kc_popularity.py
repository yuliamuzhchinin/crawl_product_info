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

    # Extract manufacturer part number
    part_number_elem = soup.select_one('div[id^="ra-catalog-accordion-"] li:-soup-contains("Mfg. Part Number:")')
    part_number = part_number_elem.text.strip().replace('Mfg. Part Number: ', '') if part_number_elem else "Part number not found"

    return {
        "part_number": "KCH"+part_number,
    }

def scrape_all_pages():
    base_url = "https://rackattack.com/kc-hilites"
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

def save_to_excel(products, filename="product_part_numbers.xlsx"):
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Part Numbers"

    # Add headers
    sheet.append(["Part Number"])

    # Add data
    for product in products:
        sheet.append([product["part_number"]])

    # Save the workbook
    workbook.save(filename)
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    products = scrape_all_pages()
    save_to_excel(products)
