import random
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from webdriver_manager.chrome import ChromeDriverManager

# Set up Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no browser window)
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Initialize WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open the Steam Charts page
url = "https://store.steampowered.com/charts/mostplayed/"
driver.get(url)

# Wait for the game list to be loaded (adjust the timeout if needed)
WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.CLASS_NAME, "_1n_4-zvf0n4aqGEksbgW9N")))

# Scrape the top 50 game names and their prices
game_elements = driver.find_elements(By.CLASS_NAME, "_1n_4-zvf0n4aqGEksbgW9N")
price_elements = driver.find_elements(By.CLASS_NAME, "_3j4dI1yA7cRfCvK8h406OB")

game_names = [game.text for game in game_elements[:50]]  # Get only top 50
game_prices = [price.text for price in price_elements[:50]]  # Get only top 50 prices

# Debugging: print the extracted game names and prices
for name, price in zip(game_names, game_prices):
    print(f"Game: {name}, Price: {price}")

# Close the browser
driver.quit()


# Function to convert price string to float
def convert_price(price_str):
    # Check if price is "Free To Play"
    if price_str == "Free To Play":
        return 0.0

    # Remove currency symbols (₪ or $) and commas, then convert to float
    price_str = price_str.replace("₪", "").replace("$", "").replace(",", "")

    # Handle cases where the price might contain non-numeric characters
    try:
        return float(price_str)
    except ValueError:
        return 0.0  # Return 0.0 if there's an issue with the conversion


# Generate game data with the actual price and a random quantity
games_data = []
for game, price in zip(game_names, game_prices):
    price_float = convert_price(price)  # Convert price to float
    quantity = random.randint(1, 20)  # Random quantity between 1 and 20
    games_data.append({"name": game, "price": price_float, "quantity": quantity})

# Save to Excel
df = pd.DataFrame(games_data)
df.to_excel("games.xlsx", index=False, engine="openpyxl")

print("Scraping complete. Data saved to games.xlsx")
