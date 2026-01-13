import time
import json
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def run_scraper():
    driver = None
    data_list = []
    
    try:
        print("🚀 启动爬虫...")
        driver = setup_driver()
        
        url = "https://www.zhihu.com/explore"
        driver.get(url)
        
        # 显式等待：直到页面中至少出现一个内容标题（最多等15秒）
        # Zhihu 的标题 class 通常包含 'ContentItem-title'
        print("⏳ 等待页面加载...")
        wait = WebDriverWait(driver, 15)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ContentItem-title")))
        
        # 模拟滚动，触发懒加载（如果需要更多数据，可以多滚动几次）
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3) 

        # 查找所有标题元素
        # 注意：知乎的前端代码经常变，如果这里抓不到，可能需要更新 Selector
        elements = driver.find_elements(By.CLASS_NAME, "ContentItem-title")
        
        print(f"✅ 找到 {len(elements)} 个内容标题。")
        
        for index, elem in enumerate(elements, 1):
            try:
                # 尝试获取标题内的链接，如果没有链接则获取文本
                link_elem = elem.find_element(By.TAG_NAME, "a")
                title = link_elem.text
                link = link_elem.get_attribute("href")
            except:
                # 备用方案
                title = elem.text
                link = "N/A"
            
            print(f"{index}. {title}")
            data_list.append({"title": title, "link": link})

    except Exception as e:
        print(f"❌ 发生错误: {e}")
        # 出错时保存截图，方便调试
        if driver:
            driver.save_screenshot("error_screenshot.png")
            
    finally:
        if driver:
            driver.quit()

    # --- 保存数据到文件 ---
    if data_list:
        # 保存为 JSON
        with open('zhihu_data.json', 'w', encoding='utf-8') as f:
            json.dump(data_list, f, ensure_ascii=False, indent=4)
        print("💾 数据已保存到 zhihu_data.json")
    else:
        print("⚠️ 未抓取到有效数据。")

if __name__ == "__main__":
    run_scraper()