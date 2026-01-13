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

# 自动下载并管理 ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://www.baidu.com")
print(driver.title)
driver.quit()