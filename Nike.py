from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd
import time

# Define the URL
url = "https://www.nike.com/ie/w/womens-shoes-5e1x6zy7ok"

# Set the path to the ChromeDriver
path = r'E:/Sneha/Web Scrapping/Chrome Driver/chromedriver-win64/chromedriver.exe'
service = Service(path)

# Initialize the WebDriver
driver = webdriver.Chrome(service=service)
driver.get(url)
time.sleep(4)
driver.maximize_window()

# Scroll the page to load all products
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Parse the page source with BeautifulSoup
soup = BeautifulSoup(driver.page_source, "lxml")

# Close the WebDriver
driver.quit()

# Initialize lists to store product details
product_names = []
product_colours = []
product_prices = []

# Locate the product containers
product_containers = soup.find_all("div", class_="product-card__body")

# Extract product details
for container in product_containers:
    # Product name
    name_tag = container.find("div", class_="product-card__titles")
    name = name_tag.text.strip() if name_tag else "N/A"
    product_names.append(name)

    # Colours
    colour_tag = container.find("div", class_="product-card__count-wrapper")
    colour = colour_tag.text.strip() if colour_tag else "N/A"
    product_colours.append(colour)

    # Prices
    price_tag = container.find("div", class_="product-card__price")
    price = price_tag.text.strip() if price_tag else "N/A"
    product_prices.append(price)

# Create a DataFrame
df = pd.DataFrame({
    "Product Name": product_names,
    "Colours": product_colours,
    "Prices": product_prices
})
print(df)
# Save the DataFrame to a CSV file
df.to_csv(r"E:/Sneha/Web Scrapping/NIke/nike_womens_shoes.csv", index=False)

#print("Data has been saved to nike_womens_shoes.csv")
