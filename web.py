# Import necessary libraries
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# Function to scroll the page
def scroll_page(driver, times):
    for _ in range(times):
        driver.execute_script("window.scrollBy(0, 350)")
        time.sleep(1)

# Function to extract and process reviews
def extract_reviews(review_elements):
    reviews = []
    try:
        for i in range(5):
            reviews.append(review_elements[i].text.split(sep="\n"))
            reviews[i] = reviews[i][0:-2]
    except IndexError:
        pass

    cleaned_reviews = [' '.join(review) for review in reviews]
    return cleaned_reviews

# Function to extract and process names
def extract_names(name_elements):
    names = []
    for i in range(5):
        name_i = name_elements[i].find_element(By.TAG_NAME, "span").text[3:]
        names.append(name_i)
    return names

# Main function for scraping reviews
def scrape_reviews(product_url):
    # Set up Chrome webdriver
    DRIVER_PATH = r"C:/Users/HP/Downloads/chromedriver (1).exe"
    options = Options()
    options.add_argument("incognito")
    driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=options)
    driver.get(product_url)

    # Scroll to load more reviews
    time.sleep(10)
    scroll_page(driver, 5)

    # Initialize lists to store data
    final_review = []
    final_name = []

    # Loop through three pages of reviews
    for _ in range(3):
        name_elements = driver.find_elements(By.CLASS_NAME, "middle")
        review_elements = driver.find_elements(By.CLASS_NAME, "item-content")

        final_name.extend(extract_names(name_elements))
        final_review.extend(extract_reviews(review_elements))

        try:
            driver.find_element(By.XPATH, '/html/body/div[4]/div/div[9]/div[1]/div[2]/div/div/div/div[3]/div[2]/div/button[2]').click()
        except NoSuchElementException:
            driver.find_element(By.XPATH, '/html/body/div[4]/div/div[9]/div[1]/div[2]/div/div/div/div[3]/div[2]/div/button[2]').click()
        time.sleep(3)
        scroll_page(driver, 5)

    # Create DataFrame
    df = pd.DataFrame({"Name": final_name, "Reviews": final_review})

    # Clean the Reviews and apply Vader Sentiment (Part b of the question)
    # Add your code here...

    # Close the webdriver
    driver.quit()

    return df

# Example usage
product_url = 'https://www.daraz.pk/products/i12_air-buds-earphones-with-charging-case-i232480276-s1451845403.html?spm=a2a0e.home.flashSale.2.35e34937sddCy5&search=1&mp=1&c=fs'
reviews_df = scrape_reviews(product_url)
print(reviews_df)
