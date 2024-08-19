from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

base_url = "https://www.4wheelparts.com/b/addictive-desert-designs/_/N-1z0dws3"
part_numbers = []

for i in range(0, 20):
    page_number = i * 12
    url = f"{base_url}?SNo={page_number}&SNrpp=24&SNs=sku.reviews.average.rating|1||sku.displayorder|0&skuSelectedTab=true"
    driver.get(url)

    # Use WebDriverWait to ensure the page is fully loaded
    # ...

    # Find part numbers based on the actual HTML structure
    part_elements = driver.find_elements_by_xpath('//a[contains(text(), "Part Number")]')
    for elem in part_elements:
        text = elem.text
        try:
            part_number = text.split(': ')[1]
            part_numbers.append(part_number)
        except IndexError:
            print(f"Error extracting part number from: {text}")

driver.quit()
print(part_numbers)
