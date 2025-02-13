import time
import random
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

# Scrape the top 50 game names
game_elements = driver.find_elements(By.CLASS_NAME, "_1n_4-zvf0n4aqGEksbgW9N")
game_names = [game.text for game in game_elements[:50]]  # Get only top 50

# Debugging: print the extracted game names
print(game_names)

# Close the browser
driver.quit()

# Generate random prices and quantities for each game
games_data = []
for game in game_names:
    price = round(random.uniform(10, 100), 2)  # Random price between $10 and $100
    quantity = random.randint(1, 20)  # Random quantity between 1 and 20
    games_data.append({"name": game, "price": price, "quantity": quantity})

# Save to Excel
df = pd.DataFrame(games_data)
df.to_excel("games.xlsx", index=False, engine="openpyxl")

print("Scraping complete. Data saved to games.xlsx")
