from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import random

# Set up Selenium WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://store.steampowered.com/charts/mostplayed/")
time.sleep(5)  # Wait for the page to load

# Scrape the top 50 game names
game_elements = driver.find_elements(By.CLASS_NAME, "weeklytopsellers_GameName_1n_4-")
game_names = [game.text for game in game_elements[:50]]

driver.quit()  # Close the browser

# Assign random prices and quantities
games_data = [
    {"Game Name": name, "Price": round(random.uniform(10, 100), 2), "Quantity": random.randint(1, 20)}
    for name in game_names
]

print(games_data)

# Save the game names, prices, and quantities to an Excel file
df = pd.DataFrame(games_data)
df.to_excel("games.xlsx", index=False)

print("games.xlsx file created successfully!")