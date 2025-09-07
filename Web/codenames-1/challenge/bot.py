#!/usr/bin/env python3
"""
Simple Selenium-based bot for joining and playing Codenames games.
Usage: python3 bot.py <GAME_CODE>
"""
import sys
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import random
import os
from shutil import which
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def main():
    if len(sys.argv) < 2:
        print("Usage: bot.py <GAME_CODE>")
        sys.exit(1)
    code = sys.argv[1].strip().upper()
    # Bot credentials
    username = f"BOT_{code}_" + os.urandom(4).hex()
    password = os.environ.get('BOT_SECRET_PREFIX', "") + os.urandom(16).hex()
    # Setup Selenium WebDriver (headless Chromium)
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    base_url = os.environ.get('BOT_BASE_URL', 'http://localhost:5000')
    try:
        # Register bot
        driver.get(f"{base_url}/register")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, 'username')))
        driver.find_element(By.NAME, 'username').send_keys(username)
        driver.find_element(By.NAME, 'password').send_keys(password)
        driver.find_element(By.CSS_SELECTOR, 'form button[type="submit"]').click()
    except Exception:
        # Ignore if already registered or page layout changed
        pass
    # Login if not redirected to lobby
    if '/lobby' not in driver.current_url:
        driver.get(f"{base_url}/login")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, 'username')))
        driver.find_element(By.NAME, 'username').send_keys(username)
        driver.find_element(By.NAME, 'password').send_keys(password)
        driver.find_element(By.CSS_SELECTOR, 'form button[type="submit"]').click()
        WebDriverWait(driver, 5).until(EC.url_contains('/lobby'))
    # Join the game
    join_url = f"{base_url}/join_game"
    driver.get(base_url + '/lobby')
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, 'code')))
    code_input = driver.find_element(By.NAME, 'code')
    code_input.clear()
    code_input.send_keys(code)
    driver.find_element(By.CSS_SELECTOR, 'form[action="/join_game"] button[type="submit"]').click()
    # Wait for game page
    WebDriverWait(driver, 20).until(EC.url_contains(f'/game/{code}'))
    # Main loop: give clues until game ends
    ctr = 0
    while True:
        # check for timeout
        if ctr > 30:
            print("quitting...")
            driver.quit()
            exit()
        # check for end-game alert
        try:
            alert = WebDriverWait(driver, 1).until(EC.alert_is_present())
            alert.accept()
            break
        except TimeoutException:
            pass
        # attempt to send a clue if form is available
        try:
            clue_box = driver.find_element(By.ID, 'clue_word')
            num_box = driver.find_element(By.ID, 'clue_num')
            send_btn = driver.find_element(By.ID, 'send_clue')
            if clue_box.is_displayed() and send_btn.is_enabled():
                # send arbitrary clue with random count 1-3
                clue_box.clear()
                clue_box.send_keys('potato')
                num = random.randint(1, 3)
                num_box.clear()
                num_box.send_keys(str(num))
                send_btn.click()
        except NoSuchElementException:
            pass
        time.sleep(1)
        ctr += 1
    driver.quit()

if __name__ == '__main__':
    main()
