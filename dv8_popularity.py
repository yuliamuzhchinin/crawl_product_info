from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time


def crawl_pages(base_url, total_pages):
    all_links = []

    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode

    # Initialize the WebDriver
    driver = webdriver.Chrome(options=chrome_options)

    try:
        for page in range(1, total_pages + 1):
            url = f"{base_url}?sort=Bestselling&page={page}"
            driver.get(url)

            # Wait for the elements to be present
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[data-qatgt="productImage"]'))
            )

            # Find all elements
            elements = driver.find_elements(By.CSS_SELECTOR, 'a[data-qatgt="productImage"]')

            # Extract href attributes
            page_links = [element.get_attribute('href') for element in elements]
            print(all_links)
            all_links.extend(page_links)
            print(f"Processed page {page}/{total_pages}")

            # Add a small delay to avoid overwhelming the server
            time.sleep(2)

    finally:
        driver.quit()

    return all_links


# Usage
base_url = "https://www.extremeterrain.com/dv8-off-road-parts.html/f/"
total_pages = 23

result = crawl_pages(base_url, total_pages)

# Print the results
print(f"\nTotal links found: {len(result)}")
print("Links:")
for link in result:
    print(link)