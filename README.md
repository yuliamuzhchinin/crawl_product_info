
# Product Data Scraper

## Overview

This project is a Python-based web scraping tool that extracts product data from various websites using Beautiful Soup and Selenium. The goal of the project was to gather relevant product information, format it uniformly, and export the data into an Excel file for easy analysis and use.

## Features

- **Web Scraping**: Utilizes Beautiful Soup and Selenium to crawl multiple websites, extracting product details such as name, price, description, and more.
- **Data Uniformity**: Processes and formats the extracted data into a consistent style across all sources.
- **Excel Export**: Compiles the formatted data into an Excel file for easy access and further analysis.

## Tech Stack

- **Python**: Core language used for scripting.
- **Beautiful Soup**: Library used for parsing HTML and XML documents.
- **Selenium**: Tool used for automating web browsers to scrape dynamic content.
- **Pandas**: Library used for data manipulation and exporting data to Excel.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/product-data-scraper.git
   cd product-data-scraper
   ```

2. Create a virtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Set up WebDriver**: Make sure you have the appropriate WebDriver installed for Selenium (e.g., ChromeDriver for Chrome). Download it and add it to your PATH.

2. **Configure the scraping targets**: Modify the `config.py` file to include the URLs of the websites you want to scrape and the relevant HTML tags/classes/IDs.

3. **Run the scraper**:

   ```bash
   python scraper.py
   ```

4. **Output**: The scraped and formatted data will be saved as an Excel file named `products_data.xlsx` in the project directory.

## Project Structure

- `scraper.py`: Main script to run the web scraping process.
- `config.py`: Configuration file to set up target URLs and HTML structures.
- `requirements.txt`: List of Python packages required for the project.
- `products_data.xlsx`: Output file containing the formatted product data.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

## Contributing

Contributions are welcome! Please open an issue or submit a pull request if you have any suggestions or improvements.

---

## Contact

For any questions or issues, please reach out to muzhchinin18@gmail.com.

