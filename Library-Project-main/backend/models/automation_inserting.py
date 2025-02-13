import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time

# Read the games from the Excel file
df = pd.read_excel('games2.xlsx')

# Setup Selenium WebDriver
driver = webdriver.Chrome()  # Make sure you have the ChromeDriver installed and in your PATH

# Open the index.html file
driver.get("file:///C:/Users/orons/Desktop/GamesShop/Library-Project-main/frontend/index.html")
time.sleep(5)
# Function to log in to the app
def login():
    try:
        phone_number = '0501234567'  # Example phone number
        password = 'pass'  # Example password
        driver.find_element(By.ID, 'phone').send_keys(phone_number)
        driver.find_element(By.ID, 'password').send_keys(password)
        driver.find_element(By.XPATH, '//button[text()="Login"]').click()

        # Wait for the main section to be visible after login
        WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, 'main-section')))
    except Exception as e:
        print(f"Error during login: {e}")

# Function to add a game to the system
def add_game(game_dict):
    try:
        WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.ID, 'game-name')))
        driver.find_element(By.ID, 'game-name').send_keys(game_dict['name'])
        driver.find_element(By.ID, 'game-price').send_keys(str(game_dict['price']))
        driver.find_element(By.ID, 'game-quantity').send_keys(str(game_dict['quantity']))
        driver.find_element(By.XPATH, '//button[text()="Add Game"]').click()

        # Wait for the game to be added
        WebDriverWait(driver, 3).until(ec.invisibility_of_element_located((By.XPATH, '//button[text()="Add Game"]')))
    except Exception as e:
        print(f"Error adding game {game_dict['name']}: {e}")

# Log in to the app
login()
time.sleep(5)

# Add all games to the system
for _, game in df.iterrows():
    add_game(game)

# Close the browser after adding all games
driver.quit()
