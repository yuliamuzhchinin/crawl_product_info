from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def get_part_numbers(driver, url):
    driver.get(url)

    # Wait for the page to load
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "ng-binding"))
    )

    # Extract part numbers
    part_numbers = []
    elements = driver.find_elements(By.XPATH, "//span[contains(@ng-if, '!product.variants && product.mpn[0]')]")
    for element in elements:
        part_number = element.text.replace('PART# ', '').strip()
        part_numbers.append(part_number)

    return part_numbers


def crawl_pages(base_url, total_pages):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode

    service = Service('path/to/chromedriver')  # Replace with your chromedriver path
    driver = webdriver.Chrome(service=service, options=chrome_options)

    all_part_numbers = []

    try:
        for page in range(1, total_pages + 1):
            url = base_url.format(page)
            print(f"Crawling page {page}...")
            part_numbers = get_part_numbers(driver, url)
            all_part_numbers.extend(part_numbers)

            # Add a delay to avoid overwhelming the server
            time.sleep(2)

    finally:
        driver.quit()

    return all_part_numbers


# Main execution
base_url = "https://www.xtremediesel.com/xdp-manufacturers/sb-filters?page={}#/showFilters"
total_pages = 15

part_numbers = crawl_pages(base_url, total_pages)

print("All part numbers:")
print(part_numbers)
print(f"Total part numbers found: {len(part_numbers)}")