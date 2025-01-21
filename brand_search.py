from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Read data from input file
data = pd.read_csv(r'C:\Users\cmonis\Desktop\input_file_goo.txt', delimiter='\t')
brands = data["Brand"]

# Initialize Chrome WebDriver
driver = webdriver.Chrome()
url = "https://www.google.com/"
driver.get(url)

# Open the output file for writing
with open('brands1.txt', 'a', encoding='utf-8') as outfile:
    outfile.write("brands\turls\tsitemaps\n")

    try:
        for brand in brands:
            try:
                # Wait for the search input field to be visible and clickable
                search_input = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.NAME, "q"))
                )

                # Clear the search input field, enter the brand name, and submit the search
                search_input.clear()
                search_input.send_keys(brand)
                search_input.send_keys(Keys.RETURN)

                # Wait for the search results to be visible
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div#search"))
                )

                # Get all URLs from the specified node (example XPath used)
                urls = driver.find_elements(By.XPATH, "//div[@id='search']//a/@href")

                for url in urls:
                    if url:
                        sitemap_url = url + "sitemap.xml"
                        print(f"{brand}, {url}, {sitemap_url}")
                        outfile.write(f"{brand}\t{url}\t{sitemap_url}\n")

            except Exception as e:
                print(f"Error processing {brand}: {str(e)}")

    finally:
        # Close the browser window
        driver.quit()
