from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup  # Import BeautifulSoup module
import pandas as pd
import time

# Rest of your code...


# URL of the target webpage
url = "https://kaspi.kz/shop/c/notebooks/?q=%3AavailableInZones%3AMagnum_ZONE1%3Acategory%3ANotebooks%3ANotebooks*Internal%20RAM%3A32%20%D0%93%D0%B1%3ANotebooks*Internal%20RAM%3A64%20%D0%93%D0%B1&sort=relevance&sc="

# Specify the path to your Chrome WebDriver executable
driver_path = r"C:\Users\Мадияр\Desktop\chromedriver.exe"

# Create an instance of ChromeOptions
chrome_options = Options()

# Set the path to the driver in ChromeOptions
chrome_options.add_argument(f"webdriver.chrome.driver={driver_path}")

# Create a Chrome WebDriver instance with ChromeOptions
driver = webdriver.Chrome(options=chrome_options)

# Open the webpage
driver.get(url)

# Initialize a list to store the notebook data as dictionaries
notebook_data = []

while True:
    # Wait for the page to load (you may need to adjust the waiting time)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'item-card__name')))

    # Get the page source after JavaScript execution
    html = driver.page_source

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Find all elements with the class 'item-card'
    notebook_cards = soup.find_all(class_='item-card')

    for card in notebook_cards:
        # Extract relevant information from each card
        notebook_name = card.find(class_='item-card__name').text.strip()
        notebook_price = card.find(class_='item-card__prices-price').text.strip()
        notebook_link = card.find('a', class_='item-card__name-link')['href']

        # Open the link to the notebook
        driver.get(notebook_link)

        # Wait for the 'Характеристики' tab to become clickable
        characteristics_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//li[@data-tab='specifications' and contains(text(), 'Характеристики')]"))
        )

        # Click on the 'Характеристики' tab
        characteristics_tab.click()

        # Wait for the characteristics to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'specifications-list')))

        # Find all 'li' elements with class 'specifications-list__spec-term-text'
        specifications_terms = driver.find_elements(By.CLASS_NAME, 'specifications-list__spec-term-text')

        # Find all 'dd' elements with class 'specifications-list__spec-definition'
        specifications_definitions = driver.find_elements(By.CLASS_NAME, 'specifications-list__spec-definition')

        # Initialize max_memory variable
        max_memory = None

        # Iterate over characteristics to find 'Максимальный размер памяти' and its value
        for term, definition in zip(specifications_terms, specifications_definitions):
            if term.text.strip() == 'Максимальный размер памяти':
                max_memory_text = definition.text.strip()
                if 'Гб' in max_memory_text:
                    max_memory_value = float(max_memory_text.split()[0])
                    if max_memory_value >= 32:
                        max_memory = max_memory_text

        if max_memory:
            # Append the notebook data as a dictionary to the list
            notebook_data.append({
                'Max Memory': max_memory,
                'Name': notebook_name,
                'Price': notebook_price,
                'Link': notebook_link
            })

        # Go back to the previous page
        driver.back()

    try:
        # Find the 'Следующая' button and click it if available
        next_button = driver.find_element(By.XPATH, "//li[@class='pagination__el' and contains(text(), 'Следующая')]")
        if 'pagination__el--disabled' not in next_button.get_attribute("class"):
            next_button.click()
        else:
            break  # If the next page is disabled, exit the loop
    except:
        break  # If the 'Следующая' button is not found, exit the loop

# Close the WebDriver after use
driver.quit()

# Create a DataFrame from the collected data
df = pd.DataFrame(notebook_data)

# Specify the path where you want to save the CSV file
csv_path = r'C:\Users\Мадияр\Desktop\notebooks30.csv'

# Save the DataFrame to a CSV file
df.to_csv(csv_path, index=False, encoding='utf-8-sig')