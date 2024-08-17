from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time
from bs4 import BeautifulSoup
import pyperclip
import keyboard

def extract_image_url(google_maps_url, driver):
    driver.get(google_maps_url)
    
    # Use explicit wait instead of time.sleep(5)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'img'))
    )
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    for img_tag in soup.find_all('img'):
        img_src = img_tag.get('src')
        if img_src and 'googleusercontent.com' in img_src:
            large_img_src = re.sub(r'=w\d+-h\d+-k-no', '=w1600-h900-k-no', img_src)
            return large_img_src
    return None

def is_google_maps_place_url(url):
    return "https://www.google.com/maps/place/" in url

def process_clipboard(driver):
    current_copied_text = pyperclip.paste().strip()

    # Check if the clipboard content is a Google Maps place URL and not an image URL
    if current_copied_text and is_google_maps_place_url(current_copied_text):
        print(f'Processing Google Maps URL: {current_copied_text}')
        
        # Extract image URL
        img_url = extract_image_url(current_copied_text, driver)
        if img_url:
            pyperclip.copy(img_url)
            print(f'Image URL has been copied to clipboard: {img_url}')
        else:
            print('No image URL found.')
    else:
        print('The copied text is not a valid Google Maps place URL.')

def monitor_keyboard(driver):
    try:
        print("Press Ctrl+Shift+Q to process the current clipboard content.")
        while True:
            # Listen for the key combination
            if keyboard.is_pressed('ctrl+shift+q'):
                process_clipboard(driver)
                # To prevent multiple triggers, wait for the keys to be released
                while keyboard.is_pressed('ctrl+shift+q'):
                    time.sleep(0.1)
            time.sleep(0.1)  # Reduced sleep time to make the script more responsive
    except KeyboardInterrupt:
        print("\nExiting gracefully...")
    finally:
        driver.quit()

if __name__ == '__main__':
    # Set up the Selenium driver
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    # Update the path to where you have placed chromedriver
    service = Service('D:/Development/chromedriver-win64/chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)

    monitor_keyboard(driver)
