from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver. chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(ChromeDriverManager().install())


driver.get("https://www.baidu.com")
print(driver.title)
driver.quit()